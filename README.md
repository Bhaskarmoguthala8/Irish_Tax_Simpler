# 🇮🇪 Irish Tax Simpler

A powerful RAG (Retrieval-Augmented Generation) application that provides accurate, citation-backed answers about Irish tax information using AI.

## ✨ Features

- **Smart Search**: Vector search with BGE embeddings finds relevant documents
- **Intelligent Reranking**: Cohere cross-encoder refines results
- **AI Answers**: Perplexity Sonar Pro generates grounded responses
- **Source Citations**: Every answer includes document sources
- **Fast Responses**: Optimized for speed (2-3 seconds)
- **Gradio Interface**: Beautiful, easy-to-use web UI

## 🏗️ Architecture

```
User Question
    ↓
Vector Retrieval (Qdrant + BGE)
    ↓
Reranking (Cohere)
    ↓
Answer Generation (Perplexity)
    ↓
Response with Citations
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file with your API keys:
```env
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_key
QDRANT_COLLECTION=gov_docs_v1
COHERE_API_KEY=your_key
PERPLEXITY_API_KEY=your_key
PERPLEXITY_MODEL=sonar-pro
PORT=8000
```

### 3. Run the Application
```bash
python app.py
```

Access at: **http://localhost:7860**

## ☁️ Deploy to Hugging Face Spaces

### Files to Upload:
- `app.py` → rename to app.py on HF
- All files from `app/` folder
- `requirements.txt`

### Environment Variables to Set:
- `QDRANT_URL`
- `QDRANT_API_KEY`
- `QDRANT_COLLECTION`
- `COHERE_API_KEY`
- `PERPLEXITY_API_KEY`
- `PERPLEXITY_MODEL`

## 📁 Project Structure

```
Irish_Tax_Simpler/
├── app.py                  # Main application (Gradio UI)
├── app/                    # Core modules
│   ├── config.py          # Configuration
│   ├── embeddings.py      # BGE embeddings
│   ├── generate.py         # Answer generation
│   ├── question_refiner.py # Spell correction (optional)
│   ├── rerank.py           # Cohere reranking
│   └── retriever.py        # Qdrant retrieval
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🧠 Technical Details

**Embedding Model**: BAAI/bge-large-en-v1.5  
**Reranker**: Cohere rerank-english-v3.0  
**Generator**: Perplexity Sonar Pro  
**Database**: Qdrant vector database  

## 📊 Performance

- **Average Response Time**: 2-3 seconds
- **Retrieval**: 10 documents (optimized)
- **Reranking**: 3 documents (optimized)
- **Citations**: Automatic source attribution

## 📝 Usage Example

**Question**: "What is PAYE and PRSI?"

**Response**:
- Comprehensive answer about PAYE (Pay As You Earn) and PRSI (Pay Related Social Insurance)
- Citations with source documents, page numbers, and relevance scores
- Diagnostic information showing retrieval performance

## 🔍 Troubleshooting

**Issue**: Slow response times
- Check internet connection
- Verify API keys are valid
- Check Qdrant connection

**Issue**: No answers
- Verify documents in Qdrant collection
- Check score threshold setting
- Ensure API keys have proper permissions

## 📚 API Requirements

You need API keys for:
- **Qdrant**: Vector database (self-hosted or cloud)
- **Cohere**: Reranking service
- **Perplexity**: Answer generation

## 🛠️ Dependencies

See `requirements.txt` for full list.

Key dependencies:
- `gradio>=4.0.0` - Web interface
- `qdrant-client>=1.9.0` - Vector database
- `sentence-transformers>=3.0.0` - BGE embeddings
- `cohere>=5.5.6` - Reranking
- `openai>=1.50.0` - Perplexity client

## 💡 Tips

1. Be specific in your questions for better results
2. Check citations for source verification
3. Response times vary based on document complexity
4. All answers are citation-backed from official sources

## 📞 Support

For issues or questions, check the configuration and API keys.

---

Built with ❤️ for simplifying Irish tax information
