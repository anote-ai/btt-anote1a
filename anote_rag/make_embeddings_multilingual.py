"""
Create embeddings from Wikipedia benchmark chunks
Adapted from make_embeddings.py for multilingual Wikipedia data

Input:  Wikipedia JSONL files (benchmark_*.jsonl)
Output: ChromaDB vectorstore for RAG

Usage:
    python anote_rag/make_embeddings_multilingual.py --input data/processed/benchmark_chunks/benchmark_es.jsonl --output chroma_spanish_db
    python anote_rag/make_embeddings_multilingual.py --input data/processed/benchmark_chunks/benchmark_he.jsonl --output chroma_hebrew_db --force
"""

import os
import json
import argparse
from typing import List, Dict
from pathlib import Path
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


def normalize_chunk(chunk: dict, line_num: int) -> dict:
    """
    Normalize chunk format to handle both flat and nested citation structures.
    
    Supports two formats:
    1. Nested format (benchmark data):
       {"text": "...", "lang": "es", "citation": {"title": "...", "url": "...", "section": "..."}}
    
    2. Flat format:
       {"text": "...", "language": "es", "title": "...", "url": "...", "section": "..."}
    
    Returns normalized dict with: text, title, url, language, section
    """
    normalized = {}
    
    # Get text
    normalized['text'] = chunk.get('text', '').strip()
    
    # Get language (handle both 'lang' and 'language' keys)
    normalized['language'] = chunk.get('language') or chunk.get('lang', '')
    
    # Handle nested citation format (benchmark data)
    if 'citation' in chunk and isinstance(chunk['citation'], dict):
        citation = chunk['citation']
        normalized['title'] = citation.get('title', 'Unknown')
        normalized['url'] = citation.get('url', '')
        normalized['section'] = citation.get('section', 'Full Article')
    # Handle flat format
    else:
        normalized['title'] = chunk.get('title', 'Unknown')
        normalized['url'] = chunk.get('url', '')
        normalized['section'] = chunk.get('section', 'Full Article')
    
    return normalized


def load_chunks(file_path: str) -> List[Document]:
    """
    Load Wikipedia chunks from JSONL file.

    Supports both nested citation format and flat format.
    
    Expected fields (after normalization):
    - text: chunk content (required)
    - title: article title (required)
    - url: wikipedia url (required)
    - language: language code (required)
    - section: section name (optional)
    """
    documents = []
    skipped_count = 0

    print(f"\nLoading data from {file_path}...")

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"\n❌ Data file not found: {file_path}\n"
            f"Make sure you have Wikipedia benchmark chunks in the correct location.\n"
            f"Expected format: data/processed/benchmark_chunks/benchmark_<lang>.jsonl"
        )

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                chunk = json.loads(line)
                
                # Normalize format (handles both nested and flat structures)
                normalized = normalize_chunk(chunk, line_num)

                # Validate required fields
                required = ['text', 'title', 'url', 'language']
                missing = [f for f in required if not normalized.get(f)]
                if missing:
                    if skipped_count < 5:  # Only show first 5 warnings
                        print(f"Warning: Line {line_num} missing fields: {missing}")
                    skipped_count += 1
                    continue

                # Skip empty text
                if not normalized['text']:
                    if skipped_count < 5:
                        print(f"Warning: Line {line_num} has empty text, skipping")
                    skipped_count += 1
                    continue

                # Create LangChain Document
                doc = Document(
                    page_content=normalized['text'],
                    metadata={
                        'title': normalized['title'],
                        'section': normalized['section'],
                        'source': normalized['url'],
                        'language': normalized['language'],
                        'chunk_index': line_num - 1  # 0-indexed
                    }
                )
                documents.append(doc)

            except json.JSONDecodeError as e:
                if skipped_count < 5:
                    print(f"Warning: Skipping malformed line {line_num}: {e}")
                skipped_count += 1
                continue
            except Exception as e:
                if skipped_count < 5:
                    print(f"Warning: Line {line_num} error: {e}")
                skipped_count += 1
                continue

    if skipped_count > 5:
        print(f"... and {skipped_count - 5} more warnings suppressed")

    if not documents:
        raise ValueError(
            f"\n❌ No valid documents loaded from {file_path}\n"
            f"Check that the file contains valid JSONL.\n"
            f"Supported formats:\n"
            f"  1. Nested: {{'text': '...', 'lang': 'es', 'citation': {{'title': '...', 'url': '...'}}}}\n"
            f"  2. Flat: {{'text': '...', 'language': 'es', 'title': '...', 'url': '...'}}"
        )

    print(f"✓ Loaded {len(documents)} chunks")
    if skipped_count > 0:
        print(f"  Skipped {skipped_count} invalid/incomplete chunks")
    
    return documents


