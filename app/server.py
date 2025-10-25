from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from .retriever import retrieve
from .rerank import rerank
from .generate import generate_answer

app = FastAPI(title="Qdrant RAG Service with Perplexity Sonar")

class AskRequest(BaseModel):
    question: str
    top_k: int = 20
    top_n: int = 6
    score_threshold: float = 0.35
    # REMOVED source_filter field entirely

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskRequest):
    """Retrieve → Re-rank → Generate pipeline with Perplexity sonar-pro."""
    retrieved = retrieve(
        req.question,
        top_k=req.top_k,
        score_threshold=req.score_threshold
        # REMOVED source_filter argument
    )
    ranked = rerank(req.question, retrieved, top_n=req.top_n)
    result = generate_answer(req.question, ranked)
    
    return {
        "question": req.question,
        "answer": result["answer"],
        "citations": result["citations"],
        "diagnostics": {
            "retrieved": len(retrieved),
            "reranked": len(ranked)
        }
    }
