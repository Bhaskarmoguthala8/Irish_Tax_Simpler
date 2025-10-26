import re
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

def _generate_citation_map(chunks: List[Dict[str, Any]]) -> Dict[str, str]:
    # Assign [1], [2], ... for each chunk
    mapping = {}
    for idx, c in enumerate(chunks, start=1):
        key = (c.get("doc_id"), c.get("page"))
        mapping[key] = f"[{idx}]"
    return mapping

def _sentence_split(text: str) -> List[str]:
    # Split the answer into clean sentences for citation injection
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]

def generate_answer(question: str, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not chunks:
        return {
            "answer": "No sufficient context found to answer the question.",
            "citations": []
        }

    context = _format_context(chunks)
    citation_map = _generate_citation_map(chunks)
    # Prepare metadata for the answer JSON
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
        "You are a tax assistant. Answer only from the provided context."
         "For every fact or definition, place any supporting citation numbers ([1], [2], etc.) "
         "at the end of each sentence. Cite only the numbers whose context actually supports the statement."
         " Example: PAYE is a system for withholding tax[1][2]." 
         "If a statement is general or not supported by the context, do not assign a citation. If you don't know, reply I dont know.
"
    )

    messages = [
        {"role": "system", "content": f"{system_prompt}\n\nContext:\n{context}"},
        {"role": "user", "content": question},
    ]

    client = _perplexity_client()
    response = client.chat.completions.create(
        model=PERPLEXITY_MODEL,
        messages=messages,
        temperature=0.12,
        max_tokens=1200,
    )
    llm_answer = response.choices[0].message.content

    # Post-process for sentence-level citations using chunk mapping (demo: all refs shown)
    sentences = _sentence_split(llm_answer)
    # For now, append all refs to all sentences; 
    # for improved precision, add ref selection logic here per sentence/context match/keyword match.
    ref_str = " ".join([f"[{i+1}]" for i in range(len(chunks))])
    answer_with_refs = " ".join(f"{sent} {ref_str}" for sent in sentences)

    return {
        "answer": answer_with_refs,
        "citations": citation_meta
    }
