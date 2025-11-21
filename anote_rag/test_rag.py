"""
Quick test script for Anote RAG system
Tests all providers and compares performance
"""

import time
import os
from dotenv import load_dotenv
from rag import AnoteRAG


def test_provider(provider: str, questions: list) -> dict:
    """Test a single provider."""
    print("\n" + "="*60)
    print(f"TESTING: {provider.upper()}")
    print("="*60)

    try:
        # Initialize
        start_init = time.time()
        rag = AnoteRAG(llm_provider=provider)
        init_time = time.time() - start_init

        # Query
        start_query = time.time()
        result = rag.query(questions[0], verbose=False)
        query_time = time.time() - start_query

        return {
            'provider': provider,
            'status': '✓ Success',
            'init_time': init_time,
            'query_time': query_time,
            'answer_length': len(result['answer'])
        }

    except Exception as e:
        return {
            'provider': provider,
            'status': f'✗ Failed: {str(e)[:50]}',
            'init_time': 0,
            'query_time': 0,
            'answer_length': 0
        }


def print_comparison(results: list):
    """Print comparison table."""
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print("="*60)
    print(f"\n{'Provider':<12} {'Status':<20} {'Init':<8} {'Query':<8} {'Answer'}")
    print("-" * 60)

    for r in results:
        print(f"{r['provider']:<12} {r['status']:<20} "
              f"{r['init_time']:<7.2f}s {r['query_time']:<7.2f}s "
              f"{r['answer_length']} chars")

    print("="*60)


def main():
    """Run tests for all providers."""

    load_dotenv()

    print("\n" + "="*60)
    print("ANOTE RAG SYSTEM TESTS")
    print("="*60)

    # Test question
    questions = ["What is Anote?"]

    # Check which providers are available
    providers = []

    # Ollama (always try)
    providers.append('ollama')

    # Claude (if API key exists)
    if os.getenv('ANTHROPIC_API_KEY'):
        providers.append('claude')
    else:
        print("\n⚠️  Skipping Claude (no ANTHROPIC_API_KEY)")

    # OpenAI (if API key exists)
    if os.getenv('OPENAI_API_KEY'):
        providers.append('openai')
    else:
        print("\n⚠️  Skipping OpenAI (no OPENAI_API_KEY)")

    # Run tests
    results = []
    for provider in providers:
        result = test_provider(provider, questions)
        results.append(result)

    # Print comparison
    print_comparison(results)

    # Recommendations
    print("\n📊 RECOMMENDATIONS:")
    print("-" * 60)

    successful = [r for r in results if 'Success' in r['status']]

    if successful:
        # Find fastest
        fastest = min(successful, key=lambda x: x['query_time'])
        print(f"\n⚡ Fastest: {fastest['provider']} ({fastest['query_time']:.2f}s)")

        # Find free option
        free = next((r for r in successful if r['provider'] == 'ollama'), None)
        if free:
            print(f"💰 Free: ollama ({free['query_time']:.2f}s)")

        print("\n✅ All systems operational!")
    else:
        print("\n❌ No providers working. Check:")
        print("  - Is Ollama running? (ollama serve)")
        print("  - Are API keys in .env file?")
        print("  - Did you run make_embeddings.py?")

    print("="*60 + "\n")


if __name__ == "__main__":
    main()