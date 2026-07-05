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
class MetadataScouter:
    """
    Đặc vụ Trinh sát (The Scout):
    - Quét toàn bộ Monorepo.
    - Phân tích Imports để tìm Dependency giữa các file.
    - Thu thập Metadata (Size, MTime, Path).
    """
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir).resolve()
        self.inventory: Dict[str, dict] = {}
        self.all_imports: Dict[str, Set[str]] = {}

    def _get_python_imports(self, file_path: Path) -> Set[str]:
        """Trích xuất danh sách các module được import trong một file python."""
        imports = set()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for n in node.names:
                            imports.add(n.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.add(node.module.split('.')[0])
        except Exception:
            pass
        return imports

    def scan_all(self):
        """Thực hiện quét toàn diện."""
        print(f"[*] Taskforce Scout đang tuần tra: {self.root_dir}")
        
        # Bỏ qua các thư mục không liên quan
        skip_dirs = {'.git', '.venv', '__pycache__', 'node_modules', 'monorepo_quarantine'}
        
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]
            
            for f in filenames:
                fp = Path(dirpath) / f
                rel_path = str(fp.relative_to(self.root_dir))
                
                stat = fp.stat()
                file_metadata = {
                    "path": rel_path,
                    "size_kb": round(stat.st_size / 1024, 2),
                    "last_modified": stat.st_mtime,
                    "extension": fp.suffix,
                    "is_core": self._is_core(rel_path),
                    "imported_by": []
                }
                
                if fp.suffix == ".py":
                    self.all_imports[rel_path] = self._get_python_imports(fp)
                
                self.inventory[rel_path] = file_metadata

        self._map_dependencies()

    def _is_core(self, rel_path: str) -> bool:
        """Kiểm tra xem file có thuộc danh sách Core/Immutable không."""
        core_keywords = ["src/base_agent", "monorepo_manifest", "awaken.py", ".clinerules", "core/"]
        return any(k in rel_path for k in core_keywords)

    def _map_dependencies(self):
        """Xây dựng bản đồ ngược: File này đang được những file nào import."""
        for target_file, metadata in self.inventory.items():
            if not target_file.endswith(".py"):
                continue
            
            module_name = Path(target_file).stem
            for source_file, imports in self.all_imports.items():
                if module_name in imports:
                    metadata["imported_by"].append(source_file)

    def save_report(self, output_path: str):
        """Lưu kết quả trinh sát ra file JSON."""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.inventory, f, indent=4)
        print(f"[+] Báo cáo trinh sát đã được lưu: {output_path}")

if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent.parent.parent
    scouter = MetadataScouter(str(root))
    scouter.scan_all()
    scouter.save_report("projects/asset_audit_taskforce/scout_report.json")
