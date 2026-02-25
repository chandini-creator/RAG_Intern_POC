# Complete Learning Guide — GenAI RAG Project (MediQuery)

This document explains **everything** in this project: what it does, what technologies are used, how the pieces connect, and how it meets the internship/curriculum criteria. Use it to understand the system end-to-end.

---

## 1. What This Project Is

**MediQuery** is a **RAG (Retrieval-Augmented Generation)** application for medical/drug documents:

- **Input:** You give it documents (PDF, TXT, MD) — e.g. drug monographs, guidelines.
- **Behaviour:** It reads and indexes them so it can **search by meaning**, not just keywords.
- **Output:** When a user asks a question (e.g. “What is the dosing for aspirin?”), the app finds the **relevant pieces** of your documents and asks a **local LLM (Ollama)** to answer **using only that context**.

So: **your docs become the knowledge base; the LLM only answers from what was retrieved.** That reduces hallucinations and keeps answers grounded.

**Deliverables you have:**

- A **FastAPI** app with `/health`, `/ask`, `/ingest`, `/ingest/upload`.
- **Upload** (file or path) → **ingest** (load, chunk, embed, store) → **ask** (retrieve, then LLM).
- **Web UI** (MediQuery) to upload and ask in the browser.
- **Local-only:** embeddings (sentence-transformers) + vector store (in-memory) + LLM (Ollama). No cloud API keys.

---

## 2. How It Meets the Criteria (Phase 1 and Beyond)

### Phase 1: Core Foundations (Week 1)

| Criteria | Where in the project |
|----------|----------------------|
| **Virtual environments** | You use `.venv` or the AppData venv; `requirements.txt` and `run_app.ps1` / `activate_venv.ps1`. |
| **pip / Poetry** | `requirements.txt` for pip; `pyproject.toml` for optional Poetry. |
| **Async vs sync** | `/health` and `/ask` are `async def`; `/health/sync` exists as a sync example. |
| **REST APIs (FastAPI)** | `GET /health`, `POST /ask`, `POST /ingest`, `POST /ingest/upload` with clear request/response. |
| **JSON handling** | Pydantic models in `app/models.py`: `AskRequest`, `AskResponse`, `IngestRequest`, `IngestResponse`, `HealthResponse`. |
| **Logging** | `app/logging_config.py` sets up logging; `logger.info` in `main.py` and elsewhere. |
| **Environment variables** | `app/config.py` uses **pydantic-settings** to load `.env` and expose `Settings`. |
| **Deliverable: Simple FastAPI app with /ask and /health** | ✅ Implemented; plus `/ingest` and `/ingest/upload`. |

### Phase 2: Embeddings + Vector DBs (Week 2)

| Criteria | Where in the project |
|----------|----------------------|
| **What is an embedding?** | Used in `app/embeddings.py` and in the ingest/query flow; text → list of numbers (vector). |
| **Semantic similarity** | Retrieval in `app/vectorstore.py` uses **cosine similarity** between query and document vectors. |
| **Chunking strategies** | `app/ingest.py` uses **RecursiveCharacterTextSplitter** (chunk size/overlap in config). |
| **Why chunk size matters** | Config has `chunk_size` and `chunk_overlap`; smaller chunks = more precise retrieval, larger = more context per chunk. |
| **Vector store** | `app/vectorstore.py` implements an **in-memory** vector store (lists + cosine similarity). Conceptually same as Chroma/FAISS: store vectors, retrieve by similarity. |
| **Metadata** | LangChain `Document` objects carry metadata (e.g. source path); the vector store holds docs with content + metadata. |

### Phase 3: RAG Architecture (Week 3)

| Criteria | Where in the project |
|----------|----------------------|
| **Ingestion pipeline** | `app/ingest.py`: load file(s) → split into chunks → embed → add to vector store. |
| **Document loaders** | LangChain `PyPDFLoader` and `TextLoader` in `ingest.py`. |
| **Text splitters** | `RecursiveCharacterTextSplitter` with configurable `chunk_size` and `chunk_overlap`. |
| **Embedding pipeline** | `app/embeddings.py`: sentence-transformers model; used in ingest and in retrieval. |
| **Indexing** | Vector store’s `add_documents()`: each chunk is embedded and stored with the doc list. |
| **Retrieval** | Vector store’s `as_retriever()`: embed query → cosine similarity → return top-k chunks. |
| **Response synthesis** | `app/rag.py`: build a prompt with “Context: {chunks}” + “Question: {question}” → send to Ollama → return answer. |
| **RAG flow** | User question → embed → vector search → top-k chunks → prompt (context + question) → LLM → response. |

