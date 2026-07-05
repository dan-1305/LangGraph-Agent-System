import os
import json
from pathlib import Path
from src.base_agent import BaseAgent

class ArchitectureCritic(BaseAgent):
    """
    Agent Architecture Critic:
    - Phân tích và đánh giá độ hoàn thiện của code Core.
    - So sánh tính hữu ích của các hàm hiện có với nhu cầu thực tế.
    - Đề xuất lộ trình nâng cấp (Upgrade Plan).
    """
    def __init__(self):
        super().__init__(
            name="ArchCritic",
            role="Thanh tra Độc lập về Kiến trúc",
            agent_label="tier-1", # Cần trí tuệ cao hơn để đánh giá
            temperature=0.2
        )
        self.root_dir = Path(__file__).resolve().parent.parent.parent.parent

    def _ai_handler(self, **kwargs):
        # Trích xuất dữ liệu context do ContextManager đẩy vào (code_context)
        code_context = kwargs.get("code_context", "")
        
        prompt = f"""Bạn là một Senior Software Architect chuyên về LangGraph và Enterprise Monorepo.
Nhiệm vụ của bạn là đọc và phân tích cấu trúc mã nguồn dự án dựa trên JIT Context dưới đây:

{code_context}

Yêu cầu phân tích (Dưới góc độ Kiến trúc):
1. Dự án này tổ chức theo mô hình nào? (Ví dụ: MVC, Clean Architecture, Agentic...).
2. Có vi phạm nguyên lý SOLID hay PEP-8 rõ rệt nào trong đoạn code được cung cấp không?
3. Luồng dữ liệu chính của dự án chạy qua các thành phần nào?

Đầu ra: Trả về một bài Đánh giá Kiến trúc (Markdown) không quá 200 từ.
"""
        print("[ArchCritic] Đang dùng AI phân tích kiến trúc dự án...")
        result = self._call_llm(prompt)
        return {"architecture_review": result if result else "LLM failed to generate evaluation."}

    def _logic_handler(self, **kwargs):
        return {"architecture_review": "Fallback: Kiến trúc không xác định do lỗi LLM."}


def architecture_critic_node(state: dict):
    print("--- [Architecture Critic] Kích hoạt ---")
    agent = ArchitectureCritic()
    res = agent.execute(code_context=state.get("code_context", ""))
    
    # Lưu nhận xét kiến trúc vào biến state để truyền tiếp cho QA Agent
    state["critique_ptr"] = res.get("architecture_review", "")
    print("[ArchCritic] Phân tích hoàn tất. Chuyển giao QA Agent.")
    return state
