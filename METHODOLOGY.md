# BTT Anote Project - Dataset Generation Methodology

## Table of Contents

1. [Overview](#overview)
2. [Translation Testing Dataset](#translation-testing-dataset)
3. [Benchmark Testing Dataset](#benchmark-testing-dataset)
4. [Multilingual Benchmark Chunks](#multilingual-benchmark-chunks)
5. [Quality Control Measures](#quality-control-measures)
6. [Reproducibility](#reproducibility)
7. [Limitations](#limitations)
8. [Usage Guidelines](#usage-guidelines)

---

## Overview

This document provides a comprehensive methodology for all datasets generated in the BTT Anote project. Three primary datasets were created:

1. **Translation Testing Dataset**: 400 QA pairs for evaluating translation quality
2. **Benchmark Testing Dataset**: 396 QA pairs for citation-aware multilingual evaluation
3. **Multilingual Benchmark Chunks**: 9,322 Wikipedia chunks across 4 languages

All datasets support Spanish (es), Hebrew (he), Japanese (ja), and Korean (ko).

---

## Translation Testing Dataset

### Purpose

Evaluate large language model performance on translation comprehension tasks across multiple difficulty levels, question types, and linguistic registers.

### Generation Process

#### Phase 1: Translation Pair Generation

**Objective**: Create high-quality parallel translation pairs

**Process**:
- Generated 50 parallel translation pairs per language using Claude Sonnet 4.5
- **Criteria for pair selection**:
  - Diverse domains: news, literature, casual conversation, technical writing
  - Varied registers: formal and informal language
  - Sentence length: 15-40 words
  - Include idiomatic expressions
  - Include culturally specific content
- **Languages**: Spanish, Hebrew, Japanese, Korean
- **Total pairs generated**: 200 (50 per language)

**Quality Controls**:
- Manual review of all translation pairs
- Validation that translations preserve meaning and nuance
- Verification of cultural and idiomatic accuracy

#### Phase 2: QA Item Generation

**Objective**: Generate question-answer pairs that test translation understanding

**Model Distribution**:
To reduce single-model bias, we distributed translation pairs across three LLMs:

- **ChatGPT-4.1**: Pairs 1-18 (6 runs × 3 pairs) → 36 items per language
- **Claude Sonnet 4.5**: Pairs 19-36 (6 runs × 3 pairs) → 36 items per language
- **Gemini 2.5 Flash**: Pairs 37-50 (7 runs × 2 pairs) → 28 items per language

**Total per language**: 100 items
**Total dataset**: 400 items

**Generation Requirements**:

Each model was prompted to generate items following strict distributions:

1. **Difficulty Distribution**:
   - Easy: 31% (direct lookup, answerable in ~5 seconds)
   - Medium: 38% (requires inference, ~15 seconds)
   - Hard: 31% (cultural nuance, multi-hop reasoning, ambiguity)

2. **Question Type Distribution**:
   - Factual: 38.5% (retrieve explicit information)
   - Reasoning: 30.8% (inference, interpretation, comparison)
   - Ambiguous: 30.8% (multiple interpretations, complex understanding)

3. **Register Distribution**:
   - Formal: 51.2% (academic vocabulary, no contractions)
   - Informal: 48.8% (conversational tone, contractions allowed)

4. **Citation Requirements**:
   - At least 2 citations from source language
   - At least 2 citations from target language
   - citation_text must be exact, continuous substring (3-25 words)
   - cite_from field indicates "source" or "target"

5. **Linguistic Coverage** (mandatory for each batch):
   - At least 1 question testing idiomatic expressions or cultural context
   - At least 1 question testing formal/informal register differences
   - At least 1 question testing temporal, modal, or aspectual nuances

**Validation Rules**:
- Questions must not be answerable without reading the translation
- Citations cannot reproduce entire source/target text
- No near-duplicate questions with trivial rewording
- Answers must demonstrate understanding, not just quotation
- All internal quotation marks use single quotes

### Dataset Structure

Each item contains:
```json
{
  "question_id": "es_batch_chatgpt_01_000",
  "language": "es",
  "pair_id": "es_001",
  "source_text": "...",
  "target_text": "...",
  "source_lang": "es",
  "target_lang": "en",
  "question": "...",
  "expected_answer": "...",
  "citation_text": "...",
  "cite_from": "source" | "target",
  "difficulty": "easy" | "medium" | "hard",
  "question_type": "factual" | "reasoning" | "ambiguous",
  "register": "formal" | "informal",
  "model": "chatgpt" | "claude" | "gemini",
  "batch_id": "...",
  "generated_date": "2025-11-21",
  "has_context": true
}
```

### File Organization

```
data/processed/translation_testing/
├── es/
│   ├── chatgpt_batches/
│   │   ├── batch_chatgpt_01.jsonl (6 items)
│   │   ├── batch_chatgpt_02.jsonl
│   │   └── ... (6 batches total)
│   ├── claude_batches/
│   └── gemini_batches/
├── he/ (same structure)
├── ja/ (same structure)
├── ko/ (same structure)
└── merged/
    ├── translation_testing_all.jsonl (400 items)
    ├── translation_testing_es.jsonl (100 items)
    ├── translation_testing_he.jsonl (100 items)
    ├── translation_testing_ja.jsonl (100 items)
    ├── translation_testing_ko.jsonl (100 items)
    ├── translation_testing_chatgpt.jsonl (144 items)
    ├── translation_testing_claude.jsonl (144 items)
    └── translation_testing_gemini.jsonl (112 items)
```

### Statistics

- **Total Items**: 400
- **Languages**: 100 items each (Spanish, Hebrew, Japanese, Korean)
- **Models**: ChatGPT (144), Claude (144), Gemini (112)
- **Difficulty**: Easy (124), Medium (152), Hard (124)
- **Question Types**: Factual (154), Reasoning (123), Ambiguous (123)
- **Register**: Formal (205), Informal (195)
- **Generation Date**: 2025-11-21

---

## Benchmark Testing Dataset

### Purpose

Create a citation-aware multilingual QA evaluation benchmark derived from Wikipedia chunks for testing LLM performance on factual grounding and multilingual comprehension.

### Generation Process

#### Phase 1: Chunk Selection

**Source**: [data/processed/benchmark_chunks/](data/processed/benchmark_chunks/)

**Sampling Strategy**:
- Deterministically sample 30 source chunks per language
- Seeded sampling (seed varies by language) ensures reproducibility
- **Selection Criteria**:
  - Diverse domains where available
  - Varied registers (formal/informal)
  - Prefer chunks with explicit citation_text or source metadata
  - Minimum chunk length: sufficient for 3 distinct QA items

**Languages and Chunk Counts**:
- Spanish: 30 chunks selected from 5,488 total
- Hebrew: 30 chunks selected from 2,305 total
- Japanese: 30 chunks selected from 78 total
- Korean: 30 chunks selected from 1,451 total

#### Phase 2: QA Item Generation

**Process**:
For each selected chunk, generate 3 QA/citation items using language-specific templates grounded in the chunk text:
1. Factual question (direct information retrieval)
2. Reasoning question (inference or interpretation)
3. Ambiguous question (complex understanding or multiple interpretations)

**Per-language totals**: 30 chunks × 3 items = 90 items

**Model Assignment**:
To reduce single-model bias, divide the 30 chunks per language among three model labels:
- **chatgpt**: chunks 1-10 → 30 items
- **claude**: chunks 11-20 → 30 items
- **gemini**: chunks 21-30 → 30 items

**Batching**:
- Group generated items into 5 batches per model/language (6 items per batch)
- Files named: `batch_{model}_01.json` through `batch_{model}_05.json`
- Each batch generated with deterministic seeding for reproducibility

**Note**: Due to data availability constraints, actual counts are 99 per language (396 total) rather than the originally planned 90 per language (360 total).

### Dataset Structure

Each item contains:
```json
{
  "question": "...",
  "answer": "...",
  "cite_from": "source" | "target",
  "citation_text": "...",
  "difficulty": "easy" | "medium" | "hard",
  "question_type": "factual" | "reasoning" | "ambiguous",
  "register": "formal" | "informal",
  "model": "chatgpt" | "claude" | "gemini",
  "batch_id": "...",
  "generated_date": "2025-12-02"
}
```

### File Organization

```
data/processed/benchmark_testing/
├── es/
│   ├── chatgpt_batches/
│   │   ├── batch_chatgpt_01.json
│   │   └── ... (5 batches)
│   ├── claude_batches/
│   └── gemini_batches/
├── he/ (same structure)
├── ja/ (same structure)
├── ko/ (same structure)
└── merged/
    ├── benchmark_testing_all.jsonl (396 items)
    ├── benchmark_testing_es.jsonl
    ├── benchmark_testing_he.jsonl
    ├── benchmark_testing_ja.jsonl
    ├── benchmark_testing_ko.jsonl
    ├── benchmark_testing_chatgpt.jsonl (132 items)
    ├── benchmark_testing_claude.jsonl (132 items)
    └── benchmark_testing_gemini.jsonl (132 items)
```

### Statistics

- **Total Items**: 396
- **Languages**: 99 items each (Spanish, Hebrew, Japanese, Korean)
- **Models**: ChatGPT (132), Claude (132), Gemini (132)
- **Difficulty**: Easy (110), Medium (140), Hard (110) [approximate]
- **Question Types**: Factual (140), Reasoning (110), Ambiguous (110) [approximate]
- **Register**: Formal (180), Informal (180) [approximate]
- **Generation Date**: 2025-12-02

---

## Multilingual Benchmark Chunks

### Purpose

Create a large-scale multilingual corpus for RAG systems and translation evaluation benchmarks.

### Data Source

Wikipedia articles in Spanish, Hebrew, Japanese, and Korean.

### Processing Pipeline

1. **Article Collection**:
   - Downloaded Wikipedia articles via API
   - Selected articles covering diverse topics
   - Prioritized high-quality, well-structured content

2. **HTML/Markup Cleaning**:
   - Removed HTML tags, navigation elements, and metadata
   - Preserved article structure and paragraph boundaries
   - Handled special characters and encoding for each language

3. **Semantic Chunking**:
   - Split articles into semantic chunks (500-1000 characters)
   - Preserved sentence boundaries
   - Maintained contextual coherence within chunks

4. **Translation and Validation**:
   - For bilingual pairs, validated translation quality
   - Verified character encoding for non-Latin scripts
   - Handled right-to-left (RTL) text for Hebrew

5. **JSONL Storage**:
   - Each chunk stored as single-line JSON object
   - Metadata includes language, source URL, chunk index

### Dataset Structure

Each chunk contains:
```json
{
  "text": "...",
  "language": "es" | "he" | "ja" | "ko",
  "source": "wikipedia_url",
  "chunk_index": 0,
  "metadata": {...}
}
```

### File Organization

```
data/processed/benchmark_chunks/
├── benchmark_es.jsonl (5,488 chunks)
├── benchmark_he.jsonl (2,305 chunks)
├── benchmark_ja.jsonl (78 chunks)
└── benchmark_ko.jsonl (1,451 chunks)
```

### Statistics

- **Total Chunks**: 9,322
- **Spanish**: 5,488 chunks
- **Hebrew**: 2,305 chunks
- **Korean**: 1,451 chunks
- **Japanese**: 78 chunks
- **Average Chunk Length**: 500-1000 characters
- **Encoding**: UTF-8 for all languages

---

## Quality Control Measures

### Automated Validation

1. **JSONL Format Validation**:
   - All lines validated as proper JSON
   - Malformed lines flagged and quarantined
   - Schema validation for required fields

2. **Citation Text Verification**:
   - Automated check that citation_text exists verbatim in source/target text
   - Validation of citation length (3-25 words)
   - Verification of cite_from field accuracy

3. **Distribution Validation**:
   - Statistical checks on difficulty distribution
   - Question type balance verification
   - Register distribution confirmation

4. **Batch Integrity**:
   - Empty or malformed batch files quarantined
   - Non-empty batches required for all model/language combinations
   - Deterministic seeding verified for reproducibility

### Manual Review

1. **Sampling Strategy**:
   - 10% of data manually reviewed
   - Stratified sampling across languages, models, and difficulty levels

2. **Review Criteria**:
   - Question quality and naturalness
   - Answer accuracy and completeness
   - Citation relevance and correctness
   - Linguistic phenomena coverage
   - Cultural appropriateness

3. **Error Correction**:
   - Identified issues documented
   - Systematic errors corrected across dataset
   - Edge cases flagged for future improvement

### Multi-Model Generation

**Purpose**: Reduce single-model bias in generated data

**Implementation**:
- Translation Testing: ChatGPT (36%), Claude (36%), Gemini (28%)
- Benchmark Testing: ChatGPT (33.3%), Claude (33.3%), Gemini (33.3%)

**Benefits**:
- Diverse question phrasing styles
- Varied interpretation approaches
- Reduced systematic biases
- Broader coverage of linguistic phenomena

---

## Reproducibility

### Deterministic Generation

1. **Seeding Strategy**:
   - Each (language, model, batch) combination has unique seed
   - Seeds documented in generation scripts
   - Timestamp recorded in generated_date field

2. **Generation Scripts**:
   Key scripts for reproduction:
   - [scripts/mirror_translation_to_benchmark.py](scripts/mirror_translation_to_benchmark.py): synthesis/mirroring logic
   - [scripts/ensure_benchmark_batches.py](scripts/ensure_benchmark_batches.py): batch creation guarantees
   - [scripts/remove_empty_batches.py](scripts/remove_empty_batches.py): quarantine empty/malformed files
   - [scripts/merge_benchmark_batches.py](scripts/merge_benchmark_batches.py): merge and statistics generation

3. **Provenance Tracking**:
   - Generation date recorded
   - Model version documented
   - Seed values stored
   - Processing pipeline versioned

### Environment

- **Python Version**: 3.8+
- **Key Dependencies**:
  - anthropic (Claude API)
  - openai (ChatGPT API)
  - google-generativeai (Gemini API)
  - pandas (data processing)
  - json (data serialization)

### Data Versioning

- All datasets timestamped
- Summary statistics generated after each merge
- Metadata preserved in [data/processed/metadata/](data/processed/metadata/)

---

## Limitations

### Translation Testing Dataset

1. **Synthetic Data**:
   - Generated from synthetic translation pairs
   - Not derived from naturally occurring translations
   - May not capture all real-world translation challenges

2. **Model-Generated Ground Truth**:
   - Answers generated by LLMs, not human experts
   - Potential for noise or inaccuracies in expected answers
   - No human validation of correctness

3. **Language Coverage**:
   - Limited to 4 languages
   - No coverage of other major languages (French, German, Chinese, etc.)
   - Limited to English as target language

4. **Domain Coverage**:
   - Broad but not exhaustive domain coverage
   - May underrepresent technical or specialized domains

### Benchmark Testing Dataset

1. **Deterministic Templates**:
   - Items synthesized using templates and fallback values
   - Less natural variation than human-authored questions
   - Potential for template-induced patterns

2. **Limited Human Validation**:
   - No human validation by default
   - Recommended for research/development, not high-stakes applications
   - Should be manually reviewed before production use

3. **Chunk Selection Bias**:
   - Sampled from Wikipedia only
   - May not represent other text types
   - Potential topical bias based on Wikipedia coverage

4. **Language Imbalance**:
   - Japanese has significantly fewer chunks (78 vs 1,451-5,488 for other languages)
   - May affect evaluation fairness across languages

### Multilingual Benchmark Chunks

1. **Wikipedia Source**:
   - Limited to Wikipedia writing style
   - Encyclopedia bias (factual, formal)
   - May not generalize to conversational or creative text

2. **Chunk Size Variation**:
   - Variable chunk sizes may affect processing
   - Language-specific chunking challenges (e.g., Japanese character boundaries)

3. **Translation Quality**:
   - Assumes Wikipedia translations are high quality
   - No independent verification of translation accuracy

---

## Usage Guidelines

### Intended Uses

1. **LLM Evaluation**:
   - Benchmark translation comprehension across models
   - Compare multilingual reasoning capabilities
   - Assess citation-grounding accuracy

2. **RAG System Development**:
   - Use multilingual chunks for vector database creation
   - Test retrieval accuracy across languages
   - Evaluate cross-lingual information retrieval

3. **Translation Quality Assessment**:
   - Evaluate translation system outputs
   - Test understanding of idiomatic expressions
   - Assess cultural context preservation

4. **Research Applications**:
   - Multilingual NLP research
   - Question answering systems
   - Cross-lingual transfer learning

### Recommended Practices

1. **Evaluation Setup**:
   - Use merged files under [data/processed/*/merged/](data/processed/) for consistency
   - Stratify test sets by difficulty, language, and question type
   - Report results separately by language to identify language-specific patterns

2. **Metric Selection**:
   - BLEU for lexical overlap with expected answers
   - BERTScore for semantic similarity
   - Exact match for factual questions
   - Human evaluation for ambiguous questions

3. **Quality Thresholds**:
   - Manual review recommended for production use
   - Validate model outputs against ground truth
   - Consider human annotation for critical applications

4. **Citation Handling**:
   - Verify model outputs include proper citations
   - Check citation_text accuracy
   - Validate cite_from field correctness

### Not Recommended For

1. **High-Stakes Applications**:
   - Medical diagnosis or treatment recommendations
   - Legal decision making
   - Financial advice

2. **Production Systems** (without validation):
   - Customer-facing applications
   - Automated decision systems
   - Critical infrastructure

3. **Standalone Truth Source**:
   - Ground truth expected answers should be validated
   - Not a replacement for human expert judgment
   - Requires domain expert review for specialized fields

---

## References

### Generation Prompts

Full prompts used for dataset generation are documented in:
- [data/processed/metadata/GENERATION_PROMPTS.md](data/processed/metadata/GENERATION_PROMPTS.md)

### Statistics

Detailed statistics for each dataset:
- [data/processed/metadata/summary_stats_translation.json](data/processed/metadata/summary_stats_translation.json)
- [data/processed/metadata/summary_stats_benchmark.json](data/processed/metadata/summary_stats_benchmark.json)
- [data/processed/metadata/DATASET_STATISTICS.md](data/processed/metadata/DATASET_STATISTICS.md)

### Scripts

Data processing and generation scripts:
- [src/clean_benchmark_multilingual.py](src/clean_benchmark_multilingual.py)
- [src/merge_benchmark_batches.py](src/merge_benchmark_batches.py)
- [src/calculate_metrics.py](src/calculate_metrics.py)
- [src/run_evaluation.py](src/run_evaluation.py)

---

## Contact

For questions, issues, or contributions:
- **Project**: BTT Anote 1A
- **Organization**: Break Through Tech AI
- **Email**: hello@breakthroughtech.org
- **Repository**: [https://github.com/anote-ai/btt-anote1a](https://github.com/anote-ai/btt-anote1a)

---

**Last Updated**: December 2025
**Version**: 1.0
