from __future__ import annotations
import re
from collections import Counter
from .models import SourceBlock

CJK = re.compile(r"[\u3400-\u9fff]")
QUESTION = re.compile(r"^(?:Q\s*\d+|\d+\s*[.)])\s*", re.I)
OPTION = re.compile(r"^[A-D][.)]\s+", re.I)
EXCLUSION = re.compile(r"录音分析|答案详解|问题分析|核心语义词|话语标记词|词汇|解析|参考答案")

def english_ratio(text: str) -> float:
    letters = sum(ch.isascii() and ch.isalpha() for ch in text)
    cjk = len(CJK.findall(text))
    return letters / max(1, letters + cjk)

def normalize_heading(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

def repeated_edge_text(blocks: list[SourceBlock]) -> set[str]:
    counts = Counter(b.text.strip() for b in blocks if b.text.strip())
    pages = max((b.page for b in blocks), default=0)
    return {text for text, count in counts.items() if count >= 3 and len(text) < 100} | {
        b.text.strip() for b in blocks if b.page and pages and (b.y0 < 45 or b.y1 > 780) and len(b.text) < 100
    }

def classify_blocks(blocks: list[SourceBlock]) -> list[SourceBlock]:
    repeated = repeated_edge_text(blocks)
    result = []
    for b in blocks:
        t = b.text.strip()
        low = normalize_heading(t)
        if t in repeated and len(t) < 100:
            b.kind, b.reason = "header-footer", "repeated edge text or page furniture"
        elif EXCLUSION.search(t) or CJK.search(t) and english_ratio(t) < 0.55:
            b.kind, b.reason = "chinese-analysis", "CJK-heavy analysis boundary"
        elif QUESTION.match(t) or OPTION.match(t) or re.match(r"^(?:question|questions)\b", low):
            b.kind, b.reason = "question", "question stem or answer option anchor"
        elif english_ratio(t) >= 0.62:
            b.kind, b.reason = "english", "English ratio and text shape"
        else:
            b.kind, b.reason = "unknown", "insufficient classification signal"
        result.append(b)
    return result
