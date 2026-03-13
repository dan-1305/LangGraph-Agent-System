# MNIST Handwritten Digit Recognition - Project Summary & Guide

## 1. Tổng quan dự án
Dự án thực nghiệm cơ bản về Machine Learning để nhận dạng chữ số viết tay, sử dụng bộ dữ liệu kinh điển MNIST và framework Tensorflow/Keras. Đây là dự án nền tảng giúp làm quen với các khái niệm Computer Vision cơ bản.

## 2. Các tệp tin cốt lõi (Core Files) - CẦN ĐỌC KHI MỞ CHAT MỚI
- `mnist_keras_modern.py`: Triển khai phân loại số viết tay bằng framework Keras hiện đại (Neural Network).
- `mnist_softmax.py`: Triển khai thuật toán Softmax Regression cơ bản, dựa trên tài liệu "MNIST For ML Beginners".

## 3. Mục đích
Dự án mang tính chất thực hành (experiments) và tham khảo tài liệu học tập từ Tensorflow.

## 4. Lưu ý quan trọng
- Tương tự như các dự án ML/Deep Learning khác trong hệ thống, hãy chú ý giới hạn tài nguyên của hệ thống (chip i3-1215u) khi thực thi huấn luyện. Tránh thiết lập số epoch quá cao hoặc batch size quá lớn làm treo máy.