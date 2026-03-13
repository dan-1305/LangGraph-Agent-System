import sqlite3
import os
from datetime import datetime

class SystemDB:
    def __init__(self):
        # Tạo thư mục data ở thư mục gốc nếu chưa có
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, "data", "system_logs.db")
        
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()
        
    def _create_tables(self):
        cursor = self.conn.cursor()
        
        # Bảng lưu quyết định hàng ngày của Live Advisor
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Trading_Decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ticker TEXT,
            price REAL,
            action TEXT,
            confidence INTEGER,
            stop_loss_pct REAL,
            take_profit_pct REAL,
            reasoning TEXT
        )
        ''')
        
        # Bảng lưu kết quả các đợt Backtest
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Backtest_Reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ticker TEXT,
            start_date TEXT,
            end_date TEXT,
            initial_capital REAL,
            final_capital REAL,
            roi_pct REAL,
            sharpe_ratio REAL,
            max_drawdown_pct REAL,
            win_rate_pct REAL
        )
        ''')
        
        # Bảng lưu lịch sử cập nhật dự án
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Project_Updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            module TEXT,
            description TEXT
        )
        ''')
        
        # Bảng lưu lịch sử Paper Trading
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Paper_Trade_Portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            btc_bal REAL,
            eth_bal REAL,
            sol_bal REAL,
            usdt_bal REAL,
            total_usdt_value REAL
        )
        ''')
        
        self.conn.commit()
        
    def log_trading_decision(self, ticker, price, action, confidence, sl, tp, reasoning):
        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
        INSERT INTO Trading_Decisions (timestamp, ticker, price, action, confidence, stop_loss_pct, take_profit_pct, reasoning)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, ticker, price, action, confidence, sl, tp, reasoning))
        self.conn.commit()
        
    def log_backtest_report(self, ticker, start_date, end_date, initial, final, roi, sharpe, max_dd, win_rate):
        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
        INSERT INTO Backtest_Reports (timestamp, ticker, start_date, end_date, initial_capital, final_capital, roi_pct, sharpe_ratio, max_drawdown_pct, win_rate_pct)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, ticker, start_date, end_date, initial, final, roi, sharpe, max_dd, win_rate))
        self.conn.commit()
        
    def log_project_update(self, module, description):
        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
        INSERT INTO Project_Updates (timestamp, module, description)
        VALUES (?, ?, ?)
        ''', (timestamp, module, description))
        self.conn.commit()
        
    def log_paper_trade_balance(self, btc_bal, eth_bal, sol_bal, usdt_bal, total_val):
        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
        INSERT INTO Paper_Trade_Portfolio (timestamp, btc_bal, eth_bal, sol_bal, usdt_bal, total_usdt_value)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, btc_bal, eth_bal, sol_bal, usdt_bal, total_val))
        self.conn.commit()
        
    def get_latest_decisions(self, limit=5):
        cursor = self.conn.cursor()
        cursor.execute('SELECT timestamp, ticker, price, action, confidence, reasoning FROM Trading_Decisions ORDER BY id DESC LIMIT ?', (limit,))
        return cursor.fetchall()
        
    def get_latest_backtests(self, limit=3):
        cursor = self.conn.cursor()
        cursor.execute('SELECT timestamp, ticker, start_date, end_date, roi_pct, sharpe_ratio, max_drawdown_pct, win_rate_pct FROM Backtest_Reports ORDER BY id DESC LIMIT ?', (limit,))
        return cursor.fetchall()
        
    def get_latest_updates(self, limit=5):
        cursor = self.conn.cursor()
        cursor.execute('SELECT timestamp, module, description FROM Project_Updates ORDER BY id DESC LIMIT ?', (limit,))
        return cursor.fetchall()
        
    def get_paper_trade_history(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute('SELECT timestamp, total_usdt_value FROM Paper_Trade_Portfolio ORDER BY id DESC LIMIT ?', (limit,))
        return cursor.fetchall()
        
    def get_latest_paper_trade_balance(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT btc_bal, eth_bal, sol_bal, usdt_bal, total_usdt_value FROM Paper_Trade_Portfolio ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        if row:
            return {"BTC": row[0], "ETH": row[1], "SOL": row[2], "USDT": row[3], "TOTAL": row[4]}
        return {"BTC": 0.0, "ETH": 0.0, "SOL": 0.0, "USDT": 10000.0, "TOTAL": 10000.0}
        
    def close(self):
        self.conn.close()
