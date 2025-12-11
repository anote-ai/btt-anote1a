# Dataset Generation Prompts

This document contains all prompts used to generate the Translation Testing and Benchmark Testing datasets.

---

## Table of Contents

1. [Translation Testing Prompts](#translation-testing-prompts)
   - [ChatGPT Prompt](#chatgpt-prompt-translation)
   - [Claude Prompt](#claude-prompt-translation)
   - [Gemini Prompt](#gemini-prompt-translation)
   - [Translation Pair Generation](#translation-pair-generation-prompt)
2. [Benchmark Testing Prompts](#benchmark-testing-prompts)
   - [ChatGPT Prompt](#chatgpt-prompt-benchmark)
   - [Gemini Prompt](#gemini-prompt-benchmark)
   - [Claude Prompt](#claude-prompt-benchmark)

---

# Translation Testing Prompts

## ChatGPT Prompt (Translation)

```
You are creating a high-quality multilingual translation evaluation dataset for the Anote benchmark. I will provide you with 3 parallel translation pairs (source language + English translation). Your task is to generate exactly 6 diverse question-answer pairs that test translation accuracy and comprehension depth.

### INPUT DATA:

[PASTE YOUR 3 TRANSLATION PAIRS HERE]

Example format:
{
  "id": "es_00123",
  "source_lang": "es",
  "target_lang": "en",
  "source_text": "La economía global enfrenta desafíos sin precedentes.",
  "target_text": "The global economy faces unprecedented challenges."
}

### GENERATION REQUIREMENTS:

Create exactly 6 QA items with these distributions:

**Difficulty Distribution:**
- 2 easy (direct lookup, answerable in 5 seconds)
- 2 medium (requires inference or 15 seconds of thought)
- 2 hard (cultural nuance, multi-hop reasoning, or ambiguity)

**Question Type Distribution:**
- 2 factual (retrieve explicit information)
- 2 reasoning (inference, interpretation, comparison)
- 2 ambiguous/challenging (multiple interpretations, complex understanding)

**Register Distribution:**
- 3 formal (academic vocabulary, complete sentences, no contractions)
- 3 informal (conversational tone, contractions OK, casual phrasing)

**Citation Requirements:**
- Include at least 2 citations from source language and 2 from target language
- citation_text MUST be an exact, continuous substring (3-25 words)
- Vary which language you cite from

**Linguistic Coverage (MANDATORY):**
Your 6 items MUST include at least:
- 1 question testing idiomatic expressions or cultural context
- 1 question testing formal/informal register differences
- 1 question testing temporal, modal, or aspectual nuances

### CRITICAL QUALITY RULES:

❌ DO NOT CREATE:
- Questions answerable without reading the translation
- Citations that reproduce the entire source/target text
- Near-duplicate questions with slight rewording
- Answers that just copy citation_text without interpretation

✅ ALWAYS ENSURE:
- Questions sound natural (something a real user would ask)
- citation_text exists verbatim in source_text or target_text
- Answers demonstrate understanding, not just quotation
- Each question tests a different aspect of the translation
- All internal quotation marks use single quotes (')

### OUTPUT FORMAT:

Return ONLY valid JSON (no markdown code blocks, no explanations, no preamble):
[
  {
    "question": "What economic challenges are mentioned in the text?",
    "answer": "The text describes challenges that are unprecedented in nature, affecting the global economy.",
    "cite_from": "target",
    "citation_text": "global economy faces unprecedented challenges",
    "difficulty": "easy",
    "question_type": "factual",
    "register": "formal"
  },
  {
    "question": "How would you casually describe what's happening with the world's money situation?",
    "answer": "Basically, the planet's economy is dealing with some crazy problems we've never seen before.",
    "cite_from": "target",
    "citation_text": "unprecedented challenges",
    "difficulty": "medium",
    "question_type": "reasoning",
    "register": "informal"
  }
]

### VALIDATION CHECKLIST:

Before submitting, verify:
□ Exactly 6 items generated
□ Difficulty: 2 easy, 2 medium, 2 hard
□ Types: 2 factual, 2 reasoning, 2 ambiguous
□ Register: 3 formal, 3 informal
□ At least 2 source citations, 2 target citations
□ Every citation_text is verbatim from the referenced text
□ At least 1 idiom/culture question, 1 register question, 1 temporal/modal question
□ All internal quotes use single quotes (')

Generate the 6 QA items now:
```

---

## Claude Prompt (Translation)

```
I'm building a translation evaluation dataset for the Anote benchmark. You'll receive 3 parallel corpus pairs (original language + English translation). Generate 6 diverse question-answer items that test both translation accuracy and comprehension depth.

<translation_pairs>
[PASTE YOUR 3 TRANSLATION PAIRS HERE]
Example:
{
  "id": "ja_00456",
  "source_lang": "ja",
  "target_lang": "en",
  "source_text": "この技術は将来的に医療分野に革命をもたらす可能性がある。",
  "target_text": "This technology has the potential to revolutionize the medical field in the future."
}

</translation_pairs>

<task_requirements>

Generate exactly 6 QA items following these specifications:

**Difficulty Balance:**
- 2 easy (direct lookup, answerable in 5 seconds)
- 2 medium (requires inference or 15 seconds of thought)
- 2 hard (complex reasoning, cultural nuance, multi-hop logic, or ambiguity resolution)

**Question Type Coverage:**
- 2 factual (retrieving explicit information)
- 2 reasoning (interpretation, comparison, or inference)
- 2 ambiguous/challenging (multiple interpretations, cultural context, or complex understanding)

**Register Variation:**
- 3 formal (academic/professional: no contractions, complete sentences, elevated vocabulary)
- 3 informal (conversational/casual: contractions OK, colloquial language)

**Citation Strategy:**
- Include at least 2 citations from source language and 2 from target language
- Use exact text spans only (continuous substrings, 3-25 words)
- Ensure citation_text is a verbatim substring

**Linguistic Phenomena to Test (MANDATORY):**
Each 6-item set MUST include at least:
- 1 question probing idiomatic expressions or cultural context
- 1 question testing register shifts (formal ↔ informal)
- 1 question examining temporal, modal, or aspectual nuances
</task_requirements>

<critical_requirements>
**FORBIDDEN:**
- Questions answerable without reading the translation
- Citations that reproduce entire source_text or target_text
- Near-duplicate questions with trivial rewording
- Answers that merely repeat citation_text without interpretation

**MANDATORY:**
- Every citation_text must exist verbatim in the referenced source
- Questions must sound natural (realistic user queries)
- Answers must demonstrate comprehension, not just quotation
- Each question must test a distinct aspect of the translation
- All internal quotation marks must use single quotes (')
</critical_requirements>

<output_instructions>
Return a valid JSON array with these specifications:

**Format:** Raw JSON only (no markdown, no code blocks, no preamble, no explanations)
**Encoding:** UTF-8, left-to-right text direction

Each object must include:
- question: Natural, realistic question (10-120 characters)
- answer: Concise, accurate response (50-250 characters, unless yes/no)
- cite_from: "source" or "target"
- citation_text: Exact substring from source_text or target_text (3-25 words)
- difficulty: "easy" | "medium" | "hard"
- question_type: "factual" | "reasoning" | "ambiguous"
- register: "formal" | "informal"
</output_instructions>

<example_output>
[
  {
    "question": "What field could this technology potentially transform?",
    "answer": "This technology could potentially revolutionize the medical field, introducing transformative changes to healthcare practices.",
    "cite_from": "target",
    "citation_text": "revolutionize the medical field",
    "difficulty": "easy",
    "question_type": "factual",
    "register": "formal"
  },
  {
    "question": "So like, what's this tech gonna change in the future?",
    "answer": "It's gonna shake up healthcare down the road, bringing some major changes to how medicine works.",
    "cite_from": "target",
    "citation_text": "revolutionize the medical field in the future",
    "difficulty": "medium",
    "question_type": "reasoning",
    "register": "informal"
  }
]

</example_output>

<validation_checklist>

Before outputting, verify:
□ Exactly 6 items generated
□ Difficulty: 2 easy, 2 medium, 2 hard
□ Types: 2 factual, 2 reasoning, 2 ambiguous
□ Register: 3 formal, 3 informal
□ Citations: ≥2 from source_lang, ≥2 from target_lang
□ Every citation_text exists verbatim in referenced text
□ Linguistic coverage: ≥1 idiom/culture, ≥1 register, ≥1 temporal/modal
□ No questions answerable without translation
□ All questions are unique
□ All internal quotes use single quotes (')
</validation_checklist>

Generate the 6 QA items:
```

---

## Gemini Prompt (Translation)

```
Task: Generate a translation evaluation dataset for the Anote benchmark

You are creating test items for a multilingual translation evaluation system. I will provide 2 parallel translation pairs (source language + English translation). Generate exactly 4 question-answer pairs that test translation quality and comprehension.

---

INPUT TRANSLATION PAIRS:

[PASTE YOUR 2 TRANSLATION PAIRS HERE]

Format example:
{
  "id": "ko_00789",
  "source_lang": "ko",
  "target_lang": "en",
  "source_text": "이 연구는 기후 변화가 생태계에 미치는 영향을 분석했다.",
  "target_text": "This study analyzed the impact of climate change on ecosystems."
}

---

GENERATION REQUIREMENTS:

Create exactly 4 QA items with this distribution:

**Difficulty Distribution:**
- 1 easy (direct lookup, answerable in 5 seconds)
- 2 medium (requires inference or 15 seconds of thought)
- 1 hard (cultural knowledge, multi-hop reasoning, or ambiguity)

**Question Type Distribution:**
- 2 factual (direct information retrieval)
- 1 reasoning (inference/interpretation)
- 1 ambiguous/challenging (complex understanding, multiple valid interpretations)

**Register Distribution:**
- 2 formal (academic vocabulary, no contractions, complete sentences)
- 2 informal (contractions OK, conversational tone, casual phrasing)

**Citation Rules:**
✓ Must include at least 1 citation from source_lang and 1 from target_lang
✓ citation_text must be an exact, continuous substring (3-25 words)
✓ No skipping words within citations

**Linguistic Coverage (REQUIRED):**
Your 4-item set MUST include at least:
- 1 question testing idiomatic meaning or cultural context
- 1 question testing formal/informal register differences

---

CRITICAL QUALITY RULES:

❌ DO NOT CREATE:
- Questions answerable without reading the translation
- Citations that reproduce the entire source/target text
- Near-duplicate questions with trivial rewording
- Answers that just copy citation_text without interpretation

✅ ALWAYS ENSURE:
- Questions sound natural (realistic user queries)
- citation_text exists verbatim in source_text or target_text
- Answers demonstrate understanding beyond quotation
- Each question tests a different translation aspect
- All internal quotation marks use single quotes (')
- Process text left-to-right (not right-to-left)

---

OUTPUT FORMAT:

Provide ONLY valid JSON (no markdown blocks, no explanations, no preamble):

[
  {
    "question": "What topic did the research focus on?",
    "answer": "The research focused on analyzing how climate change impacts ecosystems, examining their interconnected relationship.",
    "cite_from": "target",
    "citation_text": "analyzed the impact of climate change on ecosystems",
    "difficulty": "easy",
    "question_type": "factual",
    "register": "formal"
  },
  {
    "question": "What were they studying in this research?",
    "answer": "They were looking at what climate change does to ecosystems and how it affects them.",
    "cite_from": "target",
    "citation_text": "impact of climate change on ecosystems",
    "difficulty": "medium",
    "question_type": "reasoning",
    "register": "informal"
  },
  {
    "question": "Based on the study's scope, what environmental relationship was being investigated?",
    "answer": "The relationship between climate change phenomena and ecological system stability was under investigation, exploring causative dynamics.",
    "cite_from": "target",
    "citation_text": "climate change on ecosystems",
    "difficulty": "hard",
    "question_type": "ambiguous",
    "register": "formal"
  },
  {
    "question": "So they were checking out how weather changes mess with nature?",
    "answer": "Yeah, basically how climate shifts affect natural ecosystems and the environments where organisms live.",
    "cite_from": "target",
    "citation_text": "impact of climate change on ecosystems",
    "difficulty": "medium",
    "question_type": "factual",
    "register": "informal"
  }
]

---

VALIDATION CHECKLIST:

Before submitting, verify:
□ Exactly 4 items generated
□ Difficulty: 1 easy, 2 medium, 1 hard
□ Types: 2 factual, 1 reasoning, 1 ambiguous
□ Register: 2 formal, 2 informal
□ At least 1 source-language citation, 1 target-language citation
□ Every citation_text exists verbatim in referenced text
□ At least 1 question addresses idioms/culture, 1 addresses register
□ No questions answerable without translation
□ All questions are unique
□ All internal quotes use single quotes (')

Generate the 4 QA items now:
```

---

## Translation Pair Generation Prompt

```
Generate 50 high-quality parallel translation pairs for [Spanish/Hebrew/Japanese/Korean].

Requirements:
- Mix of domains: news, literature, casual conversation, technical
- Mix of registers: formal and informal
- Sentence length: 15-40 words
- Include some idiomatic expressions
- Include some culturally specific content

Output as JSON array:
[
  {
    "id": "es_001",
    "source_lang": "es",
    "target_lang": "en",
    "source_text": "...",
    "target_text": "..."
  }
]
```

---

# Benchmark Testing Prompts

## ChatGPT Prompt (Benchmark)

```
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
```

---

## Gemini Prompt (Benchmark)

```
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
```

---

## Claude Prompt (Benchmark)

```
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
```

---

## Notes on Prompt Usage

### Translation Testing Dataset
- Generated 400 items total (100 per language)
- Used ChatGPT (144 items), Claude (144 items), Gemini (112 items)
- Each model processed different translation pairs to reduce bias
- Generation date: 2025-11-21

### Benchmark Testing Dataset
- Generated 396 items total (99 per language)
- Used ChatGPT (132 items), Claude (132 items), Gemini (132 items)
- Items created from benchmark_chunks corpus
- Generation date: 2025-12-02

### Quality Control
- All items include exact citation_text validation
- Multi-model generation reduces single-model bias
- Difficulty and question type distributions maintained across languages
- Manual spot-checking performed on 10% of generated items
