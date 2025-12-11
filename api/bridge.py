"""
Simple FastAPI bridge for RAG Demo
Two RAG instances: one for multilingual Wikipedia, one for Anote docs
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import csv
from pathlib import Path
import requests
import pandas as pd
import os

sys.path.append('./anote_rag')
from rag import AnoteRAG

# ============================================================================
# LANGUAGE-SPECIFIC PROMPTS
# ============================================================================

MULTILINGUAL_PROMPTS = {
    "spanish": """Eres un asistente de IA que responde preguntas en español usando Wikipedia.
Usa el siguiente contexto para responder la pregunta con precisión. Si el contexto contiene la respuesta, proporciónala claramente con detalles. Si no estás seguro, dilo honestamente.
Contexto:
{context}
Pregunta: {question}
Respuesta:""",

    "hebrew": """אתה עוזר AI שעונה על שאלות בעברית באמצעות ויקיפדיה.
השתמש בהקשר הבא כדי לענות על השאלה במדויק. אם ההקשר מכיל את התשובה, ספק אותה בבירור עם פרטים. אם אינך בטוח, אמור זאת בכנות.
הקשר:
{context}
שאלה: {question}
תשובה:""",

    "japanese": """あなたはWikipediaを使用して日本語で質問に答えるAIアシスタントです。
次の文脈を使用して、質問に正確に答えてください。文脈に答えが含まれている場合は、詳細を明確に示してください。確信が持てない場合は、正直に伝えてください。
文脈:
{context}
質問: {question}
回答:""",

    "korean": """당신은 위키백과를 사용하여 한국어로 질문에 답하는 AI 어시스턴트입니다.
다음 맥락을 사용하여 질문에 정확하게 답하십시오. 맥락에 답이 포함되어 있으면 세부 사항과 함께 명확하게 제공하십시오. 확실하지 않으면 정직하게 말하십시오.
맥락:
{context}
질문: {question}
답변:"""
}

ANOTE_PROMPT = """You are an AI assistant that answers questions about Anote AI using the company's documentation.
Use the following context to answer the question accurately. If the context contains the answer, provide it clearly with details. If you're not sure, say so honestly.
Context:
{context}
Question: {question}
Answer:"""

# ============================================================================
# FASTAPI APP SETUP
# ============================================================================

app = FastAPI()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# TWO SEPARATE RAG INSTANCES
# ============================================================================

# Instance 1: Multilingual Wikipedia (9,322 chunks across 4 languages)
MULTILINGUAL_DB = os.getenv("MULTILINGUAL_DB_PATH", "./anote_rag/chroma_multilingual_db")

# Instance 2: Anote documentation (135 chunks, English)
ANOTE_DB = os.getenv("ANOTE_DB_PATH", "./anote_rag/chroma_anote_db")

try:
    multilingual_rag = AnoteRAG(
        llm_provider="claude",
        chroma_path=MULTILINGUAL_DB
    )
    print(f"✓ Multilingual RAG initialized: {MULTILINGUAL_DB}")
except Exception as e:
    print(f"❌ Failed to initialize multilingual RAG: {e}")
    multilingual_rag = None

try:
    anote_rag = AnoteRAG(
        llm_provider="claude",
        chroma_path=ANOTE_DB
    )
    print(f"✓ Anote RAG initialized: {ANOTE_DB}")
except Exception as e:
    print(f"❌ Failed to initialize Anote RAG: {e}")
    anote_rag = None

# ============================================================================
# REQUEST MODELS
# ============================================================================

class ChatRequest(BaseModel):
    question: str
    language: str

class CompanyChatRequest(BaseModel):
    question: str

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.post("/languages")
def chat(request: ChatRequest):
    """
    Multilingual Wikipedia chat - uses multilingual_rag instance
    """
    if not multilingual_rag:
        raise HTTPException(
            status_code=503, 
            detail="Multilingual RAG system not initialized"
        )
    
    # Validate inputs
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    language = request.language.lower()
    if language not in MULTILINGUAL_PROMPTS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported language: {language}. Supported: {list(MULTILINGUAL_PROMPTS.keys())}"
        )
    
    try:
        # Get language-specific prompt
        custom_prompt = MULTILINGUAL_PROMPTS[language]
        
        # Query multilingual Wikipedia RAG
        result = multilingual_rag.query(
            request.question, 
            custom_prompt=custom_prompt,
            verbose=False
        )
        
        return {
            "answer": result["answer"],
            "sources": [s["title"] for s in result["sources"]],
            "language": language,
            "database": "multilingual_wikipedia"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/chat/company")
def chat_company(request: CompanyChatRequest):
    """
    Anote company chat - uses anote_rag instance
    """
    if not anote_rag:
        raise HTTPException(
            status_code=503, 
            detail="Anote RAG system not initialized"
        )
    
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        # Query Anote documentation RAG
        result = anote_rag.query(
            request.question, 
            custom_prompt=ANOTE_PROMPT,
            verbose=False
        )
        
        return {
            "answer": result["answer"],
            "sources": [s["title"] for s in result["sources"]],
            "database": "anote_documentation"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/chat/general")
def general_chat(request: CompanyChatRequest):
    """
    General chat - no RAG, uses Ollama directly
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": request.question,
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            answer = response.json().get("response", "")
            return {
                "answer": answer, 
                "sources": [],
                "database": "none_ollama_direct"
            }
        else:
            raise HTTPException(
                status_code=500, 
                detail=f"Ollama returned status {response.status_code}"
            )
    
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503, 
            detail="Ollama service not available. Make sure Ollama is running on port 11434."
        )
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Ollama request timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")


@app.get("/evaluations")
async def get_evaluations():
    """
    Return leaderboard data from leaderboard_by_language.csv
    """
    try:
        leaderboard_file = Path("data/outputs/leaderboard_by_language.csv")
        
        if not leaderboard_file.exists():
            raise HTTPException(
                status_code=404, 
                detail="Leaderboard file not found. Run generate_leaderboard.py first."
            )
        
        df = pd.read_csv(leaderboard_file)
        
        results = []
        for _, row in df.iterrows():
            results.append({
                "model": str(row["Model"]),
                "language": str(row["Language"]),
                "bleu": float(row["BLEU"]),
                "bertscore_f1": float(row["BERTScore_F1"]),
                "count": int(row["Count"])
            })
        
        return results
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Leaderboard file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading leaderboard: {str(e)}")


@app.get("/model-comparison")
def get_model_comparison():
    """
    Return model comparison results from CSV
    """
    csv_path = Path("data/processed/model_comparison.csv")
    
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


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "multilingual_rag": multilingual_rag is not None,
        "anote_rag": anote_rag is not None,
        "multilingual_db": MULTILINGUAL_DB,
        "anote_db": ANOTE_DB
    }
