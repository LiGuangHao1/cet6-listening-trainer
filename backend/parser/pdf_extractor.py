from __future__ import annotations
import fitz
from .models import SourceBlock


def extract_blocks(data: bytes) -> list[SourceBlock]:
    """Extract line-level blocks while retaining geometry and font information."""
    doc = fitz.open(stream=data, filetype="pdf")
    blocks: list[SourceBlock] = []
    for page_index, page in enumerate(doc):
        payload = page.get_text("dict")
        for raw_block in payload.get("blocks", []):
            if raw_block.get("type") != 0:
                continue
            for line in raw_block.get("lines", []):
                spans = line.get("spans", [])
                text = "".join(span.get("text", "") for span in spans).strip()
                if not text:
                    continue
                rect = line.get("bbox", (0, 0, 0, 0))
                sizes = [float(s.get("size", 0)) for s in spans if s.get("size")]
                blocks.append(SourceBlock(text=text, page=page_index + 1, x0=rect[0], y0=rect[1], x1=rect[2], y1=rect[3], font_size=sum(sizes) / len(sizes) if sizes else 0))
    return blocks
