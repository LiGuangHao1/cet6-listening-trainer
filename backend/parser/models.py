from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field

ExtractionMethod = Literal["pdf-text", "ocr", "mixed"]

class SourceBlock(BaseModel):
    text: str
    page: int
    x0: float
    y0: float
    x1: float
    y1: float
    font_size: float = 0
    kind: str = "unknown"
    reason: str = ""

class SpeakerTurn(BaseModel):
    speaker: Literal["M", "W"]
    text: str
    source_page: int

class Sentence(BaseModel):
    id: str
    text: str
    speaker: Literal["M", "W"] | None = None

class Question(BaseModel):
    number: str | None = None
    stem: str
    options: list[str] = Field(default_factory=list)

class ListeningItem(BaseModel):
    id: str
    section: Literal["A", "B", "C"]
    type: Literal["conversation", "passage", "recording"]
    title: str
    transcript: str
    speaker_turns: list[SpeakerTurn] = Field(default_factory=list)
    sentences: list[Sentence] = Field(default_factory=list)
    questions: list[Question] = Field(default_factory=list)
    source_pages: list[int] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"]
    extraction_method: ExtractionMethod
    word_count: int = 0
    debug_blocks: list[SourceBlock] = Field(default_factory=list)
    detected: bool = True
    warning: str | None = None

class ListeningDocument(BaseModel):
    title: str = "CET-6 Listening Practice"
    items: list[ListeningItem]
    source_filename: str | None = None
    warnings: list[str] = Field(default_factory=list)
