import time
import json
import logging
import projects.ai_trading_agent.src.config as Config_Module
Config = Config_Module.Config

# Setup logging
logging.basicConfig(
    filename=Config.DATA_DIR / "trading_analytics.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Analytics:
    """
    Module đo lường và ghi nhận hiệu suất của AI Trading Agent.
    Theo dõi: Thời gian thực thi, Chi phí API (token), PnL, Tỷ lệ thắng/thua.
    """
    
    def __init__(self):
        self.start_time = time.time()
        self.log_file = Config.DATA_DIR / "analytics_summary.json"
        self._ensure_log_file()
        
    def _ensure_log_file(self):
        if not self.log_file.exists():
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def log_execution_time(self, task_name: str, start_time: float):
        """Ghi nhận thời gian thực thi của một task."""
        duration = time.time() - start_time
        logging.info(f"Task '{task_name}' completed in {duration:.2f} seconds.")
        return duration

    def log_api_cost(self, service: str, tokens: int, estimated_cost: float):
        """Ghi nhận chi phí sử dụng API (LLM, Data)."""
        logging.info(f"API Cost ({service}): {tokens} tokens ~ ${estimated_cost:.6f}")
        
    def log_trade_performance(self, trade_data: dict):
        """
        Ghi nhận kết quả giao dịch.
        trade_data: {
            'timestamp': '...',
            'ticker': 'BTC-USD',
            'action': 'BUY/SELL',
            'price': 50000,
            'pnl': 100, 
            'roi': 0.02
        }
        """
        try:
            with open(self.log_file, "r+", encoding="utf-8") as f:
                data = json.load(f)
                data.append(trade_data)
                f.seek(0)
                json.dump(data, f, indent=4)
            logging.info(f"Trade Logged: {trade_data}")
        except Exception as e:
            logging.error(f"Failed to log trade performance: {e}")

    def get_summary(self):
        """Tính toán tổng hợp hiệu suất."""
        if not self.log_file.exists():
            return {}
            
        with open(self.log_file, "r", encoding="utf-8") as f:
            trades = json.load(f)
            
        if not trades:
            return {"total_trades": 0, "total_pnl": 0}
            
        total_pnl = sum(t.get('pnl', 0) for t in trades)
        win_trades = sum(1 for t in trades if t.get('pnl', 0) > 0)
        
        return {
            "total_trades": len(trades),
            "total_pnl": total_pnl,
            "win_rate": (win_trades / len(trades)) * 100 if trades else 0
        }
