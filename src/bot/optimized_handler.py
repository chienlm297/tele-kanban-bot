import logging
from telegram.ext import Application
from src.bot.telegram_handler import TelegramKanbanBot
import os

class OptimizedTelegramBot(TelegramKanbanBot):
    """Telegram bot tối ưu cho Railway"""
    
    def __init__(self):
        super().__init__()
        
        # Reduce logging in production
        if os.getenv('RAILWAY_ENVIRONMENT'):
            logging.getLogger('telegram').setLevel(logging.WARNING)
            logging.getLogger('httpx').setLevel(logging.WARNING)
    
    def run(self):
        """Chạy bot với optimizations"""
        application = Application.builder().token(self.settings.BOT_TOKEN).build()
        
        # Production optimizations
        if os.getenv('RAILWAY_ENVIRONMENT'):
            # Reduce concurrent workers
            application.bot._request_timeout = 10  # Shorter timeout
            application.updater.timeout = 30
            
        # Đăng ký handlers (tương tự như parent class)
        self._register_handlers(application)
        
        logger.info("🤖 Optimized bot starting...")
        
        # Chạy với optimizations
        application.run_polling(
            poll_interval=1.0,  # Longer poll interval to save CPU
            timeout=30,
            bootstrap_retries=3,
            read_timeout=10,
            write_timeout=10,
            connect_timeout=10,
            pool_timeout=5
        )
        
    def _register_handlers(self, application):
        """Register all handlers"""
        from telegram.ext import CommandHandler, MessageHandler, filters
        
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("tasks", self.tasks_command))
        application.add_handler(CommandHandler("ai", self.ai_suggestions_command))
        application.add_handler(CommandHandler("insights", self.insights_command))
        application.add_handler(CommandHandler("all", self.all_tasks_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        
        # Handler cho tất cả messages
        application.add_handler(MessageHandler(filters.ALL, self.handle_message))
