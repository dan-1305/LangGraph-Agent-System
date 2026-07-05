import sys
import json
from pathlib import Path

# Add root to sys.path
base_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.append(str(base_dir))

from src.base_agent import BaseAgent

class FunctionalTester(BaseAgent):
    def __init__(self):
        super().__init__(model_name="label:tier-1", temperature=0.1)

    def _ai_handler(self, state: dict) -> dict:
        return state

    def _logic_handler(self, state: dict) -> dict:
        return state

    def ai_assert(self, expected_behavior: str, actual_output: str) -> bool:
        """Sử dụng LLM để chấm điểm kết quả (Functional Assertion)."""
        prompt = f"""Ngươi là một QA Functional Tester chuyên nghiệp.
Hãy đánh giá xem ACTUAL_OUTPUT có đáp ứng được EXPECTED_BEHAVIOR không.

EXPECTED_BEHAVIOR:
{expected_behavior}

ACTUAL_OUTPUT:
{actual_output}

Trả về định dạng JSON:
{{
    "pass": true/false,
    "reason": "Giải thích ngắn gọn tại sao pass hoặc fail"
}}
"""
        result = self._call_llm_with_retry(prompt, is_json=True)
        try:
            if isinstance(result, str):
                result = json.loads(result)
            return result.get("pass", False), result.get("reason", "Lỗi phân tích JSON")
        except Exception as e:
            return False, f"Lỗi AI Assertion: {str(e)}"

    def test_streamlit_ui(self):
        """Dùng Playwright test Streamlit UI (End-to-End)"""
        print("\n[TEST] Bắt đầu UI Test cho Auto Affiliate Video...")
        from playwright.sync_api import sync_playwright
        import subprocess
        import time

        print("[*] Đang khởi động Streamlit server ngầm...")
        app_path = base_dir / "projects" / "auto_affiliate_video" / "app.py"
        
        # Start streamlit in background
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", str(app_path), "--server.port=8505", "--server.headless=true"],
            env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
        time.sleep(5) # Đợi server khởi động
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto("http://localhost:8505")
                
                print("[*] Đang tương tác với giao diện...")
                page.wait_for_selector("input[aria-label='📦 Nhập Tên Sản Phẩm / Chủ đề (VD: Robot Hút Bụi, Tin tức chấn động...)']", timeout=10000)
                
                # Nhập liệu
                page.fill("input[aria-label='📦 Nhập Tên Sản Phẩm / Chủ đề (VD: Robot Hút Bụi, Tin tức chấn động...)']", "Sách Ehon cho bé")
                page.fill("input[aria-label='✨ Tính năng nổi bật / Ngữ cảnh (Cách nhau dấu phẩy)']", "Hình ảnh đẹp, giáo dục tốt")
                
                # Bấm tạo kịch bản
                # Ta không bấm "Tạo Video" vì tốn thời gian render, chỉ tick "1. Chỉ tạo Kịch Bản"
                # Nhưng mặc định nó đã tick cả 3. Ta bấm nút.
                page.click("button:has-text('BẮT ĐẦU TẠO')")
                
                print("[*] Đang chờ kết quả từ UI...")
                # Đợi text "✅ Đã có Kịch bản!" xuất hiện
                page.wait_for_selector("text=✅ Đã có Kịch bản!", timeout=30000)
                
                # Chụp ảnh màn hình làm bằng chứng
                screenshot_path = base_dir / "reports" / "ui_test_evidence.png"
                screenshot_path.parent.mkdir(exist_ok=True)
                page.screenshot(path=str(screenshot_path))
                print(f"✅ PASSED! UI Test thành công, đã lưu ảnh: {screenshot_path}")
                
                browser.close()
        except Exception as e:
            print(f"❌ FAILED UI Test: {e}")
        finally:
            process.kill()

    def test_script_generator(self):
        """Unit/Functional test cho ScriptGenerator của Auto Affiliate Video"""
        print("\n[TEST] Bắt đầu test ScriptGenerator của Auto Affiliate Video...")
        try:
            from projects.auto_affiliate_video.src.script_generator import ScriptGenerator
            sg = ScriptGenerator()
            product_name = "Robot hút bụi thông minh"
            features = "Pin trâu, dọn dẹp sạch sẽ, có AI tự né vật cản"
            
            print(f"[*] Đang sinh kịch bản cho sản phẩm: {product_name}...")
            script = sg.generate_short_video_script(product_name, features)
            
            print("[*] Đang gửi cho AI Assertion chấm điểm...")
            expected = "Kịch bản phải là tiếng Việt, đề cập đến Robot hút bụi, nêu được tính năng Pin trâu, siêu sạch, và có lời kêu gọi hành động (Call to action) ngắn gọn dưới 100 từ."
            
            passed, reason = self.ai_assert(expected, script)
            
            if passed:
                print(f"✅ PASSED! Lý do: {reason}")
            else:
                print(f"❌ FAILED! Lý do: {reason}")
                print(f"   => Output thực tế:\n{script}")
                
        except Exception as e:
            print(f"❌ CRASH TRONG QUÁ TRÌNH TEST: {e}")

if __name__ == "__main__":
    import sys
    import os
    # Fix encoding
    if sys.platform == "win32" and hasattr(sys.stdout, 'reconfigure'):
        if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
        
    tester = FunctionalTester()
    tester.test_script_generator()
    tester.test_streamlit_ui()
