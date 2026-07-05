import os
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.base_agent import BaseAgent
from src.factory.state import FactoryState

class RemediationAgent(BaseAgent):
    """
    Tác nhân Vá lỗi Tự động (Auto-Remediation).
    Tiếp nhận báo cáo lỗi từ Sandbox hoặc QA Agent, phân tích nguyên nhân và sinh ra mã nguồn mới (hoặc file patch).
    """
    def __init__(self):
        super().__init__(name="RemediationAgent", role="Kỹ sư Vá lỗi Tự động", agent_label="tier-2", temperature=0.3)

    def _ai_handler(self, **kwargs):
        test_results = kwargs.get("test_results_ptr", "")
        qa_report = kwargs.get("qa_report_ptr", "")
        code_context = kwargs.get("code_context", "")
        
        prompt = f"""
        Bạn là Remediation Agent - Kỹ sư vá lỗi hệ thống tự động.
        Nhiệm vụ của bạn là đọc báo cáo lỗi dưới đây và tiến hành SỬA MÃ NGUỒN.
        
        [JIT KNOWLEDGE BASE (Mã nguồn ban đầu)]
        {code_context}
        
        [QA REPORT / ARCHITECTURE CRITIQUE]
        {qa_report}
        
        [SANDBOX TEST RESULTS (Nếu có)]
        {test_results}
        
        YÊU CẦU:
        1. Phân tích nguyên nhân cốt lõi gây ra lỗi.
        2. Viết lại ĐOẠN CODE ĐÃ SỬA để khắc phục lỗi (đảm bảo PEP-8 và hiệu năng).
        3. CHỈ TRẢ VỀ code đã sửa trong thẻ ```python ... ```, kèm theo lời giải thích ngắn gọn. Không output lan man.
        """
        
        print("[RemediationAgent] Đang tiến hành phân tích lỗi và vá code...")
        result = self._call_llm(prompt, is_json=False)
        return {"draft_code_ptr": result if result else "# Fallback: LLM failed to remediate code"}

    def _logic_handler(self, **kwargs):
        return {"draft_code_ptr": "# Fallback logic for Remediation Agent"}

def remediation_node(state: FactoryState):
    print("--- [Remediation Agent] Kích hoạt ---")
    agent = RemediationAgent()
    res = agent.execute(
        test_results_ptr=state.get("test_results_ptr", ""),
        qa_report_ptr=state.get("qa_report_ptr", ""),
        code_context=state.get("code_context", "")
    )
    
    draft_code = res.get("draft_code_ptr", "")
    state["draft_code_ptr"] = draft_code
    
    print("\n[REMEDIATION OUTPUT]")
    print(draft_code[:300] + "...\n[TRUNCATED]")
    print("[/REMEDIATION OUTPUT]\n")
    
    # Tăng biến đếm vòng lặp để chặn mạch
    state["revision_count"] = state.get("revision_count", 0) + 1
    print(f"[RemediationAgent] Vòng lặp thứ: {state['revision_count']}")
    
    return state
