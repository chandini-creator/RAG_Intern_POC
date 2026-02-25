# MediQuery — Ask questions about your documents

This is a small app that lets you upload documents (like drug info or medical notes) and then ask questions in plain language. The answers come from your own documents, not from the internet. Everything runs on your computer. No API keys needed.

---

## What you can do

- **Upload** PDFs or text files (or point the app to a folder).
- **Ask** things like “What is the dosing for aspirin?” or “What are the warnings for ibuprofen?”
- **Get answers** that are pulled from the text you uploaded. The app finds the relevant bits and uses a local AI model (Ollama) to write a short answer based only on that text.

So your documents become a small searchable knowledge base. The AI is told to stick to what you provided, which helps keep answers accurate and reduces made-up information.

---

## What you need

- **Python** (around 3.10 or newer).
- **Ollama** — a free app that runs AI models on your machine. Install it from [ollama.com](https://ollama.com), then in a terminal run: `ollama pull llama3.2` (one time). That downloads the model the app uses by default.

---

## How to run the app

1. **Install Python dependencies**  
   Open a terminal in this folder and run:
   ```powershell
   pip install -r requirements.txt
   ```
   If you prefer a virtual environment, create one first (`python -m venv .venv`, then activate it) and then run the same command.

2. **Start the server**  
   Easiest on Windows: double-click **`START_SERVER.bat`**. It will free port 8000 if something is already using it, then start the app. Keep that window open while you use the app.  
   Or from the terminal:
   ```powershell
   python run.py
   ```
   If you use the script that puts the virtual environment in AppData: `.\run_app.ps1`

3. **Open the app**  
   In your browser go to: **http://localhost:8000**  
   You’ll see a simple page where you can upload a file and type questions.

4. **Try it**  
   Upload a PDF or text file (there’s also a `sample_docs` folder with example text). Then ask something that the document can answer. The first time you ask, the app may take a moment to load the embedding model.

---

## Using the API

If you want to call the app from code or another tool:

- **Health check:** `GET http://localhost:8000/health`
- **Upload a document:** `POST http://localhost:8000/ingest/upload` with the file in a form field named `file`
- **Ingest from a path:** `POST http://localhost:8000/ingest` with body `{"path": "sample_docs"}` or query `?path=sample_docs`
- **Ask a question:** `POST http://localhost:8000/ask` with body `{"question": "Your question here"}`

Interactive API docs: **http://localhost:8000/docs**

---

## How it works (in short)

1. **When you add documents**  
   The app reads the file(s), splits the text into small chunks, turns each chunk into a numeric vector (embedding), and stores those in memory. So it’s not storing the raw file on disk; it keeps a searchable index in RAM.

2. **When you ask a question**  
   Your question is turned into a vector too. The app finds the chunks whose vectors are closest to the question (that’s the “retrieval” part). Those chunks are sent to the local LLM (Ollama) as context, plus your question. The LLM is instructed to answer only from that context. Its reply is what you see.

3. **Why “RAG”?**  
   This pattern is called Retrieval-Augmented Generation: you *retrieve* relevant pieces of your data, then *generate* an answer using those pieces. It’s a common way to build Q&A over your own docs without fine-tuning a model.

**Note:** The index is in memory only. When you stop the server, it’s cleared. Next time you start, you need to upload or ingest your documents again.

---

## Tech used

- **FastAPI** for the web API and serving the UI.
- **LangChain** for loading documents, splitting text, and talking to the LLM.
- **sentence-transformers** for embeddings (runs locally, no key).
- **Ollama** for the language model (e.g. Llama 3.2), also local.

So: Python, FastAPI, LangChain, a local embedding model, and Ollama. All on your machine.

---

## Tweaking behaviour

You can set these in a `.env` file (copy from `.env.example`) or as environment variables:

- **OLLAMA_MODEL** — which model to use (default: `llama3.2`)
- **OLLAMA_BASE_URL** — where Ollama is running (default: `http://localhost:11434`)
- **CHUNK_SIZE** / **CHUNK_OVERLAP** — how the app splits documents (defaults: 600 and 100)
- **RETRIEVE_TOP_K** — how many chunks to use per question (default: 4)

---

## Learning more

For a full walkthrough of the project — what each file does, how it fits the RAG flow, and how it matches common learning objectives — see **`docs/LEARNING_GUIDE.md`**.
