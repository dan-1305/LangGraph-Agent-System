import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import os
import warnings
warnings.filterwarnings('ignore')

# 1. Nạp dữ liệu
DATA_DIR = r'projects\ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy\Stock_Forecasting_Project\01_Data'
TICKER = 'FPT_VN'
csv_path = os.path.join(DATA_DIR, f'{TICKER}_clean.csv')

try:
    # Bỏ qua dòng header phụ nếu MultiIndex
    df = pd.read_csv(csv_path, index_col=0, header=[0,1], parse_dates=True)
    df.columns = df.columns.droplevel(1) # Drop Ticker level
    print(f"Loaded {len(df)} rows.")
except Exception as e:
    try:
        df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    except:
        print("Fallback to dummy data.")
        dates = pd.date_range(start='2021-01-01', periods=1000, freq='B')
        df = pd.DataFrame(np.random.randn(1000, 5), index=dates, columns=['Open', 'High', 'Low', 'Close', 'Volume'])
        df['Close'] = df['Close'].cumsum() + 100

# 2. Feature Engineering đơn giản (Tạo đặc trưng ML)
df['SMA_20'] = df['Close'].rolling(window=20).mean()
df['SMA_50'] = df['Close'].rolling(window=50).mean()
df['Return'] = df['Close'].pct_change()

# Nâng cấp lên 3 nhãn (Tăng, Giảm, Đi ngang)
# Tăng = 1, Giảm = -1, Đi ngang = 0 (Dao động dưới 0.5%)
conditions = [
    (df['Return'].shift(-1) > 0.005),
    (df['Return'].shift(-1) < -0.005)
]
choices = [1, -1]
df['Target'] = np.select(conditions, choices, default=0)

df = df.dropna()

features = ['Close', 'Volume', 'SMA_20', 'SMA_50', 'Return']
X = df[features]
y = df['Target']

# 3. Chia tập Train/Test theo thời gian (Không dùng shuffle=True để tránh Data Leakage)
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 4. Huấn luyện các mô hình Machine Learning (Random Forest & SVM) với GridSearchCV
print("Training Random Forest with GridSearchCV...")
rf_param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20]
}
rf_grid = GridSearchCV(RandomForestClassifier(random_state=42), rf_param_grid, cv=3)
rf_grid.fit(X_train, y_train)
rf_model = rf_grid.best_estimator_
rf_preds = rf_model.predict(X_test)

print("Training SVM with GridSearchCV...")
svm_param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['rbf', 'linear']
}
svm_grid = GridSearchCV(SVC(random_state=42), svm_param_grid, cv=3)
svm_grid.fit(X_train, y_train)
svm_model = svm_grid.best_estimator_
svm_preds = svm_model.predict(X_test)

# 5. Đánh giá kết quả
rf_acc = accuracy_score(y_test, rf_preds)
svm_acc = accuracy_score(y_test, svm_preds)

print(f"Random Forest Accuracy: {rf_acc:.2%}")
print(f"SVM Accuracy: {svm_acc:.2%}")

# 6. Trực quan hóa Feature Importance của Random Forest
importances = rf_model.feature_importances_
indices = np.argsort(importances)

plt.figure(figsize=(10, 6))
plt.title('Mức độ quan trọng của các chỉ báo (Feature Importances)')
plt.barh(range(len(indices)), importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [features[i] for i in indices])
plt.xlabel('Độ quan trọng tương đối')

img_path = os.path.join(DATA_DIR, 'ml_feature_importance.png')
plt.savefig(img_path)
print(f"Saved ml_feature_importance.png")
