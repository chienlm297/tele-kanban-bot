#!/usr/bin/env python3
"""
Script khởi động bot cho Render.com
Được thiết kế để tránh lỗi Conflict khi deploy
"""

import os
import sys
import time
import logging
from pathlib import Path

# Thêm src vào Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Thiết lập logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Khởi động bot với xử lý đặc biệt cho Render.com"""
    try:
        logger.info("🚀 Khởi động Kanban Bot trên Render.com...")
        
        # Kiểm tra environment variables
        required_vars = ['BOT_TOKEN', 'MY_USER_ID']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"❌ Thiếu environment variables: {missing_vars}")
            sys.exit(1)
        
        # Import bot sau khi đã thiết lập path
        from src.bot.telegram_handler import TelegramKanbanBot
        
        # Tạo instance bot
        bot = TelegramKanbanBot()
        
        # Khởi động bot
        logger.info("✅ Bot instance đã được tạo, đang khởi động...")
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("📱 Bot được dừng bởi người dùng")
    except Exception as e:
        logger.error(f"❌ Lỗi khởi động bot: {e}")
        # Trên Render.com, không exit để tránh restart liên tục
        if os.getenv('RENDER'):
            logger.info("🔄 Đang chờ restart trên Render.com...")
            time.sleep(60)  # Chờ 1 phút trước khi thử lại
            main()  # Restart
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()
