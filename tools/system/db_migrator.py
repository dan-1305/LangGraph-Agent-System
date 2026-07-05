import sys
import chromadb
from pathlib import Path

def migrate_database():
    base_dir = Path(__file__).resolve().parent.parent.parent
    old_db_path = base_dir / "data" / "chroma_db"
    new_db_path = base_dir / "data" / "knowledge_db"
    
    print(f"🔄 Bắt đầu tiến trình Migration (Tách não)...")
    print(f"📂 Thư mục gốc: {old_db_path}")
    print(f"📂 Thư mục mới: {new_db_path}")
    
    if not old_db_path.exists():
        print("❌ Không tìm thấy `chroma_db`. Không có gì để migrate.")
        return
        
    old_client = chromadb.PersistentClient(path=str(old_db_path))
    
    try:
        old_collection = old_client.get_collection("langchain")
        print("✅ Đã tìm thấy collection `langchain` (chứa PDF Knowledge).")
    except Exception:
        print("⚠️ Không tìm thấy collection `langchain` trong `chroma_db`. Có thể đã được dọn dẹp hoặc chưa từng Ingest PDF.")
        return
        
    # Lấy toàn bộ dữ liệu
    results = old_collection.get(include=["embeddings", "metadatas", "documents"])
    ids = results.get("ids", [])
    embeddings = results.get("embeddings", [])
    metadatas = results.get("metadatas", [])
    documents = results.get("documents", [])
    
    if not ids:
        print("⚠️ Collection `langchain` trống. Không có dữ liệu để chuyển.")
        # Xóa luôn collection rỗng
        old_client.delete_collection("langchain")
        print("✅ Đã xóa collection `langchain` rỗng khỏi `chroma_db`.")
        return
        
    print(f"📦 Trích xuất thành công {len(ids)} chunks (Kèm vector nhị phân).")
    
    # Kết nối DB mới
    new_db_path.parent.mkdir(parents=True, exist_ok=True)
    new_client = chromadb.PersistentClient(path=str(new_db_path))
    
    try:
        new_collection = new_client.get_collection("domain_knowledge")
        print("⚠️ Collection `domain_knowledge` đã tồn tại ở DB mới. Dữ liệu sẽ được ghi đè/append.")
    except Exception:
        new_collection = new_client.create_collection("domain_knowledge")
        
    # Nạp dữ liệu vào DB mới theo từng batch (Chroma giới hạn batch size)
    batch_size = 5000
    print("🧠 Đang nạp dữ liệu vào `knowledge_db`...")
    for i in range(0, len(ids), batch_size):
        end_idx = min(i + batch_size, len(ids))
        new_collection.add(
            ids=ids[i:end_idx],
            embeddings=embeddings[i:end_idx],
            metadatas=metadatas[i:end_idx],
            documents=documents[i:end_idx]
        )
        print(f"  -> Đã nạp batch {i} đến {end_idx}")
        
    print(f"✅ Đã nạp thành công {len(ids)} chunks vào `knowledge_db`.")
    
    # Xóa collection cũ
    old_client.delete_collection("langchain")
    print("🗑️ Đã xóa vĩnh viễn collection `langchain` khỏi `chroma_db` để giải phóng dung lượng.")
    
    print("🎉 HOÀN TẤT QUÁ TRÌNH TÁCH NÃO HỆ THỐNG!")

if __name__ == "__main__":
    if sys.platform == "win32" and hasattr(sys.stdout, 'reconfigure'):
        if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
    migrate_database()
