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

logger = logging.getLogger("ArchRoundtable")

# State cho phòng họp
class ArchMeetingState(TypedDict):
    project_context: str
    architect_proposal: str
    qa_critique: str
    debate_history: Annotated[List[str], operator.add]
    ceo_decision: str
    round: int
    max_rounds: int

class ArchitectureRoundtable:
    def __init__(self):
        # Architect & QA dùng model Flash cho tốc độ
        self.architect_llm = create_fallback_chain(
            model_list=["gemini-3-flash-preview", "gemini-2.5-flash"], 
            temperature=0.7
        )
        self.qa_llm = create_fallback_chain(
            model_list=["gemini-3-flash-preview", "gemini-2.5-flash"], 
            temperature=0.7
        )
        # CEO chốt hạ bằng model tư duy sâu
        self.ceo_llm = create_fallback_chain(
            model_list=["gemini-3.1-pro-preview", "gemini-2.5-pro", "gemini-3-flash-preview"], 
            temperature=0.2
        )
        
        self.graph = self._build_graph()

    def architect_node(self, state: ArchMeetingState) -> dict:
        print(f"\n[Vòng {state['round']}] 📐 THE ARCHITECT đang đề xuất ý tưởng...")
        
        history = "\n".join(state["debate_history"]) if state["debate_history"] else "Chưa có phản biện nào."
        
        # Nếu là vòng đầu tiên, Architect sinh ý tưởng từ context.
        # Các vòng sau sẽ bảo vệ ý tưởng.
        if state['round'] == 1:
            prompt = f"""Bạn là The Principal System Architect. Dưới đây là bối cảnh của dự án LangGraph_Agent_System:
{state['project_context'][:3000]}...

Nhiệm vụ: Dựa vào bối cảnh trên, hãy ĐỀ XUẤT MỘT Ý TƯỞNG SÁNG TẠO ĐỂ NÂNG CẤP DỰ ÁN. Ý tưởng phải táo bạo nhưng khả thi. Trình bày ngắn gọn trong 150 chữ."""
        else:
            prompt = f"""Bạn là The Principal System Architect.
Đề xuất của bạn: {state['architect_proposal']}
Kẻ phản biện (QA) vừa nói: {state['debate_history'][-1]}

Nhiệm vụ: Hãy phản biện lại QA một cách tự tin, bảo vệ ý tưởng của mình, hoặc đưa ra giải pháp khắc phục điểm yếu mà QA nêu ra. Đừng dùng quá 150 chữ."""
        
        try:
            response = self.architect_llm.invoke(prompt)
            proposal = response.content
            if state['round'] == 1:
                return {"architect_proposal": proposal, "debate_history": [f"ARCHITECT: {proposal}"]}
            else:
                return {"debate_history": [f"ARCHITECT: {proposal}"]}
        except Exception as e:
            return {"debate_history": [f"ARCHITECT: Lỗi kết nối API ({e})"]}

    def qa_node(self, state: ArchMeetingState) -> dict:
        print(f"\n[Vòng {state['round']}] 🕵️ THE QA AUDITOR đang soi mói...")
        
        prompt = f"""Bạn là The QA & Security Auditor. Bạn cực kỳ khó tính và ghét những ý tưởng vẽ vời tốn kém.
Đề xuất của Architect: {state['architect_proposal']}
Lịch sử tranh luận:
{chr(10).join(state['debate_history'])}

Nhiệm vụ: Hãy bới móc lỗi, rủi ro (chi phí API cao, nợ kỹ thuật, bug tiềm ẩn) trong ý tưởng của Architect. Phản biện gắt gao. Giới hạn 150 chữ."""
        
        try:
            response = self.qa_llm.invoke(prompt)
            return {"qa_critique": response.content, "debate_history": [f"QA: {response.content}"], "round": state["round"] + 1}
        except Exception as e:
            return {"debate_history": [f"QA: Lỗi kết nối API ({e})"], "round": state["round"] + 1}

    def ceo_node(self, state: ArchMeetingState) -> dict:
        print("\n==================================================")
        print("👔 THE CEO ĐANG ĐƯA RA QUYẾT ĐỊNH (APPROVE / REJECT)...")
        print("==================================================")
        
        full_debate = "\n\n".join(state["debate_history"])
        
        prompt = f"""Bạn là The CEO của LangGraph_Agent_System.
Đây là biên bản cuộc tranh luận về ý tưởng phát triển mới giữa The Architect và The QA:
{full_debate}

Nhiệm vụ: 
1. Tóm tắt ý tưởng.
2. Đánh giá ưu/nhược điểm.
3. Ra quyết định CUỐI CÙNG (APPROVE - Chấp thuận, REJECT - Từ chối, hoặc REVISE - Yêu cầu sửa đổi). Cần ưu tiên sự ổn định của hệ thống nhưng không vùi dập sáng tạo.

TRẢ VỀ ĐỊNH DẠNG JSON SAU (không markdown, không chữ dư):
{{
    "decision": "APPROVE / REJECT / REVISE",
    "summary": "Tóm tắt phán quyết của bạn (dưới 100 chữ)"
}}
"""
        try:
            response = self.ceo_llm.invoke(prompt)
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content and "}" in content:
                content = content[content.find("{"):content.rfind("}")+1]
            decision = json.loads(content)
            return {"ceo_decision": json.dumps(decision, ensure_ascii=False, indent=2)}
        except Exception as e:
            return {"ceo_decision": f"Lỗi CEO: {e}"}

    def should_continue(self, state: ArchMeetingState) -> str:
        if state["round"] >= state["max_rounds"]:
            return "ceo"
        return "architect"

    def _build_graph(self):
        workflow = StateGraph(ArchMeetingState)
        
        workflow.add_node("architect", self.architect_node)
        workflow.add_node("qa", self.qa_node)
        workflow.add_node("ceo", self.ceo_node)
        
        workflow.set_entry_point("architect")
        workflow.add_edge("architect", "qa")
        workflow.add_conditional_edges("qa", self.should_continue, {
            "architect": "architect",
            "ceo": "ceo"
        })
        workflow.add_edge("ceo", END)
        
        return workflow.compile()

    def start_meeting(self, context_text: str, rounds: int = 2):
        print("==================================================")
        print("🏛️ ARCHITECTURE ROUNDTABLE DEBATE")
        print("==================================================")
        
        initial_state = {
            "project_context": context_text,
            "architect_proposal": "",
            "qa_critique": "",
            "debate_history": [],
            "ceo_decision": "",
            "round": 1,
            "max_rounds": rounds
        }
        
        result = self.graph.invoke(initial_state)
        
        print("\n" + "="*50)
        print("📜 PHÁN QUYẾT CỦA CEO")
        print("="*50)
        print(result["ceo_decision"])
        
        return json.loads(result["ceo_decision"])

if __name__ == "__main__":
    # Test thử bằng cách đọc 1 đoạn context
    logging.basicConfig(level=logging.ERROR)
    
    context_path = root_dir / "context" / "JARVIS_CHRONICLES.md"
    try:
        with open(context_path, 'r', encoding='utf-8') as f:
            context_text = f.read()
    except Exception as e:
        context_text = "Dự án hiện tại có nhiều Agent như Trading, Airdrop, Affiliate Video."
        
    room = ArchitectureRoundtable()
    ceo_res = room.start_meeting(context_text=context_text, rounds=2)
    
    # Self-Reflection cho Architect
    print("\n🧠 [ARCHITECT SELF-REFLECTION]:")
    if ceo_res.get("decision") == "APPROVE":
        print("Tuyệt vời! Ý tưởng đã được duyệt. Cần chuẩn bị kiến trúc chi tiết.")
    else:
        print(f"Bài học xương máu: Ý tưởng bị {ceo_res.get('decision')}. Lý do: {ceo_res.get('summary')}. Lần sau phải chú ý các lỗ hổng mà QA chỉ ra.")