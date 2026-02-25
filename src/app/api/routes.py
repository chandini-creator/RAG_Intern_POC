from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AskRequest(BaseModel):
    question: str

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/ask")
def ask(payload: AskRequest):
    # For Day-1: return a dummy response
    return {
        "question": payload.question,
        "answer": "Dummy answer (Day-1). Next we will connect an LLM + RAG.",
    }