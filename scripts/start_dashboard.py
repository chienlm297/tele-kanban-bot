#!/usr/bin/env python3
"""
Script chạy web dashboard đơn giản
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
    print("🌐 Khởi động Web Dashboard...")
    
    if not check_config():
        sys.exit(1)
    
    try:
        from src.config import settings
        from src.web.dashboard import app
        
        print(f"✅ Dashboard đang chạy tại: http://localhost:{settings.WEB_PORT}")
        print("🔄 Tự động refresh mỗi 30 giây")
        print("⏹️  Nhấn Ctrl+C để dừng")
        
        app.run(host='0.0.0.0', port=settings.WEB_PORT, debug=False)
        
    except ImportError as e:
        print(f"❌ Lỗi import: {e}")
        print("📦 Hãy cài đặt dependencies:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Lỗi khởi động dashboard: {e}")

if __name__ == "__main__":
    main()
