import os
import sys

# Đảm bảo import path đúng
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))

from projects.real_execution_simulator.agent import run_simulator

if __name__ == "__main__":
    print("="*50)
    print("🚀 KHỞI ĐỘNG REAL EXECUTION SIMULATOR")
    print("="*50)
    
    target_file = "projects/real_execution_simulator/buggy_script.py"
    task = f"Hãy chạy file {target_file}. Nó đang bị lỗi. Bạn cần đọc nội dung, tìm ra lỗi sai import và logic, ghi đè file để sửa, và chạy lại cho đến khi thành công."
    
    run_simulator(task=task, target_file=target_file, max_iterations=5)
