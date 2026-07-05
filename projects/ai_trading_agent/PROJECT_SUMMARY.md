# AI Trading Agent - Project Summary & Guide

## 1. Tổng quan dự án
Đây là hệ thống giao dịch tự động bằng AI (AI Trading Agent), tích hợp LangGraph để tạo ra một Multi-Agent System phân tích dữ liệu thị trường (BTC, ETH, SOL) và đưa ra quyết định giao dịch trên Binance Testnet hoặc Paper Trading.

## 2. Các tệp tin cốt lõi (Core Files) - CẦN ĐỌC KHI MỞ CHAT MỚI
Nếu bắt đầu một phiên chat mới và cần làm việc với dự án này, hãy đọc các tệp sau đầu tiên để lấy ngữ cảnh:
- `live_advisor.py`: Entry point chính của dự án, quản lý luồng khởi chạy AI Trading.
- `src/langgraph_agent.py`: Nơi định nghĩa Multi-Agent System (LangGraph), các node AI phân tích và đưa ra quyết định.
- `src/binance_executor.py`: Quản lý việc thực thi lệnh giao dịch trên Binance.
- `src/data_fetcher.py`: Tải dữ liệu thị trường và tính toán các chỉ báo kỹ thuật (RSI, SMA, MACD, v.v.).

## 3. Cấu trúc thư mục
- `src/`: Mã nguồn chính của ứng dụng (fetcher, agent, executor).
- `backtest/`: Chứa các script chạy backtest (thử nghiệm chiến lược dựa trên dữ liệu lịch sử).
- `tools/`: Các công cụ tiện ích (kiểm tra database, check PnL, reset PnL).
- `data/`: Nơi lưu trữ database (SQLite) cho market data và system logs.
- `scheduler/`: Các script bat để thiết lập tự động hóa trên Windows Task Scheduler.
- `docs/`: Tài liệu chi tiết của dự án.

## 4. Hướng dẫn chạy nhanh
1. **Cài đặt**: `pip install -r requirements.txt`
2. **Cấu hình**: Chỉnh sửa file `.env` với các key của OpenAI/Gemini, Binance Testnet API, Telegram bot.
3. **Chạy Live Trading**: `python live_advisor.py`
4. **Chạy Backtest**: `python backtest/backtester.py`

## 5. Lưu ý quan trọng
- Hệ thống hỗ trợ "Paper Trading" (không cần API Binance) và "Live Testnet".
- PnL được tracking trong ngày, có thể reset bằng `tools/reset_pnl.py`.
- Module `whale_alert` đã bị vô hiệu hóa để tiết kiệm chi phí, có thể mở lại khi cần thiết.