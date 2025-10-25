from typing import Optional, List, Dict, Any
from qdrant_client import QdrantClient
from .embeddings import embed_query
from .config import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION

_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=30)

def retrieve(
    question: str,
    top_k: int = 20,
    score_threshold: Optional[float] = 0.35
    # REMOVED source_filter parameter entirely
) -> List[Dict[str, Any]]:
    """Query Qdrant for relevant chunks with score threshold."""
    qvec = embed_query(question)

    res = _client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=qvec,
        limit=top_k,
        score_threshold=score_threshold,
        with_payload=True
        # REMOVED query_filter argument entirely
    )
    
    docs: List[Dict[str, Any]] = []
    for p in res.points:
        if p.payload and "text" in p.payload:
            docs.append({
                "text": p.payload.get("text"),
                "doc_id": p.payload.get("doc_id"),
                "page": p.payload.get("page"),
                "source_filename": p.payload.get("source_filename"),
                "vector_score": p.score
            })
    return docs
