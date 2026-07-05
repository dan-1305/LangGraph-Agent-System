import sys
import io
import json
import logging
import os
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

# Tool 1: list_projects
def list_projects() -> str:
    """Liệt kê tất cả các project con hiện có."""
    projects_dir = root_dir / "projects"
    if not projects_dir.exists():
        return "Không tìm thấy thư mục projects"
    
    projects = [d.name for d in projects_dir.iterdir() if d.is_dir() and not d.name.startswith('_')]
    return f"Các dự án hiện có: {', '.join(projects)}"

# Tool 2: read_document
def read_document(rel_path: str) -> str:
    """Đọc nội dung một file tài liệu hoặc code (truyền đường dẫn tương đối từ root)."""
    file_path = root_dir / rel_path
    if not file_path.exists():
        return f"File {rel_path} không tồn tại."
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Giới hạn nội dung trả về để không tràn Token (tối đa 15000 ký tự)
            if len(content) > 15000:
                return content[:15000] + "\n...[CONTENT TRUNCATED]..."
            return content
    except Exception as e:
        return f"Lỗi đọc file: {e}"

# Đóng gói tools
tools = {
    "list_projects": list_projects,
    "read_document": read_document
}

logger = logging.getLogger("AutonomousCEO")

class CEOState(TypedDict):
    current_thought: str
    tool_to_call: str
    tool_args: str
    tool_result: str
    journal: Annotated[List[str], operator.add]
    final_plan: str
    step_count: int
    max_steps: int

