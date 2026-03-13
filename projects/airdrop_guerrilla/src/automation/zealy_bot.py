import time
import random
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

base_dir = Path(__file__).resolve().parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.append(str(base_dir))

from src.automation.session_manager import SessionManager
from src.automation.stealth_behavior import StealthBehavior
from src.automation.wallet_manager import WalletManager

class ZealyBot:
    """
    Bot tự động hóa nhiệm vụ trên Zealy (Airdrop platform).
    Sử dụng Session Discord để đăng nhập và vượt rào cản.
    """
    def __init__(self, wallet_manager: WalletManager):
        self.wallet_manager = wallet_manager

    def run_quests(self, wallet_address: str, community_url: str):
        if wallet_address not in self.wallet_manager.wallets:
            print(f"❌ Ví {wallet_address} không tồn tại!")
            return
            
        wallet_info = self.wallet_manager.wallets[wallet_address]
        user_agent = wallet_info['user_agent']
        wallet_name = wallet_info['name']
        
        decrypted_data = self.wallet_manager.get_decrypted_data(wallet_address)
        dc_token = decrypted_data.get('discord_token', "")
        
        if not dc_token:
            print("❌ Không có Discord Token để login Zealy.")
            return

        session_dir = base_dir / "data" / "sessions"
        session_dir.mkdir(parents=True, exist_ok=True)
        session_file = session_dir / f"{wallet_address}.json"

        print(f"\n🚀 Khởi động Zealy Bot cho ví: {wallet_name} ({wallet_address[:6]})")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context_args = {
                'user_agent': user_agent,
                'viewport': {'width': 1280, 'height': 720}
            }
            
            # Load storage_state nếu có
            is_new_session = True
            if session_file.exists():
                context_args['storage_state'] = str(session_file)
                is_new_session = False
                
            context = browser.new_context(**context_args)
            
            if is_new_session:
                SessionManager.apply_discord_session(context, dc_token)

            page = context.new_page()
            page.set_default_timeout(30000)

            try:
                print("   🔗 Truy cập Zealy...")
                page.goto("https://zealy.io")
                StealthBehavior.human_pause(3, 5)
                
                # Giả lập login bằng Discord nếu chưa login
                if page.locator("button:has-text('Connect')").count() > 0:
                    print("   🔑 Đang thực hiện Login qua Discord...")
                    page.click("button:has-text('Connect')")
                    time.sleep(2)
                    page.click("button:has-text('Discord')")
                    page.wait_for_load_state("networkidle")
                    
                    # Cấp quyền Auth trên Discord OAuth page
                    if page.locator("button:has-text('Authorize')").count() > 0:
                        page.click("button:has-text('Authorize')")
                    
                    page.wait_for_url("**/communities**", timeout=15000)
                    # Cập nhật session sau khi login thành công
                    context.storage_state(path=str(session_file))
                
                print(f"   🎯 Truy cập Community: {community_url}")
                page.goto(community_url)
                StealthBehavior.random_scroll(page, 2, 4)
                
                # Tìm các Quest có thể Claim
                print("   🔍 Đang quét các nhiệm vụ (Quests) có thể Claim...")
                claim_buttons = page.locator("button:has-text('Claim Reward')")
                count = claim_buttons.count()
                
                if count == 0:
                    print("   💤 Không có nhiệm vụ nào sẵn sàng để Claim lúc này.")
                else:
                    print(f"   🎉 Tìm thấy {count} nhiệm vụ! Đang tự động xử lý...")
                    for i in range(count):
                        try:
                            # Phải re-query locator sau mỗi lần click vì DOM thay đổi
                            btn = page.locator("button:has-text('Claim Reward')").nth(0)
                            btn.scroll_into_view_if_needed()
                            StealthBehavior.human_pause(1, 3)
                            btn.click()
                            print(f"      ✅ Đã Claim nhiệm vụ #{i+1}!")
                            StealthBehavior.human_pause(3, 6)
                        except Exception as e:
                            print(f"      ⚠️ Lỗi khi Claim nhiệm vụ #{i+1}: {str(e)[:50]}")
                            
            except PlaywrightTimeoutError:
                print("❌ Lỗi Timeout: Trang web phản hồi quá chậm hoặc bị chặn.")
            except Exception as e:
                print(f"❌ Lỗi không xác định: {e}")
            finally:
                print(f"🏁 Đã hoàn thành quá trình cày Zealy cho {wallet_name}.")
                browser.close()

if __name__ == "__main__":
    from cryptography.fernet import Fernet
    test_key = Fernet.generate_key()
    db_path = base_dir / "data" / "wallets" / "secure_wallets.json"
    wm = WalletManager(str(db_path), test_key)
    
    test_address = "0x71C7656EC7ab88b098defB751B7401B5f6d8976F"
    if test_address not in wm.wallets:
        wm.add_wallet(test_address, "fake_pk", "Demo Wallet", "fake_tw", "fake_dc_token")
        
    bot = ZealyBot(wm)
    # Lấy community giả định
    bot.run_quests(test_address, "https://zealy.io/c/monad/questboard")
