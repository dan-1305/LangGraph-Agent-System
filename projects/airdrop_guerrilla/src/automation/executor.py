import json
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

import os
import sys
base_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(base_dir))

from twocaptcha import TwoCaptcha
from src.utils.notifier import TelegramNotifier
from src.automation.wallet_manager import WalletManager
from src.automation.session_manager import SessionManager
from src.automation.stealth_behavior import StealthBehavior

class AirdropExecutor:
    """
    Stealth Engine: Tự động hóa trình duyệt (Browser Automation) dùng Playwright.
    Đọc file JSON (Action Plan) và thực thi các bước farm airdrop một cách tàng hình.
    """
    def __init__(self, action_plan_path: str, wallet_manager: WalletManager, notifier: TelegramNotifier):
        self.action_plan_path = Path(action_plan_path)
        self.wallet_manager = wallet_manager
        self.notifier = notifier
        
        with open(self.action_plan_path, 'r', encoding='utf-8') as f:
            self.plan = json.load(f)

    def execute_wallet(self, wallet_address: str):
        """
        Khởi chạy kịch bản farm cho một ví cụ thể.
        """
        # 1. Trích xuất thông tin chống Sybil của ví
        if wallet_address not in self.wallet_manager.wallets:
            print(f"❌ Ví {wallet_address} không tồn tại trong WalletManager!")
            return
            
        wallet_info = self.wallet_manager.wallets[wallet_address]
        user_agent = wallet_info['user_agent']
        wallet_name = wallet_info['name']
        
        # Lấy token mạng xã hội đã giải mã
        decrypted_data = self.wallet_manager.get_decrypted_data(wallet_address)
        tw_token = decrypted_data.get('twitter_token', "")
        dc_token = decrypted_data.get('discord_token', "")
        
        project_name = self.plan.get('project', 'Unknown Project')
        
        print(f"\n🚀 Bắt đầu Farm [{project_name}] bằng ví: {wallet_name} ({wallet_address})")
        print(f"🕵️ Sử dụng Stealth User-Agent: {user_agent}")
        
        # Đường dẫn file storage_state
        session_dir = base_dir / "data" / "sessions"
        session_dir.mkdir(parents=True, exist_ok=True)
        session_file = session_dir / f"{wallet_address}.json"
        
        with sync_playwright() as p:
            # Khởi tạo trình duyệt Headless (Nhẹ, tiết kiệm RAM cho máy i3)
            browser = p.chromium.launch(headless=True)
            
            context_args = {
                'user_agent': user_agent,
                'viewport': {'width': 1280, 'height': 720},
                'locale': 'en-US',
                'timezone_id': 'Asia/Ho_Chi_Minh'
            }
            
            # Load storage_state nếu đã có (Bỏ qua bước nạp token)
            is_new_session = True
            if session_file.exists():
                print("   💾 Tìm thấy Session Profile. Đang nạp storageState...")
                context_args['storage_state'] = str(session_file)
                is_new_session = False
                
            context = browser.new_context(**context_args)
            
            if is_new_session:
                print("   🔑 Chưa có Session Profile, đang nạp token từ WalletManager...")
                # Nạp Session Persistence cho Twitter vào context
                if tw_token:
                    SessionManager.apply_twitter_session(context, tw_token)
                # Nạp Session Persistence cho Discord (Sử dụng context init script)
                if dc_token:
                    SessionManager.apply_discord_session(context, dc_token)
            
            # Dùng 1 page duy nhất suốt quá trình (Tiết kiệm RAM cho i3)
            page = context.new_page()
            
            # Set timeout toàn cục (30s)
            page.set_default_timeout(30000)
            
            tasks = self.plan.get('tasks', [])
            
            # Ưu tiên test Twitter trước
            tasks = sorted(tasks, key=lambda x: 0 if x.get('platform') == 'Twitter' else 1)
            
            for task in tasks:
                step = task.get('step')
                platform = task.get('platform')
                action = task.get('action')
                url = task.get('url')
                
                print(f"⏳ Đang thực hiện Step {step} - [{platform}]: {action}")
                
                try:
                    # Logic mô phỏng các thao tác
                    if platform == "Twitter":
                        self._twitter_interact(page, context, action, url, wallet_address)
                    elif platform == "Discord":
                        self._discord_join(page, context, url, wallet_address)
                    elif platform == "Faucet":
                        self._handle_faucet_demo(page, url, wallet_address)
                    else:
                        print(f"   ⏩ Chưa hỗ trợ tự động platform {platform}. Bỏ qua: {url}")
                        time.sleep(random.uniform(2, 4))
                        
                except PlaywrightTimeoutError:
                    error_msg = f"❌ Ví {wallet_name} ({wallet_address[:6]}...) gặp lỗi Timeout tại Bước {step}: {action} (Dự án: {project_name})"
                    print(error_msg)
                    
                    # Bắn thông báo Telegram ngay lập tức
                    alert_text = (
                        f"🚨 <b>[BOT ALERT] Lỗi kẹt Farm!</b>\n\n"
                        f"💻 <b>Ví:</b> {wallet_name} ({wallet_address[:6]}...)\n"
                        f"💎 <b>Dự án:</b> {project_name}\n"
                        f"⚠️ <b>Lỗi:</b> Timeout tại Bước {step} ({platform})\n"
                        f"🛑 Trình duyệt đã tự động đóng để bảo vệ máy."
                    )
                    self.notifier.send_message(alert_text)
                    
                    # Ngắt quy trình hiện tại, đóng trình duyệt giải phóng RAM
                    browser.close()
                    return
                except Exception as e:
                    print(f"❌ Lỗi không xác định: {e}")
                    browser.close()
                    return
            
            print(f"✅ Đã hoàn thành toàn bộ kịch bản cho ví {wallet_name}!")
            browser.close()

    def _handle_faucet_demo(self, page, url: str, address: str):
        """
        Logic mẫu cho việc qua mặt Faucet (Dán ví -> Giải Captcha -> Click).
        Sử dụng 2Captcha để vượt qua iframe xác thực.
        """
        print(f"   🌍 Truy cập {url}...")
        page.goto(url)
        time.sleep(random.uniform(5, 10))
        
        print(f"   ⌨️ Nhập địa chỉ ví: {address}")
        try:
            page.fill("input[name='wallet_address']", address)
        except Exception:
            print("   ⚠️ Không tìm thấy input 'wallet_address', thử dùng input type='text'")
            page.fill("input[type='text']", address)
            
        time.sleep(random.uniform(2, 5))
        
        # Tích hợp giải Captcha
        print("   🤖 Đang kiểm tra xem có Captcha không...")
        sitekey_element = page.locator("[data-sitekey]")
        if sitekey_element.count() > 0:
            sitekey = sitekey_element.first.get_attribute("data-sitekey")
            print(f"   🧩 Phát hiện ReCaptcha/HCaptcha (Sitekey: {sitekey}). Đang gửi lên 2Captcha...")
            
            api_key = os.getenv("TWOCAPTCHA_API_KEY", "")
            if not api_key:
                print("   ❌ Lỗi: Chưa cấu hình TWOCAPTCHA_API_KEY trong file .env!")
                raise PlaywrightTimeoutError("Missing 2Captcha API Key")
                
            solver = TwoCaptcha(api_key)
            try:
                # Gửi yêu cầu giải (giả định dùng reCAPTCHA v2)
                # Tuỳ chọn: hcaptcha_solver hoặc recaptcha_solver.
                result = solver.recaptcha(sitekey=sitekey, url=page.url)
                code = result['code']
                print("   ✅ Giải Captcha thành công! Đang tiêm token vào trang...")
                
                # Tiêm mã vào trang (Playwright evaluate)
                page.evaluate(f"document.getElementById('g-recaptcha-response').innerHTML = '{code}';")
                time.sleep(random.uniform(1, 2))
                
                # Gọi callback nếu trang yêu cầu
                page.evaluate("if(typeof recaptchaCallback !== 'undefined') recaptchaCallback();")
                
            except Exception as e:
                print(f"   ❌ Lỗi khi giải Captcha: {e}")
                raise PlaywrightTimeoutError("Captcha Solving Failed")
        else:
            print("   ✅ Không phát hiện Captcha (Hoặc cấu trúc DOM khác).")

        print("   🖱️ Bấm nút 'Claim Tokens'...")
        try:
            page.click("button:has-text('Claim')")
        except Exception:
            # Fallback nếu nút claim có tên khác
            page.click("button[type='submit']")
            
        try:
            page.wait_for_selector(".success-message", timeout=10000)
            print("   🎉 Claim Faucet thành công!")
        except Exception:
            print("   ⚠️ Không thấy message success, nhưng có thể đã thành công. Vui lòng check lại số dư.")

    def _verify_login_status(self, page, context, platform: str, wallet_address: str) -> bool:
        """Kiểm tra xem trang hiện tại đã được đăng nhập hay chưa (chờ tối đa 15s)."""
        print(f"   🔍 Đang kiểm tra trạng thái đăng nhập trên {platform}...")
        try:
            if platform == "Twitter":
                # Đợi một phần tử chỉ xuất hiện khi đã login (vd: menu compose hoặc User avatar) hoăc timeout
                # Cụ thể, X có một tag 'a[data-testid="AppTabBar_Profile_Link"]' hoặc input post
                page.wait_for_selector("a[data-testid='AppTabBar_Profile_Link']", timeout=15000)
                print("   ✅ Đăng nhập X (Twitter) thành công!")
                # Lưu state sau khi login thành công
                session_file = base_dir / "data" / "sessions" / f"{wallet_address}.json"
                context.storage_state(path=str(session_file))
                return True
            elif platform == "Discord":
                # Chờ load xong app
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(5)
                print(f"   👉 URL hiện tại của Discord: {page.url}")
                if "login" not in page.url:
                    print("   ✅ Đăng nhập Discord thành công!")
                    # Lưu state sau khi login thành công
                    session_file = base_dir / "data" / "sessions" / f"{wallet_address}.json"
                    context.storage_state(path=str(session_file))
                    return True
                else:
                    raise PlaywrightTimeoutError("Vẫn ở trang Login")
        except PlaywrightTimeoutError:
            print(f"   ⚠️ Hết 15 giây vẫn không thấy dấu hiệu đăng nhập của {platform}. Có thể Token hỏng hoặc bị chặn. URL: {page.url}")
            return False
        return False

    def _twitter_interact(self, page, context, action: str, url: str, wallet_address: str):
        """Logic tương tác tự động với Twitter (X) kèm Natural Browsing."""
        print(f"   🐦 Đang truy cập X (Twitter): {url}")
        page.goto(url)
        
        if not self._verify_login_status(page, context, "Twitter", wallet_address):
            # Chụp ảnh báo lỗi vào thư mục error logs
            error_dir = base_dir / "data" / "logs" / "errors"
            error_dir.mkdir(parents=True, exist_ok=True)
            proof_path = error_dir / f"twitter_login_failed_{wallet_address[:6]}.png"
            page.screenshot(path=str(proof_path))
            print(f"   📸 Đã chụp ảnh màn hình LỖI lưu tại: {proof_path}")
            raise PlaywrightTimeoutError("Twitter Authentication Failed")
            
        # Kích hoạt Natural Browsing (Khởi động)
        StealthBehavior.perform_warmup(page)
        
        if "Follow" in action:
            print("   👀 Đang tìm nút Follow...")
            follow_selector = "div[data-testid$='-follow']"
            try:
                page.wait_for_selector(follow_selector, timeout=10000)
                page.click(follow_selector)
                print("   ✅ Đã Follow thành công!")
            except PlaywrightTimeoutError:
                print("   ⚠️ Không tìm thấy nút Follow hoặc đã Follow từ trước.")
        time.sleep(random.uniform(2, 4))

    def _discord_join(self, page, context, invite_url: str, wallet_address: str):
        """Logic tự động Join Discord."""
        print("   🎮 Đang truy cập trang chủ Discord để load Token...")
        page.goto("https://discord.com/app")
        
        if not self._verify_login_status(page, context, "Discord", wallet_address):
            # Chụp ảnh báo lỗi vào thư mục error logs
            error_dir = base_dir / "data" / "logs" / "errors"
            error_dir.mkdir(parents=True, exist_ok=True)
            proof_path = error_dir / f"discord_login_failed_{wallet_address[:6]}.png"
            page.screenshot(path=str(proof_path))
            print(f"   📸 Đã chụp ảnh màn hình LỖI lưu tại: {proof_path}")
            raise PlaywrightTimeoutError("Discord Authentication Failed")
            
        print(f"   🎮 Đang truy cập Discord Invite: {invite_url}")
        page.goto(invite_url)
        time.sleep(random.uniform(4, 7))
        
        print("   🖱️ Đang tìm nút 'Accept Invite'...")
        accept_button = "button:has-text('Accept Invite')"
        try:
            page.wait_for_selector(accept_button, timeout=10000)
            page.click(accept_button)
            print("   ✅ Đã bấm Accept Invite!")
            
            time.sleep(random.uniform(5, 8))
            verify_btn = "button:has-text('Complete')"
            if page.locator(verify_btn).count() > 0:
                print("   🛡️ Tìm thấy nút Complete verification, đang xử lý...")
                page.click(verify_btn)
                time.sleep(random.uniform(1, 2))
                page.click("input[type='checkbox']")
                page.click("button:has-text('Submit')")
                print("   ✅ Đã vượt qua Verification cơ bản!")
                
        except PlaywrightTimeoutError:
            print("   ⚠️ Không tìm thấy nút Accept Invite (Có thể Link lỗi hoặc đã vào từ trước).")

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    plan_path = base_dir / "data" / "action_plans" / "monad.json"
    db_path = base_dir / "data" / "wallets" / "secure_wallets.json"
    
    notifier = TelegramNotifier()
    from cryptography.fernet import Fernet
    test_key = Fernet.generate_key()
    wm = WalletManager(str(db_path), test_key)
    
    test_address = "0x71C7656EC7ab88b098defB751B7401B5f6d8976F"
    if test_address not in wm.wallets:
        wm.add_wallet(test_address, "0xFakeKey123", "Demo Bot Wallet")
        
    tw_token = os.getenv("Auth_Token_X", "")
    dc_token = os.getenv("Auth_Token_Discord", "")
    
    # Update fake tokens with real ones for testing
    wm.wallets[test_address]["encrypted_twitter_token"] = wm.cipher.encrypt(tw_token.encode('utf-8')).decode('utf-8')
    wm.wallets[test_address]["encrypted_discord_token"] = wm.cipher.encrypt(dc_token.encode('utf-8')).decode('utf-8')
    wm._save_db()
    
    executor = AirdropExecutor(str(plan_path), wm, notifier)
    executor.execute_wallet(test_address)
