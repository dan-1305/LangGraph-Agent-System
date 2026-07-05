# BỐI CẢNH DỰ ÁN (CONTEXT)

**Tên dự án**: Hệ thống Dự báo Giá Cổ Phiếu - Đồ án AI & Học Máy  
**Quy mô dữ liệu**: Quan sát 5 năm (2021 - 2026) trên rổ chỉ số VN30 (Đại diện: FPT, HPG, MBB, MWG, VNM).

## 🎯 Mục Tiêu Lõi Của Đồ Án
Dự án được xây dựng với tinh thần ứng dụng AI để tự động hóa hoạt động giao dịch thuật toán (Algorithmic Trading) và giải quyết triệt để rào cản tâm lý của con người (hội chứng FOMO/FUD). Đồ án không chỉ là một công cụ dự đoán, mà là một hệ thống **Quản trị Rủi ro** thông minh. Lộ trình phát triển được thiết kế qua 3 cấp độ:

1. **Cấp độ Học máy (Machine Learning)**: Khai phá không gian dữ liệu OHLCV và các chỉ báo kỹ thuật (RSI, MACD, Bollinger Bands). Ứng dụng **Random Forest / SVM** để phân loại nhãn xu hướng (Tăng / Giảm / Đi ngang), đồng thời tích hợp SMOTE xử lý mất cân bằng nhãn.
2. **Cấp độ Học sâu (Deep Learning)**: Vượt qua giới hạn độ trễ của chỉ báo tĩnh. Sử dụng kỹ thuật trượt cửa sổ thời gian (Sliding Window 30 ngày) và mạng nơ-ron hồi quy **LSTM / GRU** để dự báo đa bước (3-5 phiên tiếp theo), ghi nhớ các chu kỳ dài hạn mà không bị tiêu biến đạo hàm.
3. **Cấp độ Đồ án Tốt nghiệp (Hệ thống Đa Phương Thức & Backtest)**: Dung hợp hai luồng thông tin: Dòng tiền kỹ thuật (LSTM) và Cảm xúc tin tức thị trường (Mô hình ngôn ngữ lớn **FinBERT / PhoBERT**). Kết quả dự báo được đưa vào Engine Backtesting để đánh giá các chỉ số lợi nhuận và phòng vệ rủi ro thực tế (Sharpe Ratio, Max Drawdown).

## 🧩 Luồng Hệ Thống Hoàn Thiện
Thay vì phân chia mã nguồn theo cá nhân, dự án hiện tại đã được **gộp và chuẩn hóa chuyên nghiệp** thành 4 module chính chạy theo luồng Data Pipeline nằm trong thư mục `04_Source_Code`:

- **`1_Data_Pipeline.ipynb`**: Khởi nguồn dữ liệu (Cào giá từ `vnstock`, crawl báo CafeF/Vietstock, làm sạch, tính toán chỉ báo bằng `pandas-ta`).
- **`2_ML_Baselines.ipynb`**: Phân loại xu hướng ngắn hạn (Tăng/Giảm/Sideway) bằng Học máy cổ điển, đo lường độ phủ Precision/Recall/F1-Score.
- **`3_DL_LSTM_Models.ipynb`**: Module Deep Learning hồi quy chuỗi thời gian sử dụng TensorFlow/Keras. Tối ưu hóa với EarlyStopping và cấu trúc đa lớp.
- **`4_Backtesting_Eval.ipynb`**: Engine mô phỏng chiến lược giao dịch tự động. Tích hợp điểm số Sentiment, đánh giá hiệu năng so với chiến lược Buy-and-Hold.

## 📊 Phương Pháp Đánh Giá Chuyên Môn
Hệ thống thoát ly khỏi tư duy chỉ dựa vào "Độ chính xác" (Accuracy) thuần túy. Đồ án sử dụng các công cụ đo lường tiêu chuẩn:
- **Ma trận nhầm lẫn (Confusion Matrix) & AUC-ROC** cho mô hình phân loại.
- Sai số **RMSE / MAE** cho hồi quy chuỗi thời gian.
- **Lợi nhuận ròng, Sharpe Ratio, Max Drawdown** trong mô phỏng giao dịch thực chiến.

*Tài liệu này đóng vai trò như bản đồ tư duy bám sát Đề cương chi tiết của nhóm.*