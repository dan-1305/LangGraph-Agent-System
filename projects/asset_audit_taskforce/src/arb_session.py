from src.base_agent import BaseAgent
import os
import sys
from pathlib import Path

# Setup PYTHONPATH
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from projects.asset_audit_taskforce.src.scouter import MetadataScouter
from projects.asset_audit_taskforce.src.detective import AssetDetective
from projects.asset_audit_taskforce.src.auditor import LogicAuditor
from src.factory.nodes.system_designer import SystemDesigner
from src.factory.nodes.architecture_critic import ArchitectureCritic

class ArchitectureReconstructionBoard(BaseAgent):
    """
    Ban Dự án Tái thiết Kiến trúc (ARB):
    - Phối hợp giữa AID Taskforce và ARB Agents.
    - Trực quan hóa và Đánh giá hệ thống toàn diện.
    """
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent.parent
        self.scout_report = "projects/asset_audit_taskforce/scout_report.json"
        self.detective_report = "projects/asset_audit_taskforce/detective_evidence.json"
        self.audit_md = "reports/SOVEREIGN_ASSET_AUDIT.md"
        self.arch_map_md = "reports/SOVEREIGN_ARCH_MAP.md"
        self.maturity_md = "reports/SOVEREIGN_MATURITY_ASSESSMENT.md"

    def run_full_session(self):
        print("=== [ARB] BẮT ĐẦU PHIÊN HỌP TÁI THIẾT KIẾN TRÚC ===")
        
        # 1. Thu thập dữ liệu thô
        scouter = MetadataScouter(str(self.root_dir))
        scouter.scan_all()
        scouter.save_report(self.scout_report)
        
        # 2. Điều tra bằng chứng
        detective = AssetDetective(str(self.root_dir))
        detective.investigate(self.scout_report)
        detective.save_detective_report(self.detective_report)
        
        # 3. Thẩm định và phân loại
        auditor = LogicAuditor(self.scout_report, self.detective_report)
        auditor.generate_sovereign_report(self.audit_md)
        audit_results = auditor.audit()
        
        # 4. Trực quan hóa (System Designer)
        designer = SystemDesigner()
        designer.generate_mermaid_map(self.scout_report, self.arch_map_md)
        
        # 5. Phê bình kiến trúc (Architecture Critic)
        critic = ArchitectureCritic()
        critic.evaluate_core_maturity(audit_results["GOLD"], self.maturity_md)
        
        print("\n=== [ARB] PHIÊN HỌP KẾT THÚC. TẤT CẢ BÁO CÁO ĐÃ SẴN SÀNG TRONG /reports ===")

if __name__ == "__main__":
    arb = ArchitectureReconstructionBoard()
    arb.run_full_session()
