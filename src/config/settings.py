# Cấu hình bot - Copy file này thành config.py và điền thông tin

# Telegram Bot Token - Lấy từ @BotFather
# BOT_TOKEN = "8347011918:AAEAPUWLaBXf_B17FT6KUkfd_e3Mtd2t0Dk"
BOT_TOKEN = "7825713030:AAHk0FWzUB187nNN8-rbNkLjO719bDpzL1Y"
# User ID của bạn (để bot biết ai là chủ)
MY_USER_ID = 2084719052  # Thay bằng user ID thật của bạn

# Username Telegram của bạn (không có @)
MY_USERNAME = "chienlm2"  # THAY BẰNG USERNAME THẬT CỦA BẠN

# Port cho web dashboard
WEB_PORT = 5000

# Database path
DB_PATH = "tasks.db"

# Cấu hình Proxy Server (bắt buộc ở môi trường công ty)
PROXY_ENABLED = True
PROXY_HOST = "192.168.10.12"
PROXY_PORT = 9999
PROXY_USERNAME = ""  # Nếu proxy cần authentication
PROXY_PASSWORD = ""  # Nếu proxy cần authentication

# Cấu hình HTTP/HTTPS proxy cho requests
PROXY_URL = f"http://{PROXY_HOST}:{PROXY_PORT}"
PROXY_DICT = {
    'http': PROXY_URL,
    'https': PROXY_URL
}
