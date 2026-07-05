from src.base_agent import BaseAgent
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Base Path cho module agent
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CHROMA_DB_DIR = BASE_DIR / "projects" / "sillytavern_world_card_generator" / "data" / "chroma_db_cards"

class RAGCardAgent(BaseAgent):
    """
    Agent RAG chuyên dùng để tìm kiếm thẻ mẫu từ ChromaDB, giúp AI học lỏm văn phong.
    """
    def __init__(self):
        print("🧠 Khởi tạo RAG Card Agent...")
        try:
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            self.vectorstore = Chroma(
                persist_directory=str(CHROMA_DB_DIR), 
                embedding_function=embeddings
            )
            # Tìm kiếm 2 thẻ gần giống nhất để học
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 2})
            print("✅ Đã kết nối Thư viện Thẻ thành công!")
        except Exception as e:
            print(f"⚠️ Lỗi kết nối ChromaDB: {e}")
            self.vectorstore = None
            
    def get_reference_context(self, theme: str, style: str) -> str:
        """
        Lấy context từ các thẻ cũ dựa trên theme và style.
        """
        if not self.vectorstore:
            return ""
            
        query = f"Tìm các thẻ có chủ đề {theme} và văn phong {style}"
        docs = self.retriever.invoke(query)
        
        if not docs:
            return ""
            
        # Nối các doc lại để làm reference
        references = []
        for i, doc in enumerate(docs):
            card_name = doc.metadata.get("name", f"Thẻ mẫu {i+1}")
            references.append(f"--- BẮT ĐẦU THẺ MẪU: {card_name} ---\n{doc.page_content}\n--- KẾT THÚC THẺ MẪU ---")
            
        return "\n\n".join(references)
