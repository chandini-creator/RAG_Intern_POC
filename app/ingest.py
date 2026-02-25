"""
Ingestion pipeline: load docs → chunk → embed → store in Chroma.
"""
import logging
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings
from app.vectorstore import get_vectorstore

logger = logging.getLogger(__name__)


def _load_file(path: Path) -> List[Document]:
    """Load a single file (PDF or TXT) into LangChain documents."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        loader = PyPDFLoader(str(path))
        return loader.load()
    if suffix in (".txt", ".text", ".md"):
        loader = TextLoader(str(path), encoding="utf-8", autodetect_encoding=True)
        return loader.load()
    raise ValueError(f"Unsupported file type: {suffix}")


def _load_directory(dir_path: Path) -> List[Document]:
    """Load all PDF and TXT files from a directory."""
    docs: List[Document] = []
    for ext in ("*.pdf", "*.txt", "*.md"):
        for path in dir_path.glob(ext):
            try:
                docs.extend(_load_file(path))
            except Exception as e:
                logger.warning("Skip %s: %s", path, e)
    return docs


def chunk_documents(documents: List[Document]) -> List[Document]:
    """Split documents into chunks with overlap."""
    settings = get_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)


def ingest_documents(path: str | Path) -> int:
    """
    Ingest a file or directory into the vector store.
    Returns number of chunks added.
    """
    path = Path(path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")

    if path.is_file():
        raw_docs = _load_file(path)
    else:
        raw_docs = _load_directory(path)

    if not raw_docs:
        return 0

    chunks = chunk_documents(raw_docs)
    # Add source metadata for filtering / citations
    for i, doc in enumerate(chunks):
        if not doc.metadata.get("source"):
            doc.metadata["source"] = str(path)

    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)
    logger.info("Ingested %d chunks from %s", len(chunks), path)
    return len(chunks)
