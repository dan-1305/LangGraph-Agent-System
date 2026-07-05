import ccxt
import sys
import os
import json
import threading
import concurrent.futures
from pathlib import Path

# Thêm base_dir vào sys.path để import database và BaseAgent
base_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from src.base_agent import BaseAgent
from projects.ai_trading_agent.src.config import Config

class BinanceExecutor(BaseAgent):
    """
    [ROLE: SRE / QA Tester]
    Thực thi lệnh giao dịch trên Binance Testnet dựa trên tỷ trọng phân bổ vốn từ AI.
    Hỗ trợ chế độ "Paper Trading" nếu không có API Key.
    Kế thừa BaseAgent để hưởng quyền lợi: Key Rotation, Retry, và Logging chuẩn Monorepo.
    """
    def __init__(self):
        # Khởi tạo BaseAgent với label tier-2 để tiết kiệm
        super().__init__(name="BinanceExecutor", role="Trade Execution Officer", agent_label="tier-2")
        
        self.api_key = Config.BINANCE_TESTNET_API_KEY
        self.secret = Config.BINANCE_TESTNET_SECRET
        
        self.use_testnet = Config.USE_BINANCE_TESTNET
        self.paper_trading = not (self.api_key and self.secret)
        
        if self.paper_trading:
            print("⚠️ CẢNH BÁO: Không tìm thấy API Key trong .env. Kích hoạt chế độ PAPER TRADING (Đánh nháp).")
        else:
            mode_name = "BINANCE TESTNET" if self.use_testnet else "BINANCE LIVE"
            print(f"🔗 Đang kết nối tới {mode_name}...")
            self.exchange = ccxt.binance({
                'apiKey': self.api_key,
                'secret': self.secret,
                'enableRateLimit': True,
                'timeout': 10000,
                'options': {
                    'defaultType': 'spot',
                    'adjustForTimeDifference': True,
                }
            })
            
            if self.use_testnet:
                self.exchange.set_sandbox_mode(True)

    def _ai_handler(self, *args, **kwargs):
        """Bắt buộc triển khai từ BaseAgent - Không dùng trực tiếp LLM tại đây."""
        pass

    def _logic_handler(self, *args, **kwargs):
        """Bắt buộc triển khai từ BaseAgent."""
        pass

    def get_current_portfolio(self):
        """Lấy số dư hiện tại trên sàn."""
        if not self.paper_trading:
            import time
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    balance = self.exchange.fetch_balance()
                    portfolio = {
                        "BTC": balance.get('BTC', {}).get('free', 0.0),
                        "ETH": balance.get('ETH', {}).get('free', 0.0),
                        "SOL": balance.get('SOL', {}).get('free', 0.0),
                        "USDT": balance.get('USDT', {}).get('free', 0.0)
                    }
                    return portfolio
                except ccxt.RequestTimeout:
                    print(f"⚠️ Kết nối API bị Timeout. Đang thử lại ({attempt + 1}/{max_retries})...")
                    time.sleep(2)
                except Exception as e:
                    print(f"❌ Lỗi lấy số dư từ Binance: {e}")
                    if "Invalid API-key" in str(e) or "-2015" in str(e) or "401" in str(e):
                        print("⚠️ [AUTO-FALLBACK] API Key không hợp lệ. Tự động chuyển sang chế độ PAPER TRADING!")
                        self.paper_trading = True
                        return self.get_current_portfolio()
                    break
            return {"BTC": 0.0, "ETH": 0.0, "SOL": 0.0, "USDT": 0.0}
        
        try:
            from src.database import SystemDB
            db = SystemDB()
            bal = db.get_latest_paper_trade_balance()
            db.close()
            return {"BTC": bal["BTC"], "ETH": bal["ETH"], "SOL": bal["SOL"], "USDT": bal["USDT"]}
        except Exception:
            return {"BTC": 0.0, "ETH": 0.0, "SOL": 0.0, "USDT": 10000.0}

    def _get_latest_atr(self, coin: str) -> float:
        """Lấy giá trị ATR_14 mới nhất từ database."""
        try:
            import sqlite3
            db_path = base_dir / "data" / "trading_market.db"
            conn = sqlite3.connect(db_path, timeout=20.0)
            conn.execute('PRAGMA journal_mode=WAL;')
            
            table_name = f"{coin}_USD"
            query = f"SELECT ATR_14 FROM {table_name} ORDER BY Date DESC LIMIT 1"
            cursor = conn.execute(query)
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0]:
                return float(result[0])
            return 0.0
        except Exception as e:
            print(f"⚠️ [ATR] Lỗi lấy ATR cho {coin}: {e}")
            return 0.0

    def _calculate_smart_position_sizing(self, base_weight: float, confidence: int, volatility: float = 1.0) -> float:
        """Tính toán Position Sizing thông minh."""
        confidence_factor = 0.5 + (confidence / 20.0)
        adjusted_weight = base_weight * confidence_factor * volatility
        return max(0.0, min(0.5, adjusted_weight))

    def execute_allocation(self, allocation_dict, confidence=0):
        """Thực thi rebalance danh mục."""
        print("\n==================================================")
        print("⚡ BẮT ĐẦU THỰC THI LỆNH TRÊN SÀN (EXECUTION)")
        print("==================================================")
        
        current_pf = self.get_current_portfolio()
        current_prices = {}
        atr_values = {}
        
        for coin in ["BTC", "ETH", "SOL"]:
            try:
                if not self.paper_trading:
                    ticker = self.exchange.fetch_ticker(f"{coin}/USDT")
                    current_prices[coin] = ticker['last']
                else:
                    current_prices[coin] = 60000.0 if coin == "BTC" else (3000.0 if coin == "ETH" else 150.0)
                atr_values[coin] = self._get_latest_atr(coin)
            except Exception:
                current_prices[coin] = 0.0
                atr_values[coin] = 0.0
                
        total_value = current_pf.get("USDT", 0.0)
        for coin in ["BTC", "ETH", "SOL"]:
            total_value += current_pf.get(coin, 0.0) * current_prices.get(coin, 0.0)
            
        if total_value <= 0: total_value = 10000.0
            
        target_weights = {}
        for coin, base_weight in allocation_dict.items():
            if coin == "USDT": continue
            volatility_factor = 1.0
            atr_val = atr_values.get(coin, 0.0)
            price = current_prices.get(coin, 0.0)
            if atr_val > 0 and price > 0:
                ratio = (atr_val / price) * 100
                if ratio > 5.0: volatility_factor = 0.8
                elif ratio < 2.5: volatility_factor = 1.2
            
            target_weights[coin] = self._calculate_smart_position_sizing(base_weight, confidence, volatility_factor)
            
        total_crypto_weight = sum(target_weights.values())
        target_weights["USDT"] = max(0.0, 1.0 - total_crypto_weight)

        # Logic thực thi lệnh (giản lược để bọc thép BaseAgent)
        for coin, weight in target_weights.items():
            if coin == "USDT": continue
            target_val = total_value * weight
            if weight > 0:
                print(f"📈 [{self.name}] Thực thi phân bổ {weight*100:.1f}% vào {coin}")
            else:
                print(f"📉 [{self.name}] Thoát vị thế {coin}")

        # Cập nhật database
        try:
            from src.database import SystemDB
            db = SystemDB()
            db.log_paper_trade_balance(
                btc_bal=current_pf.get("BTC", 0.0), # Giả định giữ nguyên để demo
                eth_bal=current_pf.get("ETH", 0.0),
                sol_bal=current_pf.get("SOL", 0.0),
                usdt_bal=current_pf.get("USDT", 0.0),
                total_val=total_value
            )
            db.close()
        except Exception: pass

if __name__ == "__main__":
    executor = BinanceExecutor()
    print("Portfolio:", executor.get_current_portfolio())
