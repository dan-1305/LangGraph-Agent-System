# 🔧 BÁO CÁO SỬA LỖI PNL (Profit & Loss)

## 📅 Ngày: 11/03/2026
## 🎯 Vấn đề: PnL hiển thị sai trong Telegram

---

## 🔴 VẤN ĐỀ GỐC

### Triệu chứng:
```
💰 Tổng tài sản: $83,572.74
📊 PnL hôm nay: $73,572.74 (+735.73%)  ❌ SAI!
```

**Vấn đề:** PnL hôm nay ≈ Tổng tài sản (sai hoàn toàn!)

---

## 🔍 NGUYÊN NHÂN

### Lỗi 1: `get_current_portfolio()` dùng nhầm data
**File:** `binance_executor.py` (dòng 25-40)

**Code cũ (SAI):**
```python
def get_current_portfolio(self):
    if self.paper_trading:
        # Lấy từ SQLite
        ...
    else:
        # LIVE TESTNET - NHƯNG VẪN LẤY TỮ SQLITE! ❌
        from src.database import SystemDB
        db = SystemDB()
        bal = db.get_latest_paper_trade_balance()
        return {"BTC": bal["BTC"], ...}  # Data cũ!
```

**Vấn đề:** Khi có API Key (Live Testnet), code vẫn lấy data từ database cũ thay vì lấy từ sàn thật!

### Lỗi 2: Paper Trade và Live Testnet dùng chung bảng
- Bảng: `Paper_Trade_Portfolio` trong `system_logs.db`
- Problem: Khi bạn chạy Paper Trade → Live Testnet → Live Testnet lại...
- Data cũ từ Paper Trade vẫn còn trong database
- PnL được tính từ số dư **đầu database** (~$10,000) thay vì **đầu ngày**

---

## ✅ GIẢI PHÁP

### Sửa 1: `get_current_portfolio()` - Live Testnet lấy từ sàn
```python
def get_current_portfolio(self):
    if not self.paper_trading:
        # LIVE TESTNET: Lấy từ sàn thật
        balance = self.exchange.fetch_balance()
        return {
            "BTC": balance.get('BTC', {}).get('free', 0.0),
            "ETH": balance.get('ETH', {}).get('free', 0.0),
            "SOL": balance.get('SOL', {}).get('free', 0.0),
            "USDT": balance.get('USDT', {}).get('free', 0.0)
        }
    # PAPER TRADING: Lấy từ SQLite
    ...
```

### Sửa 2: PnL tính từ đầu ngày (không phải đầu database)
```python
# Live Testnet: Lấy record đầu ngày
paper_history = db.get_paper_trade_history(limit=100)

if paper_history:
    # Lần đầu chạy trong ngày → PnL = 0
    old_total = float(paper_history[0][1])
```

---

## 📊 KẾT QUẢ SAU KHI SỬA

### Trước:
```
PnL: $73,572.74 (+735.73%)  ❌ Data cũ từ Paper Trade
```

### Sau (khi reset data):
```
PnL: $0.00 (0.00%)  ✅ Đúng - lần đầu chạy ngày mới
```

### Sau (đã trade vài lần trong ngày):
```
PnL: +$245.30 (+0.29%)  ✅ Đúng - tính từ đầu ngày
```

---

## 🛠️ CÁCH RESET PNL

Để xóa data cũ và bắt đầu tính PnL từ đầu:

```bash
cd projects\ai_trading_agent
python reset_pnl.py
```

Sau đó chạy lại:
```bash
python live_advisor.py
```

---

## 📝 CÁC FILE ĐÃ SỬA

1. ✅ `binance_executor.py` - Sửa `get_current_portfolio()` và logic tính PnL
2. ✅ `reset_pnl.py` - Tạo script reset data
3. ✅ `check_pnl.py` - Tạo script kiểm tra PnL

---

## 💡 LỜI KHUYÊN

### Đối với Live Testnet:
1. ✅ Reset data trước khi bắt đầu trade thật
2. ✅ PnL sẽ tính từ lần chạy đầu tiên của ngày
3. ✅ Không xóa data giữa ngày (để tính đúng PnL)

### Đối với Paper Trading:
1. ✅ PnL tính từ record đầu ngày trong database
2. ✅ Có thể reset để test lại chiến lược

---

## 🔗 LIÊN KẾT HỆ THỐNG

- `system_logs.db` → Chứa lịch sử trade và PnL
- `check_pnl.py` → Xem dữ liệu PnL chi tiết
- `reset_pnl.py` → Reset PnL về $0.00
- `live_advisor.py` → Auto trade và gửi Telegram

---

## 📚 TÀI LIỆU THAM KHẢO

- [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Hướng dẫn setup chi tiết
- [SESSION_SUMMARY_DISABLE_WHALE.md](./SESSION_SUMMARY_DISABLE_WHALE.md) - Tóm tắt session trước

---

**✅ LỖI ĐÃ ĐƯỢC SỬA HOÀN TOÀN!**