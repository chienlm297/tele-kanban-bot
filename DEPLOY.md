# 🚀 Deploy Guide - Tele Kanban Bot

## 🌟 **Khuyến nghị: Deploy lên Railway.app**

### **Bước 1: Chuẩn bị**
1. Push code lên GitHub repository
2. Tạo tài khoản tại [railway.app](https://railway.app)

### **Bước 2: Deploy**
1. **Connect GitHub:**
   - Đăng nhập Railway → "New Project"
   - Chọn "Deploy from GitHub repo"
   - Authorize và chọn repository

2. **Set Environment Variables:**
   ```
   BOT_TOKEN=8347011918:AAEAPUWLaBXf_B17FT6KUkfd_e3Mtd2t0Dk
   MY_USER_ID=2084719052
   MY_USERNAME=chienlm2
   ```

3. **Deploy Services:**
   - **Web Service:** `python main.py --mode web`
   - **Bot Service:** `python main.py --mode bot`

### **Bước 3: Kiểm tra**
- ✅ Web dashboard: https://your-app.railway.app
- ✅ Bot hoạt động trong Telegram

---

## 🔄 **Alternative: Render.com**

### **Deploy Steps:**
1. Fork repo trên GitHub
2. Tạo tài khoản [render.com](https://render.com)
3. Create "New Web Service"
4. Connect GitHub repo
5. Settings:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: python main.py --mode web
   ```
6. Set Environment Variables như trên

---

## 🐳 **Docker Deploy (Advanced)**

### **Dockerfile:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "main.py", "--mode", "both"]
```

### **Deploy to:**
- Railway (với Dockerfile)
- Google Cloud Run
- AWS ECS
- DigitalOcean App Platform

---

## 🔧 **Troubleshooting**

### **Common Issues:**
1. **Environment Variables không load:**
   - Check spelling chính xác
   - Restart service sau khi set

2. **Database issues:**
   - SQLite có thể bị reset trên free tier
   - Consider upgrade PostgreSQL

3. **Bot conflict:**
   - Chỉ chạy 1 bot instance
   - Stop local bot trước khi deploy

### **Logs:**
```bash
# Railway
railway logs

# Render  
Check dashboard logs
```

---

## 💡 **Production Tips**

1. **Use PostgreSQL:** Thay vì SQLite cho production
2. **Environment Variables:** Không hardcode secrets
3. **Monitoring:** Setup uptime monitoring
4. **Backup:** Regular database backup
5. **Custom Domain:** Setup custom domain

---

## 🎯 **Next Steps**

1. **Deploy Web + Bot riêng biệt:** 2 services
2. **Database migration:** SQLite → PostgreSQL  
3. **Custom domain:** your-kanban-bot.com
4. **SSL/HTTPS:** Auto-enabled trên Railway
5. **Monitoring:** Setup alerts

**Cost:** ~$0-5/month trên Railway (free tier)
