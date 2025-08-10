#!/usr/bin/env python3
"""
Startup script cho Railway
Đảm bảo service khởi động đúng và health check hoạt động
"""

import os
import sys
import time

def main():
    print("🚀 Khởi động Tele Kanban Bot...")
    print(f"🌍 Environment: {os.getenv('RAILWAY_ENVIRONMENT', 'Development')}")
    print(f"🔧 PORT: {os.getenv('PORT', '5000')}")
    
    # Import và chạy dashboard
    try:
        from src.web.dashboard import app
        
        port = int(os.getenv('PORT', 5000))
        host = '0.0.0.0'
        
        print(f"✅ Dashboard khởi động thành công trên {host}:{port}")
        print("🔄 Service đang chạy...")
        
        app.run(host=host, port=port, debug=False, threaded=True)
        
    except Exception as e:
        print(f"❌ Lỗi khởi động: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
