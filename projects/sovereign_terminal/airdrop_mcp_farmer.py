import asyncio
import os
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from projects.sovereign_terminal.core.mcp_client import mcp_manager
from core_utilities.http_client import HTTPClient

async def send_telegram_alert(message: str):
    from dotenv import load_dotenv
    load_dotenv()
    tele_token = os.getenv("TELE_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if tele_token and chat_id:
        try:
            url = f"https://api.telegram.org/bot{tele_token}/sendMessage"
            HTTPClient.post(url, json={"chat_id": chat_id, "text": message}, timeout=10.0)
        except Exception:
            pass

async def farm_faucet(target_url: str, wallet_address: str):
    """
    Sử dụng Playwright MCP (qua mcp_client.py) để tự động hóa trình duyệt
    thay vì dùng thư viện playwright trực tiếp. Điều này giúp Terminal Headless
    có thể điều khiển trình duyệt chạy ở background server.
    """
    print(f"🚜 [Airdrop MCP Farmer] Khởi động farm cho ví: {wallet_address[:6]}...")
    
    # Đảm bảo MCP Manager đã kết nối
    mcp_config_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Code", "User", "globalStorage", "saoudrizwan.claude-dev", "settings", "cline_mcp_settings.json")
    mcp_manager.load_config(mcp_config_path)
    
    # Lọc chỉ kết nối playwright
    mcp_manager.server_configs = {
        k: v for k, v in mcp_manager.server_configs.items() 
        if "playwright" in k
    }
    
    if not mcp_manager.server_configs:
        print("❌ [Airdrop MCP Farmer] Không tìm thấy server Playwright MCP trong config.")
        return

    await mcp_manager.connect_all()
    
    # Kịch bản thực thi qua MCP
    try:
        print(f"🌐 Navigating to {target_url}...")
        res = await mcp_manager.execute_tool("playwright_navigate", {"url": target_url})
        print(f"   -> {res[:100]}...")
        
        await asyncio.sleep(5) # Chờ load trang
        
        print("⌨️ Điền địa chỉ ví...")
        res = await mcp_manager.execute_tool("playwright_fill", {
            "selector": "input[type='text'], input[name='wallet']",
            "value": wallet_address
        })
        print(f"   -> {res[:100]}...")
        
        await asyncio.sleep(2)
        
        print("🖱️ Bấm nút Claim...")
        res = await mcp_manager.execute_tool("playwright_click", {
            "selector": "button:has-text('Claim'), button[type='submit']"
        })
        print(f"   -> {res[:100]}...")
        
        await asyncio.sleep(5)
        
        print("📸 Chụp ảnh màn hình bằng chứng...")
        screenshot_path = str(ROOT_DIR / "data" / "logs" / "errors" / f"faucet_mcp_{wallet_address[:6]}.png")
        Path(screenshot_path).parent.mkdir(parents=True, exist_ok=True)
        res = await mcp_manager.execute_tool("playwright_screenshot", {
            "name": f"faucet_mcp_{wallet_address[:6]}.png",
            "savePng": True
        })
        
        success_msg = f"✅ Đã chạy xong luồng Claim cho ví {wallet_address[:6]}. Kiểm tra ảnh screenshot để xác nhận."
        print(success_msg)
        await send_telegram_alert(success_msg)
        
    except Exception as e:
        err_msg = f"❌ Lỗi khi farm qua MCP: {e}"
        print(err_msg)
        await send_telegram_alert(err_msg)
    finally:
        await mcp_manager.close()

if __name__ == "__main__":
    # Test kịch bản
    test_url = "https://faucet.monad.xyz/" # Hoặc URL test
    test_wallet = "0x1234567890ABCDEF1234567890ABCDEF12345678"
    asyncio.run(farm_faucet(test_url, test_wallet))
