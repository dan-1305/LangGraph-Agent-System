# 🤖 AI Trading Agent - Cấu Trúc Project

## 📁 Cấu Trúc Folder

```
ai_trading_agent/
├── src/                    # Source code chính
│   ├── data_fetcher.py      # Fetch market data & indicators
│   ├── funding_rate.py       # Funding rate monitor (Coinglass API)
│   ├── whale_alert.py       # Whale alert monitor (DISABLED - $30/mo)
│   ├── news_scraper.py      # Scrape news from CoinTelegraph
│   ├── binance_executor.py  # Execute trades on Binance Testnet
│   └── langgraph_agent.py  # Multi-agent trading system
│
├── backtest/               # Backtest scripts
│   ├── backtester.py        # Main backtest engine
│   └── offline_backtest.py # Offline backtest mode
│
├── tools/                  # Utility tools
│   ├── verify_db.py        # Verify database integrity
│   ├── check_pnl.py        # Check PnL history
│   └── reset_pnl.py        # Reset PnL to $0.00
│
├── docs/                   # Documentation
│   ├── SETUP_GUIDE.md
│   ├── COMPLETION_REPORT.md
│   ├── PNL_FIX_REPORT.md
│   ├── SESSION_SUMMARY_DISABLE_WHALE.md
│   └── SESSION_SUMMARY_PNL_FIX.md
│
├── scheduler/              # Windows Task Scheduler scripts
│   ├── setup_scheduler.bat
│   └── remove_scheduler.bat
│
├── data/                   # Database & data files
│   ├── trading_market.db   # Market data (BTC, ETH, SOL)
│   └── system_logs.db      # Trading logs & PnL
│
├── live_advisor.py         # Main entry point (run this!)
├── .env                    # Environment variables
└── requirements.txt        # Python dependencies
```

---

## 🚀 Cách Sử Dụng

### 1. Setup Environment

```bash
cd projects\ai_trading_agent
pip install -r requirements.txt
```

### 2. Cấu hình `.env`

```env
# OpenAI / Gemini API
OPENAI_API_KEY=sk-xxx
GCLI_API_KEY=xxx
GCLI_BASE_URL=https://generativelanguage.googleapis.com/v1beta

# Binance Testnet (Optional - for Live Trading)
BINANCE_TESTNET_API_KEY=xxx
BINANCE_TESTNET_SECRET=xxx
BINANCE_TESTNET=True

# Telegram (Optional - for alerts)
TELE_TOKEN=xxx
CHAT_ID=xxx
```

### 3. Chạy Live Trading

```bash
python live_advisor.py
```

---

## 🛠️ Công Cụ Hỗ Trợ

### Backtest

```bash
# Test chiến lược với historical data
python backtest\backtester.py

# Offline backtest (không cần API)
python backtest\offline_backtest.py
```

### Tools

```bash
# Kiểm tra database
python tools\verify_db.py

# Kiểm tra PnL
python tools\check_pnl.py

# Reset PnL
python tools\reset_pnl.py
```

### Scheduler (Windows)

```bash
# Setup automation
scheduler\setup_scheduler.bat

# Remove automation
scheduler\remove_scheduler.bat
```

---

## 📊 Tính Năng

### ✅ Đã Implement
- 📈 Market Data Fetching (BTC, ETH, SOL)
- 📊 Technical Indicators (RSI, SMA, MACD, BB, ATR)
- 📰 News Sentiment Analysis (CoinTelegraph)
- 🐋 Whale Alert (DISABLED - $30/month)
- 💰 Funding Rate Monitoring (Coinglass API - FREE)
- 🤖 LangGraph Multi-Agent System
- 💳 Binance Testnet Integration
- 📊 PnL Tracking
- 📱 Telegram Alerts
- 🧪 Backtesting Engine

### ⏳ Chưa Implement
- [ ] VPS Setup cho 24/7
- [ ] Dynamic Model Selection
- [ ] Exchange Flow Data (Coinglasso)
- [ ] Mobile Dashboard

---

## 📚 Tài Liệu

- [SETUP_GUIDE.md](./docs/SETUP_GUIDE.md) - Hướng dẫn setup chi tiết
- [PNL_FIX_REPORT.md](./docs/PNL_FIX_REPORT.md) - Report fix lỗi PnL
- [SESSION_SUMMARY_PNL_FIX.md](./docs/SESSION_SUMMARY_PNL_FIX.md) - Session summary

---

## ⚠️ Lưu Ý

1. **Paper Trading vs Live Testnet:**
   - Paper Trading: Dùng database ảo, không cần API Key
   - Live Testnet: Cần API Key Binance Testnet

2. **PnL Tracking:**
   - PnL tính từ đầu ngày
   - Reset PnL bằng `tools\reset_pnl.py`

3. **Whale Alert:**
   - Hiện tại đang DISABLED (tốn $30/tháng)
   - Có thể re-enable khi profitable

---

## 🔄 Cập Nhật Cấu Trúc (11/03/2026)

Đã sắp xếp lại folder để rõ ràng hơn:
- `src/` - Source code Python
- `backtest/` - Backtest scripts
- `tools/` - Utility scripts
- `docs/` - Documentation
- `scheduler/` - Scheduler scripts

**Thay đổi import:**
- Trước: `from binance_executor import ...`
- Sau: `from src.binance_executor import ...`

---

## 📞 Liên Hệ

Xem [../CONTEXT_SUMMARY.md](../../CONTEXT_SUMMARY.md) để biết thêm chi tiết.