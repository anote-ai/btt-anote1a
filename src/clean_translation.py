# This will be for cleaning up the en-es, en-he, en-ja, en-ko training sets and prepping them for the testing dataset creation.

"""
Goal is to convert each parallel corpus into something like this:

{
  "id": "es_001",
  "source_lang": "es",
  "target_lang": "en",
  "source_text": "original text",
  "target_text": "translated text into english",
  "split": "[train | dev | test]"
}

"""

import json
from pathlib import Path
from typing import List, Dict, Tuple
import unicodedata

def cleaner(text: str) -> str:

    text = unicodedata.normalize('NFKC', text)  # Normalize
    text = ' '.join(text.split())                    # Only single spaces
    return text.strip()


def load_parallel_corpus(foreign_lang: Path, english_lang: Path) -> List[Tuple[str, str]]:

    if not foreign_lang.exists():
        raise FileNotFoundError(f"Foreign language file not found: {foreign_lang}")
    if not english_lang.exists():
        raise FileNotFoundError(f"English language file not found: {english_lang}")

    with open(foreign_lang, 'r', encoding='utf-8') as f_foreign, open(english_lang, 'r', encoding='utf-8') as f_english:
        foreign_text = f_foreign.readlines()
        english_text = f_english.readlines()

    return list(zip(foreign_text, english_text))


def process_parallel_pair(lang_code: str, data_dir: Path, output_dir: Path) -> None:

    pairs = []
    pair_id = 0
    splits = ['train', 'dev', 'test']

    for split in splits:
        foreign_lang = data_dir / f"en-{lang_code}" / f"opus.en-{lang_code}-{split}.{lang_code}.txt"
        english_lang = data_dir / f"en-{lang_code}" / f"opus.en-{lang_code}-{split}.en.txt"
        print(f"  Looking for: {foreign_lang}")
        print(f"  Looking for: {english_lang}")

        try:
            # Load in lines
            line_pairs = load_parallel_corpus(foreign_lang, english_lang)

            # Process the pairs
            for foreign_text, english_text in line_pairs:
                foreign_clean = cleaner(foreign_text)
                english_clean = cleaner(english_text)

                pairs.append({
                    'id': f"{lang_code}_{pair_id:05d}",
                    'source_lang': lang_code,
                    'target_lang': "en",
                    'source_text': foreign_clean,
                    'target_text': english_clean,
                    'split': split
                })
                pair_id += 1

        except ValueError as e:
            print(e)
            continue

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{lang_code}_pairs.jsonl"

    with open(output_file, 'w', encoding='utf-8') as f_output:
        for pair in pairs:
            f_output.write(json.dumps(pair, ensure_ascii=False) + '\n')

    print(f"[SUCCESS] {lang_code}: {len(pairs):,} pairs written to {output_file}")


def main():

    # DEBUG
    print("Script started successfully")

    # Config (EDIT FOR UR OWN ABSOLUTE PATHS IF RUNNING SCRIPT LOCALLY!)
    data_dir = Path(r"C:\Users\Bella\btt-anote1a\data\raw\translation")
    output_dir = Path(r"C:\Users\Bella\btt-anote1a\data\processed\translation_pairs")

    print(f"\nInput directory: {data_dir}")
    print(f"Output directory: {output_dir}")
    print(f"\nChecking if input directory exists: {data_dir.exists()}")
    print()

    if not data_dir.exists():
        print(f"[ERROR] Input directory does not exist: {data_dir}")
        print("Please check your path and try again.")
        return

    languages = ['es', 'he', 'ja', 'ko']
    print("Translation pairs have begun preprocessing...")

    # Confirm when each lang is processing and start it
    for lang in languages:
        print(f"Processing {lang.upper()}...")
        process_parallel_pair(lang, data_dir, output_dir)
        print()

    print(f"All done! Output saved to {output_dir}")


if __name__ == "__main__":
    main()