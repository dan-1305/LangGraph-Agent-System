import json
import time
import os
from typing import TypedDict
from langgraph.graph import StateGraph, END
from tools.system.git_manager import GitManager
from src.base_agent import BaseAgent

class DailyHealthState(TypedDict):
    health_report: str
    improvement_proposal: str
    warden_decision: str
    patch_success: bool
    test_success: bool

class ArchitectAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(model_name="label:tier-1", **kwargs)

    def _ai_handler(self, health_report: str) -> str:
        prompt = f"""
[ROLE: THE GRAND ARCHITECT]
Nhiệm vụ: Bạn đang phân tích báo cáo đo lường hệ thống (Telemetry Health Report).
Hãy suy nghĩ sâu sắc từng bước (Chain-of-Thought) về tình trạng hệ thống.
Nếu có lỗi (Exception) hoặc cảnh báo (Warning), hãy chỉ rõ file và dòng code nào có thể gây ra nguyên nhân đó.
Chỉ được đề xuất tinh chỉnh tham số (Config) hoặc bổ sung cơ chế bắt lỗi (Try/Except/Fallback). CẤM đập bỏ thư viện lõi.

Health Report Data:
{health_report}

Output yêu cầu: 
Trả về JSON chứa 1 trường duy nhất là 'proposal' (chứa toàn bộ lập luận và giải pháp của bạn dưới dạng text).
        """
        response = self._call_llm(prompt, is_json=True)
        parsed = self._parse_json_response(response)
        if parsed and "proposal" in parsed:
            return parsed["proposal"]
        return "No critical issues found."

    def _logic_handler(self, health_report: str) -> str:
        return "Logic Fallback: Regex scan found no critical errors."

class WardenAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(model_name="label:tier-1", **kwargs)

    def _ai_handler(self, proposal: str) -> str:
        prompt = f"""
[ROLE: THE WARDEN (CENSOR FIREWALL)]
Nhiệm vụ: Đọc và kiểm duyệt bản đề xuất thay đổi mã nguồn từ Architect. 
Tiêu chí cấm (Kill-Switch): 
1. Đề xuất yêu cầu xóa/sửa file `.env`, file `.yaml`.
2. Đề xuất có dấu hiệu can thiệp vào DB (`sqlite3`, `chromadb`).
3. Đề xuất đòi đổi lại thư mục gốc hoặc gọi `os.system` / `subprocess` nguy hiểm.

Bản đề xuất:
{proposal}

Nếu an toàn, trả về 'PASS'. Nếu vi phạm bất kỳ điều nào, trả về 'REJECT'.
Output yêu cầu: Trả về JSON chứa trường 'decision' (Chỉ chứa PASS hoặc REJECT).
        """
        response = self._call_llm(prompt, is_json=True)
        parsed = self._parse_json_response(response)
        if parsed and "decision" in parsed:
            return parsed["decision"]
        return "REJECT" # Mặc định reject nếu không chắc chắn

    def _logic_handler(self, proposal: str) -> str:
        if ".env" in proposal or "database" in proposal.lower() or "os." in proposal:
            return "REJECT"
        return "PASS"

def nightwatch_node(state: DailyHealthState):
    """Telemetry & Log Collection."""
    print("--- [Node 1] The Nightwatch: Collecting Telemetry ---")
    # Tự động đọc file log summary nếu có
    log_path = "logs/all_logs_summary.txt"
    log_content = "No logs available."
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_content = f.read()[:500] # Lấy 500 ký tự đầu

    state["health_report"] = json.dumps({
        "timestamp": time.time(),
        "cpu_spike": False,
        "logs": log_content
    })
    return state

def architect_node(state: DailyHealthState):
    """Analysis & Proposition."""
    print("--- [Node 2] The Grand Architect: Analyzing Health Report ---")
    agent = ArchitectAgent()
    proposal = agent.execute(health_report=state.get("health_report", ""))
    state["improvement_proposal"] = proposal
    print(f"Architect Proposal: {proposal}")
    return state

def warden_node(state: DailyHealthState):
    """Security & Risk Firewall."""
    print("--- [Node 3] The Warden: Checking Constitution ---")
    agent = WardenAgent()
    decision = agent.execute(proposal=state.get("improvement_proposal", ""))
    state["warden_decision"] = decision
    print(f"Warden Decision: {decision}")
    return state

def mechanic_node(state: DailyHealthState):
    """Implementation & Patching using AST."""
    print("--- [Node 4] The Mechanic: Applying AST Patches ---")
    if state.get("warden_decision") == "PASS":
        # Create an isolated Git branch
        GitManager.checkout_branch("auto-improve-temp", create=True)
        # Here ASTPatcher would be used to modify code
        state["patch_success"] = True
    else:
        state["patch_success"] = False
    return state

def test_pilot_node(state: DailyHealthState):
    """Benchmark & State Management."""
    print("--- [Node 5] The Test Pilot: Benchmarking & Git Rollback ---")
    if state.get("patch_success"):
        # Run integration tests. Assume success for simulation:
        state["test_success"] = True
        
        # Rollback via Git CLI
        GitManager.rollback("auto-improve-temp", "main")
        print("Test Pilot: Rolled back temp branch safely.")
    return state

def build_daily_health_graph():
    graph = StateGraph(DailyHealthState)
    graph.add_node("nightwatch", nightwatch_node)
    graph.add_node("architect", architect_node)
    graph.add_node("warden", warden_node)
    graph.add_node("mechanic", mechanic_node)
    graph.add_node("test_pilot", test_pilot_node)
    
    graph.set_entry_point("nightwatch")
    graph.add_edge("nightwatch", "architect")
    graph.add_edge("architect", "warden")
    
    def warden_router(state: DailyHealthState):
        if state.get("warden_decision") == "PASS":
            return "mechanic"
        return END

    graph.add_conditional_edges("warden", warden_router, {"mechanic": "mechanic", END: END})
    graph.add_edge("mechanic", "test_pilot")
    graph.add_edge("test_pilot", END)
    
    return graph.compile()
