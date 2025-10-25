import os
from dotenv import load_dotenv

load_dotenv()

# Qdrant
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "gov_docs_v1")

# Reranker
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Perplexity Sonar
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_MODEL = os.getenv("PERPLEXITY_MODEL", "sonar-pro")
PERPLEXITY_BASE_URL = "https://api.perplexity.ai"

# App
PORT = int(os.getenv("PORT", "8000"))
