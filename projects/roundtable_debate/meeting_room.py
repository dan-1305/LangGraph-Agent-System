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
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

logger = logging.getLogger("Roundtable")

# State cho phòng họp
class MeetingState(TypedDict):
    topic: str
    trader_proposal: str
    skeptic_critique: str
    debate_history: Annotated[List[str], operator.add]
    ceo_decision: str
    round: int
    max_rounds: int

class AIRoundtable:
    def __init__(self):
        # Trader & Skeptic dùng model Flash thế hệ mới (3.0) cho cãi nhau tốc độ & thông minh
        self.trader_llm = create_fallback_chain(
            model_list=["gemini-3-flash-preview", "gemini-2.5-flash"], 
            temperature=0.7
        )
        self.skeptic_llm = create_fallback_chain(
            model_list=["gemini-3-flash-preview", "gemini-2.5-flash"], 
            temperature=0.7
        )
        # CEO chốt hạ bằng model tư duy sâu (Pro / Pro Preview)
        self.ceo_llm = create_fallback_chain(
            model_list=["gemini-3.1-pro-preview", "gemini-2.5-pro", "gemini-3-flash-preview"], 
            temperature=0.2
        )
        
        self.graph = self._build_graph()

    def trader_node(self, state: MeetingState) -> dict:
        print(f"\n[Vòng {state['round']}] 🐂 THE TRADER đang phân tích...")
        
        history = "\n".join(state["debate_history"]) if state["debate_history"] else "Chưa có."
        
        prompt = f"""Bạn là The Trader (Kẻ Mạo Hiểm), luôn tìm kiếm cơ hội kiếm tiền và rất lạc quan.
Chủ đề cuộc họp hôm nay: {state['topic']}
Lịch sử tranh luận:
{history}

Nhiệm vụ: Dựa vào tình hình trên, hãy đưa ra (hoặc bảo vệ) quan điểm MUA/LONG của bạn. Nếu The Skeptic (Kẻ Hoài Nghi) vừa chỉ trích bạn, hãy phản biện lại hắn một cách tự tin. Đừng dùng quá 100 chữ."""
        
        try:
            response = self.trader_llm.invoke(prompt)
            return {"trader_proposal": response.content, "debate_history": [f"TRADER: {response.content}"]}
        except Exception as e:
            return {"trader_proposal": "Lỗi kết nối API", "debate_history": [f"TRADER: Lỗi kết nối API ({e})"]}

    def skeptic_node(self, state: MeetingState) -> dict:
        print(f"\n[Vòng {state['round']}] 🐻 THE SKEPTIC đang phản biện...")
        
        prompt = f"""Bạn là The Skeptic (Kẻ Hoài Nghi), một chuyên gia QA và quản lý rủi ro cực kỳ khó tính.
Chủ đề cuộc họp hôm nay: {state['topic']}
Quan điểm của The Trader vừa nói: {state['trader_proposal']}

Nhiệm vụ: Bới móc lỗi, chỉ ra các rủi ro, sợ sập sàn, sợ bong bóng. Hãy phản biện gay gắt lại The Trader. Đừng dùng quá 100 chữ."""
        
        try:
            response = self.skeptic_llm.invoke(prompt)
            return {"skeptic_critique": response.content, "debate_history": [f"SKEPTIC: {response.content}"], "round": state["round"] + 1}
        except Exception as e:
            return {"skeptic_critique": "Lỗi", "debate_history": [f"SKEPTIC: Lỗi kết nối API ({e})"], "round": state["round"] + 1}

    def ceo_node(self, state: MeetingState) -> dict:
        print("\n==================================================")
        print("👔 THE CEO ĐANG XEM XÉT VÀ RA QUYẾT ĐỊNH CUỐI CÙNG...")
        print("==================================================")
        
        full_debate = "\n\n".join(state["debate_history"])
        
        prompt = f"""Bạn là The CEO của quỹ LangGraph.
Chủ đề đầu tư: {state['topic']}

Đây là biên bản cuộc cãi vã nảy lửa giữa 2 nhân viên của bạn (The Trader và The Skeptic):
{full_debate}

Nhiệm vụ: Bạn hãy đọc kỹ biên bản, tóm tắt lại ý chính, và đưa ra PHÁN QUYẾT CUỐI CÙNG (Approve/Reject/Hold) với tư duy sâu sắc, bảo toàn vốn nhưng không bỏ lỡ cơ hội.
Trình bày rõ ràng thành 3 phần:
1. Nhận định về Trader.
2. Nhận định về Skeptic.
3. Phán quyết cuối cùng."""

        try:
            response = self.ceo_llm.invoke(prompt)
            return {"ceo_decision": response.content}
        except Exception as e:
            return {"ceo_decision": f"CEO bận đi đánh golf do lỗi API: {e}"}

    def should_continue(self, state: MeetingState) -> str:
        if state["round"] >= state["max_rounds"]:
            return "ceo"
        return "trader"

    def _build_graph(self):
        workflow = StateGraph(MeetingState)
        
        workflow.add_node("trader", self.trader_node)
        workflow.add_node("skeptic", self.skeptic_node)
        workflow.add_node("ceo", self.ceo_node)
        
        workflow.set_entry_point("trader")
        workflow.add_edge("trader", "skeptic")
        workflow.add_conditional_edges("skeptic", self.should_continue, {
            "trader": "trader",
            "ceo": "ceo"
        })
        workflow.add_edge("ceo", END)
        
        return workflow.compile()

    def start_meeting(self, topic: str, rounds: int = 2):
        print("==================================================")
        print("🏛️ AI ROUNDTABLE DEBATE (HỘI ĐỒNG PHẢN BIỆN)")
        print(f"Chủ đề: {topic}")
        print("==================================================")
        
        initial_state = {
            "topic": topic,
            "trader_proposal": "",
            "skeptic_critique": "",
            "debate_history": [],
            "ceo_decision": "",
            "round": 1,
            "max_rounds": rounds
        }
        
        result = self.graph.invoke(initial_state)
        
        print("\n" + "="*50)
        print("📜 BIÊN BẢN CUỘC HỌP (FINAL DECISION)")
        print("="*50)
        print(result["ceo_decision"])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    room = AIRoundtable()
    
    # Chủ đề hóc búa để cãi nhau
    topic = "Có nên All-in (Tất tay) 100% quỹ vào Bitcoin ngay hôm nay vì FED vừa giảm lãi suất 0.5% không?"
    room.start_meeting(topic=topic, rounds=2)
