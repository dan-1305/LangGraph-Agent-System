import sys
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# Đảm bảo import được các module trong project
base_dir = Path(__file__).resolve().parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from src.automation.wallet_manager import WalletManager
from src.automation.session_manager import SessionManager
from cryptography.fernet import Fernet
from dotenv import load_dotenv

def alert_user_for_manual_action(message: str):
    """
    Kích hoạt chuông báo (Beep) và dừng chương trình chờ người dùng can thiệp.
    (Ví dụ: Giải Captcha Cloudflare hoặc Confirm Wallet).
    """
    print(f"\n🚨 [HUMAN-IN-THE-LOOP REQUIRED] 🚨")
    print(f"👉 {message}")
    
    # Phát tiếng Beep 3 lần để gây sự chú ý
    for _ in range(3):
        sys.stdout.write('\a')
        sys.stdout.flush()
        time.sleep(0.5)
        
    input("👉 Sau khi bạn đã xử lý xong trên Trình duyệt, hãy nhấn [ENTER] để bot tiếp tục chạy...")
    print("▶️ Tiếp tục thực thi tự động...\n")

def run_semi_auto_quests():
    print("👨‍💻 KHỞI ĐỘNG HỆ THỐNG SEMI-AUTO (CÓ SỰ TRỢ GIÚP CỦA CON NGƯỜI)")
    
    load_dotenv(base_dir / ".env")
    encryption_key = os.getenv("WALLET_ENCRYPTION_KEY")
    if not encryption_key:
        encryption_key = Fernet.generate_key()
        
    db_path = base_dir / "data" / "wallets" / "secure_wallets.json"
    wm = WalletManager(str(db_path), encryption_key)
    
    test_address = "0x71C7656EC7ab88b098defB751B7401B5f6d8976F"
    if not wm.wallets:
        wm.add_wallet(test_address, "0xFakeKey", "Demo Wallet")

    with sync_playwright() as p:
        print("🌐 Mở trình duyệt có giao diện (Headless=False) để bạn dễ quan sát...")
        # Bắt buộc phải có UI để người dùng tương tác khi bị kẹt
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()

        # Ví dụ 1: Đi Faucet lấy Testnet Token bị dính Cloudflare
        print("\n--- TASK 1: XIN FAUCET INCO TESTNET ---")
        page.goto("https://faucet.testnet.inco.org/")
        
        # Dừng lại yêu cầu user tự giải captcha nếu có
        alert_user_for_manual_action(
            "Trang Faucet Inco thường có Cloudflare Turnstile hoặc ReCaptcha.\n"
            "Hãy chuyển sang cửa sổ Trình duyệt, dán địa chỉ ví và tự click Captcha.\n"
            "Chờ đến khi Token được gửi về ví thì quay lại đây."
        )

        # Ví dụ 2: Làm Zealy cần kết nối Discord
        print("\n--- TASK 2: ZEALY QUESTS ---")
        page.goto("https://zealy.io")
        
        alert_user_for_manual_action(
            "Bot đã mở Zealy. Bạn hãy tự click Login bằng Discord.\n"
            "Nếu bị kẹt xác minh Cloudflare, hãy tự giải quyết.\n"
            "Sau khi vào được Dashboard của Zealy, quay lại đây bấm Enter để bot tự động Claim quest."
        )
        
        print("🤖 Bot tiếp quản: Tự động quét và Claim Reward...")
        try:
            claim_buttons = page.locator("button:has-text('Claim Reward')")
            count = claim_buttons.count()
            if count > 0:
                print(f"🎉 Tìm thấy {count} nhiệm vụ. Đang auto claim...")
                for i in range(count):
                    page.locator("button:has-text('Claim Reward')").nth(0).click()
                    time.sleep(2)
            else:
                print("💤 Không có nhiệm vụ nào để claim.")
        except Exception as e:
            print(f"⚠️ Lỗi khi claim: {e}")

        print("\n🏁 HOÀN TẤT LUỒNG SEMI-AUTO!")
        browser.close()

if __name__ == "__main__":
    run_semi_auto_quests()
