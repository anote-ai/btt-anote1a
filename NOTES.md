### [By 09/30] Set up baseline model and submit initial predictions to Anote.
- Step 1 of README
  - Clean a small Anote dataset → JSONL or embeddings. ✓
  - Run it through either:
    - RAG setup (recc for speed) OR a tiny fine-tune (e.g., OpenAI fine-tune on Q&A). ✓
  - Plug into Autonomous-Intelligence UI. ✓
  - Show that the chatbot can answer at least a few questions correctly. ✓
  - Submit “initial predictions” to Anote = basically sample outputs / demo conversation. ✓

### [By 10/31] Fine-tune or optimize model and iterate on performance.
- Preprocessing for Multilingual Benchmark Dataset Creation (Fatima)
  - Curate data
  - Clean text, break into chunks, add citation metadata
  
- Testing Dataset Creation for Multilingual Benchmark Dataset Creation (Prudence)
  - Use multilingual LLM to create QA citation pairs
  - Include factual, reasoning-based, ambig/challenging questions
  - Ref Lutra.ai Benchmark Creator

- Preprocessing for Translation Task Dataset Creation (Bella)
  - Curate data sources (parallel corpuses via https://opus.nlpl.eu/legacy/opus-100.php)
  - Clean text, break into chunks, add citation metadata
  - NOTE: Included training, dev, and test datasets

- Testing Dataset Creation for Translation Task Dataset (Shalom)
  - Use multilingual LLM to create QA citation pairs
  - Include factual, reasoning-based, ambig/challenging questions
  - Include varied difficulty and formal/informal register
  - Ref Lutra.ai Benchmark Creator

### [By 11/30] Finalize model, evaluate results, and submit GitHub deliverables.
- Step 4 of README
