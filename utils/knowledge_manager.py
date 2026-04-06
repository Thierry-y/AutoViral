import os
from langchain_classic.indexes import index, SQLRecordManager
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.document_utils import load_all_documents_from_data

def sync_knowledge_base():
    """
    Industrial-grade Knowledge Base Synchronizer: 
    Automatically detects changes in the data/ directory and performs incremental updates.
    Returns status statistics of the update results.
    """
    print("🔄 System Check: Synchronizing local knowledge base...")
    
    # 1. Load all documents from the local data folder
    raw_documents = load_all_documents_from_data()
    
    # 2. Text Splitting
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    docs = text_splitter.split_documents(raw_documents) if raw_documents else []

    # 3. Initialize local vector store
    local_embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
    vectorstore = Chroma(persist_directory="db", embedding_function=local_embeddings)

    # 4. Core Logic: Initialize Record Manager (using SQLite to track file hashes)
    namespace = "chroma/marketing_agent_docs"
    record_manager = SQLRecordManager(
        namespace, db_url="sqlite:///record_manager_cache.sql"
    )
    record_manager.create_schema()

    # 5. Execute Intelligent Synchronization (Incremental Mode)
    result = index(
        docs,
        record_manager,
        vectorstore,
        cleanup="full", 
        source_id_key="source"
    )
    
    # Parse synchronization results
    added = result.get('num_added', 0)
    updated = result.get('num_updated', 0)
    skipped = result.get('num_skipped', 0)
    deleted = result.get('num_deleted', 0)
    
    if added == 0 and updated == 0 and deleted == 0:
        print(f"✅ Knowledge base is up to date (skipped {skipped} already processed chunks).")
    else:
        print(f"✅ Sync complete! Added: {added}, Updated: {updated}, Deleted: {deleted}, Skipped: {skipped}.")
        
    return vectorstore

if __name__ == "__main__":
    sync_knowledge_base()