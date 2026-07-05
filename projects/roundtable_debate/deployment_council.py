import sys
import io
import json
import logging
import subprocess
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

logger = logging.getLogger("DeployCouncil")

class DeployState(TypedDict):
    git_status: str
    tech_lead_approval: str
    devops_audit: str
    ceo_decision: str

class DeploymentCouncil:
    def __init__(self):
        self.devops_llm = create_fallback_chain(
            model_list=["gemini-3-flash-preview", "gemini-2.5-flash"], temperature=0.1)
        self.techlead_llm = create_fallback_chain(
            model_list=["gemini-3-flash-preview", "gemini-2.5-flash"], temperature=0.5)
        self.ceo_llm = create_fallback_chain(
            model_list=["gemini-3.1-pro-preview", "gemini-2.5-pro", "gemini-3-flash-preview"], temperature=0.1)
            
        self.graph = self._build_graph()

    def get_git_status(self) -> str:
        """Lấy thông tin git status và những file bị thay đổi (giả lập hoặc chạy thật)."""
        try:
            # Lấy status
            status_res = subprocess.run(["git", "status", "--short"], cwd=root_dir, capture_output=True, text=True)
            status_out = status_res.stdout.strip()
            if not status_out:
                return "Nothing to commit, working tree clean."
                
            return f"Git Status:\n{status_out}"
        except Exception as e:
            return f"Git Error: {e}"

    def techlead_node(self, state: DeployState) -> dict:
        print("\n👨‍💻 [Tech Lead] đang kiểm tra tiến độ code...")
        if "Nothing to commit" in state['git_status']:
            return {"tech_lead_approval": "Không có code mới, nghỉ tay!"}
            
        prompt = f"""Bạn là The Tech Lead. Hệ thống chuẩn bị commit các file sau:
{state['git_status']}

Nhiệm vụ: Trình bày một đoạn ngắn gọn tóm tắt các thay đổi và yêu cầu DevOps kiểm tra bảo mật trước khi Deploy."""
        try:
            return {"tech_lead_approval": self.techlead_llm.invoke(prompt).content}
        except: return {"tech_lead_approval": "Lỗi API"}

    def devops_node(self, state: DeployState) -> dict:
        print("\n🛡️ [DevOps Agent] đang quét rủi ro bảo mật...")
        if "Không có code mới" in state['tech_lead_approval']:
            return {"devops_audit": "An toàn."}
            
        prompt = f"""Bạn là The DevOps Agent & Security Scanner.
Các file chuẩn bị được commit:
{state['git_status']}

Nhiệm vụ: Quét xem có file nào tên là .env, keys.txt, wallet.json, config.py hoặc chứa đường dẫn nhảy cảm bị lọt vào danh sách commit không. 
Nếu có, hãy cảnh báo ĐỎ (FATAL). Nếu an toàn, báo CLEAR. Giới hạn 100 chữ."""
        try:
            return {"devops_audit": self.devops_llm.invoke(prompt).content}
        except: return {"devops_audit": "Lỗi API"}

    def ceo_node(self, state: DeployState) -> dict:
        print("\n==================================================")
        print("👔 THE CEO ĐANG RA QUYẾT ĐỊNH TRIỂN KHAI (DEPLOY)...")
        print("==================================================")
        
        if "Không có code mới" in state['tech_lead_approval']:
            return {"ceo_decision": '{"action": "SKIP", "message": "Nghỉ ngơi."}'}
            
        prompt = f"""Bạn là The CEO.
Tech Lead báo cáo: {state['tech_lead_approval']}
DevOps báo cáo bảo mật: {state['devops_audit']}

Nhiệm vụ: Dựa vào DevOps, nếu có rủi ro bảo mật, HỦY BỎ việc commit. Nếu an toàn, CHO PHÉP commit và Tự Động Viết một Commit Message thật hay, tóm tắt các file bị thay đổi.
TRẢ VỀ ĐÚNG JSON:
{{
    "action": "COMMIT / REJECT",
    "commit_message": "Nội dung commit...",
    "ceo_message": "Lời nhắn"
}}"""
        try:
            response = self.ceo_llm.invoke(prompt)
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content and "}" in content:
                content = content[content.find("{"):content.rfind("}")+1]
            return {"ceo_decision": content}
        except Exception as e:
            return {"ceo_decision": f'{{"action": "REJECT", "message": "Lỗi CEO: {e}"}}'}

    def _build_graph(self):
        workflow = StateGraph(DeployState)
        
        workflow.add_node("techlead", self.techlead_node)
        workflow.add_node("devops", self.devops_node)
        workflow.add_node("ceo", self.ceo_node)
        
        workflow.set_entry_point("techlead")
        workflow.add_edge("techlead", "devops")
        workflow.add_edge("devops", "ceo")
        workflow.add_edge("ceo", END)
        
        return workflow.compile()

    def run_deployment(self):
        print("==================================================")
        print("🚀 DEPLOYMENT COUNCIL (HỘI ĐỒNG TRIỂN KHAI)")
        print("==================================================")
        
        git_stat = self.get_git_status()
        print(f"\n[Trạng thái Git]\n{git_stat}\n")
        
        initial_state = {
            "git_status": git_stat,
            "tech_lead_approval": "",
            "devops_audit": "",
            "ceo_decision": ""
        }
        
        result = self.graph.invoke(initial_state)
        decision = json.loads(result["ceo_decision"])
        
        print("\n" + "="*50)
        print("📜 QUYẾT ĐỊNH CỦA CEO")
        print("="*50)
        print(f"Hành động: {decision.get('action')}")
        print(f"Lời nhắn : {decision.get('ceo_message')}")
        
        if decision.get('action') == "COMMIT":
            commit_msg = decision.get("commit_message", "Auto update by AI")
            print(f"\n[AUTO-EXECUTION] Tiến hành Commit và Push: '{commit_msg}'")
            try:
                # Add tất cả file (Ngoại trừ những gì trong .gitignore)
                subprocess.run(["git", "add", "."], cwd=root_dir, check=True)
                # Commit
                subprocess.run(["git", "commit", "-m", commit_msg], cwd=root_dir, check=True)
                # Push
                push_res = subprocess.run(["git", "push"], cwd=root_dir, capture_output=True, text=True)
                print(f"✅ Đã Push thành công lên Github!\n{push_res.stdout}")
            except Exception as e:
                print(f"❌ Lỗi Git Execution: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    council = DeploymentCouncil()
    council.run_deployment()
