"""
Create embeddings from cleaned Anote data
Run ONCE to create vectorstore, then use rag.py

Input:  data/processed/clean_chunks.jsonl
Output: ./chroma_anote_db/ (vectorstore)
"""

import os
import json
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


def load_chunks(file_path: str = "../data/processed/clean_chunks.jsonl") -> List[Document]:
    """
    Load cleaned chunks from JSONL file.

    Expected format:
    {
        "text": "chunk content",
        "source": "url or file path",
        "title": "document title",
        "doc_id": "unique_id",
        "chunk_index": 0
    }
    """
    documents = []

    print(f"\nLoading data from {file_path}...")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                chunk = json.loads(line)

                # Validate required fields
                required = ['text', 'source', 'title', 'doc_id', 'chunk_index']
                missing = [f for f in required if f not in chunk]
                if missing:
                    print(f"Warning: Line {line_num} missing fields: {missing}")
                    continue

                # Create LangChain Document
                doc = Document(
                    page_content=chunk['text'],
                    metadata={
                        'source': chunk['source'],
                        'title': chunk['title'],
                        'doc_id': chunk['doc_id'],
                        'chunk_index': chunk['chunk_index']
                    }
                )
                documents.append(doc)

            except json.JSONDecodeError as e:
                print(f"Warning: Skipping malformed line {line_num}: {e}")
                continue

    print(f"✓ Loaded {len(documents)} chunks")
    return documents


def create_vectorstore(
    documents: List[Document],
    output_path: str = "./chroma_anote_db",
    force_recreate: bool = False
):
    """
    Create embeddings and save to ChromaDB.

    Uses HuggingFace all-MiniLM-L6-v2 (free, runs locally)
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

    # Unique documents
    unique_docs = len(set(doc.metadata['doc_id'] for doc in documents))
    print(f"Unique documents: {unique_docs}")
    print(f"Avg chunks per doc: {len(documents)/unique_docs:.1f}")

    # Sources
    unique_sources = len(set(doc.metadata['source'] for doc in documents))
    print(f"Unique sources: {unique_sources}")

    # Text length stats
    lengths = [len(doc.page_content) for doc in documents]
    print(f"\nChunk length:")
    print(f"  Min: {min(lengths)} chars")
    print(f"  Max: {max(lengths)} chars")
    print(f"  Avg: {sum(lengths)/len(lengths):.0f} chars")

    print("\nSample chunk:")
    print("-" * 60)
    sample = documents[0]
    print(f"Title: {sample.metadata['title']}")
    print(f"Source: {sample.metadata['source']}")
    print(f"Text: {sample.page_content[:200]}...")
    print("="*60)


def main():
    """Main function to create embeddings."""

    print("\n" + "="*60)
    print("ANOTE EMBEDDINGS CREATOR")
    print("="*60)

    # Load data
    documents = load_chunks()

    if not documents:
        print("\n❌ No documents loaded. Check your data file.")
        return

    # Print stats
    print_stats(documents)

    # Create vectorstore
    create_vectorstore(documents)

    print("\n" + "="*60)
    print("COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run: python rag.py")
    print("2. Or import: from rag import AnoteRAG")
    print("\nThe vectorstore is ready to use with any LLM provider.")


if __name__ == "__main__":
    main()