import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from pydantic import BaseModel, Field
from src.base_agent import BaseAgent
from src.factory.state import FactoryState

class QAOutput(BaseModel):
    answer: str = Field(description="Câu trả lời chi tiết dựa trên bối cảnh được cung cấp.")

class QAAgent(BaseAgent):
    """
    Tác nhân Hỏi-Đáp (QA Agent).
    Nhận câu hỏi từ User và Context (đã được JIT Context Manager bơm vào),
    sau đó trả về câu trả lời mà không gọi thêm tool hay tìm kiếm gì thêm.
    """
    def __init__(self):
        # Dùng Flash LLM vì nhiệm vụ chỉ là đọc text có sẵn và tóm tắt lại
        super().__init__(name="QAAgent", role="Chuyên gia giải đáp RAG", model_name="label:tier-2")
        
    def _logic_handler(self, kwargs: dict):
        return {"answer": "Hệ thống AI đang tạm ngưng kết nối, vui lòng thử lại sau."}
        
    def _ai_handler(self, kwargs: dict):
        user_prompt = kwargs.get("user_requirement", "")
        code_context = kwargs.get("code_context", "")
        
        system_prompt = f"""
        Bạn là Chuyên gia giải đáp thắc mắc của dự án LangGraph_Agent_System.
        Hãy trả lời câu hỏi của người dùng một cách NGẮN GỌN, CHUẨN XÁC, DỄ HIỂU.
        Tuyệt đối CHỈ DỰA VÀO các thông tin được cung cấp trong [JIT KNOWLEDGE BASE] dưới đây.
        Nếu trong [JIT KNOWLEDGE BASE] không có thông tin, hãy nói "Tôi không tìm thấy thông tin này trong tài liệu hệ thống".
        KHÔNG ĐƯỢC tự bịa ra thông tin.
        
        {code_context}
        """
        
        res = self.llm.with_structured_output(QAOutput).invoke([
            ("system", system_prompt),
            ("user", user_prompt)
        ])
        
        return {"answer": res.answer}

def qa_node(state: FactoryState):
    print("--- [QA Agent] Kích hoạt ---")
    agent = QAAgent()
    res = agent.execute(
        user_requirement=state.get("user_requirement", ""),
        code_context=state.get("code_context", "")
    )
    answer = res.get("answer", "")
    
    print("\n[AI RESPONSE]")
    print(answer)
    print("[/AI RESPONSE]\n")
    
    state["response"] = answer
    return state