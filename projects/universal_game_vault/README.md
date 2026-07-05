# 🎮 Universal Game Vault

Hệ thống quản lý tri thức game đa nhiệm, sử dụng AI để tự động phân tích tài liệu, xây dựng Wiki và cung cấp chiến thuật.

## 🚀 Tính năng chính
- **Self-Branching Storage:** Tự động tạo không gian lưu trữ cho game mới khi nhận tài liệu.
- **Hybrid Storage:** Lưu trữ file Markdown (Wiki cho người) và SQLite (Data cho máy).
- **AI Analytics:** Phân tích chỉ số nhân vật, giải mã Lore và gợi ý chiến thuật.
- **RAG Ready:** Tích hợp bộ nhớ dài hạn để tra cứu thông tin game nhanh chóng.

## 📁 Cấu trúc dữ liệu (`data/`)
Dữ liệu được chia theo từng game:
- `morimens/`
  - `wiki/`: Các bài viết chi tiết.
  - `raw/`: Tài liệu gốc.
  - `database/`: Cấu trúc dữ liệu SQL.

## 🛠️ Cách sử dụng
1. Chạy `python src/dispatcher.py --game morimens --input "Tài liệu về game..."`
2. AI sẽ tự động phân loại và lưu trữ vào đúng vị trí.
