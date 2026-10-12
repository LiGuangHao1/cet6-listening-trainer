# CET-6 Listening Trainer

A local Windows app for extracting CET-6 listening transcripts from PDFs and practicing with per-word masks. WorkAudioBook remains the external audio player.

## Run locally

### Backend

```powershell
cd C:\path\to\cet6-listening-trainer
py -3 -m venv backend\.venv
backend\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python -m uvicorn backend.main:app --reload --port 8000
```

### Frontend (new terminal)

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in Chrome or Edge. The PDF parser uses PyMuPDF text-layer extraction and retains block coordinates for debugging. OCR is reserved as an optional follow-up when a sample PDF has no usable text layer.

### Optional OCR fallback

If a PDF is image-only, install Tesseract OCR for Windows and the optional Python bridge:

```powershell
winget install UB-Mannheim.TesseractOCR
cd D:\path\to\cet6-listening-trainer
backend\.venv\Scripts\python.exe -m pip install -r backend\requirements-ocr.txt
```

Restart FastAPI after installing OCR. The parser still prefers a PDF text layer; OCR is used only when no selectable text is available. If the Chinese language pack is installed, `chi_sim` is used automatically; English-only Tesseract also works, with weaker Chinese-analysis filtering.
