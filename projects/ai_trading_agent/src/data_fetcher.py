import yfinance as yf
import pandas as pd
import os
import requests
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load biến môi trường từ thư mục gốc
base_dir_env = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(base_dir_env / ".env")

def get_trade_tickers():
    tickers_str = os.getenv("TRADE_TICKERS", "BTC-USD,ETH-USD,SOL-USD")
    return [t.strip() for t in tickers_str.split(',')]

def fetch_fear_and_greed(limit=300):
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

def fetch_crypto_data(tickers=None, start_date=None, end_date=None):
    """
    Kéo dữ liệu OHLCV lịch sử từ Yahoo Finance và lưu vào SQLite.
    Bổ sung lấy Fear & Greed Index.
    """
    if tickers is None:
        tickers = get_trade_tickers()
        
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=270)).strftime("%Y-%m-%d")
        
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = data_dir / "trading_market.db"
    conn = sqlite3.connect(db_path)
    
    # 1. Lấy Fear & Greed
    print("🔄 Đang lấy Fear & Greed Index...")
    df_fng = fetch_fear_and_greed(limit=300)
    
    # 2. Lấy dữ liệu từng Ticker
    for ticker in tickers:
        print(f"🔄 Đang tải dữ liệu {ticker} từ {start_date} đến {end_date}...")
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
        if not df_fng.empty:
            df = pd.merge(df, df_fng, on='Date', how='left')
            # Fill missing FNG values bằng forward fill
            df['FNG_Value'] = df['FNG_Value'].ffill()
            df['FNG_Class'] = df['FNG_Class'].ffill()
            
        df = df.dropna().reset_index(drop=True)
        
        table_name = ticker.replace("-", "_")
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"✅ Đã lưu {len(df)} dòng dữ liệu {ticker} vào bảng {table_name}")
        
    conn.close()
    return str(db_path)

if __name__ == "__main__":
    fetch_crypto_data()