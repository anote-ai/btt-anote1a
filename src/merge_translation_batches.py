"""
Merge translation testing dataset batches
Creates language-specific, combined, and model-specific JSONL files
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from collections import defaultdict

def load_batch_file(file_path: Path) -> List[Dict]:
    """Load JSON or JSONL batch file"""
    items = []

    # JSONL first (line-by-line)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    items.append(json.loads(line))
        return items
    except json.JSONDecodeError:
        pass

    # regular JSON (array)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return [data]
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

def add_metadata(item: Dict, model: str, batch_id: str) -> Dict:
    """Add metadata fields to each item"""
    item['model'] = model
    item['batch_id'] = batch_id
    item['generated_date'] = datetime.now().strftime('%Y-%m-%d')
    return item

def extract_language_from_id(item: Dict) -> str:
    """
    Extract language code from various possible ID fields
    -> mainly for validation since language is given on folder path
    """
    # Try multiple fields in order of preference
    for field in ['original_pair_id', 'pair_id', 'id', 'question_id']:
        if field in item and item[field]:
            parts = str(item[field]).split('_')
            if len(parts) > 0:
                lang_code = parts[0].lower()
                if lang_code in ['es', 'he', 'ja', 'ko']:
                    return lang_code

    return 'unknown'

def merge_batches(base_dir: Path, output_dir: Path):
    """
    Merge all batch files into:
    1. Language-specific files (es, he, ja, ko)
    2. Combined all-languages file
    3. Model-specific files (optional)
    4. Summary statistics

    Assumes structure: base_dir/{lang}/{model}_batches/batch_*.json(l)
    """

    # Define languages and models
    languages = ['es', 'he', 'ja', 'ko']
    models = ['chatgpt', 'claude', 'gemini']

    # Storage for items by language and model
    items_by_language = defaultdict(list)
    items_by_model = defaultdict(list)
    all_items = []

    print("~" * 50)
    print("MERGING TRANSLATION TESTING DATASET BATCHES")

    # Process language folders
    for lang in languages:
        lang_folder = base_dir / lang

        if not lang_folder.exists():
            print(f"\nWarning: {lang}/ folder not found, skipping...")
            continue

        print(f"\n📁 Processing {lang.upper()} language folder...")

        # Process each model's batches within this language
        for model_name in models:
            batch_folder = lang_folder / f"{model_name}_batches"

            if not batch_folder.exists():
                print(f"{model_name}_batches not found in {lang}/, skipping...")
                continue

            print(f"   📂 {model_name.upper()} batches...")

            # Try both .jsonl and .json extensions
            batch_files = list(batch_folder.glob('batch_*.jsonl'))
            batch_files.extend(batch_folder.glob('batch_*.json'))
            batch_files = sorted(set(batch_files))

            if not batch_files:
                print(f"      No batch files found in {batch_folder.name}")
                continue

            for batch_file in batch_files:
                batch_id = f"{lang}_{batch_file.stem}"
                print(f"      Loading {batch_file.name}...", end=' ')

                try:
                    items = load_batch_file(batch_file)
                    print(f"✓ ({len(items)} items)")

                    # Add metadata and store
                    for item in items:
                        item = add_metadata(item, model_name, batch_id)

                        items_by_language[lang].append(item)
                        items_by_model[model_name].append(item)
                        all_items.append(item)

                except Exception as e:
                    print(f"✗ Error: {e}")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "~" * 50)
    print("SAVING MERGED FILES")

    # 1. language-specific
    print("\n Creating language-specific files...")
    languages = ['es', 'he', 'ja', 'ko']
    lang_stats = {}

    for lang in languages:
        if lang in items_by_language:
            output_file = output_dir / f"translation_testing_{lang}.jsonl"
            items = items_by_language[lang]

            with open(output_file, 'w', encoding='utf-8') as f:
                for item in items:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')

            lang_stats[lang] = len(items)
            print(f"   ✓ {lang.upper()}: {len(items)} items → {output_file.name}")
        else:
            print(f"{lang.upper()}: No items found")

    # 2. combined
    print("\nCreating combined file...")
    combined_file = output_dir / "translation_testing_all.jsonl"
    with open(combined_file, 'w', encoding='utf-8') as f:
        for item in all_items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"   ✓ ALL LANGUAGES: {len(all_items)} items → {combined_file.name}")

    # 3. model-specific
    print("\nCreating model-specific files...")
    for model_name, items in items_by_model.items():
        if items:
            output_file = output_dir / f"translation_testing_{model_name}.jsonl"
            with open(output_file, 'w', encoding='utf-8') as f:
                for item in items:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
            print(f"   ✓ {model_name.upper()}: {len(items)} items → {output_file.name}")

    # stats
    print("\n" + "~" * 50)
    print("SUMMARY STATISTICS")

    stats = generate_statistics(all_items, lang_stats, items_by_model)

    # Save stats to JSON
    metadata_dir = output_dir.parent.parent.parent / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    stats_file = metadata_dir / "summary_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Statistics saved to: {stats_file}")

    print("\n" + "~" * 50)
    print("✓ MERGE COMPLETE")

    print(f"\nOutput location: {output_dir}")

def generate_statistics(all_items: List[Dict], lang_stats: Dict, model_stats: Dict) -> Dict:
    """Generate and print comprehensive statistics"""

    stats = {
        'total_items': len(all_items),
        'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'languages': {},
        'models': {},
        'difficulty': {},
        'question_types': {},
        'register': {}
    }

    # Language distribution
    print("\nBy Language:")
    for lang, count in sorted(lang_stats.items()):
        pct = (count / len(all_items)) * 100 if all_items else 0
        print(f"   {lang.upper()}: {count} ({pct:.1f}%)")
        stats['languages'][lang] = {'count': count, 'percentage': round(pct, 1)}

    # Model distribution
    print("\nBy Model:")
    for model, items in sorted(model_stats.items()):
        count = len(items)
        pct = (count / len(all_items)) * 100 if all_items else 0
        print(f"   {model.upper()}: {count} ({pct:.1f}%)")
        stats['models'][model] = {'count': count, 'percentage': round(pct, 1)}

    # Difficulty distribution
    print("\nBy Difficulty:")
    difficulty_counts = defaultdict(int)
    for item in all_items:
        difficulty_counts[item.get('difficulty', 'unknown')] += 1
    for diff, count in sorted(difficulty_counts.items()):
        pct = (count / len(all_items)) * 100 if all_items else 0
        print(f"   {diff.capitalize()}: {count} ({pct:.1f}%)")
        stats['difficulty'][diff] = {'count': count, 'percentage': round(pct, 1)}

    # Question type distribution
    print("\nBy Question Type:")
    type_counts = defaultdict(int)
    for item in all_items:
        type_counts[item.get('question_type', 'unknown')] += 1
    for qtype, count in sorted(type_counts.items()):
        pct = (count / len(all_items)) * 100 if all_items else 0
        print(f"   {qtype.capitalize()}: {count} ({pct:.1f}%)")
        stats['question_types'][qtype] = {'count': count, 'percentage': round(pct, 1)}

    # Register distribution
    print("\nBy Register:")
    register_counts = defaultdict(int)
    for item in all_items:
        register_counts[item.get('register', 'unknown')] += 1
    for reg, count in sorted(register_counts.items()):
        pct = (count / len(all_items)) * 100 if all_items else 0
        print(f"   {reg.capitalize()}: {count} ({pct:.1f}%)")
        stats['register'][reg] = {'count': count, 'percentage': round(pct, 1)}

    print(f"\nTotal QA Items: {len(all_items)}")

    return stats

def main():
    """Main execution"""

    # [UPDATE PATH as needed]
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    BASE_DIR = project_root / "data" / "processed" / "translation_testing"
    OUTPUT_DIR = BASE_DIR / "merged"

    print(f"\nInput directory: {BASE_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"\nExpected structure: {BASE_DIR}/{{lang}}/{{model}}_batches/batch_*.json(l)")
    print()

    if not BASE_DIR.exists():
        print(f"Error: Input directory not found: {BASE_DIR}")
        print("\nPlease update BASE_DIR in the script to match your folder structure.")
        return

    merge_batches(BASE_DIR, OUTPUT_DIR)

    print(f"\nAll files saved to: {OUTPUT_DIR}")
    print("\nDeliverable Files Created:")
    print("   ✓ Language-specific: translation_testing_es/he/ja/ko.jsonl")
    print("   ✓ Combined: translation_testing_all.jsonl")
    print("   ✓ Model-specific: translation_testing_chatgpt/claude/gemini.jsonl")
    print("   ✓ Statistics: summary_stats.json")

if __name__ == "__main__":
    main()