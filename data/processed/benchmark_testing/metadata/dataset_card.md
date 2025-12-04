# Benchmark Testing Dataset Card

Dataset Description
A multilingual QA + citation benchmark created from benchmark_chunks. This dataset contains generated evaluation items across Spanish, Hebrew, Japanese, and Korean.

Languages
Spanish (es): 90 items
Hebrew (he): 90 items
Japanese (ja): 90 items
Korean (ko): 90 items

Dataset Structure
Each item contains:
- question: Natural language question
- answer: Expected answer
- cite_from: "source" or "target"
- citation_text: Exact text span used as evidence
- difficulty: "easy" | "medium" | "hard"
- question_type: "factual" | "reasoning" | "ambiguous"
- register: "formal" | "informal"
- model: Generation model (chatgpt / claude / gemini)
- batch_id: Batch identifier
- generated_date: ISO date

Intended Use
- Evaluating LLM citation-grounded QA performance
- Benchmarking multilingual reasoning and translation-aware understanding
- Translation quality and robustness assessments

Limitations
- Items synthesized from benchmark_chunks using deterministic templates and fallbacks
- Limited to 4 languages and three model labels
- Not human-validated; model-generated ground truth may contain noise

Citation
[Your team/project citation info]
