import os
import shutil
from pathlib import Path
from typing import Optional
from core.logic_auditor import auditor

class SafeFileManager:
    """
    Sovereign Safe File Manager.
    Cưỡng chế quy trình Draft & Verify (LV4) để bảo vệ hệ thống Core.
    """
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.sandbox_dir = self.root_dir / "temp_workspace" / "fault_isolation_sandbox"
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)

    def write_to_sandbox(self, file_path: str, content: str) -> str:
        """Viết code nháp vào Sandbox để kiểm thử."""
        original_path = Path(file_path)
        file_name = original_path.name
        draft_path = self.sandbox_dir / f"draft_{file_name}"
        
        with open(draft_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"🛡️ [SafeFile] Bản nháp đã được lưu tại: {draft_path}")
        return str(draft_path)

    def request_merge(self, draft_path: str, target_path: str, task_name: str) -> bool:
        """
        Gửi yêu cầu merge từ Sandbox vào file gốc.
        Chỉ thực hiện nếu LogicAuditor xác nhận 'Evolution Confirmed'.
        """
        # Giả sử chúng ta đã chạy test trước đó và auditor đã có dữ liệu
        # Ở đây ta gọi evaluate để chốt sổ
        report = auditor.evaluate_evolution(task_name, {})
        
        if "PASSED" in report["status"]:
            print(f"✅ [SafeFile] Tiến hóa xác nhận! Đang merge {draft_path} -> {target_path}")
            shutil.copy(draft_path, target_path)
            return True
        else:
            print(f"🚨 [SafeFile] Tiến hóa thất bại! Merge bị từ chối. Lý do: {report['reasoning']}")
            return False

safe_file_manager = SafeFileManager()
