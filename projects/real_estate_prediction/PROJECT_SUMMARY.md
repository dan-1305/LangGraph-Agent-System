# Real Estate Prediction - Project Summary & Guide

## 1. Tổng quan dự án
Real Estate Prediction là một dự án ứng dụng Machine Learning để dự đoán giá bất động sản dựa trên các đặc trưng cơ bản (Diện tích, Quận/Huyện, Tỉnh/Thành phố). Ứng dụng cung cấp một giao diện web cơ bản và các script dùng để huấn luyện mô hình.

## 2. Các tệp tin cốt lõi (Core Files) - CẦN ĐỌC KHI MỞ CHAT MỚI
Nếu bắt đầu một phiên chat mới và cần làm việc với dự án này, hãy đọc các tệp sau đầu tiên để lấy ngữ cảnh:
- `app.py`: File chạy ứng dụng Web (có thể sử dụng Flask hoặc framework tương tự) để phục vụ việc nhập dữ liệu và trả về dự đoán giá.
- `train_model.py`: Script chịu trách nhiệm đọc dữ liệu, tiền xử lý, huấn luyện mô hình (Machine Learning) và lưu lại các file `.pkl`.
- `reports/Technical_Status_Report.md`: Báo cáo cập nhật nhất về trạng thái mô hình hiện tại (các chỉ số R², MAE), các vấn đề đang gặp phải (Overfitting, Outliers).

## 3. Cấu trúc thư mục
- `app.py`: Web server ứng dụng dự đoán.
- `train_model.py`: Script huấn luyện mô hình chính.
- `generate_word_report.py`: Sinh báo cáo Word tự động từ kết quả.
- `data/`: Chứa file `raw_data.csv` (Dữ liệu đầu vào).
- `models/`: Lưu các file mô hình đã được huấn luyện (`model.pkl`, `model_high_end.pkl`, `model_mass_market.pkl`).
- `reports/`: Lưu trữ các file báo cáo định dạng Markdown và Word (`ChiTietBaoCao_DeCuong.md`, `Technical_Status_Report.md`, `Bao_Cao_Tieu_Luan_BDS.docx`).
- `templates/`: Chứa giao diện HTML (`index.html`).

## 4. Đặc điểm Mô hình & Hiện trạng (Tính đến báo cáo gần nhất)
- **Features đang dùng**: `Area_m2`, `District`, `Province`.
- **Transformation & Tuning**: Áp dụng Log Transformation và giới hạn độ sâu mô hình (`max_depth = 8`).
- **Issues/Blockers**: Vấn đề Overfitting chưa được giải quyết triệt để (R² Test thấp hơn nhiều so với R² Train) do nhiễu và outliers trong tập dữ liệu.

## 5. Lưu ý quan trọng
- Khi thay đổi dữ liệu hoặc phương pháp tiền xử lý (ví dụ: Feature Extraction mới từ cột Title), cần chạy lại `train_model.py` để ghi đè `models/model.pkl`.
- Dự án này chủ yếu tập trung vào việc Tuning mô hình và xử lý dữ liệu để cải thiện R² Test. Tôn trọng giới hạn resource: nếu chạy GridSearch/RandomSearch, hãy để `n_jobs=1` để tránh treo máy i3.