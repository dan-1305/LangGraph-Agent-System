import os
import re
from pathlib import Path
from datetime import datetime

def compress_context():
    """
    Nén nội dung ACTIVE_THOUGHTS.md bằng cách lưu trữ các task đã hoàn thành.
    """
    thoughts_path = Path("context/ACTIVE_THOUGHTS.md")
    if not thoughts_path.exists():
        print("⚠️ Không tìm thấy ACTIVE_THOUGHTS.md")
        return

    with open(thoughts_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    completed_tasks = []
    in_completed_section = False

    # Regex để tìm task đã hoàn thành: - [x] Nội dung
    completed_pattern = re.compile(r"^\s*-\s*\[x\]\s*(.*)", re.IGNORECASE)
    
    for line in lines:
        # Bỏ qua phần archived cũ để ghi đè lại
        if "## 📜 LỊCH SỬ HOÀN THÀNH (ARCHIVED)" in line:
            in_completed_section = True
            continue
        
        if in_completed_section:
            continue

        match = completed_pattern.match(line)
        if match:
            task_content = match.group(1).strip()
            completed_tasks.append(task_content)
        else:
            new_lines.append(line)

    # Dọn dẹp các dòng trống thừa ở cuối new_lines
    while new_lines and new_lines[-1].strip() == "":
        new_lines.pop()

    # Thêm phần Archived
    new_lines.append("\n\n---\n\n## 📜 LỊCH SỬ HOÀN THÀNH (ARCHIVED)\n")
    if completed_tasks:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_lines.append(f"- **[{timestamp}]**: Đã hoàn thành {len(completed_tasks)} hạng mục (Xem chi tiết trong Chronicles).\n")
    else:
        new_lines.append("- (Chưa có hạng mục nào được nén)\n")

    with open(thoughts_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"✅ Đã nén {len(completed_tasks)} hạng mục trong ACTIVE_THOUGHTS.md")

def compress_text(text: str, max_length: int = 4000) -> str:
    """
    Tiện ích nén Token (Tokenomics Utility):
    Dành cho các đoạn text quá dài (như log, source code cũ), cắt bớt hoặc tóm tắt sơ bộ
    để không làm nổ Context Window của LLM.
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
        
    print(f"⚠️ [Tokenomics] Cảnh báo: Văn bản quá dài ({len(text)} ký tự). Đang tiến hành nén xuống {max_length} ký tự...")
    
    # Giữ lại 40% đầu và 60% cuối (thường lỗi nằm ở cuối log)
    head_len = int(max_length * 0.4)
    tail_len = int(max_length * 0.6)
    
    head = text[:head_len]
    tail = text[-tail_len:]
    
    compressed = f"{head}\n\n... [NỘI DUNG ĐÃ BỊ NÉN ĐỂ TIẾT KIỆM TOKEN] ...\n\n{tail}"
    return compressed

if __name__ == "__main__":
    compress_context()