class AutonomousCEO:
    def __init__(self):
        # Dùng model xịn nhất cho CEO tự trị
        self.llm = create_fallback_chain(
            model_list=["gemini-3.1-pro-preview", "gemini-2.5-pro"], temperature=0.7)
        self.graph = self._build_graph()

    def think_node(self, state: CEOState) -> dict:
        print(f"\n[Bước {state['step_count']}] 🧠 THE CEO ĐANG SUY NGHĨ...")
        
        journal_str = "\n".join(state["journal"]) if state["journal"] else "Vừa thức dậy. Chưa có manh mối nào."
        
        prompt = f"""Bạn là TỔNG GIÁM ĐỐC TỰ TRỊ (Autonomous CEO) của LangGraph Agent System.
Nhiệm vụ của bạn là đi dạo quanh hệ thống, tìm hiểu xem công ty đang làm những dự án gì, lịch sử nợ kỹ thuật ra sao, và vạch ra Kế hoạch Chiến lược tiếp theo.

[NHẬT KÝ VI HÀNH CỦA BẠN]
{journal_str}

[KẾT QUẢ TỪ HÀNH ĐỘNG GẦN NHẤT]
{state.get('tool_result', 'Chưa có')}

Hành động (Tool) khả dụng:
1. "list_projects": Khám phá các dự án con. Không cần tham số.
2. "read_document": Đọc nội dung file. Yêu cầu tham số "path" (ví dụ: "context/JARVIS_CHRONICLES.md" hoặc "scheduler/main_scheduler.py").
3. "finish": Kết thúc vi hành và lập Bản Kế Hoạch. Không cần tham số.

Bạn đang ở bước {state['step_count']} trên tối đa {state['max_steps']}. Nếu gần hết bước, hãy gọi "finish".

XUẤT RA JSON:
{{
    "thought": "Bạn đang nghĩ gì? Bạn muốn tìm hiểu gì tiếp theo?",
    "tool": "tên tool (list_projects / read_document / finish)",
    "tool_args": "tham số cho tool (chỉ dùng cho read_document, ví dụ: 'context/ROADMAP.md')"
}}"""
        try:
            response = self.llm.invoke(prompt)
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content and "}" in content:
                content = content[content.find("{"):content.rfind("}")+1]
            data = json.loads(content)
            
            return {
                "current_thought": data.get("thought", ""),
                "tool_to_call": data.get("tool", "finish"),
                "tool_args": data.get("tool_args", ""),
                "journal": [f"Suy nghĩ: {data.get('thought')} | Gọi Tool: {data.get('tool')}"]
            }
        except Exception as e:
            print(f"Lỗi suy nghĩ: {e}")
            return {"tool_to_call": "finish"}

    def act_node(self, state: CEOState) -> dict:
        tool_name = state["tool_to_call"]
        print(f"\n🛠️ [CEO ACTION] Đang thực thi: {tool_name}('{state.get('tool_args')}')")
        
        if tool_name == "list_projects":
            res = list_projects()
        elif tool_name == "read_document":
            res = read_document(state["tool_args"])
        else:
            res = "Tool không hợp lệ."
            
        return {
            "tool_result": res,
            "step_count": state["step_count"] + 1,
            "journal": [f"Kết quả Tool: Đã nhận được dữ liệu (Độ dài: {len(res)} ký tự)"]
        }

    def finish_node(self, state: CEOState) -> dict:
        print("\n==================================================")
        print("👔 THE CEO ĐANG VIẾT KẾ HOẠCH CHIẾN LƯỢC (FINAL PLAN)...")
        print("==================================================")
        
        journal_str = "\n".join(state["journal"])
        
        prompt = f"""Bạn là TỔNG GIÁM ĐỐC TỰ TRỊ của hệ thống.
Dưới đây là hành trình vi hành của bạn:
{journal_str}

Dựa trên những gì bạn đã đọc và thu thập được từ các dự án và tài liệu, hãy vạch ra MỘT KẾ HOẠCH CHIẾN LƯỢC (Strategic Plan) cho giai đoạn tiếp theo.
Yêu cầu:
1. Đánh giá sơ bộ về tình trạng hệ thống.
2. Chỉ ra 1 lỗ hổng lớn hoặc 1 cơ hội lớn.
3. Ra quyết định hành động cụ thể cho đám lính (VD: Tạo project mới, đập bỏ project cũ, hay audit mã nguồn).

Trả về định dạng Markdown chuyên nghiệp."""

        try:
            response = self.llm.invoke(prompt)
            return {"final_plan": response.content}
        except Exception as e:
            return {"final_plan": f"Lỗi lập kế hoạch: {e}"}

    def should_continue(self, state: CEOState) -> str:
        if state["tool_to_call"] == "finish" or state["step_count"] >= state["max_steps"]:
            return "finish"
        return "act"

    def _build_graph(self):
        workflow = StateGraph(CEOState)
        
        workflow.add_node("think", self.think_node)
        workflow.add_node("act", self.act_node)
        workflow.add_node("finish", self.finish_node)
        
        workflow.set_entry_point("think")
        workflow.add_conditional_edges("think", self.should_continue, {
            "act": "act",
            "finish": "finish"
        })
        workflow.add_edge("act", "think")
        workflow.add_edge("finish", END)
        
        return workflow.compile()

    def run_vi_hanh(self, steps=4):
        print("==================================================")
        print("👑 AUTONOMOUS CEO: KHỞI ĐỘNG HÀNH TRÌNH VI HÀNH 👑")
        print("==================================================")
        
        initial_state = {
            "current_thought": "",
            "tool_to_call": "",
            "tool_args": "",
            "tool_result": "",
            "journal": [],
            "final_plan": "",
            "step_count": 1,
            "max_steps": steps
        }
        
        result = self.graph.invoke(initial_state)
        
        print("\n" + "="*50)
        print("📜 CEO'S STRATEGIC DIRECTIVES (BẢN KẾ HOẠCH CHIẾN LƯỢC)")
        print("="*50)
        print(result["final_plan"])
        
        plan_path = root_dir / "logs" / "CEO_STRATEGIC_PLAN.md"
        with open(plan_path, "w", encoding="utf-8") as f:
            f.write(result["final_plan"])
            
        print(f"\n💾 Đã lưu Kế hoạch vào {plan_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    ceo = AutonomousCEO()
    ceo.run_vi_hanh(steps=4)
