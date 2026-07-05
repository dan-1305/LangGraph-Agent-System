# 🧠 LỘ TRÌNH THỰC THI (ROADMAP): KỸ SƯ TRƯỞNG & TIME-SERIES TRANSFORMER

**Mục tiêu:** Xây dựng mạng nơ-ron Attention (Transformer) để dự báo xu hướng chứng khoán. Đây là công nghệ cốt lõi của đồ án.
**Môi trường thực thi:** Google Colab (Bật GPU T4). Code bằng `PyTorch`.
**Nhân sự:** [Tên Ngài] (Core AI Engineer).

---

## 🗓️ GIAI ĐOẠN 1: TIỀN XỬ LÝ & WINDOWING DỮ LIỆU ĐA CHIỀU (TUẦN 3)
*Bạn của ngài đã giao file `dataset_clean_features.csv`. Giờ là lúc biến nó thành Tensor để train.*

### 🎯 Nhiệm vụ 1.1: Chuẩn hóa dữ liệu (Scaling)
- **Công cụ:** `MinMaxScaler` hoặc `StandardScaler` từ `sklearn`.
- **Yêu cầu:** 
  - Mạng Transformer rất nhạy cảm với thang đo. Phải fit_transform toàn bộ các cột (Open, Close, Volume, RSI, MACD...).
  - **Lưu ý chí mạng:** Chỉ `fit` trên tập Train, sau đó `transform` trên tập Test để tránh rò rỉ dữ liệu tương lai (Data Leakage).
  - Lưu scaler lại thành `scaler.pkl` bằng thư viện `joblib` để giao cho ông bạn dùng trên Web.

### 🎯 Nhiệm vụ 1.2: Tạo Sliding Windows (Cửa sổ trượt)
- **Công cụ:** Viết hàm tự tạo Tensor `(batch_size, sequence_length, num_features)`.
- **Yêu cầu:** Chặt chuỗi thời gian thành các đoạn dài `seq_length` (ví dụ 60 ngày). 
  - `X`: Là ma trận 60 ngày gần nhất (gồm nến + chỉ báo).
  - `Y`: Là giá trị của ngày thứ 61 (hoặc `1` nếu ngày 61 giá tăng, `0` nếu giảm).
- **Phân chia tập Train/Val/Test:** (70% - 15% - 15%) theo đúng thứ tự thời gian (KHÔNG dùng random split).

---

## 🗓️ GIAI ĐOẠN 2: DÀN KHUNG KIẾN TRÚC TIME-SERIES TRANSFORMER (TUẦN 4)
*Đây là "Vũ khí bí mật" của đồ án. Thay vì dùng LSTM cũ kỹ, ngài sẽ dùng cơ chế Self-Attention.*

### 🎯 Nhiệm vụ 2.1: Positional Encoding (Mã hóa Vị trí)
- Viết một class `PositionalEncoding` trong PyTorch. Vì Transformer đọc tất cả 60 ngày cùng một lúc (không như LSTM đọc từng ngày), nên ngài phải cộng thêm sóng Sin/Cos vào dữ liệu để model biết ngày nào xảy ra trước, ngày nào sau.

### 🎯 Nhiệm vụ 2.2: Lớp Transformer Encoder
- **Kiến trúc dàn khung (Skeleton):**
  ```python
  import torch
  import torch.nn as nn

  class TimeSeriesTransformer(nn.Module):
      def __init__(self, num_features, d_model=64, nhead=4, num_layers=2, dropout=0.2):
          super().__init__()
          self.input_linear = nn.Linear(num_features, d_model)
          self.pos_encoder = PositionalEncoding(d_model)
          
          # Lõi Transformer của ChatGPT (Nhưng cấu hình siêu nhỏ)
          encoder_layers = nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward=128, dropout=dropout, batch_first=True)
          self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers)
          
          self.decoder = nn.Linear(d_model, 1) # Output ra 1 dự đoán duy nhất

      def forward(self, src):
          src = self.input_linear(src)
          src = self.pos_encoder(src)
          output = self.transformer_encoder(src)
          # Chỉ lấy feature ở node cuối cùng (ngày cuối cùng) để dự đoán
          output = self.decoder(output[:, -1, :]) 
          return output
  ```
- **Ý nghĩa để giải thích với thầy cô:** "Mô hình của em có `nhead=4` (4 cái đầu). Tức là 4 cơ chế Attention sẽ đồng thời nhìn vào 60 ngày qua. Đầu thứ 1 soi xem giá đóng cửa thay đổi thế nào. Đầu thứ 2 soi xem RSI cắt MACD ở đâu. Cuối cùng tổng hợp lại để đưa ra kết luận".

---

## 🗓️ GIAI ĐOẠN 3: TRAINING & GIẢM OVERFITTING (TUẦN 4 - TUẦN 5)
### 🎯 Nhiệm vụ 3.1: Vòng lặp Huấn luyện (Training Loop)
- **Hàm Loss:** `nn.MSELoss()` (nếu đoán giá trị chuẩn) hoặc `nn.BCEWithLogitsLoss()` (nếu đoán xu hướng Tăng/Giảm).
- **Optimizer:** `AdamW` (learning_rate = 1e-4). Thêm `lr_scheduler` để giảm dần learning rate theo thời gian.
- **Yêu cầu:** Chạy trên GPU của Google Colab khoảng 50 Epochs.

### 🎯 Nhiệm vụ 3.2: Early Stopping & Vẽ Biểu Đồ
- Viết code bắt tín hiệu: Nếu Validation Loss không giảm sau 10 epoch, tự động dừng train (Early Stopping) để chống Overfitting.
- Dùng `matplotlib` vẽ biểu đồ so sánh `Train Loss` và `Val Loss`. (Thầy rất thích!).
- Sau khi train xong, nén file mô hình thành `transformer_model.pth` và gửi lại cho bạn ngài.

---

## 🗓️ GIAI ĐOẠN 4: VIẾT BÁO CÁO HỌC SÂU (TUẦN 7)
- **Kỹ sư trưởng (Ngài) đảm nhiệm viết các chương cốt lõi:**
  - **Chương: Cơ sở Lý thuyết:** Giải thích khái niệm Self-Attention, Multi-head Attention khác gì so với LSTM. Tại sao lại cần Positional Encoding.
  - **Chương: Thiết kế Mạng nơ-ron:** Vẽ sơ đồ kiến trúc khối (Block Diagram) của cái `TimeSeriesTransformer` ở trên. 
  - **Chương: Đánh giá Hiệu năng:** Tính toán độ đo `RMSE`, `MAE` trên tập Test (Dữ liệu chưa từng thấy bao giờ). Chèn biểu đồ dự đoán đè lên giá trị thực.