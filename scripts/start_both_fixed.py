#!/usr/bin/env python3
"""
Script khởi động cả Bot và Dashboard với xử lý Conflict tốt hơn
Sử dụng threading và error handling để tránh conflict
"""

import os
import sys
import time
import logging
import threading
import asyncio
from pathlib import Path

# Thiết lập logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def check_environment():
    """Kiểm tra environment variables"""
    required_vars = ['BOT_TOKEN', 'MY_USER_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ Thiếu environment variables: {missing_vars}")
        return False
    
    logger.info("✅ Environment variables OK")
    return True

def run_dashboard():
    """Chạy web dashboard trong thread riêng"""
    try:
        logger.info("🌐 Khởi động Web Dashboard...")
        
        # Thêm src vào Python path
        src_path = Path(__file__).parent.parent / "src"
        sys.path.insert(0, str(src_path))
        
        logger.info(f"📁 Đã thêm path: {src_path}")
        logger.info(f"📁 Python path: {sys.path[:3]}")
        
        # Import dashboard
        try:
            from web.dashboard import app
            logger.info("✅ Import dashboard thành công")
        except ImportError as e:
            logger.error(f"❌ Lỗi import dashboard: {e}")
            logger.error(f"📁 Current working directory: {os.getcwd()}")
            logger.error(f"📁 Script directory: {Path(__file__).parent}")
            logger.error(f"📁 Src directory: {src_path}")
            raise
        
        # Lấy port từ environment
        port = int(os.getenv('PORT', 10000))
        host = '0.0.0.0'
        
        logger.info(f"✅ Dashboard: http://{host}:{port}")
        logger.info(f"🌐 Environment: Production (Render.com)")
        
        # Chạy dashboard
        app.run(host=host, port=port, debug=False, threaded=True)
        
    except Exception as e:
        logger.error(f"❌ Lỗi chạy dashboard: {e}")
        import traceback
        traceback.print_exc()

def run_bot_with_retry():
    """Chạy bot với retry mechanism"""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            logger.info(f"🤖 Khởi động Telegram Bot lần {retry_count + 1}/{max_retries}")
            
            # Thêm src vào Python path
            src_path = Path(__file__).parent.parent / "src"
            sys.path.insert(0, str(src_path))
            
            logger.info(f"📁 Đã thêm path cho bot: {src_path}")
            
            # Import bot
            try:
                from bot.telegram_handler import TelegramKanbanBot
                logger.info("✅ Import bot thành công")
            except ImportError as e:
                logger.error(f"❌ Lỗi import bot: {e}")
                logger.error(f"📁 Python path: {sys.path[:3]}")
                raise
            
            # Tạo và chạy bot
            bot = TelegramKanbanBot()
            logger.info("✅ Bot instance đã được tạo")
            
            # Chạy bot
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
                    logger.error("❌ Đã thử tối đa, chuyển sang chế độ dashboard only")
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
                    logger.error("❌ Đã thử tối đa, chuyển sang chế độ dashboard only")
                    break
    
    # Nếu bot không thể chạy, chỉ chạy dashboard
    if retry_count >= max_retries:
        logger.warning("⚠️ Bot không thể khởi động, chỉ chạy dashboard")
        logger.info("🌐 Dashboard vẫn hoạt động bình thường")

def main():
    """Main function - chạy cả bot và dashboard"""
    try:
        logger.info("🚀 Khởi động Kanban Bot + Dashboard với Conflict Fix...")
        
        # Kiểm tra environment
        if not check_environment():
            logger.error("❌ Environment không hợp lệ, thoát")
            return
        
        # Chạy dashboard trong thread riêng
        logger.info("🔄 Khởi động Dashboard trong thread riêng...")
        dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
        dashboard_thread.start()
        
        # Đợi dashboard khởi động
        logger.info("⏳ Đợi dashboard khởi động...")
        time.sleep(3)
        
        # Kiểm tra dashboard có hoạt động không
        if dashboard_thread.is_alive():
            logger.info("✅ Dashboard đã khởi động thành công")
        else:
            logger.warning("⚠️ Dashboard có thể chưa khởi động hoàn toàn")
        
        # Chạy bot trong main thread
        logger.info("🤖 Khởi động Telegram Bot...")
        run_bot_with_retry()
        
    except KeyboardInterrupt:
        logger.info("📱 Bot được dừng bởi người dùng")
    except Exception as e:
        logger.error(f"❌ Lỗi chính: {e}")
        import traceback
        traceback.print_exc()
        
        # Trên Render.com, restart script
        if os.getenv('RENDER'):
            logger.info("🔄 Đang restart script trên Render.com...")
            time.sleep(30)
            os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == "__main__":
    main()
