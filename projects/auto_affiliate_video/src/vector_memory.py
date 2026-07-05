import os
from pathlib import Path
import chromadb
from google import genai
from projects.auto_affiliate_video.src.config import Config

class VectorMemory:
    """Quản lý Long-term Memory bằng Vector RAG để tránh tràn Context Window."""

    def __init__(self, db_path: str = "data/chroma_db_memory"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # Kết nối tới local ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=str(self.db_path))
        
        # Tạo hoặc kết nối tới Collection dùng cho video script
        self.collection = self.chroma_client.get_or_create_collection(name="video_scripts_memory")
        
        # Cấu hình Gemini SDK (gemini-2.5-flash)
        self.client = genai.Client(api_key=Config.GCLI_API_KEY)
        self.model = "gemini-2.5-flash"

    def embed_and_store(self, document_id: str, content: str, metadata: dict = None):
        """Tạo embedding và lưu nội dung vào Vector DB."""
        try:
            # GCLI không có hàm embed riêng biệt trực tiếp trong phiên bản mới (genai.Client) 
            # mà không dùng mô hình nhúng cụ thể, nhưng ChromaDB có thể sử dụng default embedding function.
            # Để đơn giản và nhanh nhất, ta để ChromaDB tự động tạo embedding cho văn bản.
            self.collection.add(
                documents=[content],
                metadatas=[metadata or {}],
                ids=[document_id]
            )
            print(f"[VectorMemory] Đã lưu thành công document: {document_id}")
            return True
        except Exception as e:
            print(f"[VectorMemory Error] Lỗi khi lưu: {e}")
            return False

    def query_similar_context(self, query_text: str, n_results: int = 3) -> list:
        """Truy xuất N nội dung tương tự nhất dựa trên câu truy vấn."""
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            
            # Trả về danh sách các chuỗi documents
            if results and 'documents' in results and results['documents']:
                return results['documents'][0]
            return []
        except Exception as e:
            print(f"[VectorMemory Error] Lỗi khi truy vấn: {e}")
            return []

    def ingest_chronicles(self, file_path: str = "context/JARVIS_CHRONICLES.md"):
        """Đọc và băm nhỏ file JARVIS_CHRONICLES.md để nạp vào trí nhớ."""
        path = Path(file_path)
        if not path.exists():
            print(f"Không tìm thấy file: {file_path}")
            return

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Chia nhỏ nội dung theo các mốc (MỐC 1:, MỐC 2:, v.v.)
        sections = content.split("## 🛠 MỐC")
        
        # Bỏ qua phần đầu (giới thiệu)
        for i, section in enumerate(sections[1:], 1):
            chunk = f"## 🛠 MỐC{section}"
            self.embed_and_store(
                document_id=f"chronicle_moc_{i}",
                content=chunk.strip(),
                metadata={"source": "JARVIS_CHRONICLES.md", "type": "tech_debt_lesson"}
            )
        
        print("[VectorMemory] Hoàn tất nạp JARVIS_CHRONICLES.md vào trí nhớ!")

# Khởi tạo instance toàn cục (Singleton)
vector_memory = VectorMemory()

if __name__ == "__main__":
    # Test thử nạp dữ liệu
    vector_memory.ingest_chronicles()
    
    # Test thử truy vấn
    print("\n--- TEST QUERY ---")
    results = vector_memory.query_similar_context("Làm sao để tối ưu RAM khi chạy video editor bằng moviepy?")
    for idx, res in enumerate(results, 1):
        print(f"\n[Kết quả {idx}]:\n{res[:200]}...")
