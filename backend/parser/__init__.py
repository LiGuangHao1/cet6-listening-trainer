from .pdf_extractor import extract_blocks
from .transcript_parser import parse_document
from .models import ListeningDocument

def parse_pdf(data: bytes, filename: str | None = None) -> ListeningDocument:
    blocks = extract_blocks(data)
    items = parse_document(blocks)
    warnings = []
    if not blocks:
        warnings.append("No selectable text was found in this PDF. It may be a scanned/image-only PDF and needs OCR.")
    elif not items:
        warnings.append("Text was found, but no Conversation/Passage/Recording headings matched. This PDF layout needs parser tuning or manual text entry.")
    expected = {"conversation": 2, "passage": 2, "recording": 3}
    for kind, count in expected.items():
        actual = sum(i.type == kind and i.detected for i in items)
        if actual < count:
            warnings.append(f"{kind.title()}: detected {actual} of {count}; review or paste missing text.")
    return ListeningDocument(items=items, source_filename=filename, warnings=warnings)
