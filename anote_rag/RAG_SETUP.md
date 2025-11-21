# Anote RAG Chatbot

**Unified RAG system** supporting multiple LLM providers (Ollama, Claude, OpenAI).

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Embeddings (One-Time Setup)
```bash
python make_embeddings.py
```

This creates `./chroma_anote_db/` with 135+ embeddings from Anote documentation.

### 3. Set Up API Keys (Optional)

Create `.env` file for API providers:
```bash
# For Claude
ANTHROPIC_API_KEY=sk-ant-your-key-here

# For OpenAI
OPENAI_API_KEY=sk-your-key-here
```

**Note:** Ollama requires no API key (runs locally).

### 4. Run RAG System
```bash
python rag.py
```

Or import and use:
```python
from rag import AnoteRAG

# Local/free version
rag = AnoteRAG(llm_provider="ollama")

# Production API version
rag = AnoteRAG(llm_provider="claude")

# Query
result = rag.query("What is Anote?")
print(result['answer'])
```

## Provider Comparison

| Provider | Speed | Cost | Setup |
|----------|-------|------|-------|
| **Ollama** | 30-60s | Free | Install Ollama |
| **Claude** | 2-5s | ~$3/1M tokens | API key only |
| **OpenAI** | 2-5s | ~$0.15/1M tokens | API key only |

## Testing

Test all providers:
```bash
python test_rag.py
```

This will:
- Check which providers are configured
- Test query performance
- Compare response times

## Project Structure

```
anote-rag/
├── rag.py                 # Main RAG system (unified)
├── make_embeddings.py     # Create vectorstore (run once)
├── test_rag.py           # Test all providers
├── requirements.txt      # Dependencies
├── .env                  # API keys (gitignored)
├── chroma_anote_db/     # Vectorstore (created by make_embeddings.py)
└── data/
    └── processed/
        └── clean_chunks.jsonl  # Input data
```

## Usage Examples

### Basic Query
```python
from rag import AnoteRAG

rag = AnoteRAG(llm_provider="claude")
result = rag.query("What are Anote's main products?")
print(result['answer'])
```

### Batch Queries
```python
questions = [
    "What is Anote?",
    "How does Anote use fine-tuning?",
    "What is Autonomous Intelligence?"
]

results = rag.batch_query(questions, save_to="results.json")
```

### Custom Configuration
```python
rag = AnoteRAG(
    chroma_path="./chroma_anote_db",
    llm_provider="claude",
    model_name="claude-3-5-sonnet-20241022",
    temperature=0.7,
    top_k=5  # Retrieve top 5 chunks
)
```

## Troubleshooting

### Ollama not connecting
```bash
# Start Ollama server
ollama serve

# Pull model
ollama pull llama3.2:3b
```

### API key errors
- Ensure `.env` file exists in project root
- Check API key format: `sk-ant-...` (Claude) or `sk-...` (OpenAI)
- Verify key is valid at provider's website

### No embeddings found
```bash
# Create embeddings first
python make_embeddings.py
```

## Development

### Adding New Provider
Edit `rag.py` and add to `_init_llm()`:
```python
elif provider == "your_provider":
    self.llm = YourLLM(...)
```

### Modifying Prompt
Edit the `PromptTemplate` in `_create_qa_chain()`.

### Changing Retrieval Strategy
Modify `search_kwargs` in retriever:
```python
retriever = self.vectorstore.as_retriever(
    search_type="mmr",  # or "similarity"
    search_kwargs={"k": 4, "fetch_k": 10}
)
```

## Performance Tips

1. **Use Claude/OpenAI for production** - 6-12x faster than Ollama
2. **Adjust `top_k`** - More chunks = better context, slower queries
3. **Cache embeddings** - Vectorstore is created once, reused forever
4. **Batch queries** - Use `batch_query()` for multiple questions

## Architecture

```
User Question
     ↓
  Embedding (HuggingFace)
     ↓
  Vector Search (ChromaDB)
     ↓
  Retrieve Top K Chunks
     ↓
  LLM (Ollama/Claude/OpenAI)
     ↓
  Answer + Sources
```

## License

This project uses Anote's documentation for RAG training.