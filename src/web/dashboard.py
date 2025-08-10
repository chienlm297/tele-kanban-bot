from flask import Flask, render_template, jsonify, request
from src.database.models import TaskDatabase
from src.ai.analyzer import TaskAIAnalyzer
import requests
import os

# Import settings from config package
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
    try:
        stats = db.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint cho Railway"""
    return jsonify({'status': 'healthy', 'timestamp': '2024-01-01'})

@app.route('/api/tasks')
def api_tasks():
    """API lấy danh sách tasks"""
    status = request.args.get('status', 'pending')
    
    if status == 'all':
        tasks = db.get_all_tasks(100)
    elif status == 'pending':
        tasks = db.get_pending_tasks()
    elif status == 'completed':
        all_tasks = db.get_all_tasks(100)
        tasks = [task for task in all_tasks if task['status'] == 'completed']
    elif status == 'cancelled':
        all_tasks = db.get_all_tasks(100)
        tasks = [task for task in all_tasks if task['status'] == 'cancelled']
    elif status == 'in_progress':
        all_tasks = db.get_all_tasks(100)
        tasks = [task for task in all_tasks if task['status'] == 'in_progress']
    else:
        # Default to pending if unknown status
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
    """API để hoàn thành task từ web"""
    try:
        # Lấy comment từ request body
        data = request.get_json() or {}
        comment = data.get('comment', 'Hoàn thành từ web dashboard')
        
        # Lấy thông tin task
        all_tasks = db.get_all_tasks(1000)
        task = None
        for t in all_tasks:
            if t['id'] == task_id and t['status'] in ['pending', 'in_progress']:
                task = t
                break
        
        if not task:
            return jsonify({'success': False, 'error': 'Task không tìm thấy hoặc không thể hoàn thành'}), 404
        
        # Đánh dấu hoàn thành trong database
        success = db.complete_task(task_id, comment)
        
        if success:
            # Gửi message reply trong Telegram qua HTTP API trực tiếp
            send_telegram_reply(task)
            
            return jsonify({'success': True, 'message': f'Đã hoàn thành task #{task_id}'})
        else:
            return jsonify({'success': False, 'error': 'Không thể hoàn thành task'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>/pending', methods=['POST'])
def set_task_pending_api(task_id):
    """API để đặt task về trạng thái pending từ web"""
    try:
        # Lấy comment từ request body
        data = request.get_json() or {}
        comment = data.get('comment', 'Đặt lại về pending từ web dashboard')
        
        # Lấy thông tin task
        all_tasks = db.get_all_tasks(1000)
        task = None
        for t in all_tasks:
            if t['id'] == task_id and t['status'] in ['completed', 'cancelled', 'in_progress']:
                task = t
                break
        
        if not task:
            return jsonify({'success': False, 'error': 'Task không tìm thấy hoặc đã ở trạng thái pending'}), 404
        
        # Đặt về trạng thái pending trong database
        success = db.set_task_pending(task_id, comment)
        
        if success:
            return jsonify({'success': True, 'message': f'Đã đặt task #{task_id} về trạng thái pending'})
        else:
            return jsonify({'success': False, 'error': 'Không thể đặt task về pending'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>/cancel', methods=['POST'])
def cancel_task_api(task_id):
    """API để hủy bỏ task từ web"""
    try:
        # Lấy comment từ request body
        data = request.get_json() or {}
        comment = data.get('comment', 'Hủy bỏ từ web dashboard')
        
        # Lấy thông tin task
        all_tasks = db.get_all_tasks(1000)
        task = None
        for t in all_tasks:
            if t['id'] == task_id and t['status'] in ['pending', 'in_progress']:
                task = t
                break
        
        if not task:
            return jsonify({'success': False, 'error': 'Task không tìm thấy hoặc không thể hủy bỏ'}), 404
        
        # Hủy bỏ task trong database
        success = db.cancel_task(task_id, comment)
        
        if success:
            return jsonify({'success': True, 'message': f'Đã hủy bỏ task #{task_id}'})
        else:
            return jsonify({'success': False, 'error': 'Không thể hủy bỏ task'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>/in_progress', methods=['POST'])
def set_task_in_progress_api(task_id):
    """API để đặt task thành trạng thái in_progress từ web"""
    try:
        # Lấy comment từ request body
        data = request.get_json() or {}
        comment = data.get('comment', 'Đặt thành in_progress từ web dashboard')
        
        # Lấy thông tin task
        all_tasks = db.get_all_tasks(1000)
        task = None
        for t in all_tasks:
            if t['id'] == task_id and t['status'] in ['pending', 'completed']:
                task = t
                break
        
        if not task:
            return jsonify({'success': False, 'error': 'Task không tìm thấy hoặc không thể đặt thành in_progress'}), 404
        
        # Đặt task thành in_progress trong database
        success = db.set_task_in_progress(task_id, comment)
        
        if success:
            return jsonify({'success': True, 'message': f'Đã đặt task #{task_id} thành trạng thái đang làm'})
        else:
            return jsonify({'success': False, 'error': 'Không thể đặt task thành in_progress'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks/cancelled')
def api_cancelled_tasks():
    """API lấy tasks đã bị hủy bỏ"""
    all_tasks = db.get_all_tasks(100)
    cancelled_tasks = [task for task in all_tasks if task['status'] == 'cancelled']
    return jsonify(cancelled_tasks)

@app.route('/api/tasks/in_progress')
def api_in_progress_tasks():
    """API lấy tasks đang trong quá trình thực hiện"""
    all_tasks = db.get_all_tasks(100)
    in_progress_tasks = [task for task in all_tasks if task['status'] == 'in_progress']
    return jsonify(in_progress_tasks)

def send_telegram_reply(task):
    """Gửi reply message trong Telegram khi hoàn thành từ web"""
    try:
        chat_id = task['chat_id']
        message_id = task['message_id']
        
        # Gửi request trực tiếp đến Telegram API
        url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': f"🎉 Task #{task['id']} done!",
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
    """API lấy insights từ AI"""
    try:
        insights = ai_analyzer.get_productivity_insights()
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/assignees')
def api_assignees_stats():
    """API lấy thống kê tasks theo người giao việc"""
    try:
        assignees = db.get_tasks_by_assignee()
        return jsonify(assignees)
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
    
    # Production mode: sử dụng PORT từ environment
    port = int(os.getenv('PORT', settings.WEB_PORT))
    host = '0.0.0.0'
    
    print(f"🌐 Khởi động dashboard trên {host}:{port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"🌍 Environment: {'Production' if os.getenv('RAILWAY_ENVIRONMENT') else 'Development'}")
    
    app.run(
        host=host, 
        port=port, 
        debug=debug_mode,
        threaded=True,  # Enable threading for better performance
        processes=1     # Single process to save memory
    )
