# Translation Testing Dataset - Methodology

## Overview
This dataset contains 400 question-answer pairs for evaluating translation quality across 4 languages.

## Dataset Generation Process

### Phase 1: Translation Pair Generation
- Used Claude Sonnet 4.5 to generate 50 high-quality parallel translation pairs per language
- Criteria: diverse domains, varied registers, 15-40 words, idiomatic expressions
- Languages: Spanish, Hebrew, Japanese, Korean

### Phase 2: QA Item Generation
- Split 50 pairs among 3 models:
  - ChatGPT-4.1: Pairs 1-18 (6 runs × 3 pairs) → 36 items
  - Claude Sonnet 4.5: Pairs 19-36 (6 runs × 3 pairs) → 36 items
  - Gemini 2.5 Flash: Pairs 37-50 (7 runs × 2 pairs) → 28 items
- Total: 100 items per language

### Quality Controls
- Each QA item includes:
  - Exact citation from source/target text
  - Difficulty level (easy/medium/hard)
  - Question type (factual/reasoning/ambiguous)
  - Register (formal/informal)
- Multi-model generation reduces single-model bias

## Dataset Statistics
See `summary_stats.json` for full breakdown.

## File Structure
See main README.md

## Usage
See `../data/processed/translation_testing/merged/` for final datasets.