import random
import asyncio
from typing import Optional
from playwright.async_api import Page, BrowserContext, Playwright, async_playwright
import playwright_stealth

class StealthBrowser:
    """
    Giả lập trình duyệt ẩn danh chống detect bot của Cloudflare / Zealy / Galxe.
    """
    def __init__(self, headless: bool = False):
        self.headless = headless
        
    async def init_browser(self, playwright: Playwright, profile_dir: str = "./chrome_profile") -> BrowserContext:
        """Khởi tạo Persistent Browser Context để lưu Cookies và Extension."""
        
        # Random User Agent (Có thể cố định để an toàn hơn cho Persistent)
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        import os
        import os.path
        
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir)
            
        print(f"[*] Su dung Chrome Profile tai: {os.path.abspath(profile_dir)}")
        
        # Sửa lỗi Cloudflare Turnstile: Mượn xác Microsoft Edge cài sẵn trên Windows
        chrome_args = [
            '--start-maximized',       # Mở to toàn màn hình tránh lộ viewport 1280x720 mặc định
            '--disable-blink-features=AutomationControlled'
        ]
        
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            channel="msedge", # DÙNG EDGE XỊN CỦA MÁY ĐỂ CHỐNG CLOUDFLARE 100% (Sạch hơn Chrome)
            headless=False, # Extension chi hoat dong o che do co giao dien
            no_viewport=True, # Tắt ép kích thước để ăn theo --start-maximized
            locale='en-US',
            timezone_id='America/New_York',
            args=chrome_args,
            ignore_default_args=['--enable-automation', '--disable-extensions', '--disable-component-extensions-with-background-pages'] 
        )
        
        # Thiết lập timeout mặc định cho toàn bộ trình duyệt tránh sập khi mạng lag
        context.set_default_timeout(30000)
        
        return context
        
    async def stealth_page(self, page: Page):
        """Bơm stealth xịn vào page"""
        try:
            # Tuỳ theo phiên bản của playwright-stealth mà hàm có thể khác nhau
            if hasattr(playwright_stealth, 'stealth_async'):
                await playwright_stealth.stealth_async(page)
            else:
                # Cách gọi cũ cho vài version
                from playwright_stealth import stealth
                await stealth(page)
        except Exception as e:
            print(f"[*] Canh bao: Khong the bom stealth vao page ({e})")

    async def random_delay(self, min_ms: int = 1000, max_ms: int = 3000):
        """Tạo độ trễ ngẫu nhiên giống con người."""
        delay = random.uniform(min_ms, max_ms) / 1000.0
        await asyncio.sleep(delay)
        
    async def human_scroll(self, page: Page, scrolls: int = 3):
        """Giả lập thao tác cuộn trang của người dùng."""
        for _ in range(scrolls):
            direction = random.choice([1, -1])
            distance = random.randint(100, 400) * direction
            await page.mouse.wheel(0, distance)
            await self.random_delay(500, 1500)
