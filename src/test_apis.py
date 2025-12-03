"""
Test script to verify all API connections work
Run this BEFORE running the full evaluation
"""

import os
import sys
from dotenv import load_dotenv
load_dotenv()


print("\n" + "="*70)
print("API CONNECTION TEST")
print("="*70 + "\n")

# Check environment variables
print("1️⃣  Checking environment variables...")
apis = {
    "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY")
}

for name, key in apis.items():
    if key:
        masked = key[:8] + "..." + key[-4:] if len(key) > 12 else "***"
        print(f"   ✓ {name}: {masked}")
    else:
        print(f"   ✗ {name}: Not set")

print()

# Test Claude
print("2️⃣  Testing Claude API...")
try:
    import anthropic
    if apis["ANTHROPIC_API_KEY"]:
        client = anthropic.Anthropic(api_key=apis["ANTHROPIC_API_KEY"])
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say 'Hello' in Spanish"}]
        )
        response = message.content[0].text
        print(f"   ✓ Claude works! Response: {response[:50]}")
    else:
        print("   ✗ No API key set")
except Exception as e:
    print(f"   ✗ Error: {str(e)[:100]}")

print()

# Test OpenAI
print("3️⃣  Testing OpenAI API...")
try:
    from openai import OpenAI
    if apis["OPENAI_API_KEY"]:
        client = OpenAI(api_key=apis["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use cheaper model for testing
            messages=[{"role": "user", "content": "Say 'Hello' in Spanish"}],
            max_tokens=50
        )
        answer = response.choices[0].message.content
        print(f"   ✓ OpenAI works! Response: {answer[:50]}")
    else:
        print("   ✗ No API key set")
except Exception as e:
    print(f"   ✗ Error: {str(e)[:100]}")

print()

# Test Gemini
print("4️⃣  Testing Gemini API...")
try:
    import google.generativeai as genai
    if apis["GOOGLE_API_KEY"]:
        genai.configure(api_key=apis["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say 'Hello' in Spanish")
        print(f"   ✓ Gemini works! Response: {response.text[:50]}")
    else:
        print("   ✗ No API key set")
except Exception as e:
    print(f"   ✗ Error: {str(e)[:100]}")

print()

# Test Ollama
print("5️⃣  Testing Ollama (local)...")
try:
    import requests
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": "Say 'Hello' in Spanish",
            "stream": False
        },
        timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        answer = data.get("response", "")
        print(f"   ✓ Ollama works! Response: {answer[:50]}")
    else:
        print(f"   ✗ HTTP {response.status_code}")
except requests.exceptions.ConnectionError:
    print("   ✗ Ollama not running. Start with: ollama serve")
except Exception as e:
    print(f"   ✗ Error: {str(e)[:100]}")

print()

# Summary
print("="*70)
working_apis = []
if apis["ANTHROPIC_API_KEY"]:
    working_apis.append("Claude")
if apis["OPENAI_API_KEY"]:
    working_apis.append("OpenAI")
if apis["GOOGLE_API_KEY"]:
    working_apis.append("Gemini")

print(f"✅ Working APIs: {', '.join(working_apis) if working_apis else 'None'}")
print("\n💡 To get Gemini free API key: https://makersuite.google.com/app/apikey")
print("💡 To install Ollama: https://ollama.com/download")
print("\n▶️  Ready to run: python src/run_evaluation.py")
print("="*70 + "\n")
