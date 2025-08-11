# 🚀 Deploy Tele Kanban Bot lên Render

Hướng dẫn chi tiết để deploy project lên Render.com với 2 services: Web Dashboard và Telegram Bot Worker.

## 📋 Yêu cầu trước khi deploy

1. **Tài khoản Render**: Đăng ký tại [render.com](https://render.com)
2. **Repository GitHub**: Push code lên GitHub repository
3. **Telegram Bot Token**: Lấy từ [@BotFather](https://t.me/BotFather)
4. **Telegram User ID**: Lấy từ [@userinfobot](https://t.me/userinfobot)

### Lấy thông tin cần thiết:

**Telegram Bot Token:**
1. Nhắn tin cho [@BotFather](https://t.me/BotFather)
2. Gửi `/newbot` và làm theo hướng dẫn
3. Copy token có dạng: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

**Telegram User ID:**
1. Nhắn tin cho [@userinfobot](https://t.me/userinfobot)
2. Bot sẽ trả về User ID của bạn (dạng số: `123456789`)

**Tham khảo file `env_example` để biết các biến environment cần thiết.**

## 🛠️ Bước 1: Chuẩn bị Repository

```bash
# 1. Add và commit tất cả files
git add .
git commit -m "Add Render deployment configuration"

# 2. Push lên GitHub
git push origin main
```

## 🌐 Bước 2: Deploy Web Service

1. **Tạo Web Service**:
   - Vào Render Dashboard → **New** → **Web Service**
   - Connect repository GitHub của bạn
   - Chọn branch `main`

2. **Cấu hình Web Service**:
   - **Name**: `tele-kanban-web`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py --mode web`
   - **Plan**: Free (hoặc Starter nếu cần)

3. **Environment Variables**:
   ```
   RENDER=true
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   MY_USER_ID=your_telegram_user_id
   PORT=10000
   ```

4. **Advanced Settings**:
   - **Auto-Deploy**: Yes
   - **Health Check Path**: `/api/stats`

## 🤖 Bước 3: Deploy Bot Worker

1. **Tạo Background Worker**:
   - Vào Render Dashboard → **New** → **Background Worker**
   - Connect cùng repository GitHub
   - Chọn branch `main`

2. **Cấu hình Worker**:
   - **Name**: `tele-kanban-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py --mode bot`
   - **Plan**: Free

3. **Environment Variables**:
   ```
   RENDER=true
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   MY_USER_ID=your_telegram_user_id
   ```

## 🔧 Bước 4: Cấu hình Environment Variables

### Bắt buộc:
- `RENDER=true` - Để nhận biết môi trường production
- `TELEGRAM_BOT_TOKEN` - Token bot từ BotFather
- `MY_USER_ID` - Telegram User ID của bạn

### Tùy chọn:
- `DATABASE_PATH=tasks.db` - Đường dẫn database (mặc định: tasks.db)
- `PROXY_ENABLED=false` - Bật/tắt proxy (mặc định: false)
- `PROXY_HOST` - Proxy host (nếu cần)
- `PROXY_PORT` - Proxy port (nếu cần)
- `PROXY_USERNAME` - Proxy username (nếu cần)
- `PROXY_PASSWORD` - Proxy password (nếu cần)

## 🎯 Bước 5: Verify Deployment

1. **Kiểm tra Web Service**:
   - Truy cập URL được cung cấp bởi Render
   - Kiểm tra dashboard hoạt động bình thường

2. **Kiểm tra Bot Worker**:
   - Vào Logs của Worker service
   - Tìm thông báo "✅ Bot đã khởi động thành công"
   - Test bot bằng cách tag trong Telegram

3. **Test tích hợp**:
   - Tạo task mới qua Telegram
   - Kiểm tra task xuất hiện trong web dashboard
   - Hoàn thành task từ dashboard và kiểm tra bot reply

## 📊 Monitoring & Logs

### Web Service Logs:
```bash
# Truy cập logs qua Render Dashboard
# Hoặc sử dụng Render CLI
render logs -s tele-kanban-web
```

### Bot Worker Logs:
```bash
# Truy cập logs qua Render Dashboard
# Hoặc sử dụng Render CLI
render logs -s tele-kanban-bot
```

## 🔄 Auto-Deploy

Khi bạn push code mới lên GitHub:
1. Render sẽ tự động detect changes
2. Rebuild và redeploy cả 2 services
3. Zero-downtime deployment

## 🆓 Render Free Plan Limitations

- **Web Service**: 750 giờ/tháng, sleep sau 15 phút không hoạt động
- **Background Worker**: 750 giờ/tháng
- **Database**: Ephemeral (mất data khi restart)

### Giải pháp cho Database:
1. **Upgrade lên Paid Plan**: $7/tháng cho persistent storage
2. **Sử dụng External Database**: PostgreSQL, MySQL từ các provider khác
3. **Backup định kỳ**: Export data về local

## 🔧 Troubleshooting

### Bot không hoạt động:
```bash
# Kiểm tra logs worker
# Thường do:
# 1. TELEGRAM_BOT_TOKEN sai
# 2. MY_USER_ID sai
# 3. Network issues
```

### Web dashboard không load:
```bash
# Kiểm tra logs web service
# Thường do:
# 1. Port configuration sai
# 2. Build command failed
# 3. Dependencies missing
```

### Database issues:
```bash
# Free plan database sẽ reset khi service restart
# Cân nhắc upgrade hoặc sử dụng external database
```

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra logs trên Render Dashboard
2. Verify environment variables
3. Test local trước khi deploy
4. Check Render status page: [status.render.com](https://status.render.com)

## 🎉 Hoàn thành!

Sau khi hoàn thành các bước trên, bạn sẽ có:
- ✅ Web Dashboard chạy 24/7 trên Render
- ✅ Telegram Bot Worker chạy liên tục
- ✅ Auto-deploy khi push code mới
- ✅ Free hosting (với limitations)

**URL Dashboard**: https://your-service-name.onrender.com
**Bot**: Hoạt động trực tiếp trong Telegram
