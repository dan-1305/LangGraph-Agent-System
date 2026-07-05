import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
from jarvis_core.config import Config

logger = logging.getLogger(__name__)

class TelegramWebhookBot:
    """
    Telegram bot với hỗ trợ webhook cho deployment trên Render/Heroku
    """
    
    def __init__(self):
        self.config = Config()
        self.token = self.config.get("TELEGRAM_BOT_TOKEN")
        self.webhook_url = self.config.get("WEBHOOK_URL", "")
        self.use_webhook = self.config.get("USE_WEBHOOK", "false").lower() == "true"
        self.port = int(self.config.get("PORT", "8443"))
        
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not configured")
        
        self.application = Application.builder().token(self.token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup command and message handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle photo messages for calendar parsing"""
        caption = update.message.caption or ""
        if "lịch" not in caption.lower() and "schedule" not in caption.lower():
            await update.message.reply_text("Tôi đã nhận được ảnh. Gửi kèm caption có chữ 'lịch' để tự động tạo sự kiện nhé.")
            return

        await update.message.reply_text("⏳ Đang phân tích ảnh lịch tuần... Vui lòng đợi trong giây lát.")
        try:
            photo_file = await update.message.photo[-1].get_file()
            os.makedirs("data", exist_ok=True)
            file_path = f"data/temp_schedule_{update.message.message_id}.jpg"
            await photo_file.download_to_drive(file_path)
            
            # Logic xử lý
            from jarvis_core.vision_parser import parse_schedule_image
            from jarvis_core.google_services import get_creds, create_calendar_event
            import datetime
            
            def get_next_weekday(day_name):
                days = {'thứ 2': 0, 'monday': 0, 'thứ 3': 1, 'tuesday': 1, 'thứ 4': 2, 'wednesday': 2,
                        'thứ 5': 3, 'thursday': 3, 'thứ 6': 4, 'friday': 4, 'thứ 7': 5, 'saturday': 5,
                        'chủ nhật': 6, 'sunday': 6, 'cn': 6}
                day_name_lower = day_name.lower().strip()
                target_day = next((v for k, v in days.items() if k in day_name_lower), None)
                if target_day is None: return datetime.date.today().isoformat()
                today = datetime.date.today()
                days_ahead = target_day - today.weekday()
                if days_ahead < 0: days_ahead += 7
                return (today + datetime.timedelta(days_ahead)).isoformat()

            events_json = parse_schedule_image(file_path)
            if not events_json:
                await update.message.reply_text("❌ Không trích xuất được sự kiện nào từ ảnh.")
                return
                
            creds = get_creds()
            if not creds:
                await update.message.reply_text("❌ Chưa cấp quyền Google Calendar. Vui lòng kiểm tra lại token.")
                return
                
            added_events = []
            for ev in events_json:
                raw_date = ev.get('date', '')
                date_iso = get_next_weekday(raw_date) if len(raw_date) != 10 or "-" not in raw_date else raw_date
                start_time_iso = f"{date_iso}T{ev.get('start_time', '00:00')}:00"
                end_time_iso = f"{date_iso}T{ev.get('end_time', '01:00')}:00"
                summary = ev.get('summary', 'Sự kiện')
                
                success = create_calendar_event(
                    creds, summary, start_time_iso, end_time_iso, 
                    ev.get('description', 'Tạo từ AI'), ev.get('location', '')
                )
                if success:
                    added_events.append(f"- {summary} ({date_iso} {ev.get('start_time')})")
            
            if os.path.exists(file_path):
                os.remove(file_path)
                
            reply_text = f"✅ Đã thêm {len(added_events)} sự kiện vào lịch:\n" + "\n".join(added_events)
            await update.message.reply_text(reply_text)
            
        except Exception as e:
            logger.error(f"Error processing photo: {e}")
            await update.message.reply_text("❌ Có lỗi xảy ra khi xử lý ảnh lịch.")
            
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        await update.message.reply_text(
            "👋 Xin chào! Tôi là Jarvis RPG Assistant.\n"
            "Sử dụng /help để xem danh sách lệnh."
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 <b>Jarvis RPG Assistant Commands</b>

/start - Khởi động bot
/help - Hiển thị trợ giúp
/stats - Xem thống kê của bạn
/tasks - Xem danh sách nhiệm vụ
/learn - Học từ vựng mới

📝 Bạn cũng có thể gửi tin nhắn thường để chat với AI!
        """
        await update.message.reply_text(help_text, parse_mode='HTML')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        user_message = update.message.text
        logger.info(f"Received message from {update.effective_user.id}: {user_message}")
        
        await update.message.reply_text(f"Bạn đã nói: {user_message}")
    
    def run_polling(self):
        """Run bot with polling (for local development)"""
        logger.info("Starting bot with polling mode...")
        self.application.run_polling()
    
    async def setup_webhook(self):
        """Setup webhook for production deployment"""
        if not self.webhook_url:
            raise ValueError("WEBHOOK_URL not configured for webhook mode")
        
        webhook_path = f"{self.webhook_url}/webhook/{self.token}"
        
        await self.application.bot.set_webhook(
            url=webhook_path,
            drop_pending_updates=True
        )
        logger.info(f"Webhook set to: {webhook_path}")
    
    def run_webhook(self, listen="0.0.0.0"):
        """Run bot with webhook (for production)"""
        logger.info(f"Starting bot with webhook mode on port {self.port}...")
        
        import asyncio
        asyncio.run(self.setup_webhook())
        
        self.application.run_webhook(
            listen=listen,
            port=self.port,
            url_path=f"webhook/{self.token}",
            webhook_url=f"{self.webhook_url}/webhook/{self.token}"
        )
    
    def run(self):
        """Run bot with appropriate mode based on configuration"""
        if self.use_webhook:
            self.run_webhook()
        else:
            self.run_polling()


def main():
    """Main entry point"""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    bot = TelegramWebhookBot()
    bot.run()


if __name__ == '__main__':
    main()
