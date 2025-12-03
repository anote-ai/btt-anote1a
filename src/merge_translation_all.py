#!/usr/bin/env python3
"""
Merge Translation QA Dataset

This script combines:
1. Translation QA questions (JSONL format with 400 questions)
2. Source translation pairs (JSON format with 200 pairs)

Output: Comprehensive CSV ready for multi-model evaluation

"""

import json
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict


class TranslationDataMerger:
    """Merges translation questions with source pairs."""
    
    def __init__(self):
        self.qa_data = []
        self.source_pairs = {}
        self.merged_data = []
        self.stats = {
            'total_questions': 0,
            'total_pairs': 0,
            'matched': 0,
            'unmatched': 0,
            'by_language': defaultdict(lambda: {'matched': 0, 'unmatched': 0})
        }
    
    def load_qa_jsonl(self, filepath: str) -> None:
        """Load QA questions from JSONL file."""
        print(f"\n📖 Loading QA data from {filepath}...")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if line.strip():
                        try:
                            data = json.loads(line)
                            self.qa_data.append(data)
                        except json.JSONDecodeError as e:
                            print(f"⚠️  Warning: Skipping line {line_num} due to JSON error: {e}")
            
            self.stats['total_questions'] = len(self.qa_data)
            print(f"✅ Loaded {len(self.qa_data)} questions")
            
            # Show distribution
            lang_counts = defaultdict(int)
            for item in self.qa_data:
                # Extract language from batch_id (e.g., "es_batch_chatgpt_01" -> "es")
                batch_id = item.get('batch_id', '')
                if batch_id:
                    lang = batch_id.split('_')[0]
                    lang_counts[lang] += 1
            
            print("   Distribution by language:")
            for lang, count in sorted(lang_counts.items()):
                print(f"   - {lang.upper()}: {count} questions")
                
        except FileNotFoundError:
            print(f"❌ Error: File not found: {filepath}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading QA data: {e}")
            sys.exit(1)
    
    def load_source_pairs(self, filepaths: List[str]) -> None:
        """Load source translation pairs from JSON files."""
        print(f"\n📖 Loading source translation pairs...")
        
        for filepath in filepaths:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    pairs = json.load(f)
                    
                for pair in pairs:
                    pair_id = pair.get('id')
                    if pair_id:
                        self.source_pairs[pair_id] = pair
                        
                print(f"✅ Loaded {len(pairs)} pairs from {Path(filepath).name}")
                        
            except FileNotFoundError:
                print(f"⚠️  Warning: File not found: {filepath}")
            except Exception as e:
                print(f"⚠️  Warning: Error loading {filepath}: {e}")
        
        self.stats['total_pairs'] = len(self.source_pairs)
        print(f"\n📊 Total unique source pairs: {len(self.source_pairs)}")
    
    def find_matching_pair(self, qa_item: Dict) -> Optional[Dict]:
        """
        Find the source pair that matches this QA item.
        
        Matching strategy:
        1. Try to extract pair_id from citation_text or batch_id
        2. Fuzzy match on citation_text vs source_text/target_text
        """
        citation_text = qa_item.get('citation_text', '').strip()
        cite_from = qa_item.get('cite_from', '')
        batch_id = qa_item.get('batch_id', '')
        
        # Extract language and approximate ID from batch_id
        # Example: "es_batch_chatgpt_01" -> es, potentially es_001 to es_012
        if batch_id:
            parts = batch_id.split('_')
            if len(parts) >= 3:
                lang = parts[0]  # e.g., "es"
                batch_num = parts[-1]  # e.g., "01"
                
                # Try to guess potential pair IDs
                # Each batch of ~12 questions might map to ~2 source pairs
                try:
                    batch_int = int(batch_num)
                    # Estimate: batch 01 -> pairs 001-012, batch 02 -> pairs 013-024, etc.
                    start_idx = (batch_int - 1) * 12 + 1
                    end_idx = start_idx + 12
                    
                    # Check all pairs in this range
                    for idx in range(start_idx, end_idx):
                        pair_id = f"{lang}_{idx:03d}"
                        if pair_id in self.source_pairs:
                            pair = self.source_pairs[pair_id]
                            
                            # Verify citation_text appears in source or target
                            if citation_text:
                                source_text = pair.get('source_text', '')
                                target_text = pair.get('target_text', '')
                                
                                # Check if citation appears in the appropriate text
                                if cite_from == 'source' and citation_text in source_text:
                                    return pair
                                elif cite_from == 'target' and citation_text in target_text:
                                    return pair
                                # Also check reverse in case cite_from is wrong
                                elif citation_text in source_text or citation_text in target_text:
                                    return pair
                except ValueError:
                    pass
        
        # Fallback: Search all pairs for citation match
        if citation_text:
            for pair_id, pair in self.source_pairs.items():
                source_text = pair.get('source_text', '')
                target_text = pair.get('target_text', '')
                
                if citation_text in source_text or citation_text in target_text:
                    return pair
        
        return None
    
    def merge_data(self) -> None:
        """Merge QA data with source pairs."""
        print(f"\n🔄 Merging datasets...")
        
        for qa_item in self.qa_data:
            # Find matching source pair
            matching_pair = self.find_matching_pair(qa_item)
            
            # Extract language from batch_id
            batch_id = qa_item.get('batch_id', '')
            lang = batch_id.split('_')[0] if batch_id else 'unknown'
            
            # Create merged record
            merged_record = {
                # Identifiers
                'question_id': f"{batch_id}_{len(self.merged_data):03d}",
                'language': lang,
                'pair_id': matching_pair.get('id') if matching_pair else None,
                
                # Context (from source pairs)
                'source_text': matching_pair.get('source_text') if matching_pair else None,
                'target_text': matching_pair.get('target_text') if matching_pair else None,
                'source_lang': matching_pair.get('source_lang') if matching_pair else lang,
                'target_lang': matching_pair.get('target_lang') if matching_pair else 'en',
                
                # Question & Answer (from QA JSONL)
                'question': qa_item.get('question', ''),
                'expected_answer': qa_item.get('answer', ''),
                
                # Citation info
                'citation_text': qa_item.get('citation_text', ''),
                'cite_from': qa_item.get('cite_from', ''),
                
                # Metadata
                'difficulty': qa_item.get('difficulty', ''),
                'question_type': qa_item.get('question_type', ''),
                'register': qa_item.get('register', ''),
                'model': qa_item.get('model', ''),
                'batch_id': batch_id,
                'generated_date': qa_item.get('generated_date', ''),
                
                # Match status
                'has_context': 'yes' if matching_pair else 'no'
            }
            
            self.merged_data.append(merged_record)
            
            # Update stats
            if matching_pair:
                self.stats['matched'] += 1
                self.stats['by_language'][lang]['matched'] += 1
            else:
                self.stats['unmatched'] += 1
                self.stats['by_language'][lang]['unmatched'] += 1
        
        print(f"✅ Merged {len(self.merged_data)} records")
    
    def save_to_csv(self, output_path: str) -> None:
        """Save merged data to CSV."""
        print(f"\n💾 Saving merged data to {output_path}...")
        
        if not self.merged_data:
            print("❌ No data to save!")
            return
        
        # Define field order
        fieldnames = [
            'question_id', 'language', 'pair_id',
            'source_text', 'target_text', 'source_lang', 'target_lang',
            'question', 'expected_answer',
            'citation_text', 'cite_from',
            'difficulty', 'question_type', 'register',
            'model', 'batch_id', 'generated_date', 'has_context'
        ]
        
        try:
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.merged_data)
            
            print(f"✅ Saved {len(self.merged_data)} records to CSV")
            
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            sys.exit(1)
    
    def print_statistics(self) -> None:
        """Print merge statistics."""
        print("\n" + "="*60)
        print("📊 MERGE STATISTICS")
        print("="*60)
        
        print(f"\n📖 Input Data:")
        print(f"   Questions (JSONL):     {self.stats['total_questions']}")
        print(f"   Source Pairs (JSON):   {self.stats['total_pairs']}")
        
        print(f"\n🔗 Matching Results:")
        print(f"   ✅ Matched:            {self.stats['matched']} ({self.stats['matched']/self.stats['total_questions']*100:.1f}%)")
        print(f"   ❌ Unmatched:          {self.stats['unmatched']} ({self.stats['unmatched']/self.stats['total_questions']*100:.1f}%)")
        
        print(f"\n🌍 By Language:")
        for lang in sorted(self.stats['by_language'].keys()):
            matched = self.stats['by_language'][lang]['matched']
            unmatched = self.stats['by_language'][lang]['unmatched']
            total = matched + unmatched
            match_pct = matched/total*100 if total > 0 else 0
            
            print(f"   {lang.upper()}: {matched}/{total} matched ({match_pct:.1f}%)")
        
        print("\n" + "="*60)
        
        if self.stats['unmatched'] > 0:
            print("\n⚠️  NOTE: Some questions don't have matching source pairs.")
            print("   These questions will still be in the CSV but with empty context fields.")
            print("   Models will need to answer based on the question alone.")