### Later Phases (LangChain, LangGraph, Memory, Evaluation)

- The project uses **LangChain** (prompts, document loaders, text splitters, embeddings, Ollama chat model). That aligns with Phase 4 (LangChain).
- **Structured output** is partially there: Pydantic for API request/response; you could add stricter JSON for the LLM later.
- **LangGraph, agent memory, evaluation** are not implemented yet; see `docs/CURRICULUM_MAPPING.md` for what to add.

---

## 3. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         INGESTION (when you add docs)                     │
│                                                                          │
│  File (PDF/TXT/MD)  →  Load (PyPDF/TextLoader)  →  Chunk (RecursiveSplitter) │
│       →  Embed (sentence-transformers)  →  Store (in-memory vector store)   │
└─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Vector store: list of (document_chunk, embedding_vector)                │
│  Retrieval = embed query → cosine similarity → top-k chunks                │
└─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         QUERY (when user asks)                            │
│                                                                          │
│  User question  →  Embed same model  →  Retrieve top-k chunks             │
│       →  Build prompt: "Context: {chunks}\nQuestion: {question}"          │
│       →  Ollama (LLM)  →  Answer (only from context)                       │
└─────────────────────────────────────────────────────────────────────────┘
```

**Why RAG reduces hallucinations:** The LLM is instructed to answer **only** from the provided context. So the answer is grounded in your documents instead of the model’s training data.

---

## 4. Tech Stack and Why

| Component | Technology | Why |
|-----------|------------|-----|
| **API** | FastAPI | Async, automatic OpenAPI docs, Pydantic integration, simple to extend. |
| **Config** | pydantic-settings + .env | Type-safe config, no hardcoded secrets, 12-factor style. |
| **Documents** | LangChain loaders (PyPDF, TextLoader) | Standard way to load PDF/TXT/MD into LangChain `Document` objects. |
| **Chunking** | LangChain RecursiveCharacterTextSplitter | Splits by paragraphs/sentences/words; configurable size and overlap. |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) | Runs locally, no API key, good quality for semantic search. |
| **Vector store** | In-memory (Python lists + cosine similarity) | No extra process or DB; simple and portable. (Chroma was replaced for compatibility.) |
| **LLM** | Ollama (e.g. llama3.2) | Local, no API key, same interface as cloud LLMs for learning. |
| **Orchestration** | LangChain (prompts, Ollama) | Clean prompt templates and model invocation. |
| **Front end** | Single HTML (static/index.html) | No build step; upload + ask form; calls same API. |

---

## 5. File-by-File Explanation

### Root / scripts

- **`run.py`** — Entry point: loads settings and runs **uvicorn** with `app.main:app`. You run the server with `python run.py`.
- **`requirements.txt`** — Python dependencies (FastAPI, uvicorn, pydantic, LangChain, sentence-transformers, pypdf, etc.).
- **`pyproject.toml`** — Optional Poetry config; same project metadata and dependency intent.
- **`START_SERVER.bat`** — Stops any process on port 8000, then starts the app. Easiest way to run on Windows.
- **`run_app.ps1`** / **`activate_venv.ps1`** — Use the venv in AppData (handy when `.venv` in project fails, e.g. OneDrive).
- **`.env.example`** — Template for env vars; copy to `.env` and adjust (optional).

### `app/` — Core application

- **`app/main.py`**
  - Creates the **FastAPI** app and sets **lifespan** (startup/shutdown logging).
  - Calls `_set_hf_cache_to_project()` so HuggingFace/embedding cache stays under the project (avoids permission issues).
  - **Routes:**
    - `GET /health` — Returns status, app name, version (for monitoring).
    - `POST /ask` — Body: `{ "question": "..." }`. Calls `ask_rag()`, returns answer and `model_used`.
    - `POST /ingest` — Body `{ "path": "..." }` or query `?path=...`. Resolves path and calls `ingest_documents()`.
    - `POST /ingest/upload` — Multipart file upload; saves to temp file, runs same ingest, deletes temp file.
    - `GET /` — Serves the web UI (`static/index.html`).
  - Uses **Pydantic** models for request/response (from `app.models`).

- **`app/config.py`**
  - **pydantic-settings** `Settings` class: reads from `.env`, validates types.
  - Fields: `app_name`, `debug`, `log_level`, and RAG-related: `embedding_model`, `ollama_model`, `ollama_base_url`, `chunk_size`, `chunk_overlap`, `retrieve_top_k`, etc.
  - **Meets “environment variables”**: all config comes from env (or defaults).

- **`app/models.py`**
  - **Pydantic** models for API:
    - `HealthResponse`, `AskRequest`, `AskResponse`, `IngestRequest`, `IngestResponse`.
  - **Meets “JSON handling”**: type-safe request/response and validation (e.g. min/max length).

- **`app/logging_config.py`**
  - Sets up **logging** (level from config, format, stdout).
  - **Meets “logging”**: one place to configure and use `logger` across the app.

- **`app/embeddings.py`**
  - **Embeddings:** LangChain `HuggingFaceEmbeddings` with **sentence-transformers** (e.g. all-MiniLM-L6-v2).
  - **Cache:** `_embedding_cache_dir()` and `_set_hf_cache_to_project()` so all HuggingFace/transformers cache is under the project (avoids “Access denied” on user `.cache`).
  - Used by the vector store to **embed** document chunks and the user query.

- **`app/vectorstore.py`**
  - **SimpleVectorStore:** in-memory store:
    - `_docs`: list of LangChain `Document`.
    - `_vectors`: list of embedding vectors.
  - `add_documents(docs)` — Embeds each doc’s text and appends to `_docs` and `_vectors`.
  - `as_retriever(search_kwargs={"k": n})` — Returns a function that: embeds the query, computes **cosine similarity** with all stored vectors, returns top-k documents.
  - **Singleton:** `get_vectorstore()` returns one shared store for the process.

- **`app/ingest.py`**
  - **Load:** `_load_file()` uses PyPDFLoader or TextLoader by extension; `_load_directory()` globs PDF/TXT/MD and loads each.
  - **Chunk:** `chunk_documents()` uses **RecursiveCharacterTextSplitter** (size/overlap from config).
  - **Ingest:** `ingest_documents(path)` loads (file or dir), chunks, adds metadata (e.g. source), then `vectorstore.add_documents(chunks)`.
  - **Meets “ingestion pipeline”, “document loaders”, “text splitters”, “embedding pipeline”, “indexing”.**

- **`app/rag.py`**
  - **RAG prompt:** Template with placeholders `{context}` and `{question}`; instructs the LLM to answer only from context.
  - **ask_rag(question):**
    1. Get vector store and retriever (top-k from config).
    2. Retrieve chunks for the question.
    3. Format chunks into one “Context” string.
    4. Build messages from the prompt (context + question).
    5. Call **ChatOllama** (LangChain) with those messages.
    6. Return the LLM’s reply (e.g. `result.content`).
  - **Meets “retrieval”, “response synthesis”, “prompt engineering”, “LLM (Ollama)”.**

### `static/`

- **`static/index.html`** — MediQuery UI: upload area (drag-and-drop or file picker), question input, “Ask” button. Uses `fetch()` to call `POST /ingest/upload` and `POST /ask`. Medical-themed (teal, simple layout).

### `docs/`

- **`docs/CURRICULUM_MAPPING.md`** — Maps internship phases (2–7) and deliverables to this project and lists what’s missing (e.g. streaming, reranking, LangGraph).
- **`docs/LEARNING_GUIDE.md`** — This file.

### `sample_docs/`

- **`sample_docs/sample_drug_info.txt`** — Example text (e.g. aspirin, ibuprofen, acetaminophen) so you can ingest and ask without your own files.

---

## 6. Key Concepts in One Place

- **RAG (Retrieval-Augmented Generation):** Retrieve relevant chunks from your data, then generate an answer from those chunks with an LLM. Improves accuracy and reduces hallucinations for domain-specific Q&A.

- **Embedding:** A function that turns text into a fixed-size list of numbers (vector). Similar meaning → similar vectors. We use it for both document chunks and the user question.

- **Chunking:** Splitting long documents into smaller segments (e.g. 600 characters with 100 overlap). So retrieval can return the right “paragraph” instead of the whole doc.

- **Vector store:** A store that holds (document, vector) and supports “find documents whose vectors are most similar to this query vector.” Here we use in-memory lists + cosine similarity.

- **Cosine similarity:** Measure of similarity between two vectors (dot product / (norm product)). Used in `vectorstore.py` to rank chunks for the query.

- **Prompt engineering (here):** One prompt: “Context: … Question: … Answer only from context.” That’s the “system” instruction that keeps the LLM grounded.

- **Ollama:** Local server that runs open-weight LLMs (e.g. Llama). The app talks to it at `http://localhost:11434` via LangChain’s ChatOllama.

