import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Base Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

load_dotenv(BASE_DIR / ".env")

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Paths
DATA_DIR = BASE_DIR / "projects" / "sillytavern_world_card_generator" / "data" / "world_card"
CHROMA_DB_DIR = BASE_DIR / "projects" / "sillytavern_world_card_generator" / "data" / "chroma_db_cards"

def extract_card_text(json_data):
    """Trích xuất các trường nội dung quan trọng từ thẻ JSON của SillyTavern."""
    # Thẻ V2/V3 thường chứa data trong key 'data', hoặc ở ngay root
    data = json_data.get('data', json_data)
    
    parts = []
    name = data.get('name', 'Unknown')
    parts.append(f"Tên nhân vật/Thế giới: {name}")
    
    if data.get('description'):
        parts.append(f"Mô tả (Description): {data.get('description')}")
        
    if data.get('personality'):
        parts.append(f"Tính cách (Personality): {data.get('personality')}")
        
    if data.get('scenario'):
        parts.append(f"Bối cảnh (Scenario): {data.get('scenario')}")
        
    if data.get('first_mes'):
        parts.append(f"Tin nhắn mở đầu (First Message): {data.get('first_mes')}")
        
    if data.get('mes_example'):
        parts.append(f"Ví dụ hội thoại (Message Examples): {data.get('mes_example')}")
        
    # Xử lý Lorebook nếu có
    if data.get('character_book') and data['character_book'].get('entries'):
        lore_parts = []
        for entry in data['character_book']['entries']:
            keys = ", ".join(entry.get('keys', []))
            content = entry.get('content', '')
            lore_parts.append(f"- Từ khóa [{keys}]: {content}")
        if lore_parts:
            parts.append("Lorebook (Kiến thức thế giới):\n" + "\n".join(lore_parts))
            
    return "\n\n".join(parts)

def ingest_cards():
    print(f"🔄 Đang đọc các file JSON thẻ từ {DATA_DIR}...")
    
    if not DATA_DIR.exists():
        print(f"❌ Thư mục {DATA_DIR} không tồn tại!")
        return
        
    documents = []
    for file in os.listdir(DATA_DIR):
        if not file.endswith('.json'):
            continue
            
        file_path = DATA_DIR / file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                card_json = json.load(f)
                
            text_content = extract_card_text(card_json)
            if text_content.strip():
                # Bỏ metadata để dễ truy xuất
                doc = Document(
                    page_content=text_content,
                    metadata={"source": file, "name": card_json.get('data', card_json).get('name', 'Unknown')}
                )
                documents.append(doc)
        except Exception as e:
            print(f"⚠️ Lỗi khi đọc {file}: {e}")
    
    print(f"✅ Đã tải và trích xuất text từ {len(documents)} thẻ nhân vật.")
    
    print("🔄 Đang chia nhỏ văn bản (Chunking)...")
    # Tăng kích thước chunk để giữ trọn vẹn context của một thẻ (thẻ thường dài 1500-3000 từ)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Đã chia thành {len(chunks)} chunks.")
    
    print("🧠 Đang tạo Embedding (HuggingFace) và lưu vào ChromaDB...")
    
    # Initialize Embedding model - using local HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Xóa DB cũ nếu tồn tại để tránh trùng lặp
    import shutil
    if CHROMA_DB_DIR.exists():
        print("🗑️ Đang xóa ChromaDB cũ...")
        shutil.rmtree(CHROMA_DB_DIR)
        
    # Create and persist vectorstore
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_DIR)
    )
    
    print(f"🎉 Hoàn tất! Đã lưu Database Thẻ Nhân Vật tại: {CHROMA_DB_DIR}")

if __name__ == "__main__":
    ingest_cards()
