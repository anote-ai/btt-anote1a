"""
RAG Implementation for Anote Chatbot
Uses: Ollama (local LLM) + HuggingFace (free embeddings)
100% FREE - NO API KEYS NEEDED
"""

import os
import json
from typing import List, Dict
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document


CLEANED_DATA_PATH = "data/processed/clean_chunks.jsonl"
CHROMA_DB_PATH = "./chroma_anote_db"
OLLAMA_MODEL = "llama3.2:3b"  # can change to "mistral" or "phi3"

print("-"*60)
print("ANOTE RAG CHATBOT (OLLAMA)")


def load_cleaned_chunks(file_path: str) -> List[Document]:
    """Load the cleaned chunks from JSONL file."""
    documents = []
    
    print(f"\nLoading cleaned data from {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                chunk = json.loads(line)
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
                print(f"Warning: Skipping malformed line {line_num}")
                continue
    
    print(f"Loaded {len(documents)} chunks")
    return documents


def create_or_load_vectorstore(documents: List[Document], force_recreate: bool = False):
    """
    Create embeddings using FREE HuggingFace model.
    """
    print("\nSetting up embeddings (HuggingFace)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("Embeddings model loaded")
    
    # Check if vector store exists
    if os.path.exists(CHROMA_DB_PATH) and not force_recreate:
        print(f"\nLoading existing vector store from {CHROMA_DB_PATH}...")
        vectorstore = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embeddings
        )
        print(f"Loaded {vectorstore._collection.count()} embeddings")
        return vectorstore
    
    # Create new vector store
    print(f"\nCreating embeddings for {len(documents)} chunks...")
    
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    
    print(f"Created vector store with {vectorstore._collection.count()} embeddings")
    return vectorstore


def create_rag_chain(vectorstore):
    """
    Create RAG chain using Ollama.
    """
    print("\nSetting up RAG chain with Ollama...")
    print(f"Model: {OLLAMA_MODEL}")
    
    try:
        # Initialize Ollama
        llm = ChatOllama(
            model=OLLAMA_MODEL,
            temperature=0,
            num_predict=512  # Max tokens 256/512
        )
        
        # verify if Ollama is working
        print("Testing Ollama connection...")
        test_response = llm.invoke("Hi")
        print(f"Ollama is working")
        
    except Exception as e:
        print(f"\nERROR: Could not connect to Ollama")
        print(f"Error details: {e}")
        exit(1)
    
    # Custom prompt to force better answers
    prompt_template = """Use the following context to answer the question. Be specific and detailed.
If the context contains the answer, provide it clearly. Don't say "I don't know" if the answer is in the context.

Context: {context}

Question: {question}

Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, 
        input_variables=["context", "question"]
    )

    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5} # 3/5
    )
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
        verbose=False
    )
    
    print("RAG chain ready")
    return qa_chain


def query_anote_chatbot(qa_chain, question: str) -> Dict:
    """Query the chatbot and return answer with sources."""
    print(f"QUESTION: {question}")
    print(f"{'-'*60}")
    print("Processing...")
    
    try:
        response = qa_chain.invoke({"query": question})
        answer = response['result']
        sources = response['source_documents']
        
        print(f"\nANSWER:\n{answer}")
        print(f"\n{'-'*60}")
        print(f"SOURCES ({len(sources)} chunks used):")
        print(f"{'-'*60}")
        
        for i, doc in enumerate(sources, 1):
            print(f"\n[{i}] {doc.metadata['title']}")
            print(f"    Chunk {doc.metadata['chunk_index']}")
            print(f"    Preview: {doc.page_content[:100]}...")
        
        return {
            'question': question,
            'answer': answer,
            'sources': [
                {
                    'title': doc.metadata['title'],
                    'source': doc.metadata['source'],
                    'chunk_index': doc.metadata['chunk_index'],
                    'text_preview': doc.page_content[:200]
                }
                for doc in sources
            ]
        }
    except Exception as e:
        print(f"\nError during query: {e}")
        return {'question': question, 'answer': f'Error: {e}', 'sources': []}


def save_predictions(predictions: List[Dict], output_file: str = "initial_predictions.json"):
    """Save predictions."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(predictions, f, indent=2, ensure_ascii=False)
    print(f"\nSaved predictions to {output_file}")


def main():
    """Main function to set up and test the RAG system."""
    
    documents = load_cleaned_chunks(CLEANED_DATA_PATH)
    
    if not documents:
        print("ERROR: No documents loaded")
        return
    
    unique_docs = len(set(doc.metadata['doc_id'] for doc in documents))
    print(f"\nDataset stats:")
    print(f"  Total chunks: {len(documents)}")
    print(f"  Unique documents: {unique_docs}")
    
    vectorstore = create_or_load_vectorstore(documents, force_recreate=False)
    
    qa_chain = create_rag_chain(vectorstore)
    
    print("\n" + "-"*60)
    print("TEST WITH SAMPLE QUESTIONS")
    print("-"*60)
    
    test_questions = [
        "What is Anote?",
        "What are Anote's main products?",
        "How does Anote use fine-tuning?",
    ]
    
    predictions = []
    for question in test_questions:
        result = query_anote_chatbot(qa_chain, question)
        predictions.append(result)
        print("\n" + "-"*60)
    
    save_predictions(predictions)
    
    print("\nSETUP COMPLETE!")
    print("\nBuilt:")
    print("  100% free RAG system")
    print("  No API keys needed")
    print("  Runs completely locally")
    print("  Unlimited usage")
    print("\nFiles created:")
    print(f"  - {CHROMA_DB_PATH}/ (vector database)")
    print(f"  - initial_predictions.json (sample outputs)")

if __name__ == "__main__":
    main()