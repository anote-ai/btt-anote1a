import json
import os
from pathlib import Path

stats_report = []

# 1. Translation Dataset Stats
stats_report.append("## Translation Testing Dataset\n")
trans_stats_path = 'data/processed/translation_testing/metadata/summary_stats.json'
if os.path.exists(trans_stats_path):
    with open(trans_stats_path, 'r') as f:
        trans_stats = json.load(f)
    
    stats_report.append(f"- **Total Items:** {trans_stats['total_items']}")
    
    # Handle languages
    if 'languages' in trans_stats:
        lang_names = {'es': 'Spanish', 'he': 'Hebrew', 'ja': 'Japanese', 'ko': 'Korean'}
        langs = [lang_names.get(code, code) for code in trans_stats['languages'].keys()]
        stats_report.append(f"- **Languages:** {', '.join(langs)}")
    
    # Handle difficulty distribution
    if 'difficulty' in trans_stats:
        stats_report.append(f"- **Difficulty Distribution:**")
        for diff, info in trans_stats['difficulty'].items():
            count = info['count']
            pct = info['percentage']
            stats_report.append(f"  - {diff.capitalize()}: {count} ({pct:.1f}%)")
    
    # Handle models
    if 'models' in trans_stats:
        stats_report.append(f"- **Models:**")
        for model, info in trans_stats['models'].items():
            count = info['count']
            stats_report.append(f"  - {model.upper()}: {count} test cases")
else:
    stats_report.append("- Translation stats file not found")

# 2. Multilingual Benchmark Stats
stats_report.append("\n## Multilingual Benchmark Chunks\n")

benchmark_files = {
    'Spanish': 'data/processed/benchmark_chunks/benchmark_es.jsonl',
    'Hebrew': 'data/processed/benchmark_chunks/benchmark_he.jsonl',
    'Korean': 'data/processed/benchmark_chunks/benchmark_ko.jsonl',
    'Japanese': 'data/processed/benchmark_chunks/benchmark_ja.jsonl'
}

total_chunks = 0
for lang, filepath in benchmark_files.items():
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            count = sum(1 for _ in f)
            total_chunks += count
            stats_report.append(f"- **{lang}:** {count:,} chunks")

stats_report.append(f"\n**Total Benchmark Chunks:** {total_chunks:,}")

# 3. RAG System Stats
stats_report.append("\n## RAG System\n")
stats_report.append("- **Anote Documentation Chunks:** 135")
stats_report.append("- **Embedding Model:** HuggingFace all-MiniLM-L6-v2")
stats_report.append("- **Vector DB:** ChromaDB")
stats_report.append("- **LLM Providers Supported:** Claude, OpenAI, Ollama")

# 4. Multilingual QA Pairs
stats_report.append("\n## Multilingual QA Pairs\n")
# Count QA pairs from merged benchmark testing files
qa_stats = {
    'Spanish': 'data/processed/benchmark_testing/merged/benchmark_testing_es.jsonl',
    'Hebrew': 'data/processed/benchmark_testing/merged/benchmark_testing_he.jsonl',
    'Korean': 'data/processed/benchmark_testing/merged/benchmark_testing_ko.jsonl',
    'Japanese': 'data/processed/benchmark_testing/merged/benchmark_testing_ja.jsonl'
}

total_qa = 0
for lang, filepath in qa_stats.items():
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            count = sum(1 for _ in f)
            total_qa += count
            stats_report.append(f"- **{lang}:** {count} QA pairs")

if total_qa > 0:
    stats_report.append(f"\n**Total QA Pairs:** {total_qa:,}")

# 5. Additional Statistics from merged files
stats_report.append("\n## Dataset Breakdown by LLM Provider\n")
llm_files = {
    'ChatGPT': 'data/processed/benchmark_testing/merged/benchmark_testing_chatgpt.jsonl',
    'Claude': 'data/processed/benchmark_testing/merged/benchmark_testing_claude.jsonl',
    'Gemini': 'data/processed/benchmark_testing/merged/benchmark_testing_gemini.jsonl'
}

for llm, filepath in llm_files.items():
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            count = sum(1 for _ in f)
            stats_report.append(f"- **{llm}:** {count} test cases")

# Write report
with open('DATASET_STATISTICS.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(stats_report))

print("Statistics report generated successfully!")
print(f"Total sections: {len([s for s in stats_report if s.startswith('##')])}")
