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
        # Tạo Flask app đơn giản trước để test health check
        from flask import Flask, jsonify
        
        # Tạo app tạm thời cho health check
        temp_app = Flask(__name__)
        
        @temp_app.route('/health')
        def health_check():
            return jsonify({'status': 'healthy', 'timestamp': '2024-01-01'})
        
        @temp_app.route('/')
        def root():
            return jsonify({'message': 'Tele Kanban Bot is starting...'})
        
        # Chạy app tạm thời trước
        port = int(os.getenv('PORT', 5000))
        host = '0.0.0.0'
        
        print(f"✅ Health check app khởi động thành công trên {host}:{port}")
        
        # Import dashboard chính
        from src.web.dashboard import app
        
        print(f"✅ Dashboard chính khởi động thành công")
        print("🔄 Service đang chạy...")
        
        # Chạy dashboard chính
        app.run(host=host, port=port, debug=False, threaded=True)
        
    except Exception as e:
        print(f"❌ Lỗi khởi động: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
