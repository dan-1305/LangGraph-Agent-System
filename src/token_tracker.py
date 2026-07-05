import sqlite3
import os
from datetime import datetime
from pathlib import Path

class QuotaExceededError(Exception):
    pass

class TokenTracker:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent
        self.db_path = base_dir / "data" / "system_logs.db"
        self._init_db()
        self.session_tokens = 0
        self.MAX_SESSION_TOKENS = int(os.getenv("MAX_SESSION_TOKENS", "50000"))
        
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS API_Usage_Logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            project_name TEXT,
            model_name TEXT,
            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            total_tokens INTEGER,
            estimated_cost_usd REAL
        )
        ''')
        conn.commit()
        conn.close()
        
    def _calculate_cost(self, model_name: str, prompt_tokens: int, completion_tokens: int) -> float:
        """
        Tính toán chi phí dựa trên bảng giá (tham khảo).
        Giá có thể thay đổi, đây là mức giá ước tính (USD / 1M tokens).
        """
        pricing = {
            "gemini-2.5-flash": {"prompt": 0.075, "completion": 0.30},
            "gemini-2.5-pro": {"prompt": 3.50, "completion": 10.50},
            "gemini-1.5-flash": {"prompt": 0.075, "completion": 0.30},
            "gemini-1.5-pro": {"prompt": 3.50, "completion": 10.50},
            "gpt-4o-mini": {"prompt": 0.15, "completion": 0.60},
            "gpt-4o": {"prompt": 5.00, "completion": 15.00}
        }
        
        # Mặc định lấy giá flash nếu không match
        rates = pricing.get(model_name, {"prompt": 0.1, "completion": 0.5})
        
        cost = (prompt_tokens / 1000000) * rates["prompt"] + (completion_tokens / 1000000) * rates["completion"]
        return cost

    def log_usage(self, project_name: str, model_name: str, prompt_tokens: int, completion_tokens: int):
        total_tokens = prompt_tokens + completion_tokens
        
        # Mốc 16: The Circuit Breaker (Hard Quota Limit)
        self.session_tokens += total_tokens
        if self.session_tokens > self.MAX_SESSION_TOKENS:
            raise QuotaExceededError(f"CRITICAL: Session exceeded {self.MAX_SESSION_TOKENS} tokens. Halting to prevent API bill shock!")
            
        cost = self._calculate_cost(model_name, prompt_tokens, completion_tokens)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO API_Usage_Logs (timestamp, project_name, model_name, prompt_tokens, completion_tokens, total_tokens, estimated_cost_usd)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, project_name, model_name, prompt_tokens, completion_tokens, total_tokens, cost))
        conn.commit()
        conn.close()
        
        return cost
        
    def get_total_cost(self, project_name: str = None) -> float:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if project_name:
            cursor.execute('SELECT SUM(estimated_cost_usd) FROM API_Usage_Logs WHERE project_name = ?', (project_name,))
        else:
            cursor.execute('SELECT SUM(estimated_cost_usd) FROM API_Usage_Logs')
        
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0.0

# Singleton instance
tracker = TokenTracker()

def track_llm_usage(response, project_name: str, model_name: str):
    """
    Helper function để parse token usage từ response của LangChain/OpenAI
    và log vào database.
    """
    try:
        # Langchain AIMessage often has response_metadata
        if hasattr(response, 'response_metadata') and 'token_usage' in response.response_metadata:
            usage = response.response_metadata['token_usage']
            p_tokens = usage.get('prompt_tokens', 0)
            c_tokens = usage.get('completion_tokens', 0)
            tracker.log_usage(project_name, model_name, p_tokens, c_tokens)
    except Exception as e:
        print(f"⚠️ Không thể track token usage: {e}")
