# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run the web app (development):**
```bash
uv run -m uvicorn app:app --reload
```

**Run the web app (production):**
```bash
uv run -m uvicorn app:app --host 127.0.0.1 --port 8000
```

**Build and run with Docker:**
```bash
docker build -t memm .
docker run -p 8000:8000 memm
```

**Install dependencies:**
```bash
uv sync
```

## Architecture

This project is a **Maximum Entropy Markov Model (MEMM) for Named Entity Recognition**, specifically person-name detection. It has two layers:

### Core ML (`memm.py`)
The `MEMM` class handles everything: feature extraction, training via NLTK's `MaxentClassifier`, and inference via **Viterbi decoding**. There are two feature functions:
- `features()` — original feature extractor with an `use_custom_features` toggle (used during training experiments)
- `features_best_model()` — static method with the full, fixed feature set; this is what `analyze()` and `_preprocess_data()` call at runtime

The `analyze(file_path)` method tokenizes text with NLTK's `word_tokenize`, runs Viterbi over the token sequence, and returns `[(word, label), ...]` where labels are `"O"` or `"PERSON"`.

Training data format: tab-separated `word\tlabel` per line, blank lines between sentences.

### Web API (`app.py`)
FastAPI app that loads the pickled model once at startup (`config.MODEL_PATH = models/9646-300iters.pkl`). Because `analyze()` reads from a file path, the `/analyze` endpoint writes the request text to a tempfile, calls `memm.analyze()`, then deletes it.

Endpoints:
- `GET /health` — returns model load status
- `POST /analyze` — accepts `{"text": "..."}`, returns `{"tokens": [{"word": ..., "label": ...}]}`
- `GET /` — serves `index.html`

### `archive/`
Original coursework (CISC3025 project 3) with a standalone CLI `main.py` for training and evaluation. Not used by the web app.
