# 🗺️ CHIẾN LƯỢC NÂNG CẤP HẠ TẦNG NGỮ CẢNH (SOVEREIGN CONTEXT UPGRADE)

> **Mục tiêu:** Triệt tiêu hoàn toàn tình trạng AI bị "lú" khi chuyển phiên chat và ngăn chặn các lỗi nghẽn môi trường (Venv Lock, Broken Dependencies).

---

## 🛠️ I. CÁC THÀNH PHẦN CỐT LÕI (CORE COMPONENTS)

### 1. Đặc vụ Y tế (`tools/system/health_check.py`)
- **Chức năng:**
    - Kiểm tra Venv Lock (PID nào đang chiếm dụng `.pyd`).
    - Verify thư viện quan trọng: `numpy`, `pandas`, `chromadb`.
    - Kiểm tra tài nguyên: RAM trống > 1GB, Disk D: > 5GB.
    - Kiểm tra trạng thái API trong `.env` (Sơ bộ).
- **Điểm kích hoạt:** Nhúng vào đầu file `awaken.py`.

### 2. Máy nén Nhận thức (`tools/system/context_compressor.py`)
- **Chức năng:**
    - Quét file `context/ACTIVE_THOUGHTS.md`.
    - Nhận diện các hạng mục đã đánh dấu hoàn thành `[x]`.
    - Nén chúng thành 1 dòng tóm tắt trong mục "Sử ký gần đây".
    - Giữ lại chi tiết 100% cho các hạng mục đang chạy `[ ]` hoặc `[/]`.
- **Điểm kích hoạt:** Chạy tự động trong `endtask.py`.

### 3. Bản đồ Thực thể (`tools/system/entity_tracker.py`)
- **Chức năng:**
    - Lưu trữ các "Điểm neo" quan trọng dưới dạng JSON.
    - Ví dụ: Path history mới nhất, Folder game đang test, Model đang ưu tiên.
    - Cập nhật tự động mỗi khi AI phát hiện ra một Path quan trọng.
- **Điểm kích hoạt:** AI chủ động gọi khi tìm thấy dữ liệu mới.

---

## 📈 II. LỘ TRÌNH TRIỂN KHAI (ROADMAP)

1.  **Giai đoạn 1 (Ổn định hạ tầng):**
    - [ ] Viết `health_check.py`.
    - [ ] Cập nhật `awaken.py` để gọi Health Check.
    - [ ] Tích hợp `taskkill` thông minh vào `endtask.py` để giải phóng venv.

2.  **Giai đoạn 2 (Tối ưu bộ nhớ):**
    - [ ] Viết `context_compressor.py`.
    - [ ] Tích hợp vào quy trình SAS (Sovereign Anchoring Protocol).

3.  **Giai đoạn 3 (Bản đồ thực thể):**
    - [ ] Thiết lập cấu trúc `entity_map.json`.
    - [ ] Viết `entity_tracker.py` để quản lý đọc/ghi map.

---

## ⚖️ III. TIÊU CHUẨN HOÀN THÀNH (SUCCESS CRITERIA)
- AI mới (phiên chat sau) nắm bắt bối cảnh trong < 2 lượt chat.
- Không còn lỗi `Access is denied` khi bắt đầu phiên.
- `ACTIVE_THOUGHTS.md` luôn duy trì dưới 100 dòng nhưng đủ ý.

---
*Phê duyệt bởi: CEO Sovereign - 2026-07-09*
