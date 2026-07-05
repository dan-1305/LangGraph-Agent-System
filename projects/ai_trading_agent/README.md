# 📈 SOVEREIGN AI TRADING ADVISOR (V2.1)

> **Định vị:** Cố vấn Chiến lược Swing Trading cấp cao dựa trên tinh hoa của các Phù thủy Thị trường (Mark Minervini, Ray Dalio).

---

## 🎯 I. TRIẾT LÝ VẬN HÀNH: "RISK-FIRST"

Khác với các Bot Trading "làm phép" hứa hẹn lợi nhuận ảo, Sovereign Trading Advisor tập trung vào sự thật khách quan và bảo vệ vốn tuyệt đối:

1.  **Thẩm định Trend Template:** Chỉ giải ngân khi tài sản hội đủ 6 tiêu chuẩn Stage 2 (Siêu cổ phiếu/Siêu tài sản).
2.  **Mẫu hình VCP (Volatility Contraction):** Tìm kiếm sự cạn kiệt nguồn cung trước khi bùng nổ giá.
3.  **Nguyên tắc Ray Dalio:** Đối soát FA, TA và Tâm lý đám đông để tìm ra "Sự thật khách quan" trước khi đặt lệnh.
4.  **Hardware Awareness:** Tối ưu hóa tính năng tính toán bằng Pandas Vectorization, đảm bảo Validation Gate chạy dưới 1 giây trên Workstation Xeon.

---

## 🏗️ II. KIẾN TRÚC ĐA TÁC NHÂN (MULTI-AGENT)

Hệ thống được vận hành bởi một Hội đồng Quản trị AI (Sovereign Board):

-   **Strategic Advisor (TA):** Thẩm định xu hướng Stage 2, RS, và mẫu hình tích lũy.
-   **Sentiment Expert:** Phân tích Funding Rate, Whale Alert và chỉ số Fear & Greed để nhận diện bẫy hưng phấn.
-   **Value Analyst (FA):** Tính toán "Biên độ an toàn" (Margin of Safety) dựa trên dữ liệu cơ bản.
-   **Sovereign Risk Manager:** Người ra quyết định cuối cùng, điều phối tỷ trọng USDT phòng thủ.

---

## ⚡ III. HIỆU NĂNG VƯỢT TRỘI

-   **Engine:** Pandas Vectorized Technical Analysis.
-   **Latency:** < 1s cho toàn bộ khâu thẩm định kỹ thuật.
-   **Reliability:** Tích hợp `stream_fallback_generator`, tự động gối đầu Groq/OpenRouter nếu Gemini lỗi.
-   **Memory:** Hệ thống tự học từ sai lầm qua file `TRADING_LORE.md`.

---

## �️ IV. HƯỚNG DẪN VẬN HÀNH (1-CLICK)

1.  Cấu hình Tickers tại `src/config.py`.
2.  Chạy Advisor Live:
    ```bash
    uv run python projects/ai_trading_agent/live_advisor.py
    ```
3.  Xem báo cáo PnL tại Dashboard Web.

---
*Sovereign System - Build for Integrity, Perform for Excellence.*
