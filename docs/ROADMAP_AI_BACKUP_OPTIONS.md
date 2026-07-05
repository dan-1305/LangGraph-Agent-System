# 🛟 LỘ TRÌNH DỰ PHÒNG (BACKUP OPTIONS): KỸ SƯ TRƯỞNG & DỰ BÁO CHỨNG KHOÁN

*Tài liệu này chứa các dàn khung kiến trúc (Skeleton) dự phòng. Trong trường hợp Option B (Transformer) gặp khó khăn khi huấn luyện, quá tốn tài nguyên hoặc khó giải thích với hội đồng bảo vệ, Kỹ sư trưởng có thể lập tức xoay trục (pivot) sang một trong hai phương án này để đảm bảo tiến độ Đồ án.*

---

## 🛠️ DÀN KHUNG OPTION A: THUẦN LSTM (Long Short-Term Memory)
**Định vị:** Giải pháp an toàn, tiêu chuẩn vàng của mọi đồ án chuỗi thời gian. Dễ hiểu, dễ code, dễ giải thích với thầy cô.

### 1. Kiến trúc mạng `TimeSeriesLSTM` (PyTorch)
LSTM xử lý dữ liệu theo cơ chế tuần tự (từng ngày một), giữ lại bộ nhớ ngắn hạn và dài hạn để dự báo ngày tiếp theo.

```python
import torch
import torch.nn as nn

class TimeSeriesLSTM(nn.Module):
    def __init__(self, num_features, hidden_size=64, num_layers=2, dropout=0.2):
        super(TimeSeriesLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # Lõi LSTM cốt lõi
        self.lstm = nn.LSTM(
            input_size=num_features,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        
        # Lớp Linear (Fully Connected) để ép đầu ra về 1 dự đoán
        self.fc = nn.Linear(hidden_size, 1)
        
    def forward(self, x):
        # x shape: (batch_size, sequence_length, num_features)
        
        # Khởi tạo trạng thái ẩn (hidden state) và trạng thái tế bào (cell state)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        # Đưa qua mạng LSTM
        out, _ = self.lstm(x, (h0, c0))
        
        # Chỉ lấy đầu ra ở bước thời gian cuối cùng (ngày cuối của window)
        out = out[:, -1, :]
        
        # Đưa qua lớp Linear để ra giá trị dự đoán
        predictions = self.fc(out)
        return predictions
```

### 2. Ưu điểm & Điểm cộng lúc bảo vệ:
- Code cực kỳ ngắn gọn, không cần hàm Positional Encoding phức tạp như Transformer.
- Dễ dàng trực quan hóa cơ chế Cổng Quên (Forget Gate) và Cổng Nhớ (Input Gate) bằng sơ đồ.
- Tốc độ huấn luyện trên Google Colab T4 siêu tốc (chỉ khoảng 5-10 phút cho 100 epochs).

---

## 🛠️ DÀN KHUNG OPTION C: KIẾN TRÚC LAI (HYBRID LSTM + XGBOOST)
**Định vị:** Kiến trúc "Thực dụng", mang tính chất Kỹ sư Dữ liệu (Data Engineering) chuyên sâu. Lấy tinh hoa của Deep Learning nhồi vào sức mạnh của Tree-based Model.

### 1. Ý tưởng Kiến trúc (Pipeline)
Thay vì dùng LSTM để dự đoán thẳng giá cổ phiếu, ta sẽ dùng LSTM để **Rút trích đặc trưng (Feature Extraction)**. Sau đó kết hợp với các chỉ báo kỹ thuật (RSI, MACD) đút vào **XGBoost** để ra quyết định cuối cùng.

### 2. Dàn khung Code Triển khai (Python)

**Bước 1: Lấy Đặc Trưng Từ LSTM (Embeddings)**
Sau khi huấn luyện mô hình `TimeSeriesLSTM` ở Option A, ta không lấy giá trị cuối cùng, mà cắt bỏ lớp `self.fc` đi. Ta lấy vector `out[:, -1, :]` (ví dụ có kích thước 64 chiều).

```python
# Giả sử model_lstm đã được train xong
model_lstm.eval()
with torch.no_grad():
    # Lấy vector ẩn 64 chiều từ tập Train và Test
    lstm_features_train = model_lstm.lstm(X_train)[0][:, -1, :].cpu().numpy()
    lstm_features_test  = model_lstm.lstm(X_test)[0][:, -1, :].cpu().numpy()
```

**Bước 2: Nối (Concat) dữ liệu LSTM với TA-Lib Data**
```python
import numpy as np

# Nối 64 cột tính năng của LSTM với các cột MACD, RSI có sẵn
hybrid_X_train = np.hstack((lstm_features_train, traditional_features_train))
hybrid_X_test  = np.hstack((lstm_features_test, traditional_features_test))
```

**Bước 3: Đưa vào XGBoost & Giải thích mô hình**
```python
import xgboost as xgb
import matplotlib.pyplot as plt

# Khởi tạo mô hình XGBoost
xgb_model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5)
xgb_model.fit(hybrid_X_train, y_train)

# Dự đoán
predictions = xgb_model.predict(hybrid_X_test)

# ĐẶC SẢN CỦA XGBOOST: Hiển thị Feature Importance (Mức độ quan trọng của Đặc trưng)
xgb.plot_importance(xgb_model, max_num_features=10)
plt.title("Những yếu tố quyết định giá Cổ Phiếu")
plt.show()
```

### 3. Ưu điểm & Điểm cộng lúc bảo vệ:
- Thể hiện kỹ năng **Ensemble Learning** (Học kết hợp) cực tốt, hiếm có nhóm sinh viên nào làm tới mức này.
- Thầy cô rất thích khi sinh viên biết dùng **XGBoost Feature Importance** hoặc **SHAP values** để giải thích (Explainable AI) được mô hình (Ví dụ: Biểu đồ sẽ chứng minh rằng "RSI quan trọng hơn Khối lượng", hoặc "Trí nhớ của LSTM đóng vai trò số 1 trong dự đoán"). Khắc phục hoàn toàn điểm yếu "Hộp Đen" (Blackbox) của mạng Nơ-ron.
