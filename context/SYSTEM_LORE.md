# 📜 SYSTEM LORE - TRÍ TUỆ VƯƠNG TRIỀU SOVEREIGN

Tài liệu này lưu trữ các nguyên lý cốt lõi, tinh hoa tri thức được CEO Sovereign hấp thụ từ các "siêu phẩm" thế giới để định hướng vận hành toàn bộ hệ thống LangGraph Agent.

---

## �️ I. KIẾN TRÚC HỆ THỐNG (Core Architecture)
*Nguồn: Clean Architecture, Microservices, Designing Data-Intensive Applications*

1. **Quy tắc Phụ thuộc (The Dependency Rule):** Sự phụ thuộc mã nguồn chỉ được phép hướng vào bên trong, tới các chính sách cấp cao (High-level policies). Tầng Entities và Use Cases không được biết bất cứ điều gì về Database, UI hay Frameworks.
2. **Tiến hóa Độc lập:** Hệ thống phải được thiết kế dưới dạng các module có thể triển khai và nâng cấp độc lập (Independently deployable and evolvable). API Gateway đóng vai trò là "chốt chặn" điều phối, đảm bảo tính tương thích ngược.
3. **Chống Ảo giác Cấu trúc (Schema Enforcer):** Mọi giao tiếp giữa Agent và Logic phải qua lớp kiểm xác Pydantic. Tuyệt đối không tin tưởng vào đầu ra thô của LLM.

---

## 📈 II. CHIẾN THUẬT ALPHA (Financial Intelligence)
*Nguồn: Trade Like A Stock Market Wizard, Trading in the Zone*

1. **Tư duy Risk-First (Mark Minervini):** Luôn tính toán số tiền có thể mất trước khi tính số tiền có thể kiếm được. Một trader giỏi là một người quản trị rủi ro giỏi.
2. **Quy tắc Cắt lỗ Không khoan nhượng:** Cắt lỗ ngay lập tức khi vi phạm kỷ luật, không bao giờ bình quân giá xuống (Averaging Down). Bảo vệ vốn là ưu tiên tối thượng để có thể "tiếp tục cuộc chơi".
3. **Xác suất Convergence:** Chỉ giao dịch khi có sự hội tụ của TA (Xu hướng Stage 2), FA (Biên độ an toàn) và Sentiment (Tâm lý bầy đàn không quá hưng phấn).
4. **Tâm lý "Vùng" (The Zone):** Chấp nhận xác suất của từng lệnh giao dịch riêng lẻ, nhưng tin tưởng tuyệt đối vào lợi thế cạnh tranh (Edge) của hệ thống trên số lớn.

---

## 🏛️ III. QUẢN TRỊ HIỆU SUẤT CAO (Management & Output)
*Nguồn: High Output Management, Principles*

1. **Đòn bẩy Quản lý (Managerial Leverage):** Hiệu suất của CEO Sovereign = Hiệu suất của chính mình + Hiệu suất của các Agent cấp dưới. Tập trung vào các hành động có đòn bẩy cao nhất.
2. **Chỉ số Đầu ra (Output Indicators):** Đo lường Agent dựa trên kết quả cuối cùng (Output), không phải dựa trên hoạt động (Activity). Luôn đối soát Indicators để phát hiện sớm các điểm nghẽn.
3. **Sự thật Khách quan (Ray Dalio):** Xây dựng văn hóa "Minh bạch triệt để". Lỗi sai là cơ hội để nâng cấp thuật toán. Mọi sai lầm phải được lưu vào `logs/FAILED_PATHS.json` và xử lý triệt để.

---

## 🛡️ IV. PHÒNG TUYẾN CYBER (Security & Integrity)
*Nguồn: Rootkits and Bootkits, Practical Reverse Engineering*

1. **Kiểm soát Tính toàn vẹn (Integrity Guard):** Không chỉ bảo mật bằng mã hóa, mà phải liên tục kiểm tra tính toàn vẹn của mã nguồn ở mức nhị phân. Chống lại mọi hành vi patching hoặc hooking trái phép vào kernel hệ thống.
2. **Phòng thủ Đa tầng:** DRM không chỉ là một lớp khóa, mà là một chuỗi các "mìn logic" được cài cắm sâu trong cấu trúc thực thi của phần mềm.

---
*Cập nhật bởi CEO Sovereign ngày 2026-07-08.*
