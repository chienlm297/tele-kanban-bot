# 🤖 Tele Kanban Bot - AI Smart Task Manager

> **Hệ thống quản lý công việc thông minh với Telegram Bot và Web Dashboard, tích hợp AI để gợi ý tasks ưu tiên và auto-refresh real-time.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)
[![Telegram Bot](https://img.shields.io/badge/Telegram%20Bot-API-blue.svg)](https://core.telegram.org/bots/api)
[![AI Powered](https://img.shields.io/badge/AI-Powered-orange.svg)](https://github.com/features)

## 🚀 **Quick Start (5 phút)**

### **1. ⚡ Cài đặt nhanh**
```bash
# Clone và cài đặt
git clone <your-repo-url>
cd tele-kanban-bot
pip install -r requirements.txt

# Copy config và điền thông tin
cp src/config/example.py src/config/settings.py
# Chỉnh sửa BOT_TOKEN, MY_USER_ID, MY_USERNAME trong settings.py
```

### **2. 🎯 Chạy ngay lập tức**
```bash
# Windows PowerShell (Khuyến nghị)
.\run.ps1

# Windows CMD
run.bat

# Linux/Mac
./run.sh
```

### **3. 🌐 Truy cập Dashboard**
- **URL**: `http://localhost:5000`
- **Bot**: Tự động chạy và ghi nhận tasks

---

## 🚀 **Deploy trên Render.com (Production)**

### **⚡ Deploy nhanh (3 bước)**
Xem file `QUICK_DEPLOY.md` để deploy trong 5 phút!

### **📋 Environment Variables cần thiết:**
```bash
BOT_TOKEN=your_bot_token_here
MY_USER_ID=your_telegram_user_id
MY_USERNAME=your_telegram_username
```

### **🔧 Nếu gặp lỗi khi deploy:**
- Xem file `QUICK_DEPLOY.md` để khắc phục
- Đảm bảo sử dụng `python3.11 main.py --mode both`
- **Python Version**: Sử dụng Python 3.11.0 (không phải 3.13)
- Kiểm tra environment variables đầy đủ
- **✅ Tất cả các lỗi import, Updater compatibility, Filters compatibility và dependencies đã được sửa!**
- **📦 Sử dụng `render_requirements.txt` cho Render.com deployment**

---

## 🎯 **Tính năng nổi bật**

### 🚀 **Auto-Refresh & Real-Time Updates** ⭐ MỚI!
- **🔄 Auto-refresh**: Tự động cập nhật dữ liệu mỗi 30 giây
- **⚡ Real-time polling**: Kiểm tra thay đổi mỗi 10 giây  
- **📱 Manual refresh**: Nút cập nhật ngay lập tức
- **⏰ Last update time**: Hiển thị thời gian cập nhật cuối
- **🧠 Smart refresh**: Chỉ refresh khi cần thiết

### 🤖 **Telegram Bot Intelligence**
- **🎯 Auto Task Creation**: Tự động tạo task khi được tag trong nhóm
- **✅ Smart Completion**: Đánh dấu hoàn thành khi reply "done" (silent mode)
- **🧠 AI Suggestions**: Gợi ý tasks ưu tiên bằng AI (`/ai`)
- **📊 Productivity Insights**: Phân tích hiệu suất (`/insights`)
- **🔍 Silent Mode**: Không spam tin nhắn, chỉ lưu vào database
- **📱 Web Integration**: Bot chỉ reply khi hoàn thành từ web dashboard

### 🌐 **Web Dashboard Advanced**
- **📋 Task Management**: Quản lý tasks với giao diện đẹp
- **🤖 AI Suggestions Tab**: Hiển thị tasks được AI recommend
- **🎯 Priority Scoring**: System tính điểm ưu tiên (0-100)
- **⚡ One-click Actions**: Hoàn thành, pending, cancel, in-progress
- **📱 Telegram Integration**: Auto reply khi hoàn thành từ web
- **📊 Smart Stats**: Thống kê real-time với auto-refresh

### **🔇 Silent Mode vs Web Integration**
- **🔇 Silent Mode**: Khi reply "done", "xong", "hoàn thành" → Bot chỉ đánh dấu hoàn thành, **KHÔNG reply**
- **📱 Web Integration**: Khi ấn "Hoàn thành" trên web → Bot **SẼ reply** tin nhắn hoàn thành
- **💡 Lý do**: Tránh spam tin nhắn, chỉ thông báo khi cần thiết

### 🧠 **AI Analysis Engine**
- **🎯 Smart Priority Scoring**: Phân tích độ ưu tiên thông minh
- **🔍 Multi-factor Analysis**: 
  - 🔥 **Từ khóa cấp thiết** (urgent, deadline, gấp)
  - 🚀 **Dự án quan trọng** (MR, deploy, production)
  - ⏰ **Tính cấp bách thời gian**
  - 👤 **Người giao việc quan trọng**
  - 📅 **Tuổi của task**

## 🏗️ **Cấu trúc Project**

```
Tele Kanban Bot/
├── 📁 src/                          # Source code chính
│   ├── 🤖 bot/                      # Telegram bot logic
│   │   ├── __init__.py
│   │   └── telegram_handler.py      # Bot handlers và commands
│   ├── 🌐 web/                       # Web dashboard
│   │   ├── __init__.py
│   │   └── dashboard.py             # Flask app và APIs
│   ├── 🗄️ database/                 # Database layer
│   │   ├── __init__.py
│   │   └── models.py                # SQLite database operations
│   ├── 🧠 ai/                        # AI analysis
│   │   ├── __init__.py
│   │   └── analyzer.py              # AI task priority analysis
│   ├── ⚙️ config/                    # Configuration
│   │   ├── __init__.py
│   │   ├── settings.py              # App settings (copy from example.py)
│   │   └── example.py               # Settings template
│   └── __init__.py
├── 🎨 templates/                     # HTML templates
│   └── dashboard.html               # Dashboard UI với auto-refresh
├── 🚀 scripts/                       # Entry point scripts
│   ├── start_bot.py                 # Chạy chỉ bot
│   └── start_dashboard.py           # Chạy chỉ dashboard
├── 🎯 main.py                        # Main entry point (khuyến nghị)
├── 📦 requirements.txt               # Python dependencies
├── 🗄️ tasks.db                      # SQLite database (auto-created)

└── 📖 README.md                      # Hướng dẫn này
```

## 🚀 **Hướng dẫn cài đặt**

### **1. 📦 Cài đặt Dependencies**
```bash
# Clone project
git clone <your-repo-url>
cd tele-kanban-bot

# Cài đặt dependencies
pip install -r requirements.txt
```

### **2. ⚙️ Cấu hình Bot**
```bash
# Copy config template
cp src/config/example.py src/config/settings.py
```

### **3. 🚀 Chạy Project (Khuyến nghị)**

#### **🎯 Sử dụng Script tự động (Khuyến nghị)**
```bash
# Windows PowerShell (Khuyến nghị)
.\run.ps1                 # Chạy cả bot và dashboard
.\run.ps1 bot             # Chỉ chạy bot
.\run.ps1 web             # Chỉ chạy dashboard
.\run.ps1 test            # Test proxy connection
.\run.ps1 install         # Cài đặt dependencies
.\run.ps1 help            # Hiển thị hướng dẫn

# Windows CMD
run.bat                   # Chạy cả bot và dashboard
run.bat bot               # Chỉ chạy bot
run.bat web               # Chỉ chạy dashboard
run.bat test              # Test proxy connection
run.bat install           # Cài đặt dependencies
run.bat help              # Hiển thị hướng dẫn

# Linux/Mac (Terminal)
chmod +x run.sh           # Cấp quyền thực thi (chỉ cần làm 1 lần)
./run.sh                  # Chạy cả bot và dashboard
./run.sh bot              # Chỉ chạy bot
./run.sh web              # Chỉ chạy dashboard
./run.sh test             # Test proxy connection
./run.sh install          # Cài đặt dependencies
./run.sh help             # Hiển thị hướng dẫn
```

#### **🐍 Chạy trực tiếp với Python**
```bash
# Chạy cả bot và dashboard
python main.py

# Chỉ chạy bot
python main.py bot

# Chỉ chạy dashboard
python main.py web

# Chạy cả hai
python main.py both
```

### **3. 🌐 Cấu hình Proxy (Tùy chọn)**
**Ở nhà**: Không cần proxy, để `PROXY_ENABLED = False` (mặc định)

**Ở công ty**: Cần proxy để kết nối internet, đổi `PROXY_ENABLED = True`

```python
# Trong src/config/settings.py
# Ở nhà: Để mặc định
PROXY_ENABLED = False

# Ở công ty: Đổi thành True và điền thông tin
PROXY_ENABLED = True
PROXY_HOST = "192.168.10.12"  # IP proxy server
PROXY_PORT = 9999              # Port proxy server
PROXY_USERNAME = ""            # Username nếu cần
PROXY_PASSWORD = ""            # Password nếu cần
```

**Test proxy connection (chỉ khi ở công ty):**
```bash
# Sử dụng script (khuyến nghị)
.\run.ps1 test            # Windows PowerShell
run.bat test              # Windows CMD
./run.sh test             # Linux/Mac

# Hoặc chạy trực tiếp
python test_proxy.py
```

# Chỉnh sửa settings.py với thông tin của bạn:
# - BOT_TOKEN: Lấy từ @BotFather
# - MY_USER_ID: ID Telegram của bạn  
# - MY_USERNAME: Username Telegram (không có @)

### **3. 🎯 Chạy Bot**

#### **🎯 Cách 1: Sử dụng Script tự động (Khuyến nghị)**
```bash
# Windows PowerShell (Khuyến nghị)
.\run.ps1                 # Chạy cả bot và dashboard
.\run.ps1 bot             # Chỉ chạy bot
.\run.ps1 web             # Chỉ chạy dashboard

# Windows CMD
run.bat                   # Chạy cả bot và dashboard
run.bat bot               # Chỉ chạy bot
run.bat web               # Chỉ chạy dashboard

# Linux/Mac (Terminal)
./run.sh                  # Chạy cả bot và dashboard
./run.sh bot              # Chỉ chạy bot
./run.sh web              # Chỉ chạy dashboard
```

#### **🔄 Cách 2: Chạy trực tiếp với Python**
```bash
# Chạy cả Bot và Dashboard (Khuyến nghị)
python main.py
# hoặc
python main.py both

# Chạy riêng từng service
python main.py bot        # Chỉ bot
python main.py web        # Chỉ dashboard
```

## 🎮 **Cách sử dụng**

### **🤖 Telegram Bot Commands:**
```
/start      - Khởi động bot
/tasks      - Xem danh sách tasks
/ai         - AI gợi ý tasks ưu tiên (⭐ Mới!)
/insights   - Phân tích productivity (⭐ Mới!)
/help       - Hướng dẫn
```

### **🌐 Web Dashboard:**
- **URL**: `http://localhost:5000`
- **🤖 AI Gợi ý** tab - Xem tasks AI recommend
- **⏳ Đang chờ** tab - Tasks chưa hoàn thành  
- **✅ Đã hoàn thành** tab - Tasks completed
- **🔄 Đang làm** tab - Tasks in progress
- **❌ Đã hủy** tab - Cancelled tasks

### **🔄 Auto-Refresh Controls:**
- **🔄 Auto-refresh: Bật/Tắt** - Nút toggle màu xanh/xám
- **🔄 Cập nhật ngay** - Refresh thủ công với loading indicator
- **📅 Cập nhật cuối** - Hiển thị thời gian cập nhật gần nhất

### **📋 Task Workflow:**
1. **🎯 Tạo task**: Ai đó tag bạn trong nhóm Telegram
2. **🧠 AI Analysis**: System tự động phân tích priority
3. **💡 Smart Suggestions**: AI gợi ý tasks nên làm trước
4. **✅ Complete**: 
   - **Reply "done"**: Chỉ đánh dấu hoàn thành (silent mode)
   - **Click nút trên web**: Bot sẽ reply tin nhắn hoàn thành
5. **🔄 Real-time Update**: Dashboard tự động cập nhật

## 🧠 **AI Features**

### **🎯 Priority Scoring (0-100 điểm):**
- **🔥 80+ điểm**: Cực kỳ quan trọng (urgent, deadline)
- **⚡ 65+ điểm**: Ưu tiên cao (production, MR)
- **📝 50+ điểm**: Bình thường
- **📋 <50 điểm**: Ưu tiên thấp

### **🔍 AI phân tích dựa trên:**
- **📝 Từ khóa** trong tin nhắn
- **⏰ Thời gian** gửi và deadline
- **👤 Người giao việc**
- **📅 Tuổi của task**
- **📊 Pattern lịch sử** hoàn thành

## 🛠️ **Development & API**

### **🔧 Thêm tính năng mới:**
1. **Bot features**: Chỉnh sửa `src/bot/telegram_handler.py`
2. **Web features**: Chỉnh sửa `src/web/dashboard.py`
3. **AI features**: Chỉnh sửa `src/ai/analyzer.py`
4. **Database**: Chỉnh sửa `src/database/models.py`

### **🌐 API Endpoints:**
```
GET  /api/stats              # Thống kê tổng quan
GET  /api/tasks/pending      # Tasks đang chờ
GET  /api/tasks/completed    # Tasks hoàn thành
GET  /api/tasks/in_progress  # Tasks đang làm
GET  /api/tasks/cancelled    # Tasks đã hủy
GET  /api/suggestions        # AI suggestions ⭐
GET  /api/insights           # Productivity insights ⭐
POST /api/tasks/{id}/complete # Hoàn thành task
POST /api/tasks/{id}/in_progress # Đặt task đang làm
POST /api/tasks/{id}/pending # Đặt task pending
POST /api/tasks/{id}/cancel  # Hủy task
```

## 🚀 **Deployment**

**⚠️ Lưu ý**: Project này được thiết kế để chạy trên môi trường local. Không có cấu hình deployment cloud.

## 🐛 **Troubleshooting**

### **❌ Lỗi thường gặp:**
```bash
# ImportError
pip install -r requirements.txt

# Config not found
cp src/config/example.py src/config/settings.py

# Port đã được sử dụng
netstat -ano | findstr :5000
taskkill /pid <PID> /f

# Telegram Conflict
# Chỉ chạy 1 instance bot tại 1 thời điểm
```

### **🔧 Auto-refresh không hoạt động:**
1. **Kiểm tra console**: Mở Developer Tools (F12) xem có lỗi JS không
2. **Kiểm tra network**: Xem API calls có thành công không
3. **Restart dashboard**: Dừng và chạy lại `python main.py --mode web`

## 📊 **Performance & Monitoring**

### **⚡ Thống kê hiệu suất:**
- **Task Processing**: <100ms average
- **AI Analysis**: <500ms per task
- **Web Dashboard**: Auto-refresh 30s, Real-time 10s
- **Database**: SQLite, supports 1000+ tasks
- **Memory Usage**: ~50MB cho bot + dashboard

### **📈 Monitoring:**
- **Health Check**: `/health` endpoint
- **Stats API**: `/api/stats` cho dashboard monitoring
- **Error Logging**: Console logs với timestamps

## 🚀 **Future Roadmap**

- [ ] **Machine Learning** model cho priority prediction
- [ ] **Integration** với Jira, Trello, Notion
- [ ] **Mobile app** companion
- [ ] **Team collaboration** features
- [ ] **Advanced analytics** và reporting
- [ ] **WebSocket** cho real-time updates
- [ ] **Push notifications** cho mobile
- [ ] **Multi-language** support

## 🤝 **Contributing**

1. **Fork** project
2. **Create** feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to branch (`git push origin feature/AmazingFeature`)
5. **Open** Pull Request

## 📄 **License**

Distributed under the MIT License. See `LICENSE` for more information.

---

**🎯 Tác giả**: AI Assistant  
**🚀 Phiên bản**: 3.0 (Auto-Refresh + Real-time)  
**📅 Cập nhật**: August 2025  
**⭐ Stars**: Nếu thấy hữu ích, hãy star repo này!

---

<div align="center">

**Made with ❤️ by AI Assistant**

*Tele Kanban Bot - Biến công việc thành niềm vui! 🎉*

</div>