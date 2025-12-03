"""
Multi-Model Evaluation Script
Runs translation test cases through Claude, Ollama, Gemini, and OpenAI
Saves raw responses to JSON for later metric calculation
"""

import json
import time
from pathlib import Path
from datetime import datetime
import os
from typing import Optional, Dict, Any
import argparse

# API Clients
import anthropic
import openai
from openai import OpenAI
import google.generativeai as genai
import requests

from dotenv import load_dotenv
load_dotenv()


class MultiModelEvaluator:
    """Evaluates questions across multiple LLM providers"""
    
    def __init__(self, enabled_models=None):
        """Initialize API clients for enabled models"""
        print("\n" + "="*70)
        print("MULTI-MODEL EVALUATION SYSTEM")
        print("="*70)
        
        self.enabled_models = enabled_models or ['claude', 'openai', 'gemini', 'ollama']
        
        # API Keys from environment
        self.claude_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_key = os.getenv("GOOGLE_API_KEY")
        
        # Initialize clients
        self.claude_client = None
        self.openai_client = None
        self.gemini_model = None
        self.ollama_available = False
        
        if 'claude' in self.enabled_models:
            self.claude_client = anthropic.Anthropic(api_key=self.claude_key) if self.claude_key else None
        
        if 'openai' in self.enabled_models:
            self.openai_client = OpenAI(api_key=self.openai_key) if self.openai_key else None
        
        if 'gemini' in self.enabled_models:
            if self.gemini_key:
                genai.configure(api_key=self.gemini_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Ollama base URL (local)
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Print status
        print("\n📡 API Status:")
        if 'claude' in self.enabled_models:
            print(f"  Claude:  {'✓ Ready' if self.claude_client else '✗ No API key'}")
        if 'openai' in self.enabled_models:
            print(f"  OpenAI:  {'✓ Ready' if self.openai_client else '✗ No API key'}")
        if 'gemini' in self.enabled_models:
            print(f"  Gemini:  {'✓ Ready' if self.gemini_model else '✗ No API key'}")
        if 'ollama' in self.enabled_models:
            print(f"  Ollama:  Checking...")
            self.ollama_available = self._test_ollama()
            print(f"  Ollama:  {'✓ Ready' if self.ollama_available else '✗ Not running'}")
        print()
    
    def _test_ollama(self) -> bool:
        """Test if Ollama is running"""
        try:
            response = requests.post(
                self.ollama_url,
                json={"model": "llama3.2:3b", "prompt": "test", "stream": False},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def query_claude(self, question: str, language: str) -> Dict[str, Any]:
        """Query Claude API"""
        if not self.claude_client:
            return {"answer": None, "error": "No API key", "response_time": 0}
        
        start_time = time.time()
        try:
            message = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": f"Answer this question in {language}: {question}"
                }]
            )
            response_time = time.time() - start_time
            answer = message.content[0].text
            
            return {
                "answer": answer,
                "response_time": response_time,
                "model": "claude-sonnet-4-20250514",
                "tokens": message.usage.input_tokens + message.usage.output_tokens,
                "error": None
            }
        except Exception as e:
            return {
                "answer": None,
                "error": str(e),
                "response_time": time.time() - start_time
            }
    
    def query_openai(self, question: str, language: str) -> Dict[str, Any]:
        """Query OpenAI API"""
        if not self.openai_client:
            return {"answer": None, "error": "No API key", "response_time": 0}
        
        start_time = time.time()
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": f"Answer this question in {language}: {question}"
                }],
                max_tokens=1024
            )
            response_time = time.time() - start_time
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "response_time": response_time,
                "model": "gpt-4o",
                "tokens": response.usage.total_tokens,
                "error": None
            }
        except Exception as e:
            return {
                "answer": None,
                "error": str(e),
                "response_time": time.time() - start_time
            }
    
    def query_gemini(self, question: str, language: str) -> Dict[str, Any]:
        """Query Gemini API"""
        if not self.gemini_model:
            return {"answer": None, "error": "No API key", "response_time": 0}
        
        start_time = time.time()
        try:
            prompt = f"Answer this question in {language}: {question}"
            response = self.gemini_model.generate_content(prompt)
            response_time = time.time() - start_time
            
            return {
                "answer": response.text,
                "response_time": response_time,
                "model": "gemini-1.5-pro",
                "tokens": None,
                "error": None
            }
        except Exception as e:
            return {
                "answer": None,
                "error": str(e),
                "response_time": time.time() - start_time
            }
    
    def query_ollama(self, question: str, language: str, model: str = "llama3.2:3b") -> Dict[str, Any]:
        """Query Ollama (local)"""
        if not self.ollama_available:
            return {"answer": None, "error": "Ollama not running", "response_time": 0}
        
        start_time = time.time()
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": model,
                    "prompt": f"Answer this question in {language}: {question}",
                    "stream": False
                },
                timeout=60
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "answer": data.get("response", ""),
                    "response_time": response_time,
                    "model": f"ollama-{model}",
                    "tokens": None,
                    "error": None
                }
            else:
                return {
                    "answer": None,
                    "error": f"HTTP {response.status_code}",
                    "response_time": response_time
                }
        except Exception as e:
            return {
                "answer": None,
                "error": str(e),
                "response_time": time.time() - start_time
            }
    
    def evaluate_question(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single question through enabled models"""
        question = question_data['question']
        language = question_data.get('language', 'english')
        
        # Map language codes to full names
        language_map = {
            'es': 'Spanish',
            'he': 'Hebrew',
            'ja': 'Japanese',
            'ko': 'Korean'
        }
        language_full = language_map.get(language, language)
        
        result = {
            "question_id": question_data.get('question_id', ''),
            "question": question,
            "language": language,
            "difficulty": question_data.get('difficulty', ''),
            "question_type": question_data.get('question_type', ''),
            "expected_answer": question_data.get('expected_answer', ''),
            "timestamp": datetime.now().isoformat(),
            "responses": {}
        }
        
        # Query Claude
        if 'claude' in self.enabled_models and self.claude_client:
            result["responses"]["claude"] = self.query_claude(question, language_full)
            time.sleep(0.5)
        
        # Query OpenAI
        if 'openai' in self.enabled_models and self.openai_client:
            result["responses"]["openai"] = self.query_openai(question, language_full)
            time.sleep(0.5)
        
        # Query Gemini
        if 'gemini' in self.enabled_models and self.gemini_model:
            result["responses"]["gemini"] = self.query_gemini(question, language_full)
            time.sleep(4)  # Rate limit: 15/min
        
        # Query Ollama
        if 'ollama' in self.enabled_models and self.ollama_available:
            result["responses"]["ollama"] = self.query_ollama(question, language_full)
        
        return result


def load_test_cases(file_path: str) -> list:
    """Load test cases from CSV"""
    import csv
    test_cases = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_cases.append(row)
    
    return test_cases


def main():
    """Main evaluation loop"""
    parser = argparse.ArgumentParser(description='Run model evaluations')
    parser.add_argument('--models', type=str, default='claude,openai,gemini,ollama',
                      help='Comma-separated list of models to evaluate (default: all)')
    parser.add_argument('--input', type=str, 
                      default='data/processed/translation_evaluation_merged.csv',
                      help='Input test cases file')
    parser.add_argument('--output', type=str,
                      default='data/processed/evaluation_results_raw.json',
                      help='Output file for raw results')
    
    args = parser.parse_args()
    enabled_models = [m.strip() for m in args.models.split(',')]
    
    # Initialize evaluator
    evaluator = MultiModelEvaluator(enabled_models=enabled_models)
    
    # Load test cases
    base_dir = Path(__file__).parent.parent
    test_file = base_dir / args.input
    print(f"📂 Loading test cases from: {test_file}")
    test_cases = load_test_cases(str(test_file))
    print(f"✓ Loaded {len(test_cases)} test cases\n")
    
    # Count available models
    available_models = []
    if 'claude' in enabled_models and evaluator.claude_client:
        available_models.append("Claude")
    if 'openai' in enabled_models and evaluator.openai_client:
        available_models.append("OpenAI")
    if 'gemini' in enabled_models and evaluator.gemini_model:
        available_models.append("Gemini")
    if 'ollama' in enabled_models and evaluator.ollama_available:
        available_models.append("Ollama")
    
    print(f"🤖 Models enabled: {', '.join(available_models)}")
    print(f"📊 Total API calls: {len(test_cases)} questions × {len(available_models)} models = {len(test_cases) * len(available_models)}")
    
    # Estimate time
    avg_time_per_question = 6
    total_time_minutes = (len(test_cases) * avg_time_per_question) / 60
    print(f"⏱️  Estimated time: {total_time_minutes:.0f} minutes")
    
    response = input("\n▶️  Start evaluation? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    # Run evaluation
    print("\n" + "="*70)
    print("STARTING EVALUATION")
    print("="*70 + "\n")
    
    results = []
    start_time = time.time()
    
    for i, case in enumerate(test_cases, 1):
        lang = case['language']
        print(f"[{i}/{len(test_cases)}] {lang.upper()} - {case.get('difficulty', 'N/A')[:3]} - {case['question'][:50]}...")
        
        result = evaluator.evaluate_question(case)
        results.append(result)
        
        # Show which models succeeded
        success_count = sum(1 for r in result["responses"].values() if r.get("answer"))
        print(f"          ✓ {success_count}/{len(result['responses'])} models responded")
        
        # Save progress every 10 questions
        if i % 10 == 0:
            backup_file = base_dir / "data" / "processed" / "evaluation_results_raw_backup.json"
            save_results(results, str(backup_file))
    
    # Save final results
    output_file = base_dir / args.output
    save_results(results, str(output_file))
    
    # Summary
    elapsed = time.time() - start_time
    print("\n" + "="*70)
    print("EVALUATION COMPLETE")
    print("="*70)
    print(f"✓ Evaluated {len(results)} questions")
    print(f"✓ Total time: {elapsed/60:.1f} minutes")
    print(f"✓ Results saved to: {output_file}")
    print(f"✓ Next step: python src/calculate_metrics.py")
    print("="*70 + "\n")


def save_results(results: list, filename: str):
    """Save results to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
