import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Optional

import chromadb
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

if hasattr(sys.stdout, 'reconfigure'):
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

def query_rag_return_context(query: str, n_results: int = 5, top_k: int = None, collection_name: str = "system_architecture_docs") -> str:
    """
    Hàm helper dùng cho các Agent để lấy context từ RAG.
    collection_name: Cho phép chọn collection (system_architecture_docs hoặc knowledge_base_core).
    """
    if top_k is not None:
        n_results = top_k
        
    root_dir = Path(__file__).resolve().parent.parent.parent
    load_dotenv(root_dir / ".env")
    
    storage_dir = os.getenv("STORAGE_DIR")
    
    # Định tuyến DB path dựa trên collection
    if collection_name == "knowledge_base_core":
        db_path = Path(storage_dir) / 'knowledge_db' if storage_dir else root_dir / 'data' / 'knowledge_db'
    else:
        db_path = Path(storage_dir) / 'chroma_db' if storage_dir else root_dir / 'data' / 'chroma_db'
    
    if not db_path.exists():
        return f"Lỗi: Không tìm thấy DB tại {db_path}"
        
    client = chromadb.PersistentClient(path=str(db_path))
    
    try:
        collection = client.get_collection(name=collection_name)
    except Exception:
        return f"Lỗi: Không tìm thấy collection '{collection_name}' trong DB."
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    context = ""
    if results['documents'] and len(results['documents']) > 0:
        for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
            context += f"\n--- Nguồn: {meta.get('source', 'Unknown')} ---\n{doc}\n"
    
    return context if context else "No relevant context found."

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str)
    parser.add_argument("--collection", type=str, default="system_architecture_docs")
    args = parser.parse_args()
    
    context = query_rag_return_context(args.query, collection_name=args.collection)
    print(f"RAG Query Result for: {args.query} [Collection: {args.collection}]")
    print("--------------------------------------------------")
    print(context)

if __name__ == "__main__":
    main()
