import os
import sys
from pathlib import Path
from typing import List, Dict

# Base Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src.base_agent import BaseAgent

CHROMA_DB_DIR = BASE_DIR / "data" / "chroma_db"

class RAGAgent(BaseAgent):
    """
    Agent RAG (Retrieval-Augmented Generation) chuyên dùng để query kiến thức từ Ebook.
    Kế thừa từ BaseAgent để dùng chung model LLM.
    """
    def __init__(self, model_name: str = "gemini-3.1-pro-preview"):
        super().__init__(model_name=model_name, temperature=0.3) # Temperature thấp cho RAG để tránh ảo giác
        
        # Initialize Vector Store
        print("🧠 Đang tải Knowledge Base từ ChromaDB...")
        try:
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            self.vectorstore = Chroma(
                persist_directory=str(CHROMA_DB_DIR), 
                embedding_function=embeddings
            )
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
            print("✅ Đã kết nối Knowledge Base thành công!")
        except Exception as e:
            print(f"⚠️ Không thể kết nối ChromaDB (Có thể bạn chưa chạy file ingest.py): {e}")
            self.vectorstore = None
            
    def query(self, question: str) -> str:
        """
        Nhận câu hỏi, tìm kiếm relevant chunks và đưa cho LLM tổng hợp câu trả lời.
        """
        if not self.vectorstore:
            return "Knowledge Base chưa được khởi tạo. Vui lòng chạy cập nhật Ebook trước."
            
        # 1. Tìm kiếm context (Retrieval)
        docs = self.retriever.invoke(question)
        context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])
        
        if not context_text.strip():
            return "Không tìm thấy thông tin liên quan trong thư viện Ebook."
            
        # 2. Sinh câu trả lời (Generation)
        prompt = f"""Bạn là một chuyên gia học thuật (Knowledge Base Agent).
Dựa vào các đoạn tài liệu được trích xuất từ sách dưới đây, hãy trả lời câu hỏi của người dùng một cách chính xác và chuyên sâu.
NẾU TÀI LIỆU KHÔNG CHỨA ĐỦ THÔNG TIN, HÃY TRẢ LỜI "Tôi không tìm thấy thông tin này trong thư viện sách hiện tại" và KHÔNG TỰ BỊA RA.

[TÀI LIỆU THAM KHẢO]:
{context_text}

[CÂU HỎI CỦA NGƯỜI DÙNG]:
{question}

TRẢ LỜI:"""
        
        print("🧠 Đang tổng hợp câu trả lời từ Ebook...")
        return self._call_llm(prompt)

if __name__ == "__main__":
    agent = RAGAgent()
    while True:
        q = input("\nNhập câu hỏi cho Knowledge Base (hoặc 'q' để thoát): ")
        if q.lower() == 'q':
            break
        ans = agent.query(q)
        print(f"\n💡 TRẢ LỜI:\n{ans}")
