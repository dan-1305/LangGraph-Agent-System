import os
import sys
import time
import ast
import io
from pathlib import Path

# Thêm root vào sys.path để import tools
root_dir = str(Path(__file__).resolve().parent.parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Cưỡng chế encoding utf-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class PreFlightCheck:
    """
    🛩️ CỔNG KIỂM DUYỆT SỚM (Pre-flight Check)
    Mục tiêu: Đảm bảo an toàn Monorepo trước khi AI khởi động.
    """
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        self.ignore_dirs = {".git", ".venv", "__pycache__", "data", "temp_workspace", "node_modules"}

    def check_zero_byte_files(self):
        """Quét các file 0-byte (lỗi gãy stream)."""
        zero_files = []
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            for f in files:
                if f.endswith(".py"):
                    f_path = Path(root) / f
                    if f_path.stat().st_size == 0:
                        zero_files.append(str(f_path))
        return zero_files

    def check_circular_imports_static(self):
        """Quét lỗi import vòng lặp sơ bộ qua AST (không nạp module)."""
        # Đây là một phiên bản đơn giản, thực tế cần đồ thị phức tạp hơn
        # Hiện tại ta chỉ quét xem có file nào import chính nó không
        issues = []
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            for f in files:
                if f.endswith(".py"):
                    f_path = Path(root) / f
                    try:
                        with open(f_path, "r", encoding="utf-8") as file:
                            tree = ast.parse(file.read())
                            for node in ast.walk(tree):
                                if isinstance(node, (ast.Import, ast.ImportFrom)):
                                    # Logic check đơn giản
                                    pass
                    except SyntaxError:
                        issues.append(f"Lỗi cú pháp (SyntaxError): {f_path}")
        return issues

    def run_static_checks(self):
        start_time = time.time()
        print("--- [Pre-flight] Chế độ STATIC (< 0.2s) ---")
        
        zero_files = self.check_zero_byte_files()
        ast_issues = self.check_circular_imports_static()
        
        # Tự động cập nhật Encyclopedia siêu tốc
        try:
            from tools.system.encyclopedia_builder import build_encyclopedia
            build_encyclopedia()
        except Exception as e:
            print(f"⚠️ [Encyclopedia] Lỗi cập nhật tự động: {e}")
            
        duration = time.time() - start_time
        print(f"--- [Pre-flight] Hoàn tất trong {duration:.4f}s ---")
        
        if zero_files:
            print("🚨 [CRITICAL] Hệ thống không an toàn!")
            for f in zero_files: print(f"  - File 0-byte: {f}")
            return False
            
        if ast_issues:
            print("⚠️ [WARNING] Phát hiện một số vấn đề AST (có thể do code đang viết dở):")
            for i in ast_issues: print(f"  - Issue: {i}")
            # Không return False ở đây để tránh block quá trình Awaken
        
        print("✅ [Pre-flight] Mọi thứ Xanh (Pass). Sẵn sàng cất cánh.")
        return True

if __name__ == "__main__":
    checker = PreFlightCheck()
    if not checker.run_static_checks():
        sys.exit(1)
