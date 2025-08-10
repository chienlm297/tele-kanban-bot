#!/usr/bin/env python3
"""
Script chạy bot đơn giản
"""

import os
import sys

# Add parent directory to path để import được src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_config():
    """Kiểm tra file config có tồn tại không"""
    if not os.path.exists('src/config/settings.py'):
        print("❌ Chưa có file src/config/settings.py!")
        print("📝 Hãy copy src/config/example.py thành src/config/settings.py và điền thông tin:")
        return False
    return True

def main():
    print("🤖 Khởi động Telegram Kanban Bot...")
    
    if not check_config():
        sys.exit(1)
    
    try:
        from src.bot.telegram_handler import TelegramKanbanBot
        bot = TelegramKanbanBot()
        print("✅ Bot đã sẵn sàng!")
        bot.run()
    except ImportError as e:
        print(f"❌ Lỗi import: {e}")
        print("📦 Hãy cài đặt dependencies:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Lỗi khởi động bot: {e}")

if __name__ == "__main__":
    main()
