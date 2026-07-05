import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import json
from src.factory.state import FactoryState
from core.principles_enforcer import enforcer

def principles_gate_node(state: FactoryState):
    """
    Sovereign Principles Gate.
    Đảm bảo mọi yêu cầu và ngữ cảnh đều tuân thủ nguyên lý hệ thống trước khi rẽ nhánh.
    Tích hợp Self-Healing Loop và Luồng Draft & Verify (LV4).
    """
    print("--- [Principles Gate] Kiểm soát tính chính trực ---")
    
    # Kiểm tra Hiến chương Tiến hóa (Evolution Charter)
    evolution_charter = Path(root_dir) / "docs" / "AGENT_EVOLUTION_STANDARDS.md"
    if evolution_charter.exists():
        print("[Principles Gate] Hiến chương LV4 đã được nạp. Đang thực thi 'La bàn Tiến hóa'...")
    
    user_req = state.get("user_requirement", "")
    code_context = state.get("code_context", "")
    
    # --- [Self-Healing Loop] Nạp ký ức thất bại ---
    failed_paths_file = Path(root_dir) / "logs" / "FAILED_PATHS.json"
    failure_context = ""
    if failed_paths_file.exists():
        try:
            with open(failed_paths_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                failures = data.get("failure_logs", [])
                if failures:
                    failure_context = "\n[FAILURE MEMORY - HÀNH VI CẦN TRÁNH]\n"
                    for fail in failures:
                        failure_context += f"- {fail}\n"
                    failure_context += "[/FAILURE MEMORY]\n"
                    print(f"[Principles Gate] Đã nạp {len(failures)} ký ức thất bại để phòng vệ.")
        except Exception as e:
            print(f"⚠️ [Principles Gate] Lỗi nạp FAILED_PATHS: {e}")

    # Kiểm tra độ tuân thủ của Requirement và Context
    req_score = enforcer.audit_agent_output(user_req)
    context_score = enforcer.audit_agent_output(code_context)
    
    avg_score = (req_score + context_score) / 2
    
    print(f"[Principles Gate] Score: {avg_score:.2f} (Req: {req_score:.2f}, Context: {context_score:.2f})")
    
    # Lưu điểm vào state để các Agent sau này có thể sử dụng (ví dụ: điều chỉnh mức độ rủi ro)
    state["qa_score"] = avg_score 
    
    if avg_score < 0.4:
        print("🚨 [Principles Gate] CẢNH BÁO: Độ tuân thủ nguyên lý cực thấp!")
        # Ta có thể ép buộc chuyển hướng hoặc thêm cảnh báo vào context
        state["code_context"] += "\n\n⚠️ [SYSTEM WARNING]: Yêu cầu này có dấu hiệu vi phạm nguyên lý hệ thống. Hãy cực kỳ cẩn trọng.\n"

    # Bơm ký ức thất bại vào context để Agent sau này né tránh
    if failure_context:
        state["code_context"] = failure_context + state["code_context"]

    # --- [Manifest-Driven Governance: Immutable Guard] ---
    # Sovereign Override: Cổng thoát hiểm tối cao cho Boss
    import os
    is_override = os.getenv("SOVEREIGN_OVERRIDE", "FALSE").upper() == "TRUE"
    
    manifest_path = Path(root_dir) / "monorepo_manifest.json"
    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
                immutable_files = manifest.get("immutable_files", [])
                
                # Kiểm tra xem yêu cầu có định sửa file bất biến không
                for imm_file in immutable_files:
                    if imm_file in user_req:
                        if is_override:
                            print(f"� [Principles Gate] OVERRIDE: Boss dang thuc thi quyen nang toi cao len file: {imm_file}")
                            state["code_context"] += f"\n[SYSTEM NOTICE] Cổng thoát hiểm Sovereign đã MỞ. Bạn được phép sửa file '{imm_file}' dưới sự giám sát trực tiếp của Boss.\n"
                        else:
                            print(f"�🚨 [Principles Gate] BLOCK: Phat hien yeu cau sua file bat bien: {imm_file}")
                            state["code_context"] += f"\n[CRITICAL BLOCK] Bạn KHÔNG ĐƯỢC PHÉP sửa file '{imm_file}'. Đây là file hệ thống bất biến. Mọi thay đổi sẽ bị từ chối.\n"
        except Exception as e:
            print(f"⚠️ [Principles Gate] Loi doc Manifest: {e}")

    # --- [Evolutionary Compass - Cưỡng chế Sandbox cho LV4] ---
    if avg_score > 0.7:
        print("[Principles Gate] Yêu cầu High-Impact phát hiện. Đang kích hoạt Mental Sandbox Protocol...")
        state["code_context"] += (
            "\n[SYSTEM PROTOCOL - LV4 STRATEGIC]\n"
            "Yêu cầu của bạn có tính ảnh hưởng cao. Bạn BẮT BUỘC phải tuân thủ quy trình Draft & Verify:\n"
            "1. Tuyệt đối KHÔNG dùng write_to_file/replace_in_file lên file gốc ngay lập tức.\n"
            "2. Hãy viết bản nháp vào: temp_workspace/fault_isolation_sandbox/draft_[file_name].py\n"
            "3. Sử dụng tool execute_command để chạy thử bản nháp đó.\n"
            "4. Chỉ merge khi đã xác nhận hoạt động 100%.\n"
            "[/SYSTEM PROTOCOL]\n"
        )

    return state
