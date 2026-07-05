# 📈 LỘ TRÌNH THỰC THI (ROADMAP): DỰ BÁO GIÁ CỔ PHIẾU BẰNG HỌC Sâu (DEEP LEARNING)

**Mục tiêu dự án:** Phát triển hệ thống dự báo xu hướng chứng khoán (Tăng/Giảm hoặc giá tương lai) bằng mạng nơ-ron LSTM/GRU.
**Môi trường thực thi:** 100% Google Colab (để tận dụng GPU miễn phí và dễ dàng chia sẻ code `.ipynb`).
**Nhân sự:** 
- **Core AI Engineer (Kỹ sư trưởng):** [Tên Ngài] - Chịu trách nhiệm kiến trúc mạng nơ-ron và độ chính xác của AI.
- **Data & MLOps Developer:** [Tên Bạn Ngài] - Chịu trách nhiệm cào dữ liệu, tính toán chỉ báo và xây dựng Web UI.

---

## 🗓️ GIAI ĐOẠN 1: DATA PIPELINE & FEATURE ENGINEERING (TUẦN 1 - TUẦN 2)
*Giai đoạn này là nền móng. Nếu dữ liệu rác (Garbage In), AI sẽ sinh ra rác (Garbage Out).*

### 👤 Trách nhiệm chính: Data Developer (Tiến)
**Hạn chót (Deadline):** Cuối Tuần 2.
**Nhiệm vụ chi tiết:**
1. **Thu thập dữ liệu (Data Crawling):**
   - Viết một script (trên 1 file Jupyter Notebook) sử dụng thư viện `yfinance` hoặc `vnstock` để tải dữ liệu OHLCV (Mở cửa, Cao, Thấp, Đóng cửa, Khối lượng) của 3-5 mã cổ phiếu tiêu biểu (ví dụ: FPT, VCB, HPG hoặc BTC).
   - Dữ liệu phải kéo dài ít nhất 5 năm để AI có đủ độ dài học chu kỳ.
2. **Khai phá đặc trưng (Feature Engineering):**
   - Sử dụng `pandas` và `TA-Lib` để tính toán thêm các chỉ báo kỹ thuật bắt buộc: **RSI** (Sức mạnh tương đối), **MACD** (Trung bình động hội tụ phân kỳ), và **SMA/EMA** (Trung bình động 20 ngày, 50 ngày).
   - *Lý do:* Mạng LSTM rất thích các biến số đã được làm mượt này thay vì chỉ nhìn vào giá trần thô.
3. **Làm sạch dữ liệu (Data Cleaning):**
   - Xử lý các dòng bị thiếu (`NaN`), loại bỏ các ngày nghỉ lễ (không có giao dịch).
4. **Nghiệm thu (Bàn giao cho Kỹ sư trưởng):**
   - Phải nộp lại một file `dataset_clean.csv` hoàn hảo, không có lỗi.
   - Kỹ sư trưởng (Ngài) sẽ review file này. Nếu thấy dữ liệu bị lệch cột hoặc thiếu ngày, trả lại bắt làm lại!

---

## 🗓️ GIAI ĐOẠN 2: DEEP LEARNING CORE & TRAINING (TUẦN 3 - TUẦN 4)
*Giai đoạn này là linh hồn của môn Học Sâu. Nơi thể hiện trình độ toán học và thuật toán.*

### 👤 Trách nhiệm chính: Core AI Engineer (Ngài)
**Hạn chót (Deadline):** Cuối Tuần 4.
**Nhiệm vụ chi tiết:**
1. **Tiền xử lý chuỗi thời gian (Time-series Windowing):**
   - Dùng `MinMaxScaler` của sklearn để ép toàn bộ dữ liệu CSV về dải [0, 1] (Bắt buộc với LSTM).
   - Chặt dữ liệu thành các "Cửa sổ thời gian" (Sliding Windows). Ví dụ: Dùng dữ liệu 30 ngày qua để đoán 1 ngày tới.
