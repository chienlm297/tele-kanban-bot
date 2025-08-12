#!/usr/bin/env python3
"""
Script test để kiểm tra import có hoạt động không
"""

import os
import sys
from pathlib import Path

print("🧪 Testing imports...")

# Thêm src vào Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

print(f"📁 Added path: {src_path}")
print(f"📁 Python path: {sys.path[:3]}")
print(f"📁 Current working directory: {os.getcwd()}")

# Test import database
try:
    from database.models import TaskDatabase
    print("✅ Database import OK")
except ImportError as e:
    print(f"❌ Database import failed: {e}")

# Test import AI
try:
    from ai.analyzer import TaskAIAnalyzer
    print("✅ AI import OK")
except ImportError as e:
    print(f"❌ AI import failed: {e}")

# Test import web
try:
    from web.dashboard import app
    print("✅ Web dashboard import OK")
except ImportError as e:
    print(f"❌ Web dashboard import failed: {e}")

# Test import bot
try:
    from bot.telegram_handler import TelegramKanbanBot
    print("✅ Bot import OK")
except ImportError as e:
    print(f"❌ Bot import failed: {e}")

print("🏁 Import test completed!")
