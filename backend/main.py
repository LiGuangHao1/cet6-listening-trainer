from __future__ import annotations
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .parser import parse_pdf

app = FastAPI(title="CET-6 Listening Trainer API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/parse")
async def parse(file: UploadFile = File(...)):
    if file.content_type != "application/pdf" and not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Please upload a PDF file.")
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="The uploaded PDF is empty.")
    try:
        return parse_pdf(data, file.filename)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"PDF parsing failed: {exc}") from exc
