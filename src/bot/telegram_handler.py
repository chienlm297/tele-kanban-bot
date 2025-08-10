import logging
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.database.models import TaskDatabase
from src.ai.analyzer import TaskAIAnalyzer
import os

# Import settings from config package
from src.config import settings

# Thiết lập logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramKanbanBot:
    def __init__(self):
        self.db = TaskDatabase(settings.DB_PATH)
        self.ai_analyzer = TaskAIAnalyzer(settings.DB_PATH)
        self.my_user_id = settings.MY_USER_ID
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler cho lệnh /start"""
        if update.effective_user.id != self.my_user_id:
            await update.message.reply_text("Xin lỗi, bot này chỉ dành cho chủ sở hữu.")
            return
            
        await update.message.reply_text(
                    "🤖 *Kanban Bot đã sẵn sàng!*\n\n"
                    "Bot sẽ tự động:\n"
                    "• Tạo task khi bạn được tag trong nhóm (lặng lẽ lưu vào danh sách)\n"
                    "• Đánh dấu hoàn thành khi bạn reply 'done'\n\n"
                    "Lệnh có sẵn:\n"
                    "/tasks - Xem danh sách công việc\n"
                    "/ai - Gợi ý AI tasks ưu tiên\n"
                    "/stats - Xem thống kê\n"
                    "/insights - Phân tích productivity\n"
                    "/help - Hướng dẫn sử dụng",
                    parse_mode='Markdown'
                )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler cho lệnh /help"""
        if update.effective_user.id != self.my_user_id:
            return
            
        help_text = """
🤖 *Hướng dẫn sử dụng Kanban Bot*

*Cách hoạt động:*
1. Khi ai đó tag bạn trong nhóm → Bot tự động tạo task (lặng lẽ lưu vào danh sách)
2. Bạn reply "done" vào message đó → Task được đánh dấu hoàn thành

*Lệnh có sẵn:*
/start - Khởi động bot
/tasks - Xem danh sách công việc chưa hoàn thành
/all - Xem tất cả công việc (bao gồm đã hoàn thành)
/stats - Xem thống kê
/help - Hiển thị hướng dẫn này

*Cách đánh dấu hoàn thành:*
- Reply "done", "Done", "DONE"
- Reply "xong", "Xong", "XONG"
- Reply "hoàn thành"

*Lưu ý:* Bot chỉ hoạt động với chủ sở hữu (bạn).
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def tasks_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler cho lệnh /tasks - hiển thị tasks chưa hoàn thành"""
        if update.effective_user.id != self.my_user_id:
            return
            
        tasks = self.db.get_pending_tasks()
        
        if not tasks:
            await update.message.reply_text("🎉 Tuyệt vời! Bạn không có công việc nào đang chờ.")
            return
        
        message = f"📋 *Danh sách công việc ({len(tasks)} việc):*\n\n"
        
        for i, task in enumerate(tasks, 1):
            chat_title = task['chat_title'] or "Chat riêng"
            tagged_by = task['tagged_by_full_name'] or task['tagged_by_username'] or "Không rõ"
            created_date = task['created_at'][:10]  # Lấy ngày
            
            # Cắt ngắn message nếu quá dài
            task_text = task['message_text']
            if len(task_text) > 100:
                task_text = task_text[:97] + "..."
            
            message += f"*{i}.* ID: {task['id']}\n"
            message += f"📍 *Nhóm:* {chat_title}\n"
            message += f"👤 *Người giao:* {tagged_by}\n"
            message += f"📅 *Ngày:* {created_date}\n"
            message += f"💬 *Nội dung:* {task_text}\n\n"
        
        # Escape markdown special characters in dynamic content
        safe_message = message.replace('*', '\\*').replace('_', '\\_').replace('[', '\\[').replace(']', '\\]')
        await update.message.reply_text(safe_message, parse_mode='Markdown')
    
    async def ai_suggestions_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler cho lệnh /ai - hiển thị AI suggestions"""
        if update.effective_user.id != self.my_user_id:
            return
            
        suggestions = self.ai_analyzer.get_smart_suggestions(5)
        
        if not suggestions:
            await update.message.reply_text("🎉 Tuyệt vời! AI không có gợi ý ưu tiên nào - bạn đã hoàn thành hết việc quan trọng!")
            return
        
        message = f"🤖 *AI Smart Suggestions* (Top {len(suggestions)})\n\n"
        message += "Dựa trên phân tích thông minh, đây là các tasks AI khuyên bạn nên ưu tiên:\n\n"
        
        for i, task in enumerate(suggestions, 1):
            priority_emoji = self._get_priority_emoji(task['priority_score'])
            score = round(task['priority_score'])
            
            message += f"{priority_emoji} *{i}. Task #{task['id']}* (Score: {score}/100)\n"
            message += f"📍 *Nhóm:* {task['chat_title'] or 'Chat riêng'}\n"
            message += f"👤 *Người giao:* {task['tagged_by_full_name'] or task['tagged_by_username'] or 'Không rõ'}\n"
            
            # Limit message text length
            task_text = task['message_text'] or '[Media/File]'
            if len(task_text) > 100:
                task_text = task_text[:97] + "..."
            # Escape markdown in task text and suggestion reason
            safe_task_text = task_text.replace('*', '\\*').replace('_', '\\_').replace('[', '\\[').replace(']', '\\]').replace('`', '\\`')
            safe_reason = task['suggestion_reason'].replace('*', '\\*').replace('_', '\\_').replace('[', '\\[').replace(']', '\\]').replace('`', '\\`')
            
            message += f"💬 *Nội dung:* {safe_task_text}\n"
            message += f"🧠 *Lý do AI:* {safe_reason}\n\n"
        
        message += "💡 *Tip:* Sử dụng /tasks để xem tất cả tasks hoặc truy cập web dashboard để quản lý chi tiết!"
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    def _get_priority_emoji(self, score: float) -> str:
        """Get emoji based on priority score"""
        if score >= 80:
            return "🔥"
        elif score >= 65:
            return "⚡"
        elif score >= 50:
            return "📝"
        else:
            return "📋"
    
    async def insights_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler cho lệnh /insights - hiển thị productivity insights"""
        if update.effective_user.id != self.my_user_id:
            return
            
        insights = self.ai_analyzer.get_productivity_insights()
        
        message = f"📊 *Productivity Insights*\n\n"
        message += f"📈 *Tổng quan:*\n"
        message += f"• Tổng số việc: {insights['total_tasks']}\n"
        message += f"• Hoàn thành: {insights['completed_tasks']} ✅\n"
        message += f"• Đang chờ: {insights['pending_tasks']} ⏳\n"
        message += f"• Tỷ lệ hoàn thành: {insights['completion_rate']:.1f}%\n\n"
        
        if insights['avg_completion_time_hours'] > 0:
            avg_hours = insights['avg_completion_time_hours']
            message += f"⏱️ *Thời gian xử lý:*\n"
            message += f"• Trung bình: {avg_hours:.1f} giờ\n"
            
            if insights['fastest_completion_hours'] > 0:
                message += f"• Nhanh nhất: {insights['fastest_completion_hours']:.1f} giờ\n"
            if insights['slowest_completion_hours'] > 0:
                message += f"• Chậm nhất: {insights['slowest_completion_hours']:.1f} giờ\n"
            message += "\n"
        
        if 'most_productive_hour' in insights:
            message += f"🕐 *Giờ làm việc hiệu quả nhất:* {insights['most_productive_hour']}\n\n"
        
        message += "💡 *Tip:* Truy cập web dashboard để xem phân tích chi tiết hơn!"
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def all_tasks_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler cho lệnh /all - hiển thị tất cả tasks"""
        if update.effective_user.id != self.my_user_id:
            return
            
        tasks = self.db.get_all_tasks(50)  # Giới hạn 50 tasks gần nhất
        
        if not tasks:
            await update.message.reply_text("Chưa có công việc nào được ghi nhận.")
            return
        
        message = f"📊 *Tất cả công việc ({len(tasks)} việc gần nhất):*\n\n"
        
        for i, task in enumerate(tasks, 1):
            status_icon = "✅" if task['status'] == 'completed' else "⏳"
            chat_title = task['chat_title'] or "Chat riêng"
            created_date = task['created_at'][:10]
            
            task_text = task['message_text']
            if len(task_text) > 80:
                task_text = task_text[:77] + "..."
            
            message += f"{status_icon} *{task['id']}.* {task_text}\n"
            message += f"📍 {chat_title} | 📅 {created_date}\n\n"
            
            # Giới hạn độ dài message
            if len(message) > 3500:
                message += "... (và nhiều hơn nữa)"
                break
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler cho lệnh /stats"""
        if update.effective_user.id != self.my_user_id:
            return
            
        stats = self.db.get_stats()
        
        message = f"""
📊 *Thống kê công việc*

📈 *Tổng quan:*
• Tổng số việc: {stats['total']}
• Đang chờ: {stats['pending']} ⏳
• Đã hoàn thành: {stats['completed']} ✅
• Hôm nay: {stats['today']} 📅

💪 *Tỷ lệ hoàn thành:* {(stats['completed'] / max(stats['total'], 1) * 100):.1f}%
        """
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler cho tất cả messages"""
        try:
            message = update.message
            user = update.effective_user
            chat = update.effective_chat
            
            # Kiểm tra xem có phải message trong group không
            if chat.type in ['group', 'supergroup']:
                await self.handle_group_message(update, context)
            elif user.id == self.my_user_id:
                await self.handle_private_message(update, context)
                
        except Exception as e:
            logger.error(f"Lỗi xử lý message: {e}")
    
    async def handle_group_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Xử lý message trong group"""
        message = update.message
        user = update.effective_user
        chat = update.effective_chat
        
        # Debug: Log tất cả messages trong group
        logger.info(f"📩 Message trong {chat.title}: '{message.text}' từ {user.full_name} (@{user.username})")
        
        # Kiểm tra xem có phải mình được tag không
        is_tagged = self.is_tagged_in_message(message)
        logger.info(f"🏷️ Có được tag không: {is_tagged}")
        
        if is_tagged:
            # Tạo task mới
            task_id = self.db.add_task(
                chat_id=chat.id,
                chat_title=chat.title,
                message_id=message.message_id,
                message_text=message.text or message.caption or "[Media/File]",
                tagged_by_user_id=user.id,
                tagged_by_username=user.username,
                tagged_by_full_name=user.full_name
            )
            
            logger.info(f"✅ Tạo task mới #{task_id} từ {user.full_name} trong {chat.title}")
            # Không gửi tin nhắn hay reaction, chỉ lưu vào danh sách
        
        # Kiểm tra xem có phải reply "done" không
        elif (user.id == self.my_user_id and 
              message.reply_to_message and 
              self.is_done_message(message.text)):
            
            logger.info(f"🔍 Tìm task để đánh dấu hoàn thành...")
            
            # Tìm task tương ứng
            task = self.db.find_task_by_message(
                chat.id, 
                message.reply_to_message.message_id
            )
            
            if task:
                success = self.db.complete_task(task['id'], message.text)
                if success:
                    await message.reply_text(f"🎉 Hoàn thành công việc #{task['id']}!")
                    logger.info(f"✅ Hoàn thành task #{task['id']}")
            else:
                logger.info(f"❌ Không tìm thấy task để hoàn thành")
    
    async def handle_private_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Xử lý message riêng từ chủ sở hữu"""
        message = update.message
        
        # Có thể thêm các lệnh đặc biệt ở đây
        if message.text and message.text.lower() in ['tasks', 'task']:
            await self.tasks_command(update, context)
    
    def is_tagged_in_message(self, message) -> bool:
        """Kiểm tra xem mình có được tag trong message không"""
        if not message.text and not message.caption:
            logger.info(f"❌ Message không có text/caption")
            return False
        
        text = message.text or message.caption
        logger.info(f"🔍 Kiểm tra text: '{text}'")
        
        # Kiểm tra entities để tìm mention
        if message.entities:
            logger.info(f"📝 Có {len(message.entities)} entities")
            for entity in message.entities:
                logger.info(f"📝 Entity: type={entity.type}, offset={entity.offset}, length={entity.length}")
                
                if entity.type == "mention":
                    mentioned_text = text[entity.offset:entity.offset + entity.length]
                    logger.info(f"🏷️ Mention text: '{mentioned_text}'")
                    
                    if hasattr(settings, 'MY_USERNAME') and mentioned_text == f"@{settings.MY_USERNAME}":
                        logger.info(f"✅ Tìm thấy mention @{settings.MY_USERNAME}")
                        return True
                        
                elif entity.type == "text_mention":
                    logger.info(f"🏷️ Text mention: user_id={entity.user.id if entity.user else 'None'}")
                    if entity.user and entity.user.id == self.my_user_id:
                        logger.info(f"✅ Tìm thấy text mention cho user {self.my_user_id}")
                        return True
        else:
            logger.info(f"❌ Message không có entities")
            
        # Fallback: kiểm tra đơn giản bằng text search
        if hasattr(settings, 'MY_USERNAME') and f"@{settings.MY_USERNAME}" in text:
            logger.info(f"✅ Tìm thấy @{settings.MY_USERNAME} trong text")
            return True
        
        logger.info(f"❌ Không tìm thấy mention nào")
        return False
    
    def is_done_message(self, text: str) -> bool:
        """Kiểm tra xem message có phải là 'done' không"""
        if not text:
            return False
        
        done_words = [
            'done', 'Done', 'DONE',
            'xong', 'Xong', 'XONG', 
            'hoàn thành', 'Hoàn thành', 'HOÀN THÀNH',
            'ok', 'OK', 'Ok'
        ]
        
        return text.strip() in done_words
    
    def run(self):
        """Chạy bot"""
        application = Application.builder().token(settings.BOT_TOKEN).build()
        
        # Đăng ký handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("tasks", self.tasks_command))
        application.add_handler(CommandHandler("ai", self.ai_suggestions_command))
        application.add_handler(CommandHandler("insights", self.insights_command))
        application.add_handler(CommandHandler("all", self.all_tasks_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        
        # Handler cho tất cả messages
        application.add_handler(MessageHandler(filters.ALL, self.handle_message))
        
        logger.info("Bot đang khởi động...")
        application.run_polling()

if __name__ == "__main__":
    bot = TelegramKanbanBot()
    bot.run()
