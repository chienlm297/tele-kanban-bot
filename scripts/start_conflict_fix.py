#!/usr/bin/env python3
"""
Script khởi động đặc biệt để xử lý Conflict error trên Render.com
Tự động restart bot khi gặp conflict
"""

import os
import sys
import time
import logging
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

async def run_bot_with_retry():
    """Chạy bot với retry mechanism"""
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            logger.info(f"🚀 Khởi động bot lần {retry_count + 1}/{max_retries}")
            
            # Thêm src vào Python path
            src_path = Path(__file__).parent.parent / "src"
            sys.path.insert(0, str(src_path))
            
            # Import bot
            from bot.telegram_handler import TelegramKanbanBot
            
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
                logger.info("🔄 Đang chờ 60 giây trước khi thử lại...")
                await asyncio.sleep(60)
                
            elif "Forbidden" in error_msg:
                logger.error("❌ Bot bị block hoặc token không hợp lệ")
                break
                
            else:
                logger.error(f"❌ Lỗi khác lần {retry_count}: {error_msg}")
                logger.info("🔄 Đang chờ 30 giây trước khi thử lại...")
                await asyncio.sleep(30)
    
    if retry_count >= max_retries:
        logger.error(f"❌ Đã thử {max_retries} lần, dừng retry")
        logger.info("🔄 Chờ 5 phút trước khi restart hoàn toàn...")
        await asyncio.sleep(300)
        # Restart script
        os.execv(sys.executable, ['python'] + sys.argv)

async def main():
    """Main function"""
    try:
        logger.info("🚀 Khởi động Kanban Bot với Conflict Fix trên Render.com...")
        
        # Kiểm tra environment
        if not check_environment():
            logger.error("❌ Environment không hợp lệ, thoát")
            return
        
        # Chạy bot với retry
        await run_bot_with_retry()
        
    except KeyboardInterrupt:
        logger.info("📱 Bot được dừng bởi người dùng")
    except Exception as e:
        logger.error(f"❌ Lỗi chính: {e}")
        # Trên Render.com, restart script
        if os.getenv('RENDER'):
            logger.info("🔄 Đang restart script trên Render.com...")
            time.sleep(30)
            os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == "__main__":
    # Chạy async main
    asyncio.run(main())
