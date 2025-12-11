# Quick Start Guide

Get the BTT Anote RAG system and evaluation framework running in minutes.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Quick Setup (5 Minutes)](#quick-setup-5-minutes)
4. [Run the RAG System](#run-the-rag-system)
5. [Run the Full Demo](#run-the-full-demo)
6. [Evaluate Models](#evaluate-models)
7. [Troubleshooting](#troubleshooting)
8. [Next Steps](#next-steps)

---

## Prerequisites

### Required
- Python 3.8 or higher
- pip package manager
- 2GB free disk space

### Optional (for full functionality)
- Node.js 14+ and npm (for frontend)
- Anthropic API key (for Claude)
- OpenAI API key (for GPT-4)
- Ollama installed (for local LLM)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/anote-ai/btt-anote1a.git
cd btt-anote1a
```

### 2. Install Python Dependencies

```bash
# Install core dependencies
pip install -r anote_rag/requirements.txt

# Install API dependencies (optional)
pip install fastapi uvicorn[standard] pydantic
```

### 3. Set Up API Keys (Optional)

Create a `.env` file in the project root:

```bash
# For Claude (recommended)
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# For OpenAI (optional)
echo "OPENAI_API_KEY=your-key-here" >> .env
```

**Get API Keys**:
- Anthropic Claude: [https://console.anthropic.com/](https://console.anthropic.com/)
- OpenAI: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

## Quick Setup (5 Minutes)

### Create Vector Database

This one-time setup creates embeddings from Anote documentation:

```bash
cd anote_rag
python make_embeddings.py
```

**What this does**:
- Loads 135 Anote documentation chunks from [data/processed/clean_chunks.jsonl](data/processed/clean_chunks.jsonl)
- Creates 384-dimensional embeddings using HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- Stores in ChromaDB at `./chroma_anote_db/`
- Takes approximately 1-2 minutes

**Expected output**:
```
Loading data from ../data/processed/clean_chunks.jsonl...
✓ Loaded 135 documents
Creating embeddings...
✓ Embeddings created successfully
Saved to ./chroma_anote_db/
```

---

## Run the RAG System

### Basic Usage (Python)

```bash
cd anote_rag
python rag.py
```

This launches an interactive command-line interface:

```
====================================
RAG SYSTEM
====================================

Loading vectorstore from ./chroma_anote_db...
✓ Loaded 135 embeddings
✓ RAG system ready
====================================

Enter your question (or 'quit' to exit): What is Anote?

Answer: Anote is a data labeling and active learning platform...

Sources:
1. Anote - Executive Summary
2. Anote - Platform Overview

Enter your question (or 'quit' to exit):
```

### Using Different LLM Providers

**Claude (Recommended)**:
```python
from anote_rag.rag import AnoteRAG

rag = AnoteRAG(llm_provider="claude")
response = rag.query("What is active learning?")
print(response['answer'])
```

**OpenAI**:
```python
rag = AnoteRAG(llm_provider="openai")
response = rag.query("How does Anote handle multilingual data?")
```

**Ollama (Local, Free)**:
```python
rag = AnoteRAG(llm_provider="ollama")
response = rag.query("What languages does Anote support?")
```

---

## Run the Full Demo

### Start the Backend API

Terminal 1:
```bash
# From project root
uvicorn api.bridge:app --port 8001 --reload
```

**Expected output**:
```
✓ Multilingual RAG initialized: ./anote_rag/chroma_multilingual_db
✓ Anote RAG initialized: ./anote_rag/chroma_anote_db
INFO:     Uvicorn running on http://localhost:8001
```

### Start the Frontend

Terminal 2:
```bash
cd frontend
npm install  # First time only
npm start
```

**Expected output**:
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
```

### Access the Demo

Open your browser to [http://localhost:3000](http://localhost:3000)

**Features**:
- **Home Page**: Navigation to Chat and Evaluations
- **Chat Page** ([/chat](http://localhost:3000/chat)): Ask questions in Spanish, Hebrew, Japanese, or Korean
- **Evaluations Page** ([/evaluations](http://localhost:3000/evaluations)): View model performance metrics
- **Company Chat** ([/companies](http://localhost:3000/companies)): Ask about Anote

---

## Evaluate Models

### Run Evaluation on Test Data

```bash
python src/run_evaluation.py
```

**What this does**:
- Loads 400 test cases from [data/processed/translation_testing/merged/translation_testing_all.jsonl](data/processed/translation_testing/merged/translation_testing_all.jsonl)
- Runs each through the RAG system
- Calculates BLEU and BERTScore metrics
- Outputs to [data/processed/translation_evaluation_merged.csv](data/processed/translation_evaluation_merged.csv)
- Takes approximately 20 minutes with Claude API

### Calculate Metrics Manually

```bash
python src/calculate_metrics.py
```

Generates:
- [data/processed/evaluation_metrics.json](data/processed/evaluation_metrics.json)
- [data/processed/leaderboard.csv](data/processed/leaderboard.csv)
- [data/processed/leaderboard_by_language.csv](data/processed/leaderboard_by_language.csv)

### View Results

```python
import pandas as pd

# View leaderboard
leaderboard = pd.read_csv('data/processed/leaderboard_by_language.csv')
print(leaderboard)

# View detailed metrics
import json
with open('data/processed/evaluation_metrics.json') as f:
    metrics = json.load(f)
    print(json.dumps(metrics['claude'], indent=2))
```

---

## Troubleshooting

### API Won't Start

**Error**: `FileNotFoundError: Vectorstore not found`

**Solution**:
```bash
cd anote_rag
python make_embeddings.py
```

Make sure `chroma_anote_db/` directory exists.

---

### Frontend Shows CORS Error

**Error**: `Access to fetch at 'http://localhost:8001/chat' has been blocked by CORS policy`

**Solution**:
1. Verify API is running on port 8001
2. Check `ALLOWED_ORIGINS` in `.env`:
   ```bash
   echo "ALLOWED_ORIGINS=http://localhost:3000" >> .env
   ```
3. Restart the API server

---

### Missing API Key

**Error**: `anthropic.APIConnectionError: API key not found`

**Solution**:
1. Create `.env` file in project root
2. Add your API key:
   ```bash
   echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
   ```
3. Verify the file exists and contains the key
4. Restart the Python script

---

### Ollama Not Found

**Error**: `Ollama service not available`

**Solution**:
1. Install Ollama: [https://ollama.ai/](https://ollama.ai/)
2. Pull the model:
   ```bash
   ollama pull llama3.2:3b
   ```
3. Verify it's running:
   ```bash
   curl http://localhost:11434/api/generate -d '{"model":"llama3.2:3b","prompt":"test"}'
   ```

---

### Evaluation Takes Too Long

**Problem**: Evaluation running for hours

**Solution - Test on Subset**:
```python
# In src/run_evaluation.py, modify to test on 50 items:
test_items = all_items[:50]  # Instead of all_items
```

**Solution - Use Faster Model**:
```python
# Use Ollama (local, free, faster):
rag = AnoteRAG(llm_provider="ollama")
```

---

### Frontend Build Errors

**Error**: `npm ERR! code ELIFECYCLE`

**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

---

## Next Steps

### Explore the Datasets

1. **Translation Testing Dataset** (400 items):
   ```python
   import json
   with open('data/processed/translation_testing/merged/translation_testing_all.jsonl') as f:
       items = [json.loads(line) for line in f]
   print(f"Loaded {len(items)} translation test items")
   ```

2. **Benchmark Testing Dataset** (396 items):
   ```python
   with open('data/processed/benchmark_testing/merged/benchmark_testing_all.jsonl') as f:
       items = [json.loads(line) for line in f]
   print(f"Loaded {len(items)} benchmark test items")
   ```

3. **Multilingual Chunks** (9,322 chunks):
   ```python
   for lang in ['es', 'he', 'ja', 'ko']:
       with open(f'data/processed/benchmark_chunks/benchmark_{lang}.jsonl') as f:
           chunks = [json.loads(line) for line in f]
       print(f"{lang.upper()}: {len(chunks)} chunks")
   ```

### Customize the RAG System

**Adjust Retrieval**:
```python
rag = AnoteRAG(
    llm_provider="claude",
    top_k=6,              # Retrieve more chunks (default: 4)
    temperature=0.3       # More focused responses (default: 0.7)
)
```

**Use Custom Prompt**:
```python
custom_prompt = """You are a helpful assistant. Use this context: {context}
Question: {question}
Answer:"""

rag = AnoteRAG(llm_provider="claude", custom_prompt=custom_prompt)
```

### Extend the System

1. **Add More Languages**:
   - Add chunks to `data/processed/benchmark_chunks/benchmark_xx.jsonl`
   - Rebuild embeddings: `python make_embeddings_multilingual.py`

2. **Add Custom Documents**:
   - Add to `data/processed/clean_chunks.jsonl`
   - Rebuild: `python make_embeddings.py`

3. **Create New Evaluations**:
   - Add test cases to `data/processed/translation_testing/`
   - Run evaluation: `python src/run_evaluation.py`

### Read the Documentation

- **[METHODOLOGY.md](METHODOLOGY.md)**: Comprehensive dataset generation methodology
- **[FINAL_WRITEUP.md](FINAL_WRITEUP.md)**: Complete project report
- **[DEMO_SETUP.md](DEMO_SETUP.md)**: Detailed demo instructions
- **[data/processed/metadata/GENERATION_PROMPTS.md](data/processed/metadata/GENERATION_PROMPTS.md)**: Full prompts used for data generation

---

## Getting Help

### Common Commands Reference

**Create Embeddings**:
```bash
cd anote_rag && python make_embeddings.py
```

**Run RAG System**:
```bash
cd anote_rag && python rag.py
```

**Start API**:
```bash
uvicorn api.bridge:app --port 8001 --reload
```

**Start Frontend**:
```bash
cd frontend && npm start
```

**Run Evaluation**:
```bash
python src/run_evaluation.py
```

**Calculate Metrics**:
```bash
python src/calculate_metrics.py
```

### File Locations

- **Datasets**: [data/processed/](data/processed/)
- **RAG System**: [anote_rag/](anote_rag/)
- **API**: [api/bridge.py](api/bridge.py)
- **Frontend**: [frontend/](frontend/)
- **Scripts**: [src/](src/)
- **Metadata**: [data/processed/metadata/](data/processed/metadata/)

### Support

- **Issues**: [https://github.com/anote-ai/btt-anote1a/issues](https://github.com/anote-ai/btt-anote1a/issues)
- **Email**: hello@breakthroughtech.org
- **Documentation**: See [README.md](README.md) for full project overview

---

**Last Updated**: December 2025
