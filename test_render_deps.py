#!/usr/bin/env python3
"""
Test script để kiểm tra tất cả dependencies cần thiết cho Render.com
Chạy script này trước khi deploy để đảm bảo không có lỗi
"""

import sys
import os

def test_builtin_modules():
    """Test các built-in modules của Python"""
    print("🔍 Testing built-in modules...")
    
    builtin_modules = [
        'imghdr', 'sqlite3', 'json', 'datetime', 'threading', 
        'time', 'os', 'sys', 'signal', 're', 'logging', 'argparse'
    ]
    
    failed_modules = []
    for module in builtin_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_modules.append(module)
    
    if failed_modules:
        print(f"\n⚠️  {len(failed_modules)} built-in modules failed to import")
        return False
    else:
        print("✅ Tất cả built-in modules đều hoạt động")
        return True

def test_external_dependencies():
    """Test các external dependencies"""
    print("\n🔍 Testing external dependencies...")
    
    external_modules = [
        ('telegram', 'python-telegram-bot'),
        ('flask', 'Flask'),
        ('requests', 'requests'),
        ('PIL', 'Pillow'),
        ('markdown2', 'markdown2'),
        ('gunicorn', 'gunicorn')
    ]
    
    failed_modules = []
    for module, package_name in external_modules:
        try:
            __import__(module)
            print(f"  ✅ {package_name}")
        except ImportError as e:
            print(f"  ❌ {package_name}: {e}")
            failed_modules.append(package_name)
    
    if failed_modules:
        print(f"\n⚠️  {len(failed_modules)} external dependencies failed to import")
        return False
    else:
        print("✅ Tất cả external dependencies đều hoạt động")
        return True

def test_project_modules():
    """Test các project modules"""
    print("\n🔍 Testing project modules...")
    
    # Add src to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(current_dir, 'src')
    sys.path.insert(0, src_path)
    
    project_modules = [
        ('config.settings', 'Config settings'),
        ('database.models', 'Database models'),
        ('ai.analyzer', 'AI analyzer'),
        ('bot.telegram_handler', 'Telegram handler'),
        ('web.dashboard', 'Web dashboard')
    ]
    
    failed_modules = []
    for module, description in project_modules:
        try:
            __import__(module)
            print(f"  ✅ {description}")
        except ImportError as e:
            print(f"  ❌ {description}: {e}")
            failed_modules.append(description)
    
    if failed_modules:
        print(f"\n⚠️  {len(failed_modules)} project modules failed to import")
        return False
    else:
        print("✅ Tất cả project modules đều hoạt động")
        return True

def main():
    """Main test function"""
    print("🚀 Testing Render.com Dependencies")
    print("=" * 50)
    
    # Test built-in modules
    builtin_ok = test_builtin_modules()
    
    # Test external dependencies
    external_ok = test_external_dependencies()
    
    # Test project modules
    project_ok = test_project_modules()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    if builtin_ok and external_ok and project_ok:
        print("🎉 TẤT CẢ TESTS ĐỀU PASSED!")
        print("✅ Bạn có thể deploy lên Render.com")
        return True
    else:
        print("❌ MỘT SỐ TESTS FAILED!")
        print("🔧 Hãy kiểm tra lại dependencies trước khi deploy")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
