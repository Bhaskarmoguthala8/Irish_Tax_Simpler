import cohere
from typing import List, Dict, Any
from .config import COHERE_API_KEY

_co = cohere.Client(api_key=COHERE_API_KEY)

def rerank(
    query: str,
    docs: List[Dict[str, Any]],
    top_n: int = 6,
    model: str = "rerank-english-v3.0"
) -> List[Dict[str, Any]]:
    """Rerank retrieved candidates using Cohere cross-encoder."""
    if not docs:
        return []
    
    # Cohere rerank expects a list of strings or dicts with "text" key
    items = [d["text"] for d in docs]
    
    out = _co.rerank(
        query=query,
        documents=items,
        top_n=top_n,
        model=model,
        return_documents=False  # We already have the docs, just need scores
    )
    
    ranked: List[Dict[str, Any]] = []
    for r in out.results:
        # Use r.index to map back to original docs
        idx = r.index
        ranked.append({
            **docs[idx],
            "rerank_score": r.relevance_score
        })
    return ranked
