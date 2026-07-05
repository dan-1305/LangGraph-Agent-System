import os
import sys
import random
import traceback
import importlib.util
from pathlib import Path

# Fix import path
base_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.append(str(base_dir))

from projects.qa_chaos_agent.src.llm_autopsy import LLMAutopsy
from projects.qa_chaos_agent.src.encyclopedia_writer import write_to_encyclopedia

class FuzzerEngine:
    def __init__(self):
        self.map_file = base_dir / "docs" / "SYSTEM_MAP.md"
        self.autopsy = LLMAutopsy()
        
    def extract_python_files_from_map(self):
        """Đọc SYSTEM_MAP.md để lấy ra các file Python có thể Fuzz."""
        files = []
        try:
            with open(self.map_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("### 📄 File: `"):
                        # Extract the path from markdown: "### 📄 File: `src/api_gateway.py`"
                        path = line.split("`")[1]
                        if not "qa_chaos_agent" in path and not "test_" in path:
                            files.append(path)
        except Exception:
            pass
        return files

    def dummy_fuzz_import(self, file_path):
        """
        Thử import module động để kiểm tra lỗi cú pháp, lỗi thiếu import (ModuleNotFoundError),
        hoặc code chạy ngoài scope.
        """
        module_name = file_path.replace(".py", "").replace("/", ".").replace("\\", ".")
        print(f"[*] Đang Fuzzing Import: {module_name}...")
        try:
            spec = importlib.util.spec_from_file_location(module_name, str(base_dir / file_path))
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"✅ {module_name} Pass (Import OK).")
                return True
            return False
        except Exception as e:
            tb = traceback.format_exc()
            print(f"❌ CRASH PHÁT HIỆN TẠI {module_name}!")
            
            # Chỉ gọi LLM nếu lỗi thực sự nguy hiểm (bỏ qua những lỗi do thiếu biến môi trường trong lúc test)
            if "ModuleNotFoundError" in str(e) or "SyntaxError" in str(e) or "AttributeError" in str(e):
                self.process_crash(module_name, tb)
            return False

    def process_crash(self, module_name, tb):
        print("🔍 Đang gửi Traceback cho Bác sĩ pháp y LLM...")
        analysis = self.autopsy.analyze_crash(module_name, tb)
        
        cause = analysis.get("cause", "Lỗi Fuzzing không xác định.")
        action = analysis.get("action", "Cần kiểm tra kỹ mã nguồn.")
        
        error_name = tb.strip().split("\n")[-1]
        symptoms = f"Module `{module_name}` crash khi thử Import/Load trong môi trường trống."
        
        write_to_encyclopedia(error_name, symptoms, cause, action)

    def run_nightly_fuzz(self, max_files=2):
        """Chạy Fuzzing ngẫu nhiên 2 file mỗi đêm để nhẹ server."""
        print("========================================")
        print("🌪️ KHỞI ĐỘNG QA CHAOS AGENT (FUZZER) 🌪️")
        print("========================================")
        
        files = self.extract_python_files_from_map()
        if not files:
            print("Không tìm thấy file nào trong SYSTEM_MAP.md")
            return
            
        # Bắt buộc Fuzzing 3 Hero Products trước khi đem bán
        hero_products = [
            "projects/auto_affiliate_video/app.py",
            "projects/auto_x_bot/app.py",
            "projects/godot_translator/app.py"
        ]
        
        # Lọc ra các file có thực (tránh lỗi file không tồn tại)
        targets = [f for f in hero_products if os.path.exists(base_dir / f)]
        
        if not targets:
            # Fallback ngẫu nhiên nếu không tìm thấy hero products
            targets = random.sample(files, min(max_files, len(files)))
            
        for t in targets:
            self.dummy_fuzz_import(t)
            
        print("========================================")
        print("✅ Đã hoàn tất phiên Fuzzing ban đêm.")

if __name__ == "__main__":
    fuzzer = FuzzerEngine()
    fuzzer.run_nightly_fuzz()
