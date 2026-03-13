import sqlite3
import pandas as pd
from pathlib import Path

# Connect to database
base_dir = Path(__file__).resolve().parent
db_path = base_dir.parent.parent.parent / "data" / "trading_market.db"
conn = sqlite3.connect(db_path)

# Get table info for BTC_USD
query = "PRAGMA table_info(BTC_USD)"
df = pd.read_sql(query, conn)
print("=" * 60)
print("📊 DATABASE SCHEMA - BTC_USD TABLE")
print("=" * 60)
print(df.to_string(index=False))

# Get sample data
print("\n" + "=" * 60)
print("📊 SAMPLE DATA (Last 3 rows)")
print("=" * 60)
query = "SELECT * FROM BTC_USD ORDER BY Date DESC LIMIT 3"
df = pd.read_sql(query, conn)
print(df.to_string(index=False))

# Check for new indicators
print("\n" + "=" * 60)
print("✅ INDICATORS VERIFICATION")
print("=" * 60)
required_indicators = [
    'Date', 'Open', 'High', 'Low', 'Close', 'Volume',
    'SMA_20', 'SMA_50', 'RSI_14', 'FNG_Value', 'FNG_Class',
    'MACD', 'MACD_Signal', 'MACD_Histogram',
    'BB_Upper', 'BB_Middle', 'BB_Lower', 'BB_Width',
    'ATR_14'
]

all_columns = df.columns.tolist()
missing = [ind for ind in required_indicators if ind not in all_columns]

if not missing:
    print("✅ All 16 indicators are present!")
    print(f"   Total columns: {len(all_columns)}")
    print("\n   Indicators:")
    for i, ind in enumerate(required_indicators, 1):
        status = "✓" if ind in ['MACD', 'MACD_Signal', 'MACD_Histogram', 
                                   'BB_Upper', 'BB_Middle', 'BB_Lower', 'BB_Width', 'ATR_14'] else " "
        print(f"   {i:2d}. {ind:20s} {'(NEW)' if status == '✓' else ''}")
else:
    print(f"❌ Missing indicators: {missing}")

conn.close()