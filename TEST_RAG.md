# How to test the RAG app

Do these in order. The server must be running (`python run.py` or `.\run_app.ps1`).

---

## 1. Health check (server is up)

**Browser:** Open http://localhost:8000/health  

**Or PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```

**Success:** You see `{"status":"ok","app_name":"GenAI-RAG-Phase1","version":"0.1.0"}`

---

## 2. Ingest docs (add content so RAG has something to search)

### Option A – Upload a file (recommended)

**Using Swagger UI:**  
1. Open http://localhost:8000/docs  
2. Click **POST /ingest/upload** → Try it out  
3. Click **Choose File** and select a PDF, TXT, or MD file from your computer  
4. Execute  

**Success:** Response like `{"path":"yourfile.pdf","chunks_added":5,"message":"Ingested 5 chunks..."}`  

### Option B – Ingest from server path

**Query param:** `POST` http://localhost:8000/ingest?path=sample_docs (no body).  

**JSON body:** `POST` http://localhost:8000/ingest with body `{"path": "sample_docs"}`.  

**Success:** Same as above.  

**Note:** First ingest can take 1–2 minutes while the embedding model downloads into `.cache/` in the project.

---

## 3. Ask a question (RAG + Ollama)

**Request:**  
`POST` http://localhost:8000/ask  
Body (raw JSON): `{"question": "What is the dosing for aspirin?"}`  
Header: `Content-Type: application/json`

**Using Swagger UI:**  
1. Open http://localhost:8000/docs  
2. Click **POST /ask** → Try it out  
3. Request body: `{"question": "What is the dosing for aspirin?"}`  
4. Execute  

**Success:** You get an `answer` that uses the ingested drug info (e.g. aspirin dosing from `sample_docs`).  

**Requirement:** Ollama must be running and a model pulled (e.g. `ollama run llama3.2`). If Ollama isn’t running, you’ll get a connection error.

---

## Quick checklist

| Step | What to do | Success |
|------|------------|--------|
| 1 | GET /health | `status: "ok"` |
| 2 | POST /ingest with path `sample_docs` | `chunks_added` > 0 |
| 3 | POST /ask with a drug question | Answer refers to your docs (e.g. aspirin dosing) |

---

## If ingest fails with “Can’t load the model”

The embedding model (`sentence-transformers/all-MiniLM-L6-v2`) is downloaded on first use. Ensure:

1. You have internet access (model downloads from Hugging Face).
2. The project folder (or `.\\.cache`) is writable.
3. Run ingest again; the first run may take 1–2 minutes while the model downloads.

To pre-download the model in Python:
```powershell
& "$env:LOCALAPPDATA\GenAI-venv\Scripts\python.exe" -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', cache_folder='.cache/sentence_transformers')"
```
