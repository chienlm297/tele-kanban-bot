#!/usr/bin/env python3
"""
Test imports sau khi sửa lỗi path
"""

import sys
import os

def test_imports():
    """Test import các modules chính"""
    try:
        print("🔍 Testing imports...")
        
        # Add src to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_path = os.path.join(current_dir, 'src')
        sys.path.insert(0, src_path)
        sys.path.insert(0, current_dir)
        
        print(f"📁 Current directory: {current_dir}")
        print(f"📁 Src path: {src_path}")
        print(f"📁 Python path: {sys.path[:3]}")
        
        # Test AI analyzer
        print("\n📦 Testing AI analyzer...")
        from src.ai.analyzer import TaskAIAnalyzer
        print("✅ TaskAIAnalyzer imported successfully")
        
        # Test bot handler
        print("\n🤖 Testing bot handler...")
        from src.bot.telegram_handler import TelegramKanbanBot
        print("✅ TelegramKanbanBot imported successfully")
        
        # Test database models
        print("\n🗄️ Testing database models...")
        from src.database.models import TaskDatabase
        print("✅ TaskDatabase imported successfully")
        
        # Test web dashboard
        print("\n🌐 Testing web dashboard...")
        from src.web.dashboard import app
        print("✅ Flask app imported successfully")
        
        print("\n🎉 Tất cả imports đều thành công!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Tele Kanban Bot imports...")
    print("=" * 50)
    
    test_imports()
    
    print("\n" + "=" * 50)
    print("🏁 Import test completed!")
