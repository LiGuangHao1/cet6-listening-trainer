from __future__ import annotations
import re
from collections import defaultdict
from .models import ListeningItem, SpeakerTurn, Question, SourceBlock
from .layout_parser import classify_blocks
from .sentence_parser import split_sentences

MARKER = re.compile(r"^\s*\d+\s*-\s*([MW])\s*[:：]\s*(.*)$", re.I)
HEADING = re.compile(r"^\s*(conversation|passage|recording)\s+(one|two|three|1|2|3)\b", re.I)
PART = re.compile(r"part\s+ii|section\s+[abc]", re.I)
QUESTION_START = re.compile(r"^(?:q\s*\d+|\d+\s*[.)])\s*(.*)$", re.I)
OPTION = re.compile(r"^[A-D][.)]\s+(.*)$", re.I)
NUM = {"one": 1, "two": 2, "three": 3, "1": 1, "2": 2, "3": 3}


def _section_for(kind: str, count: int) -> str:
    return "A" if kind == "conversation" else "B" if kind == "passage" else "C"

def _clean_annotation_numbers(text: str) -> str:
    # Remove explicit bracketed/superscript cue markers, retaining spoken numbers.
    text = re.sub(r"\s*[\[［(（]\s*[²³¹⁴⁵⁶⁷⁸⁹]\s*[\]］)）]", "", text)
    text = re.sub(r"(?<!\w)[¹²³⁴⁵⁶⁷⁸⁹](?!\w)", "", text)
    return re.sub(r"\s{2,}", " ", text).strip()

def _heading_parts(blocks: list[SourceBlock]):
    found = []
    for i, b in enumerate(blocks):
        m = HEADING.match(b.text)
        if m:
            found.append((i, m.group(1).lower(), NUM[m.group(2).lower()], b))
    return found

def parse_document(blocks: list[SourceBlock]) -> list[ListeningItem]:
    blocks = classify_blocks(blocks)
    headings = _heading_parts(blocks)
    items: list[ListeningItem] = []
    counts = defaultdict(int)
    for hidx, (start, kind, ordinal, heading) in enumerate(headings):
        end = headings[hidx + 1][0] if hidx + 1 < len(headings) else len(blocks)
        segment = blocks[start + 1:end]
        counts[kind] += 1
        section = _section_for(kind, counts[kind])
        title = f"{kind.title()} {heading.text.split()[-1].title()}"
        turns: list[SpeakerTurn] = []
        current: SpeakerTurn | None = None
        transcript_blocks: list[SourceBlock] = []
        questions: list[Question] = []
        pending_question: Question | None = None
        for b in segment:
            text = _clean_annotation_numbers(b.text.strip())
            marker = MARKER.match(text) if kind == "conversation" else None
            if b.kind in {"header-footer", "chinese-analysis"}:
                continue
            qmatch = QUESTION_START.match(text)
            if qmatch or OPTION.match(text):
                if qmatch:
                    pending_question = Question(number=re.match(r"(?:q\s*)?(\d+)", text, re.I).group(1) if re.match(r"(?:q\s*)?(\d+)", text, re.I) else None, stem=qmatch.group(1).strip())
                    questions.append(pending_question)
                elif pending_question:
                    pending_question.options.append(OPTION.match(text).group(1).strip())
                continue
            if marker:
                if current:
                    turns.append(current)
                current = SpeakerTurn(speaker=marker.group(1).upper(), text=marker.group(2).strip(), source_page=b.page)
                if current.text:
                    transcript_blocks.append(b.model_copy(update={"text": current.text, "kind": "transcript", "reason": "speaker marker anchor"}))
                continue
            if kind == "conversation":
                if current and b.kind == "english":
                    current.text = f"{current.text} {text}".strip()
                    transcript_blocks.append(b.model_copy(update={"text": text, "kind": "transcript", "reason": "English continuation after speaker marker"}))
            elif b.kind == "english" and len(text.split()) >= 3:
                transcript_blocks.append(b.model_copy(update={"text": text, "kind": "transcript", "reason": "English candidate near item heading"}))
        if current:
            turns.append(current)
        if kind == "conversation":
            turns = [t for t in turns if t.text.strip()]
            transcript = "\n".join(f"{t.speaker}  {t.text}" for t in turns)
            sentences = []
            for idx, turn in enumerate(turns):
                sentences.extend(split_sentences(turn.text, turn.speaker, f"{ordinal}-{idx}"))
        else:
            transcript = " ".join(b.text for b in transcript_blocks)
            sentences = split_sentences(transcript, None, str(ordinal))
        pages = sorted({b.page for b in transcript_blocks})
        words = len(re.findall(r"\b[\w’'-]+\b", transcript))
        confidence = "high" if transcript and (len(turns) >= 2 if kind == "conversation" else len(transcript.split()) >= 3) else "low"
        if confidence == "high" and kind != "conversation" and words < 40:
            confidence = "medium"
        items.append(ListeningItem(id=f"{section.lower()}-{kind}-{ordinal}", section=section, type=kind, title=title, transcript=transcript, speaker_turns=turns, sentences=sentences, questions=questions, source_pages=pages, confidence=confidence, extraction_method="pdf-text", word_count=words, debug_blocks=segment, detected=bool(transcript), warning=None if transcript else "No reliable English transcript candidate was detected."))
    return items
