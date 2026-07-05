import asyncio
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from openai import AsyncOpenAI
from projects.sovereign_terminal.core.config import Config
from projects.sovereign_terminal.core.persona import load_persona
from projects.sovereign_terminal.core.tools import TOOL_DEFINITIONS, execute_tool
from projects.sovereign_terminal.core.mcp_client import mcp_manager
from projects.sovereign_terminal.main import handle_tool_calls

# Global state
client = None
system_prompt = ""
chat_histories = {} # CHAT_ID -> messages list

async def initialize_system():
    global client, system_prompt
    load_dotenv()
    
    if not Config.validate():
        sys.exit(1)
        
    print("[TELEGRAM] Đang khởi tạo MCP Clients...")
    mcp_config_path = str(ROOT_DIR / "../../../AppData/Roaming/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json")
    if Path(mcp_config_path).exists():
        mcp_manager.load_config(mcp_config_path)
        await mcp_manager.connect_all()
        print(f"[TELEGRAM] Đã nạp {len(mcp_manager.available_tools)} MCP tools.")
        
    system_prompt = load_persona()
    client = AsyncOpenAI(**Config.get_client_config())
    print("[TELEGRAM] Hệ thống AI đã sẵn sàng.")

async def process_message(user_message: str, chat_id: int) -> str:
    global chat_histories
    
    if chat_id not in chat_histories:
        chat_histories[chat_id] = [{"role": "system", "content": system_prompt}]
        
    messages = chat_histories[chat_id]
    messages.append({"role": "user", "content": user_message})
    
    # Trim history
    if len(messages) > Config.MAX_HISTORY + 1:
        chat_histories[chat_id] = [messages[0]] + messages[-Config.MAX_HISTORY:]
        messages = chat_histories[chat_id]
        
    all_tools = list(TOOL_DEFINITIONS)
    all_tools.extend(mcp_manager.available_tools)
    
    api_kwargs = {
        "model": Config.DEFAULT_MODEL,
        "messages": messages,
        "temperature": Config.TEMPERATURE,
        "max_tokens": Config.MAX_TOKENS,
    }
    if all_tools:
        api_kwargs["tools"] = all_tools
        api_kwargs["tool_choice"] = "auto"
        
    try:
        response = await client.chat.completions.create(**api_kwargs)
        msg = response.choices[0].message
        
        max_tool_rounds = 5
        while msg.tool_calls and max_tool_rounds > 0:
            max_tool_rounds -= 1
            messages.append(msg.model_dump(exclude_none=True))
            msg = await handle_tool_calls(client, Config.DEFAULT_MODEL, messages, msg.tool_calls)
            
        messages.append({"role": "assistant", "content": msg.content or ""})
        return msg.content or "[Empty Response]"
        
    except Exception as e:
        messages.pop() # remove user message if failed
        return f"❌ Lỗi xử lý: {e}"

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 SOVEREIGN TERMINAL - Đã kết nối.\nHãy ra lệnh cho tôi!")

async def reset_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_histories[chat_id] = [{"role": "system", "content": system_prompt}]
    await update.message.reply_text("🔄 Đã xóa bộ nhớ context.")

async def daily_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_chat_id = os.getenv("CHAT_ID")
    if admin_chat_id and str(update.effective_chat.id) != admin_chat_id:
        await update.message.reply_text("⛔ Không có quyền truy cập.")
        return
        
    await update.message.reply_text("⏳ Đang khởi động Sovereign Daily Routine... Quá trình này có thể mất vài phút.")
    
    # Chạy script trong background để không block bot
    script_path = ROOT_DIR / "scripts" / "run_daily_routine.py"
    
    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable, str(script_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(ROOT_DIR)
        )
        
        # Chờ chạy xong
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            await update.message.reply_text("✅ Daily Routine hoàn tất! Hãy kiểm tra báo cáo.")
        else:
            await update.message.reply_text(f"❌ Có lỗi khi chạy Daily Routine:\n{stderr.decode('utf-8')[:1000]}")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi hệ thống: {e}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    admin_chat_id = os.getenv("CHAT_ID")
    
    # Auth check
    if admin_chat_id and str(chat_id) != admin_chat_id:
        await update.message.reply_text("⛔ Không có quyền truy cập.")
        return
        
    user_text = update.message.text
    # Typing indicator
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    reply = await process_message(user_text, chat_id)
    
    # Split message if too long (Telegram limit ~4096)
    for i in range(0, len(reply), 4000):
        await update.message.reply_text(reply[i:i+4000])

async def run_bot():
    load_dotenv()
    tele_token = os.getenv("TELE_TOKEN")
    if not tele_token:
        print("[ERROR] Thiếu TELE_TOKEN trong .env")
        sys.exit(1)
        
    await initialize_system()
    
    app = ApplicationBuilder().token(tele_token).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("reset", reset_cmd))
    app.add_handler(CommandHandler("daily", daily_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("🚀 [TELEGRAM BOT] Đang chạy... Nhấn Ctrl+C để thoát.")
    # Chạy vòng lặp polling
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Chặn chạy forever, nhưng allow Ctrl+C
    stop_event = asyncio.Event()
    try:
        await stop_event.wait()
    except KeyboardInterrupt:
        pass
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        await mcp_manager.close()

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("Đã thoát.")
