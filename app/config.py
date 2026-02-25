"""
Configuration via environment variables.
Uses pydantic-settings to load from .env and validate types.
"""
import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def _env_path() -> Path:
    """Resolve .env from project root (parent of app/)."""
    return Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    """App settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=_env_path(),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "GenAI-RAG-Phase1"
    debug: bool = False
    log_level: str = "INFO"

    # RAG (local-only)
    chroma_persist_dir: str = "chroma_db"
    chroma_collection_name: str = "drug_docs"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ollama_model: str = "llama3.2"
    ollama_base_url: str = "http://localhost:11434"
    chunk_size: int = 600
    chunk_overlap: int = 100
    retrieve_top_k: int = 4


def get_settings() -> Settings:
    """Return validated settings (singleton-style usage)."""
    return Settings()
