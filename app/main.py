"""
FastAPI app: /health, /ask (RAG), /ingest, /ingest/upload.
RAG is local-only: Chroma + sentence-transformers + Ollama.
"""
import logging
import tempfile
import warnings

# Suppress LangChain HuggingFaceEmbeddings deprecation warning (we use community for compatibility)
warnings.filterwarnings("ignore", message=".*HuggingFaceEmbeddings.*deprecated.*", category=DeprecationWarning)
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Body, File, FastAPI, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse

from app.config import get_settings
from app.embeddings import _set_hf_cache_to_project
from app.logging_config import setup_logging
from app.models import AskRequest, AskResponse, HealthResponse, IngestRequest, IngestResponse

# Use project .cache for HuggingFace so we avoid "Access denied" on user .cache
_set_hf_cache_to_project()
# Setup logging before using it
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown: load config, log readiness."""
    settings = get_settings()
    logger.info("Starting %s (debug=%s)", settings.app_name, settings.debug)
    yield
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(
    title="GenAI RAG API",
    description="RAG over your docs: /health, /ask (drug questions), /ingest (add docs)",
    version="0.2.0",
    lifespan=lifespan,
)

@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """
    Health check for load balancers and monitoring.
    Async endpoint: use 'async def' for I/O-bound work later (DB, LLM calls).
    """
    settings = get_settings()
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version="0.1.0",
    )


@app.post("/ask", response_model=AskResponse)
async def ask(body: AskRequest) -> AskResponse:
    """
    RAG: retrieve relevant chunks from ingested docs, then answer with Ollama.
    Ingest docs first via POST /ingest.
    """
    logger.info("Ask received: question_len=%d", len(body.question))
    settings = get_settings()
    try:
        from app.rag import ask_rag

        answer = ask_rag(body.question)
        return AskResponse(
            answer=answer,
            question=body.question,
            model_used=settings.ollama_model,
        )
    except Exception as e:
        logger.exception("RAG error")
        raise HTTPException(status_code=503, detail=f"RAG failed: {str(e)}")


@app.post("/ingest", response_model=IngestResponse)
async def ingest(
    body: IngestRequest | None = Body(default=None),
    path: str | None = Query(None, description="Path to file or folder (use if no body)"),
) -> IngestResponse:
    """
    Ingest a file or directory into the vector store.
    Supports .pdf, .txt, .md. Path can be absolute or relative to project root.

    **Either** send a JSON body: `{"path": "sample_docs"}`
    **Or** use query: `?path=sample_docs` (no body needed).
    """
    path_str = (body.path if body else None) or path
    if not path_str or not path_str.strip():
        raise HTTPException(
            status_code=422,
            detail='Missing path. Send JSON body {"path": "sample_docs"} or query ?path=sample_docs',
        )
    project_root = Path(__file__).resolve().parent.parent
    path = Path(path_str.strip()).expanduser()
    if not path.is_absolute():
        path = (project_root / path).resolve()
    else:
        path = path.resolve()
    try:
        from app.ingest import ingest_documents

        n = ingest_documents(path)
        return IngestResponse(
            path=str(path),
            chunks_added=n,
            message=f"Ingested {n} chunks from {path}.",
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Ingest error")
        raise HTTPException(status_code=500, detail=str(e))


ALLOWED_UPLOAD_EXTENSIONS = {".pdf", ".txt", ".md", ".text"}


@app.post("/ingest/upload", response_model=IngestResponse)
async def ingest_upload(file: UploadFile = File(..., description="PDF, TXT, or MD file to ingest")) -> IngestResponse:
    """
    Upload a document to ingest into the vector store.
    Supports .pdf, .txt, .md. The file is saved temporarily, ingested, then removed.
    """
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_UPLOAD_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_UPLOAD_EXTENSIONS)}",
        )
    try:
        content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {e}")
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(content)
            temp_path = Path(tmp.name)
        from app.ingest import ingest_documents

        n = ingest_documents(temp_path)
        return IngestResponse(
            path=file.filename or temp_path.name,
            chunks_added=n,
            message=f"Ingested {n} chunks from uploaded file '{file.filename}'.",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Ingest upload error")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_path and temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass


# Optional: sync version for comparison (prefer async for I/O)
@app.get("/health/sync", response_model=HealthResponse)
def health_sync() -> HealthResponse:
    """Sync endpoint example — use async for production I/O."""
    settings = get_settings()
    return HealthResponse(status="ok", app_name=settings.app_name, version="0.1.0")


# Minimal web UI at /
static_dir = Path(__file__).resolve().parent.parent / "static"
index_path = static_dir / "index.html"


@app.get("/", include_in_schema=False)
def serve_ui():
    """Serve the minimal medical doc Q&A UI."""
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    raise HTTPException(status_code=404, detail="UI not found")
