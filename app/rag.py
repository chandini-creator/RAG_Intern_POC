"""
RAG chain: retriever → prompt → Ollama. Local-only, no API keys.
"""
import logging
from typing import List

try:
    from langchain_ollama import ChatOllama
except ImportError:
    from langchain_community.chat_models import ChatOllama  # type: ignore

from langchain_core.prompts import ChatPromptTemplate

from app.config import get_settings
from app.vectorstore import get_vectorstore

logger = logging.getLogger(__name__)

RAG_PROMPT = """You are a helpful assistant that answers questions about drugs using only the provided context. If the context does not contain relevant information, say so. Do not make up information.

Context:
{context}

Question: {question}

Answer (based only on the context above):"""


def _format_docs(docs: List) -> str:
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def ask_rag(question: str) -> str:
    """Run RAG for one question. Returns answer string."""
    settings = get_settings()
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": settings.retrieve_top_k})
    docs = retriever(question)
    context = _format_docs(docs)

    llm = ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=0.2,
        num_predict=1024,
    )
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT)
    messages = prompt.format_messages(context=context, question=question)
    result = llm.invoke(messages)
    return getattr(result, "content", str(result))
