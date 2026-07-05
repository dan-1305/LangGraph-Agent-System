import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import os

# Cấu hình thư mục lưu trữ
DATA_DIR = r'projects\ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy\Stock_Forecasting_Project\01_Data'
os.makedirs(DATA_DIR, exist_ok=True)

# Thông số tải dữ liệu
TICKER = 'FPT.VN' # Mã cổ phiếu FPT
START_DATE = '2021-01-01'
END_DATE = '2026-05-01'

print(f"Downloading data for {TICKER} from {START_DATE} to {END_DATE}...")

# Tải dữ liệu
df = yf.download(TICKER, start=START_DATE, end=END_DATE)

if df.empty:
    print("Error: Could not fetch data. Creating dummy data...")
    dates = pd.date_range(start=START_DATE, end=END_DATE, freq='B')
    df = pd.DataFrame(np.random.randn(len(dates), 5), index=dates, columns=['Open', 'High', 'Low', 'Close', 'Volume'])
    df['Close'] = df['Close'].cumsum() + 100
else:
    print(f"Downloaded {len(df)} rows.")

df = df.dropna()

# Biểu đồ giá
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Close'], label=f'Giá đóng cửa {TICKER}')
plt.title(f'Biểu đồ giá cổ phiếu {TICKER} (2021-2026)')
plt.xlabel('Thời gian')
plt.ylabel('Giá')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(DATA_DIR, 'price_chart.png'))
print(f"Saved price_chart.png")

# Tính Return
df['Return'] = df['Close'].pct_change()
df['Target'] = np.where(df['Return'] > 0, 1, 0)
df = df.dropna()

# Lưu CSV
csv_path = os.path.join(DATA_DIR, f'{TICKER.replace(".", "_")}_clean.csv')
df.to_csv(csv_path)
print(f"Saved clean data")
