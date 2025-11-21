"""
Unified RAG Implementation for Anote Chatbot
Supports: Ollama (local/free) OR Claude API (production) OR OpenAI

Usage:
    # Local/free
    rag = AnoteRAG(llm_provider="ollama")

    # Production
    rag = AnoteRAG(llm_provider="claude")

    # OpenAI
    rag = AnoteRAG(llm_provider="openai")
"""

import os
import json
from typing import List, Dict, Literal, Optional
from dotenv import load_dotenv

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# LLM imports
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI


class AnoteRAG:
    """Unified RAG system for Anote chatbot."""

    def __init__(
        self,
        chroma_path: str = "./chroma_anote_db",
        llm_provider: Literal["ollama", "claude", "openai"] = "ollama",
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        top_k: int = 4
    ):
        """
        Initialize RAG system.

        Args:
            chroma_path: Path to ChromaDB vectorstore
            llm_provider: "ollama" (free), "claude", or "openai"
            model_name: Override default model
            temperature: LLM temperature (0-1)
            top_k: Number of chunks to retrieve
        """
        load_dotenv()

        self.llm_provider = llm_provider
        self.top_k = top_k

        print("\n" + "="*60)
        print("ANOTE RAG SYSTEM")
        print("="*60)

        # Load embeddings and vectorstore
        print(f"\nLoading vectorstore from {chroma_path}...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

        if not os.path.exists(chroma_path):
            raise FileNotFoundError(
                f"Vectorstore not found at {chroma_path}\n"
                f"Run make_embeddings.py first to create it."
            )

        self.vectorstore = Chroma(
            persist_directory=chroma_path,
            embedding_function=embeddings
        )

        count = self.vectorstore._collection.count()
        print(f"✓ Loaded {count} embeddings")

        # Initialize LLM based on provider
        self._init_llm(llm_provider, model_name, temperature)

        # Create QA chain
        self._create_qa_chain()

        print("✓ RAG system ready")
        print("="*60 + "\n")

    def _init_llm(self, provider: str, model_name: Optional[str], temperature: float):
        """Initialize the LLM based on provider."""

        if provider == "ollama":
            model_name = model_name or "llama3.2:3b"
            print(f"\nUsing Ollama: {model_name}")
            print("  - Free & local")
            print("  - Slower responses (~30-60s)")

            try:
                self.llm = ChatOllama(
                    model=model_name,
                    temperature=temperature,
                    num_predict=512
                )
                # Test connection
                self.llm.invoke("test")
                print("✓ Ollama connected")
            except Exception as e:
                raise ConnectionError(
                    f"Could not connect to Ollama: {e}\n"
                    f"Make sure Ollama is running: ollama serve"
                )

        elif provider == "claude":
            model_name = model_name or "claude-sonnet-4-5-20250929"
            api_key = os.getenv('ANTHROPIC_API_KEY')

            if not api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY not found\n"
                    "Add to .env file: ANTHROPIC_API_KEY=your_key_here"
                )

            print(f"\nUsing Claude: {model_name}")
            print("  - API-based")
            print("  - Fast responses (~2-5s)")

            self.llm = ChatAnthropic(
                anthropic_api_key=api_key,
                model_name=model_name,
                temperature=temperature,
                max_tokens=1024
            )
            print("✓ Claude API configured")

        elif provider == "openai":
            model_name = model_name or "gpt-4o-mini"
            api_key = os.getenv('OPENAI_API_KEY')

            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY not found\n"
                    "Add to .env file: OPENAI_API_KEY=your_key_here"
                )

            print(f"\nUsing OpenAI: {model_name}")
            print("  - API-based")
            print("  - Fast responses (~2-5s)")

            self.llm = ChatOpenAI(
                openai_api_key=api_key,
                model=model_name,
                temperature=temperature,
                max_tokens=1024
            )
            print("✓ OpenAI API configured")

        else:
            raise ValueError(f"Unknown provider: {provider}")

    def _create_qa_chain(self):
        """Create the QA chain with retriever using modern LCEL syntax."""

        # Prompt template
        prompt = PromptTemplate.from_template("""You are an AI assistant for Anote, an AI company specializing in data labeling, model evaluation, and autonomous AI agents.

Use the following context to answer the question accurately and specifically. If the context contains the answer, provide it clearly with details. If you're not sure or the context doesn't contain enough information, say so honestly.

Context:
{context}

Question: {question}

Answer:""")

        # Create retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": self.top_k}
        )

        # Helper function to format documents
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # Create chain using LCEL (LangChain Expression Language)
        self.qa_chain = (
                {
                    "context": self.retriever | format_docs,
                    "question": RunnablePassthrough()
                }
                | prompt
                | self.llm
                | StrOutputParser()
        )

    def query(self, question: str, verbose: bool = True) -> Dict:
        """
        Query the RAG system.

        Args:
            question: User's question
            verbose: Print progress

        Returns:
            Dictionary with answer, sources, and metadata
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"QUESTION: {question}")
            print(f"{'='*60}")
            print(f"Processing with {self.llm_provider}...")

        try:
            # Get answer from chain
            answer = self.qa_chain.invoke(question)

            # Get source documents separately
            source_docs = self.retriever.invoke(question)

            # Format sources
            sources = []
            for doc in source_docs:
                sources.append({
                    "title": doc.metadata.get("title", "Unknown"),
                    "source": doc.metadata.get("source", "Unknown"),
                    "chunk_index": doc.metadata.get("chunk_index", 0),
                    "text_preview": doc.page_content[:200]
                })

            result = {
                "question": question,
                "answer": answer,
                "sources": sources,
                "provider": self.llm_provider
            }

            if verbose:
                self.print_response(result)

            return result

        except Exception as e:
            error_msg = f"Error during query: {str(e)}"
            print(f"\n❌ {error_msg}")
            return {
                "question": question,
                "answer": f"Error: {error_msg}",
                "sources": [],
                "provider": self.llm_provider
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

    def batch_query(self, questions: List[str], save_to: Optional[str] = None) -> List[Dict]:
        """
        Query multiple questions and optionally save results.

        Args:
            questions: List of questions
            save_to: Optional file path to save results

        Returns:
            List of result dictionaries
        """
        print(f"\nProcessing {len(questions)} questions with {self.llm_provider}...")

        results = []
        for i, question in enumerate(questions, 1):
            print(f"\n[{i}/{len(questions)}]")
            result = self.query(question, verbose=True)
            results.append(result)

        if save_to:
            with open(save_to, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Saved {len(results)} results to {save_to}")

        return results


def main():
    """Test the RAG system with sample questions."""

    # Choose provider (change this to test different providers)
    PROVIDER = "claude"  # or "claude" or "openai"

    # Initialize RAG
    rag = AnoteRAG(
        chroma_path="./chroma_anote_db",
        llm_provider=PROVIDER
    )

    # Test questions
    test_questions = [
        "What is Anote?",
        "What are Anote's main products?",
        "How does Anote use fine-tuning?",
        "What is Autonomous Intelligence?"
    ]

    # Run queries and save results
    results = rag.batch_query(
        test_questions,
        save_to=f"predictions_{PROVIDER}.json"
    )

    print("\n" + "="*60)
    print(f"COMPLETED - Results saved to predictions_{PROVIDER}.json")
    print("="*60)


if __name__ == "__main__":
    main()