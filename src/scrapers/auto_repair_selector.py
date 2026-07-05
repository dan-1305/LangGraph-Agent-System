import sys
import io
import os
from pathlib import Path
from typing import Optional, List

# Đảm bảo Encoding UTF-8 trên Windows CMD
if sys.platform == "win32":
    try:
        if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, io.UnsupportedOperation):
        pass

from src.base_agent import BaseAgent
from pydantic import BaseModel, Field

class SelectorPatch(BaseAgent, BaseModel):
    new_selector: str = Field(description="CSS Selector hoặc XPath mới được tìm thấy từ HTML.")
    reasoning: str = Field(description="Giải thích tại sao selector này lại chính xác.")

class AutoRepairSelector(BaseAgent):
    """
    🧬 SELF-REPAIRING SCRAPER MODULE (Hero Product 1)
    Nhiệm vụ: Tự động sửa mã nguồn Scraper khi giao diện Web thay đổi.
    Cơ chế: Failure -> Capture HTML -> LLM Analysis -> Patch Code.
    """
    def __init__(self):
        super().__init__(name="SelectorRepairman", role="Chuyên gia giải phẫu DOM", agent_label="tier-1")

    def _logic_handler(self, **kwargs):
        # Fallback logic nếu AI sập
        return {"new_selector": None, "reasoning": "Fallback: AI không khả dụng để sửa lỗi."}

    def _ai_handler(self, **kwargs):
        html_snippet = kwargs.get("html_snippet", "")
        target_description = kwargs.get("target_description", "Nút bấm hoặc trường dữ liệu cần tìm")
        failed_selector = kwargs.get("failed_selector", "")

        prompt = f"""Bạn là một Chuyên gia Web Scraping bậc thầy.
Giao diện trang web vừa thay đổi khiến Selector cũ [{failed_selector}] bị hỏng (trả về None).

Dưới đây là một phần cấu trúc HTML của trang:
---
{html_snippet}
---

Nhiệm vụ: Hãy tìm một CSS Selector hoặc XPath mới để lấy dữ liệu cho: "{target_description}".
Yêu cầu: Selector phải có tính ổn định cao (Robust), tránh dùng các class ngẫu nhiên của React/Next.js nếu có thể.

Trả về duy nhất JSON định dạng SelectorPatch."""
        
        result = self._call_llm(prompt, schema=SelectorPatch)
        return result

    def repair_and_patch(self, file_path: str, failed_selector: str, html_snippet: str, target_desc: str, http_status: int = 200):
        """
        Thực hiện quy trình sửa lỗi và vá code tự động.
        Tích hợp [Anti-Bot Guard]: Kháng độc Cloudflare & Blocked IP.
        """
        # --- [Anti-Bot Guard Layer] ---
        if http_status in [403, 429, 503]:
            print(f"🚨 [AutoRepair] ABORT: Phat hien bi chan (Status {http_status}). Cam LLM va code de tranh nhiu.")
            return False
            
        anti_bot_keywords = ["cloudflare", "turnstile", "captcha", "security check", "robot check"]
        if any(kw in html_snippet.lower() for kw in anti_bot_keywords):
            print(f"🚨 [AutoRepair] ABORT: HTML chua tin hieu Anti-Bot. Khong phai loi DOM change.")
            return False

        print(f"🔧 [AutoRepair] Dang phan tich HTML de sua Selector: '{failed_selector}'...")
        res = self.execute(html_snippet=html_snippet, failed_selector=failed_selector, target_description=target_desc)
        
        new_selector = res.get("new_selector")
        if new_selector:
            print(f"✅ [AutoRepair] Đã tìm thấy Selector mới: '{new_selector}'")
            print(f"📝 [AutoRepair] Lý do: {res.get('reasoning')}")
            
            # Đọc file gốc
            full_path = Path(file_path)
            if full_path.exists():
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Vá code (Dùng replace đơn giản cho demo, trong thực tế sẽ dùng AST)
                new_content = content.replace(failed_selector, new_selector)
                
                # Lưu file
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"🚀 [AutoRepair] ĐÃ VÁ THÀNH CÔNG MÃ NGUỒN TẠI: {file_path}")
                return True
        return False

# Singleton instance
selector_repairman = AutoRepairSelector()
