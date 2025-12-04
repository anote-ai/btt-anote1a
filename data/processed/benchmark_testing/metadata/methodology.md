# Benchmark Testing Dataset — Methodology

Overview  
This dataset contains 360 question-answer-citation items (90 per language) created from benchmark_chunks for citation-aware multilingual evaluation across Spanish, Hebrew, Japanese, and Korean.

Dataset Generation Process

Phase 1 — Chunk Selection
- Source: data/processed/benchmark_chunks.
- Per language: deterministically sample 30 source chunks (seeded sampling to ensure reproducibility).
- Criteria: diverse domains and registers where available; prefer chunks with explicit citation_text or source metadata.

Phase 2 — QA Item Generation
- For each selected chunk produce 3 QA/citation items (factual, reasoning, ambiguous) using language-specific templates grounded in the chunk text.
- Per-language totals: 30 chunks × 3 items = 90 items.
- Model assignment (to reduce single-model bias): divide the 30 chunks per language among the three model labels:
  - chatgpt: chunks 1–10 → 30 items
  - claude:  chunks 11–20 → 30 items
  - gemini:  chunks 21–30 → 30 items
- Batching: group generated items into 5 batches per model/language (6 items per batch). Files named batch_{model}_01..05.json(.jsonl).

Quality Control
- All source JSONL lines are validated; malformed lines are skipped.
- Empty or malformed batch files are quarantined for inspection; non-empty batches are required.
- Each QA item includes an exact citation_text (from source when available) and a cite_from tag ("source" or "target").
- Items include metadata: difficulty (easy/medium/hard), question_type (factual/reasoning/ambiguous), register (formal/informal), model, batch_id, generated_date.
- Deterministic seeding per (language, model, batch) is used to ensure reproducibility and minimise accidental duplicates.
- No human validation is assumed by default; human review recommended before high-stakes use.

Dataset Statistics
- Expected totals (example): total_items = 360 (4 languages × 3 models × 5 batches × 6 items).
- Concrete counts and distributions are recorded in metadata/summary_stats.json after merging.

File Structure
- Per-language/per-model batches:
  data/processed/benchmark_testing/{lang}/{model}_batches/batch_{model}_01..05.json(.jsonl)
- Merged outputs:
  data/processed/benchmark_testing/merged/benchmark_testing_{lang}.jsonl  
  data/processed/benchmark_testing/merged/benchmark_testing_{model}.jsonl  
  data/processed/benchmark_testing/merged/benchmark_testing_all.jsonl
- Metadata:
  data/processed/benchmark_testing/metadata/{dataset_card.md, generation_prompts.md, methodology.md, summary_stats.json}

Reproducibility & Scripts
- Key scripts:
  - scripts/mirror_translation_to_benchmark.py (synthesis/mirroring logic)
  - scripts/ensure_benchmark_batches.py (batch creation guarantees)
  - scripts/remove_empty_batches.py (quarantine empty/malformed files)
  - scripts/merge_benchmark_batches.py (merge + stats)
- Generation is seeded and timestamped; include seed and generated_date in provenance fields.

Limitations
- Items are synthesized from chunks with deterministic templates and fallback values when metadata is missing.
- Dataset is limited to four languages and three model labels; model-generated ground truth can contain noise.
- Human validation is recommended for tasks requiring gold-standard answers.

Usage
- Use merged files under data/processed/benchmark_testing/merged/ for evaluation pipelines and analysis.
- Consult metadata/summary_stats.json for final counts and distributions.
