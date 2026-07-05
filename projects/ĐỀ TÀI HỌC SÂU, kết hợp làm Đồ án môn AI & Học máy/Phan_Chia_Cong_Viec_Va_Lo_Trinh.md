# BẢNG PHÂN CÔNG CÔNG VIỆC VÀ LỘ TRÌNH ĐỒ ÁN
**Đề tài:** Dự báo giá cổ phiếu/chỉ số chứng khoán bằng Trí Tuệ Nhân Tạo
**Thành viên:** 
- Nguyễn Công Tiến (Thành viên 2 - Chuyên trách Data/UI/Ops) -> *Phần dễ/Ứng dụng*
- Phạm Công Danh (Admin - Chuyên trách AI Core/Architecture) -> *Phần khó/Cốt lõi*

---

## MÔN 1: HỌC MÁY (MACHINE LEARNING)
*Mục tiêu môn học: Xây dựng mô hình phân loại xu hướng ngắn hạn (Tăng/Giảm).*

### 🧑‍💻 Nguyễn Công Tiến (Thành viên 2)
- **Công việc:** 
  - Khai thác dữ liệu (Data Collection): Viết script cào dữ liệu VN30 từ API (VNDirect/SSI/VNStock).
  - Khám phá dữ liệu (EDA): Vẽ biểu đồ nến, phân tích phân phối dữ liệu.
  - Kỹ nghệ đặc trưng (Feature Engineering): Code các hàm tính toán RSI, MACD, Bollinger Bands bằng thư viện `pandas-ta`.
- **Thuyết trình/Báo cáo:** Trình bày phần Tổng quan dữ liệu và cách chuẩn bị đầu vào cho mô hình Học Máy.

### 🧑‍💻 Phạm Công Danh (Admin)
- **Công việc:**
  - AI Core: Code các mô hình Random Forest, SVM, Logistic Regression bằng `scikit-learn`.
  - Tối ưu hóa: Dùng GridSearch/RandomSearch để dò tìm siêu tham số tốt nhất.
  - Đánh giá: Xây dựng hàm tính Accuracy, Precision, Recall và in ra Confusion Matrix.
- **Thuyết trình/Báo cáo:** Trình bày phần thuật toán lõi, giải thích vì sao chọn Random Forest và so sánh kết quả độ chính xác.

---

## MÔN 2: HỌC SÂU (DEEP LEARNING)
*Mục tiêu môn học: Ứng dụng mạng nơ-ron hồi quy (LSTM) dự báo giá đóng cửa chuỗi thời gian.*

### 🧑‍💻 Nguyễn Công Tiến (Thành viên 2)
- **Công việc:**
  - Tiền xử lý Tensor: Code các hàm trượt cửa sổ thời gian (Sliding Window), biến array 1D thành 3D Tensor cho LSTM. Min-Max Scaling.
  - Giao diện Demo (UI): Xây dựng một trang web đơn giản bằng Streamlit (hoặc Gradio). Người dùng nhập mã VN30 -> Web gọi Model dự báo -> Trả ra biểu đồ.
- **Thuyết trình/Báo cáo:** Trình bày phần Tiền xử lý dữ liệu đặc thù cho DL và Demo trực tiếp phần mềm Web.

### 🧑‍💻 Phạm Công Danh (Admin)
- **Công việc:**
  - AI Core: Thiết kế kiến trúc mạng LSTM / GRU nhiều lớp (Multi-layer) bằng `PyTorch` hoặc `TensorFlow/Keras`.
  - Kỹ thuật nâng cao: Viết các callback như EarlyStopping, Dropout để chống Overfitting (vấn đề rất lớn của chứng khoán).
  - Đánh giá: Tính toán hàm Loss (RMSE, MAE) và xuất đồ thị Training Loss vs Validation Loss.
- **Thuyết trình/Báo cáo:** Trình bày chi tiết về kiến trúc Mạng nơ-ron, phân tích biểu đồ Loss và giải thích vì sao LSTM ưu việt hơn ML tĩnh trong bài toán Time-series.

---

## HƯỚNG TỚI: ĐỒ ÁN TỐT NGHIỆP (AI TRADING AGENT)
*Mục tiêu ĐATN: Xây dựng hệ thống giao dịch tự động Đa phương thức (Multimodal) kết hợp Backtest.*

### 🧑‍💻 Nguyễn Công Tiến (Thành viên 2)
- **Công việc:**
  - Dữ liệu Văn bản (Text): Viết tool Crawl tin tức tài chính (CafeF, Vietstock).
  - DevOps / Ops: Thiết lập cơ sở dữ liệu SQLite lưu trữ lịch sử giao dịch. Viết bot Telegram báo tín hiệu (Signal Alert).
- **Thuyết trình/Báo cáo:** Trình bày Hệ thống Cảnh báo tự động và luồng Data Pipeline.

### 🧑‍💻 Phạm Công Danh (Admin)
- **Công việc:**
  - AI Core (Multimodal): Chạy mô hình PhoBERT/FinBERT để chấm điểm cảm xúc tin tức. Kết hợp vector này với LSTM tạo thành mô hình Đa phương thức.
  - Backtesting Engine: Lập trình (hoặc tích hợp thư viện) để giả lập việc Mua/Bán trong quá khứ, tính toán phí giao dịch, độ trượt giá (Slippage) và kết xuất biểu đồ PnL (Lợi nhuận - Max Drawdown).
- **Thuyết trình/Báo cáo:** Trình bày Kiến trúc Đa phương thức (Sự dung hợp giữa Giá và Tin tức) và phân tích báo cáo Hiệu suất Giao dịch (Backtest Report).

---

## KẾ HOẠCH THỜI GIAN (MILESTONES)
- **Tuần 1-2:** Hoàn thiện source code môn Học Máy (Tiến: Data, Danh: Core). Nộp quyển báo cáo Học Máy.
- **Tuần 3-4:** Hoàn thiện source code môn Học Sâu (Tiến: Web UI, Danh: LSTM Core). Nộp quyển báo cáo Học Sâu.
- **Tuần 5-8:** Tích hợp Backtest, FinBERT và Telegram Bot. Căn chỉnh Slide cho Đồ Án Tốt Nghiệp.