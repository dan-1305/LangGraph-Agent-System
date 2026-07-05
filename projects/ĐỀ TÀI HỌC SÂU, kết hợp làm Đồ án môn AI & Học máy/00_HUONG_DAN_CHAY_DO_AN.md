# HƯỚNG DẪN CHẠY DEMO ĐỒ ÁN (HỌC MÁY & HỌC SÂU)
*(Tài liệu dành cho Giảng viên và Hội đồng chấm thi)*

## 1. CẤU TRÚC MÃ NGUỒN (SOURCE CODE)
Mã nguồn của Đồ án được chia thành 2 phần rõ rệt trong thư mục `Stock_Forecasting_Project/04_Source_Code/`:
- **`Tien_Machine_Learning/`**: Chứa code cào dữ liệu (`01_Tien_Data_Pipeline.ipynb`) và các thuật toán Học máy cơ bản (Random Forest, SVM trong `02_Tien_ML_Baselines.ipynb`).
- **`Danh_Deep_Learning_Core/`**: Chứa code mô hình mạng nơ-ron Học sâu LSTM (`03_Danh_LSTM_Models.ipynb`). 

## 2. NHỮNG ĐIỂM SÁNG TRONG CODE (NÂNG CAO)
Sinh viên đã áp dụng các kỹ thuật tối ưu hóa thay vì chỉ dùng mô hình mặc định:
- **GridSearchCV (Lưới tối ưu):** Được áp dụng trong `02_Tien_ML_Baselines.ipynb` để tự động quét và tìm ra bộ siêu tham số tốt nhất cho Random Forest và SVM.
- **Dự báo Đa bước (Multi-step Forecasting):** Thay vì chỉ dự đoán 1 ngày, mô hình LSTM trong `03_Danh_LSTM_Models.ipynb` được thiết kế cấu trúc `Dense(5)` để dự báo chuỗi 5 ngày liên tiếp trong tương lai.
- **Keras 3.0 với PyTorch Backend:** Áp dụng chuẩn công nghệ mới nhất (`os.environ["KERAS_BACKEND"] = "torch"`) thay vì TensorFlow cũ.
- **ReduceLROnPlateau:** Cơ chế tự động giảm Tốc độ học (Learning Rate) khi phát hiện mô hình có dấu hiệu chững lại, kết hợp cùng lớp Dropout (0.2) để triệt tiêu Overfitting.

## 3. CÁCH CHẠY GIAO DIỆN DEMO (STREAMLIT TRÊN COLAB)
Nhóm đã chuẩn bị sẵn một giao diện Web (Dashboard) cực kỳ trực quan để thầy có thể tự tay kiểm chứng kết quả mô hình.

**Các bước chạy:**
1. Upload thư mục `Stock_Forecasting_Project` lên Google Drive cá nhân.
2. Mở file **`02_Notebooks/05_Demo_Streamlit_Colab.ipynb`** bằng Google Colab.
3. Bấm "Run All" (Chạy tất cả các ô code).
4. Ở ô code cuối cùng, hệ thống sẽ in ra một dòng chữ: `Mật khẩu Endpoint IP của bạn là: 34.xx.yy.zz`. **Hãy copy đoạn số IP này.**
5. Bấm vào đường link `https://...loca.lt` màu xanh xuất hiện bên dưới.
6. Một trang web sẽ mở ra yêu cầu nhập Password. **Dán đoạn số IP vừa copy vào** và bấm Submit.
7. Giao diện Web Dashboard sẽ hiện ra với 2 Tab (Học Máy và Học Sâu). Thầy có thể xem biểu đồ Feature Importance, Loss Chart, và Line Chart so sánh Giá thực tế vs Giá AI dự đoán 5 ngày tới một cách sinh động nhất!