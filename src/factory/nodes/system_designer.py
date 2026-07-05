import os
import json
from pathlib import Path
from src.base_agent import BaseAgent

class SystemDesigner(BaseAgent):
    """
    Agent System Designer:
    - Chịu trách nhiệm trực quan hóa cấu trúc hệ thống.
    - Vẽ biểu đồ Mermaid từ Core tới các module dự án.
    - Duy trì bản đồ thư mục thông minh.
    """
    def __init__(self):
        super().__init__(
            name="SystemDesigner",
            role="Kiến trúc sư Trực quan hóa Hệ thống",
            agent_label="tier-2",
            temperature=0.1
        )
        self.root_dir = Path(__file__).resolve().parent.parent.parent.parent

    def _ai_handler(self, inventory_data: dict):
        # Trích xuất thông tin rút gọn để tránh Token Limit
        minimal_data = []
        for path, meta in inventory_data.items():
            minimal_data.append({
                "p": path,
                "imp": meta.get("imported_by", [])[:3] # Chỉ lấy 3 dependency tiêu biểu
            })

        prompt = f"""Bạn là một Principal System Architect. Nhiệm vụ của bạn là vẽ biểu đồ Mermaid (graph TD) trực quan hóa cấu trúc hệ thống.
Dữ liệu rút gọn:
{json.dumps(minimal_data, indent=2)}

Yêu cầu:
1. Vẽ biểu đồ Mermaid `graph TD`.
2. Phân nhóm bằng `subgraph`: CORE (src/base_agent...), PROJECTS (ai_trading...), TOOLS, UTILS.
3. Chỉ vẽ các node quan trọng nhất.
4. Trả về DUY NHẤT nội dung Mermaid, không giải thích.
"""
        result = self._call_llm(prompt)
        # Nếu LLM trả về có bọc ```mermaid thì tách ra
        if "```" in result:
            import re
            match = re.search(r'```(?:mermaid)?\n?(.*?)\n?```', result, re.DOTALL)
            if match:
                result = match.group(1).strip()
        return result.strip()

    def _logic_handler(self, *args, **kwargs):
        return "graph TD\n  Core --> Projects"

    def generate_mermaid_map(self, inventory_report_path: str, output_path: str):
        """Đọc báo cáo từ AID Taskforce và sinh biểu đồ Mermaid."""
        if not os.path.exists(inventory_report_path):
            print(f"[-] Không tìm thấy báo cáo inventory: {inventory_report_path}")
            return

        with open(inventory_report_path, "r", encoding="utf-8") as f:
            inventory = json.load(f)

        # Lọc bớt dữ liệu để tránh tràn Context window của LLM
        # Chỉ lấy file core và các file python có dependency rõ ràng
        filtered_inventory = {k: v for k, v in inventory.items() if v.get("is_core") or (k.endswith(".py") and v.get("imported_by"))}
        
        # Nếu vẫn quá nhiều, chỉ lấy Top 30 file quan trọng nhất
        if len(filtered_inventory) > 30:
            core_files = {k: v for k, v in filtered_inventory.items() if v.get("is_core")}
            active_files = {k: v for k, v in filtered_inventory.items() if not v.get("is_core")}
            # Sắp xếp active files theo số lượng dependency
            sorted_active = sorted(active_files.items(), key=lambda x: len(x[1].get("imported_by", [])), reverse=True)
            filtered_inventory = {**core_files, **dict(sorted_active[:20])}

        print(f"[*] System Designer đang phác thảo biểu đồ kiến trúc ({len(filtered_inventory)} nodes)...")
        mermaid_code = self._ai_handler(filtered_inventory)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# 🗺️ SOVEREIGN SYSTEM ARCHITECTURE MAP\n\n")
            f.write("```mermaid\n")
            f.write(mermaid_code)
            f.write("\n```\n")
        
        print(f"[+] Biểu đồ kiến trúc đã được lưu tại: {output_path}")

if __name__ == "__main__":
    designer = SystemDesigner()
    designer.generate_mermaid_map(
        "projects/asset_audit_taskforce/scout_report.json",
        "reports/SOVEREIGN_ARCH_MAP.md"
    )
