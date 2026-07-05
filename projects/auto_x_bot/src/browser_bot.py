from src.base_agent import BaseAgent
import asyncio
import os
import random
from pathlib import Path
from playwright.async_api import async_playwright
import sys

# Import stealth browser from airdrop_guerrilla
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

try:
    from projects.airdrop_guerrilla.src.automation.stealth_behavior import StealthBrowser
except ImportError:
    # Minimal fallback if not found
    class StealthBrowser(BaseAgent):
        async def init_browser(self, p, profile_dir): return await p.chromium.launch_persistent_context(user_data_dir=profile_dir, headless=False)
        async def stealth_page(self, p): pass
        async def random_delay(self, a, b): await asyncio.sleep(1)
        async def human_scroll(self, page, scrolls): pass

class XBrowserBot(BaseAgent):
    """
    Agent tuong tac X (Twitter) qua trinh duyet de lach luat cam API.
    """
    def __init__(self, profile_name="x_bot_profile"):
        self.profile_dir = BASE_DIR / "data" / "profiles" / profile_name
        self.stealth = StealthBrowser()

    async def post_tweet_browser(self, content: str):
        """Dang tweet bang cach dieu khien trinh duyet."""
        async with async_playwright() as p:
            context = await self.stealth.init_browser(p, str(self.profile_dir))
            page = await context.new_page()
            await self.stealth.stealth_page(page)
            
            print(f"🌐 Dang truy cap X.com...")
            await page.goto("https://x.com/compose/post", wait_until="networkidle")
            await asyncio.sleep(5) # Cho load form
            
            # Kiem tra neu can login
            if "login" in page.url:
                print("⚠️ Yeu cau dang nhap! Vui long dang nhap thu cong vao profile.")
                await page.pause()
                return False

            print(f"✍️ Dang nhap noi dung tweet...")
            # Tim o nhap lieu (X dung div contenteditable)
            editor = await page.wait_for_selector('div[data-testid="tweetTextarea_0"]')
            await editor.click()
            await page.keyboard.type(content, delay=100)
            await asyncio.sleep(2)

            print(f"🚀 Bam nut POST...")
            btn_post = await page.wait_for_selector('button[data-testid="tweetButtonInline"]')
            await btn_post.click()
            
            await asyncio.sleep(5) # Cho post xong
            print("✅ Da dang tweet thanh cong qua trinh duyet!")
            await context.close()
            return True

    async def interact_with_trends(self, keywords=["Bitcoin", "AI", "Web3"]):
        """Tuong tac voi cac xu huong de tang uy tin account."""
        async with async_playwright() as p:
            context = await self.stealth.init_browser(p, str(self.profile_dir))
            page = await context.new_page()
            await self.stealth.stealth_page(page)
            
            for kw in keywords:
                print(f"🔍 Dang tim kiem tu khoa: {kw}")
                await page.goto(f"https://x.com/search?q={kw}&src=typed_query", wait_until="networkidle")
                await asyncio.sleep(random.randint(3, 7))
                
                # Cuon trang de tim bai dang
                await self.stealth.human_scroll(page, scrolls=2)
                
                # Like ngau nhien mot vai post
                like_buttons = await page.query_selector_all('div[data-testid="like"]')
                if like_buttons:
                    target_likes = random.randint(1, min(3, len(like_buttons)))
                    for i in range(target_likes):
                        try:
                            await like_buttons[i].click()
                            print(f"❤️ Da Like 1 bai dang ve {kw}")
                            await asyncio.sleep(random.randint(2, 5))
                        except Exception: continue

            print("✅ Da hoan tat chu ky tuong tac xa hoi.")
            await context.close()
            return True

if __name__ == "__main__":
    bot = XBrowserBot()
    # asyncio.run(bot.post_tweet_browser("Automated tweet from AI Sovereign system! #Web3 #AI"))
