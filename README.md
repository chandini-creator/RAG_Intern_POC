# GenAI RAG — Drug-doc Q&A (local-only)

**RAG over your documents:** ingest PDF/TXT → ask questions (e.g. about drugs) → get answers from your docs using **Chroma** + **sentence-transformers** + **Ollama**. No API keys.

---

## Quick start

**Option A — If `python -m venv .venv` works (e.g. project not on OneDrive):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

**Option B — If venv fails (e.g. "Unable to copy" on OneDrive):**  
Use the venv in AppData and run the app in one step:

```powershell
.\run_app.ps1
```

Or activate that venv first, then run:

```powershell
.\activate_venv.ps1
python run.py
```

**2. Install Ollama (one-time)**  
Download [Ollama](https://ollama.com), then run: `ollama pull llama3.2`

**3. Ingest docs, then ask**  
- Ingest: `POST /ingest` body `{"path": "sample_docs"}`  
- Ask: `POST /ask` body `{"question": "What is the dosing for aspirin?"}`  

- **Web UI:** http://localhost:8000 — upload docs, ask questions (medical-themed)  
- **API docs:** http://localhost:8000/docs  
- **Health:** http://localhost:8000/health

---

## What the intern learns (Week 1)

| Topic | Where it’s used |
|--------|------------------|
| **Virtual environments** | `.venv` + `pip install -r requirements.txt` (or `poetry install`) |
| **pip / Poetry** | `requirements.txt` and optional `pyproject.toml` |
| **Async vs sync** | `/health` and `/ask` are `async def`; `/health/sync` is `def` for comparison |
| **REST APIs (FastAPI)** | `GET /health`, `POST /ask`, request/response models |
| **JSON handling** | Pydantic models in `app/models.py` — validation and serialization |
| **Logging** | `app/logging_config.py` + `logger.info(...)` in `app/main.py` |
| **Environment variables** | `app/config.py` with `pydantic-settings` and `.env` |

---

## Project layout

```
GenAI/
├── app/
│   ├── __init__.py
│   ├── config.py          # Settings (Chroma, Ollama, chunk size)
│   ├── embeddings.py      # Local embeddings (sentence-transformers)
│   ├── ingest.py          # Load docs → chunk → embed → Chroma
│   ├── logging_config.py
│   ├── main.py            # FastAPI: /health, /ask (RAG), /ingest
│   ├── models.py          # Request/response models
│   ├── rag.py             # RAG chain: retriever → prompt → Ollama
│   └── vectorstore.py     # Chroma (persist on disk)
├── sample_docs/            # Sample TXT to test ingest + ask
├── chroma_db/              # Vector DB (created on first ingest)
├── docs/                   # Curriculum and deliverable docs
├── requirements.txt
└── run.py
```

---

## API summary

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/ingest` | Body: `{"path": "sample_docs"}` or query `?path=...`. Index a file or folder from disk. |
| POST | `/ingest/upload` | **Upload a file** (PDF, TXT, MD). Form field: `file`. Indexes the uploaded doc. |
| POST | `/ask` | Body: `{"question": "..."}`. RAG: retrieve from Chroma → answer with Ollama. |

---

## Config (optional)

Set in `.env` or environment:

- `CHROMA_PERSIST_DIR` — default `chroma_db`
- `OLLAMA_MODEL` — default `llama3.2`
- `CHUNK_SIZE` / `CHUNK_OVERLAP` — splitting (default 600 / 100)
- `RETRIEVE_TOP_K` — chunks per query (default 4)
