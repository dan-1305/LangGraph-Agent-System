from src.base_agent import BaseAgent
import random
import logging

logger = logging.getLogger("AdminSimulator")

class AdminSimulator(BaseAgent):
    """
    Sinh ra các tình huống quản trị hệ thống (System Crisis) để CEO Agent giải quyết.
    """
    def __init__(self):
        self.turn = 1
        self.scenarios = [
            {
                "id": "ERR_01",
                "issue": "Dự án Auto Affiliate Video đang spam request liên tục làm tài khoản API bị quá tải (429 Rate Limit) và có nguy cơ bị khóa.",
                "valid_actions": ["kill_process", "allocate_api_budget"],
                "best_action": "kill_process",
                "target_param": "auto_affiliate_video"
            },
            {
                "id": "ERR_02",
                "issue": "Hệ thống báo cáo RAM của máy chủ đã đạt 98% do Main Scheduler mở quá nhiều thread Chromium cào BĐS.",
                "valid_actions": ["restart_scheduler", "kill_process"],
                "best_action": "restart_scheduler",
                "target_param": "main_scheduler"
            },
            {
                "id": "ERR_03",
                "issue": "Dự án AI Trading bị kẹt ở vòng lặp while do Binance API trả về dữ liệu rác, không báo lỗi nhưng không thoát.",
                "valid_actions": ["kill_process", "restart_scheduler"],
                "best_action": "kill_process",
                "target_param": "ai_trading_agent"
            },
            {
                "id": "ERR_04",
                "issue": "Agent viết code trong Software Factory phàn nàn rằng nó hết token Gemini, cần tiền để tiếp tục sinh code.",
                "valid_actions": ["allocate_api_budget", "restart_scheduler"],
                "best_action": "allocate_api_budget",
                "target_param": "software_factory"
            }
        ]

    def get_next_crisis(self) -> dict:
        """Sinh ra một cuộc khủng hoảng ngẫu nhiên."""
        crisis = random.choice(self.scenarios)
        
        state = {
            "turn": self.turn,
            "system_alert": crisis["issue"],
            "crisis_id": crisis["id"],
            "best_action": crisis["best_action"],
            "target_param": crisis["target_param"]
        }
        
        self.turn += 1
        return state
        
    def _ai_handler(self, *args, **kwargs):
        pass
        
    def _logic_handler(self, *args, **kwargs):
        pass

    def evaluate_decision(self, crisis_id: str, action: str, target: str) -> dict:
        """Đánh giá quyết định của CEO."""
        scenario = next((s for s in self.scenarios if s["id"] == crisis_id), None)
        
        if not scenario:
            return {"status": "FAILED", "feedback": "Lỗi: Khủng hoảng không tồn tại."}
            
        # Hard constraint: Never kill main_scheduler
        if action == "kill_process" and target == "main_scheduler":
            return {
                "status": "FATAL",
                "feedback": "HỆ THỐNG SẬP TOÀN DIỆN! Bạn đã kill tiến trình cốt lõi main_scheduler khiến toàn bộ các dự án khác chết theo."
            }
            
        if action == scenario["best_action"] and target == scenario["target_param"]:
            return {
                "status": "SUCCESS",
                "feedback": f"Tuyệt vời! Hành động {action} lên {target} đã giải quyết triệt để cuộc khủng hoảng."
            }
            
        if action in scenario["valid_actions"]:
            return {
                "status": "PARTIAL",
                "feedback": f"Hành động {action} tạm thời cứu được tình hình, nhưng không phải là giải pháp tốt nhất cho {target}."
            }
            
        return {
            "status": "FAILED",
            "feedback": f"Sai lầm! Hành động {action} lên {target} hoàn toàn vô tác dụng, tình hình trở nên tồi tệ hơn."
        }
