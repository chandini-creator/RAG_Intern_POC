"""
Simple in-memory vector store for RAG (no external DB).
Avoids Chroma/pydantic/Python 3.14 compatibility issues.
"""
from typing import List, Dict, Any

from langchain_core.documents import Document

from app.config import get_settings
from app.embeddings import get_embeddings


class SimpleVectorStore:
    """Minimal vector store backed by Python lists and cosine similarity."""

    def __init__(self) -> None:
        self._docs: List[Document] = []
        self._vectors: List[List[float]] = []
        self._embeddings = get_embeddings()

    def add_documents(self, docs: List[Document]) -> None:
        if not docs:
            return
        texts = [d.page_content for d in docs]
        vectors = self._embeddings.embed_documents(texts)
        self._docs.extend(docs)
        self._vectors.extend(vectors)

    def as_retriever(self, search_kwargs: Dict[str, Any] | None = None):
        settings = get_settings()
        k = (search_kwargs or {}).get("k", settings.retrieve_top_k)

        def _retrieve(query: str) -> List[Document]:
            if not self._docs:
                return []
            q_vec = self._embeddings.embed_query(query)
            # Cosine similarity
            q_norm_sq = sum(q * q for q in q_vec) or 1e-9
            scores: List[tuple[float, int]] = []
            for i, v in enumerate(self._vectors):
                dot = sum(q * d for q, d in zip(q_vec, v))
                d_norm_sq = sum(d * d for d in v) or 1e-9
                sim = dot / ((q_norm_sq * d_norm_sq) ** 0.5)
                scores.append((sim, i))
            scores.sort(reverse=True, key=lambda x: x[0])
            top = scores[:k]
            return [self._docs[i] for _, i in top]

        return _retrieve


_STORE: SimpleVectorStore | None = None


def get_vectorstore() -> SimpleVectorStore:
    """Return singleton in-memory vector store."""
    global _STORE
    if _STORE is None:
        _STORE = SimpleVectorStore()
    return _STORE

