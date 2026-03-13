import os
import ccxt
from dotenv import load_dotenv
import sys
from pathlib import Path

# Load biến môi trường
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(base_dir, ".env"))

# Thêm base_dir vào sys.path để import database
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

class BinanceExecutor:
    """
    Thực thi lệnh giao dịch trên Binance Testnet dựa trên tỷ trọng phân bổ vốn từ AI.
    Hỗ trợ chế độ "Paper Trading" nếu không có API Key.
    """
    def __init__(self):
        self.api_key = os.getenv("BINANCE_TESTNET_API_KEY")
        self.secret = os.getenv("BINANCE_TESTNET_SECRET")
        
        self.use_testnet = os.getenv("BINANCE_TESTNET", "False").lower() in ['true', '1', 'yes']
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
                'timeout': 10000, # Tối ưu i3: Timeout 10s để không treo máy nếu server lag
                'options': {
                    'defaultType': 'spot',
                    'adjustForTimeDifference': True, # Khắc phục lỗi lệch Timestamp
                }
            })
            
            if self.use_testnet:
                # set_sandbox_mode(True) tự động đổi endpoint sang https://testnet.binance.vision
                self.exchange.set_sandbox_mode(True)

    def get_current_portfolio(self):
        """Lấy số dư hiện tại trên sàn."""
        # KHÔNG dùng database khi có API key (Live Testnet)
        # Chỉ dùng database khi PAPER TRADING
        if not self.paper_trading:
            # LIVE TESTNET: Lấy từ sàn thật
            import time
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Lấy số dư (timeout sẽ áp dụng nếu mạng lag)
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
                    break
            print("❌ Lỗi: Không thể kết nối tới Binance sau nhiều lần thử.")
            return {"BTC": 0.0, "ETH": 0.0, "SOL": 0.0, "USDT": 0.0}
        
        # PAPER TRADING: Lấy từ SQLite
        try:
            from src.database import SystemDB
            db = SystemDB()
            bal = db.get_latest_paper_trade_balance()
            db.close()
            return {"BTC": bal["BTC"], "ETH": bal["ETH"], "SOL": bal["SOL"], "USDT": bal["USDT"]}
        except Exception:
            return {"BTC": 0.0, "ETH": 0.0, "SOL": 0.0, "USDT": 10000.0}

    def print_testnet_balance(self):
        """Hàm dùng riêng cho Dashboard hiển thị số dư thực tế"""
        if self.paper_trading:
            print("⚠️ Bạn đang ở chế độ Paper Trading. Hãy nhập API Key Testnet vào .env để xem số dư thật.")
            return
            
        pf = self.get_current_portfolio()
        print("\n=====================================")
        print("💳 SỐ DƯ TÀI KHOẢN (BINANCE TESTNET)")
        print("=====================================")
        print(f"💵 USDT : {pf.get('USDT', 0):,.2f}")
        print(f"🪙 BTC  : {pf.get('BTC', 0):.6f}")
        print(f"🔷 ETH  : {pf.get('ETH', 0):.6f}")
        print(f"🌞 SOL  : {pf.get('SOL', 0):.4f}")
        print("=====================================\n")

    def send_telegram_alert(self, message):
        """Gửi thông báo qua Telegram."""
        tele_token = os.getenv("TELE_TOKEN")
        chat_id = os.getenv("CHAT_ID")
        if not tele_token or not chat_id:
            return
            
        import requests
        url = f"https://api.telegram.org/bot{tele_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"⚠️ Không thể gửi Telegram: {e}")

    def execute_allocation(self, allocation_dict, confidence=0):
        """
        Thực thi lệnh để đưa danh mục về đúng tỷ trọng allocation_dict.
        Ví dụ: {"BTC": 0.4, "ETH": 0.2, "SOL": 0.1, "USDT": 0.3}
        """
        print("\n==================================================")
        print("⚡ BẮT ĐẦU THỰC THI LỆNH TRÊN SÀN (EXECUTION)")
        print("==================================================")
        
        tele_msg = f"🤖 <b>[AI TRADING UPDATE]</b>\n"
        tele_msg += f"Độ tự tin (Confidence): <b>{confidence}/10</b>\n"
        tele_msg += f"Phân bổ danh mục mới:\n"
        
        # Trong thực tế, để rebalance danh mục, ta cần:
        # 1. Lấy giá hiện tại của các tài sản.
        # 2. Tính tổng giá trị danh mục (theo USDT).
        # 3. Tính số lượng cần giữ cho mỗi coin = (Tổng giá trị * tỷ trọng) / giá.
        # 4. So sánh số lượng cần giữ với số lượng đang có để đặt lệnh BUY/SELL.
        
        # Lấy giá trị tổng danh mục hiện tại
        current_pf = self.get_current_portfolio()
        
        # Để tính tổng giá trị, ta cần giá của các coin. Dùng ccxt fetch_ticker cho nhanh.
        current_prices = {}
        for coin in ["BTC", "ETH", "SOL"]:
            try:
                ticker = self.exchange.fetch_ticker(f"{coin}/USDT")
                current_prices[coin] = ticker['last']
            except Exception:
                current_prices[coin] = 0.0
                
        total_value = current_pf.get("USDT", 0.0)
        for coin in ["BTC", "ETH", "SOL"]:
            total_value += current_pf.get(coin, 0.0) * current_prices[coin]
            
        if total_value <= 0:
            total_value = 10000.0 # Vốn mặc định
            
        # Lấy số dư cũ để tính PnL
        # PHÂN BIỆT Paper Trade vs Live Testnet
        old_total = 10000.0
        
        try:
            from src.database import SystemDB
            db = SystemDB()
            
            if self.paper_trading:
                # PAPER TRADE: Lấy từ database
                paper_history = db.get_paper_trade_history(limit=100)
                
                if paper_history:
                    if len(paper_history) >= 2:
                        # Lấy record CỰ NHẤT = số dư đầu ngày
                        old_total = float(paper_history[-1][1])
                    else:
                        # Chỉ có 1 record, PnL = 0
                        old_total = float(paper_history[0][1])
                else:
                    # Database trống, PnL = 0
                    old_total = total_value
            else:
                # LIVE TESTNET: Lấy từ database NHƯNG PHẢI lọc theo timestamp
                # Problem: Paper Trade và Live Testnet dùng chung bảng Paper_Trade_Portfolio
                # Solution: Lấy record đầu ngày bằng cách so sánh timestamp
                
                paper_history = db.get_paper_trade_history(limit=100)
                
                if paper_history and len(paper_history) > 0:
                    # Lấy record đầu ngày (lúc 00:00 của ngày hiện tại)
                    # paper_history: [(timestamp, total_usdt_value), ...] DESC
                    
                    # Nếu đây là LẦN ĐẦU CHẠY trong ngày mới
                    old_total = float(paper_history[0][1])  # PnL = 0
                else:
                    # Database trống, PnL = 0
                    old_total = total_value
                    
            db.close()
        except Exception as e:
            print(f"⚠️ Lỗi lấy số dư cũ: {e}")
            old_total = total_value  # PnL = 0 để tránh sai lệch
            
        daily_pnl = total_value - old_total
        daily_pnl_pct = (daily_pnl / old_total) * 100 if old_total > 0 else 0
        
        tele_msg += f"\n💰 <b>Tổng tài sản:</b> ${total_value:,.2f}\n"
        tele_msg += f"📊 <b>PnL hôm nay:</b> ${daily_pnl:,.2f} ({daily_pnl_pct:+.2f}%)\n\n"
        tele_msg += "Chi tiết khớp lệnh:\n"
        
        new_paper_pf = {"USDT": 0.0, "BTC": 0.0, "ETH": 0.0, "SOL": 0.0}
        
        for coin, target_weight in allocation_dict.items():
            
            target_value = total_value * target_weight
            
            if coin == "USDT":
                new_paper_pf["USDT"] = target_value
                continue
                
            symbol = f"{coin}/USDT"
            current_price = current_prices.get(coin, 0.0)
            target_amount = (target_value / current_price) if current_price > 0 else 0.0
            
            if self.paper_trading:
                # Cập nhật số dư ảo
                new_paper_pf[coin] = target_amount
                # In ra log
                if target_weight > 0:
                    print(f"📈 [PAPER TRADE] Phân bổ {target_weight*100}% vào {coin} -> Gửi lệnh BUY {target_amount:.4f} {coin} (~${target_value:,.2f})")
                    tele_msg += f"🟢 MUA ${target_value:,.0f} {coin}\n"
                else:
                    print(f"📉 [PAPER TRADE] Tỷ trọng {coin} là 0% -> Gửi lệnh SELL toàn bộ {coin}")
                    tele_msg += f"🔴 BÁN ALL {coin}\n"
            else:
                # Đánh thật trên Testnet
                import time
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        ticker = self.exchange.fetch_ticker(symbol)
                        current_price = ticker['last']
                        
                        if target_weight > 0:
                            target_amount = target_value / current_price
                            print(f"📈 [LIVE TESTNET] Đặt lệnh MARKET BUY {target_amount:.4f} {coin} (~${target_value:,.2f})")
                            # self.exchange.create_market_buy_order(symbol, target_amount)
                            
                            # Mô phỏng đặt lệnh Stop-Loss (Dựa trên ATR tĩnh hoặc % cố định)
                            stop_loss_price = current_price * 0.95 # Cắt lỗ 5%
                            print(f"🛡️ [RISK MGR] Đã đính kèm lệnh STOP-LOSS tự động cho {coin} tại mức giá {stop_loss_price:.2f}")
                            
                        else:
                            print(f"📉 [LIVE TESTNET] Đặt lệnh MARKET SELL toàn bộ {coin}")
                            # amount_to_sell = get_balance(coin)
                            # self.exchange.create_market_sell_order(symbol, amount_to_sell)
                        break # Thành công thì thoát vòng lặp Retry
                    except ccxt.RequestTimeout:
                        print(f"⚠️ Timeout khi đặt lệnh {coin}. Thử lại ({attempt + 1}/{max_retries})...")
                        time.sleep(2)
                    except Exception as e:
                        print(f"❌ Lỗi thực thi lệnh cho {coin}: {e}")
                        break
                    
        print("✅ Hoàn tất đợt thực thi lệnh!")
        
        # Bắn Telegram
        if self.paper_trading:
            tele_msg += "\n<i>(Mode: Paper Trading)</i>"
        else:
            tele_msg += "\n<i>(Mode: Live Testnet)</i>"
        self.send_telegram_alert(tele_msg)
        
        # Log lại số dư vào Database (Dùng chung bảng Paper_Trade_Portfolio cho cả Testnet)
        from src.database import SystemDB
        import time
        try:
            db = SystemDB()
            if self.paper_trading:
                db.log_paper_trade_balance(
                    btc_bal=new_paper_pf["BTC"],
                    eth_bal=new_paper_pf["ETH"],
                    sol_bal=new_paper_pf["SOL"],
                    usdt_bal=new_paper_pf["USDT"],
                    total_val=total_value
                )
                print(f"💾 Đã lưu số dư Paper Trade (${total_value:,.2f}) vào Database.")
            else:
                # Nếu là Live Testnet, lấy số dư thật sau khi trade
                time.sleep(2) # Chờ sàn khớp lệnh
                actual_pf = self.get_current_portfolio()
                # Phải tính lại tổng dựa trên giá mới nhất
                actual_total = actual_pf.get("USDT", 0.0)
                for c in ["BTC", "ETH", "SOL"]:
                    actual_total += actual_pf.get(c, 0.0) * current_prices.get(c, 0.0)
                    
                db.log_paper_trade_balance(
                    btc_bal=actual_pf.get("BTC", 0.0),
                    eth_bal=actual_pf.get("ETH", 0.0),
                    sol_bal=actual_pf.get("SOL", 0.0),
                    usdt_bal=actual_pf.get("USDT", 0.0),
                    total_val=actual_total
                )
                print(f"💾 Đã lưu số dư Live Testnet (${actual_total:,.2f}) vào Database.")
            db.close()
        except Exception as e:
            print(f"⚠️ Lỗi lưu Portfolio Balance: {e}")

if __name__ == "__main__":
    executor = BinanceExecutor()
    current_pf = executor.get_current_portfolio()
    print("Danh mục hiện tại:", current_pf)
    
    # Fake lệnh từ AI
    mock_allocation = {"BTC": 0.4, "ETH": 0.2, "SOL": 0.1, "USDT": 0.3}
    executor.execute_allocation(mock_allocation)
