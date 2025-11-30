# Generation Prompts and Settings

**Reference:** Lutra.ai Benchmark Creator methodology

**Models Used:** ChatGPT, Claude, Gemini

**Temperature:** 0.0–0.3 for deterministic outputs

**Batch Configuration:**
- Batches per model per language: 6
- Items per batch: 6
- Total items per model per language: 36

## Question Types

### Factual
Template: "¿Cuál es el valor de {entity} en {period}?" (Spanish example)
- Answer: Direct fact/value from text
- Difficulty: easy to medium
- Citation: Specific value or statistic

### Reasoning
Template: "¿Qué se puede inferir sobre {topic} a partir del texto?" (Spanish example)
- Answer: Inference or logical conclusion
- Difficulty: medium to hard
- Citation: Source text supporting inference

### Ambiguous/Challenging
Template: "¿Qué interpretación cultural o pragmática podría tener '{snippet}'?" (Spanish example)
- Answer: Cultural or pragmatic interpretation
- Difficulty: hard
- Citation: Snippet of text

## Generation Process
1. Load source translation_testing batches
2. Extract entity, period, topic, snippet from source or use variation pools
3. Format templates per language
4. Ensure uniqueness across batches via deterministic randomization
5. Write 6 batches per model with ~36 items per batch

## Fields Per Item
- `id`: Unique identifier (lang_model_batchbatch_item)
- `language`: ISO 639-1 code (es, he, ja, ko)
- `model`: LLM name (chatgpt, claude, gemini)
- `question_type`: factual | reasoning | ambiguous
- `question`: Multilingual question string
- `answer`: Expected answer string
- `cite_from`: source | target
- `citation_text`: Exact text snippet from source
- `difficulty`: easy | medium | hard
- `register`: formal | informal
- `batch_id`: lang_batch_model_batchnum
- `generated_date`: ISO date
