# Technical Status Report (Updated)

## 1. Metrics Hiện Tại (Sau khi áp dụng GridSearchCV & Segmentation)
Hệ thống sử dụng K-Fold Cross Validation (cv=3) kết hợp RandomizedSearchCV để tìm tham số tối ưu, tránh Overfitting.
* **Phân khúc High-End (Cao cấp):**
  * **R² Train**: ~0.6445
  * **R² Test**: ~0.4525
  * **MAE Test**: ~4,604,840,148 VND
* **Phân khúc Mass-Market (Phổ thông):**
  * **R² Train**: ~0.6520
  * **R² Test**: ~0.3731
  * **MAE Test**: ~1,929,867,581 VND

*(Ghi chú: Đã áp dụng Log Transformation $\ln(1+x)$ cho biến mục tiêu Price_VND để chuẩn hóa phân phối).*

## 2. Dữ liệu & Tính năng (Features)
* **Số dòng còn lại sau lọc**: 914 dòng (Lọc cơ bản: Xóa NAs, Area 10-1000m2, Price 1tr - 300tr/m2, loại bỏ Outlier bằng Z-Score theo từng Quận).
* **Các biến Features đang dùng (Đã bổ sung 8 biến Regex từ Title)**: 
  * Biến số (Numeric): `Area_m2`, `num_floors`, `width_m`, `alley_width_m`.
  * Biến phân loại (Categorical): `District`, `Province`, `is_frontage`, `is_alley`, `has_furniture`, `Property_Type`, `is_so_hong`.
* **Cơ chế Phân mảnh (Segmentation Logic)**: Dữ liệu được tự động phân rẽ thành `High_End` (Biệt thự, nhà mặt tiền, hoặc quận trung tâm) và `Mass_Market` (các trường hợp còn lại).

## 3. Cấu trúc Folder
Hệ thống đã xác nhận các file trọng yếu nằm đúng vị trí trong thư mục `projects/real_estate_prediction/`:
* `app.py`: Tồn tại (True) - Đã tích hợp bản đồ Folium và cơ chế phân luồng dự báo.
* `train_model.py`: Tồn tại (True) - Có tích hợp Pipeline, ColumnTransformer và Hyperparameter Tuning.
* `data/raw_data.csv`: Tồn tại (True) (hoặc đọc trực tiếp từ SQLite).
* `models/model_high_end.pkl`: Tồn tại (True).
* `models/model_mass_market.pkl`: Tồn tại (True).

## 4. Trạng thái & Blockers
* **Overfitting đã được kiểm soát đáng kể** thông qua việc giảm `max_depth` (xuống 3-4), thêm hệ số phạt `reg_alpha`, `reg_lambda` và áp dụng `min_child_weight`. 
* **Blocker duy nhất hiện tại**: Kích thước bộ dữ liệu (914 rows) là tương đối nhỏ cho việc huấn luyện Machine Learning cường độ cao. Để cải thiện thêm $R^2$ vượt mức 0.60, hệ thống cần được nạp thêm dữ liệu thô (cào thêm khoảng 2000 - 5000 dòng).
