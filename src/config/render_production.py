"""
Cấu hình production cho Render.com
Tối ưu hóa để tránh lỗi Conflict khi deploy
"""

import os

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
MY_USER_ID = int(os.getenv('MY_USER_ID', 0))
MY_USERNAME = os.getenv('MY_USERNAME', '')

# Database configuration
DB_PATH = os.getenv('DB_PATH', 'kanban_tasks.db')

# Proxy configuration (nếu cần)
PROXY_ENABLED = os.getenv('PROXY_ENABLED', 'false').lower() == 'true'
PROXY_HOST = os.getenv('PROXY_HOST', '')
PROXY_PORT = os.getenv('PROXY_PORT', '')
PROXY_URL = f"http://{PROXY_HOST}:{PROXY_PORT}" if PROXY_HOST and PROXY_PORT else ''

# Render.com specific settings
RENDER_ENVIRONMENT = True
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')  # Nếu muốn sử dụng webhook mode

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Bot behavior settings
ENABLE_AI_ANALYSIS = os.getenv('ENABLE_AI_ANALYSIS', 'true').lower() == 'true'
MAX_TASKS_DISPLAY = int(os.getenv('MAX_TASKS_DISPLAY', '50'))
TASK_TEXT_MAX_LENGTH = int(os.getenv('TASK_TEXT_MAX_LENGTH', '100'))

# Timeout settings (để tránh conflict)
POLLING_TIMEOUT = int(os.getenv('POLLING_TIMEOUT', '30'))
CONNECTION_TIMEOUT = int(os.getenv('CONNECTION_TIMEOUT', '30'))
