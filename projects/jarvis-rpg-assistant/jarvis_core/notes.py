# jarvis_core/notes.py

import datetime
import logging
import os
from typing import Tuple

# Định nghĩa đường dẫn file journal
JOURNAL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'journal.md')

logging.basicConfig(level=logging.INFO)


def add_note(note_content: str) -> Tuple[bool, str]:
    """
    Ghi một ghi chú mới cùng với timestamp vào file journal.
    """
    # Đảm bảo thư mục data tồn tại
    data_dir = os.path.dirname(JOURNAL_PATH)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Sử dụng format Markdown để dễ đọc
    entry = f"## 📝 Journal Entry: {timestamp}\n"
    entry += f"{note_content}\n\n"
    entry += "---\n"  # Dấu phân cách

    try:
        # Mở file ở chế độ 'a' (append) và encoding utf-8
        with open(JOURNAL_PATH, 'a', encoding='utf-8') as f:
            f.write(entry)

        logging.info(f"Đã lưu ghi chú: '{note_content[:50]}...' vào {JOURNAL_PATH}")
        return True, "Ghi chú đã được lưu thành công."

    except IOError as e:
        error_msg = f"Lỗi I/O khi ghi file Journal: {e}"
        logging.error(error_msg)
        return False, error_msg


if __name__ == "__main__":
    # Test nhanh module
    add_note("Ý tưởng GameFi mới: Token Burning theo cơ chế Tái sinh (Rebirth).")
