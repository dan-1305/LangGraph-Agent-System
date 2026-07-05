import os
import random
import time
from typing import Dict, List

class CEOTrainingArena:
    """
    Môi trường huấn luyện chuyên biệt dành cho CEO (Cline).
    Mục tiêu: Ép CEO sử dụng Metadata DB và suy luận thay vì brute-force đọc file.
    """
    
    def __init__(self):
        self.scenarios: List[Dict] = [
            {
                "id": "SCENARIO_01_TOKEN_BLEED",
                "title": "Phát hiện Phình Context Window",
                "description": (
                    "Dự án 'projects/jarvis-rpg-assistant' đang ngốn quá nhiều token do "
                    "thư mục '.venv' chưa được chặn đúng cách. \n"
                    "NHIỆM VỤ: Hãy dùng SQLite MCP truy vấn 'SYSTEM_MAP_METADATA.db' để đếm "
                    "số file rác, sau đó cập nhật '.clineignore' để chặn thư mục này."
                ),
                "expected_tools": ["sqlite", "replace_in_file"],
                "max_tokens": 15000
            },
            {
                "id": "SCENARIO_02_CIRCULAR_IMPORT",
                "title": "Gỡ rối Phụ thuộc (Dependency Hell)",
                "description": (
                    "File 'tools/system/project_indexer.py' đang dùng hàm từ một project con "
                    "gây nguy cơ Circular Dependency. \n"
                    "NHIỆM VỤ: Hãy dùng 'sequentialthinking' để phân tích luồng import, "
                    "và cấu trúc lại import để nó độc lập."
                ),
                "expected_tools": ["read_file", "sequentialthinking", "replace_in_file"],
                "max_tokens": 25000
            },
            {
                "id": "SCENARIO_03_COMPLIANCE_BREACH",
                "title": "Khủng hoảng Kiến trúc (Security Guard)",
                "description": (
                    "Một developer vừa push code vào 'projects/nsfw_multimedia_auditor' nhưng "
                    "quên kế thừa BaseAgent. \n"
                    "NHIỆM VỤ: Hãy tìm file vi phạm bằng lệnh SQL hoặc grep nhanh, "
                    "sửa lại code kế thừa BaseAgent, và chạy Pytest để xác nhận."
                ),
                "expected_tools": ["sqlite", "replace_in_file", "execute_command"],
                "max_tokens": 30000
            }
        ]

    def start_exam(self):
        print("\n" + "="*60)
        print("🏛️ THE SOVEREIGN ARENA: CEO EXAMINATION INITIATED 🏛️")
        print("="*60)
        print("Mục tiêu: Đánh giá khả năng hiểu sâu Monorepo và tối ưu Token.\n")
        
        scenario = random.choice(self.scenarios)
        
        print(f"🔥 BÀI THI: {scenario['title']}")
        print(f"🆔 ID: {scenario['id']}")
        print("-" * 60)
        print(f"MÔ TẢ:\n{scenario['description']}")
        print("-" * 60)
        print(f"⏳ YÊU CẦU TỐI ƯU:")
        print(f"- Công cụ khuyến nghị: {', '.join(scenario['expected_tools'])}")
        print(f"- Giới hạn Token (Ước tính): {scenario['max_tokens']}")
        print("\n[HƯỚNG DẪN CHO ADMIN]:")
        print("Hãy copy đoạn MÔ TẢ trên và dán vào khung chat của Cline.")
        print("Kèm theo lệnh: '[FORCE_EXAM] Hãy giải quyết vấn đề này ngay lập tức.'")
        print("="*60 + "\n")

if __name__ == "__main__":
    arena = CEOTrainingArena()
    arena.start_exam()
