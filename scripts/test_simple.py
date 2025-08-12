#!/usr/bin/env python3
"""
Script test đơn giản để kiểm tra import
"""

import os
import sys
from pathlib import Path

print("🧪 Testing simple imports...")

# Thêm cả hai paths
src_path = Path(__file__).parent.parent / "src"
parent_path = Path(__file__).parent.parent

sys.path.insert(0, str(src_path))
sys.path.insert(0, str(parent_path))

print(f"📁 Added src path: {src_path}")
print(f"📁 Added parent path: {parent_path}")
print(f"📁 Current working directory: {os.getcwd()}")
print(f"📁 Python path: {sys.path[:3]}")

# Test import database
try:
    from database.models import TaskDatabase
    print("✅ Database import OK (relative)")
except ImportError as e:
    print(f"❌ Database import failed (relative): {e}")
    try:
        from src.database.models import TaskDatabase
        print("✅ Database import OK (absolute)")
    except ImportError as e2:
        print(f"❌ Database import failed (absolute): {e2}")

# Test import web
try:
    from web.dashboard import app
    print("✅ Web dashboard import OK (relative)")
except ImportError as e:
    print(f"❌ Web dashboard import failed (relative): {e}")
    try:
        from src.web.dashboard import app
        print("✅ Web dashboard import OK (absolute)")
    except ImportError as e2:
        print(f"❌ Web dashboard import failed (absolute): {e2}")

print("🏁 Import test completed!")
