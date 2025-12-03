"""
Calculate Metrics from Raw Evaluation Results
Computes BLEU and BERTScore for each model's responses
No API calls - runs locally on saved responses
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any, List
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# Metrics
from sacrebleu import corpus_bleu
from bert_score import score as bert_score


class MetricsCalculator:
    """Calculate translation quality metrics"""
    
    def __init__(self):
        print("\n" + "="*70)
        print("METRICS CALCULATION")
        print("="*70 + "\n")
    
    def calculate_bleu(self, predictions: List[str], references: List[List[str]]) -> float:
        """Calculate corpus BLEU score"""
        try:
            bleu = corpus_bleu(predictions, references)
            return bleu.score
        except Exception as e:
            print(f"BLEU calculation error: {e}")
            return 0.0
    
    def calculate_bertscore(self, predictions: List[str], references: List[str], lang: str = 'en') -> Dict[str, float]:
        """Calculate BERTScore (batched for efficiency)"""
        try:
            # Map language codes
            lang_map = {
                'es': 'es',
                'he': 'en',  # BERTScore doesn't support Hebrew well, use multilingual
                'ja': 'ja',
                'ko': 'ko'
            }
            bert_lang = lang_map.get(lang, 'en')
            
            P, R, F1 = bert_score(
                predictions,
                references,
                lang=bert_lang,
                verbose=False,
                device='cpu'  # Use GPU if available
            )
            
            return {
                "precision": float(P.mean()),
                "recall": float(R.mean()),
                "f1": float(F1.mean())
            }
        except Exception as e:
            print(f"BERTScore calculation error: {e}")
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    
    def calculate_metrics_for_model(self, results: List[Dict], model_name: str) -> Dict[str, Any]:
        """Calculate metrics for a single model across all questions"""
        print(f"\n📊 Calculating metrics for: {model_name}")
        
        # Group by language
        language_groups = {}
        for result in results:
            lang = result['language']
            if lang not in language_groups:
                language_groups[lang] = {
                    'predictions': [],
                    'references': []
                }
            
            # Get model response
            if model_name in result['responses']:
                response = result['responses'][model_name]
                answer = response.get('answer', '')
                
                if answer:
                    language_groups[lang]['predictions'].append(answer)
                    language_groups[lang]['references'].append(result['expected_answer'])
        
        # Calculate metrics per language
        metrics = {
            "model": model_name,
            "overall": {},
            "by_language": {}
        }
        
        all_predictions = []
        all_references = []
        
        for lang, data in language_groups.items():
            if len(data['predictions']) == 0:
                continue
            
            print(f"  - {lang.upper()}: {len(data['predictions'])} responses")
            
            # BLEU (needs list of references)
            bleu = self.calculate_bleu(
                data['predictions'],
                [[ref] for ref in data['references']]
            )
            
            # BERTScore
            bertscore = self.calculate_bertscore(
                data['predictions'],
                data['references'],
                lang=lang
            )
            
            metrics["by_language"][lang] = {
                "bleu": bleu,
                "bertscore": bertscore,
                "count": len(data['predictions'])
            }
            
            all_predictions.extend(data['predictions'])
            all_references.extend(data['references'])
        
        # Overall metrics
        if all_predictions:
            overall_bleu = self.calculate_bleu(
                all_predictions,
                [[ref] for ref in all_references]
            )
            overall_bertscore = self.calculate_bertscore(
                all_predictions,
                all_references
            )
            
            metrics["overall"] = {
                "bleu": overall_bleu,
                "bertscore": overall_bertscore,
                "total_responses": len(all_predictions)
            }
        
        return metrics


def main():
    """Main metrics calculation"""
    parser = argparse.ArgumentParser(description='Calculate metrics from raw results')
    parser.add_argument('--input', type=str,
                      default='data/processed/evaluation_results_raw.json',
                      help='Input raw results file')
    parser.add_argument('--output', type=str,
                      default='data/processed/evaluation_metrics.json',
                      help='Output metrics file')
    
    args = parser.parse_args()
    
    # Load raw results
    base_dir = Path(__file__).parent.parent
    input_file = base_dir / args.input
    
    print(f"📂 Loading raw results from: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    print(f"✓ Loaded {len(results)} evaluation results\n")
    
    # Find all models
    all_models = set()
    for result in results:
        all_models.update(result['responses'].keys())
    
    print(f"🤖 Found models: {', '.join(sorted(all_models))}\n")
    
    # Calculate metrics
    calculator = MetricsCalculator()
    all_metrics = {}
    
    for model in sorted(all_models):
        metrics = calculator.calculate_metrics_for_model(results, model)
        all_metrics[model] = metrics
    
    # Save metrics
    output_file = base_dir / args.output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_metrics, f, indent=2, ensure_ascii=False)
    
    # Summary
    print("\n" + "="*70)
    print("METRICS CALCULATION COMPLETE")
    print("="*70)
    print(f"✓ Calculated metrics for {len(all_metrics)} models")
    print(f"✓ Results saved to: {output_file}")
    print(f"✓ Next step: python src/generate_leaderboard.py")
    print("="*70 + "\n")
    
    # Preview
    print("📊 Preview of Results:")
    for model, metrics in all_metrics.items():
        overall = metrics.get('overall', {})
        if overall:
            print(f"  {model}:")
            print(f"    BLEU: {overall.get('bleu', 0):.2f}")
            print(f"    BERTScore F1: {overall.get('bertscore', {}).get('f1', 0):.3f}")


if __name__ == "__main__":
    main()
