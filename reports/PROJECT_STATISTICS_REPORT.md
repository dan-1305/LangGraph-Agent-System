# BÁO CÁO THỐNG KÊ VÀ ĐÁNH GIÁ TRỌNG YẾU DỰ ÁN
*(Ngày tạo: 2026-06-17 20:04:03)*

## 1. Tổng quan
- **Tổng số thư mục (loại trừ .hidden và __pycache__):** 399
- **Tổng số tệp tin:** 1469

## 2. Thống kê theo loại tệp tin (Đuôi file)
| Đuôi file | Số lượng | Tỷ lệ (%) | Mức độ trọng yếu (Ước tính) |
| :--- | :--- | :--- | :--- |
| `.py` | 346 | 23.6% | 🔴 Cao (Core Logic/Config) |
| `.json` | 313 | 21.3% | 🔴 Cao (Core Logic/Config) |
| `no_extension` | 263 | 17.9% | Thấp |
| `.md` | 256 | 17.4% | 🟡 Trung bình (Docs/Scripts/Ops) |
| `.txt` | 47 | 3.2% | 🟢 Thấp (Data/Logs/Archive) |
| `.toml` | 22 | 1.5% | 🔴 Cao (Core Logic/Config) |
| `.log` | 20 | 1.4% | 🟢 Thấp (Data/Logs/Archive) |
| `.zip` | 19 | 1.3% | 🟢 Thấp (Data/Logs/Archive) |
| `.html` | 19 | 1.3% | Thấp |
| `.docx` | 15 | 1.0% | Thấp |
| `.bin` | 13 | 0.9% | Thấp |
| `.pdf` | 13 | 0.9% | Thấp |
| `.bat` | 12 | 0.8% | 🟡 Trung bình (Docs/Scripts/Ops) |
| `.yaml` | 12 | 0.8% | 🟡 Trung bình (Docs/Scripts/Ops) |
| `.db` | 10 | 0.7% | 🟢 Thấp (Data/Logs/Archive) |
| `.bak` | 10 | 0.7% | 🟢 Thấp (Data/Logs/Archive) |
| `.pb` | 10 | 0.7% | Thấp |
| `.tflite` | 10 | 0.7% | Thấp |
| `.png` | 8 | 0.5% | Thấp |
| `.csv` | 8 | 0.5% | 🟢 Thấp (Data/Logs/Archive) |
| `.ipynb` | 7 | 0.5% | Thấp |
| `.yml` | 4 | 0.3% | 🟡 Trung bình (Docs/Scripts/Ops) |
| `.sqlite3` | 4 | 0.3% | Thấp |
| `.mp3` | 4 | 0.3% | Thấp |
| `.pkl` | 3 | 0.2% | Thấp |
| `.mp4` | 2 | 0.1% | Thấp |
| `.pma` | 2 | 0.1% | Thấp |
| `.db-journal` | 2 | 0.1% | Thấp |
| `.lock` | 1 | 0.1% | 🔴 Cao (Core Logic/Config) |
| `.onnx` | 1 | 0.1% | Thấp |
| `.example` | 1 | 0.1% | Thấp |
| `.pickle` | 1 | 0.1% | Thấp |
| `.jsonl` | 1 | 0.1% | Thấp |
| `.conf` | 1 | 0.1% | Thấp |
| `.ini` | 1 | 0.1% | Thấp |
| `.dat` | 1 | 0.1% | Thấp |
| `.baj` | 1 | 0.1% | Thấp |
| `.baf` | 1 | 0.1% | Thấp |
| `.gz` | 1 | 0.1% | Thấp |
| `.js` | 1 | 0.1% | Thấp |
| `.css` | 1 | 0.1% | Thấp |
| `.sh` | 1 | 0.1% | 🟡 Trung bình (Docs/Scripts/Ops) |
| `.xml` | 1 | 0.1% | Thấp |

## 3. Phân tích độ trọng yếu theo cấu trúc thư mục
Hệ thống LangGraph_Agent_System là một kiến trúc đa tầng (Polymorphic Agent System). Độ trọng yếu được đánh giá như sau:

### 🔴 TIER 1 & TIER 2: Vùng Trọng Yếu Cao Nhất (Core & Application Logic)
Đây là bộ não và bộ xương của hệ thống. Bất kỳ thay đổi nào cũng có thể làm sập toàn bộ các Agent.
- `src/` (Đặc biệt là `src/factory/`, `src/base_agent.py`): Khung xương của kiến trúc LangGraph V2. Quản lý trạng thái, node, router.
- `projects/`: Chứa các Agent độc lập (AI Trading, Airdrop, Chaos QA). Mỗi folder đại diện cho một Domain cụ thể với Domain Rules riêng.
- `core/` & `core_engine/`: Các module tiện ích cốt lõi dùng chung.

### 🟡 TIER 3: Vùng Trọng Yếu Trung Bình (Infrastructure & Tooling)
Tầng giao tiếp và công cụ hỗ trợ. Lỗi ở đây thường chỉ ảnh hưởng cục bộ (ví dụ: hỏng một tool quét) chứ không sập core.
- `tools/`: Chứa hàng loạt script tự động hóa (scanner, RAG query, auto mapper...).
- `docs/` & `context/`: Lưu trữ Bách khoa toàn thư, luật lệ, và bản đồ hệ thống cho RAG.
- `scheduler/`: Hệ thống lập lịch chạy tự động.
- `tests/`: Bộ Unit test bảo vệ hệ thống.

### 🟢 TIER 4: Vùng Trọng Yếu Thấp (Ephemeral / Data)
Vùng đệm, lưu trữ kết quả, log hoặc rác. Xóa đi hệ thống vẫn khởi động bình thường.
- `logs/`, `reports/`: Nhật ký và báo cáo đầu ra.
- `archives/`, `_archive_old_files/`: Nơi chứa file cũ, file backup.
- Các thư mục sinh data tạm thời như `images_output/`.

---
*Báo cáo được tự động tạo bởi `tools/scanners/project_stat_analyzer.py`*