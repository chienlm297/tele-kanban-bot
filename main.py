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

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_bot():
    """Chạy Telegram bot"""
    try:
        from src.bot.telegram_handler import TelegramKanbanBot
        from src.config import settings
        
        print("🤖 Khởi động Telegram Bot...")
        
        # Hiển thị thông tin proxy nếu có
        if hasattr(settings, 'PROXY_ENABLED') and settings.PROXY_ENABLED:
            print(f"🌐 Sử dụng proxy: {settings.PROXY_URL}")
        else:
            print("🌐 Không sử dụng proxy (môi trường nhà)")
        
        bot = TelegramKanbanBot()
        bot.run()
    except Exception as e:
        print(f"❌ Lỗi chạy bot: {e}")

def run_dashboard():
    """Chạy web dashboard"""
    try:
        from src.config import settings
        from src.web.dashboard import app
        print("🌐 Khởi động Web Dashboard...")
        
        # Production mode: sử dụng PORT từ environment
        port = int(os.getenv('PORT', settings.WEB_PORT))
        host = '0.0.0.0'
        
        print(f"✅ Dashboard: http://{host}:{port}")
        print(f"🌐 Environment: Development")
        
        app.run(host=host, port=port, debug=False, threaded=True)
    except Exception as e:
        print(f"❌ Lỗi chạy dashboard: {e}")
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
        print(f"❌ Thiếu dependencies: {e}")
        print("📦 Chạy: pip install -r requirements.txt")
        return False

def check_config():
    """Kiểm tra config"""
    # Development mode only
    return True
    
    # Development mode: use settings file
    if not os.path.exists('src/config/settings.py'):
        print("❌ Chưa có file src/config/settings.py!")
        print("📝 Copy src/config/example.py thành src/config/settings.py và điền thông tin")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description='Tele Kanban Bot')
    parser.add_argument('--mode', choices=['bot', 'web', 'both'], default='both',
                       help='Chế độ chạy: bot, web, hoặc both (mặc định: both)')
    
    args = parser.parse_args()
    
    print("🚀 Tele Kanban Bot - AI Smart Task Manager")
    print("=" * 50)
    
    # Kiểm tra config và dependencies
    if not check_config() or not check_dependencies():
        sys.exit(1)
    
    try:
        if args.mode == 'bot':
            run_bot()
        elif args.mode == 'web':
            run_dashboard()
        elif args.mode == 'both':
            print("🔄 Chạy cả Bot và Dashboard...")
            
            # Chạy dashboard trong thread riêng
            dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
            dashboard_thread.start()
            
            # Đợi dashboard khởi động
            time.sleep(2)
            
            # Chạy bot trong main thread
            run_bot()
            
    except KeyboardInterrupt:
        print("\n⏹️  Đang dừng...")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()
