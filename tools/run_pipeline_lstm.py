import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import os
import warnings
warnings.filterwarnings('ignore')

# 1. Nạp dữ liệu
DATA_DIR = r'projects\ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy\Stock_Forecasting_Project\01_Data'
TICKER = 'FPT_VN'
csv_path = os.path.join(DATA_DIR, f'{TICKER}_clean.csv')

try:
    # Bỏ qua 2 dòng header đầu tiên nếu file có MultiIndex
    df = pd.read_csv(csv_path, index_col=0, header=[0,1], parse_dates=True)
    # Lấy đúng Series Close
    close_series = df['Close'].iloc[:, 0]
    data = close_series.values.reshape(-1, 1)
    print(f"Loaded {len(data)} rows.")
except Exception as e:
    print(f"File format issue or not found. Fallback to simple format.")
    try:
        df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
        data = df['Close'].values.reshape(-1, 1)
    except:
        print("Fallback to dummy data.")
        data = (np.random.randn(1000, 1).cumsum() + 100).reshape(-1, 1)

# 2. Chuẩn hóa dữ liệu (Scaling)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

training_data_len = int(np.ceil(len(data) * 0.8))
train_data = scaled_data[0:int(training_data_len), :]

print(f"Train size: {len(train_data)}")

# 3. Tạo Sliding Window (Multi-step: 5 days)
window_size = 60
forecast_days = 5
x_train, y_train = [], []

for i in range(window_size, len(train_data) - forecast_days + 1):
    x_train.append(train_data[i-window_size:i, 0])
    y_train.append(train_data[i:i+forecast_days, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
print(f"Shape of x_train: {x_train.shape}")
print(f"Shape of y_train: {y_train.shape}")

# 4. Khai báo Môi trường Keras 3.0 với PyTorch Backend theo tài liệu thầy
os.environ["KERAS_BACKEND"] = "torch"
import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

print(f"Using Keras version: {keras.__version__}")
print(f"Backend in use: {keras.backend.backend()}")

model = Sequential([
    keras.Input(shape=(x_train.shape[1], 1)),
    LSTM(50, return_sequences=True),
    Dropout(0.2), # Chống Overfitting theo bài 2
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(25, activation='relu'),
    Dense(5)
])

model.compile(optimizer='adam', loss='mean_squared_error')
model.summary()

# Huấn luyện thực tế (Training)
print("Starting training...")
from keras.callbacks import ReduceLROnPlateau

lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6, verbose=1)

# Sử dụng 20% dữ liệu train để Validation chống Overfitting
history = model.fit(x_train, y_train, batch_size=32, epochs=20, validation_split=0.2, callbacks=[lr_scheduler], verbose=1)

# Chuẩn bị dữ liệu Test
test_data = scaled_data[training_data_len - window_size:, :]
x_test = []
for i in range(window_size, len(test_data)):
    x_test.append(test_data[i-window_size:i, 0])
x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Lấy nhãn thực tế
y_test = []
for i in range(window_size, len(test_data) - forecast_days + 1):
    y_test.append(test_data[i:i+forecast_days, 0])
y_test = np.array(y_test)
y_test = scaler.inverse_transform(y_test)

# Sửa lại x_test để khớp với y_test
x_test = []
for i in range(window_size, len(test_data) - forecast_days + 1):
    x_test.append(test_data[i-window_size:i, 0])
x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Dự đoán thực tế
predictions_scaled = model.predict(x_test)
predictions = scaler.inverse_transform(predictions_scaled)
print("Training complete!")

# Vẽ biểu đồ Loss
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Theo dõi hàm mất mát (Loss) qua các Epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
loss_chart_path = os.path.join(DATA_DIR, 'lstm_loss_chart.png')
plt.savefig(loss_chart_path)
print(f"Saved loss chart to {loss_chart_path}")

# 5. Đánh giá và Vẽ biểu đồ
rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
print(f"RMSE (Multi-step 5 Days): {rmse:.2f}")

plt.figure(figsize=(16,8))
plt.title('Đánh giá LSTM Dự báo Đa bước (5 Phiên Tới)')
plt.xlabel('Cửa sổ dự đoán', fontsize=18)
plt.ylabel('Giá Đóng cửa', fontsize=18)

# Vẽ 50 mẫu đầu tiên để biểu đồ không bị rối rắm do quá nhiều dự đoán đè lên nhau
for i in range(50):
    plt.plot(range(i, i+5), y_test[i], color='green', alpha=0.5, label='Thực tế' if i==0 else "")
    plt.plot(range(i, i+5), predictions[i], color='red', linestyle='dashed', alpha=0.8, label='Dự đoán 5 Ngày' if i==0 else "")

plt.legend(loc='lower right')
plt.grid(True)

img_path = os.path.join(DATA_DIR, 'lstm_prediction_chart.png')
plt.savefig(img_path)
print(f"Saved chart.")
