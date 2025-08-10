#!/usr/bin/env python3
"""
Simple Flask app for Railway health check
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint cho Railway"""
    return jsonify({
        'status': 'healthy', 
        'timestamp': '2024-01-01',
        'environment': os.getenv('RAILWAY_ENVIRONMENT', 'development'),
        'port': os.getenv('PORT', '5000')
    })

@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Tele Kanban Bot is running!',
        'health_check': '/health',
        'environment': os.getenv('RAILWAY_ENVIRONMENT', 'development')
    })

@app.route('/api/stats')
def api_stats():
    """Simple stats endpoint"""
    try:
        # Thử import và chạy dashboard chính
        from src.web.dashboard import app as main_app
        from src.database.models import TaskDatabase
        from src.config import settings
        
        # Tạo database instance
        db = TaskDatabase(settings.DB_PATH)
        stats = db.get_stats()
        
        return jsonify(stats)
        
    except Exception as e:
        print(f"⚠️  Dashboard chính chưa sẵn sàng: {e}")
        return jsonify({
            'total': 0,
            'pending': 0,
            'completed': 0,
            'status': 'service_starting',
            'message': 'Dashboard chính đang khởi động...'
        })

@app.route('/dashboard')
def dashboard():
    """Test dashboard chính"""
    try:
        from src.web.dashboard import dashboard as main_dashboard
        return main_dashboard()
    except Exception as e:
        return jsonify({
            'error': 'Dashboard chính chưa sẵn sàng',
            'details': str(e)
        }), 503

if __name__ == '__main__':
    try:
        port = int(os.getenv('PORT', 5000))
        host = '0.0.0.0'
        
        print(f"🚀 Khởi động simple app trên {host}:{port}")
        print(f"🌍 Environment: {os.getenv('RAILWAY_ENVIRONMENT', 'development')}")
        print(f"🔧 PORT: {port}")
        
        app.run(host=host, port=port, debug=False, threaded=True)
        
    except Exception as e:
        print(f"❌ Lỗi khởi động app: {e}")
        import traceback
        traceback.print_exc()
        # Fallback: chạy trên port mặc định
        try:
            print("🔄 Thử chạy trên port 5000...")
            app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
        except Exception as e2:
            print(f"❌ Lỗi fallback: {e2}")
            import sys
            sys.exit(1)
