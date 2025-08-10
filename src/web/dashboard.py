from flask import Flask, render_template, jsonify, request
from src.database.models import TaskDatabase
from src.ai.analyzer import TaskAIAnalyzer
import requests
import os

# Use production config if in cloud environment
if os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('RENDER') or os.getenv('DYNO'):
    from src.config import production as settings
else:
    from src.config import settings

app = Flask(__name__, template_folder='../../templates')
db = TaskDatabase(settings.DB_PATH)
ai_analyzer = TaskAIAnalyzer(settings.DB_PATH)

@app.route('/')
def dashboard():
    """Trang chủ dashboard"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    """API lấy thống kê"""
    stats = db.get_stats()
    return jsonify(stats)

@app.route('/api/tasks')
def api_tasks():
    """API lấy danh sách tasks"""
    task_type = request.args.get('type', 'pending')
    
    if task_type == 'all':
        tasks = db.get_all_tasks(100)
    else:
        tasks = db.get_pending_tasks()
    
    return jsonify(tasks)

@app.route('/api/tasks/pending')
def api_pending_tasks():
    """API lấy tasks chưa hoàn thành"""
    tasks = db.get_pending_tasks()
    return jsonify(tasks)

@app.route('/api/tasks/completed')
def api_completed_tasks():
    """API lấy tasks đã hoàn thành"""
    all_tasks = db.get_all_tasks(100)
    completed_tasks = [task for task in all_tasks if task['status'] == 'completed']
    return jsonify(completed_tasks)

@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task_api(task_id):
    """API để đánh dấu task hoàn thành từ web"""
    try:
        # Lấy thông tin task
        all_tasks = db.get_all_tasks(1000)
        task = None
        for t in all_tasks:
            if t['id'] == task_id and t['status'] == 'pending':
                task = t
                break
        
        if not task:
            return jsonify({'success': False, 'error': 'Task không tìm thấy hoặc đã hoàn thành'}), 404
        
        # Đánh dấu hoàn thành trong database
        success = db.complete_task(task_id, 'Hoàn thành từ web dashboard')
        
        if success:
            # Gửi message reply trong Telegram qua HTTP API trực tiếp
            send_telegram_reply(task)
            
            return jsonify({'success': True, 'message': f'Đã hoàn thành task #{task_id}'})
        else:
            return jsonify({'success': False, 'error': 'Không thể hoàn thành task'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def send_telegram_reply(task):
    """Gửi reply message trong Telegram khi hoàn thành từ web"""
    try:
        chat_id = task['chat_id']
        message_id = task['message_id']
        
        # Gửi request trực tiếp đến Telegram API
        url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': f"🎉 Task #{task['id']} đã được hoàn thành từ web dashboard!",
            'reply_to_message_id': message_id
        }
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print(f"✅ Đã gửi reply hoàn thành task #{task['id']} trong chat {chat_id}")
        else:
            print(f"❌ Lỗi gửi reply: {response.status_code} - {response.text}")
        
    except Exception as e:
        print(f"❌ Lỗi gửi reply: {e}")

@app.route('/api/suggestions')
def api_suggestions():
    """API lấy smart suggestions"""
    try:
        limit = request.args.get('limit', 5, type=int)
        suggestions = ai_analyzer.get_smart_suggestions(limit)
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/insights')
def api_insights():
    """API lấy productivity insights"""
    try:
        insights = ai_analyzer.get_productivity_insights()
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>/analyze')
def api_analyze_task(task_id):
    """API phân tích priority của một task cụ thể"""
    try:
        all_tasks = db.get_all_tasks(1000)
        task = None
        for t in all_tasks:
            if t['id'] == task_id:
                task = t
                break
        
        if not task:
            return jsonify({'error': 'Task không tìm thấy'}), 404
        
        priority_score = ai_analyzer.analyze_task_priority(task)
        priority_level = ai_analyzer._get_priority_level(priority_score)
        suggestion_reason = ai_analyzer._generate_suggestion_reason(task, priority_score)
        
        return jsonify({
            'task_id': task_id,
            'priority_score': priority_score,
            'priority_level': priority_level,
            'suggestion_reason': suggestion_reason
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Production optimizations
    debug_mode = settings.DEBUG if hasattr(settings, 'DEBUG') else False
    app.run(
        host='0.0.0.0', 
        port=settings.WEB_PORT, 
        debug=debug_mode,
        threaded=True,  # Enable threading for better performance
        processes=1     # Single process to save memory
    )
