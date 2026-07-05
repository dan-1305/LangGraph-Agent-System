import os
import sys
import time
import random
import threading
import psutil
from pathlib import Path

# Ensure UTF-8 for Windows
if hasattr(sys.stdout, 'reconfigure'):
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

class ChaosMonkey:
    """
    [ROLE: QA Chaos Overlord]
    Công cụ "Khỉ hỗn loạn" để thử nghiệm tính kiên cường của hệ thống.
    Chuyên tiêm lỗi, làm cạn kiệt tài nguyên và phá hoại luồng thực thi.
    """
    def __init__(self):
        self.is_active = False

    def simulate_memory_leak(self, target_mb: int, duration_sec: int):
        """Giả lập việc nuốt RAM để test Watchdog."""
        print(f"💀 [ChaosMonkey] Đang bắt đầu tấn công RAM: {target_mb}MB trong {duration_sec}s...")
        
        def leak():
            dummy_data = []
            chunk = "X" * (1024 * 1024) # 1MB string
            for _ in range(target_mb):
                dummy_data.append(chunk)
                time.sleep(0.1) # Leak từ từ
            
            print(f"💀 [ChaosMonkey] Đã đạt ngưỡng leak {target_mb}MB. Giữ trạng thái trong {duration_sec}s...")
            time.sleep(duration_sec)
            del dummy_data
            print("💀 [ChaosMonkey] Kết thúc tấn công RAM.")

        thread = threading.Thread(target=leak, daemon=True)
        thread.start()

    def simulate_api_blackout(self, duration_sec: int):
        """
        Giả lập việc mất kết nối API bằng cách tạm thời ghi đè URL trong .env
        hoặc chặn traffic (giả định thông qua mock).
        """
        print(f"💀 [ChaosMonkey] Kích hoạt API BLACKOUT trong {duration_sec}s...")
        # Lưu ý: Việc thực sự đổi .env rất nguy hiểm, nên ChaosMonkey thường dùng mock 
        # hoặc gán biến môi trường tạm thời cho tiến trình hiện tại.
        os.environ["GCLI_BASE_URL"] = "http://localhost:9999/invalid" # Trỏ vào port chết
        
        def restore():
            time.sleep(duration_sec)
            # Restore (trong thực tế cần lấy giá trị cũ từ .env)
            from dotenv import load_dotenv
            load_dotenv(override=True)
            print("💀 [ChaosMonkey] Đã phục hồi kết nối API.")

        threading.Thread(target=restore, daemon=True).start()

    def corrupt_database(self, db_path: str):
        """Tiêm dữ liệu rác vào Database để test Validation Gates."""
        print(f"💀 [ChaosMonkey] Đang tiêm dữ liệu rác vào {db_path}...")
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            # Thử tìm các bảng giá coin để tiêm giá ảo (VD: BTC = 1 triệu đô)
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            for table in tables:
                if "USD" in table:
                    conn.execute(f"UPDATE {table} SET Close = 1000000.0 WHERE Date = (SELECT MAX(Date) FROM {table});")
                    print(f"💀 [ChaosMonkey] Đã tiêm giá ảo vào bảng {table}")
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"💀 [ChaosMonkey] Lỗi khi phá hoại DB: {e}")

if __name__ == "__main__":
    monkey = ChaosMonkey()
    # Thử nghiệm leak nhẹ 100MB
    # monkey.simulate_memory_leak(100, 10)
    print("ChaosMonkey initialized and ready for carnage.")
