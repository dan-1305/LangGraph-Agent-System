import sys
import io
import json
import logging
from pathlib import Path
from typing import TypedDict, List, Annotated
import operator

# Force UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

# Path setup for root
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from langgraph.graph import StateGraph, END
from src.factory.config import create_fallback_chain

logger = logging.getLogger("CodeReview")

class ReviewState(TypedDict):
    target_file: str
    file_content: str
    coder_proposal: str
    qa_feedback: str
    debate_history: Annotated[List[str], operator.add]
    tech_lead_decision: str
    round: int
    max_rounds: int

class CodeReviewCouncil:
    def __init__(self):
        # Coder và QA dùng Flash cho nhanh
        self.coder_llm = create_fallback_chain(
            model_list=["gemini-3-flash-preview", "gemini-2.5-flash"], temperature=0.7)
        self.qa_llm = create_fallback_chain(
            model_list=["gemini-3-flash-preview", "gemini-2.5-flash"], temperature=0.7)
        # Tech Lead dùng Pro để chốt hạ
        self.techlead_llm = create_fallback_chain(
            model_list=["gemini-3.1-pro-preview", "gemini-2.5-pro", "gemini-3-flash-preview"], temperature=0.2)
            
        self.graph = self._build_graph()

    def coder_node(self, state: ReviewState) -> dict:
        print(f"\n[Vòng {state['round']}] 👨‍💻 THE CODER đang phân tích code...")
        
        if state['round'] == 1:
            prompt = f"""Bạn là The Coder (Một lập trình viên xuất sắc).
Dưới đây là mã nguồn của file '{state['target_file']}':
```python
{state['file_content'][:5000]} # Trích xuất 5000 ký tự đầu tiên
```

Nhiệm vụ: Đọc đoạn code trên, tìm điểm yếu hoặc chỗ có thể nâng cấp, và ĐỀ XUẤT 1 TÍNH NĂNG MỚI hoặc 1 CÁCH REFACTOR ĐỂ NÂNG CẤP DỰ ÁN. 
Trình bày ngắn gọn trong 150 chữ."""
        else:
            prompt = f"""Bạn là The Coder.
Đề xuất nâng cấp của bạn: {state['coder_proposal']}
Tên QA (Kiểm thử viên) vừa bới móc: {state['debate_history'][-1]}

Nhiệm vụ: Cãi lại QA! Bảo vệ ý tưởng của bạn hoặc đưa ra cách vá lỗi mà QA vừa nêu. Hãy tự tin. Dùng không quá 150 chữ."""
            
        try:
            response = self.coder_llm.invoke(prompt)
            if state['round'] == 1:
                return {"coder_proposal": response.content, "debate_history": [f"CODER: {response.content}"]}
            else:
                return {"debate_history": [f"CODER: {response.content}"]}
        except Exception as e:
            return {"debate_history": [f"CODER: Lỗi API ({e})"]}

    def qa_node(self, state: ReviewState) -> dict:
        print(f"\n[Vòng {state['round']}] 🕵️ THE QA đang review và bới móc...")
        
        prompt = f"""Bạn là The QA/Reviewer. Bạn nổi tiếng với việc bắt lỗi cực kỳ gắt gao.
Mã nguồn gốc: {state['target_file']}
Đề xuất sửa code của The Coder: {state['coder_proposal']}

Lịch sử tranh luận:
{chr(10).join(state['debate_history'])}

Nhiệm vụ: Bới móc lỗi trong đề xuất của Coder. Hãy tập trung vào: Lỗi bảo mật, Race Condition (đa luồng), rò rỉ bộ nhớ (Memory Leak), hoặc phá vỡ nền móng kiến trúc cũ. Phản biện gắt gao. Giới hạn 150 chữ."""
        
        try:
            response = self.qa_llm.invoke(prompt)
            return {"qa_feedback": response.content, "debate_history": [f"QA: {response.content}"], "round": state["round"] + 1}
        except Exception as e:
            return {"debate_history": [f"QA: Lỗi API ({e})"], "round": state["round"] + 1}

    def techlead_node(self, state: ReviewState) -> dict:
        print("\n==================================================")
        print("👔 THE TECH LEAD ĐANG ĐƯA RA QUYẾT ĐỊNH (MERGE / REJECT)...")
        print("==================================================")
        
        full_debate = "\n\n".join(state["debate_history"])
        
        prompt = f"""Bạn là The Tech Lead (Giám đốc kỹ thuật).
Dưới đây là cuộc cãi vã giữa The Coder và The QA về file '{state['target_file']}':
{full_debate}

Nhiệm vụ:
1. Đánh giá tính khả thi của đề xuất từ Coder.
2. Đánh giá rủi ro từ cảnh báo của QA.
3. Chốt hạ: MERGE (Cho phép viết code) hay REJECT (Từ chối).
4. Rút ra BÀI HỌC (Lesson Learned) để ghi vào sổ tay kiến trúc.

XUẤT RA DUY NHẤT ĐỊNH DẠNG JSON SAU (không markdown):
{{
    "decision": "MERGE / REJECT",
    "review_summary": "Tóm tắt phán quyết...",
    "lesson_learned": "Bài học kỹ thuật rút ra..."
}}"""
        try:
            response = self.techlead_llm.invoke(prompt)
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content and "}" in content:
                content = content[content.find("{"):content.rfind("}")+1]
            return {"tech_lead_decision": content}
        except Exception as e:
            return {"tech_lead_decision": f'{{"decision": "ERROR", "review_summary": "Lỗi API: {e}", "lesson_learned": ""}}'}

    def should_continue(self, state: ReviewState) -> str:
        if state["round"] >= state["max_rounds"]:
            return "techlead"
        return "coder"

    def _build_graph(self):
        workflow = StateGraph(ReviewState)
        
        workflow.add_node("coder", self.coder_node)
        workflow.add_node("qa", self.qa_node)
        workflow.add_node("techlead", self.techlead_node)
        
        workflow.set_entry_point("coder")
        workflow.add_edge("coder", "qa")
        workflow.add_conditional_edges("qa", self.should_continue, {
            "coder": "coder",
            "techlead": "techlead"
        })
        workflow.add_edge("techlead", END)
        
        return workflow.compile()

    def run_review(self, target_file: str, rounds: int = 2):
        print("==================================================")
        print(f"🛠️ CODE REVIEW COUNCIL - Mục tiêu: {target_file}")
        print("==================================================")
        
        file_path = root_dir / target_file
        if not file_path.exists():
            print(f"❌ Không tìm thấy file {file_path}")
            return
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        initial_state = {
            "target_file": target_file,
            "file_content": content,
            "coder_proposal": "",
            "qa_feedback": "",
            "debate_history": [],
            "tech_lead_decision": "",
            "round": 1,
            "max_rounds": rounds
        }
        
        result = self.graph.invoke(initial_state)
        
        decision_data = json.loads(result["tech_lead_decision"])
        
        print("\n" + "="*50)
        print("📜 PHÁN QUYẾT TỪ TECH LEAD")
        print("="*50)
        print(f"Quyết định: {decision_data.get('decision')}")
        print(f"Tổng kết: {decision_data.get('review_summary')}")
        print(f"🧠 BÀI HỌC KỸ THUẬT: {decision_data.get('lesson_learned')}")
        
        # Ghi bài học ra file directives
        logs_dir = root_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        directive_path = logs_dir / "TECH_DIRECTIVES.md"
        with open(directive_path, "a", encoding="utf-8") as f:
            f.write(f"\n### Review File: {target_file}\n")
            f.write(f"- **Decision:** {decision_data.get('decision')}\n")
            f.write(f"- **Lesson:** {decision_data.get('lesson_learned')}\n")
        
        print(f"\n💾 Đã lưu bài học vào {directive_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    council = CodeReviewCouncil()
    # Test với file main_scheduler.py
    council.run_review("scheduler/main_scheduler.py", rounds=2)