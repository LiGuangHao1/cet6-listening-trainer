from __future__ import annotations
import re
from .models import Sentence

_ABBREVIATIONS = re.compile(r"\b(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|etc|e\.g|i\.e)\.$", re.I)

def split_sentences(text: str, speaker: str | None = None, prefix: str = "s") -> list[Sentence]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    pieces: list[str] = []
    start = 0
    quote = False
    for i, ch in enumerate(text):
        if ch in '"\'':
            quote = not quote
        if ch not in ".?!" or quote:
            continue
        candidate = text[start:i + 1].strip()
        if _ABBREVIATIONS.search(candidate.split()[-1] if candidate.split() else ""):
            continue
        if i + 1 < len(text) and text[i + 1].isalnum():
            continue
        pieces.append(candidate)
        start = i + 1
    tail = text[start:].strip()
    if tail:
        pieces.append(tail)
    return [Sentence(id=f"{prefix}-{i}", text=p, speaker=speaker) for i, p in enumerate(pieces) if p]
