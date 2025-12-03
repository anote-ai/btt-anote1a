"""
Generate Leaderboard from Metrics
Creates CSV leaderboard with rankings by language, difficulty, etc.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd


def generate_leaderboard(metrics: Dict[str, Any]) -> pd.DataFrame:
    """Generate overall leaderboard"""
    rows = []
    
    for model, data in metrics.items():
        overall = data.get('overall', {})
        if not overall:
            continue
        
        rows.append({
            'Model': model,
            'BLEU': round(overall.get('bleu', 0), 2),
            'BERTScore_F1': round(overall.get('bertscore', {}).get('f1', 0), 3),
            'BERTScore_Precision': round(overall.get('bertscore', {}).get('precision', 0), 3),
            'BERTScore_Recall': round(overall.get('bertscore', {}).get('recall', 0), 3),
            'Total_Responses': overall.get('total_responses', 0)
        })
    
    df = pd.DataFrame(rows)
    df = df.sort_values('BERTScore_F1', ascending=False).reset_index(drop=True)
    df.index = df.index + 1  # Start ranking from 1
    df.index.name = 'Rank'
    
    return df


def generate_language_leaderboard(metrics: Dict[str, Any]) -> pd.DataFrame:
    """Generate leaderboard by language"""
    rows = []
    
    for model, data in metrics.items():
        by_language = data.get('by_language', {})
        
        for lang, lang_metrics in by_language.items():
            rows.append({
                'Model': model,
                'Language': lang.upper(),
                'BLEU': round(lang_metrics.get('bleu', 0), 2),
                'BERTScore_F1': round(lang_metrics.get('bertscore', {}).get('f1', 0), 3),
                'Count': lang_metrics.get('count', 0)
            })
    
    df = pd.DataFrame(rows)
    df = df.sort_values(['Language', 'BERTScore_F1'], ascending=[True, False])
    
    return df


def main():
    """Main leaderboard generation"""
    parser = argparse.ArgumentParser(description='Generate leaderboard from metrics')
    parser.add_argument('--input', type=str,
                      default='data/processed/evaluation_metrics.json',
                      help='Input metrics file')
    parser.add_argument('--output', type=str,
                      default='data/processed/leaderboard.csv',
                      help='Output leaderboard CSV')
    
    args = parser.parse_args()
    
    # Load metrics
    base_dir = Path(__file__).parent.parent
    input_file = base_dir / args.input
    
    print("\n" + "="*70)
    print("LEADERBOARD GENERATION")
    print("="*70 + "\n")
    
    print(f"📂 Loading metrics from: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        metrics = json.load(f)
    
    print(f"✓ Loaded metrics for {len(metrics)} models\n")
    
    # Generate overall leaderboard
    print("📊 Generating overall leaderboard...")
    overall_df = generate_leaderboard(metrics)
    
    # Generate language-specific leaderboard
    print("📊 Generating language-specific leaderboard...")
    language_df = generate_language_leaderboard(metrics)
    
    # Save overall leaderboard
    output_file = base_dir / args.output
    overall_df.to_csv(output_file)
    
    # Save language leaderboard
    language_output = output_file.parent / "leaderboard_by_language.csv"
    language_df.to_csv(language_output, index=False)
    
    # Display
    print("\n" + "="*70)
    print("OVERALL LEADERBOARD")
    print("="*70)
    print(overall_df.to_string())
    
    print("\n" + "="*70)
    print("LEADERBOARD BY LANGUAGE")
    print("="*70)
    print(language_df.to_string(index=False))
    
    # Summary
    print("\n" + "="*70)
    print("LEADERBOARD GENERATION COMPLETE")
    print("="*70)
    print(f"✓ Overall leaderboard: {output_file}")
    print(f"✓ By language: {language_output}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
