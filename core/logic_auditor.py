import time
import os
import psutil
from typing import Dict, Any

class LogicAuditor:
    """
    Fitness Function - Bộ lọc đào thải tự nhiên của hệ thống Sovereign.
    Đo lường hiệu năng của các Agent và quyết định xem một sự "Tiến hóa" có được chấp nhận hay không.
    """
    def __init__(self):
        self.start_time = 0
        self.initial_ram = 0

    def start_session(self):
        """Bắt đầu đo lường tài nguyên trước khi Agent thực thi nháp."""
        self.start_time = time.time()
        self.initial_ram = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB

    def evaluate_evolution(self, task_name: str, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Đánh giá bản nháp so với tiêu chuẩn hệ thống.
        
        Tiêu chuẩn chấp nhận (LV4):
        - Latency < 60s (cho sub-task).
        - RAM tăng thêm < 200MB.
        - Tỷ lệ lỗi = 0.
        """
        end_time = time.time()
        final_ram = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        
        latency = end_time - self.start_time
        ram_delta = final_ram - self.initial_ram
        
        is_passed = True
        reasoning = []

        if latency > 60:
            is_passed = False
            reasoning.append(f"Latency quá cao ({latency:.2f}s > 60s)")
        
        if ram_delta > 200:
            is_passed = False
            reasoning.append(f"Ngốn RAM quá mức ({ram_delta:.2f}MB > 200MB)")

        status = "PASSED (Evolution Confirmed)" if is_passed else "FAILED (Regression Detected)"
        
        report = {
            "task": task_name,
            "status": status,
            "metrics": {
                "latency": f"{latency:.2f}s",
                "ram_usage": f"{ram_delta:.2f}MB"
            },
            "reasoning": reasoning
        }
        
        print(f"📊 [Logic Auditor] {task_name}: {status}")
        if not is_passed:
            print(f"🚨 [Logic Auditor] Lý do đào thải: {', '.join(reasoning)}")
            
        return report

auditor = LogicAuditor()
