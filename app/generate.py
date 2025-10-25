from typing import List, Dict, Any
from openai import OpenAI
from .config import PERPLEXITY_API_KEY, PERPLEXITY_MODEL, PERPLEXITY_BASE_URL

def _perplexity_client() -> OpenAI:
    """OpenAI-compatible client pointing to Perplexity Sonar API."""
    return OpenAI(
        api_key=PERPLEXITY_API_KEY,
        base_url=PERPLEXITY_BASE_URL
    )

def _format_context(chunks: List[Dict[str, Any]]) -> str:
    """Format reranked chunks into a grounded context block with metadata."""
    parts = []
    for c in chunks:
        did = c.get("doc_id", "unknown")
        page = c.get("page", "unknown")
        parts.append(f"[doc_id={did} page={page}]\n{c['text']}")
    return "\n\n---\n\n".join(parts)

def _format_citations(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract citation metadata from reranked chunks."""
    cites = []
    for c in chunks:
        cites.append({
            "doc_id": c.get("doc_id"),
            "page": c.get("page"),
            "source_filename": c.get("source_filename"),
            "vector_score": c.get("vector_score"),
            "rerank_score": c.get("rerank_score"),
        })
    return cites

def generate_answer(question: str, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a grounded answer using Perplexity sonar-pro with reranked context."""
    if not chunks:
        return {
            "answer": "No sufficient context found to answer the question.",
            "citations": []
        }

    ctx = _format_context(chunks)
    system_prompt = (
        "You are a helpful assistant that answers STRICTLY from the provided context. "
        "If the context is insufficient to answer the question, say you don't know. "
        "Include inline citations in the format [doc_id:page] when referencing specific information."
    )
    
    messages = [
        {"role": "system", "content": f"{system_prompt}\n\nContext:\n{ctx}"},
        {"role": "user", "content": question},
    ]
    
    client = _perplexity_client()
    response = client.chat.completions.create(
        model=PERPLEXITY_MODEL,
        messages=messages,
        temperature=0.2,  # Lower for more focused answers
        max_tokens=2048   # Adjust based on your needs
    )
    
    answer = response.choices[0].message.content
    
    return {
        "answer": answer,
        "citations": _format_citations(chunks)
    }
