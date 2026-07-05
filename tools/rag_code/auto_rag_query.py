import sys
from pathlib import Path
import codecs

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

import os
storage_dir = os.getenv("STORAGE_DIR", r"D:\Users\Admin\Downloads\LangGraphStorage")
CHROMA_DB_CODE_DIR = Path(storage_dir) / "chroma_db_code"
K_RESULTS = 5

def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_rag_query.py 'your query'")
        return

    question = sys.argv[1]

    if not CHROMA_DB_CODE_DIR.exists():
        print(f"Error: Database directory not found at '{CHROMA_DB_CODE_DIR}'")
        return

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(
        persist_directory=str(CHROMA_DB_CODE_DIR), 
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": K_RESULTS})

    docs = retriever.invoke(question)

    if not docs:
        print("No relevant documents found.")
        return
    
    print(f"RAG Query Result for: {question}")
    print("--------------------------------------------------")
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "Unknown file")
        print(f"\n--- Snippet {i+1}: (Source: {source}) ---")
        print(doc.page_content)

if __name__ == "__main__":
    main()
