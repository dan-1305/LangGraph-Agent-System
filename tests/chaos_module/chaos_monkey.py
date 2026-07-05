import random
import time

class ChaosMonkey:
    """
    Một 'Con Khỉ' phá hoại chuyên tiêm mã lỗi (Chaos Injector) vào hệ thống
    để kiểm tra xem kiến trúc Phản Giòn (Antifragility) có hoạt động hay không.
    """
    def __init__(self, failure_rate=0.4):
        self.failure_rate = failure_rate
        
    def inject_chaos(self, func):
        def wrapper(*args, **kwargs):
            if random.random() < self.failure_rate:
                chaos_type = random.choice(["rate_limit", "timeout", "corrupted_json", "502_bad_gateway"])
                print(f"[CHAOS MONKEY \U0001f412] Đã tấn công luồng LLM bằng kịch bản: {chaos_type}")
                
                if chaos_type == "rate_limit":
                    # Giả lập lỗi 429
                    raise Exception("429 Too Many Requests: Quota Exceeded")
                elif chaos_type == "timeout":
                    # Giả lập nghẽn mạng
                    time.sleep(1) # Fake delay
                    raise Exception("TimeoutError: API Server did not respond in time")
                elif chaos_type == "corrupted_json":
                    # Trả về output bị hỏng, mô phỏng lỗi LLM bị ảo giác quên đóng ngoặc
                    class FakeResponse:
                        content = '{"result": "Đây là kết quả bị vỡ ngoặc, mất data'
                    return FakeResponse()
                elif chaos_type == "502_bad_gateway":
                    # Giả lập proxy die
                    raise Exception("502 Bad Gateway: Proxy Server is down")
            
            # Trạng thái bình thường: không bị tấn công, gọi hàm gốc
            return func(*args, **kwargs)
        return wrapper