2. **Xây dựng Mạng Nơ-ron (PyTorch / Keras):**
   - Định nghĩa kiến trúc: 1 lớp Input -> 2 lớp LSTM (có Dropout 20% chống học vẹt) -> 1 lớp Dense (Linear) đầu ra.
   - Hàm Loss: `MSE` (nếu đoán giá trị thực) hoặc `Binary Cross Entropy` (nếu đoán Tăng/Giảm).
3. **Huấn luyện (Training trên Colab GPU):**
   - Bật `T4 GPU` trên Google Colab. Bấm chạy epochs (khoảng 50-100 epochs).
   - Vẽ biểu đồ `Training Loss` và `Validation Loss` ép sát nhau (Thầy rất thích nhìn biểu đồ này để chấm điểm).
4. **Nghiệm thu (Bàn giao lại cho Frontend):**
   - Ngài sẽ xuất ra một file mô hình đã được train chín mùi (ví dụ: `stock_lstm_model.h5` hoặc `model.pth`).
   - Ngài giao file này lại cho bạn ngài để ổng đem đi ráp vào giao diện.

---

## 🗓️ GIAI ĐOẠN 3: TRIỂN KHAI GIAO DIỆN (DEPLOYMENT & UI) (TUẦN 5 - TUẦN 6)
*Giai đoạn này biến những dòng code khô khan thành một sản phẩm có thể click, tương tác được.*

### 👤 Trách nhiệm chính: MLOps Developer (Tiến)
**Hạn chót (Deadline):** Cuối Tuần 6.
**Nhiệm vụ chi tiết:**
1. **Thiết lập Gradio / Streamlit trên Colab:**
   - Viết một script giao diện đơn giản. Giao diện gồm 1 ô nhập "Mã Cổ Phiếu" và nút "Dự Đoán".
2. **Tích hợp Pipeline (End-to-End):**
   - Khi user bấm nút, script phải tự động: (1) Tải data mới nhất của ngày hôm nay -> (2) Chạy qua hàm tiền xử lý scaling -> (3) Đút vào file `model.pth` của Kỹ sư trưởng -> (4) Nhận kết quả và nhả ra màn hình.
3. **Trực quan hóa (Visualization):**
   - Hiển thị thêm một biểu đồ đường (Line chart) bằng `matplotlib` hoặc `plotly` vẽ mức giá thực tế và giá dự đoán đè lên nhau.
4. **Nghiệm thu:**
   - Cung cấp một đường link Public (Gradio Share Link hoặc ngrok) để thầy cô có thể dùng điện thoại truy cập và test thử model ngay tại lớp.

---

## 🗓️ GIAI ĐOẠN 4: VIẾT BÁO CÁO & BẢO VỆ (TUẦN 7)
*Giai đoạn gom điểm.*

### 👤 Trách nhiệm chung (Cả 2 người)
- **Kỹ sư trưởng (Ngài):** Viết chương về *Kiến trúc Mạng LSTM*, *Hàm Loss*, *Lý do chọn siêu tham số (Hyperparameters)*.
- **Developer (Tiến):** Viết chương về *Sự cần thiết của TA-Lib*, *Sơ đồ luồng dữ liệu (Data Flow)*, và chụp ảnh Demo giao diện chèn vào Word.
- **Thực tập:** Cùng nhau ngồi bấm chạy thử các mã cổ phiếu lạ để xem bot phán đoán có ổn không, chuẩn bị sẵn kịch bản nếu thầy cô hỏi xoáy.

---

### 📝 HƯỚNG DẪN QUẢN LÝ DÀNH CHO ADMIN (KỸ SƯ TRƯỞNG)
Để đôn đốc ông bạn làm việc, ngài hãy lập một thư mục Google Drive dùng chung.
1. Hết Tuần 2, ngài vào Drive yêu cầu ổng nộp file `dataset_clean.csv`. Mở ra xem cột, dòng có mượt không. Nếu rác, bắt làm lại.
2. Hết Tuần 6, yêu cầu ổng nộp cái Link Gradio chạy thử. Ngài trực tiếp đóng vai người dùng nhập mã linh tinh vào xem app có bị sập (crash) không. Mọi thứ phải hoàn hảo trước khi đi bảo vệ!
