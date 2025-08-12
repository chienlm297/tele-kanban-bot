#!/usr/bin/env python3
"""
Tele Kanban Bot - Main Entry Point
Hỗ trợ nhiều cách chạy: bot, dashboard, hoặc cả hai
"""

import sys
import os
import argparse
import threading
import time
import logging

# Thiết lập logging trước
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_bot():
    """Chạy Telegram bot"""
    try:
        from src.bot.telegram_handler import TelegramKanbanBot
        from src.config import settings
        
        logger.info("🤖 Khởi động Telegram Bot...")
        
        # Hiển thị thông tin proxy nếu có
        if hasattr(settings, 'PROXY_ENABLED') and settings.PROXY_ENABLED:
            logger.info(f"🌐 Sử dụng proxy: {settings.PROXY_URL}")
        else:
            logger.info("🌐 Không sử dụng proxy (môi trường nhà)")
        
        bot = TelegramKanbanBot()
        bot.run()
    except Exception as e:
        logger.error(f"❌ Lỗi chạy bot: {e}")
        import traceback
        traceback.print_exc()

def run_dashboard():
    """Chạy web dashboard"""
    try:
        from src.config import settings
        from src.web.dashboard import app
        logger.info("🌐 Khởi động Web Dashboard...")
        
        # Production mode: sử dụng PORT từ environment
        port = int(os.getenv('PORT', getattr(settings, 'WEB_PORT', 8080)))
        host = '0.0.0.0'
        
        logger.info(f"✅ Dashboard: http://{host}:{port}")
        logger.info(f"🌐 Environment: Production (Render.com)")
        
        app.run(host=host, port=port, debug=False, threaded=True)
    except Exception as e:
        logger.error(f"❌ Lỗi chạy dashboard: {e}")
        import traceback
        traceback.print_exc()

def check_dependencies():
    """Kiểm tra dependencies"""
    try:
        import telegram
        import flask
        import requests
        return True
    except ImportError as e:
        logger.error(f"❌ Thiếu dependencies: {e}")
        logger.error("📦 Chạy: pip install -r requirements.txt")
        return False

def check_config():
    """Kiểm tra config"""
    # Check if running on Render (production)
    if os.getenv('RENDER'):
        logger.info("🌍 Running on Render (Production)")
        # Check required environment variables for production
        if not os.getenv('BOT_TOKEN'):
            logger.error("❌ BOT_TOKEN environment variable is required!")
            return False
        if not os.getenv('MY_USER_ID'):
            logger.error("❌ MY_USER_ID environment variable is required!")
            return False
        logger.info("✅ Environment variables OK")
        return True
    
    # Development mode: use settings file
    if not os.path.exists('src/config/settings.py'):
        logger.error("❌ Chưa có file src/config/settings.py!")
        logger.error("📝 Copy src/config/example.py thành src/config/settings.py và điền thông tin")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description='Tele Kanban Bot')
    parser.add_argument('--mode', choices=['bot', 'web', 'both'], default='both',
                       help='Chế độ chạy: bot, web, hoặc both (mặc định: both)')
    
    args = parser.parse_args()
    
    logger.info("🚀 Tele Kanban Bot - AI Smart Task Manager")
    logger.info("=" * 50)
    
    # Kiểm tra config và dependencies
    if not check_config() or not check_dependencies():
        sys.exit(1)
    
    try:
        if args.mode == 'bot':
            run_bot()
        elif args.mode == 'web':
            run_dashboard()
        elif args.mode == 'both':
            logger.info("🔄 Chạy cả Bot và Dashboard...")
            
            # Chạy dashboard trong thread riêng
            dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
            dashboard_thread.start()
            
            # Đợi dashboard khởi động
            time.sleep(3)
            
            # Kiểm tra dashboard có hoạt động không
            if dashboard_thread.is_alive():
                logger.info("✅ Dashboard đã khởi động thành công")
            else:
                logger.warning("⚠️ Dashboard có thể chưa khởi động hoàn toàn")
            
            # Chạy bot trong main thread với retry mechanism
            logger.info("🤖 Khởi động Telegram Bot...")
            run_bot_with_retry()
            
    except KeyboardInterrupt:
        logger.info("\n⏹️  Đang dừng...")
    except Exception as e:
        logger.error(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

def run_bot_with_retry():
    """Chạy bot với retry mechanism để xử lý conflict"""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            logger.info(f"🤖 Khởi động Telegram Bot lần {retry_count + 1}/{max_retries}")
            
            # Import bot
            from src.bot.telegram_handler import TelegramKanbanBot
            from src.config import settings
            
            # Hiển thị thông tin proxy nếu có
            if hasattr(settings, 'PROXY_ENABLED') and settings.PROXY_ENABLED:
                logger.info(f"🌐 Sử dụng proxy: {settings.PROXY_URL}")
            else:
                logger.info("🌐 Không sử dụng proxy (môi trường nhà)")
            
            bot = TelegramKanbanBot()
            bot.run()
            
        except Exception as e:
            retry_count += 1
            error_msg = str(e)
            
            if "Conflict" in error_msg:
                logger.warning(f"⚠️ Conflict error lần {retry_count}: {error_msg}")
                if retry_count < max_retries:
                    logger.info("🔄 Đang chờ 30 giây trước khi thử lại...")
                    time.sleep(30)
                else:
                    logger.error("❌ Đã thử tối đa, bot không thể khởi động")
                    logger.info("🌐 Dashboard vẫn hoạt động bình thường")
                    break
                    
            elif "Forbidden" in error_msg:
                logger.error("❌ Bot bị block hoặc token không hợp lệ")
                break
                
            else:
                logger.error(f"❌ Lỗi khác lần {retry_count}: {error_msg}")
                if retry_count < max_retries:
                    logger.info("🔄 Đang chờ 15 giây trước khi thử lại...")
                    time.sleep(15)
                else:
                    logger.error("❌ Đã thử tối đa, bot không thể khởi động")
                    logger.info("🌐 Dashboard vẫn hoạt động bình thường")
                    break

if __name__ == "__main__":
    main()
