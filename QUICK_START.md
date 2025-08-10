# 🚀 QUICK START - Tele Kanban Bot

> **Hướng dẫn nhanh để chạy project trong 5 phút**

## ⚡ **Bước 1: Cài đặt nhanh**

```bash
# Clone project
git clone <your-repo-url>
cd tele-kanban-bot

# Cài đặt dependencies
pip install -r requirements.txt
```

## ⚙️ **Bước 2: Cấu hình Bot**

```bash
# Copy config template
cp src/config/example.py src/config/settings.py
```

**Chỉnh sửa `src/config/settings.py`:**
- `BOT_TOKEN`: Lấy từ @BotFather
- `MY_USER_ID`: ID Telegram của bạn
- `MY_USERNAME`: Username Telegram (không có @)

## 🎯 **Bước 3: Chạy ngay lập tức**

### **Windows PowerShell (Khuyến nghị)**
```powershell
.\run.ps1                 # Chạy cả bot và dashboard
.\run.ps1 bot             # Chỉ chạy bot
.\run.ps1 web             # Chỉ chạy dashboard
.\run.ps1 help            # Xem hướng dẫn
```

### **Windows CMD**
```cmd
run.bat                   # Chạy cả bot và dashboard
run.bat bot               # Chỉ chạy bot
run.bat web               # Chỉ chạy dashboard
run.bat help              # Xem hướng dẫn
```

### **Linux/Mac**
```bash
chmod +x run.sh           # Cấp quyền thực thi (1 lần)
./run.sh                  # Chạy cả bot và dashboard
./run.sh bot              # Chỉ chạy bot
./run.sh web              # Chỉ chạy dashboard
./run.sh help             # Xem hướng dẫn
```

## 🌐 **Bước 4: Truy cập Dashboard**

- **URL**: `http://localhost:5000`
- **Bot**: Tự động chạy và ghi nhận tasks

## 🔧 **Các lệnh hữu ích**

```bash
# Cài đặt dependencies
.\run.ps1 install         # Windows PowerShell
run.bat install           # Windows CMD
./run.sh install          # Linux/Mac

# Test proxy (nếu ở công ty)
.\run.ps1 test            # Windows PowerShell
run.bat test              # Windows CMD
./run.sh test             # Linux/Mac

# Xem hướng dẫn
.\run.ps1 help            # Windows PowerShell
run.bat help              # Windows CMD
./run.sh help             # Linux/Mac
```

## 🎯 **Tính năng chính**

- **🤖 Bot**: Tự động ghi nhận công việc khi được tag tên
- **🌐 Dashboard**: Quản lý tasks với giao diện web đẹp
- **🔄 Auto-refresh**: Cập nhật dữ liệu real-time
- **🧠 AI**: Gợi ý tasks ưu tiên thông minh
- **📊 Stats**: Thống kê theo người giao việc
- **💬 Comments**: Ghi chú khi hoàn thành task

## 🆘 **Gặp vấn đề?**

1. **Python không được cài đặt**: Cài Python 3.7+
2. **File settings.py không tồn tại**: Copy từ example.py
3. **Bot không hoạt động**: Kiểm tra BOT_TOKEN
4. **Proxy lỗi**: Chạy `.\run.ps1 test` để kiểm tra

## 📖 **Xem thêm**

- **README.md**: Hướng dẫn chi tiết
- **src/config/example.py**: Template cấu hình
- **test_proxy.py**: Test kết nối proxy

---

**🎉 Chúc bạn sử dụng project thành công!**
