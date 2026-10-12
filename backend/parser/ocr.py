"""Optional local OCR fallback.

OCR is deliberately optional because Windows needs the Tesseract executable and
language data installed separately. The normal PDF text layer remains preferred.
"""
from __future__ import annotations
from collections import defaultdict
import io
import os
import fitz
from .models import SourceBlock


def extract_ocr_blocks(data: bytes) -> list[SourceBlock]:
    try:
        from PIL import Image
        import pytesseract
        from pytesseract import Output
    except ImportError:
        return []
    doc = fitz.open(stream=data, filetype="pdf")
    result: list[SourceBlock] = []
    language = os.getenv("CET6_TESSERACT_LANG", "eng+chi_sim")
    for page_number, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        image = Image.open(io.BytesIO(pix.tobytes("png")))
        try:
            payload = pytesseract.image_to_data(image, lang=language, output_type=Output.DICT)
        except Exception:
            # English-only installations are common on Windows.
            payload = pytesseract.image_to_data(image, lang="eng", output_type=Output.DICT)
        lines: dict[tuple[int, int, int], list[tuple[str, float, float, float, float, float]]] = defaultdict(list)
        count = len(payload.get("text", []))
        for i in range(count):
            text = (payload["text"][i] or "").strip()
            confidence = float(payload.get("conf", ["-1"])[i])
            if not text or confidence < 20:
                continue
            key = (int(payload["block_num"][i]), int(payload["par_num"][i]), int(payload["line_num"][i]))
            lines[key].append((text, float(payload["left"][i]) / 2, float(payload["top"][i]) / 2, float(payload["width"][i]) / 2, float(payload["height"][i]) / 2, confidence))
        for words in lines.values():
            words.sort(key=lambda item: item[1])
            text = " ".join(item[0] for item in words).strip()
            if not text:
                continue
            x0 = min(item[1] for item in words)
            y0 = min(item[2] for item in words)
            x1 = max(item[1] + item[3] for item in words)
            y1 = max(item[2] + item[4] for item in words)
            result.append(SourceBlock(text=text, page=page_number, x0=x0, y0=y0, x1=x1, y1=y1, font_size=max(8.0, y1 - y0), kind="unknown", reason="local OCR line"))
    return result
