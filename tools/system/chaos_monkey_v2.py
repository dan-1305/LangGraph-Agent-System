import sys
import os
import time
import random
import logging
from pathlib import Path

# Thêm đường dẫn gốc
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from projects.ceo_agent.admin_simulator import AdminSimulator
from projects.ceo_agent.ceo_mind import CEOAgent

logger = logging.getLogger("ChaosMonkeyV2")
logging.basicConfig(level=logging.INFO, format="[🔥 ChaosMonkey] %(message)s")

class ChaosMonkeyV2:
    """
    [PHASE 1 Q4 - AUTOMATED CHAOS]
    Tự động bắn phá hệ thống bằng cách liên tục gọi AdminSimulator.
    Kích hoạt CEO Agent để giải quyết và học hỏi từ các thất bại (FATAL/FAILED).
    """
    def __init__(self, iterations=5):
        self.iterations = iterations
        self.simulator = AdminSimulator()
        self.ceo = CEOAgent()
        
    def unleash_chaos(self):
        logger.info(f"Bắt đầu chiến dịch bắn phá hệ thống với {self.iterations} đợt (Crisis).")
        
        for i in range(self.iterations):
            logger.info(f"\n{'='*50}\nĐỢT TẤN CÔNG THỨ {i+1}\n{'='*50}")
            
            # Lấy khủng hoảng từ Simulator
            state = self.simulator.get_next_crisis()
            logger.info(f"🚨 SỰ CỐ: {state['system_alert']}")
            
            # Gọi CEO xử lý
            logger.info("🧠 Kích hoạt CEOAgent suy luận...")
            decision = self.ceo.handle_crisis(state)
            
            action = decision.get("action")
            target = decision.get("target")
            reasoning = decision.get("reasoning")
            
            logger.info(f"👔 Quyết định của CEO:")
            logger.info(f"   - Hành động : {action}")
            logger.info(f"   - Mục tiêu  : {target}")
            logger.info(f"   - Suy luận  : {reasoning}")
            
            # Đánh giá kết quả
            result = self.simulator.evaluate_decision(state["crisis_id"], action, target)
            status = result["status"]
            
            if status == "FATAL":
                logger.error(f"☠️ HẬU QUẢ NGHIÊM TRỌNG: {result['feedback']}")
            elif status == "SUCCESS":
                logger.info(f"✅ THÀNH CÔNG: {result['feedback']}")
            else:
                logger.warning(f"⚠️ KẾT QUẢ KHÁC: {result['feedback']}")
                
            # Đúc kết bài học (Kích hoạt Self-Evolution V2)
            self.ceo.reflect_and_learn(state["crisis_id"], state["system_alert"], decision, result)
            
            # Giả lập thời gian chờ giữa các đợt
            time.sleep(2)
            
        logger.info("\n🎉 Hoàn tất đợt bắn phá. Các bài học đã được lưu vào Ký ức (Memory) của CEO.")
        
if __name__ == "__main__":
    monkey = ChaosMonkeyV2(iterations=3)
    monkey.unleash_chaos()
