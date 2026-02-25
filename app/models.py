"""
Pydantic models for request/response JSON.
Teaches: type-safe API contracts, validation, serialization.
"""
from pydantic import BaseModel, Field


# --- Health ---
class HealthResponse(BaseModel):
    """Response for GET /health."""

    status: str = Field(description="Service status")
    app_name: str = Field(description="Application name")
    version: str = Field(default="0.1.0", description="API version")


# --- Ask (placeholder for later RAG/LLM) ---
class AskRequest(BaseModel):
    """Request body for POST /ask."""

    question: str = Field(..., min_length=1, max_length=2000, description="User question")
    context: str | None = Field(default=None, max_length=10000, description="Optional context (e.g. for RAG)")


class AskResponse(BaseModel):
    """Response body for POST /ask."""

    answer: str = Field(description="Generated or placeholder answer")
    question: str = Field(description="Echo of the question")
    model_used: str = Field(default="placeholder", description="Model identifier (for later phases)")
    sources: list[str] = Field(default_factory=list, description="Source doc identifiers when using RAG")


# --- Ingest ---
class IngestRequest(BaseModel):
    """Request body for POST /ingest. Path to a file or folder (absolute or relative to project)."""

    path: str = Field(..., min_length=1, description="File or directory path to ingest (e.g. ./sample_docs or C:\\data\\drugs.pdf)")


class IngestResponse(BaseModel):
    """Response body for POST /ingest."""

    path: str = Field(description="Path that was ingested")
    chunks_added: int = Field(description="Number of chunks added to the vector store")
    message: str = Field(description="Status message")
