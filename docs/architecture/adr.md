# Quyết định kiến trúc (Architecture Decision Records - ADR)

Trang này lưu trữ các quyết định kiến trúc cốt lõi của hệ thống **LangGraph Agent System**.

## ADR-001: Sử dụng Local Proxy cho mọi API Calls
- **Trạng thái:** Đã chấp thuận
- **Bối cảnh:** Việc sử dụng các API key trực tiếp trong từng Agent dẫn đến rủi ro lộ key, khó khăn khi quản lý Rate Limit, và khó áp dụng quy tắc "The Death Rule" (Cấm gọi thẳng API Google/OpenAI).
- **Quyết định:** Tất cả các truy vấn (I/O) ra bên ngoài đều phải chạy qua `local_proxy_server` ở cổng 8000. Các endpoint bên ngoài sẽ bị chặn nếu gọi từ các module bên trong mà không thông qua Proxy.
- **Hệ quả:** Dễ dàng thay đổi LLM model ở Proxy mà các Agent không cần đổi code. Tích hợp Load Balancer tự động.

## ADR-002: Kiến trúc Đa đặc vụ (Polymorphic System)
- **Trạng thái:** Đã chấp thuận
- **Bối cảnh:** Nhu cầu mở rộng ra hàng loạt mảng (Trading, Web Scraper, Auto Video, CEO Agent) khiến cho mã nguồn dễ bị rối và lặp lại code (Spaghetti code).
- **Quyết định:** Chia hệ thống thành 1 `src.base_agent` dùng chung (quản lý bộ nhớ, State, Tools) và nhiều `projects/` tách biệt, mỗi project kế thừa từ BaseAgent và có logic riêng.
- **Hệ quả:** Cho phép mở rộng thành 100 dự án mà không dẫm chân lên nhau. Dễ dàng debug bằng phương pháp "Khoanh vùng lỗi đa chéo".

## ADR-003: Docs as Code (MkDocs)
- **Trạng thái:** Mới áp dụng
- **Bối cảnh:** Tài liệu rải rác, không cập nhật, và hay bị AI "ảo giác".
- **Quyết định:** Chuyển tài liệu từ Markdown thủ công sang `mkdocs-material` và tự động đọc (crawl) docstrings từ code thông qua `mkdocstrings`.
- **Hệ quả:** Web tài liệu luôn phản ánh đúng 100% code mới nhất. Developer/AI bắt buộc phải viết docstring chuẩn.