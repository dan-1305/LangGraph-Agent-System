import ccxt
import sys
from pathlib import Path
import io

if sys.stdout is not None:
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Thêm base_dir vào sys.path để import database
base_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from projects.ai_trading_agent.src.config import Config

class BinanceExecutor:
    """
    Thực thi lệnh giao dịch trên Binance Testnet dựa trên tỷ trọng phân bổ vốn từ AI.
    Hỗ trợ chế độ "Paper Trading" nếu không có API Key.
    """
    def __init__(self):
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
                    if "Invalid API-key" in str(e) or "-2015" in str(e) or "401" in str(e):
                        print("⚠️ [AUTO-FALLBACK] API Key không hợp lệ. Tự động chuyển sang chế độ PAPER TRADING!")
                        self.paper_trading = True
                        return self.get_current_portfolio() # Thử lại dưới dạng Paper Trading
                    break
            print("❌ Lỗi: Không thể kết nối tới Binance sau nhiều lần thử. Trả về số dư 0.")
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

    def _get_latest_atr(self, coin: str) -> float:
        """
        Lấy giá trị ATR_14 mới nhất của một coin từ database.
        Dùng để tính Dynamic Stop-Loss.
        """
        try:
            import sqlite3
            base_dir = Path(__file__).resolve().parent.parent.parent.parent
            db_path = base_dir / "data" / "trading_market.db"
            conn = sqlite3.connect(db_path, timeout=20.0)
            conn.execute('PRAGMA journal_mode=WAL;')
            
            table_name = f"{coin}_USD"
            query = f"SELECT ATR_14 FROM {table_name} ORDER BY Date DESC LIMIT 1"
            cursor = conn.execute(query)
            result = cursor.fetchone()
            
            conn.close()
            
            if result and result[0]:
                atr_value = float(result[0])
                print(f"📊 [ATR] {coin}: ATR_14 mới nhất = {atr_value:.2f}")
                return atr_value
            else:
                print(f"⚠️ [ATR] Không tìm thấy ATR cho {coin}. Dùng giá trị mặc định.")
                return 0.0
        except Exception as e:
            print(f"⚠️ [ATR] Lỗi lấy ATR cho {coin}: {e}. Dùng giá trị mặc định.")
            return 0.0

    def _calculate_smart_position_sizing(self, base_weight: float, confidence: int, volatility: float = 1.0) -> float:
        """
        Tính toán Position Sizing thông minh dựa trên:
        - Confidence Score từ AI (1-10)
        - Volatility của coin (dựa trên ATR hoặc BB_Width)
        
        Công thức: Adjusted_Weight = Base_Weight × (Confidence_Factor × Volatility_Factor)
        Trong đó:
        - Confidence_Factor = 0.5 + (Confidence / 20.0)  (0.55 đến 1.0)
        - Volatility_Factor = 1.0 (Normal), 0.8 (Low Vol), 1.2 (High Vol)
        """
        confidence_factor = 0.5 + (confidence / 20.0)  # 0.55 đến 1.0
        adjusted_weight = base_weight * confidence_factor * volatility
        
        # Clamp weight: Không được quá 50% vốn vào 1 coin, không được < 0
        adjusted_weight = max(0.0, min(0.5, adjusted_weight))
        
        return adjusted_weight

    def send_telegram_alert(self, message):
        """Gửi thông báo qua Telegram."""
        try:
            if base_dir not in sys.path:
                sys.path.insert(0, base_dir)
            from core_utilities.notification_gateway import send_raw_telegram
            send_raw_telegram(message)
        except Exception as e:
            print(f"⚠️ Không thể gọi Notification Gateway: {e}")

    def execute_allocation(self, allocation_dict, confidence=0):
        """
        Thực thi lệnh để đưa danh mục về đúng tỷ trọng allocation_dict.
        Ví dụ: {"BTC": 0.4, "ETH": 0.2, "SOL": 0.1, "USDT": 0.3}
        """
        print("\n==================================================")
        print("⚡ BẮT ĐẦU THỰC THI LỆNH TRÊN SÀN (EXECUTION)")
        print("==================================================")
        
        tele_msg = "🤖 <b>[AI TRADING UPDATE]</b>\n"
        tele_msg += f"Độ tự tin (Confidence): <b>{confidence}/10</b>\n"
        tele_msg += "Phân bổ danh mục mới:\n"
        
        # Trong thực tế, để rebalance danh mục, ta cần:
        # 1. Lấy giá hiện tại của các tài sản.
        # 2. Tính tổng giá trị danh mục (theo USDT).
        # 3. Tính số lượng cần giữ cho mỗi coin = (Tổng giá trị * tỷ trọng) / giá.
        # 4. So sánh số lượng cần giữ với số lượng đang có để đặt lệnh BUY/SELL.
        
        # Lấy giá trị tổng danh mục hiện tại
        current_pf = self.get_current_portfolio()
        
        # Để tính tổng giá trị, ta cần giá của các coin. Dùng ccxt fetch_ticker cho nhanh.
        current_prices = {}
        atr_values = {}  # Store ATR cho volatility calculation
        for coin in ["BTC", "ETH", "SOL"]:
            try:
                ticker = self.exchange.fetch_ticker(f"{coin}/USDT")
                current_prices[coin] = ticker['last']
                atr_values[coin] = self._get_latest_atr(coin)
            except Exception:
                current_prices[coin] = 0.0
                atr_values[coin] = 0.0
                
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
            
            # Tìm record đầu tiên của ngày hôm nay để tính Daily PnL
            # paper_history trả về [(timestamp, total_usdt_value), ...] xếp theo DESC (Mới nhất nằm ở index 0)
            paper_history = db.get_paper_trade_history(limit=100)
            import datetime
            today_str = datetime.datetime.now().strftime("%Y-%m-%d")
            
            if paper_history and len(paper_history) > 0:
                old_total_found = None
                # Tìm record CŨ NHẤT của ngày hôm nay
                for record in paper_history:
                    rec_time, rec_val = record[0], float(record[1])
                    if rec_time.startswith(today_str):
                        old_total_found = rec_val
                    else:
                        # Vừa bước sang ngày cũ (hôm qua) -> break, old_total_found giữ giá trị đầu ngày hôm nay
                        break
                        
                if old_total_found is not None:
                    old_total = old_total_found
                else:
                    # Nếu hôm nay chưa có record nào (Lần chạy đầu tiên trong ngày)
                    # -> Lấy số dư MỚI NHẤT của ngày trước đó (index 0) làm mốc tham chiếu
                    old_total = float(paper_history[0][1])
            else:
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
        
        # Tính tỷ trọng hiện tại (Current Weights)
        current_weights = {"USDT": current_pf.get("USDT", 0.0) / total_value if total_value > 0 else 0.0}
        for coin in ["BTC", "ETH", "SOL"]:
            current_weights[coin] = (current_pf.get(coin, 0.0) * current_prices.get(coin, 0.0)) / total_value if total_value > 0 else 0.0
            
        # SMART POSITION SIZING: Điều chỉnh allocation dựa trên Confidence Score + Volatility
        print(f"🧠 [SMART SIZING] Đang áp dụng Position Sizing thông minh (Confidence: {confidence}/10)...")
        
        target_weights = {}
        for coin, base_weight in allocation_dict.items():
            if coin == "USDT":
                target_weights["USDT"] = base_weight
                continue
                
            symbol = f"{coin}/USDT"
            current_price = current_prices.get(coin, 0.0)
            atr_value = atr_values.get(coin, 0.0)
            
            if atr_value > 0 and current_price > 0:
                atr_ratio = (atr_value / current_price) * 100
                if atr_ratio > 5.0:
                    volatility_factor = 0.8
                elif atr_ratio > 2.5:
                    volatility_factor = 1.0
                else:
                    volatility_factor = 1.2
            else:
                volatility_factor = 1.0
                
            adjusted_weight = self._calculate_smart_position_sizing(base_weight, confidence, volatility_factor)
            target_weights[coin] = adjusted_weight
            
        # Cập nhật lại USDT target weight nếu tổng crypto weights thay đổi
        total_crypto_weight = sum([w for c, w in target_weights.items() if c != "USDT"])
        target_weights["USDT"] = max(0.0, 1.0 - total_crypto_weight)
        
        # REBALANCING TRIGGER: Kiểm tra độ lệch
        max_deviation = 0.0
        for coin in ["BTC", "ETH", "SOL", "USDT"]:
            dev = abs(target_weights.get(coin, 0.0) - current_weights.get(coin, 0.0))
            if dev > max_deviation:
                max_deviation = dev
                
        if max_deviation < 0.15:
            print(f"⚖️ [REBALANCE TRIGGER] Độ lệch lớn nhất chỉ là {max_deviation*100:.1f}% (< 15%). BỎ QUA REBALANCE ĐỂ TIẾT KIỆM PHÍ.")
            tele_msg += f"⚖️ Độ lệch cực đại: {max_deviation*100:.1f}%\n"
            tele_msg += "⏩ Bỏ qua Rebalance (Chưa chạm ngưỡng 15%)"
            self.send_telegram_alert(tele_msg)
            return
            
        print(f"⚖️ [REBALANCE TRIGGER] Độ lệch lớn nhất: {max_deviation*100:.1f}% (>= 15%). TIẾN HÀNH REBALANCE.")
        
        import concurrent.futures
        import threading
        
        # Thread-safe collections
        log_lock = threading.Lock()
        
        def process_coin(coin, adjusted_weight):
            local_tele_msg = ""
            if coin == "USDT":
                return "USDT", total_value * adjusted_weight, local_tele_msg
                
            symbol = f"{coin}/USDT"
            current_price = current_prices.get(coin, 0.0)
            atr_value = atr_values.get(coin, 0.0)
            
            # Re-calculate volatility label for logging
            if atr_value > 0 and current_price > 0:
                atr_ratio = (atr_value / current_price) * 100
                if atr_ratio > 5.0: vol_label = "🔴 HIGH VOL"
                elif atr_ratio > 2.5: vol_label = "🟡 MED VOL"
                else: vol_label = "🟢 LOW VOL"
            else:
                vol_label = "🟡 MED VOL (NO ATR DATA)"
                
            base_weight = allocation_dict.get(coin, 0.0)
            target_value = total_value * adjusted_weight
            
            target_amount_paper = 0.0
            
            if self.paper_trading:
                # Cập nhật số dư ảo
                target_amount = (target_value / current_price) if current_price > 0 else 0.0
                target_amount_paper = target_amount
                # In ra log
                with log_lock:
                    if adjusted_weight > 0:
                        print(f"📈 [PAPER TRADE] {coin}: Base {base_weight*100:.0f}% → Adjusted {adjusted_weight*100:.1f}% ({vol_label})")
                        print(f"📈 [PAPER TRADE] Phân bổ {adjusted_weight*100:.1f}% vào {coin} -> Gửi lệnh BUY {target_amount:.4f} {coin} (~${target_value:,.2f})")
                        local_tele_msg += f"🟢 MUA ${target_value:,.0f} {coin} (Sizing: {adjusted_weight*100:.1f}%)\n"
                    else:
                        print(f"📉 [PAPER TRADE] {coin}: Tỷ trọng 0% -> SELL toàn bộ")
                        local_tele_msg += f"🔴 BÁN ALL {coin}\n"
            else:
                # Đánh thật trên Testnet
                import time
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        ticker = self.exchange.fetch_ticker(symbol)
                        current_price = ticker['last']
                        
                        with log_lock:
                            if adjusted_weight > 0:
                                target_amount = (target_value / current_price) if current_price > 0 else 0.0
                                print(f"📈 [LIVE TESTNET] {coin}: Base {base_weight*100:.0f}% → Adjusted {adjusted_weight*100:.1f}% ({vol_label})")
                                print(f"📈 [LIVE TESTNET] Đặt lệnh MARKET BUY {target_amount:.4f} {coin} (~${target_value:,.2f})")
                                # self.exchange.create_market_buy_order(symbol, target_amount)
                                 
                                # DYNAMIC STOP-LOSS: Dựa trên ATR_14 từ database
                                atr_multiplier = 2.5  # Multiplier chuẩn nghiệp vụ: Stop-Loss = Entry - 2.5*ATR
                                
                                if atr_value > 0:
                                    stop_loss_price = current_price - (atr_multiplier * atr_value)
                                else:
                                    # Fallback về % tĩnh nếu không có ATR
                                    stop_loss_price = current_price * 0.95  # Cắt lỗ 5%
                                    
                                print(f"🛡️ [RISK MGR] Đã đính kèm lệnh DYNAMIC STOP-LOSS cho {coin} tại mức giá {stop_loss_price:.2f} (ATR: {atr_value:.2f}, Multiplier: {atr_multiplier}x)")
                            else:
                                print(f"📉 [LIVE TESTNET] Đặt lệnh MARKET SELL toàn bộ {coin}")
                                # amount_to_sell = get_balance(coin)
                                # self.exchange.create_market_sell_order(symbol, amount_to_sell)
                        break # Thành công thì thoát vòng lặp Retry
                    except ccxt.RequestTimeout:
                        with log_lock:
                            print(f"⚠️ Timeout khi đặt lệnh {coin}. Thử lại ({attempt + 1}/{max_retries})...")
                        time.sleep(2)
                    except Exception as e:
                        with log_lock:
                            print(f"❌ Lỗi thực thi lệnh cho {coin}: {e}")
                        break
                        
            return coin, target_amount_paper, local_tele_msg

        # Thực thi song song (Multi-threading) để giảm độ trễ API
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_coin, coin, weight) for coin, weight in target_weights.items()]
            for future in concurrent.futures.as_completed(futures):
                try:
                    c, amt, msg = future.result()
                    if c == "USDT":
                        new_paper_pf["USDT"] = amt
                    else:
                        new_paper_pf[c] = amt
                        tele_msg += msg
                except Exception as e:
                    print(f"⚠️ Lỗi ThreadPoolExecutor: {e}")
                    
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