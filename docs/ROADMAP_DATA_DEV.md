# 📊 LỘ TRÌNH THỰC THI (ROADMAP): DATA PIPELINE & GIAO DIỆN WEB

**Mục tiêu:** Cung cấp dữ liệu SẠCH và xây dựng giao diện tương tác (Web UI) cho mô hình dự báo chứng khoán bằng Học Sâu.
**Môi trường thực thi:** Google Colab (Code bằng Python Notebook `.ipynb`).
**Nhân sự:** [Tên Bạn Ngài] (Data & MLOps Developer).

---

## 🗓️ GIAI ĐOẠN 1: THU THẬP & TIỀN XỬ LÝ DỮ LIỆU (TUẦN 1 - TUẦN 2)
*Giai đoạn này là nền móng. Dữ liệu bẩn thì AI sẽ học rác (Garbage In, Garbage Out).*

### 🎯 Nhiệm vụ 1.1: Cào dữ liệu (Data Crawling)
- **Công cụ:** Dùng thư viện `yfinance` (cho chứng khoán Mỹ/Crypto như AAPL, BTC-USD) hoặc `vnstock` (cho chứng khoán Việt Nam như FPT, VCB).
- **Yêu cầu:** 
  - Lấy dữ liệu OHLCV (Open, High, Low, Close, Volume) theo khung ngày (Daily).
  - Khoảng thời gian: Ít nhất từ 2015 đến nay (10 năm dữ liệu) để AI có đủ chu kỳ kinh tế học tập.

### 🎯 Nhiệm vụ 1.2: Khai phá đặc trưng (Feature Engineering)
- **Công cụ:** Dùng `pandas` và `TA-Lib` (hoặc `pandas_ta` nếu cài TA-Lib khó trên Colab).
- **Yêu cầu (Rất quan trọng):** Mạng Transformer của Kỹ sư trưởng cần rất nhiều tín hiệu mượt mà. Bạn phải tính toán thêm các cột (Features) sau vào DataFrame:
  1. **RSI (Relative Strength Index):** Chu kỳ 14 ngày.
  2. **MACD (Moving Average Convergence Divergence):** Đường MACD, đường Signal và Histogram.
  3. **Đường trung bình động (Moving Averages):** SMA_20, SMA_50, EMA_20.
  4. **Bollinger Bands:** Dải trên, Dải dưới, Dải giữa.
  5. **Log Return:** Tỷ suất sinh lời logarit của giá Đóng cửa (giúp dữ liệu chuẩn hóa tốt hơn).

### 🎯 Nhiệm vụ 1.3: Làm sạch và Nghiệm thu
- **Yêu cầu:** 
  - Xóa bỏ các dòng bị khuyết dữ liệu (`NaN`) sinh ra do tính toán MA ở những ngày đầu tiên (`df.dropna()`).
  - Đảm bảo dữ liệu được sắp xếp theo thời gian (từ cũ đến mới).
- **Nghiệm thu:** Xuất ra file `dataset_clean_features.csv` và gửi cho Kỹ sư trưởng (AI Engineer) qua Google Drive để ổng bắt đầu train model.

---

## 🗓️ GIAI ĐOẠN 2: TRIỂN KHAI GIAO DIỆN & TÍCH HỢP (TUẦN 5 - TUẦN 6)
*Lúc này Kỹ sư trưởng đã train xong con AI Transformer cực xịn. Nhiệm vụ của bạn là ráp nó vào web để biểu diễn.*

### 🎯 Nhiệm vụ 2.1: Xây dựng Giao diện Web (Gradio)
- **Công cụ:** `gradio` (Cực kỳ dễ chạy trực tiếp trên Colab).
- **Yêu cầu giao diện:**
  - Có ô Textbox để nhập "Mã Chứng Khoán" (Ví dụ: FPT).
  - Nút bấm "Chạy Dự Báo Bằng AI Transformer".

### 🎯 Nhiệm vụ 2.2: Tích hợp Model của Kỹ sư trưởng (Inference Pipeline)
- **Luồng xử lý khi bấm nút:**
  1. Gọi hàm crawl data (của Tuần 1) để lấy dữ liệu 60 ngày gần nhất của mã cổ phiếu đó.
  2. Tính toán lại RSI, MACD, MA (như Tuần 1).
  3. Đọc file `scaler.pkl` (do Kỹ sư trưởng gửi) để scale dữ liệu về dải [0, 1].
  4. Nạp mảng dữ liệu cuối cùng vào `transformer_model.pth` của Kỹ sư trưởng.
  5. Lấy kết quả dự đoán (Giá trị ngày mai hoặc Nhãn Tăng/Giảm).

### 🎯 Nhiệm vụ 2.3: Trực quan hóa (Visualization)
- **Công cụ:** `plotly` hoặc `matplotlib`.
- **Yêu cầu:** Vẽ một biểu đồ nến (Candlestick) thật ngầu của 30 ngày qua, và vẽ thêm một điểm chấm đỏ to đùng (Hoặc mũi tên 🚀/🔻) thể hiện dự báo của ngày mai.
- **Nghiệm thu:** Chạy lệnh `demo.launch(share=True)` để lấy đường link Public gửi cho Kỹ sư trưởng test thử trên điện thoại. Cả nhóm cùng kiểm tra xem có bị crash khi nhập mã tào lao không.

---

## 🗓️ GIAI ĐOẠN 3: VIẾT BÁO CÁO (TUẦN 7)
- **Phần việc của Data Developer:**
  - Viết chương: "Quy trình thu thập và xử lý dữ liệu tài chính đa chiều". Giải thích lý luận tại sao lại chọn các chỉ báo (RSI, MACD) làm đặc trưng cho AI.
  - Viết chương: "Thiết kế kiến trúc hệ thống triển khai (Deployment) với Gradio".
  - Chụp ảnh màn hình giao diện nhét vào file Word.
