#!/usr/bin/env python3
"""
Script monitor chi phí Railway deployment
"""

import os
import time
import requests
import psutil
from datetime import datetime

class RailwayCostMonitor:
    def __init__(self):
        self.start_time = time.time()
        
    def get_resource_usage(self):
        """Lấy thông tin resource usage hiện tại"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_percent': cpu_percent,
            'memory_used_mb': memory.used / (1024 * 1024),
            'memory_percent': memory.percent,
            'disk_used_gb': disk.used / (1024 * 1024 * 1024),
            'uptime_hours': (time.time() - self.start_time) / 3600
        }
    
    def estimate_monthly_cost(self, usage):
        """Ước tính chi phí hàng tháng"""
        # Railway pricing
        cpu_cost_per_hour = 10 / (30 * 24)  # $10/vCPU/month
        memory_cost_per_hour = 10 / (30 * 24)  # $10/GB/month
        
        # Tính chi phí dựa trên usage
        cpu_cost = (usage['cpu_percent'] / 100) * cpu_cost_per_hour * 24 * 30
        memory_cost = (usage['memory_used_mb'] / 1024) * memory_cost_per_hour * 24 * 30
        
        total_cost = cpu_cost + memory_cost
        
        return {
            'cpu_cost_monthly': cpu_cost,
            'memory_cost_monthly': memory_cost,
            'total_monthly': total_cost,
            'within_free_tier': total_cost <= 5.0
        }
    
    def print_report(self):
        """In báo cáo chi phí"""
        usage = self.get_resource_usage()
        cost = self.estimate_monthly_cost(usage)
        
        print("\n" + "="*50)
        print("🚀 RAILWAY COST MONITOR")
        print("="*50)
        
        print(f"📊 Resource Usage:")
        print(f"   CPU: {usage['cpu_percent']:.1f}%")
        print(f"   Memory: {usage['memory_used_mb']:.1f}MB ({usage['memory_percent']:.1f}%)")
        print(f"   Disk: {usage['disk_used_gb']:.2f}GB")
        print(f"   Uptime: {usage['uptime_hours']:.1f} hours")
        
        print(f"\n💰 Estimated Monthly Cost:")
        print(f"   CPU: ${cost['cpu_cost_monthly']:.2f}")
        print(f"   Memory: ${cost['memory_cost_monthly']:.2f}")
        print(f"   Total: ${cost['total_monthly']:.2f}")
        
        if cost['within_free_tier']:
            print(f"   ✅ Within $5 free tier!")
        else:
            print(f"   ⚠️  Exceeds free tier by ${cost['total_monthly'] - 5:.2f}")
            
        print(f"\n📈 Recommendations:")
        if usage['cpu_percent'] > 50:
            print("   - Consider optimizing CPU usage")
        if usage['memory_used_mb'] > 400:
            print("   - Consider reducing memory usage")
        if not cost['within_free_tier']:
            print("   - Consider splitting services or optimizing")
            
    def log_usage(self):
        """Log usage to file for tracking"""
        usage = self.get_resource_usage()
        timestamp = datetime.now().isoformat()
        
        log_entry = f"{timestamp},{usage['cpu_percent']},{usage['memory_used_mb']},{usage['uptime_hours']}\n"
        
        with open('railway_usage.log', 'a') as f:
            f.write(log_entry)

if __name__ == "__main__":
    monitor = RailwayCostMonitor()
    monitor.print_report()
    monitor.log_usage()
