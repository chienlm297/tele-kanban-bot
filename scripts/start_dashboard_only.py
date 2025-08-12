#!/usr/bin/env python3
"""
Script chạy chỉ web dashboard
Tách biệt với bot để tránh conflict
"""

import os
import sys
import logging
from pathlib import Path

# Thiết lập logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Chạy chỉ web dashboard"""
    try:
        logger.info("🌐 Khởi động Web Dashboard...")
        
        # Thêm src vào Python path
        src_path = Path(__file__).parent.parent / "src"
        sys.path.insert(0, str(src_path))
        
        # Import dashboard
        from web.dashboard import app
        
        # Lấy port từ environment
        port = int(os.getenv('PORT', 10000))
        host = '0.0.0.0'
        
        logger.info(f"✅ Dashboard: http://{host}:{port}")
        logger.info(f"🌐 Environment: Production (Render.com)")
        
        # Chạy dashboard
        app.run(host=host, port=port, debug=False, threaded=True)
        
    except Exception as e:
        logger.error(f"❌ Lỗi chạy dashboard: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
