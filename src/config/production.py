"""
Production Configuration for Render Deployment
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
BOT_TOKEN = TELEGRAM_BOT_TOKEN  # Alias for compatibility
if not TELEGRAM_BOT_TOKEN:
    print("⚠️  Warning: TELEGRAM_BOT_TOKEN environment variable is not set!")

# Web Configuration
WEB_PORT = int(os.getenv('PORT', 10000))
WEB_HOST = '0.0.0.0'

# Database Configuration
DATABASE_PATH = os.getenv('DATABASE_PATH', 'tasks.db')
DB_PATH = DATABASE_PATH  # Alias for compatibility

# Bot Configuration
MY_USER_ID = int(os.getenv('MY_USER_ID', 0))  # Set your Telegram user ID
MY_USERNAME = os.getenv('MY_USERNAME', '')  # Your Telegram username

# Proxy Configuration (Optional for production)
PROXY_ENABLED = os.getenv('PROXY_ENABLED', 'false').lower() == 'true'

if PROXY_ENABLED:
    PROXY_HOST = os.getenv('PROXY_HOST')
    PROXY_PORT = int(os.getenv('PROXY_PORT', 8080))
    PROXY_USERNAME = os.getenv('PROXY_USERNAME')
    PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
    
    if PROXY_USERNAME and PROXY_PASSWORD:
        PROXY_URL = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
    else:
        PROXY_URL = f"http://{PROXY_HOST}:{PROXY_PORT}"
    
    PROXY_DICT = {
        'http': PROXY_URL,
        'https': PROXY_URL
    }
else:
    PROXY_URL = None
    PROXY_DICT = None

print(f"🌍 Production Environment Loaded")
print(f"📡 Bot Token: {'✅ Set' if TELEGRAM_BOT_TOKEN else '❌ Missing'}")
print(f"🌐 Web Port: {WEB_PORT}")
print(f"🗄️  Database: {DATABASE_PATH}")
print(f"🔗 Proxy: {'✅ Enabled' if PROXY_ENABLED else '❌ Disabled'}")
