#!/usr/bin/env python3
"""
Cron job để cleanup data cũ và optimize database
Chạy hàng ngày để tiết kiệm storage
"""

import sys
import os
import logging
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def cleanup_database():
    """Cleanup database để tiết kiệm storage"""
    try:
        # Import settings from config package
        from src.config import settings
            
        from src.database.optimized import OptimizedDatabase
        
        db = OptimizedDatabase(settings.DB_PATH)
        
        # Cleanup old completed tasks
        cleanup_days = getattr(settings, 'AUTO_CLEANUP_DAYS', 30)
        db.cleanup_old_data(cleanup_days)
        
        # Get stats
        db_size = db.get_db_size()
        
        print(f"✅ Database cleanup completed:")
        print(f"   - Cleaned tasks older than {cleanup_days} days")
        print(f"   - Current DB size: {db_size:.2f}MB")
        
        # Log cleanup
        timestamp = datetime.now().isoformat()
        with open('cleanup.log', 'a') as f:
            f.write(f"{timestamp},cleanup_completed,{db_size:.2f}MB\n")
            
    except Exception as e:
        logging.error(f"Cleanup failed: {e}")
        print(f"❌ Cleanup failed: {e}")

def check_resource_usage():
    """Check và báo cáo resource usage"""
    try:
        from scripts.monitor_costs import RailwayCostMonitor
        
        monitor = RailwayCostMonitor()
        usage = monitor.get_resource_usage()
        cost = monitor.estimate_monthly_cost(usage)
        
        # Log usage
        monitor.log_usage()
        
        # Warning nếu vượt free tier
        if not cost['within_free_tier']:
            print(f"⚠️  WARNING: Estimated cost ${cost['total_monthly']:.2f} exceeds free tier!")
            
    except Exception as e:
        logging.error(f"Resource monitoring failed: {e}")

if __name__ == "__main__":
    print(f"🔄 Starting daily cleanup - {datetime.now()}")
    
    cleanup_database()
    check_resource_usage()
    
    print(f"✅ Daily cleanup completed - {datetime.now()}")
