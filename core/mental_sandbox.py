import os
import shutil
import tempfile
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

# Ensure UTF-8 for Windows
if hasattr(sys.stdout, 'reconfigure'):
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

class MentalSandbox:
    """
    [ROLE: Principal System Architect / Chaos Engineer]
    Cơ chế "Nghĩ hai lần, viết một lần" (Draft & Verify).
    Tạo ra một môi trường cách ly (Sandbox) để chạy thử nghiệm các thay đổi code
    trước khi cho phép merge vào file core.
    """
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.sandbox_dir = self.root_dir / "temp_workspace" / "mental_sandbox"
        self._ensure_sandbox()

    def _ensure_sandbox(self):
        if not self.sandbox_dir.exists():
            self.sandbox_dir.mkdir(parents=True, exist_ok=True)

    def create_draft(self, original_file: str, new_content: str) -> Path:
        """Tạo bản nháp của file trong sandbox."""
        rel_path = Path(original_file).relative_to(self.root_dir)
        draft_path = self.sandbox_dir / rel_path
        draft_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(draft_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        # In log không dùng emoji để tránh lỗi encoding trên một số môi trường
        print(f"[Sandbox] Draft created at: {draft_path}")
        return draft_path

    def verify_syntax(self, file_path: Path) -> bool:
        """Kiểm tra lỗi cú pháp (Syntax Check) bằng AST."""
        try:
            import ast
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                tree = ast.parse(content)
            
            # [VULN-001 FIX] Kiểm tra Logic Runtime (Infinite Loops)
            if not self.verify_logic(tree):
                return False
                
            print(f"[Sandbox] Syntax & Logic Check PASSED: {file_path.name}")
            return True
        except SyntaxError as e:
            print(f"[Sandbox] Syntax Error: {e}")
            return False

    def verify_logic(self, tree: 'ast.AST') -> bool:
        """
        [VULN-001] Kiểm tra các lỗi logic nguy hiểm (Runtime Risks).
        """
        import ast
        for node in ast.walk(tree):
            # 1. Phát hiện vòng lặp vô hạn: while True hoặc while 1
            if isinstance(node, ast.While):
                if isinstance(node.test, ast.Constant) and node.test.value:
                    # Kiểm tra xem có lệnh break hoặc return bên trong không
                    has_exit = False
                    for subnode in ast.walk(node):
                        if isinstance(subnode, (ast.Break, ast.Return)):
                            has_exit = True
                            break
                    if not has_exit:
                        print("[Sandbox] [CRITICAL] Potential Infinite Loop detected (while True with no break/return).")
                        return False
            
            # 2. Phát hiện đệ quy không kiểm soát (Đơn giản: Hàm gọi chính nó)
            if isinstance(node, ast.FunctionDef):
                for subnode in ast.walk(node):
                    if isinstance(subnode, ast.Call) and isinstance(subnode.func, ast.Name):
                        if subnode.func.id == node.name:
                            # Đây là đệ quy, tạm thời cảnh báo (có thể hợp lệ nhưng rủi ro)
                            print(f"[Sandbox] [WARNING] Recursion detected in function '{node.name}'.")
        
        return True

    def run_unit_tests(self, test_pattern: str = "tests/") -> bool:
        """
        Chạy các bài unit test liên quan.
        """
        print(f"[Sandbox] Running tests: {test_pattern}...")
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{self.sandbox_dir}{os.pathsep}{self.root_dir}"
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_pattern],
                capture_output=True,
                text=True,
                env=env,
                timeout=60
            )
            if result.returncode == 0:
                print("[Sandbox] Unit Tests PASSED!")
                return True
            else:
                print(f"[Sandbox] Unit Tests FAILED:\n{result.stdout}")
                return False
        except Exception as e:
            print(f"[Sandbox] Test execution error: {e}")
            return False

    def deploy_draft(self, draft_path: Path, original_file: Path):
        """Merge bản nháp vào file gốc sau khi đã qua kiểm duyệt."""
        print(f"[Sandbox] Deploying draft to {original_file}...")
        shutil.copy2(draft_path, original_file)
        print("[Sandbox] Deployment successful!")

    def cleanup(self):
        """Dọn dẹp sandbox."""
        if self.sandbox_dir.exists():
            shutil.rmtree(self.sandbox_dir)

if __name__ == "__main__":
    # Test nhanh Sandbox
    root = Path(__file__).resolve().parent.parent
    sandbox = MentalSandbox(root)
    
    test_file = root / "src" / "base_agent.py"
    if test_file.exists():
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Thử tạo một bản nháp sạch
        draft = sandbox.create_draft(str(test_file), content + "\n# SANDBOX TEST\n")
        
        if sandbox.verify_syntax(draft):
            print("[Sandbox] Verification system working correctly.")
        
        sandbox.cleanup()
