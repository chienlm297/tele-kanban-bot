import os
from pathlib import Path

# Production configuration for cloud deployment

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
MY_USER_ID = int(os.getenv('MY_USER_ID', '0'))
MY_USERNAME = os.getenv('MY_USERNAME', '')

# Web configuration  
WEB_PORT = int(os.getenv('PORT', '5000'))  # Railway/Heroku use PORT env var
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Database configuration
DB_PATH = os.getenv('DB_PATH', 'tasks.db')

# Ensure database directory exists
Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

# Validate required environment variables (only warn, don't crash)
if not BOT_TOKEN:
    print("⚠️  Warning: BOT_TOKEN environment variable is not set")
    BOT_TOKEN = "dummy_token_for_health_check"
if not MY_USER_ID:
    print("⚠️  Warning: MY_USER_ID environment variable is not set")
    MY_USER_ID = 0
if not MY_USERNAME:
    print("⚠️  Warning: MY_USERNAME environment variable is not set")
    MY_USERNAME = "dummy_user"

# Cost optimization settings
ENABLE_COST_MONITORING = os.getenv('ENABLE_COST_MONITORING', 'True').lower() == 'true'
AUTO_CLEANUP_DAYS = int(os.getenv('AUTO_CLEANUP_DAYS', '30'))  # Cleanup old data
REDUCE_LOGGING = os.getenv('REDUCE_LOGGING', 'True').lower() == 'true'

# Performance optimizations
MAX_TASKS_PER_REQUEST = int(os.getenv('MAX_TASKS_PER_REQUEST', '100'))
CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', '300'))  # 5 minutes

if not REDUCE_LOGGING:
    print(f"✅ Production config loaded:")
    print(f"   - Bot token: {'*' * 20}...")
    print(f"   - User ID: {MY_USER_ID}")
    print(f"   - Username: {MY_USERNAME}")
    print(f"   - Web port: {WEB_PORT}")
    print(f"   - Database: {DB_PATH}")
    print(f"   - Cost monitoring: {ENABLE_COST_MONITORING}")
    print(f"   - Auto cleanup: {AUTO_CLEANUP_DAYS} days")
