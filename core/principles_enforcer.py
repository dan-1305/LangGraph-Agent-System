import logging
from typing import Any, Dict

class PrinciplesEnforcer:
    """
    Lớp đối soát nguyên lý (Principles Enforcer) - Sovereign Core.
    Nhiệm vụ: Kiểm tra độ tuân thủ nguyên lý của các đầu ra từ Agent.
    """
    def __init__(self):
        self.logger = logging.getLogger("PrinciplesEnforcer")
        self.principles = {
            "risk_first": "Ưu tiên quản trị rủi ro trước lợi nhuận.",
            "clean_arch": "Dependencies hướng vào chính sách cấp cao.",
            "high_output": "Đo lường dựa trên kết quả đầu ra thực tế.",
            "integrity": "Kiểm soát tính toàn vẹn tuyệt đối."
        }

    def verify_decision(self, agent_role: str, decision: Dict[str, Any]) -> bool:
        """
        Kiểm tra xem quyết định có vi phạm nguyên lý cốt lõi không.
        """
        self.logger.info(f"🧐 [Core Enforcer] Đang kiểm tra quyết định của {agent_role}...")
        
        # Ví dụ: Kiểm tra Risk Manager
        if agent_role == "RiskManager":
            allocation = decision.get("allocation", {})
            # Nguyên lý: Phải có USDT phòng thủ nếu rủi ro cao (giả định rủi ro cao qua confidence_score thấp)
            if decision.get("confidence_score", 0) < 5 and allocation.get("USDT", 0) < 0.3:
                self.logger.critical("🚨 VI PHẠM: Confidence thấp nhưng tỷ lệ USDT < 30%.")
                return False
                
        return True

    def audit_agent_output(self, output: str) -> float:
        """Chấm điểm độ tuân thủ nguyên lý của văn bản (0.0 - 1.0)"""
        # Logic chấm điểm dựa trên từ khóa hoặc LLM (hiện tại dùng regex đơn giản)
        score = 0.5
        keywords = ["rủi ro", "risk", "bảo vệ", "nguyên lý", "đầu ra", "toàn vẹn"]
        matches = [word for word in keywords if word in output.lower()]
        score += (len(matches) / len(keywords)) * 0.5
        return min(score, 1.0)

enforcer = PrinciplesEnforcer()
