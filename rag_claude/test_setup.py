"""
Quick test script to verify Claude API setup
Run this BEFORE main.py to catch issues early
"""

import os
import sys
from dotenv import load_dotenv


def test_environment():
    """Test 1: Check environment variables."""
    print("\n" + "="*60)
    print("TEST 1: Environment Variables")
    print("="*60)
    
    load_dotenv()
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("❌ FAILED: ANTHROPIC_API_KEY not found")
        print("\nPlease create .env file with:")
        print("ANTHROPIC_API_KEY=your_key_here")
        return False
    
    if not api_key.startswith('sk-ant-'):
        print("⚠️  WARNING: API key format looks incorrect")
        print("   Should start with 'sk-ant-'")
        return False
    
    print(f"✓ PASSED: API key found (length: {len(api_key)})")
    return True


def test_embeddings():
    """Test 2: Check if embeddings exist."""
    print("\n" + "="*60)
    print("TEST 2: Embeddings Existence")
    print("="*60)
    
    paths_to_check = [
        "./chroma_anote_db",
        "../chroma_anote_db",
        "../../chroma_anote_db"
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            print(f"✓ PASSED: Found embeddings at {path}")
            return True
    
    print("❌ FAILED: No chroma_anote_db folder found")
    print("\nPlease run: python src/make_rag_embeddings.py")
    return False


def test_dependencies():
    """Test 3: Check if required packages are installed."""
    print("\n" + "="*60)
    print("TEST 3: Python Dependencies")
    print("="*60)
    
    required_packages = [
        ('langchain', 'langchain'),
        ('langchain_anthropic', 'langchain-anthropic'),
        ('langchain_chroma', 'langchain-chroma'),
        ('chromadb', 'chromadb'),
        ('sentence_transformers', 'sentence-transformers')
    ]
    
    missing = []
    
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - NOT INSTALLED")
            missing.append(package_name)
    
    if missing:
        print(f"\n❌ FAILED: Missing {len(missing)} packages")
        print("\nRun: pip install -r requirements.txt")
        return False
    
    print("\n✓ PASSED: All dependencies installed")
    return True


def test_api_connection():
    """Test 4: Verify Claude API is accessible."""
    print("\n" + "="*60)
    print("TEST 4: Claude API Connection")
    print("="*60)
    
    try:
        from langchain_anthropic import ChatAnthropic
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        
        print("Attempting connection to Claude API...")
        llm = ChatAnthropic(
            anthropic_api_key=api_key,
            model_name="claude-3-5-sonnet-20241022",
            temperature=0,
            max_tokens=50
        )
        
        # Simple test message
        response = llm.invoke("Say 'test successful'")
        
        print(f"✓ PASSED: API connection successful")
        print(f"   Response: {response.content[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        print("\nPossible issues:")
        print("- Invalid API key")
        print("- No internet connection")
        print("- API rate limit reached")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("ANOTE RAG SETUP VERIFICATION")
    print("="*60)
    
    tests = [
        ("Environment Variables", test_environment),
        ("Embeddings Existence", test_embeddings),
        ("Python Dependencies", test_dependencies),
        ("Claude API Connection", test_api_connection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        print("\nYou're ready to run: python main.py")
    else:
        print("\n" + "="*60)
        print("⚠️  SOME TESTS FAILED")
        print("="*60)
        print("\nPlease fix the issues above before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    main()