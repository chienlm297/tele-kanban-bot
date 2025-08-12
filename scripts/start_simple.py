#!/usr/bin/env python3
"""
Script khởi động đơn giản cho Render.com
Tránh các vấn đề import phức tạp
"""

import os
import sys
import logging

# Thiết lập logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Khởi động bot với cách đơn giản nhất"""
    try:
        logger.info("🚀 Khởi động Kanban Bot trên Render.com...")
        
        # Kiểm tra environment variables
        if not os.getenv('BOT_TOKEN'):
            logger.error("❌ Thiếu BOT_TOKEN")
            return
        
        if not os.getenv('MY_USER_ID'):
            logger.error("❌ Thiếu MY_USER_ID")
            return
        
        logger.info("✅ Environment variables OK")
        
        # Import và chạy bot
        try:
            # Thêm current directory vào path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            src_dir = os.path.join(parent_dir, 'src')
            
            sys.path.insert(0, parent_dir)
            sys.path.insert(0, src_dir)
            
            logger.info(f"📁 Paths: {sys.path[:3]}")
            
            # Import bot
            from bot.telegram_handler import TelegramKanbanBot
            logger.info("✅ Import thành công")
            
            # Tạo và chạy bot
            bot = TelegramKanbanBot()
            logger.info("🚀 Khởi động bot...")
            bot.run()
            
        except ImportError as e:
            logger.error(f"❌ Lỗi import: {e}")
            logger.error(f"📁 Current dir: {os.getcwd()}")
            logger.error(f"📁 Script dir: {current_dir}")
            logger.error(f"📁 Parent dir: {parent_dir}")
            logger.error(f"📁 Src dir: {src_dir}")
            logger.error(f"📁 Python path: {sys.path}")
            
        except Exception as e:
            logger.error(f"❌ Lỗi khác: {e}")
            
    except Exception as e:
        logger.error(f"❌ Lỗi chính: {e}")

if __name__ == "__main__":
    main()
