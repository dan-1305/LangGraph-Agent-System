import sys
import os
from pathlib import Path
from typing import Dict, Any

root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.base_agent import BaseAgent
from src.factory.state import FactoryState
from pydantic import BaseModel, Field
from tools.system.workflow_engine import WorkflowEngine, CHAIN_PRESETS

class WorkflowDecision(BaseModel):
    action: str = Field(description="Hành động cần làm: 'run_chain', 'run_cycle', hoặc 'skip'")
    target_id: str = Field(description="ID của cycle hoặc chain cần chạy (ví dụ: 'safe_commit', 'self_review', 'deep_audit')")
    reasoning: str = Field(description="Lý do ngắn gọn tại sao chọn chạy workflow này")

class AIWorkflowAgent(BaseAgent):
    """
    AI Workflow Agent: Tự động quyết định gọi cycle/chain nào từ Workflow Engine
    """
    def __init__(self):
        super().__init__(name="WorkflowAgent", role="Orchestrator", model_name="gemini-3.1-flash-lite", temperature=0.1)
        self.engine = WorkflowEngine()
        
    def decide_workflow(self, state: FactoryState) -> Dict[str, Any]:
        req = state.get("user_requirement", "")
        if not req:
            return {"action": "skip", "target_id": "", "reasoning": "Không có yêu cầu cụ thể"}
            
        cycles = self.engine.db.list_cycles()
        cycle_list = "\n".join([f"- {c['cycle_id']} ({c['category']}): {c['cycle_name']}" for c in cycles])
        
        chains = []
        for chain_id, cycle_ids in CHAIN_PRESETS.items():
            chains.append(f"- {chain_id}: {' -> '.join(cycle_ids)}")
        chain_list = "\n".join(chains)
        
        prompt = f"""
        Nhiệm vụ: Dựa trên yêu cầu của người dùng, hãy quyết định xem có cần kích hoạt một Workflow Cycle hoặc Chain nào từ hệ thống Workflow Engine không.
        
        Các Cycles có sẵn:
        {cycle_list}
        
        Các Chains có sẵn:
        {chain_list}
        
        Yêu cầu của người dùng:
        "{req}"
        
        Nếu yêu cầu liên quan đến kiểm tra code, review, đánh giá dự án, security, hoặc chuẩn bị commit, hãy chọn 'run_chain' hoặc 'run_cycle' phù hợp (VD: 'safe_commit' để review và test, 'deep_audit' để audit toàn diện).
        Nếu yêu cầu không liên quan gì đến các chu trình này, hãy chọn 'skip'.
        """
        
        print("[WorkflowAgent] Đang đánh giá yêu cầu để kích hoạt Workflow Engine...")
        try:
            decision = self._call_llm(prompt, is_json=False, schema=WorkflowDecision)
            if decision and "action" in decision:
                return decision
            else:
                return {"action": "skip", "target_id": "", "reasoning": "Schema error"}
        except Exception as e:
            print(f"[WorkflowAgent] Lỗi khi gọi LLM: {e}")
            return {"action": "skip", "target_id": "", "reasoning": str(e)}

    def _ai_handler(self, *args, **kwargs) -> Any:
        pass

    def _logic_handler(self, *args, **kwargs) -> Any:
        pass


def workflow_agent_node(state: FactoryState):
    print("\n--- [Workflow Agent] Kích hoạt ---")
    agent = AIWorkflowAgent()
    decision = agent.decide_workflow(state)
    
    action = decision.get("action", "skip")
    target_id = decision.get("target_id", "")
    reasoning = decision.get("reasoning", "")
    
    print(f"[WorkflowAgent] Quyết định: {action.upper()} | Target: {target_id}")
    print(f"[WorkflowAgent] Lý do: {reasoning}")
    
    file_path = state.get("file_path", "")
    
    if action == "run_chain" and target_id:
        print(f"[WorkflowAgent] Thực thi Chain: {target_id}")
        res = agent.engine.run_chain(target_id, target_file=file_path)
        
        report = f"✅ Workflow Agent đã chạy Chain: {target_id}\nKết quả: {res.get('status')}\nĐiểm trung bình: {res.get('score')}\n"
        state["response"] = str(state.get("response", "")) + "\n\n" + report
        
    elif action == "run_cycle" and target_id:
        print(f"[WorkflowAgent] Thực thi Cycle: {target_id}")
        res = agent.engine.run_cycle(target_id, target_file=file_path)
        
        report = f"✅ Workflow Agent đã chạy Cycle: {target_id}\nKết quả: {res.get('status')}\nĐiểm: {res.get('score')}\n"
        if res.get("findings"):
            report += "Findings:\n" + "\n".join([f"- {f}" for f in res["findings"][:5]])
        state["response"] = str(state.get("response", "")) + "\n\n" + report
        
    return state
