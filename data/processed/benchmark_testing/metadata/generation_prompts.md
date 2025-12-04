# Generation Prompts

## ChatGPT Prompt
You are creating a high-quality multilingual translation evaluation dataset for the Anote benchmark. I will provide you with 3 parallel translation pairs (source language + English translation). Your task is to generate exactly 6 diverse question-answer pairs that test translation accuracy and comprehension depth.

### INPUT DATA
Paste 3 translation pairs as JSON objects. Example:
{
  "id": "es_00123",
  "source_lang": "es",
  "target_lang": "en",
  "source_text": "La economía global enfrenta desafíos sin precedentes.",
  "target_text": "The global economy faces unprecedented challenges."
}

### GENERATION REQUIREMENTS
- Output: a JSON array only (no markdown, no preamble).
- Exactly 6 QA items.

Difficulty Distribution:
- 2 easy (direct lookup, answerable in ~5 seconds)
- 2 medium (requires inference, ~15 seconds)
- 2 hard (cultural nuance, multi-hop, ambiguity)

Question Type Distribution:
- 2 factual
- 2 reasoning
- 2 ambiguous/challenging

Register Distribution:
- 3 formal (no contractions)
- 3 informal (contractions OK)

Citation Requirements:
- At least 2 citations from source language and 2 from target language
- citation_text must be an exact continuous substring (3–25 words)

Linguistic Coverage (MANDATORY):
- At least 1 idiom/culture item
- At least 1 register/formality item
- At least 1 temporal/modal/aspectual item

Critical Rules:
- Do not create questions answerable without reading the translation
- Do not cite entire source/target text
- Do not create near-duplicates
- Answers must interpret, not just quote
- Use single quotes for internal quotes ('...')

Output format (each item):
{
  "question": "...",
  "answer": "...",
  "cite_from": "source" | "target",
  "citation_text": "...",
  "difficulty": "easy"|"medium"|"hard",
  "question_type": "factual"|"reasoning"|"ambiguous",
  "register": "formal"|"informal"
}

Validation checklist (generator must enforce):
- Exactly 6 items
- 2 easy / 2 medium / 2 hard
- 2 factual / 2 reasoning / 2 ambiguous
- 3 formal / 3 informal
- ≥2 source citations, ≥2 target citations
- All citation_text verbatim in referenced text
- Includes idiom/culture, register, temporal/modal coverage
- All internal quotes use single quotes

## Gemini Prompt
Task: Generate translation-evaluation QA items for Anote.

INPUT:
Provide 2 parallel translation pairs as JSON objects (example included).

Requirements:
- Output exactly 4 QA items (JSON array only).
- Difficulty: 1 easy, 2 medium, 1 hard.
- Types: 2 factual, 1 reasoning, 1 ambiguous.
- Register: 2 formal, 2 informal.
- Citations: at least 1 source and 1 target citation; citation_text must be exact continuous substring (3–25 words).
- Linguistic coverage: include idiom/culture and register questions.
- Critical rules identical to ChatGPT prompt (no questions answerable without translation, no full-text citations, no near-duplicates, interpretive answers, single quotes for internal quotes).

Output format: raw JSON array with fields identical to ChatGPT prompt.

## Claude Prompt
You are building a translation evaluation dataset for the Anote benchmark. You will receive 3 parallel corpus pairs (original language + English translation). Generate 6 diverse question-answer items that test translation accuracy and comprehension depth.

Key constraints:
- Exactly 6 items (JSON array only).
- Difficulty: 2 easy, 2 medium, 2 hard.
- Types: 2 factual, 2 reasoning, 2 ambiguous.
- Register: 3 formal, 3 informal.
- Citations: ≥2 source citations and ≥2 target citations, citation_text must be an exact continuous substring (3–25 words).
- Linguistic coverage: include idiom/cultural, register shift, temporal/modal checks.
- Forbidden: questions answerable without reading translation, entire-text citations, trivial rewordings, answers that merely copy citation_text.
- Mandatory: all citation_text verbatim exists, answers show comprehension, single quotes for internal quotes.

Output format: raw JSON array only. Ensure generator validates all checklist items before returning.
