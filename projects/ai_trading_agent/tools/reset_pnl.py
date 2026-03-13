"""Xóa dữ liệu cũ trong Paper_Trade_Portfolio để reset PnL"""
import sqlite3
import os
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent.parent.parent
db_path = base_dir / "data" / "system_logs.db"

print("=" * 70)
print("⚠️  RESET PAPER TRADE PORTFOLIO DATA")
print("=" * 70)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Xem số lượng record hiện tại
cursor.execute('SELECT COUNT(*) FROM Paper_Trade_Portfolio')
count = cursor.fetchone()[0]
print(f"\n📊 Số lượng record hiện tại: {count}")

if count > 0:
    # Xóa toàn bộ dữ liệu
    cursor.execute('DELETE FROM Paper_Trade_Portfolio')
    conn.commit()
    print("✅ Đã xóa toàn bộ dữ liệu cũ!")
else:
    print("ℹ️  Database đã trống, không cần xóa.")

conn.close()

print("\n💡 Sau khi reset, lần chạy tiếp theo sẽ:")
print("   - PnL = $0.00 (lần đầu chạy)")
print("   - Tính PnL từ số dư thật trên Binance Testnet")
print("=" * 70)