"""
Embeddings Manager using HuggingFace (FREE)
Manages ChromaDB vectorstore with existing embeddings
NO CHANGES NEEDED - Your embeddings are already correct!
"""

import os
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


class AnoteEmbeddingsManager:
    """Manages embeddings and vectorstore for Anote RAG."""
    
    def __init__(self, persist_directory: str = "./chroma_anote_db"):
        """
        Initialize embeddings manager.
        
        Args:
            persist_directory: Path to ChromaDB storage
        """
        self.persist_directory = persist_directory
        
        print("\n" + "="*60)
        print("Setting up Embeddings Manager...")
        print("="*60)
        
        # Initialize HuggingFace embeddings (FREE)
        print("Loading HuggingFace embeddings model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("✓ Embeddings model loaded (all-MiniLM-L6-v2)")
        
        self.vectorstore = None
    
    def load_vectorstore(self) -> Chroma:
        """
        Load existing vectorstore from disk.
        
        Returns:
            Loaded Chroma vectorstore
        """
        if not os.path.exists(self.persist_directory):
            print(f"\n⚠️  No existing vectorstore found at {self.persist_directory}")
            print("Run the original OLLAMA_make_rag_embeddings.py first to create embeddings")
            return None
        
        print(f"\nLoading vectorstore from {self.persist_directory}...")
        
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        
        count = self.vectorstore._collection.count()
        print(f"✓ Loaded vectorstore with {count} embeddings")
        print("="*60 + "\n")
        
        return self.vectorstore
    
    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """
        Create new vectorstore from documents.
        
        Args:
            documents: List of Document objects to embed
            
        Returns:
            New Chroma vectorstore
        """
        print(f"\nCreating embeddings for {len(documents)} documents...")
        
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        count = self.vectorstore._collection.count()
        print(f"✓ Created vectorstore with {count} embeddings")
        print(f"✓ Saved to {self.persist_directory}")
        print("="*60 + "\n")
        
        return self.vectorstore
    
    def get_vectorstore(self) -> Chroma:
        """Get the current vectorstore."""
        if self.vectorstore is None:
            raise ValueError("Vectorstore not loaded. Call load_vectorstore() first.")
        return self.vectorstore