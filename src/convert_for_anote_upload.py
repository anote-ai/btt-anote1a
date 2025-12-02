"""
Convert translation test cases to CSV for Anote web upload
Outputs: anote_upload_test_cases.csv (50 balanced cases)
"""
import json
import csv
from pathlib import Path

def main():
    print("\n" + "="*60)
    print("CONVERT TEST CASES FOR ANOTE WEB UPLOAD")
    print("="*60)

    # Load all test cases
    test_file = Path("data/processed/translation_testing/merged/translation_testing_all.jsonl")
    all_cases = []
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            all_cases.append(json.loads(line))

    print(f"\nLoaded {len(all_cases)} total test cases")

    # Select 12-13 per language (50 total)
    selected_cases = []
    langs = {'es': 0, 'he': 0, 'ja': 0, 'ko': 0}
    target_per_lang = 13

    for case in all_cases:
        lang = case.get('batch_id', '').split('_')[0]
        if lang in langs and langs[lang] < target_per_lang:
            selected_cases.append(case)
            langs[lang] += 1
        if len(selected_cases) >= 50:
            break

    print(f"Selected {len(selected_cases)} cases: {dict(langs)}")

    # Convert to CSV format
    csv_data = []
    for case in selected_cases:
        lang = case.get('batch_id', '').split('_')[0]

        # Use citation_text as the document, truncate to 5000 chars
        text = case.get('citation_text', case.get('answer', ''))[:5000]

        csv_data.append({
            'text': text,
            'question': case['question'],
            'expected_answer': case['answer'],
            'language': lang,
            'difficulty': case.get('difficulty', 'unknown'),
            'question_type': case.get('question_type', 'unknown')
        })

    # Save to CSV
    output_file = Path("anote_upload_test_cases.csv")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"\n✓ Saved {len(csv_data)} test cases to {output_file}")
    print("\nReady for Anote web upload!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
