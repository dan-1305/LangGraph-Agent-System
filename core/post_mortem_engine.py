import sqlite3
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

class PostMortemEngine:
    """
    Module tự động phân tích lỗi lầm thực tế (Post-Mortem).
    Nhiệm vụ: Đọc lịch sử Trading, đối chiếu nguyên lý Minervini để rút ra bài học.
    """
    def __init__(self, db_path: str = "data/system_logs.db"):
        self.db_path = db_path
        self.failed_paths_file = Path("logs/FAILED_PATHS.json")
        self.logger = logging.getLogger("PostMortemEngine")

    def analyze_recent_trades(self, limit: int = 10):
        """Phân tích các lệnh giao dịch gần đây."""
        self.logger.info(f"🔍 [Post-Mortem] Đang rà soát {limit} lệnh gần nhất...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ticker, action, price, reasoning FROM Trading_Decisions ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            trades = cursor.fetchall()
            conn.close()
            
            for trade in trades:
                ticker, action, price, reasoning = trade
                # Logic phân tích đơn giản: Nếu action là BUY nhưng reasoning không nhắc đến 'Stage 2' hoặc 'Base'
                if action.upper() == "BUY" and not any(k in reasoning.lower() for k in ["stage 2", "tích lũy", "vcp", "pivot"]):
                    self._log_failure(f"Lệnh BUY {ticker} tại giá {price} vi phạm nguyên lý Minervini: Thiếu xác nhận Stage 2/VCP.")
                    
        except Exception as e:
            self.logger.error(f"❌ Lỗi truy vấn DB: {e}")

    def _log_failure(self, reason: str):
        """Cập nhật vào FAILED_PATHS.json"""
        data = {"failure_logs": []}
        if self.failed_paths_file.exists():
            with open(self.failed_paths_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        
        # Tránh trùng lặp
        if reason not in data["failure_logs"]:
            data["failure_logs"].append(reason)
            with open(self.failed_paths_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"🚩 [Post-Mortem] Đã ghi nhận sai lầm mới: {reason}")

if __name__ == "__main__":
    engine = PostMortemEngine()
    engine.analyze_recent_trades()
