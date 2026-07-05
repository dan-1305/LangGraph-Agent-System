import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

import chromadb
from langchain_huggingface import HuggingFaceEmbeddings

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str)
    args = parser.parse_args()
    
    root_dir = Path(__file__).resolve().parent.parent.parent
    load_dotenv(root_dir / ".env")
    
    storage_dir = os.getenv("STORAGE_DIR")
    db_path = Path(storage_dir) / 'chroma_db' if storage_dir else root_dir / 'data' / 'chroma_db'
    
    if not db_path.exists():
        print(f"Lỗi: Không tìm thấy DB tại {db_path}")
        return
        
    client = chromadb.PersistentClient(path=str(db_path))
    collection = client.get_collection(name="system_architecture_docs")
    
    # [TỐI ƯU HÓA] Sử dụng model MiniLM siêu nhẹ đồng bộ với rag_ingest.py
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    query_embed = embeddings.embed_query(args.query)
    
    results = collection.query(
        query_embeddings=[query_embed],
        n_results=5
    )
    
    print("RAG Query Result for: ", args.query)
    print("--------------------------------------------------")
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        print(f"\\n--- Nguồn: {meta.get('source', 'Unknown')} ---")
        print(doc)

if __name__ == "__main__":
    main()
