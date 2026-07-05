# 📜 SOVEREIGN MANAGEMENT STANDARDS (V1.0)

> **Status:** [APPROVED] | **Last Update:** 2026-07-18

Tài liệu này quy định các tiêu chuẩn kỹ thuật và quy trình quản lý vòng đời cho tất cả các dự án con trong Monorepo.

---

## 🏆 Project Maturity Framework

| Level | Name | Technical Requirements | Operational Policy |
| :--- | :--- | :--- | :--- |
| **L1** | **Draft / Experimental** | Code chạy được. Không yêu cầu test. Kế thừa `BaseAgent` là tùy chọn. | Chỉ dùng cho nghiên cứu. Bị xóa nếu dormant > 30 ngày. |
| **L2** | **Stable / Internal** | Test Coverage > 80%. Bắt buộc kế thừa `BaseAgent`. Có file `README.md` chuẩn. | Sử dụng cho vận hành nội bộ Monorepo. Được Cline ưu tiên context. |
| **L3** | **Sovereign / Ready** | Docker Sandbox. Visual QA (Playwright). 0 vi phạm Compliance. Bảo mật tuyệt đối. | Sẵn sàng thương mại hóa hoặc triển khai Public. |

---

## 🛠️ Performance & Efficiency Standards

1.  **Token Economy:**
    *   Mọi project phải được index vào `reports/SYSTEM_MAP_METADATA.db`.
    *   Sử dụng RAG cho các file documentation > 1000 dòng.
2.  **Storage Directive:**
    *   Dữ liệu nặng (>50MB) PHẢI lưu tại `D:\Users\Admin\Downloads\LangGraphStorage`.
    *   Tuyệt đối không lưu model hoặc dataset lớn ở ổ C.
3.  **Security (The Death Rule):**
    *   API Key không được hardcode.
    *   Phải qua `compliance_checker.py` trước khi merge vào nhánh chính.

---

## 🔄 Lifecycle Management Process

1.  **Creation:** Sử dụng template Agent chuẩn từ `projects/project_manager_sentry`.
2.  **Audit:** `lifecycle_manager.py` chạy hàng tuần để chấm điểm Maturity.
3.  **Upgrade:** Để nâng cấp từ L1 lên L2, project phải vượt qua bài kiểm tra Pytest tự động.
4.  **Archiving:** Các dự án L1 không đạt KPI sẽ được đưa vào Quarantine (Triple-Filter Protocol).

---
*By Order of the AI Board of Directors.*
