import json
import os
import time
from pathlib import Path
import sys
from typing import List, Dict, Any
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings

# Đảm bảo src vào sys.path để import thư viện lõi
root_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.factory.config import create_fallback_chain

class MemoryModule:
    """Hệ thống nén ký ức và Vector Store cho Project Eden"""
    def __init__(self, memory_dir: str):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Khởi tạo LLM cho việc nén và HyDE sử dụng Fallback Chain thay vì ChatOpenAI trần
        self.llm = create_fallback_chain(
            model_list=["gemini-2.5-flash", "gemini-2.5-flash-lite"],
            temperature=0.3
        )
        
        # 2. Khởi tạo Embedding Model (nhẹ, chạy local tốt)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 3. Khởi tạo ChromaDB
        db_path = self.memory_dir / "chroma_db"
        self.chroma_client = chromadb.PersistentClient(path=str(db_path))
        self.collection = self.chroma_client.get_or_create_collection(name="eden_lore_memory")
        
        self.short_term_memory: List[Dict[str, Any]] = []
        self.total_importance = 0.0

    def add_lesson(self, lesson: str):
        """Đánh giá Importance Score của bài học bằng LLM và thêm vào bộ nhớ ngắn hạn."""
        if not lesson or not lesson.strip():
            return
            
        # Pydantic schema hoặc cấu trúc ép kiểu JSON để chấm điểm
        prompt = f"""
Bạn là một nhà phân tích tâm lý. Hãy đánh giá độ quan trọng của sự kiện/suy nghĩ sau đây đối với sự sinh tồn trong một môi trường khắc nghiệt:
"{lesson}"

Hãy trả về duy nhất một con số từ 1 đến 10 (1 là nhàm chán như đi bộ, 10 là bị quái vật cắn hoặc phát minh ra lửa).
"""
        try:
            response = self.llm.invoke(prompt)
            score_str = response.content.strip()
            score = float(score_str)
            
            try:
                from src.token_tracker import track_llm_usage
                model_name = getattr(self.llm, 'model', 'unknown') if hasattr(self.llm, 'model') else 'fallback_chain_model'
                track_llm_usage(response, "minecraft_eden_simulation", model_name)
            except Exception:
                pass
        except Exception as e:
            print(f"❌ [Circuit Breaker] Fallback kích hoạt ở Memory: {e}")
            score = 5.0 # Mặc định nếu lỗi

        self.short_term_memory.append({
            "content": lesson,
            "importance": score
        })
        self.total_importance += score
        print(f"🧠 [Memory] Đã ghi nhớ (Score: {score}/10): {lesson}")

    def should_compress(self) -> bool:
        """Kích hoạt Deep Reflection khi tổng điểm quan trọng vượt ngưỡng 100."""
        return self.total_importance >= 100.0

    def compress_memory(self):
        """Nén các bài học ngắn hạn thành 1-2 nguyên lý cốt lõi và lưu vào ChromaDB."""
        if not self.short_term_memory:
            return

        print(f"🔮 [Thiên Đạo] Tổng điểm áp lực ({self.total_importance}). Kích hoạt Deep Reflection...")
        raw_lessons = "\n".join(f"- [{m['importance']}/10] {m['content']}" for m in self.short_term_memory)
        
        prompt = f"""
Bạn là Hệ thống Quản trị Ký ức (Thiên Đạo). Dưới đây là 10 bài học lắt nhắt mà Player rút ra được:
{raw_lessons}

NHIỆM VỤ:
Hãy chắt lọc và tóm tắt thành 1 nguyên tắc cốt lõi (Core Principle) hoặc 1 công thức chế tạo chính xác nhất.
Trả về duy nhất đoạn văn bản tóm tắt đó, gạt bỏ suy nghĩ thừa.
"""
        try:
            response = self.llm.invoke(prompt)
            compressed_lore = response.content.strip()
            
            try:
                from src.token_tracker import track_llm_usage
                model_name = getattr(self.llm, 'model', 'unknown') if hasattr(self.llm, 'model') else 'fallback_chain_model'
                track_llm_usage(response, "minecraft_eden_simulation", model_name)
            except Exception:
                pass
                
            # Lưu vào ChromaDB với Metadata chuẩn
            doc_id = f"lore_{int(time.time())}"
            metadata = {
                "agent_id": "player_steve_01",
                "memory_type": "semantic",
                "importance_score": 0.8,
                "last_accessed_at": int(time.time()),
                "access_count": 1,
                "is_core_knowledge": False
            }
            
            # Lấy vector embedding (ChromaDB có thể tự tính nhưng dùng embedding ngoài sẽ đồng bộ hơn)
            vector = self.embeddings.embed_query(compressed_lore)
            
            self.collection.add(
                ids=[doc_id],
                embeddings=[vector],
                documents=[compressed_lore],
                metadatas=[metadata]
            )
            
            print("✅ [Memory] Đã nén và lưu Vector Embedding thành công!")
            
            # Dọn rác
            self.short_term_memory.clear()
            self.total_importance = 0.0
            self._garbage_collection()
            
        except Exception as e:
            print(f"⚠️ [Memory] Lỗi khi nén ký ức: {e}")

    def _garbage_collection(self):
        """Xóa các ký ức không quan trọng theo Ebbinghaus Forgetting Curve."""
        try:
            # Dùng toán tử Where của ChromaDB để dọn rác các ký ức có importance < 0.3
            # Không được xóa is_core_knowledge = True
            self.collection.delete(where={
                "$and": [
                    {"importance_score": {"$lt": 0.3}},
                    {"is_core_knowledge": {"$eq": False}}
                ]
            })
            print("🧹 [Memory] Đã dọn dẹp các ký ức mờ nhạt (Garbage Collection).")
        except Exception as e:
            print(f"⚠️ [Memory] Lỗi Garbage Collection: {e}")

    def retrieve_memory(self, query: str, top_k: int = 2) -> str:
        """Truy xuất ký ức sử dụng thuật toán HyDE (Hypothetical Document Embeddings)."""
        print(f"🔍 [Memory] Đang truy xuất ký ức cho câu hỏi: '{query}'...")
        
        # 1. HyDE: Sinh câu trả lời ảo
        hyde_prompt = f"Hãy viết một đoạn văn ngắn mô tả cách giải quyết vấn đề sau trong thế giới sinh tồn cơ khí không có phép thuật: {query}"
        try:
            response = self.llm.invoke(hyde_prompt)
            hyde_response = response.content.strip()
            
            try:
                from src.token_tracker import track_llm_usage
                model_name = getattr(self.llm, 'model', 'unknown') if hasattr(self.llm, 'model') else 'fallback_chain_model'
                track_llm_usage(response, "minecraft_eden_simulation", model_name)
            except Exception:
                pass
                
            search_vector = self.embeddings.embed_query(hyde_response)
        except Exception as e:
            print(f"❌ [Circuit Breaker] Fallback truy xuất vector: {e}")
            # Fallback nếu LLM sập
            search_vector = self.embeddings.embed_query(query)
            
        # 2. Query ChromaDB
        try:
            results = self.collection.query(
                query_embeddings=[search_vector],
                n_results=top_k
            )
            
            if results['documents'] and len(results['documents'][0]) > 0:
                docs = results['documents'][0]
                # Cập nhật access_count và last_accessed_at cho metadata nếu cần
                return "\n".join(docs)
        except Exception as e:
            print(f"⚠️ [Memory] Lỗi truy xuất: {e}")
            
        return ""
