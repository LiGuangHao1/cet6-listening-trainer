from backend.parser.models import SourceBlock
from backend.parser.transcript_parser import parse_document

def b(text, page=1, kind="english", y=100):
    return SourceBlock(text=text, page=page, x0=0, y0=y, x1=500, y1=y+18, font_size=12, kind=kind)

def test_conversation_skips_chinese_analysis_and_keeps_turns():
    items = parse_document([b("Conversation One"), b("1-M: Hello, how are you?"), b("录音分析：中文说明", kind="chinese-analysis"), b("2-W: I am fine. Nice to see you."), b("1. What happened?", kind="question")])
    assert len(items) == 1
    assert [t.speaker for t in items[0].speaker_turns] == ["M", "W"]
    assert "录音分析" not in items[0].transcript
    assert "What happened" not in items[0].transcript

def test_conversation_can_cross_page_and_strip_marker():
    items = parse_document([b("Conversation Two", 1), b("1-M: It costs $20.", 1), b("2-W: I worked there for 3 years in 2025.", 2)])
    assert items[0].source_pages == [1, 2]
    assert items[0].speaker_turns[0].text == "It costs $20."
    assert "2025" in items[0].transcript

def test_questions_do_not_enter_passage():
    items = parse_document([b("Passage One"), b("The city opened a new museum last year."), b("Q1: Why did it open?", kind="question"), b("A) For tourism", kind="question")])
    assert "Why did" not in items[0].transcript
    assert items[0].questions[0].options == ["For tourism"]

def test_cue_numbers_removed_but_spoken_numbers_remain():
    items = parse_document([b("Recording One"), b("I would agree, yes. [²] It costs $20 in 2025.")])
    assert "[²]" not in items[0].transcript
    assert "$20" in items[0].transcript and "2025" in items[0].transcript
