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

logger = logging.getLogger("AutonomousAuditor")

class AuditorState(TypedDict):
    target_files: List[str]
    current_file_idx: int
    current_file_content: str
    coder_proposal: str
    qa_feedback: str
    debate_history: Annotated[List[str], operator.add]
    tech_lead_decision: str
    round: int
    max_rounds: int
    all_decisions: Annotated[List[dict], operator.add]
    master_plan: str

class AutonomousAuditor:
    def __init__(self):
        # Coder và QA dùng Flash cho nhanh
        self.coder_llm = create_fallback_chain(
            model_list=["gemini-3-flash-preview", "gemini-2.5-flash"], temperature=0.7)
        self.qa_llm = create_fallback_chain(
            model_list=["gemini-3-flash-preview", "gemini-2.5-flash"], temperature=0.7)
        # Tech Lead dùng Pro để chốt hạ từng file
        self.techlead_llm = create_fallback_chain(
            model_list=["gemini-3.1-pro-preview", "gemini-2.5-pro"], temperature=0.2)
        # Master Architect dùng Pro Preview để tổng hợp báo cáo cuối cùng
        self.master_llm = create_fallback_chain(
            model_list=["gemini-3.1-pro-preview", "gemini-2.5-pro"], temperature=0.2)
            
        self.graph = self._build_graph()

    def get_file_content(self, file_path: str) -> str:
        try:
            full_path = root_dir / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()[:5000] # Truncate for token limits
        except Exception as e:
            return f"Error reading file: {e}"

    def file_reader_node(self, state: AuditorState) -> dict:
        idx = state["current_file_idx"]
        file_path = state["target_files"][idx]
        print(f"\n==================================================")
        print(f"📖 ĐANG KIỂM DUYỆT FILE: {file_path} ({idx+1}/{len(state['target_files'])})")
        print("==================================================")
        content = self.get_file_content(file_path)
        return {
            "current_file_content": content,
            "coder_proposal": "",
            "qa_feedback": "",
            "debate_history": [],
            "tech_lead_decision": "",
            "round": 1
        }

    def coder_node(self, state: AuditorState) -> dict:
        file_path = state["target_files"][state["current_file_idx"]]
        print(f"[Vòng {state['round']}] 👨‍💻 THE CODER đang phân tích code...")
        
        if state['round'] == 1:
            prompt = f"""Bạn là The Coder (Lập trình viên xuất sắc).
Dưới đây là mã nguồn của file '{file_path}':
```python
{state['current_file_content']}
```

Nhiệm vụ: Đọc đoạn code trên, tìm điểm yếu và ĐỀ XUẤT 1 CÁCH REFACTOR ĐỂ NÂNG CẤP. Trình bày ngắn gọn trong 150 chữ."""
        else:
            prompt = f"""Bạn là The Coder.
Đề xuất nâng cấp của bạn: {state['coder_proposal']}
QA vừa bới móc: {state['debate_history'][-1]}

Nhiệm vụ: Phản biện lại QA và bảo vệ ý tưởng của mình. Dùng không quá 150 chữ."""
            
        try:
            response = self.coder_llm.invoke(prompt)
            if state['round'] == 1:
                return {"coder_proposal": response.content, "debate_history": [f"CODER: {response.content}"]}
            else:
                return {"debate_history": [f"CODER: {response.content}"]}
        except Exception as e:
            return {"debate_history": [f"CODER: Lỗi API ({e})"]}

    def qa_node(self, state: AuditorState) -> dict:
        file_path = state["target_files"][state["current_file_idx"]]
        print(f"[Vòng {state['round']}] 🕵️ THE QA đang review và bới móc...")
        
        prompt = f"""Bạn là The QA/Reviewer. Bạn nổi tiếng với việc bắt lỗi cực kỳ gắt gao.
Mã nguồn gốc: {file_path}
Đề xuất của Coder: {state['coder_proposal']}

Lịch sử tranh luận:
{chr(10).join(state['debate_history'])}

Nhiệm vụ: Bới móc lỗi trong đề xuất của Coder. Phản biện gắt gao. Giới hạn 150 chữ."""
        
        try:
            response = self.qa_llm.invoke(prompt)
            return {"qa_feedback": response.content, "debate_history": [f"QA: {response.content}"], "round": state["round"] + 1}
        except Exception as e:
            return {"debate_history": [f"QA: Lỗi API ({e})"], "round": state["round"] + 1}

    def techlead_node(self, state: AuditorState) -> dict:
        file_path = state["target_files"][state["current_file_idx"]]
        print("👔 THE TECH LEAD ĐANG ĐƯA RA PHÁN QUYẾT...")
        
        full_debate = "\n\n".join(state["debate_history"])
        
        prompt = f"""Bạn là The Tech Lead.
Cuộc cãi vã về file '{file_path}':
{full_debate}

Nhiệm vụ:
Đánh giá và chốt hạ: MERGE hay REJECT.
XUẤT RA JSON:
{{
    "file": "{file_path}",
    "decision": "MERGE / REJECT",
    "lesson_learned": "Bài học kỹ thuật..."
}}"""
        try:
            response = self.techlead_llm.invoke(prompt)
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content and "}" in content:
                content = content[content.find("{"):content.rfind("}")+1]
            decision = json.loads(content)
            return {
                "tech_lead_decision": content,
                "all_decisions": [decision],
                "current_file_idx": state["current_file_idx"] + 1
            }
        except Exception as e:
            return {
                "all_decisions": [{"file": file_path, "decision": "ERROR", "lesson_learned": f"Lỗi: {e}"}],
                "current_file_idx": state["current_file_idx"] + 1
            }

    def master_architect_node(self, state: AuditorState) -> dict:
        print("\n==================================================")
        print("🏛️ THE MASTER ARCHITECT ĐANG VIẾT BÁO CÁO TỔNG HỢP...")
        print("==================================================")
        
        decisions_str = json.dumps(state["all_decisions"], indent=2, ensure_ascii=False)
        prompt = f"""Bạn là The Master Architect của LangGraph_Agent_System.
Dưới đây là kết quả kiểm duyệt tự động (Batch Review) của hàng loạt file trong hệ thống:
{decisions_str}

Nhiệm vụ:
Dựa trên tất cả các "bài học kỹ thuật" (lesson_learned) trên, hãy viết một Bản báo cáo tái cấu trúc (MASTER REFACTOR PLAN).
1. Phân tích các lỗ hổng kiến trúc chung mà nhiều file cùng mắc phải.
2. Đề xuất quy chuẩn code (Coding Convention) mới cho công ty.
3. Kế hoạch hành động cụ thể.

Trả về Markdown chuyên nghiệp."""
        try:
            response = self.master_llm.invoke(prompt)
            return {"master_plan": response.content}
        except Exception as e:
            return {"master_plan": f"Lỗi sinh báo cáo: {e}"}

    def should_continue_debate(self, state: AuditorState) -> str:
        if state["round"] >= state["max_rounds"]:
            return "techlead"
        return "coder"

    def has_more_files(self, state: AuditorState) -> str:
        if state["current_file_idx"] < len(state["target_files"]):
            return "read_file"
        return "master_architect"

    def _build_graph(self):
        workflow = StateGraph(AuditorState)
        
        workflow.add_node("read_file", self.file_reader_node)
        workflow.add_node("coder", self.coder_node)
        workflow.add_node("qa", self.qa_node)
        workflow.add_node("techlead", self.techlead_node)
        workflow.add_node("master_architect", self.master_architect_node)
        
        workflow.set_entry_point("read_file")
        workflow.add_edge("read_file", "coder")
        workflow.add_edge("coder", "qa")
        workflow.add_conditional_edges("qa", self.should_continue_debate, {
            "coder": "coder",
            "techlead": "techlead"
        })
        workflow.add_conditional_edges("techlead", self.has_more_files, {
            "read_file": "read_file",
            "master_architect": "master_architect"
        })
        workflow.add_edge("master_architect", END)
        
        return workflow.compile()

    def run_audit(self, directory: str, limit: int = 3, rounds: int = 1):
        print("==================================================")
        print(f"🚀 THE AUTONOMOUS AUDITOR: STARTING BATCH REVIEW")
        print(f"Thư mục mục tiêu: {directory}")
        print("==================================================")
        
        target_path = root_dir / directory
        if not target_path.exists():
            print(f"❌ Không tìm thấy thư mục {target_path}")
            return
            
        files = []
        for f in target_path.rglob("*.py"):
            if not f.name.startswith("__"):
                files.append(str(f.relative_to(root_dir)).replace("\\", "/"))
                
        # Giới hạn số lượng file để không cháy API
        files = files[:limit]
        
        if not files:
            print("❌ Không có file python nào để review.")
            return
            
        print(f"📌 Đã tìm thấy {len(files)} files. Đang chuyển cho hội đồng...")
        
        initial_state = {
            "target_files": files,
            "current_file_idx": 0,
            "current_file_content": "",
            "coder_proposal": "",
            "qa_feedback": "",
            "debate_history": [],
            "tech_lead_decision": "",
            "round": 1,
            "max_rounds": rounds,
            "all_decisions": [],
            "master_plan": ""
        }
        
        result = self.graph.invoke(initial_state)
        
        print("\n" + "="*50)
        print("📜 MASTER REFACTOR PLAN (BẢN KẾ HOẠCH TÁI CẤU TRÚC)")
        print("="*50)
        print(result["master_plan"])
        
        plan_path = root_dir / "logs" / "MASTER_REFACTOR_PLAN.md"
        with open(plan_path, "w", encoding="utf-8") as f:
            f.write(result["master_plan"])
            
        print(f"\n💾 Đã lưu Kế hoạch vào {plan_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    auditor = AutonomousAuditor()
    # Quét thử 3 file trong thư mục factory/nodes
    auditor.run_audit("src/factory/nodes", limit=3, rounds=1)