---

## 7. End-to-End Flows

### Ingest (add documents)

1. User uploads a file (UI) or calls `POST /ingest` with a path.
2. **main.py** receives the file or path; for upload, writes to a temp file.
3. **ingest.ingest_documents(path)** is called:
   - Load: PyPDFLoader or TextLoader → list of LangChain `Document`.
   - Chunk: RecursiveCharacterTextSplitter → list of smaller `Document`s.
   - Embed: `get_embeddings().embed_documents(texts)` → one vector per chunk.
   - Store: `get_vectorstore().add_documents(chunks)` → vectors and docs appended in memory.
4. Response: path, `chunks_added`, message.

### Ask (question → answer)

1. User types a question (UI) or calls `POST /ask` with `{ "question": "..." }`.
2. **main.py** calls **rag.ask_rag(question)**.
3. **rag.ask_rag**:
   - Gets vector store and retriever (top-k).
   - Retriever(question): embed question → cosine similarity with all chunk vectors → return top-k chunks.
   - Format chunks into a single “Context” string.
   - Build prompt: “Context: … Question: … Answer only from context.”
   - Call Ollama via LangChain → get reply text.
   - Return reply.
4. **main.py** returns `AskResponse(answer=..., question=..., model_used=...)`.

---

## 8. How to Extend (Curriculum and Beyond)

