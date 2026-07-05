import os
import requests
from dotenv import load_dotenv

# Nạp biến môi trường từ file .env
load_dotenv()

class TelegramNotifier:
    """
    Module gửi thông báo (Alerting) qua Telegram Bot.
    Giúp theo dõi các kèo Airdrop tiềm năng (Alpha Leads) một cách tự động.
    """
    def __init__(self):
        self.bot_token = os.getenv("TELE_TOKEN") or os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def is_configured(self) -> bool:
        """Kiểm tra xem đã cấu hình đủ Token và Chat ID chưa."""
        return bool(self.bot_token and self.chat_id)

    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """
        Gửi tin nhắn thô qua Telegram.
        
        Args:
            text (str): Nội dung tin nhắn.
            parse_mode (str): Định dạng tin nhắn (HTML hoặc Markdown).
            
        Returns:
            bool: True nếu gửi thành công, False nếu thất bại.
        """
        if not self.is_configured():
            print("⚠️ Chưa cấu hình TELE_TOKEN hoặc CHAT_ID trong file .env")
            return False
            
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True
        }
        
        try:
            response = requests.post(self.base_url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi khi gửi tin nhắn Telegram: {e}")
            return False

    def send_alpha_alert(self, project_data: dict) -> bool:
        """
        Format dữ liệu dự án thành một tin nhắn đẹp mắt và gửi đi.
        
        Args:
            project_data (dict): Dictionary chứa thông tin dự án.
            
        Returns:
            bool: Trạng thái gửi tin nhắn.
        """
        name = project_data.get('project_name', 'Unknown')
        sector = project_data.get('sector', 'Unknown')
        # Chuyển đổi funding sang Triệu USD nếu cần, giả định đầu vào là USD tuyệt đối
        funding_usd = project_data.get('funding_usd', 0)
        funding_m = funding_usd / 1_000_000
        
        investors_list = project_data.get('investors', [])
        investors = ", ".join(investors_list) if investors_list else "Chưa công bố"
        score = project_data.get('alpha_score', 0)
        
        message = (
            f"🚀 <b>[NEW ALPHA] Phát hiện Kèo Thơm!</b>\n\n"
            f"💎 <b>Dự án:</b> {name}\n"
            f"🏷 <b>Lĩnh vực:</b> {sector}\n"
            f"💰 <b>Funding:</b> {funding_m:.1f}M USD\n"
            f"🏦 <b>Quỹ đầu tư (VCs):</b> {investors}\n\n"
            f"🔥 <b>Alpha Score:</b> <b>{score}</b> Điểm\n"
            f"⚡️ <i>Hệ thống Airdrop Guerrilla</i>"
        )
        
        return self.send_message(message)

if __name__ == "__main__":
    # Test thử Notifier
    test_project = {
        "project_name": "Monad (Test)",
        "sector": "L1 Blockchain",
        "funding_usd": 225000000,
        "investors": ["Paradigm", "Electric Capital", "Greenfield One"],
        "alpha_score": 1875.0
    }
    
    notifier = TelegramNotifier()
    if notifier.is_configured():
        print("Đang gửi tin nhắn test...")
        success = notifier.send_alpha_alert(test_project)
        if success:
            print("✅ Gửi tin nhắn thành công!")
    else:
        print("Vui lòng thêm TELE_TOKEN và CHAT_ID vào .env để test.")
