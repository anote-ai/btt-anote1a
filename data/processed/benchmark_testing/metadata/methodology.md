# Benchmark Testing Methodology

## Overview
This document describes the methodology for generating the Multilingual Benchmark Testing Dataset, a QA-citation evaluation resource covering 4 languages (Spanish, Hebrew, Japanese, Korean) and 3 LLM models (ChatGPT, Claude, Gemini).

## Phase 1: Source Preparation
- Scan existing `translation_testing` directory structure
- Load source JSONL files per language per model
- Extract entities, periods, topics, snippets from source items
- Validate JSONL integrity and skip malformed records

## Phase 2: QA Generation
- For each source item, synthesize 3 QA types (factual, reasoning, ambiguous)
- Use multilingual templates with slot filling (entity, period, value, etc.)
- Maintain uniqueness via deterministic randomization (seeded by lang, model, batch)
- Vary difficulty and register (formal/informal) across items

## Phase 3: Batch Assembly
- Distribute generated items into 6 batches per model per language
- 6 items per batch file (36 items per model per language)
- Ensure balanced representation of question types and difficulty levels

## Phase 4: Validation
- Check JSONL schema completeness for each item
- Verify citation_text is substring of source text
- Confirm language tag consistency
- Deduplicate Q-A pairs

## Phase 5: Merging & Metadata
- Create merged JSONL files (all, by-model, by-language)
- Generate summary statistics
- Write dataset card, generation prompts, and methodology documentation

## Quality Assurance
- All questions are distinct within a batch
- All answers map to cited text snippets
- Multilingual consistency across languages
- Difficulty and type distribution balanced

## Citation Grounding
All items include:
- `citation_text`: Exact substring from source
- `cite_from`: Label (source or target)
- Verifiable mapping between answer and citation

## Known Limitations
- Synthetic generation may not capture all edge cases
- Domain coverage limited to source corpus scope
- Potential model-specific biases in LLM outputs
