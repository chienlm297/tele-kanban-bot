#!/usr/bin/env python3
"""
Test script để kiểm tra tất cả các import
Chạy: python test_imports.py
"""

import sys
import os

# Add src to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)
sys.path.insert(0, current_dir)

def test_imports():
    """Test tất cả các import cần thiết"""
    print("🧪 Testing imports...")
    
    try:
        # Test config imports
        print("📁 Testing config imports...")
        from config import settings
        print("✅ config.settings imported successfully")
        
        # Test database imports
        print("🗄️ Testing database imports...")
        from database.models import TaskDatabase
        print("✅ database.models imported successfully")
        
        # Test AI imports
        print("🤖 Testing AI imports...")
        from ai.analyzer import TaskAIAnalyzer
        print("✅ ai.analyzer imported successfully")
        
        # Test bot imports
        print("📱 Testing bot imports...")
        from bot.telegram_handler import TelegramKanbanBot
        print("✅ bot.telegram_handler imported successfully")
        
        # Test web imports
        print("🌐 Testing web imports...")
        from web.dashboard import app
        print("✅ web.dashboard imported successfully")
        
        print("\n🎉 Tất cả imports đều thành công!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_config_loading():
    """Test việc load config"""
    print("\n🔧 Testing config loading...")
    
    try:
        # Test production config
        os.environ['RENDER'] = 'true'
        from config import production
        print("✅ production config loaded successfully")
        
        # Test render_production config
        from config import render_production
        print("✅ render_production config loaded successfully")
        
        # Test settings config
        from config import settings
        print("✅ settings config loaded successfully")
        
        print("🎉 Tất cả config đều load thành công!")
        return True
        
    except Exception as e:
        print(f"❌ Config loading error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting import tests...\n")
    
    # Test basic imports
    imports_ok = test_imports()
    
    # Test config loading
    config_ok = test_config_loading()
    
    if imports_ok and config_ok:
        print("\n🎉 Tất cả tests đều PASSED!")
        print("✅ Bạn có thể deploy lên Render.com")
    else:
        print("\n❌ Một số tests FAILED!")
        print("🔧 Hãy kiểm tra lại các import paths")
