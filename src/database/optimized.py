import sqlite3
import os
from contextlib import contextmanager
import logging

class OptimizedDatabase:
    """Database tối ưu cho Railway deployment"""
    
    def __init__(self, db_path: str = "tasks.db"):
        self.db_path = db_path
        self.setup_database()
        
    def setup_database(self):
        """Khởi tạo database với optimizations"""
        with self.get_connection() as conn:
            # Enable optimizations
            conn.execute("PRAGMA journal_mode = WAL")  # Better concurrency
            conn.execute("PRAGMA synchronous = NORMAL")  # Balance safety/speed
            conn.execute("PRAGMA cache_size = 1000")  # Cache optimization
            conn.execute("PRAGMA temp_store = memory")  # Use memory for temp
            
            # Create tables nếu chưa có
            conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,
                chat_id INTEGER NOT NULL,
                chat_title TEXT,
                message_text TEXT,
                tagged_by_username TEXT,
                tagged_by_full_name TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )''')
            
            # Create indexes for performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON tasks(created_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_chat_id ON tasks(chat_id)")
            
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.row_factory = sqlite3.Row
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
                
    def cleanup_old_data(self, days: int = 90):
        """Xóa data cũ để tiết kiệm space"""
        with self.get_connection() as conn:
            conn.execute("""
                DELETE FROM tasks 
                WHERE status = 'completed' 
                AND completed_at < datetime('now', '-{} days')
            """.format(days))
            
            # Vacuum để thu hồi space
            conn.execute("VACUUM")
            
    def get_db_size(self) -> float:
        """Lấy kích thước database (MB)"""
        if os.path.exists(self.db_path):
            return os.path.getsize(self.db_path) / (1024 * 1024)
        return 0