def main():
    """Main execution function."""
    print("="*60)
    print("🔀 TRANSLATION DATA MERGER")
    print("="*60)
    
    # Initialize merger
    merger = TranslationDataMerger()
    
    # Define file paths
    # Adjust these paths based on your actual file locations
    base_dir = Path(__file__).parent.parent  # Get project root directory
    qa_jsonl_path = base_dir / "data" / "processed" / "translation_testing" / "merged" / "translation_testing_all.jsonl"
    source_pairs_paths = [
        base_dir / "data" / "processed" / "translation_pairs" / "qa_source_pairs" / "es_qa_source.json",
        base_dir / "data" / "processed" / "translation_pairs" / "qa_source_pairs" / "he_qa_source.json",
        base_dir / "data" / "processed" / "translation_pairs" / "qa_source_pairs" / "ja_qa_source.json",
        base_dir / "data" / "processed" / "translation_pairs" / "qa_source_pairs" / "ko_qa_source.json"
    ]

    output_csv_path = base_dir / "data" / "processed" / "translation_evaluation_merged.csv"
    
    # Check if files exist and provide guidance
    print("\n🔍 Checking for input files...")

    qa_exists = qa_jsonl_path.exists()
    print(f"   QA JSONL: {'✅ Found' if qa_exists else '❌ Not found'} - {qa_jsonl_path}")

    if not qa_exists:
        # Try to find alternative JSONL files
        merged_dir = base_dir / "data" / "processed" / "translation_testing" / "merged"
        if merged_dir.exists():
            jsonl_files = list(merged_dir.glob("*.jsonl"))

            if jsonl_files:
                print(f"\n   💡 Found JSONL file(s) in merged directory:")
                for f in jsonl_files:
                    print(f"      - {f.name}")
                qa_jsonl_path = jsonl_files[0]
                print(f"   Using: {qa_jsonl_path}")

    # Check for source pair JSON files
    found_pairs = []
    for path in source_pairs_paths:
        if path.exists():
            found_pairs.append(str(path))
            print(f"   Source pairs: ✅ Found {path.name}")
        else:
            print(f"   Source pairs: ❌ Not found {path.name}")

    if not found_pairs:
        # Try to find JSON files in the qa_source_pairs directory
        pairs_dir = base_dir / "data" / "processed" / "translation_pairs" / "qa_source_pairs"
        if pairs_dir.exists():
            json_files = list(pairs_dir.glob("*.json"))

            if json_files:
                print(f"\n   💡 Found JSON file(s) in qa_source_pairs directory:")
                for f in json_files:
                    print(f"      - {f.name}")
                found_pairs = [str(f) for f in json_files]
    
    # Load data
    merger.load_qa_jsonl(str(qa_jsonl_path))
    merger.load_source_pairs(found_pairs if found_pairs else [str(p) for p in source_pairs_paths])
    
    # Merge
    merger.merge_data()

    # Save
    merger.save_to_csv(str(output_csv_path))
    
    # Print statistics
    merger.print_statistics()
    
    print(f"\n✨ Merge complete!")
    print(f"\n📄 Output file: {output_csv_path}")
    print(f"\n💡 Next steps:")
    print(f"   1. Review the CSV in Excel/Google Sheets")
    print(f"   2. Use this file with run_evaluations_csv.py for evaluation")
    print(f"   3. Check match rates - consider manual matching for unmatched questions")
    

if __name__ == "__main__":
    main()
