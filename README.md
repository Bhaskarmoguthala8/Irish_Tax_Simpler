# Irish Tax Simpler

A sophisticated RAG (Retrieval-Augmented Generation) service designed to simplify Irish tax information by providing accurate, context-aware answers from government documents. This application uses a multi-stage pipeline with vector search, reranking, and AI generation to deliver precise tax guidance.

## 🏗️ Architecture

The application follows a **Retrieve → Rerank → Generate** pipeline:

1. **Retrieval**: Uses Qdrant vector database with BGE embeddings to find relevant document chunks
2. **Reranking**: Employs Cohere's cross-encoder to refine search results by relevance
3. **Generation**: Leverages Perplexity's Sonar Pro model for grounded, citation-rich answers

## 🚀 Features

- **Vector Search**: BGE-large-en-v1.5 embeddings for semantic document retrieval
- **Intelligent Reranking**: Cohere's rerank-english-v3.0 model for precision
- **AI-Powered Answers**: Perplexity Sonar Pro for context-aware responses
- **Citation Tracking**: Automatic source attribution with document IDs and page numbers
- **RESTful API**: FastAPI-based service with health checks and diagnostics
- **Configurable Parameters**: Adjustable retrieval and ranking thresholds

## 📋 Prerequisites

- Python 3.8+
- Qdrant vector database instance
- API keys for:
  - Cohere (for reranking)
  - Perplexity (for answer generation)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Irish_Tax_Simpler
   ```

2. **Create and activate virtual environment**
   
   **Windows:**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Copy the example environment file and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` with your actual API keys:
   ```env
   # Qdrant Configuration
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_COLLECTION=gov_docs_v1
   
   # Cohere API (for reranking)
   COHERE_API_KEY=your_cohere_api_key
   
   # Perplexity API (for generation)
   PERPLEXITY_API_KEY=your_perplexity_api_key
   PERPLEXITY_MODEL=sonar-pro
   
   # Application
   PORT=8000
   ```

## 🚀 Usage

### Starting the Server

```bash
python main.py
```

The server will start on `http://localhost:8000` (or your configured PORT).

### API Endpoints

#### Health Check
```http
GET /health
```
Returns server status.

#### Ask Question
```http
POST /ask
Content-Type: application/json

{
  "question": "What are the income tax rates for 2024?",
  "top_k": 20,
  "top_n": 6,
  "score_threshold": 0.35
}
```

**Parameters:**
- `question` (required): Your tax-related question
- `top_k` (optional, default: 20): Number of documents to retrieve initially
- `top_n` (optional, default: 6): Number of documents to use after reranking
- `score_threshold` (optional, default: 0.35): Minimum similarity score for retrieval

**Response:**
```json
{
  "question": "What are the income tax rates for 2024?",
  "answer": "Based on the provided context...",
  "citations": [
    {
      "doc_id": "tax_guide_2024",
      "page": 15,
      "source_filename": "income_tax_rates.pdf",
      "vector_score": 0.85,
      "rerank_score": 0.92
    }
  ],
  "diagnostics": {
    "retrieved": 20,
    "reranked": 6
  }
}
```

## 🔧 Configuration

The application uses environment variables for configuration. Key settings:

- **QDRANT_URL**: Your Qdrant instance URL
- **QDRANT_COLLECTION**: Collection name containing Irish tax documents
- **COHERE_API_KEY**: Required for document reranking
- **PERPLEXITY_API_KEY**: Required for answer generation
- **PORT**: Server port (default: 8000)

## 📁 Project Structure

```
Irish_Tax_Simpler/
├── app/
│   ├── config.py          # Environment configuration
│   ├── embeddings.py      # BGE embedding model
│   ├── generate.py        # Perplexity answer generation
│   ├── rerank.py          # Cohere reranking logic
│   ├── retriever.py       # Qdrant vector search
│   └── server.py          # FastAPI application
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🧠 Technical Details

### Embedding Model
- **Model**: BAAI/bge-large-en-v1.5
- **Purpose**: Converts text queries to high-dimensional vectors
- **Instruction**: "Represent this sentence for searching relevant passages:"

### Reranking
- **Provider**: Cohere
- **Model**: rerank-english-v3.0
- **Purpose**: Cross-encoder reranking for improved relevance

### Generation
- **Provider**: Perplexity AI
- **Model**: sonar-pro
- **Features**: Grounded responses with inline citations

## 🔍 Troubleshooting

### Common Issues

1. **Symlinks Warning (Windows)**
   - This is normal and doesn't affect functionality
   - To disable: Set `HF_HUB_DISABLE_SYMLINKS_WARNING=1`

2. **API Key Errors**
   - Ensure all required API keys are set in `.env`
   - Check key validity and permissions

3. **Qdrant Connection Issues**
   - Verify QDRANT_URL and QDRANT_API_KEY
   - Ensure the collection exists and contains data

## 📝 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📞 Support

[Add support information here]