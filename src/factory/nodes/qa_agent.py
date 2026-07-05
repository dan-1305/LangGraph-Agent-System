import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from pydantic import BaseModel, Field
from src.base_agent import BaseAgent
from src.factory.state import FactoryState

class QAOutput(BaseAgent, BaseModel):
    answer: str = Field(description="Câu trả lời chi tiết dựa trên bối cảnh được cung cấp.")

class QAAgent(BaseAgent):
    """
    Tác nhân Hỏi-Đáp (QA Agent).
    Nhận câu hỏi từ User và Context (đã được JIT Context Manager bơm vào),
    sau đó trả về câu trả lời mà không gọi thêm tool hay tìm kiếm gì thêm.
    """
    def __init__(self):
        # Dùng Flash LLM vì nhiệm vụ chỉ là đọc text có sẵn và tóm tắt lại
        super().__init__(name="QAAgent", role="Chuyên gia giải đáp RAG", agent_label="tier-2")
        
    def _logic_handler(self, **kwargs):
        return {"answer": "Hệ thống AI đang tạm ngưng kết nối, vui lòng thử lại sau."}
        
    def _ai_handler(self, **kwargs):
        user_prompt = kwargs.get("user_requirement", "")
        code_context = kwargs.get("code_context", "")
        
        # Kết hợp thêm Nhận xét kiến trúc từ Node trước (nếu có)
        arch_critique = kwargs.get("critique_ptr", "")
        
        system_prompt = f"""
        Bạn là Chuyên gia QA / Linter tự động của dự án LangGraph_Agent_System.
        Nhiệm vụ của bạn là rà soát lỗi cú pháp, PEP-8 và xác nhận chất lượng mã nguồn.
        
        [NGUYÊN TẮC SUY LUẬN - CHAIN OF THOUGHT]
        1. Đọc nhận xét từ Architecture Critic (nếu có).
        2. Rà soát [JIT KNOWLEDGE BASE] để tìm các điểm mù (blind spots) hoặc lỗi cú pháp (Syntax error, thiếu Type Hint...).
        3. Chấm điểm chất lượng mã nguồn từ 0-100 (QA Score).
        
        [NHẬN XÉT TỪ ARCHITECTURE CRITIC]:
        {arch_critique}
        
        [JIT KNOWLEDGE BASE]:
        {code_context}
        """
        
        # Test sử dụng LLM mặc định (Có thể swap sang Local Model từ Config)
        res = self._call_llm(system_prompt + f"\n\nYêu cầu user: {user_prompt}", is_json=False)
        return {"answer": res}

def qa_node(state: FactoryState):
    print("--- [QA Agent] Kích hoạt ---")
    agent = QAAgent()
    res = agent.execute(
        user_requirement=state.get("user_requirement", ""),
        code_context=state.get("code_context", ""),
        critique_ptr=state.get("critique_ptr", "")
    )
    answer = res.get("answer", "")
    
    print("\n[QA REPORT]")
    print(answer)
    print("[/QA REPORT]\n")
    
    state["qa_report_ptr"] = answer
    return state
