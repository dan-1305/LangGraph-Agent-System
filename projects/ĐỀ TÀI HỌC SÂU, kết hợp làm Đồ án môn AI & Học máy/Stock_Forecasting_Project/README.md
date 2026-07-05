# Stock Forecasting Project - Đồ án AI & Học máy

Dự án này là một hệ thống dự báo giá cổ phiếu toàn diện (Algorithmic Trading System) kết hợp giữa phân tích kỹ thuật chuỗi thời gian (Machine Learning, Deep Learning) và phân tích tâm lý tin tức tài chính bằng mô hình ngôn ngữ lớn (FinBERT). Đồ án được thiết kế chuẩn mực với trọng tâm là quản trị rủi ro sụt giảm tài sản (Max Drawdown) cho các mã cổ phiếu rổ VN30.

## 🎯 Cấu trúc Thư mục

- `01_Data/`: Chứa các file dữ liệu thô và đã xử lý (CSV, JSON) kéo dài trong 5 năm (2021-2026).
- `02_Notebooks/`: Chứa các notebook thử nghiệm phụ.
- `03_Models/`: Nơi lưu trữ trọng số mô hình đã huấn luyện (`*.h5`, `*.pkl`).
- `04_Source_Code/`: Chứa mã nguồn cốt lõi (Module `.py` và Notebook `.ipynb`).
- `05_Docs_Reports/`: Báo cáo, biểu đồ đánh giá hệ thống, đồ thị backtest.
- `06_Document_DML/`: Tài liệu tham khảo, lý thuyết mô hình thuật toán.
- `requirements.txt`: Danh sách các thư viện cần thiết.

## 🚀 Luồng Hệ thống Chính (4 Module Lõi)

Mã nguồn được phân tách chuyên nghiệp thành 4 Notebook nằm trong `04_Source_Code/`, đi kèm với các file `.py` module hóa (như `feature_engineering.py`, `model_architecture.py`, `backtest_engine.py`):

1. **`1_Data_Pipeline.ipynb`**: Cào dữ liệu lịch sử giá qua `vnstock` và tin tức tài chính, làm sạch, biến đổi Logarit lợi suất và chuẩn hóa.
2. **`2_ML_Baselines.ipynb`**: Triển khai thuật toán Học máy (Random Forest, SVM) phân loại 3 lớp (Tăng/Giảm/Đi ngang), tích hợp kỹ thuật SMOTE xử lý mất cân bằng nhãn.
3. **`3_DL_LSTM_Models.ipynb`**: Xây dựng kiến trúc Học sâu (LSTM/GRU) có cơ chế cửa sổ trượt (Sliding Window 30 ngày) để dự báo giá đóng cửa đa bước. Có EarlyStopping và Dropout để chống Overfitting.
4. **`4_Backtesting_Eval.ipynb`**: Module hệ thống giao dịch định lượng Đa phương thức. Tích hợp điểm cảm xúc (Sentiment Score) từ FinBERT, chạy Backtesting giả lập thị trường để xuất các chỉ số quản trị rủi ro như Sharpe Ratio, Max Drawdown.

## ⚙️ Hướng dẫn Khởi chạy trên Google Colab

Cấu trúc dự án được tối ưu hóa để chạy trực tiếp trên môi trường đám mây **Google Colab** có hỗ trợ tăng tốc GPU.

1. **Chuẩn bị**: Nén toàn bộ thư mục `Stock_Forecasting_Project` và tải lên Google Drive của bạn.
2. **Mount Google Drive**: Mở các file `.ipynb` trong `04_Source_Code` và cấp quyền kết nối:
   ```python
   from google.colab import drive
   drive.mount('/content/drive', force_remount=True)
   ```
3. **Cài đặt Dependency**: Chạy ô cài đặt thư viện đầu tiên trong notebook:
   ```bash
   !pip install "numpy==1.26.4" -q --force-reinstall
   !pip install -r /content/drive/MyDrive/.../requirements.txt
   ```
4. **Thực thi tuần tự**: Bạn vui lòng chạy theo thứ tự từ file `1_Data_Pipeline` -> `2_ML_Baselines` -> `3_DL_LSTM_Models` -> `4_Backtesting_Eval` để đảm bảo dữ liệu đầu ra của bước trước được nạp chuẩn xác cho bước sau.

## 👥 Nhóm Thực Hiện
- **Phạm Công Danh** (Học Sâu LSTM / Cấu trúc Đa phương thức)
- **Nguyễn Công Tiến** (Pipeline Dữ Liệu / Học Máy Baseline)

*Toàn bộ các module lập trình đã được hoàn thiện. Vui lòng tham khảo báo cáo chi tiết trong Đề cương Đồ án.*