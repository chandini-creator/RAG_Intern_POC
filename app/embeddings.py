"""
Local embedding model (sentence-transformers) for RAG.
No API keys; runs on CPU/GPU.
Uses project-local cache to avoid "Access denied" on user .cache.
"""
import os
from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings

from app.config import get_settings


def _embedding_cache_dir() -> str:
    """Cache dir inside project so we don't need write access to user .cache."""
    root = Path(__file__).resolve().parent.parent
    cache = root / ".cache" / "sentence_transformers"
    cache.mkdir(parents=True, exist_ok=True)
    return str(cache)


def _set_hf_cache_to_project():
    """Point all HuggingFace/transformers caches to project .cache to avoid Access denied."""
    root = Path(__file__).resolve().parent.parent
    hf_root = root / ".cache" / "huggingface"
    hub = hf_root / "hub"
    hf_root.mkdir(parents=True, exist_ok=True)
    hub.mkdir(parents=True, exist_ok=True)
    os.environ["HF_HOME"] = str(hf_root)
    os.environ["TRANSFORMERS_CACHE"] = str(hub)
    os.environ["HF_HUB_CACHE"] = str(hub)
    os.environ["SENTENCE_TRANSFORMERS_HOME"] = str(root / ".cache")


def get_embeddings() -> HuggingFaceEmbeddings:
    """Return HuggingFace embeddings singleton (model loaded once)."""
    _set_hf_cache_to_project()
    cache_dir = _embedding_cache_dir()
    settings = get_settings()
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        cache_folder=cache_dir,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
