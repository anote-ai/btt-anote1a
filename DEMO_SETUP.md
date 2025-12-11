# Anote Demo Setup Guide

## Quick Start (4 Steps)

### 1. Create Vectorstore (ONE-TIME SETUP)
```bash
cd anote_rag
python make_embeddings.py
```
This creates `./chroma_anote_db/` from your 135 Anote company chunks.

### 2. Install API Dependencies
```bash
pip install fastapi uvicorn[standard] pydantic
```

### 3. Start Backend API (Terminal 1)
```bash
# From project root
uvicorn api.bridge:app --port 8001 --reload
```
API will run on [http://localhost:8001](http://localhost:8001)

### 4. Start Frontend (Terminal 2)
```bash
cd frontend
npm start
```
Frontend will open at [http://localhost:3000](http://localhost:3000)

---

## What You'll See

### Home Page (/)
- Landing page with links to Chat and Evaluations

### Chat Page (/chat)
- Language selector: Spanish | Hebrew | Japanese | Korean
- Ask questions about Anote
- Get RAG-powered answers with sources

### Evaluations Page (/evaluations)
- View evaluation results from CSV
- Filter by language
- See question difficulty and type

---

## API Endpoints

### POST /chat
Request:
```json
{
  "question": "What is Anote?",
  "language": "spanish"
}
```

Response:
```json
{
  "answer": "Anote is...",
  "sources": ["Anote - Executive Summary", "..."]
}
```

### GET /evaluations
Returns array of evaluation results from [leaderboard_by_language.csv](data/processed/leaderboard_by_language.csv)

---

## Optional: Generate Evaluation CSV

If you want to populate the Evaluations page:

```bash
# Create and run the evaluation script
python src/run_evaluation.py
```

This will:
1. Load 400 test cases from [translation_testing_all.jsonl](data/processed/translation_testing/merged/translation_testing_all.jsonl)
2. Run each through RAG system
3. Output to [translation_evaluation_merged.csv](data/processed/translation_evaluation_merged.csv)
4. Takes approximately 20 minutes with Claude API

---

## Troubleshooting

**API won't start:**
- Make sure you ran `python make_embeddings.py` first
- Check that `chroma_anote_db/` directory exists
- Verify you have ANTHROPIC_API_KEY in .env file

**Frontend shows CORS error:**
- Make sure API is running on port 8001
- Check browser console for errors

**Evaluations page shows error:**
- Run `python src/run_evaluation.py` to generate CSV first
- Or comment out the Evaluations route for demo

---

## File Structure Created

```
btt-anote1a/
├── api/
│   ├── bridge.py                  # FastAPI backend
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js                # Router + navbar
│   │   ├── index.css             # Tailwind styles
│   │   ├── colors.css            # Anote color vars
│   │   └── components/
│   │       ├── Home.js           # Landing page
│   │       ├── Chat.js           # Chat interface
│   │       ├── Evaluations.js    # Results table
│   │       └── Companies.js      # Company chat
│   ├── tailwind.config.js
│   └── package.json
├── chroma_anote_db/              # Generated vectorstore
└── data/processed/
    └── translation_evaluation_merged.csv  # Generated results
```

---

## Demo Script (Friday Presentation)

1. **Show Home Page** - Explain the two main features
2. **Demo Chat** - Ask "What is Anote?" in Spanish and Hebrew
3. **Show Evaluations** - Filter by language, explain metrics
4. **Show Code** - Quick walk through:
   - [bridge.py](api/bridge.py) (304 lines)
   - [Chat.js](frontend/src/components/Chat.js) (simple React)
   - Mention RAG system in [anote_rag/](anote_rag/)

Total demo time: 5-10 minutes
