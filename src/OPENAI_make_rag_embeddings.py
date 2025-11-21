"""
RAG Implementation for Anote Chatbot
Uses: OpenAI
"""

import os
import json
from typing import List, Dict
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_core.documents import Document


# CONFIGURATION
CLEANED_DATA_PATH = "data/processed/clean_chunks.jsonl"
CHROMA_DB_PATH = "./chroma_anote_db"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def load_cleaned_chunks(file_path: str) -> List[Document]:
    """
    Load the cleaned chunks from JSONL file.
    """
    documents = []
    
    print(f"Loading cleaned data from {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                chunk = json.loads(line)
                
                # Create LangChain Document from each chunk
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
    
    print(f"Loaded {len(documents)} chunks successfully")
    return documents


def create_or_load_vectorstore(documents: List[Document], force_recreate: bool = False):
    """
    Create embeddings and store in Chroma.
    If vectorstore already exists, load it (unless force_recreate=True).
    """
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=OPENAI_API_KEY
    )
    
    # Check if vector store already exists
    if os.path.exists(CHROMA_DB_PATH) and not force_recreate:
        print(f"Loading existing vector store from {CHROMA_DB_PATH}...")
        vectorstore = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embeddings
        )
        print(f"Loaded vector store with {vectorstore._collection.count()} embeddings")
        return vectorstore
    
    # Create new vector store
    print(f"Embedding {len(documents)} chunks...")
    
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    
    print(f"Created vector store with {vectorstore._collection.count()} embeddings")
    print(f"Saved to {CHROMA_DB_PATH}")
    return vectorstore


def create_rag_chain(vectorstore):
    """
    Create the RAG chain with retriever and LLM.
    """
    print("Setting up RAG chain...")
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,  # Deterministic for evaluation
        openai_api_key=OPENAI_API_KEY
    )
    
    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}  # Return top 3 chunks
    )
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Put all retrieved docs in prompt
        retriever=retriever,
        return_source_documents=True,  # For citations
        verbose=False
    )
    
    print("RAG chain ready")
    return qa_chain


def query_anote_chatbot(qa_chain, question: str) -> Dict:
    """
    Query Anote chatbot and return answer with sources.
    """
    print(f"\n{'-'*60}")
    print(f"QUESTION: {question}")
    
    # Get response
    response = qa_chain.invoke({"query": question})
    
    answer = response['result']
    sources = response['source_documents']
    
    print(f"\nANSWER:\n{answer}")
    print(f"\n{'-'*60}")
    print(f"SOURCES ({len(sources)} chunks used):")
    
    for i, doc in enumerate(sources, 1):
        print(f"\n[{i}] {doc.metadata['title']}")
        print(f"    Source: {doc.metadata['source']}")
        print(f"    Chunk: {doc.metadata['chunk_index']}")
        print(f"    Preview: {doc.page_content[:150]}...")
    
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


def save_predictions(predictions: List[Dict], output_file: str = "initial_predictions.json"):
    """
    Save predictions to JSON file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(predictions, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved predictions to {output_file}")


# MAIN EXECUTION
def main():
    """
    Main function to set up and test the RAG system.
    """
    print("-"*60)
    print("ANOTE RAG CHATBOT SETUP")
    
    # Step 1: Load cleaned data
    documents = load_cleaned_chunks(CLEANED_DATA_PATH)
    
    if not documents:
        print("ERROR: No documents loaded. Check file path.")
        return
    
    print(f"\nDataset stats:")
    print(f"  Total chunks: {len(documents)}")
    unique_docs = len(set(doc.metadata['doc_id'] for doc in documents))
    print(f"  Unique documents: {unique_docs}")
    print(f"  Avg chunks per doc: {len(documents)/unique_docs:.1f}")
    
    # Step 2: Create vector store
    vectorstore = create_or_load_vectorstore(documents, force_recreate=False)
    
    # Step 3: Create RAG chain
    qa_chain = create_rag_chain(vectorstore)
    
    print("\n" + "-"*60)
    print("TESTING WITH SAMPLE QUESTIONS")
    
    # Step 4: Test with sample questions
    test_questions = [
        "What is Anote?",
        "What are Anote's main products?",
        "How does Anote use fine-tuning?",
        "What is Anote's approach to RAG?",
        "What companies has Anote worked with?",
        "How does Anote handle multilingual data?"
    ]
    
    predictions = []
    for question in test_questions:
        result = query_anote_chatbot(qa_chain, question)
        predictions.append(result)
        print("\n" + "-"*60)
    
    # Step 5: Save predictions
    save_predictions(predictions)
    
    print("SETUP COMPLETE!")
    print("-"*60)
    print("\nNext steps:")
    print("1. Review the answers above")
    print("2. Check initial_predictions.json")
    print("3. Submit to Anote for evaluation")
    print("\nTo query interactively:")
    print("  result = query_anote_chatbot(qa_chain, 'your question here')")

if __name__ == "__main__":
    # Ensure API key is set
    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY not set!")
        print("Run: export OPENAI_API_KEY='your-key-here'")
        exit(1)
    
    main()
