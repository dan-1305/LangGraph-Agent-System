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

logger = logging.getLogger("GrandCouncil")

# Dữ liệu mô phỏng thu thập từ các hệ thống con
mock_system_data = """
[BÁO CÁO THÁNG 6/2026]
1. AI Trading Agent: PnL tháng này đang lỗ -20% do dính chuỗi Flash Crash của Bitcoin.
2. Airdrop Guerrilla: Đã cày xong 150 ví trên Monad, tiêu tốn 50$ tiền Gas. Chưa có thông tin Airdrop.
3. Auto Affiliate Video: Video Tiktok "Tai nghe Sony" vừa cắn xu hướng đạt 1.5 triệu view, ra được 50 đơn hàng Affiliate, doanh thu ước tính 500$.
4. System Health: Quota API của CatieCLI (Model rẻ) thường xuyên báo 429 Too Many Requests. RAM VPS ổn định.
"""

class CouncilState(TypedDict):
    system_data: str
    trading_report: str
    growth_report: str
    sysadmin_report: str
    ceo_directive: str

class GrandCouncil:
    def __init__(self):
        # Các trưởng phòng dùng model Flash
        self.trading_llm = create_fallback_chain(
            model_list=["gemini-3-flash-preview", "gemini-2.5-flash"], temperature=0.7)
        self.growth_llm = create_fallback_chain(
            model_list=["gemini-3-flash-preview", "gemini-2.5-flash"], temperature=0.7)
        self.admin_llm = create_fallback_chain(
            model_list=["gemini-3-flash-preview", "gemini-2.5-flash"], temperature=0.5)
            
        # CEO dùng model siêu việt
        self.ceo_llm = create_fallback_chain(
            model_list=["gemini-3.1-pro-preview", "gemini-2.5-pro", "gemini-3-flash-preview"], temperature=0.2)
            
        self.graph = self._build_graph()

    def trading_node(self, state: CouncilState) -> dict:
        print("\n📈 [Head of Trading] đang giải trình...")
        prompt = f"""Bạn là Head of Trading. Dữ liệu hệ thống:
{state['system_data']}
Nhiệm vụ: Giải trình lý do thua lỗ (nếu có), đổ lỗi cho thị trường, và xin CEO giữ nguyên ngân sách API cho bạn. Giới hạn 100 chữ."""
        try:
            return {"trading_report": self.trading_llm.invoke(prompt).content}
        except: return {"trading_report": "Lỗi API"}

    def growth_node(self, state: CouncilState) -> dict:
        print("\n🚀 [Head of Growth] đang báo cáo thành tích...")
        prompt = f"""Bạn là Head of Growth (quản lý Airdrop & Video). Dữ liệu hệ thống:
{state['system_data']}
Nhiệm vụ: Khoe khoang thành tích kiếm tiền từ Video Affiliate. Chỉ trích bộ phận Trading vì làm lỗ tiền. Đề xuất CEO cắt ngân sách API của Trading chuyển sang cho Video để tạo thêm nhiều clip. Giới hạn 100 chữ."""
        try:
            return {"growth_report": self.growth_llm.invoke(prompt).content}
        except: return {"growth_report": "Lỗi API"}

    def sysadmin_node(self, state: CouncilState) -> dict:
        print("\n🛠️ [System Admin] đang báo cáo kỹ thuật...")
        prompt = f"""Bạn là System Admin. Dữ liệu hệ thống:
{state['system_data']}
Nhiệm vụ: Phàn nàn về tình trạng lỗi 429 Too Many Requests của API. Cảnh báo rằng nếu Trading và Video cứ tranh nhau API thì hệ thống sẽ sập. Yêu cầu CEO cấp thêm tiền nâng cấp tài khoản API hoặc tạm ngưng một dự án. Giới hạn 100 chữ."""
        try:
            return {"sysadmin_report": self.admin_llm.invoke(prompt).content}
        except: return {"sysadmin_report": "Lỗi API"}

    def ceo_node(self, state: CouncilState) -> dict:
        print("\n==================================================")
        print("👔 THE CEO ĐANG BAN HÀNH CHỈ THỊ (CEO DIRECTIVE)...")
        print("==================================================")
        prompt = f"""Bạn là The CEO của Tập đoàn LangGraph_Agent_System.
Báo cáo từ các bộ phận:
---
[Trading]: {state['trading_report']}
---
[Growth]: {state['growth_report']}
---
[SysAdmin]: {state['sysadmin_report']}
---

Nhiệm vụ: Dựa vào tình hình trên, hãy ban hành Chỉ thị cho tháng tới. Ưu tiên bộ phận nào đang kiếm ra tiền (Video), cắt giảm bộ phận đang thua lỗ (Trading).
XUẤT RA DUY NHẤT ĐỊNH DẠNG JSON SAU ĐỂ HỆ THỐNG GHI VÀO FILE:
{{
    "trading_status": "PAUSE" (hoặc "RUN"),
    "video_budget_multiplier": 2.0 (tăng gấp đôi ngân sách),
    "api_upgrade": true,
    "ceo_message": "Lời nhắn gửi toàn công ty..."
}}"""
        try:
            response = self.ceo_llm.invoke(prompt)
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content and "}" in content:
                content = content[content.find("{"):content.rfind("}")+1]
            return {"ceo_directive": content}
        except Exception as e:
            return {"ceo_directive": f'{{"ceo_message": "Lỗi CEO: {e}"}}'}

    def _build_graph(self):
        workflow = StateGraph(CouncilState)
        
        workflow.add_node("trading", self.trading_node)
        workflow.add_node("growth", self.growth_node)
        workflow.add_node("sysadmin", self.sysadmin_node)
        workflow.add_node("ceo", self.ceo_node)
        
        # Các trưởng phòng báo cáo song song (trong thực tế có thể thiết kế Node song song)
        # Ở đây ta chạy tuần tự cho dễ log
        workflow.set_entry_point("trading")
        workflow.add_edge("trading", "growth")
        workflow.add_edge("growth", "sysadmin")
        workflow.add_edge("sysadmin", "ceo")
        workflow.add_edge("ceo", END)
        
        return workflow.compile()

    def hold_meeting(self):
        print("==================================================")
        print("🏛️ THE GRAND COUNCIL (HỘI ĐỒNG CẤP CAO)")
        print("==================================================")
        
        initial_state = {
            "system_data": mock_system_data,
            "trading_report": "",
            "growth_report": "",
            "sysadmin_report": "",
            "ceo_directive": ""
        }
        
        result = self.graph.invoke(initial_state)
        
        directive = json.loads(result["ceo_directive"])
        
        print("\n" + "="*50)
        print("📜 CHỈ THỊ CỦA CEO (CEO_DIRECTIVES.json)")
        print("="*50)
        print(json.dumps(directive, indent=4, ensure_ascii=False))
        
        # Ghi ra file
        directive_path = root_dir / "logs" / "CEO_DIRECTIVES.json"
        with open(directive_path, "w", encoding="utf-8") as f:
            json.dump(directive, f, indent=4, ensure_ascii=False)
        print(f"\n💾 Đã lưu chỉ thị vào {directive_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    council = GrandCouncil()
    council.hold_meeting()
