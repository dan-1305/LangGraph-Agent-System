import os
import datetime
from pathlib import Path

def write_to_encyclopedia(error_name: str, symptoms: str, root_cause: str, action_item: str):
    """
    Ghi lỗi mới vào Bách khoa toàn thư để các Agent RAG có thể học được.
    """
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    file_path = base_dir / "docs" / "ERROR_ENCYCLOPEDIA.md"
    
    # Số thứ tự lỗi mới
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Đếm số lượng "## " để biết id tiếp theo
        count = content.count("## ")
        new_id = count + 1
    except FileNotFoundError:
        content = "# 📚 BÁCH KHOA TOÀN THƯ LỖI (ERROR ENCYCLOPEDIA)\n\n"
        new_id = 1
        
    new_entry = f"""
## {new_id}. LỖI TỰ ĐỘNG PHÁT HIỆN: {error_name}
- **Thời gian (Timestamp):** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Triệu chứng (Symptoms):** {symptoms}
- **Nguyên nhân gốc (Root Cause):** {root_cause}
- **Cách khắc phục đề xuất (Action Item):** {action_item}
---
"""
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(new_entry)
        
    print(f"✅ Đã ghi nhận Bug {new_id} vào ERROR_ENCYCLOPEDIA.md")
    
    # Tự động trigger RAG Ingest ngầm nếu có thể
    # ... (Trong thực tế nên đưa vào message queue hoặc chạy cronjob sau)
