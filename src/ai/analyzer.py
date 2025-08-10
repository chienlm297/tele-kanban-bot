import re
import datetime
from typing import List, Dict, Tuple
from src.database.models import TaskDatabase
import json

class TaskAIAnalyzer:
    def __init__(self, db_path: str = "tasks.db"):
        self.db = TaskDatabase(db_path)
        
        # Từ khóa ưu tiên cao
        self.high_priority_keywords = [
            'urgent', 'asap', 'emergency', 'critical', 'immediately', 'deadline',
            'khẩn cấp', 'gấp', 'urgent', 'deadline', 'hạn chót', 'cần gấp',
            'hot', 'fix', 'bug', 'error', 'lỗi', 'sự cố', 'crash',
            'meeting', 'họp', 'presentation', 'demo', 'thuyết trình',
            'review', 'merge', 'deploy', 'release', 'production', 'prod'
        ]
        
        # Từ khóa dự án quan trọng  
        self.important_project_keywords = [
            'mr', 'merge request', 'pull request', 'pr', 'git',
            'deploy', 'deployment', 'release', 'production',
            'database', 'db', 'server', 'api', 'backend',
            'client', 'customer', 'khách hàng', 'boss', 'sếp'
        ]
        
        # Pattern thời gian
        self.time_patterns = [
            r'hôm nay|today',
            r'ngày mai|tomorrow', 
            r'tuần này|this week',
            r'tháng này|this month',
            r'\d{1,2}[/\-]\d{1,2}',  # dd/mm or dd-mm
            r'(\d{1,2})\s*(giờ|h|hour)',  # X giờ
        ]
    
    def analyze_task_priority(self, task: Dict) -> float:
        """
        Phân tích độ ưu tiên của task (0-100)
        """
        score = 50.0  # Base score
        message_text = task['message_text'].lower()
        
        # 1. Phân tích từ khóa ưu tiên cao (+30 points)
        high_priority_score = self._analyze_keywords(message_text, self.high_priority_keywords)
        score += high_priority_score * 30
        
        # 2. Phân tích dự án quan trọng (+20 points)  
        project_score = self._analyze_keywords(message_text, self.important_project_keywords)
        score += project_score * 20
        
        # 3. Phân tích thời gian (+25 points)
        time_score = self._analyze_time_urgency(message_text)
        score += time_score * 25
        
        # 4. Phân tích người giao việc (+15 points)
        person_score = self._analyze_person_importance(task)
        score += person_score * 15
        
        # 5. Phân tích thời gian tạo (+10 points)
        age_score = self._analyze_task_age(task['created_at'])
        score += age_score * 10
        
        return min(100.0, max(0.0, score))
    
    def _analyze_keywords(self, text: str, keywords: List[str]) -> float:
        """Phân tích mật độ từ khóa quan trọng"""
        matches = 0
        for keyword in keywords:
            if keyword in text:
                matches += 1
        
        # Normalize by text length and keyword count
        density = matches / max(len(keywords), 1)
        return min(1.0, density * 2)  # Cap at 1.0
    
    def _analyze_time_urgency(self, text: str) -> float:
        """Phân tích tính cấp thiết về thời gian"""
        urgency_score = 0.0
        
        # Kiểm tra các pattern thời gian
        for pattern in self.time_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                urgency_score += 0.3
        
        # Từ khóa thời gian đặc biệt
        time_keywords = {
            'hôm nay': 1.0, 'today': 1.0,
            'ngày mai': 0.8, 'tomorrow': 0.8,
            'gấp': 0.9, 'urgent': 0.9,
            'deadline': 0.9, 'hạn chót': 0.9
        }
        
        for keyword, weight in time_keywords.items():
            if keyword in text:
                urgency_score = max(urgency_score, weight)
        
        return min(1.0, urgency_score)
    
    def _analyze_person_importance(self, task: Dict) -> float:
        """Phân tích tầm quan trọng của người giao việc"""
        # Có thể mở rộng để phân tích based on:
        # - Frequency của người này giao việc
        # - Historical completion rate
        # - Role/position (boss keywords)
        
        message_text = task['message_text'].lower()
        
        # Từ khóa chỉ người quan trọng
        important_person_keywords = [
            'anh', 'chị', 'boss', 'sếp', 'manager', 'lead',
            'director', 'client', 'customer', 'khách hàng'
        ]
        
        for keyword in important_person_keywords:
            if keyword in message_text:
                return 0.8
        
        return 0.3  # Default importance
    
    def _analyze_task_age(self, created_at: str) -> float:
        """Phân tích độ tuổi của task (task cũ hơn = ưu tiên cao hơn)"""
        try:
            created_time = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            now = datetime.datetime.now(created_time.tzinfo)
            age_hours = (now - created_time).total_seconds() / 3600
            
            # Tasks cũ hơn 24h có priority cao hơn
            if age_hours > 72:  # 3 days
                return 1.0
            elif age_hours > 24:  # 1 day  
                return 0.7
            elif age_hours > 8:  # 8 hours
                return 0.5
            else:
                return 0.2
                
        except:
            return 0.3
    
    def get_smart_suggestions(self, limit: int = 5) -> List[Dict]:
        """
        Lấy danh sách tasks được gợi ý ưu tiên
        """
        pending_tasks = self.db.get_pending_tasks()
        
        if not pending_tasks:
            return []
        
        # Tính priority score cho mỗi task
        scored_tasks = []
        for task in pending_tasks:
            priority_score = self.analyze_task_priority(task)
            task_with_score = task.copy()
            task_with_score['priority_score'] = priority_score
            task_with_score['priority_level'] = self._get_priority_level(priority_score)
            task_with_score['suggestion_reason'] = self._generate_suggestion_reason(task, priority_score)
            scored_tasks.append(task_with_score)
        
        # Sort by priority score descending
        scored_tasks.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return scored_tasks[:limit]
    
    def _get_priority_level(self, score: float) -> str:
        """Convert numeric score to priority level"""
        if score >= 80:
            return "🔥 Cực kỳ quan trọng"
        elif score >= 65:
            return "⚡ Ưu tiên cao"
        elif score >= 50:
            return "📝 Bình thường"
        else:
            return "📋 Ưu tiên thấp"
    
    def _generate_suggestion_reason(self, task: Dict, score: float) -> str:
        """Tạo lý do gợi ý cho task"""
        reasons = []
        message_text = task['message_text'].lower()
        
        # Phân tích lý do
        if any(keyword in message_text for keyword in ['urgent', 'gấp', 'khẩn cấp']):
            reasons.append("⏰ Có tính cấp thiết")
            
        if any(keyword in message_text for keyword in ['mr', 'merge', 'deploy', 'release']):
            reasons.append("🚀 Liên quan đến deployment")
            
        if any(keyword in message_text for keyword in ['bug', 'lỗi', 'error', 'fix']):
            reasons.append("🐛 Cần fix lỗi")
            
        if any(keyword in message_text for keyword in ['meeting', 'họp', 'demo']):
            reasons.append("👥 Có meeting/demo")
            
        if any(keyword in message_text for keyword in ['boss', 'sếp', 'client', 'khách hàng']):
            reasons.append("👤 Từ người quan trọng")
        
        # Phân tích thời gian
        try:
            created_time = datetime.datetime.fromisoformat(task['created_at'].replace('Z', '+00:00'))
            now = datetime.datetime.now(created_time.tzinfo)
            age_hours = (now - created_time).total_seconds() / 3600
            
            if age_hours > 48:
                reasons.append("⏳ Task đã cũ, cần xử lý")
        except:
            pass
        
        if not reasons:
            reasons.append("📊 Dựa trên pattern phân tích")
            
        return " • ".join(reasons[:3])  # Limit to 3 reasons
    
    def get_productivity_insights(self) -> Dict:
        """Phân tích insights về productivity"""
        all_tasks = self.db.get_all_tasks(100)
        completed_tasks = [t for t in all_tasks if t['status'] == 'completed']
        pending_tasks = [t for t in all_tasks if t['status'] == 'pending']
        
        # Tính completion time statistics
        completion_times = []
        for task in completed_tasks:
            if task['completed_at'] and task['created_at']:
                try:
                    created = datetime.datetime.fromisoformat(task['created_at'].replace('Z', '+00:00'))
                    completed = datetime.datetime.fromisoformat(task['completed_at'].replace('Z', '+00:00'))
                    hours = (completed - created).total_seconds() / 3600
                    completion_times.append(hours)
                except:
                    continue
        
        insights = {
            'total_tasks': len(all_tasks),
            'completed_tasks': len(completed_tasks),
            'pending_tasks': len(pending_tasks),
            'completion_rate': len(completed_tasks) / max(len(all_tasks), 1) * 100,
            'avg_completion_time_hours': sum(completion_times) / max(len(completion_times), 1) if completion_times else 0,
            'fastest_completion_hours': min(completion_times) if completion_times else 0,
            'slowest_completion_hours': max(completion_times) if completion_times else 0,
        }
        
        # Phân tích patterns
        patterns = self._analyze_completion_patterns(completed_tasks)
        insights.update(patterns)
        
        return insights
    
    def _analyze_completion_patterns(self, completed_tasks: List[Dict]) -> Dict:
        """Phân tích patterns hoàn thành tasks"""
        if not completed_tasks:
            return {}
        
        # Phân tích theo giờ trong ngày
        hourly_completion = {}
        for task in completed_tasks:
            try:
                completed_time = datetime.datetime.fromisoformat(task['completed_at'].replace('Z', '+00:00'))
                hour = completed_time.hour
                hourly_completion[hour] = hourly_completion.get(hour, 0) + 1
            except:
                continue
        
        # Tìm productive hours
        if hourly_completion:
            most_productive_hour = max(hourly_completion, key=hourly_completion.get)
            productivity_peak = f"{most_productive_hour}:00"
        else:
            productivity_peak = "Chưa đủ dữ liệu"
        
        return {
            'most_productive_hour': productivity_peak,
            'hourly_distribution': hourly_completion
        }
