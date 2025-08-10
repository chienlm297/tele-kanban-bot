#!/usr/bin/env python3
"""
Test Proxy Connection
Kiểm tra kết nối proxy đến Telegram API
"""

import requests
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_proxy_connection():
    """Test kết nối proxy"""
    try:
        from src.config import settings
        
        print("🔍 Kiểm tra cấu hình proxy...")
        
        if not hasattr(settings, 'PROXY_ENABLED') or not settings.PROXY_ENABLED:
            print("❌ Proxy chưa được bật trong settings.py")
            return False
        
        print(f"✅ Proxy được bật: {settings.PROXY_URL}")
        
        # Test kết nối đến Telegram API
        test_url = "https://api.telegram.org/bot123/getMe"
        
        print(f"🌐 Test kết nối đến: {test_url}")
        print(f"🔗 Sử dụng proxy: {settings.PROXY_URL}")
        
        # Test với proxy
        response = requests.get(
            test_url, 
            proxies=settings.PROXY_DICT, 
            timeout=30
        )
        
        print(f"✅ Kết nối thành công! Status: {response.status_code}")
        print(f"📝 Response: {response.text[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi kết nối proxy: {e}")
        return False

def test_telegram_bot_token():
    """Test bot token với proxy"""
    try:
        from src.config import settings
        
        if not hasattr(settings, 'BOT_TOKEN') or not settings.BOT_TOKEN:
            print("❌ Chưa có BOT_TOKEN trong settings.py")
            return False
        
        print(f"🤖 Test bot token: {settings.BOT_TOKEN[:10]}...")
        
        # Test với bot token thật
        test_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getMe"
        
        print(f"🌐 Test kết nối bot đến: {test_url}")
        print(f"🔗 Sử dụng proxy: {settings.PROXY_URL}")
        
        response = requests.get(
            test_url, 
            proxies=settings.PROXY_DICT, 
            timeout=30
        )
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get('ok'):
                print(f"✅ Bot kết nối thành công!")
                print(f"🤖 Bot name: {bot_info['result']['first_name']}")
                print(f"👤 Username: @{bot_info['result']['username']}")
                return True
            else:
                print(f"❌ Bot API error: {bot_info}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi test bot token: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test Proxy Connection cho Tele Kanban Bot")
    print("=" * 50)
    
    # Test 1: Kết nối proxy cơ bản
    print("\n1️⃣ Test kết nối proxy cơ bản...")
    proxy_ok = test_proxy_connection()
    
    if proxy_ok:
        # Test 2: Bot token với proxy
        print("\n2️⃣ Test bot token với proxy...")
        bot_ok = test_telegram_bot_token()
        
        if bot_ok:
            print("\n🎉 Tất cả test đều thành công! Proxy hoạt động tốt.")
            print("✅ Bạn có thể chạy bot và dashboard với proxy.")
        else:
            print("\n⚠️  Proxy hoạt động nhưng bot token có vấn đề.")
            print("🔧 Kiểm tra lại BOT_TOKEN trong settings.py")
    else:
        print("\n❌ Proxy không hoạt động.")
        print("🔧 Kiểm tra lại cấu hình proxy trong settings.py")
        print("🌐 Đảm bảo proxy server 192.168.10.12:9999 đang hoạt động")
