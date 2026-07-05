# 🧠 AI ENGINEERING MATURITY MODEL (V1.0)

> **Status:** [ACTIVE] | **Date:** 2026-07-18
> **Reference:** Google "AI Orchestration", Meta "Agentic Workflows", Spotify "Golden Paths".

Tài liệu này định nghĩa 4 cấp độ trưởng thành trong việc ứng dụng AI (đặc biệt là Cline) vào phát triển phần mềm trong Monorepo. Mục tiêu là chuyển dịch từ việc sử dụng AI như "công cụ gõ phím" sang "Người điều phối hệ thống" để tiết kiệm token và tăng ROI.

---

## 📈 The 4 Levels of AI Engineering Maturity

### Level 1: Syntax Assistant (Copilot Mode)
*   **Hành vi:** Admin giao cho AI một file cụ thể và bảo sửa 1 dòng code, fix syntax, hoặc viết Docstring.
*   **Ví dụ:** *"Cline, vào file `main.py` sửa dòng 15 thành `x = 2`"*.
*   **Hệ quả:** Rất tốn Context Window vì AI phải load toàn bộ file chỉ để sửa 1 dòng. Gây phân mảnh tư duy.
*   **Khuyến nghị:** **KHÔNG NÊN DÙNG**. Hãy tự sửa bằng tay hoặc dùng GitHub Copilot nội tuyến.

### Level 2: Local Problem Solver (Feature Mode)
*   **Hành vi:** Admin giao cho AI một task cụ thể trong phạm vi 1 project con. AI tự đọc file, tự đề xuất giải pháp, và tự sửa.
*   **Ví dụ:** *"Cline, tạo thêm tính năng gửi tin báo Telegram khi RAM > 90% trong project `ai_trading_agent`"*.
*   **Hệ quả:** Hiệu quả tốt, AI phát huy được sức mạnh tư duy cục bộ.
*   **Khuyến nghị:** **ĐƯỢC PHÉP DÙNG**. Tuy nhiên, Admin phải giới hạn đường dẫn cụ thể để Cline không quét nhầm thư mục khác.

### Level 3: Architectural Orchestrator (Agentic Mode)
*   **Hành vi:** Admin giao cho AI một "Issue" hoặc "Goal" vĩ mô. AI sử dụng công cụ (MCP, SQLite, Indexer) để tự tìm file lỗi, tự thiết kế giải pháp qua `Sequential Thinking`, và tự thực thi.
*   **Ví dụ:** *"Cline, hệ thống báo lỗi `JSONDecodeError` ở đâu đó trên production, hãy tìm và sửa nó"*.
*   **Hệ quả:** Token được tối ưu tối đa vì AI tự điều hướng qua Metadata DB thay vì đọc file rác.
*   **Khuyến nghị:** **MỨC ĐỘ TIÊU CHUẨN**. Admin nên áp dụng triết lý "Issue-Driven Development" thay vì chỉ đạo trực tiếp.

### Level 4: Autonomous Sovereign (The End Goal)
*   **Hành vi:** AI tự động thức tỉnh qua script, tự đọc báo cáo `MONOREPO_HEALTH_AUDIT.md`, tự sinh RFC cho các project đang ở Level 1 để nâng cấp chúng lên Level 3. Admin chỉ đóng vai trò "Ký duyệt" (Approve).
*   **Ví dụ:** *"Cline thức tỉnh." -> Cline tự báo cáo: "Dự án `ceo_agent` thiếu Test. Xin phép được viết Test."*
*   **Hệ quả:** Monorepo trở thành một thực thể "Tự miễn dịch" và "Tự tiến hóa".

---

## 🛠️ Best Practices for Admin (Issue-Driven AI)

1.  **Don't micro-manage:** Đừng bảo Cline sửa dòng code nào. Hãy cung cấp Traceback Error và để Cline tự dùng MCP tìm file.
2.  **Trust the Metadata:** Khi cần phân tích dự án, hãy yêu cầu Cline query `SYSTEM_MAP_METADATA.db` thay vì dùng lệnh `list_files` hoặc `read_file` hàng loạt.
3.  **Visual Validation:** Luôn yêu cầu Cline chụp màn hình kết quả (qua Playwright) nếu liên quan đến UI.

---
*Prepared by the Principal System Architect.*
