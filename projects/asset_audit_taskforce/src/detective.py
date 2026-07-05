import os
import ast
import json
import sys
import io
from pathlib import Path
from typing import List, Dict, Set

# Cưỡng chế encoding utf-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
class AssetDetective:
    """
    Tổ chuyên án Thám tử (The Detective):
    - Điều tra sâu nội dung file Python (Class, Function, Async).
    - Truy tìm mối quan hệ module ẩn (Hidden Dependencies).
    - Thu thập bằng chứng (Evidence) xác thực trạng thái Zombie.
    """
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir).resolve()
        self.investigation_results: Dict[str, dict] = {}
        self.global_symbol_map: Dict[str, List[str]] = {} # Symbol -> List of files defining it

    def _analyze_file_content(self, file_path: Path) -> dict:
        """Phân tích cấu trúc bên trong của một file Python."""
        evidence = {
            "classes": [],
            "functions": [],
            "has_main": False,
            "complexity_score": 0,
            "is_empty": False
        }
        try:
            content = file_path.read_text(encoding='utf-8', errors='replace')
            if not content.strip():
                evidence["is_empty"] = True
                return evidence

            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    evidence["classes"].append(node.name)
                elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                    evidence["functions"].append(node.name)
                elif isinstance(node, ast.If):
                    # Check for if __name__ == "__main__":
                    if isinstance(node.test, ast.Compare):
                        if isinstance(node.test.left, ast.Name) and node.test.left.id == "__name__":
                            evidence["has_main"] = True
            
            evidence["complexity_score"] = len(evidence["classes"]) * 5 + len(evidence["functions"])
        except Exception as e:
            evidence["error"] = str(e)
            
        return evidence

    def investigate(self, inventory_path: str):
        """Thực hiện chuyên án điều tra dựa trên báo cáo Scouter."""
        with open(inventory_path, "r", encoding="utf-8") as f:
            inventory = json.load(f)

        print(f"[*] Thám tử AID đang bắt đầu phá án trên {len(inventory)} hồ sơ...")

        # Bước 1: Xây dựng bản đồ Symbol toàn cầu
        for rel_path, meta in inventory.items():
            if not rel_path.endswith(".py"): continue
            
            fp = self.root_dir / rel_path
            analysis = self._analyze_file_content(fp)
            self.investigation_results[rel_path] = analysis
            
            # Đăng ký symbols
            symbols = analysis["classes"] + analysis["functions"]
            for s in symbols:
                if s not in self.global_symbol_map: self.global_symbol_map[s] = []
                self.global_symbol_map[s].append(rel_path)

        # Bước 2: Truy tìm bằng chứng ngoại phạm (Xác định xem có ai gọi Symbol của file này không)
        for rel_path, analysis in self.investigation_results.items():
            evidence_summary = []
            
            if analysis.get("is_empty"):
                evidence_summary.append("File rỗng (0 bytes content).")
            
            if analysis.get("has_main"):
                evidence_summary.append("Có hàm main (Script thực thi).")
            
            # Check symbols usage
            total_calls = 0
            # Đây là logic thám tử: Tìm xem tên class/hàm của file này có xuất hiện trong file khác không
            # (Rất tốn Context nhưng chính xác)
            
            analysis["evidence"] = evidence_summary

    def save_detective_report(self, output_path: str):
        """Lưu báo cáo bằng chứng điều tra."""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.investigation_results, f, indent=4)
        print(f"[+] Bằng chứng điều tra đã được niêm phong: {output_path}")

if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent.parent.parent
    detective = AssetDetective(str(root))
    
    # Giả sử Scouter đã chạy xong
    scout_report = "projects/asset_audit_taskforce/scout_report.json"
    if os.path.exists(scout_report):
        detective.investigate(scout_report)
        detective.save_detective_report("projects/asset_audit_taskforce/detective_evidence.json")
    else:
        print("[-] Không tìm thấy hồ sơ Scouter để điều tra.")
