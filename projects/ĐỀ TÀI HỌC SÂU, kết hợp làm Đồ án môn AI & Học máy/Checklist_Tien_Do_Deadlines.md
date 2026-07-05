# CHECKLIST TIẾN ĐỘ THỰC HIỆN ĐỒ ÁN
*(Áp dụng phương pháp Agile - Cuốn chiếu)*

## I. MÔN HỌC SÂU (DEEP LEARNING) - DEADLINE: 13/06/2026
**Phụ trách chính:** Phạm Công Danh (Admin) - Code Core LSTM
**Hỗ trợ:** Nguyễn Công Tiến - Data, Demo UI, Soạn Word

| Mã | Hạng Mục Công Việc | Cấp Độ | Người Phụ Trách | Trạng Thái | Deadline Nội Bộ |
|----|-------------------|--------|----------------|------------|-----------------|
| DL-1 | Cào dữ liệu OHLCV 5 năm (VD: FPT) và Scale Min-Max | Sinh tồn | Tiến | [ ] Chưa làm | 04/06 |
| DL-2 | Code mạng LSTM đơn giản (PyTorch/Keras), xuất Chart | Sinh tồn | Danh | [ ] Chưa làm | 06/06 |
| DL-3 | Đắp bản Draft Word (C1, C2, C4) thành File Báo cáo | Sinh tồn | Tiến | [ ] Chưa làm | 07/06 |
| DL-4 | Tinh chỉnh Model (Dropout, tính RMSE, MAE) | Phòng thủ | Danh | [ ] Chưa làm | 09/06 |
| DL-5 | Thiết kế Slide Thuyết Trình (Học Sâu) | Phòng thủ | Cả 2 | [ ] Chưa làm | 10/06 |
| DL-6 | Tích hợp Model vào Web Streamlit chạy Demo | Nâng cao | Tiến | [ ] Chưa làm | 11/06 |
| DL-7 | In ấn quyển báo cáo, diễn tập thuyết trình | Bứt phá | Cả 2 | [ ] Chưa làm | 12/06 |

---

## II. MÔN HỌC MÁY (MACHINE LEARNING) - DEADLINE: 20/06/2026
**Phụ trách chính:** Nguyễn Công Tiến - Khai phá dữ liệu, ML cơ bản
**Hỗ trợ:** Phạm Công Danh (Admin) - GridSearch, Code Core ML

| Mã | Hạng Mục Công Việc | Cấp Độ | Người Phụ Trách | Trạng Thái | Deadline Nội Bộ |
|----|-------------------|--------|----------------|------------|-----------------|
| ML-1 | Kế thừa Data từ môn Học Sâu, tính RSI, MACD | Sinh tồn | Tiến | [ ] Chưa làm | 14/06 |
| ML-2 | Code Random Forest phân loại Tăng/Giảm | Sinh tồn | Danh | [ ] Chưa làm | 15/06 |
| ML-3 | Hoàn thiện File Báo cáo Word Học Máy | Sinh tồn | Tiến | [ ] Chưa làm | 15/06 |
| ML-4 | Thử nghiệm SVM/XGBoost để so sánh, tính Accuracy | Phòng thủ | Danh | [ ] Chưa làm | 16/06 |
| ML-5 | Thiết kế Slide Thuyết Trình (Học Máy) | Phòng thủ | Cả 2 | [ ] Chưa làm | 17/06 |
| ML-6 | Xuất Feature Importance, Confusion Matrix đẹp | Nâng cao | Danh | [ ] Chưa làm | 18/06 |
| ML-7 | In ấn quyển báo cáo, diễn tập thuyết trình | Bứt phá | Cả 2 | [ ] Chưa làm | 19/06 |

---

## III. TIÊU CHUẨN NGHIỆM THU (RUBRICS)
Để tránh bị bắt bẻ khi lên Hội đồng, trước khi chốt in quyển, phải kiểm tra các tiêu chuẩn sau:

- [ ] **Data Leakage Check:** Tuyệt đối KHÔNG dùng hàm `train_test_split` với tham số `shuffle=True` trên dữ liệu Time-series. Phải cắt data theo thời gian (VD: Train từ 2021-2024, Test 2025-2026).
- [ ] **Reproducibility (Tính tái lặp):** Phải đặt `random_state=42` ở mọi mô hình để code chạy trên máy thầy hay máy mình đều ra cùng 1 kết quả biểu đồ.
- [ ] **Thuyết minh rõ ràng:** Trong Slide phải có 1 trang so sánh Khuyết điểm của Machine Learning (ML) và Ưu điểm bù đắp của Deep Learning (DL) để chứng minh tính liên kết của đề tài.