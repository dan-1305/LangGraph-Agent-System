# Knowledge Base Agent - Project Summary & Guide

## 1. Tổng quan dự án
Knowledge Base Agent là một dự án ứng dụng RAG (Retrieval-Augmented Generation) để tạo ra một chuyên gia học thuật ảo. Dự án sử dụng ChromaDB làm Vector Store và HuggingFace Embeddings để đọc, trích xuất và truy vấn kiến thức từ các tài liệu Ebook.

## 2. Các tệp tin cốt lõi (Core Files) - CẦN ĐỌC KHI MỞ CHAT MỚI
Nếu bắt đầu một phiên chat mới và cần làm việc với dự án này, hãy đọc các tệp sau đầu tiên để lấy ngữ cảnh:
- `src/rag_agent.py`: Agent chính xử lý RAG. Nhận câu hỏi, tìm kiếm (retrieval) context từ ChromaDB và đưa cho LLM tổng hợp câu trả lời.
- `src/ingest.py`: Script dùng để nhúng (embed) dữ liệu từ tài liệu Ebook vào Vector Database (ChromaDB).

## 3. Cấu trúc thư mục
- `src/`: Mã nguồn chính của dự án.
- `data/chroma_db/`: Thư mục lưu trữ cơ sở dữ liệu vector ChromaDB sau khi ingest. (Được lưu tập trung ở thư mục data gốc)

## 4. Luồng hoạt động chính
1. **Ingest dữ liệu:** Chạy `ingest.py` để nhúng các tài liệu dạng Ebook vào `ChromaDB` dùng model embedding `all-MiniLM-L6-v2`.
2. **Khởi tạo Agent:** `RAGAgent` kế thừa từ `BaseAgent`, kết nối vào `ChromaDB`.
3. **Truy vấn:** Người dùng đặt câu hỏi. Hệ thống tìm 3 đoạn văn bản liên quan nhất (k=3) và gửi prompt kèm văn bản cho LLM (`gemini-3.1-pro-preview`) để trả lời chính xác, tránh hallucination (ảo giác).

## 5. Lưu ý quan trọng
- Agent được cấu hình với `temperature=0.3` để đảm bảo độ chính xác học thuật.
- Nếu LLM không tìm thấy thông tin trong Database, nó được prompt phải trả lời rõ là không tìm thấy thay vì tự bịa ra.
- Luôn phải chạy `ingest.py` trước tiên nếu Database chưa có.