from typing import List, Dict, Any
from openai import OpenAI
from .config import PERPLEXITY_API_KEY, PERPLEXITY_MODEL, PERPLEXITY_BASE_URL

def _perplexity_client() -> OpenAI:
    return OpenAI(
        api_key=PERPLEXITY_API_KEY,
        base_url=PERPLEXITY_BASE_URL
    )

def _format_context(chunks: List[Dict[str, Any]]) -> str:
    # For LLM grounding, include metadata for retrieval traceability
    parts = []
    for c in chunks:
        did = c.get("doc_id", "unknown")
        page = c.get("page", "unknown")
        parts.append(f"[doc_id={did} page={page}]\n{c['text']}")
    return "\n\n---\n\n".join(parts)

def generate_answer(question: str, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not chunks:
        return {
            "answer": "No sufficient context found to answer the question.",
            "citations": []
        }

    context = _format_context(chunks)
    
    # Prepare citation metadata for the response
    citation_meta = []
    for idx, c in enumerate(chunks, start=1):
        citation_meta.append({
            "ref": f"[{idx}]",
            "doc_id": c.get("doc_id"),
            "page": c.get("page"),
            "source_filename": c.get("source_filename"),
            "vector_score": c.get("vector_score"),
            "rerank_score": c.get("rerank_score"),
        })

    system_prompt = (
        "You are a tax assistant providing accurate information about Irish taxes. "
        "Answer STRICTLY from the provided context only.\n\n"
        "IMPORTANT CITATION RULES:\n"
        "- Each citation reference [1], [2], [3] etc. corresponds to a chunk in the context\n"
        "- Cite each chunk's number ONLY ONCE per sentence where it's relevant\n"
        "- Do NOT repeat the same citation numbers within one sentence\n"
        "- Place citations at the END of sentences that reference that information\n"
        "- Only cite chunks that actually support the statement you're making\n\n"
        "GOOD example: 'PAYE is a tax system used in Ireland[1][2] where employers deduct tax[3].'\n"
        "BAD example: 'PAYE[1][2][3][4][5][6] is a tax system[1][2][3][4][5][6] used in Ireland[1][2][3][4][5][6].'\n\n"
        "If the context doesn't contain sufficient information, say 'I don't know.'"
    )

    messages = [
        {"role": "system", "content": f"{system_prompt}\n\nContext:\n{context}"},
        {"role": "user", "content": question},
    ]

    client = _perplexity_client()
    response = client.chat.completions.create(
        model=PERPLEXITY_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=2000,
    )
    llm_answer = response.choices[0].message.content

    # Return the LLM's answer directly without post-processing citations
    # The LLM has been instructed to cite properly, so we trust its output
    # We return all citation metadata so users can see what sources were used
    return {
        "answer": llm_answer,
        "citations": citation_meta
    }
