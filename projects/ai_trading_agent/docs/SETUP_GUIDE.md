# 🚀 AI TRADING AGENT - SETUP GUIDE

> **Last Updated:** 2026-03-11  
> **Version:** 2.0 (With Advanced On-Chain Data)

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [New Features](#new-features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [API Keys Setup](#api-keys-setup)
7. [Running the System](#running-the-system)
8. [Windows Task Scheduler Setup](#windows-task-scheduler-setup)
9. [Testing Features](#testing-features)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 OVERVIEW

The AI Trading Agent is a sophisticated multi-agent system that uses:

- **Technical Analysis** - MACD, Bollinger Bands, ATR, RSI, SMA
- **Sentiment Analysis** - News scraping + Whale Alert integration
- **Risk Management** - Dynamic portfolio allocation with AI
- **On-Chain Data** - Whale Alert + Funding Rate tracking

---

## ✨ NEW FEATURES (v2.0)

### 🆕 Enhanced Technical Indicators
- **MACD** (Moving Average Convergence Divergence)
  - MACD Line, Signal Line, Histogram
  - Trend reversal signals
  
- **Bollinger Bands**
  - Upper, Middle, Lower bands
  - Overbought/Oversold detection
  - Band width for volatility
  
- **ATR** (Average True Range)
  - Dynamic volatility measurement
  - Used for dynamic stop-loss

### 🐋 Whale Alert Integration
- Real-time large transaction monitoring
- Exchange inflow/outflow analysis
- Smart money movement detection
- Automatic confidence score adjustment

### 📊 Funding Rate Tracking
- Multi-exchange funding rate monitoring
- Open interest analysis
- Overcrowded position detection
- Sentiment analysis from derivatives

### 🔄 Offline Backtest Mode
- Test strategies without live trading
- Multiple strategy comparison
- Performance metrics (Alpha, Win Rate, Max Drawdown)
- No API calls required

### ⏰ Windows Task Scheduler
- Automated 24/7 trading
- Data fetcher every 1 hour
- Live advisor every 4 hours
- News scraper every 2 hours
- Daily backtest at 02:00

---

## 📦 PREREQUISITES

### Required Software
- **Python 3.8+** - Download from [python.org](https://www.python.org)
- **Git** - For version control (optional)
- **Windows 10/11** - For Task Scheduler

### Python Packages
Install required packages:

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install yfinance pandas numpy requests
pip install langchain langchain-openai langgraph
pip install python-binance python-dotenv
pip install flask folium
```

---

## 🔧 INSTALLATION

### 1. Clone/Download Project
```bash
cd c:\Users\Admin\Desktop\WorkSpace\Project\LangGraph_Agent_System
```

### 2. Install Python Packages
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
python --version
pip list | findstr langchain
```

---

## ⚙️ CONFIGURATION

### Environment Variables (.env file)

Create a `.env` file in the project root:

```env
# Gemini API (Required)
GCLI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
GCLI_API_KEY=your_gemini_api_key_here

# Binance Testnet (Optional - for Paper Trading)
BINANCE_TESTNET_API_KEY=your_binance_testnet_api_key
BINANCE_TESTNET_SECRET=your_binance_testnet_secret
BINANCE_TESTNET=True

# Telegram Alerts (Optional)
TELE_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id

# Whale Alert API (Optional)
WHALE_ALERT_API_KEY=your_whale_alert_api_key
```

### How to Get API Keys

#### Gemini API (Required)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste to `.env` file

#### Binance Testnet (Optional)
1. Go to [Binance Testnet](https://testnet.binance.vision/)
2. Register and get API credentials
3. Add to `.env` file

#### Telegram (Optional)
1. Create bot via [@BotFather](https://t.me/botfather)
2. Get bot token
3. Get your chat ID via [@userinfobot](https://t.me/userinfobot)

#### Whale Alert (Optional)
1. Go to [Whale Alert](https://whale-alert.io/documentation/api)
2. Register for free API key
3. Add to `.env` file

---

## 🚀 RUNNING THE SYSTEM

### Method 1: Using Dashboard (Recommended)

```bash
python dashboard.py
```

Then select from menu:
- **Option 4** - Run Live Advisor
- **Option 5** - Run Backtest
- **Option 6** - Update Data

### Method 2: Direct Script Execution

```bash
# Update market data
cd projects/ai_trading_agent
python data_fetcher.py

# Run live advisor
python live_advisor.py

# Run backtest
python backtester.py

# Run offline backtest
python offline_backtest.py
```

---

## ⏰ WINDOWS TASK SCHEDULER SETUP

### Automated Trading Setup

**Step 1:** Run as Administrator
```bash
Right-click setup_scheduler.bat → "Run as administrator"
```

**Step 2:** Verify Tasks
1. Press `Win + R`, type `taskschd.msc`
2. Look for tasks with "AI_Trading_" prefix

**Step 3:** Monitor Tasks
- **AI_Trading_Data_Fetcher** - Every 1 hour
- **AI_Trading_Live_Advisor** - Every 4 hours
- **AI_Trading_News_Scraper** - Every 2 hours
- **AI_Trading_Daily_Backtest** - Daily at 02:00

### Remove Tasks
```bash
Right-click remove_scheduler.bat → "Run as administrator"
```

---

## 🧪 TESTING FEATURES

### Test 1: Data Fetcher with New Indicators
```bash
cd projects/ai_trading_agent
python data_fetcher.py
```

**Expected Output:**
```
🔄 Đang lấy Fear & Greed Index...
🔄 Đang tải dữ liệu BTC-USD...
✅ Đã lưu 221 dòng dữ liệu BTC_USD
```

### Test 2: Verify Database
```bash
python verify_db.py
```

**Expected Output:**
```
✅ All 16 indicators are present!
   Total columns: 19
   Indicators:
    1. Date
    ...
   12. MACD                 (NEW)
   ...
   19. ATR_14               (NEW)
```

### Test 3: Whale Alert (Requires API Key)
```bash
python whale_alert.py
```

**Expected Output:**
```
🐋 Testing Whale Alert Monitor...
📊 Exchange Flow Analysis (BITCOIN - 24h):
   Inflow:   $XX,XXX,XXX
   Outflow:  $XX,XXX,XXX
   Net Flow: $X,XXX,XXX (BULLISH/BEARISH)
```

### Test 4: Funding Rate
```bash
python funding_rate.py
```

**Expected Output:**
```
📊 Testing Funding Rate Monitor...
📊 FUNDING RATE MONITOR (Coinglass)
📌 BTC:
   Avg Rate: +0.0123%
   Sentiment: BULLISH (Longs paying Shorts)
```

### Test 5: Offline Backtest
```bash
python offline_backtest.py
```

**Expected Output:**
```
🚀 OFFLINE BACKTEST MODE
📊 BACKTEST RESULTS - BTC_USD
💰 Capital:
   Initial: $100,000.00
   Final:   $XXX,XXX.XX
📈 Performance:
   Total Return:  +XX.XX%
   Alpha:         +X.XX%
```

### Test 6: Live Trading with All Features
```bash
python live_advisor.py
```

**Expected Output:**
```
🔄 Fetching market data...
🐋 Whale Alert Monitor...
📊 Funding Rate Monitor...
🕵️ [Technical Agent] Đang phân tích...
📰 [Sentiment Agent] Đang đọc tin tức...
🛡️ [Risk Manager] Đang phân bổ danh mục...
```

---

## 🔍 TROUBLESHOOTING

### Issue: "No module named 'langchain'"
**Solution:**
```bash
pip install langchain langchain-openai langgraph
```

### Issue: "API Key not found"
**Solution:**
- Check `.env` file exists in project root
- Verify API key is correct
- Restart terminal

### Issue: "Whale Alert API rate limit exceeded"
**Solution:**
- Wait 1 hour before retrying
- Or upgrade to paid plan

### Issue: "Coinglass API timeout"
**Solution:**
- Check internet connection
- Try again later (API may be busy)

### Issue: Task Scheduler not working
**Solution:**
- Run `setup_scheduler.bat` as Administrator
- Check Task Scheduler history for errors
- Verify Python path is correct

### Issue: Database locked
**Solution:**
- Close all database connections
- Restart Python scripts
- Check if another script is using the DB

---

## 📊 PERFORMANCE TIPS

### For Intel i3-1215U (Low-Resource System)

1. **Use Paper Trading Mode** - Less CPU intensive
2. **Reduce Update Frequency** - Change Task Scheduler to every 4 hours
3. **Disable Whale Alert** - If API limits are reached
4. **Use Flash Model** - Faster and cheaper than Pro

### Token Management

- **Flash (10,000 requests)** - Use for:
  - Technical Analysis
  - Sentiment Analysis
  - Simple tasks
  
- **Pro (1,900 requests)** - Use for:
  - Risk Manager (critical decisions)
  - Complex planning
  - Final review

---

## 📞 SUPPORT

### Documentation
- **Master Guide:** `MASTER_GUIDE.md`
- **Context Summary:** `CONTEXT_SUMMARY.md`
- **Latest Report:** `LATEST_REPORT.md`

### File Structure
```
projects/ai_trading_agent/
├── data_fetcher.py          # Market data + indicators
├── whale_alert.py           # Whale monitoring
├── funding_rate.py          # Funding rates
├── langgraph_agent.py       # 3-Agent system
├── live_advisor.py         # Live trading signals
├── backtester.py           # Backtesting
├── offline_backtest.py      # Offline testing (NEW)
├── news_scraper.py         # News scraping
├── binance_executor.py     # Trade execution
├── verify_db.py            # Database verification (NEW)
├── setup_scheduler.bat      # Task scheduler setup (NEW)
└── remove_scheduler.bat     # Task scheduler removal (NEW)
```

---

## 🎓 LEARNING RESOURCES

### Understanding Indicators
- **RSI:** https://www.investopedia.com/terms/r/rsi.asp
- **MACD:** https://www.investopedia.com/terms/m/macd.asp
- **Bollinger Bands:** https://www.investopedia.com/terms/b/bollingerbands.asp
- **ATR:** https://www.investopedia.com/terms/a/atr.asp

### Understanding Whale Activity
- **Whale Alert:** https://whale-alert.io
- **On-Chain Analysis:** Why it matters

### Understanding Funding Rates
- **Funding Rate Explained:** https://www.coinglass.com/learn/funding-rate
- **Long vs Short:** How to interpret

---

## 🚀 NEXT STEPS

After setup, consider:

1. **Test Paper Trading** - Run for 1-2 weeks
2. **Analyze Performance** - Review backtest results
3. **Fine-Tune Parameters** - Adjust based on results
4. **Enable Live Trading** - Only after confidence
5. **Set Up VPS** - For 24/7 operation (optional)

---

## ⚠️ DISCLAIMER

**This is a trading bot for educational purposes only.**
- Past performance does not guarantee future results
- Always use risk management
- Never invest more than you can afford to lose
- Cryptocurrency trading is highly volatile

**Use at your own risk!**

---

**💡 Good luck with your trading journey! 🚀**