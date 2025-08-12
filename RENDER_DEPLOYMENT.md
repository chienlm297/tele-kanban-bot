# 🚀 Hướng dẫn Deploy Kanban Bot trên Render.com

## 🔍 **Nguyên nhân gây lỗi Conflict**

Lỗi `telegram.error.Conflict: Conflict: terminated by other getUpdates request` xảy ra khi:

1. **Nhiều instance bot chạy cùng lúc** - Render.com có thể restart service nhiều lần
2. **Polling mode conflict** - Khi bot restart, nó vẫn giữ connection cũ
3. **Thiếu graceful shutdown** - Bot không dừng polling một cách an toàn
4. **drop_pending_updates=True** - Gây conflict khi có nhiều instance

## 🛠️ **Giải pháp đã áp dụng**

### **1. Cải thiện Telegram Handler**
- ✅ Thêm graceful shutdown với signal handlers
- ✅ Sử dụng `drop_pending_updates=False` trên Render.com
- ✅ Thêm timeout settings để tránh conflict
- ✅ Hỗ trợ webhook mode (khuyến nghị cho production)

### **2. Cấu hình đặc biệt cho Render.com**
- ✅ File `render_production.py` với settings tối ưu
- ✅ Script khởi động `start_bot_render.py` 
- ✅ Environment variables được cấu hình đúng

### **3. Cải thiện error handling**
- ✅ Fallback mechanism khi webhook thất bại
- ✅ Restart tự động trên Render.com
- ✅ Logging chi tiết để debug

## 📋 **Environment Variables cần thiết**

Trong Render.com dashboard, thêm các variables sau:

```bash
# Bắt buộc
BOT_TOKEN=your_bot_token_here
MY_USER_ID=your_telegram_user_id
MY_USERNAME=your_telegram_username

# Tùy chọn
DB_PATH=kanban_tasks.db
LOG_LEVEL=INFO
POLLING_TIMEOUT=30
CONNECTION_TIMEOUT=30

# Nếu muốn sử dụng webhook mode
WEBHOOK_URL=https://your-app-name.onrender.com/webhook

# Nếu cần proxy
PROXY_ENABLED=false
PROXY_HOST=
PROXY_PORT=
```

## 🚀 **Cách Deploy**

### **Bước 1: Push code lên GitHub**
```bash
git add .
git commit -m "Fix Conflict error for Render.com deployment"
git push origin main
```

### **Bước 2: Cấu hình Render.com**
1. Tạo new Web Service
2. Connect với GitHub repository
3. Sử dụng `python scripts/start_bot_render.py` làm start command
4. Thêm environment variables

### **Bước 3: Deploy**
- Render.com sẽ tự động build và deploy
- Bot sẽ khởi động với cấu hình tối ưu cho production

## 🔧 **Troubleshooting**

### **Nếu vẫn gặp lỗi Conflict:**

1. **Kiểm tra logs** trong Render.com dashboard
2. **Đảm bảo chỉ có 1 service** đang chạy
3. **Restart service** nếu cần thiết
4. **Kiểm tra BOT_TOKEN** có đúng không

### **Nếu bot không hoạt động:**

1. **Kiểm tra environment variables** đã đầy đủ chưa
2. **Xem logs** để tìm lỗi cụ thể
3. **Kiểm tra BOT_TOKEN** có hợp lệ không
4. **Đảm bảo bot chưa bị block** bởi Telegram

## 📊 **Monitoring**

### **Logs quan trọng cần theo dõi:**
- `🚀 Khởi động Kanban Bot trên Render.com...`
- `✅ Bot đã khởi động thành công`
- `🌐 Không sử dụng proxy` hoặc `🌐 Sử dụng proxy: ...`
- `🚀 Chạy trên Render.com - sử dụng cấu hình polling production`

### **Nếu thấy lỗi:**
- `❌ Lỗi khởi động bot: ...`
- `❌ Lỗi khi chạy webhook mode: ...`
- `🔄 Fallback về polling mode...`

## 💡 **Tips để tránh lỗi**

1. **Luôn sử dụng script `start_bot_render.py`** thay vì `main.py`
2. **Không thay đổi BOT_TOKEN** khi bot đang chạy
3. **Sử dụng webhook mode** nếu có thể (ổn định hơn polling)
4. **Monitor logs** thường xuyên để phát hiện vấn đề sớm
5. **Không deploy nhiều lần** trong thời gian ngắn

## 🔄 **Restart Service**

Nếu cần restart service:

1. Vào Render.com dashboard
2. Chọn service `tele-kanban-bot`
3. Click "Manual Deploy" → "Deploy latest commit"
4. Hoặc click "Suspend" rồi "Resume"

---

**Lưu ý:** Sau khi deploy thành công, bot sẽ hoạt động ổn định và không còn gặp lỗi Conflict nữa! 🎉
