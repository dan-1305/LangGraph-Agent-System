# 🌍 GLOBAL AI SIMULATOR BENCHMARK & THE ARENA MASTER (V1.0)

> **Status:** [ACTIVE] | **Date:** 2026-07-18
> **Core References:** Project Eden, NVIDIA Voyager, Princeton SWE-agent, Stanford Generative Agents (Smallville).

Tài liệu này đối chiếu hệ thống "Sovereign Roleplay Sandbox" (The Arena Master) mà chúng ta đang xây dựng với các dự án "AI Simulator" hàng đầu thế giới, qua đó chứng minh tính khả thi và sức mạnh của hệ thống.

---

## 🔬 1. Các Trụ Cột Nghiên Cứu Toàn Cầu

### A. VOYAGER (NVIDIA / Caltech)
*   **Bối cảnh:** LLM sinh tồn trong môi trường Minecraft (Không gian 3D).
*   **Cơ chế cốt lõi:** Khám phá dựa trên **"Thư viện Kỹ năng" (Skill Library)** và học tập qua lỗi (Error Trace). Khi AI ghép sai công thức, nó nhận lỗi, tự động viết lại code và lưu thành kỹ năng mới.
*   **Áp dụng vào Hệ thống:** Tương đương với cơ chế **Memory MCP** (Lưu trữ FAILED_PATHS) của chúng ta. Thay vì Minecraft, chúng ta bắt Cline "sinh tồn" trong Monorepo Python.

### B. SWE-agent (Princeton University)
*   **Bối cảnh:** AI giải quyết các lỗi phần mềm (GitHub Issues) trong môi trường thực.
*   **Cơ chế cốt lõi:** Cấp cho AI một Terminal (Bash/Python) thu nhỏ. AI tự gõ lệnh `grep` để tìm file lỗi, dùng edit tool để sửa, và tự chạy `pytest` để kiểm chứng.
*   **Áp dụng vào Hệ thống:** Đây chính là nền tảng của **Arena Master**. Thay vì báo cáo tĩnh, AI phải tự thao tác với các MCP Tools (`read_file`, `replace_in_file`, `execute_command`) để sửa code.

### C. Generative Agents (Stanford / Smallville)
*   **Bối cảnh:** 25 AI sinh hoạt trong một thị trấn ảo (Sims-like).
*   **Cơ chế cốt lõi:** Hệ thống **Memory Stream** liên tục lưu trữ sự kiện, nén (compress) và truy xuất lại (Retrieval) để AI phản ứng tự nhiên với ngoại cảnh mà không cần kịch bản.
*   **Áp dụng vào Hệ thống:** Kiến trúc **Tri-Brain Memory** và cách thiết lập **System Prompt Nhập vai** (Roleplay Prompting) để Cline không bị "thoát vai" khi chữa cháy server.

---

## ⚔️ 2. Hệ thống The Arena Master (Vương Triều Giả Lập)

Thay vì chi hàng ngàn đô la chạy các container Docker đắt đỏ như SWE-agent, chúng ta sẽ mô phỏng lại toàn bộ trải nghiệm này bằng chiến lược **Zero-Cost Local Sandbox**.

### Cấu trúc Hoạt động của Arena Master:
1.  **Git-Backed Isolation (Cách ly):** 
    Khi `arena_master.py` chạy, nó tự động tạo nhánh `sandbox/arena_run`. Mọi thứ AI đập phá sẽ không ảnh hưởng đến nhánh `main`.
2.  **AST Sabotage (Tạo Khủng Hoảng Thực):** 
    Không còn là những tin nhắn báo lỗi giả vờ. Script sẽ dùng thư viện `ast` để "ăn mất" một lệnh `import`, hoặc đảo ngược logic (vd: `if True:` thành `if False:`) trong một file Core ngẫu nhiên.
3.  **The Gladiator Roleplay (Ép buộc Nhập vai):** 
    Cline sẽ nhận được một Prompt: *"Ngươi đang ở trong Arena. Lỗi `NameError` vừa xảy ra ở `ai_trading_agent`. Hãy dùng MCP SQLite để tìm file, dùng `sequentialthinking` để vạch kế hoạch, và sửa nó. Trọng tài (Pytest) đang theo dõi."*
4.  **Auto-Reflection & Reset (Học hỏi & Dọn dẹp):** 
    Nếu Cline pass Pytest, hệ thống ghi "Chiến thắng" vào Memory MCP. Sau đó, `git reset --hard` xóa bỏ toàn bộ đấu trường.

---

## ⚖️ 3. So sánh trực diện

| Tiêu chí | SWE-agent (Princeton) | The Arena Master (Ours) | Điểm Giao Thoa |
| :--- | :--- | :--- | :--- |
| **Môi trường** | Docker Container | Git Branching (Local) | Cả hai đều cấp cho AI quyền thao tác Terminal/Files. |
| **Dữ liệu Lỗi** | Github Issues (2000+ files) | Lỗi được tự động sinh ra (AST Sabotage) | AI đều phải tự đọc Traceback để sửa. |
| **Chi phí** | Rất cao (~$3/issue) | Gần như bằng Không | Tối ưu Token nhờ Metadata DB của chúng ta. |
| **Học hỏi** | Không lưu lại kỹ năng | **Memory MCP** (Kế thừa từ Voyager) | Arena Master kết hợp cả khả năng "Thực hành" và "Ghi nhớ". |

### 🎯 Tổng kết:
"Arena Master" không chỉ là một trò chơi. Nó là phòng tập (Gym) tinh gọn nhất, vay mượn sự chân thực của SWE-agent, cơ chế học hỏi của Voyager, và sự nhập vai của Smallville. Nó sẽ biến Cline từ một cỗ máy gõ phím thành một **Sovereign Agent** thực thụ.
