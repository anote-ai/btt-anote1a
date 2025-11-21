# RAG System Setup Instructions

Complete guide for setting up the Anote RAG chatbot system using Ollama (free, local LLM).

## Prerequisites
- Python 3.10+
- At least 8GB RAM (16GB recommended)
- ~5GB free disk space

## Step 1: Install Ollama

### Windows:
1. Download Ollama installer: https://ollama.com/download/windows
2. Run the installer
3. Open Command Prompt and verify installation:
   ```bash
   ollama --version
   ```

### Mac:
```bash
brew install ollama
```

### Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Step 2: Pull the LLM Model

Open terminal and run:
```bash
ollama pull llama3.2:3b
```

This downloads ~2GB. Wait for completion.

**Verify it works:**
```bash
ollama run llama3.2:3b
```
Type "Hello" and you should get a response. Type `/bye` to exit.

## Step 3: Clone the Repo and Set Up Python Environment

```bash
cd btt-anote1a

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install langchain langchain-community langchain-chroma langchain-ollama sentence-transformers chromadb
```

## Step 4: Generate Vector Database

This creates the embeddings from the cleaned data:

```bash
python src/OLLAMA_make_rag_embeddings.py
```

**Expected output:**
- "Loaded 135 chunks"
- "Created vector store with 135 embeddings"
- Creates `chroma_anote_db/` folder (locally only, not committed)
- Generates `initial_predictions.json`

**First run takes 5-10 minutes** (downloads embedding model).

## Step 5: Verify It Works

Check `initial_predictions.json` for the test answers. You should see:
- Detailed answers about Anote
- Source citations
- No "I don't know" responses

## Troubleshooting

### "Could not connect to Ollama"
- Ensure Ollama is running (runs as background service after install)
- Restart your terminal
- Try: `ollama serve` in one terminal, then run script in another

### "Loaded 0 embeddings"
- Delete `chroma_anote_db/` folder
- Run `python src/make_rag_embeddings.py` again

### Slow performance
- The 3b model is optimized for speed
- If you have more RAM/GPU, upgrade to 7b model:
  ```bash
  ollama pull llama3.2:7b
  ```
  Then change `OLLAMA_MODEL` variable in `make_rag_embeddings.py`

## Files Generated Locally (Don't Commit)
- `chroma_anote_db/` - Vector database (regenerate from clean_chunks.jsonl)
- `__pycache__/` - Python cache
