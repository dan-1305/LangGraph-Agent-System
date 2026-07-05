import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any
import random

# Path setup
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.base_agent import BaseAgent
from tools.system.rag_query import query_rag_return_context

class LibrarianAgent(BaseAgent):
    """Agent phụ trách việc đọc sách, tóm tắt và cập nhật vào bộ nhớ dài hạn."""
    
    def __init__(self):
        super().__init__(model_name="gemini-3.1-pro-preview", agent_label="tier-1")
        self.kb_dir = root_dir / "data" / "knowledge_base"
        self.lore_file = root_dir / "context" / "SYSTEM_LORE.md"

    def _ai_handler(self, book_name: str, chunk_content: str) -> str:
        prompt = f"""Bạn là LIBRARIAN của vương triều AI. 
Nhiệm vụ: Đọc đoạn trích dưới đây từ quyển sách '{book_name}' và rút ra 1-2 nguyên lý cốt lõi (Core Principles) có thể áp dụng để nâng cấp hệ thống LangGraph Agent hiện tại.

ĐOẠN TRÍCH:
{chunk_content}

YÊU CẦU:
- Trình bày dưới dạng Markdown Bullet points.
- Chỉ tập trung vào tính ứng dụng cho AI và Hệ thống.
- Ngôn ngữ: Tiếng Việt, súc tích.
"""
        response = self._call_llm(prompt)
        return response

    def _logic_handler(self, *args, **kwargs) -> str:
        return "Librarian logic fallback: Unable to process book chunk."

    def read_random_wisdom(self):
        """Chọn ngẫu nhiên một mẩu tri thức từ Knowledge DB và học tập."""
        print(f"📖 [Librarian] Đang tìm kiếm tri thức từ Tàng Kinh Các...")
        
        # Giả lập chọn một chủ đề quan trọng
        topics = ["Clean Architecture", "System Design", "Trading Psychology", "Prompt Engineering"]
        topic = random.choice(topics)
        
        # Query từ Knowledge DB (ổ D)
        context = query_rag_return_context(f"Nguyên lý cốt lõi về {topic}", collection_name="knowledge_base_core")
        
        if not context or "No relevant context found" in context:
            print(f"⚠️ Không tìm thấy tri thức về {topic} trong DB.")
            return

        wisdom = self.execute(book_name=topic, chunk_content=context)
        
        # Cập nhật vào SYSTEM_LORE.md
        with open(self.lore_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n### 🎓 Thấu thị từ {topic} ({datetime.now().strftime('%Y-%m-%d')})\n")
            f.write(wisdom)
            
        print(f"✅ Đã nạp tri thức mới về {topic} vào SYSTEM_LORE.md")

if __name__ == "__main__":
    from datetime import datetime
    librarian = LibrarianAgent()
    librarian.read_random_wisdom()