- **Phase 2 deliverables:** Add short docs on “What is an embedding?”, “Cosine similarity,” “Why RAG reduces hallucinations,” “Context window.”
- **Phase 3:** Add a one-page “RAG flow” diagram; document retrieval failure cases and how to improve recall/precision.
- **Phase 4:** Use more LangChain (e.g. LCEL chains, output parsers); document “Chain vs Agent,” “Memory vs Vector store.”
- **Phase 5:** Introduce LangGraph (e.g. retrieve → validate → generate); optional agent with tools.
- **Phase 6:** Add memory (e.g. conversation or user-scoped) and document when to use it.
- **Phase 7:** Add evaluation (e.g. faithfulness, relevance) and optional latency/token logging.

See **`docs/CURRICULUM_MAPPING.md`** for the full checklist and where each item is covered or missing.

---

## 9. Summary

- **What:** A local RAG app (MediQuery) for medical/drug docs: upload or path → ingest → ask questions → answers from your docs via Ollama.
- **How:** FastAPI + LangChain (loaders, splitters, embeddings, Ollama) + in-memory vector store (cosine similarity) + simple web UI.
- **Criteria:** Phase 1 (venv, pip, async, REST, JSON, logging, env) and Phase 2–3 (embeddings, chunking, vector store, RAG pipeline) are met in code and behaviour; later phases are partially covered or documented for extension.
- **Run:** `START_SERVER.bat` or `python run.py`; open http://localhost:8000; upload a doc, then ask.

This learning guide plus the code and `CURRICULUM_MAPPING.md` give you a full picture of what was built and how it fits the internship criteria.
