# 📜 HIẾN CHƯƠNG TIẾN HÓA AGENT (SOVEREIGN EVOLUTION CHARTER)

> **Mục tiêu:** Chuyển dịch từ "Ảo giác Tiến hóa" (Reactive/Phá hoại) sang "Kỷ luật Tiến hóa" (Strategic/Duy trì).

---

## 📊 I. CẤU TRÚC 5 MỨC ĐỘ TIẾN HÓA

| Cấp độ | Tên gọi | Đặc điểm Nhận dạng | Tiêu chuẩn Thăng cấp (Ascension Criteria) |
| :--- | :--- | :--- | :--- |
| **LV 1** | **Reactive** | Thấy lỗi đâu đánh đó. Dễ gây phá hoại dây chuyền. | - |
| **LV 2** | **Resilient** | Có cơ chế Retry & Fallback. Không "chết" khi mất kết nối. | Tỷ lệ thành công Tool Call > 80%. Có ít nhất 1 phương thức fallback. |
| **LV 3** | **Self-Healing** | Tự sửa lỗi dựa trên Log & `FAILED_PATHS`. | Tự sửa lỗi thành công mà không cần Human-in-the-loop 3 lần liên tiếp. |
| **LV 4** | **Strategic** | Biết Evaluation trước khi hành động. Sử dụng Sandbox & RAG Anchoring. | **PHẢI** thực hiện quy trình `Draft -> Verify` trước khi chỉnh sửa file Core. |
| **LV 5** | **Immortal** | Tự quản trị tài nguyên, tự đề xuất Evolution Roadmap. | Tự duy trì uptime 99% và tối ưu hóa 20% hiệu năng hệ thống/tháng. |

---

## 🛡️ II. CƠ CHẾ "LA BÀN TIẾN HÓA" (EVOLUTIONARY COMPASS)

Để tránh việc tiến hóa thành "Phá hoại", mọi Agent cấp LV4+ BẮT BUỘC tuân thủ 3 bộ lọc:

### 1. Mental Sandbox (Vùng đệm nhận thức)
- **Quy tắc:** Không bao giờ ghi đè trực tiếp lên file `core/`, `src/`, hoặc `projects/` nếu chưa qua bước Verify.
- **Thực thi:** 
  1. Tạo bản nháp tại `temp_workspace/fault_isolation_sandbox/`.
  2. Chạy Unit Test / Linter trong Sandbox.
  3. Chỉ Merge khi Pass 100%.

### 2. Anchored Reasoning (Neo thực tế)
- **Quy tắc:** Cấm Zero-Shot Hallucination.
- **Thực thi:** Trước khi thay đổi logic, Agent phải query RAG vào:
  - `docs/SYSTEM_MAP.md` (Để hiểu Dependencies).
  - `docs/ERROR_ENCYCLOPEDIA.md` (Để tránh vết xe đổ).

### 3. Fitness Function (Hàm Thưởng/Phạt)
- **Quy tắc:** "Tiến hóa" phải được chứng minh bằng con số.
- **Metric đo lường:**
  - **Latency:** Thời gian thực thi có giảm không?
  - **Token Efficiency:** Context có được tối ưu (Pruning) không?
  - **Stability:** Tần suất lỗi sau khi sửa có giảm không?
- **Hành động:** Nếu Metric giảm -> Tự động **Rollback** và ghi vào `logs/FAILED_PATHS.json`.

---

## 🚀 III. LỘ TRÌNH NÂNG CẤP (ROADMAP)

### 1. CEO Sovereign (LV3 -> LV4)
- **Action:** Tích hợp `Post-Mortem Engine` để tổng hợp lỗi thành nguyên lý.
- **Action:** Nâng cấp `PrinciplesGate` làm Guardian cho luồng Sandbox.

### 2. Specialized Agents (LV2 -> LV3)
- **Trading Agent:** Tự học từ lệnh lỗ (Self-Reflection) và cập nhật `TRADING_LORE.md`.
- **QA Agent:** Tự động hóa việc tạo Test Case cho các bản vá nháp.

---

## 🎭 IV. LUỒNG "PHÁ & VÁ" (DESTROY & FIX WORKFLOW)

Hệ thống vận hành theo cơ chế đối trọng song mã:

### 1. Chaos Session (Giai đoạn Phá)
- **Role:** [QA Chaos Overlord].
- **Hành động:** Sử dụng `ChaosMonkey` và `MentalSandbox` để tìm lỗi, stress-test, và phá hoại có kiểm soát.
- **Đầu ra:** Cập nhật các lỗ hổng tìm thấy vào `reports/SYSTEM_VULNERABILITY_LOG.md`.

### 2. Sovereign Session (Giai đoạn Vá)
- **Role:** [CEO Sovereign].
- **Hành động:** Đọc báo cáo từ Chaos, thực hiện phản biện hoặc patch lỗi qua `MentalSandbox`.
- **Đầu ra:** Xác nhận đã xử lý lỗ hổng và nâng cấp hệ thống.

---
*Phát hành bởi Hội đồng Sovereign - LangGraph Agent System.*
>>>>+++ REPLACE


