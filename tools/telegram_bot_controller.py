import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

base_dir = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv
load_dotenv(base_dir / ".env")

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Lấy token từ .env
TOKEN = os.getenv("TELE_TOKEN")
if not TOKEN:
    print("❌ Lỗi: Không tìm thấy TELE_TOKEN trong .env")
    sys.exit(1)

# Danh sách user được phép truy cập (bảo mật)
ALLOWED_CHAT_ID = os.getenv("CHAT_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gửi menu điều khiển khi user gõ /start."""
    user_id = str(update.effective_user.id)
    if ALLOWED_CHAT_ID and user_id != ALLOWED_CHAT_ID:
        await update.message.reply_text("⛔ Bạn không có quyền truy cập hệ thống này.")
        return

    keyboard = [
        ["🚀 Chạy AI Trading Agent", "🌐 Chạy Airdrop Guerrilla"],
        ["🔄 Xem trạng thái hệ thống", "🗄️ Backup Database Ngay"],
        ["🏥 Kích hoạt Đặc vụ Y tế (Watchdog)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "🤖 **POLYMORPHIC AGENT SYSTEM - COMMAND CENTER**\n"
        "Chào sếp! Vui lòng chọn tác vụ bên dưới để điều khiển các Agent (Thay thế hoàn toàn cho Streamlit UI để tiết kiệm RAM).",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    if ALLOWED_CHAT_ID and user_id != ALLOWED_CHAT_ID:
        return

    text = update.message.text
    
    if text == "🚀 Chạy AI Trading Agent":
        await update.message.reply_text("⏳ Đang kích hoạt AI Trading Agent (Chạy ngầm)...")
        # Logic gọi Agent
        import threading
        def run_trading():
            os.system(f"uv run python projects/ai_trading_agent/src/live_advisor.py")
        threading.Thread(target=run_trading).start()
        await update.message.reply_text("✅ Trading Agent đã bắt đầu vòng lặp thị trường.")
        
    elif text == "🌐 Chạy Airdrop Guerrilla":
        await update.message.reply_text("⏳ Đang kích hoạt Airdrop Guerrilla (Chế độ Stealth)...")
        def run_airdrop():
            os.system(f"uv run python projects/airdrop_guerrilla/src/modes/full_auto_cli.py")
        import threading
        threading.Thread(target=run_airdrop).start()
        await update.message.reply_text("✅ Airdrop Guerrilla đã lên đường làm nhiệm vụ.")
        
    elif text == "🔄 Xem trạng thái hệ thống":
        import psutil
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        await update.message.reply_text(f"📊 **Trạng thái:**\n- CPU: {cpu}%\n- RAM: {ram}%", parse_mode='Markdown')
        
    elif text == "🗄️ Backup Database Ngay":
        await update.message.reply_text("⏳ Đang nén và backup Database sang ổ D...")
        os.system(f"uv run python core_utilities/backup_manager.py --now")
        await update.message.reply_text("✅ Đã gửi lệnh Backup. Vui lòng check log hoặc tin báo hệ thống.")
        
    elif text == "🏥 Kích hoạt Đặc vụ Y tế (Watchdog)":
        await update.message.reply_text("⏳ Đang dò tìm và tiêu diệt Zombie Process...")
        import subprocess
        # Chạy script watchdog 1 lần
        subprocess.Popen(["uv", "run", "python", "-c", "from core_utilities.process_watchdog import check_system_health, check_and_kill_zombies; check_system_health(); check_and_kill_zombies()"])
        await update.message.reply_text("✅ Lệnh càn quét đã được ban hành.")
        
    else:
        await update.message.reply_text("❓ Lệnh không hợp lệ. Vui lòng chọn menu bên dưới.")

def main() -> None:
    """Start the bot."""
    print("🤖 Telegram Bot Controller đang chạy...")
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
