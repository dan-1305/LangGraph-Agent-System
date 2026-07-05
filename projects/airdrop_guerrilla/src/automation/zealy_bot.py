import sys
import os
from pathlib import Path
import asyncio

# Fix relative import when running directly
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from playwright.async_api import async_playwright
from stealth_behavior import StealthBrowser

class ZealyBot:
    """
    Web Automation Bot chuyên làm task trên nền tảng Zealy.io
    Sử dụng kiến trúc StealthBrowser chống detection.
    """
    def __init__(self, community_slug: str):
        self.community_slug = community_slug
        self.stealth_browser = StealthBrowser(headless=False) # Để False để sếp có thể xem bot chạy
        
    async def run_quests(self):
        """Khởi động luồng chạy quest tự động"""
        print(f"Bat dau nhiem vu Guerrilla tren cong dong: {self.community_slug}")
        
        async with async_playwright() as p:
            context = await self.stealth_browser.init_browser(p)
            # persistent_context tự có sẵn 1 page
            page = context.pages[0] if context.pages else await context.new_page()
            
            try:
                # Tính năng: Tạm dừng VÔ HẠN để sếp đăng nhập lần đầu
                print("\n=======================================================")
                print("[*] TRINH DUYET DA MO.")
                print("[*] Ban co the tim 'Metamask Extension' tren Google de tai vao Chrome ao nay.")
                print("[*] Trinh duyet se TAM DUNG. Khi nao setup xong, bam nut 'Resume' (mui ten) tren Inspector de tiep tuc.")
                print("[*] Cookies va Extension se duoc luu lai vinh vien!")
                print("=======================================================\n")
                
                # Treo bot vô hạn cho đến khi user bấm Resume
                await page.pause()
                
                print("\n[*] Dang truy cap Zealy.io...")
                # Đi tới trang quest board
                await page.goto(f"https://zealy.io/cw/{self.community_slug}/questboard")
                await self.stealth_browser.random_delay(3000, 5000)
                
                # Giả lập cuộn trang như người thật để load UI
                print("Dang cuon trang lam gia nguoi dung...")
                await self.stealth_browser.human_scroll(page, scrolls=4)
                
                print("Dang kiem tra nut 'Log in' hoac 'Connect Wallet' tren Zealy...")
                # Dựa vào DOM thực tế của Zealy: <a href="/login">Log in</a>
                login_button = page.locator('a[href="/login"]')
                
                if await login_button.count() > 0:
                    print("[+] Phat hien nut Log in! Tien hanh click...")
                    await login_button.first.click()
                    await self.stealth_browser.random_delay(2000, 3000)
                    print("[+] Vui long chon phuong thuc dang nhap bang Metamask hoac Discord o man hinh tiep theo.")
                else:
                    print("[+] Da dang nhap san (Khong thay nut Log in). Tien hanh quet cac Quest...")
                
                await self.stealth_browser.random_delay(2000, 4000)
                print("[*] Hoan tat luong gia lap Web Automation cho Zealy!")
                
            except Exception as e:
                print(f"Loi trong qua trinh chay web automation: {e}")
            finally:
                print("Dang dong trinh duyet Stealth...")
                await context.close()

if __name__ == "__main__":
    # Test script chạy bot thử
    bot = ZealyBot(community_slug="test-community")
    asyncio.run(bot.run_quests())
