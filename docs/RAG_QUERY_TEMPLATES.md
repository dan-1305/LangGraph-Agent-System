# 🧠 BỘ CÂU HỎI MẪU RAG (RAG QUERY TEMPLATES FRAMEWORK)

Bộ khung câu hỏi này được thiết kế để chuẩn hóa cách các Agent (và Cline) giao tiếp với hệ thống RAG (`tools/system/rag_query.py`). 
Thay vì hỏi lan man và nhận lại Context nhiễu, việc sử dụng đúng Template theo đúng cấp độ nhiệm vụ sẽ giúp trích xuất chính xác 100% dữ liệu cần thiết từ ChromaDB.

---

## 🟢 CẤP ĐỘ 1: CƠ BẢN (Dành cho Debug, Fix Bug lặt vặt)
*Khi được giao nhiệm vụ sửa một lỗi (Bug) hoặc thay đổi một dòng code nhỏ, hãy query RAG bằng các câu hỏi sau TRƯỚC khi chạm vào file:*

1. **Tra cứu lỗi đã biết:** 
   `"Bách khoa toàn thư có ghi nhận mã lỗi [TÊN_LỖI] hoặc triệu chứng [TRIỆU_CHỨNG] không? Cách giải quyết là gì?"`
2. **Định vị hàm bị lỗi:** 
   `"Trong Bản đồ hệ thống (System Map), hàm [TÊN_HÀM] hoặc class [TÊN_CLASS] nằm ở file nào?"`
3. **Check biến môi trường:** 
   `"Quy định về biến môi trường cho [TÊN_TÍNH_NĂNG] là gì? Có được phép dùng API key trực tiếp không?"`
4. **Luật an toàn:** 
   `"Khi chạy file trên Windows CMD, có cần ép kiểu UTF-8 không? Làm thế nào?"`

---

## 🟡 CẤP ĐỘ 2: NÂNG CAO (Dành cho Tạo Sub-project / Thêm tính năng mới)
*Khi cần viết một Module mới, thêm một Agent mới, hoặc một Tool mới, hãy dùng các câu hỏi sau để học kiến trúc cũ:*

1. **Kế thừa hệ thống Core:** 
   `"Lớp BaseAgent hoạt động như thế nào? Làm sao để tạo một Agent mới kế thừa từ BaseAgent và gọi LLM chuẩn?"`
2. **Cách cấu hình Lịch trình:** 
   `"Cơ chế Scheduler và Smart Catch-up hoạt động thế nào? Làm sao để thêm một Task mới chạy vào lúc 15:00 hàng ngày?"`
3. **Kết nối Module khác:** 
   `"Hàm send_telegram_alert() nhận tham số gì và hoạt động ra sao? Nó nằm ở file nào?"`
4. **Quy tắc Thư mục:** 
   `"Sub-project mới nên đặt ở đâu? (src/ hay projects/) Cấu trúc thư mục chuẩn của một project con là gì?"`
5. **Cấu hình Local Proxy Server & API Rotation:** 
   `"Cơ chế xoay vòng khóa (Fail-on-Demand Key Rotation) trong local_proxy_server hoạt động như thế nào? Làm sao để cấu hình nhiều GEMINI_API_KEYS?"`

---

## 🔴 CẤP ĐỘ 3: CHUYÊN NGHIỆP (Dành cho Thay đổi Kiến trúc Core / Đập đi xây lại)
*CẤM tự ý thay đổi file Core nếu chưa đọc kỹ các cảnh báo sau bằng RAG:*

1. **Hiểu giới hạn sinh tồn:** 
   `"4 Pillars (Bốn Trụ cột sinh tồn) của kiến trúc LangGraph V2 là gì? Circuit Breaker hoạt động ra sao?"`
2. **Tech Debt (Nợ kỹ thuật):** 
   `"Nhật ký JARVIS_CHRONICLES có cảnh báo Tech Debt hay rủi ro gì về RAM/CPU mà tao cần tránh không?"`
3. **Quy trình State mỏng:** 
   `"Disk-as-State và Vector-as-Memory là gì? Tại sao không được lưu string dài vào FactoryState?"`
4. **Fallback:** 
   `"Nếu API LLM sập toàn bộ thì hệ thống đang xử lý Fallback (Try/Except) như thế nào?"`

---

> **LƯU Ý:** Đừng copy y xì câu hỏi trong ngoặc vuông `[...]`. Hãy điền thông số thực tế vào để RAG Vector Search tìm kiếm chính xác nhất bằng cơ chế tính khoảng cách Cosine!
