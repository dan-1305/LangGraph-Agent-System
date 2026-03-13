"""Kiểm tra dữ liệu PnL trong database"""
import sqlite3
import sys
from pathlib import Path

# Lấy đường dẫn đến database
base_dir = Path(__file__).resolve().parent.parent.parent.parent
db_path = base_dir / "data" / "system_logs.db"

print("=" * 70)
print("📊 DỮ LIỆU PAPER TRADE PORTFOLIO")
print("=" * 70)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query lấy 10 record gần nhất
cursor.execute('''
    SELECT id, timestamp, btc_bal, eth_bal, sol_bal, usdt_bal, total_usdt_value
    FROM Paper_Trade_Portfolio
    ORDER BY id DESC
    LIMIT 10
''')

rows = cursor.fetchall()

if not rows:
    print("❌ Chưa có dữ liệu trong bảng Paper_Trade_Portfolio")
else:
    print(f"{'ID':<5} {'Timestamp':<20} {'BTC':<12} {'ETH':<12} {'SOL':<12} {'USDT':<15} {'Total ($)':<15}")
    print("-" * 70)
    
    for row in rows:
        id_, timestamp, btc, eth, sol, usdt, total = row
        print(f"{id_:<5} {timestamp:<20} {btc:<12.6f} {eth:<12.6f} {sol:<12.4f} {usdt:<15.2f} {total:<15.2f}")
    
    print("\n" + "=" * 70)
    print("📈 TÍNH TOÁN PnL")
    print("=" * 70)
    
    if len(rows) >= 2:
        newest = rows[0]
        oldest = rows[-1]
        
        newest_total = newest[6]  # total_usdt_value
        oldest_total = oldest[6]
        
        pnl = newest_total - oldest_total
        pnl_pct = (pnl / oldest_total) * 100 if oldest_total > 0 else 0
        
        print(f"Số dư gần nhất: ${newest_total:,.2f} ({newest[1]})")
        print(f"Số dư cũ nhất: ${oldest_total:,.2f} ({oldest[1]})")
        print(f"\n📊 PnL tổng: ${pnl:,.2f} ({pnl_pct:+.2f}%)")
        
        # Tính PnL giữa các lần trade gần nhất
        print("\n📊 PnL giữa các lần trade:")
        print(f"{'Từ':<20} {'Đến':<20} {'PnL ($)':<15} {'PnL (%)':<10}")
        print("-" * 70)
        
        for i in range(len(rows) - 1):
            current = rows[i]
            previous = rows[i + 1]
            
            current_total = current[6]
            previous_total = previous[6]
            
            pnl_trade = current_total - previous_total
            pnl_pct_trade = (pnl_trade / previous_total) * 100 if previous_total > 0 else 0
            
            print(f"{previous[1]:<20} {current[1]:<20} {pnl_trade:<15.2f} {pnl_pct_trade:<+10.2f}%")

conn.close()

print("\n💡 Phân tích:")
print("- PnL gần nhất = Tổng hiện tại - Số dư đầu ngày")
print("- Nếu có dữ liệu Paper Trade cũ, nó sẽ ảnh hưởng Live Testnet")
print("- Nên xóa data cũ nếu muốn reset PnL")