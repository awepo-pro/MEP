#!/usr/bin/env python3
"""
FastAPI web demo for MEMM Named Entity Recognition (Person Detection).
Run with: uvicorn app:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pickle, os
import config

# ── Try to import the MEMM class (must be in the same directory) ──────────────
try:
    from memm import MEMM          # adjust import name to match your file
    _memm_available = True
except ImportError:
    _memm_available = False

app = FastAPI(title="MEMM NER Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load model once at startup ─────────────────────────────────────────────────
memm: MEMM | None = None
model_error: str = ""

def load_memm():
    global memm, model_error
    if not _memm_available:
        model_error = "MEMM class not found – place memm.py (your MEMM source) next to app.py."
        return
    model_path = config.MODEL_PATH
    if not os.path.exists(model_path):
        model_error = f"Model file '{model_path}' not found. Train the model first."
        return
    try:
        m = MEMM()
        m.model_path = model_path
        m.load_model()
        memm = m
    except Exception as e:
        model_error = str(e)

load_memm()


# ── API ────────────────────────────────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    text: str

class Token(BaseModel):
    word: str
    label: str   # "PERSON" or "O"

class AnalyzeResponse(BaseModel):
    tokens: list[Token]
    error: str = ""

@app.get("/health")
def health():
    return {"ok": memm is not None, "error": model_error}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    if memm is None:
        return AnalyzeResponse(tokens=[], error=model_error or "Model not loaded.")

    import tempfile, os
    # analyze() reads from a file path, so we write text to a temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                     delete=False, encoding="utf-8") as tmp:
        tmp.write(req.text)
        tmp_path = tmp.name
    try:
        pairs = memm.analyze(tmp_path)          # [(word, label), ...]
        tokens = [Token(word=w, label=l) for w, l in pairs]
        return AnalyzeResponse(tokens=tokens)
    except Exception as e:
        return AnalyzeResponse(tokens=[], error=str(e))
    finally:
        os.unlink(tmp_path)


# ── Serve the frontend ─────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def index():
    return open("index.html", encoding="utf-8").read()