def create_vectorstore(
    documents: List[Document],
    output_path: str,
    force_recreate: bool = False
):
    """
    Create embeddings and save to ChromaDB.

    Uses HuggingFace all-MiniLM-L6-v2 (free, runs locally)
    Supports multilingual text (trained on 50+ languages)
    """

    # Check if already exists
    if os.path.exists(output_path) and not force_recreate:
        print(f"\n⚠️  Vectorstore already exists at {output_path}")
        response = input("Recreate? This will delete existing embeddings (y/n): ")
        if response.lower() != 'y':
            print("Aborted. Using existing vectorstore.")
            return

        # Delete existing
        import shutil
        shutil.rmtree(output_path)
        print("✓ Deleted existing vectorstore")

    # Initialize embeddings model
    print("\nLoading embeddings model (HuggingFace)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("✓ Model loaded (all-MiniLM-L6-v2)")
    print("  (Supports 50+ languages including ES, HE, JA, KO)")

    # Create embeddings
    print(f"\nCreating embeddings for {len(documents)} chunks...")
    print("This may take 2-5 minutes...")

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=output_path
    )

    count = vectorstore._collection.count()
    print(f"\n✓ Created {count} embeddings")
    print(f"✓ Saved to {output_path}")

    return vectorstore


def print_stats(documents: List[Document]):
    """Print dataset statistics."""
    print("\n" + "="*60)
    print("DATASET STATISTICS")
    print("="*60)

    print(f"\nTotal chunks: {len(documents)}")

    # Unique articles
    unique_articles = len(set(doc.metadata['title'] for doc in documents))
    print(f"Unique articles: {unique_articles}")
    print(f"Avg chunks per article: {len(documents)/unique_articles:.1f}")

    # Languages
    languages = [doc.metadata['language'] for doc in documents]
    language_counts = {}
    for lang in languages:
        language_counts[lang] = language_counts.get(lang, 0) + 1

    print(f"\nLanguage distribution:")
    for lang, count in sorted(language_counts.items()):
        print(f"  {lang.upper()}: {count} chunks ({count/len(documents)*100:.1f}%)")

    # Sources (URLs)
    unique_sources = len(set(doc.metadata['source'] for doc in documents))
    print(f"\nUnique Wikipedia URLs: {unique_sources}")

    # Text length stats
    lengths = [len(doc.page_content) for doc in documents]
    print(f"\nChunk length:")
    print(f"  Min: {min(lengths)} chars")
    print(f"  Max: {max(lengths)} chars")
    print(f"  Avg: {sum(lengths)/len(lengths):.0f} chars")

    # Sections
    sections = [doc.metadata.get('section', '') for doc in documents]
    sections_with_content = [s for s in sections if s]
    print(f"\nSections:")
    print(f"  Chunks with sections: {len(sections_with_content)} ({len(sections_with_content)/len(documents)*100:.1f}%)")

    print("\nSample chunk:")
    print("-" * 60)
    sample = documents[0]
    print(f"Title: {sample.metadata['title']}")
    print(f"Language: {sample.metadata['language']}")
    print(f"Section: {sample.metadata.get('section', '(none)')}")
    print(f"URL: {sample.metadata['source']}")
    print(f"Text: {sample.page_content[:200]}...")
    print("="*60)


def main():
    """Main function to create embeddings."""

    parser = argparse.ArgumentParser(
        description="Create embeddings from Wikipedia benchmark chunks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python anote_rag/make_embeddings_multilingual.py --input data/processed/benchmark_chunks/benchmark_es.jsonl --output chroma_spanish_db
  python anote_rag/make_embeddings_multilingual.py --input data/processed/benchmark_chunks/benchmark_he.jsonl --output chroma_hebrew_db --force

Supported languages: ES (Spanish), HE (Hebrew), JA (Japanese), KO (Korean)

The script automatically handles both nested citation format and flat format.
        """
    )

    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Path to input JSONL file (e.g., data/processed/benchmark_chunks/benchmark_es.jsonl)'
    )

    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Path to output ChromaDB directory (e.g., chroma_spanish_db)'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Force recreate vectorstore without prompting (deletes existing)'
    )

    args = parser.parse_args()

    print("\n" + "="*60)
    print("MULTILINGUAL WIKIPEDIA EMBEDDINGS CREATOR")
    print("="*60)

    # Validate input path
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"\n❌ Input file not found: {args.input}")
        print("\nExpected location: data/processed/benchmark_chunks/benchmark_<lang>.jsonl")
        print("Available languages: es, he, ja, ko")
        return 1

    # Load data
    try:
        documents = load_chunks(args.input)
    except (FileNotFoundError, ValueError) as e:
        print(str(e))
        return 1

    if not documents:
        print("\n❌ No documents loaded. Check your data file.")
        return 1

    # Print stats
    print_stats(documents)

    # Create vectorstore
    try:
        create_vectorstore(documents, args.output, force_recreate=args.force)
    except Exception as e:
        print(f"\n❌ Error creating vectorstore: {e}")
        return 1

    print("\n" + "="*60)
    print("COMPLETE!")
    print("="*60)
    print(f"\nVectorstore created: {args.output}")
    print("\nNext steps:")
    print("1. Use with RAG system: from rag import AnoteRAG")
    print(f"2. Initialize: rag = AnoteRAG(chroma_path='{args.output}')")
    print("3. Query: result = rag.query('your question')")
    print("\nThe vectorstore is ready for multilingual RAG queries.")

    return 0


if __name__ == "__main__":
    exit(main())
