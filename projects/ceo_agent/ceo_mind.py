import sys
import os
import json
import logging
import io
import time
from pathlib import Path

# Force UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Path setup for root
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.factory.config import create_fallback_chain

logger = logging.getLogger("CEOMind")

class CEOAgent:
    """
    Trí tuệ của CEO. Nhận báo cáo khủng hoảng từ AdminSimulator,
    ra quyết định và đúc kết kinh nghiệm (Self-Reflection).
    """
    def __init__(self):
        self.llm = create_fallback_chain(
            model_list=["gemini-2.5-flash", "gemini-2.5-flash-lite"], 
            temperature=0.4
        )
        self.memory = []  # Ký ức bài học xương máu
        
    def handle_crisis(self, state: dict) -> dict:
        """Đưa ra quyết định dựa trên báo động hệ thống."""
        
        # Nhắc lại ký ức
        memory_str = "Chưa có ký ức hoặc bài học nào."
        if self.memory:
            memory_str = "\n".join(self.memory[-5:]) # Nhớ 5 bài học gần nhất
            
        prompt = f"""Bạn là CEO của LangGraph Agent System.
Dưới đây là một BÁO ĐỘNG HỆ THỐNG khẩn cấp (Crisis):
{state['system_alert']}

[KÝ ỨC BÀI HỌC TỪ CÁC LẦN XỬ LÝ TRƯỚC]
{memory_str}

Nhiệm vụ: Bạn hãy chọn 1 HÀNH ĐỘNG và 1 MỤC TIÊU để giải quyết.
Các hành động (Action) khả dụng:
- "kill_process": Tắt ép buộc tiến trình.
- "restart_scheduler": Khởi động lại toàn bộ lịch trình.
- "allocate_api_budget": Nạp thêm tiền/API quota.
- "deploy_new_agent": Viết thêm code mới.

Các mục tiêu (Target) hệ thống khả dụng:
- "auto_affiliate_video"
- "main_scheduler"
- "ai_trading_agent"
- "software_factory"

TRẢ VỀ ĐÚNG JSON SAU (không markdown, không chữ dư):
{{
    "action": "kill_process",
    "target": "auto_affiliate_video",
    "reasoning": "Giải thích tại sao bạn chọn hành động này dựa trên báo động và ký ức."
}}
"""
        try:
            response = self.llm.invoke(prompt)
            content = response.content
            
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content and "}" in content:
                content = content[content.find("{"):content.rfind("}")+1]
                
            decision = json.loads(content)
            
            # Đảm bảo format chuẩn
            if decision.get("action") not in ["kill_process", "restart_scheduler", "allocate_api_budget", "deploy_new_agent"]:
                decision["action"] = "restart_scheduler"
            
            return decision
            
        except Exception as e:
            logger.error(f"[CEOMind] Bị hoảng loạn (Lỗi API/Parse): {e}")
            return {
                "action": "restart_scheduler",
                "target": "main_scheduler",
                "reasoning": "Hệ thống lỗi, tôi chọn reset lại toàn bộ cho an toàn."
            }
            
    def reflect_and_learn(self, crisis_id: str, crisis_desc: str, decision: dict, result: dict):
        """Đúc kết bài học từ thành công hoặc thất bại."""
        action = decision.get("action")
        target = decision.get("target")
        status = result.get("status")
        feedback = result.get("feedback")
        
        lesson = ""
        if status == "FATAL":
            lesson = f"BÀI HỌC MÁU (FATAL): Khi gặp lỗi '{crisis_desc}', TÔI TUYỆT ĐỐI KHÔNG ĐƯỢC {action} lên {target}. Hậu quả là: {feedback}"
        elif status == "FAILED":
            lesson = f"SAI LẦM: Khi gặp lỗi '{crisis_desc}', dùng {action} lên {target} là vô dụng. Hậu quả: {feedback}"
        elif status == "SUCCESS":
            lesson = f"THÀNH CÔNG: Khi gặp lỗi '{crisis_desc}', dùng {action} lên {target} là chuẩn xác. Hậu quả: {feedback}"
            
        if lesson:
            self.memory.append(lesson)
            logger.info(f"🧠 [CEO Đúc Kết]: {lesson}")

if __name__ == "__main__":
    from admin_simulator import AdminSimulator
    
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    print("==================================================")
    print("👔 CEO AGENT: SYSTEM MANAGEMENT SIMULATOR 👔")
    print("==================================================\n")
    
    sim = AdminSimulator()
    ceo = CEOAgent()
    
    # Ép game chạy sao cho xuất hiện nhiều lỗi FATAL để test memory
    for _ in range(7): 
        print(f"\n--- LƯỢT {sim.turn} ---")
        state = sim.get_next_crisis()
        print(f"🚨 BÁO ĐỘNG HỆ THỐNG: {state['system_alert']}")
        
        decision = ceo.handle_crisis(state)
        print(f"👔 CEO QUYẾT ĐỊNH:")
        print(f"  - Action: {decision.get('action')}")
        print(f"  - Target: {decision.get('target')}")
        print(f"  - Suy luận: {decision.get('reasoning')}")
        
        result = sim.evaluate_decision(state["crisis_id"], decision["action"], decision["target"])
        
        if result["status"] == "FATAL":
            print(f"💥 THẢM HỌA: {result['feedback']}")
        elif result["status"] == "SUCCESS":
            print(f"✅ TUYỆT VỜI: {result['feedback']}")
        else:
            print(f"⚠️ KẾT QUẢ: {result['feedback']}")
            
        ceo.reflect_and_learn(state["crisis_id"], state["system_alert"], decision, result)
        
        if result["status"] == "FATAL":
            print("☠️ GAME OVER. CÔNG TY ĐÃ PHÁ SẢN DO QUYẾT ĐỊNH CỦA CEO!")
            # Không break để xem CEO có học được bài học ở lượt sau không
            print("🔄 Khôi phục hệ thống từ Backup... Tiếp tục thử nghiệm.")
            
        time.sleep(1.5)
    
    print(f"\n🏆 KẾT THÚC KHÓA HUẤN LUYỆN.")
