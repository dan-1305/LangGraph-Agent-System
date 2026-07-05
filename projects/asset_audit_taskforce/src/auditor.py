from src.base_agent import BaseAgent
import json
import sys
import io
from pathlib import Path
from typing import List, Dict

# Cưỡng chế encoding utf-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
class LogicAuditor(BaseAgent):
    """
    Thanh tra Logic (The Logic Auditor):
    - Đọc báo cáo từ Scouter và Bằng chứng từ Detective.
    - Phân tích giá trị của từng file dựa trên mức độ quan trọng và tần suất sử dụng.
    - Gán nhãn: [GOLD], [ACTIVE], [ZOMBIE], [RISK].
    """
    def __init__(self, scout_report_path: str, detective_report_path: str = None):
        self.report_path = Path(scout_report_path)
        with open(self.report_path, "r", encoding="utf-8") as f:
            self.inventory: Dict[str, dict] = json.load(f)
        
        self.evidence: Dict[str, dict] = {}
        if detective_report_path:
            with open(detective_report_path, "r", encoding="utf-8") as f:
                self.evidence = json.load(f)

    def audit(self) -> Dict[str, List[str]]:
        """Thực hiện kiểm toán logic."""
        results = {
            "GOLD": [],    # File cốt lõi
            "ACTIVE": [],  # File đang hoạt động (được import)
            "ZOMBIE": [],  # File không ai dùng, không rõ mục đích
            "RISK": []     # File có thể gây lỗi hoặc rác nặng
        }

        for rel_path, meta in self.inventory.items():
            # 1. Kiểm tra Core
            if meta["is_core"]:
                results["GOLD"].append(rel_path)
                continue

            # 2. Kiểm tra mức độ sử dụng (chỉ áp dụng cho .py)
            if rel_path.endswith(".py"):
                if meta["imported_by"]:
                    results["ACTIVE"].append(rel_path)
                else:
                    # Nếu là script thực thi (main, app, run...) thì vẫn coi là ACTIVE
                    if any(x in rel_path.lower() for x in ["main", "app", "run", "start", "dashboard", "advisor"]):
                        results["ACTIVE"].append(rel_path)
                    else:
                        results["ZOMBIE"].append(rel_path)
                continue

            # 3. Phân loại rác dựa trên định dạng
            if meta["extension"] in [".log", ".tmp", ".bak", ".old", ".zip"]:
                results["RISK"].append(rel_path)
            elif meta["extension"] == ".scn" or "archive" in rel_path.lower():
                results["ZOMBIE"].append(rel_path)
            else:
                results["ACTIVE"].append(rel_path)

        return results

    def generate_sovereign_report(self, output_path: str):
        """Tạo báo cáo Markdown cực gọn cho Boss duyệt."""
        audit_results = self.audit()
        
        report = "# 🏛️ SOVEREIGN ASSET AUDIT REPORT (WITH EVIDENCE)\n\n"
        report += f"> **Hệ thống:** LangGraph Monorepo | **Điều tra bởi:** AID Taskforce\n\n"
        
        report += "## 🏆 1. TÀI SẢN VÀNG (GOLD - IMMUTABLE)\n"
        report += "*Các file cốt lõi bảo vệ vương triều. CẤM CHẠM.*\n"
        for f in audit_results["GOLD"][:15]: # Show top 15
            report += f"- `[CORE]` {f}\n"
        report += "*(Và nhiều file core khác...)*\n\n"

        report += "## 🧟 2. DANH SÁCH ZOMBIE (XÁC THỰC BỞI THÁM TỬ)\n"
        report += "*Không có dependency, không được import, hoặc module rỗng.*\n"
        for f in audit_results["ZOMBIE"]:
            size = self.inventory[f]["size_kb"]
            ev = self.evidence.get(f, {})
            evidence_str = ""
            if ev:
                evidence_str = f" | **Bằng chứng:** {len(ev.get('classes', []))} classes, {len(ev.get('functions', []))} funcs"
                if ev.get("has_main"): evidence_str += ", Has Main"
                if ev.get("is_empty"): evidence_str = " | **Bằng chứng:** FILE RỖNG"
            
            report += f"- [ ] `{f}` ({size} KB){evidence_str}\n"
        
        report += "\n## ⚠️ 3. KHU VỰC RỦI RO (LOG/BACKUP/ZIP)\n"
        for f in audit_results["RISK"]:
            report += f"- [ ] `{f}`\n"

        report += "\n## ⚖️ QUYẾT ĐỊNH CỦA BOSS\n"
        report += "- **Phê duyệt:** Chạy `uv run python tools/system/system_cleaner.py --run` để di dời đống trên sang Lớp 1.\n"
        
        with open(output_path, "w", encoding="utf-8") as f:
            report = report.encode('utf-8', errors='replace').decode('utf-8')
            f.write(report)
        print(f"[+] Báo cáo Thẩm định đã sẵn sàng: {output_path}")

if __name__ == "__main__":
    auditor = LogicAuditor(
        "projects/asset_audit_taskforce/scout_report.json",
        "projects/asset_audit_taskforce/detective_evidence.json"
    )
    auditor.generate_sovereign_report("reports/SOVEREIGN_ASSET_AUDIT.md")
