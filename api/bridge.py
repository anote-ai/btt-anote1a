"""
Simple FastAPI bridge for Anote RAG Demo
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import csv
from pathlib import Path

sys.path.append('./anote_rag')
from rag import AnoteRAG

app = FastAPI()

# CORS for localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG instances
rag_instances = {
    "spanish": AnoteRAG(llm_provider="claude", chroma_path="./anote_rag/chroma_anote_db"),
    "hebrew": AnoteRAG(llm_provider="claude", chroma_path="./anote_rag/chroma_anote_db"),
    "japanese": AnoteRAG(llm_provider="claude", chroma_path="./anote_rag/chroma_anote_db"),
    "korean": AnoteRAG(llm_provider="claude", chroma_path="./anote_rag/chroma_anote_db")
}

class ChatRequest(BaseModel):
    question: str
    language: str

@app.post("/chat")
def chat(request: ChatRequest):
    """Chat endpoint - answer questions using RAG"""
    rag = rag_instances.get(request.language.lower(), rag_instances["spanish"])
    result = rag.query(request.question, verbose=False)

    return {
        "answer": result["answer"],
        "sources": [s["title"] for s in result["sources"]]
    }

@app.get("/evaluations")
def get_evaluations():
    """Return evaluation results from CSV"""
    csv_path = Path("data/processed/evaluation_results.csv")

    if not csv_path.exists():
        return []

    try:
        results = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
        return results
    except Exception as e:
        print(f"Error reading evaluation results: {e}")
        return []

@app.get("/model-comparison")
def get_model_comparison():
    """Return model comparison results from CSV"""
    csv_path = Path("model_comparison.csv")

    if not csv_path.exists():
        return []

    try:
        results = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
        return results
    except Exception:
        return []
