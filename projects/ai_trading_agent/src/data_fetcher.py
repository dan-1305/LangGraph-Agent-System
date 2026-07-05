import yfinance as yf
import pandas as pd
import requests
import sqlite3
from pathlib import Path
import sys
from datetime import datetime, timedelta
from typing import List, Optional

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Setup sys.path để tránh Dependency Hell khi được gọi từ Scheduler
ai_trading_src_dir = Path(__file__).resolve().parent
ai_trading_root_dir = ai_trading_src_dir.parent
base_dir = ai_trading_root_dir.parent.parent

if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))
# Không thêm ai_trading_root_dir vào sys.path để tránh shadowing 'src'
if str(ai_trading_src_dir) not in sys.path:
    sys.path.insert(0, str(ai_trading_src_dir))

# Chuyển từ src.config sang import trực tiếp config vì đã add thư mục src vào path
import config as Config_Module
Config = Config_Module.Config

def get_trade_tickers() -> List[str]:
    """Lấy danh sách các cặp giao dịch từ cấu hình."""
    return Config.TRADE_TICKERS

def fetch_fear_and_greed(limit: int = 300) -> pd.DataFrame:
    """Lấy chỉ số Fear & Greed Index từ API của Alternative.me."""
    url = f"https://api.alternative.me/fng/?limit={limit}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data['metadata']['error'] is None:
            fng_data = []
            for item in data['data']:
                date_str = datetime.fromtimestamp(int(item['timestamp'])).strftime('%Y-%m-%d')
                fng_data.append({
                    'Date': date_str,
                    'FNG_Value': int(item['value']),
                    'FNG_Class': item['value_classification']
                })
            df_fng = pd.DataFrame(fng_data)
            # Dữ liệu API trả về từ mới nhất đến cũ nhất, ta cần đảo ngược lại
            df_fng = df_fng.sort_values(by='Date').reset_index(drop=True)
            return df_fng
    except Exception as e:
        print(f"⚠️ Lỗi khi lấy Fear & Greed: {e}")
    return pd.DataFrame()

def fetch_crypto_data(tickers: Optional[List[str]] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
    """
    Kéo dữ liệu OHLCV lịch sử từ Yahoo Finance và lưu vào SQLite.
    Bổ sung lấy Fear & Greed Index.
    IMPROVEMENT: Data Caching - chỉ fetch data mới nhất (Incremental Update).
    """
    if tickers is None:
        tickers = get_trade_tickers()
        
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=270)).strftime("%Y-%m-%d")
        
    data_dir = Config.DATA_DIR
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = Config.DB_PATH
    conn = sqlite3.connect(db_path, timeout=20.0)
    conn.execute('PRAGMA journal_mode=WAL;')
    
    # 1. Lấy Fear & Greed
    print("🔄 Đang lấy Fear & Greed Index...")
    df_fng = fetch_fear_and_greed(limit=300)
    
    # 2. Lấy dữ liệu từng Ticker (Với Data Caching)
    for ticker in tickers:
        table_name = ticker.replace("-", "_")
        
        # KIỂM TRA CACHE: Tìm ngày mới nhất trong DB
        latest_date = None
        try:
            check_query = f"SELECT MAX(Date) as latest_date FROM {table_name}"
            cursor = conn.execute(check_query)
            result = cursor.fetchone()
            if result and result[0]:
                latest_date = result[0]
                print(f"💾 [CACHE] Tìm thấy data cũ mới nhất: {latest_date}")
        except Exception:
            print(f"💾 [CACHE] Bảng {table_name} chưa tồn tại, sẽ fetch toàn bộ data.")
        
        # TỐN ƯU: Chỉ fetch data mới (từ ngày hôm sau latest_date)
        if latest_date:
            # Tính start_date mới: ngày hôm sau của latest_date
            latest_dt = datetime.strptime(latest_date, '%Y-%m-%d')
            new_start_date = (latest_dt + timedelta(days=1)).strftime("%Y-%m-%d")
            print(f"🔄 [INCREMENTAL] Chỉ fetch data từ {new_start_date} đến {end_date}...")
            df_new = yf.download(ticker, start=new_start_date, end=end_date, progress=False)
            
            if df_new.empty:
                print(f"✅ [UP-TO-DATE] {ticker}: Không có data mới để cập nhật.")
                continue
            
            # Đọc lại toàn bộ data cũ để tính lại Indicators
            df_old = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            df_old['Date'] = pd.to_datetime(df_old['Date'])
            df_new = df_new.reset_index()
            df_new['Date'] = pd.to_datetime(df_new['Date'])
            
            # Merge data cũ + mới
            df = pd.concat([df_old, df_new], ignore_index=True)
            df = df.sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
        else:
            # Không có cache: fetch toàn bộ data
            print(f"🔄 [FULL FETCH] Đang tải dữ liệu {ticker} từ {start_date} đến {end_date}...")
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        if df.empty:
            print(f"❌ Không tìm thấy dữ liệu cho {ticker}.")
            continue
            
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        df = df.reset_index()
        # Chuẩn hóa format Date
        if pd.api.types.is_datetime64_any_dtype(df['Date']):
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
            
        # Tính toán chỉ báo (Technical Indicators)
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        
        # RSI (Relative Strength Index)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI_14'] = 100 - (100 / (1 + rs))
        
        # MACD (Moving Average Convergence Divergence)
        ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = ema_12 - ema_26
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        # Bollinger Bands
        sma_20 = df['Close'].rolling(window=20).mean()
        std_20 = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = sma_20 + (std_20 * 2)
        df['BB_Middle'] = sma_20
        df['BB_Lower'] = sma_20 - (std_20 * 2)
        df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Middle']
        
        # ATR (Average True Range) - Cho Stop-Loss động
        high_low = df['High'] - df['Low']
        high_close = (df['High'] - df['Close'].shift(1)).abs()
        low_close = (df['Low'] - df['Close'].shift(1)).abs()
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['ATR_14'] = true_range.rolling(window=14).mean()
        
        # Merge với Fear & Greed
        if not df_fng.empty and 'Date' in df.columns:
            df = pd.merge(df, df_fng, on='Date', how='left')
            # Fill missing FNG values bằng forward fill
            if 'FNG_Value' in df.columns:
                df['FNG_Value'] = df['FNG_Value'].ffill()
            if 'FNG_Class' in df.columns:
                df['FNG_Class'] = df['FNG_Class'].ffill()
            
        # Chuẩn hóa Date trước khi tính indicators
        if pd.api.types.is_datetime64_any_dtype(df['Date']):
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        # DROPNA sau khi đã merge và chuẩn hóa
        df = df.dropna().reset_index(drop=True)
        
        # LƯU: Replace toàn bộ bảng (đơn giản và đảm bảo consistency)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"✅ [SAVED] Đã lưu {len(df)} dòng dữ liệu {ticker} vào bảng {table_name}")
        
    conn.close()
    return str(db_path)

if __name__ == "__main__":
    fetch_crypto_data()