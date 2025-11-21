"""
RAG Chain using Claude API (Anthropic)
Replaces Ollama with Claude 3.5 Sonnet
"""

import os
from typing import Dict, List
from langchain_anthropic import ChatAnthropic
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document


class AnoteRAGChain:
    """RAG chain using Claude API for Anote chatbot."""
    
    def __init__(self, vectorstore):
        """Initialize RAG chain with Claude."""
        
        # Get API key from environment
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        print("\n" + "="*60)
        print("Setting up RAG chain with Claude API...")
        print("="*60)
        
        # Initialize Claude
        self.llm = ChatAnthropic(
            anthropic_api_key=self.api_key,
            model_name="claude-3-5-sonnet-20241022",  # Latest Claude 3.5 Sonnet
            temperature=0.7,
            max_tokens=1024
        )
        
        print("✓ Claude 3.5 Sonnet initialized")
        
        # Store vectorstore
        self.vectorstore = vectorstore
        
        # Create retriever
        self.retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}  # Top 4 most relevant chunks
        )
        
        print("✓ Retriever configured (top 4 chunks)")
        
        # Custom prompt for Anote
        self.prompt_template = """You are an AI assistant for Anote, an AI company specializing in data labeling, model evaluation, and autonomous AI agents.

Use the following context to answer the question accurately and specifically. If the context contains the answer, provide it clearly with details. If you're not sure or the context doesn't contain enough information, say so honestly.

Context:
{context}

Question: {question}

Answer:"""
        
        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt},
            verbose=False
        )
        
        print("✓ RAG chain ready")
        print("="*60 + "\n")
    
    def query(self, question: str) -> Dict:
        """
        Query the RAG system.
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer and sources
        """
        try:
            print(f"\n{'='*60}")
            print(f"QUERY: {question}")
            print(f"{'='*60}")
            print("Processing with Claude API...")
            
            # Get response from RAG chain
            response = self.qa_chain.invoke({"query": question})
            
            answer = response["result"]
            source_docs = response["source_documents"]
            
            print(f"\n✓ Response generated ({len(source_docs)} sources used)")
            
            # Format sources
            sources = []
            for doc in source_docs:
                sources.append({
                    "title": doc.metadata.get("title", "Unknown"),
                    "source": doc.metadata.get("source", "Unknown"),
                    "chunk_index": doc.metadata.get("chunk_index", 0),
                    "text_preview": doc.page_content[:200]
                })
            
            return {
                "answer": answer,
                "sources": sources,
                "question": question
            }
            
        except Exception as e:
            print(f"\n❌ Error during query: {str(e)}")
            return {
                "answer": f"I encountered an error: {str(e)}",
                "sources": [],
                "question": question
            }
    
    def print_response(self, result: Dict):
        """Pretty print the response."""
        print(f"\n{'='*60}")
        print("ANSWER:")
        print(f"{'='*60}")
        print(result["answer"])
        
        if result["sources"]:
            print(f"\n{'='*60}")
            print(f"SOURCES ({len(result['sources'])} chunks):")
            print(f"{'='*60}")
            
            for i, source in enumerate(result["sources"], 1):
                print(f"\n[{i}] {source['title']}")
                print(f"    Chunk: {source['chunk_index']}")
                print(f"    Preview: {source['text_preview'][:100]}...")
        
        print(f"\n{'='*60}\n")