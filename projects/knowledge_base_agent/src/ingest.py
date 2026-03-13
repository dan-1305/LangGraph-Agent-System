import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Base Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

load_dotenv(BASE_DIR / ".env")

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Paths
DATA_DIR = BASE_DIR / "data" / "document" / "new_ebook"
CHROMA_DB_DIR = BASE_DIR / "data" / "chroma_db"

def ingest_pdfs():
    print(f"🔄 Đang đọc các file PDF từ {DATA_DIR}...")
    
    if not DATA_DIR.exists():
        print(f"❌ Thư mục {DATA_DIR} không tồn tại!")
        return
        
    loader = PyPDFDirectoryLoader(str(DATA_DIR))
    documents = loader.load()
    
    print(f"✅ Đã tải {len(documents)} trang tài liệu.")
    
    print("🔄 Đang chia nhỏ văn bản (Chunking)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Đã chia thành {len(chunks)} chunks.")
    
    print("🧠 Đang tạo Embedding (HuggingFace) và lưu vào ChromaDB...")
    
    # Initialize Embedding model - using local HuggingFace embeddings
    # sentence-transformers/all-MiniLM-L6-v2 is fast and lightweight, perfect for i3 CPU
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create and persist vectorstore
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_DIR)
    )
    
    print(f"🎉 Hoàn tất! Đã lưu Database tại: {CHROMA_DB_DIR}")

if __name__ == "__main__":
    ingest_pdfs()
