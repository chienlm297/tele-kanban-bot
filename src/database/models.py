import sqlite3
import datetime
from typing import List, Dict, Optional

class TaskDatabase:
    def __init__(self, db_path: str = "tasks.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Khởi tạo database và tạo bảng tasks"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                chat_title TEXT,
                message_id INTEGER NOT NULL,
                message_text TEXT NOT NULL,
                tagged_by_user_id INTEGER NOT NULL,
                tagged_by_username TEXT,
                tagged_by_full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP NULL,
                status TEXT DEFAULT 'pending',
                notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_task(self, chat_id: int, chat_title: str, message_id: int, 
                 message_text: str, tagged_by_user_id: int, 
                 tagged_by_username: str = None, tagged_by_full_name: str = None) -> int:
        """Thêm task mới"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tasks (chat_id, chat_title, message_id, message_text, 
                             tagged_by_user_id, tagged_by_username, tagged_by_full_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (chat_id, chat_title, message_id, message_text, 
              tagged_by_user_id, tagged_by_username, tagged_by_full_name))
        
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return task_id
    
    def complete_task(self, task_id: int, notes: str = None) -> bool:
        """Đánh dấu task hoàn thành"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tasks 
            SET status = 'completed', completed_at = CURRENT_TIMESTAMP, notes = ?
            WHERE id = ?
        ''', (notes, task_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def set_task_pending(self, task_id: int, notes: str = None) -> bool:
        """Đặt task về trạng thái pending"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tasks 
            SET status = 'pending', completed_at = NULL, notes = ?
            WHERE id = ?
        ''', (notes, task_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def cancel_task(self, task_id: int, notes: str = None) -> bool:
        """Hủy bỏ task"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tasks 
            SET status = 'cancelled', completed_at = NULL, notes = ?
            WHERE id = ?
        ''', (notes, task_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def set_task_in_progress(self, task_id: int, notes: str = None) -> bool:
        """Đặt task thành trạng thái in_progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tasks 
            SET status = 'in_progress', notes = ?
            WHERE id = ?
        ''', (notes, task_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def get_pending_tasks(self) -> List[Dict]:
        """Lấy danh sách tasks chưa hoàn thành (pending)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, chat_id, chat_title, message_id, message_text,
                   tagged_by_user_id, tagged_by_username, tagged_by_full_name,
                   created_at, status
            FROM tasks 
            WHERE status = 'pending'
            ORDER BY created_at DESC
        ''')
        
        tasks = []
        for row in cursor.fetchall():
            tasks.append({
                'id': row[0],
                'chat_id': row[1],
                'chat_title': row[2],
                'message_id': row[3],
                'message_text': row[4],
                'tagged_by_user_id': row[5],
                'tagged_by_username': row[6],
                'tagged_by_full_name': row[7],
                'created_at': row[8],
                'status': row[9]
            })
        
        conn.close()
        return tasks
    
    def get_active_tasks(self) -> List[Dict]:
        """Lấy danh sách tasks đang hoạt động (pending + in_progress)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, chat_id, chat_title, message_id, message_text,
                   tagged_by_user_id, tagged_by_username, tagged_by_full_name,
                   created_at, status
            FROM tasks 
            WHERE status IN ('pending', 'in_progress')
            ORDER BY created_at DESC
        ''')
        
        tasks = []
        for row in cursor.fetchall():
            tasks.append({
                'id': row[0],
                'chat_id': row[1],
                'chat_title': row[2],
                'message_id': row[3],
                'message_text': row[4],
                'tagged_by_user_id': row[5],
                'tagged_by_username': row[6],
                'tagged_by_full_name': row[7],
                'created_at': row[8],
                'status': row[9]
            })
        
        conn.close()
        return tasks
    
    def get_all_tasks(self, limit: int = 100) -> List[Dict]:
        """Lấy tất cả tasks (bao gồm hoàn thành)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, chat_id, chat_title, message_id, message_text,
                   tagged_by_user_id, tagged_by_username, tagged_by_full_name,
                   created_at, completed_at, status, notes
            FROM tasks 
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        tasks = []
        for row in cursor.fetchall():
            tasks.append({
                'id': row[0],
                'chat_id': row[1],
                'chat_title': row[2],
                'message_id': row[3],
                'message_text': row[4],
                'tagged_by_user_id': row[5],
                'tagged_by_username': row[6],
                'tagged_by_full_name': row[7],
                'created_at': row[8],
                'completed_at': row[9],
                'status': row[10],
                'notes': row[11]
            })
        
        conn.close()
        return tasks
    
    def find_task_by_message(self, chat_id: int, reply_to_message_id: int) -> Optional[Dict]:
        """Tìm task dựa trên message được reply"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, chat_id, chat_title, message_id, message_text,
                   tagged_by_user_id, tagged_by_username, tagged_by_full_name,
                   created_at, status
            FROM tasks 
            WHERE chat_id = ? AND message_id = ? AND status = 'pending'
        ''', (chat_id, reply_to_message_id))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'chat_id': row[1],
                'chat_title': row[2],
                'message_id': row[3],
                'message_text': row[4],
                'tagged_by_user_id': row[5],
                'tagged_by_username': row[6],
                'tagged_by_full_name': row[7],
                'created_at': row[8],
                'status': row[9]
            }
        return None
    
    def get_stats(self) -> Dict:
        """Lấy thống kê tasks"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tổng số tasks
        cursor.execute('SELECT COUNT(*) FROM tasks')
        total = cursor.fetchone()[0]
        
        # Tasks pending
        cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "pending"')
        pending = cursor.fetchone()[0]
        
        # Tasks completed
        cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "completed"')
        completed = cursor.fetchone()[0]
        
        # Tasks cancelled
        cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "cancelled"')
        cancelled = cursor.fetchone()[0]
        
        # Tasks in progress
        cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "in_progress"')
        in_progress = cursor.fetchone()[0]
        
        # Tasks hôm nay
        cursor.execute('''
            SELECT COUNT(*) FROM tasks 
            WHERE DATE(created_at) = DATE('now', 'localtime')
        ''')
        today = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total,
            'pending': pending,
            'completed': completed,
            'cancelled': cancelled,
            'in_progress': in_progress,
            'today': today
        }
    
    def get_tasks_by_assignee(self) -> List[Dict]:
        """Lấy thống kê số lượng tasks theo người giao việc"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                tagged_by_full_name,
                tagged_by_username,
                COUNT(*) as task_count,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_count,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_count,
                SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_count,
                SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress_count
            FROM tasks 
            WHERE tagged_by_full_name IS NOT NULL OR tagged_by_username IS NOT NULL
            GROUP BY COALESCE(tagged_by_full_name, tagged_by_username)
            ORDER BY task_count DESC
        ''')
        
        assignees = []
        for row in cursor.fetchall():
            full_name = row[0] or row[1] or "Không rõ tên"
            username = row[1] or "Không có username"
            assignees.append({
                'name': full_name,
                'username': username,
                'total_tasks': row[2],
                'pending_tasks': row[3],
                'completed_tasks': row[4],
                'cancelled_tasks': row[5],
                'in_progress_tasks': row[6]
            })
        
        conn.close()
        return assignees
