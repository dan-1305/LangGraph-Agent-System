# 📝 SOVEREIGN RFC PROCESS (Request for Comments)

> **Status:** [ACTIVE] | **Date:** 2026-07-18

Mọi thay đổi lớn về kiến trúc hoặc refactor sâu (> 3 core files) trong Monorepo phải tuân thủ quy trình RFC để đảm bảo tính nhất quán và sự đồng thuận của AI Board.

---

## 📅 RFC Workflow

1.  **Drafting:** Cline (CEO) hoặc Agent phụ trách dự án tạo một file `docs/rfc/RFC_YYYYMMDD_NAME.md`.
2.  **Simulation Debate:** Triệu tập AI Board (Architect, Dev, QA, Security) để phản biện bản thảo.
3.  **Approval:** CEO Sovereign ký duyệt (`[APPROVED BY CEO]`).
4.  **Execution:** Bắt đầu triển khai trong ACT Mode.
5.  **Anchoring:** Cập nhật kết quả vào `JARVIS_CHRONICLES.md`.

---

## 📋 RFC Template Standard

*   **Objective:** Tại sao cần thay đổi này? (Vấn đề hiện tại).
*   **Proposed Solution:** Giải pháp kỹ thuật chi tiết (Mermaid Diagrams, Class changes).
*   **Dependencies:** Ảnh hưởng đến các project con khác như thế nào? (Dựa trên Dependency Graph).
*   **Security Risks:** Các rủi ro tiềm ẩn (API leaks, bypass).
*   **Success Metrics:** Làm sao để biết thay đổi này thành công?

---

## ⚖️ Governance Rules

*   **Breaking Changes:** Tuyệt đối không commit code phá vỡ project L3 mà chưa có RFC.
*   **One Version Rule:** RFC phải đề xuất hướng nâng cấp đồng bộ cho toàn Monorepo nếu có thay đổi về thư viện.

---
*By Order of the Principal System Architect.*
