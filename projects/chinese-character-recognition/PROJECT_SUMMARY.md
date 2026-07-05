# Chinese Character Recognition - Project Summary & Guide

## 1. Tổng quan dự án
Chinese Character Recognition là một mô hình Machine Learning dùng để nhận diện chữ Hán. Dự án áp dụng Deep Learning với Keras/Tensorflow, kết hợp Batch Normalization để tăng độ chính xác trong việc phân loại chữ.

## 2. Các tệp tin cốt lõi (Core Files) - CẦN ĐỌC KHI MỞ CHAT MỚI
- `chinese_keras_modern.py`: Script huấn luyện/test mô hình (phiên bản Keras hiện đại).
- `chinese_character_recognition_bn.py`: Script huấn luyện có áp dụng Batch Normalization.

## 3. Hiệu suất mô hình (Performance)
- **Top 1 accuracy:** ~0.925 (92.5%)
- **Top k accuracy:** ~0.975 (97.5%)

## 4. Lưu ý quan trọng
- Khi chạy huấn luyện mô hình ML/Deep Learning trên cấu hình máy tính Intel i3-1215u, phải đảm bảo không mở quá nhiều tác vụ song song (`n_jobs=1` hoặc không chạy các batch size quá lớn) để tránh treo máy.