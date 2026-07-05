# 🗺️ STRATEGIC PLAN Q4 2026: BEYOND ZERO-TOLERANCE

*Dựa trên kết quả phiên tranh biện (Board Summit 2026-07-16) và việc đạt chuẩn Zero-Tolerance Compliance toàn hệ thống.*

---

## 🎯 1. TẦM NHÌN QUÝ 4 (Q4 VISION)
Kiến trúc LangGraph Agent System sẽ dịch chuyển từ trạng thái "Gia cố thụ động" (Passive Hardening) sang trạng thái "Tự miễn dịch & Nhận thức sâu" (Active Immunity & Deep Cognition). Hệ thống không chỉ cần chạy đúng, mà phải tự nhận biết lỗi, tự tìm kiếm trong ký ức và tự triển khai môi trường cách ly cho các module rủi ro cao.

---

## 🛠️ 2. CÁC MỤC TIÊU TRỌNG ĐIỂM (CORE OBJECTIVES)

### 🧱 PHASE 1: FOUNDATION (Robust CI/CD & Testing)
- **Tech Debt Resolution:** Khắc phục triệt để lỗi `ValueError: underlying buffer has been detached` của Pytest trên môi trường Windows (do xung đột quản lý `sys.stdout` buffer).
- **Automated Chaos:** Triển khai **Chaos Monkey V2**, tự động bắn phá hệ thống định kỳ. Tích hợp trực tiếp với `admin_simulator.py` để ép hệ thống rơi vào trạng thái FATAL ngẫu nhiên, giúp rèn luyện "Ký ức thất bại" cho CEO Agent.

### 🧠 PHASE 2: INTELLIGENCE (Deep RAG & Vector DB Integration)
- **Local Vector Database:** Tích hợp ChromaDB (hoặc FAISS) chạy cục bộ, hoàn toàn offline.
- **Cognitive Shift:** Chuyển đổi toàn bộ `ACTIVE_THOUGHTS.md`, `JARVIS_CHRONICLES.md`, và `FAILED_PATHS.json` thành các Vector tri thức.
- **Dynamic Context Injection:** Các Agent cốt lõi (như `QAAgent`, `CEOAgent`) sẽ không cần nhồi nhét toàn bộ file text vào prompt. Chúng sẽ tự động truy vấn Vector DB để bốc xuất chính xác đoạn ký ức/bài học tương ứng với bối cảnh (JIT Context Manager V2).

### 🛡️ PHASE 3: DEFENSE (Dockerized Sandbox)
- **Shadow Sentinel V6 Isolation:** Dự án tình báo hình ảnh NSFW (`nsfw_multimedia_auditor`) sở hữu rủi ro cực cao về bảo mật và tài nguyên (NudeNet, Whisper, Moondream). 
- **Containerization:** Toàn bộ sub-project này bắt buộc phải được đóng gói vào Docker Container riêng biệt. Mọi giao tiếp với Monorepo chính phải thông qua API REST nội bộ hoặc WebSocket, cắt đứt hoàn toàn quyền truy cập trực tiếp vào File System chính của OS.

---

## 📅 3. LỘ TRÌNH THỰC THI (TIMELINE)
- **Tuần 1 - Tuần 2:** Sửa lỗi Pytest Buffer, ổn định CI/CD. Đưa Chaos Monkey vào luồng Test.
- **Tuần 3 - Tuần 4:** Cài đặt ChromaDB, viết tool Ingestion tự động hóa chuyển đổi Markdown sang Vector. Tái cấu trúc Prompt cho các Agent lõi.
- **Tháng tiếp theo:** Xây dựng `Dockerfile` và `docker-compose.yml` cho dự án `nsfw_multimedia_auditor`. Hoàn thiện luồng API nội bộ.

---
*Phê duyệt bởi: [CEO Sovereign & Hội Đồng AI]*
*Lệnh thực thi: [Q4 KICK-OFF]*
