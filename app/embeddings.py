from sentence_transformers import SentenceTransformer

BGE_MODEL_NAME = "BAAI/bge-large-en-v1.5"
_INSTRUCTION = "Represent this sentence for searching relevant passages: "

_bge = SentenceTransformer(BGE_MODEL_NAME)

def embed_query(text: str) -> list[float]:
    q = _INSTRUCTION + text
    vec = _bge.encode([q], normalize_embeddings=True)[0]
    return vec.tolist()
