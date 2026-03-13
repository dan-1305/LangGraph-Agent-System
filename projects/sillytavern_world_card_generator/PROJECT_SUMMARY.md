# SillyTavern World Card Generator - Project Summary & Guide

## 1. Tổng quan dự án
SillyTavern World Card Generator là một công cụ giúp tạo tự động các tệp "World Card" (V3) cho SillyTavern bằng trí tuệ nhân tạo (LLMs như Gemini). Hệ thống sử dụng kiến trúc Multi-Agent, nơi mỗi Agent phụ trách một phần công việc chuyên biệt (viết cốt truyện, xây dựng thế giới, thiết lập Regex/Extension) để ghép thành một file JSON duy nhất sẵn sàng nạp vào SillyTavern.

## 2. Các tệp tin cốt lõi (Core Files) - CẦN ĐỌC KHI MỞ CHAT MỚI
Nếu bắt đầu một phiên chat mới và cần làm việc với dự án này, hãy đọc các tệp sau đầu tiên để lấy ngữ cảnh:
- `src/world_card_generator.py`: Lớp Orchestrator quản lý quy trình chạy (Pipeline) gọi tuần tự Storyteller -> Lore Master -> Coder và gộp kết quả thành file World Card V3 chuẩn.
- `ui/app.py`: Ứng dụng giao diện người dùng (chạy web UI) để tiếp nhận ý tưởng người dùng và trả về file World Card JSON.
- `src/models/world_card_v3.py`: Định nghĩa cấu trúc Pydantic cho thẻ World Card V3 (Data, Book, Extensions, v.v.).
- `src/agents/base_agent.py`: Định nghĩa các Agent cơ bản phục vụ cho việc sinh prompt và gọi LLM.

## 3. Cấu trúc thư mục
- `src/agents/`: Chứa mã nguồn của từng Agent cụ thể (`storyteller_agent.py`, `lore_master_agent.py`, `coder_agent.py`).
- `src/models/`: Định nghĩa các Pydantic Models mô phỏng cấu trúc dữ liệu JSON của SillyTavern V3.
- `src/world_card_generator.py`: Flow chính tạo thẻ.
- `ui/`: Chứa file `app.py` cho giao diện người dùng.
- `data/templates/`: Nơi lưu trữ các file mẫu (Lorebook, Preset, Regex, World Card).

## 4. Luồng xử lý chính
1. Nhận ý tưởng (`UserIdeaInput`) từ UI.
2. **Storyteller Agent**: Sinh `system_prompt` và `first_message` (cốt truyện, tính cách thế giới).
3. **Lore Master Agent**: Sinh các mục `Lorebook` để định hình kiến thức thế giới.
4. **Coder Agent**: Lắp ráp các tập lệnh `Regex`/UI Extensions vào thẻ (hiện tại có thể đang dùng template tĩnh).
5. Đóng gói tất cả thành đối tượng `WorldCardV3` và xuất ra file JSON tải về.

## 5. Hướng phát triển tiếp theo (Roadmap)
Dự án được lên kế hoạch phát triển theo 3 giai đoạn chính:

### Giai đoạn 1: Nâng cấp AI Generator (Chất lượng nội dung)
- **RAG (Retrieval-Augmented Generation)**: Sử dụng Vector Database (như ChromaDB) để AI tự động search và "học lỏm" văn phong hoặc luật lệ từ các file mẫu `preset_and_lorebook` (ví dụ: Cơ Nương Bẫy Rập) trước khi sinh thẻ mới.
- **Auto-Balancing Stats (Hệ thống Cân bằng Tự động)**: Tích hợp logic AI tự động tính toán điểm thuộc tính của các Class/Quái vật để không bị "Overpowered" hoặc "Underpowered".

### Giai đoạn 2: Nâng cấp Giao diện (Streamlit UI)
- **Nút Edit từng Entry**: Thêm chức năng chỉnh sửa trực tiếp từng entry Lorebook (Tên, Nội dung) trên giao diện Streamlit trước khi tải về.
- **Dark Mode CSS Customizer**: Cho phép người dùng chọn màu sắc, hình nền của khung Chat/UI (Cyberpunk neon, Fantasy gold...) bằng bảng màu trên Streamlit, sau đó gán thẳng vào code CSS của Regex.

### Giai đoạn 3: Hệ thống Mở rộng Vượt bậc
- **Dynamic Quest Generation (Nhiệm vụ động)**: Agent có khả năng tạo ra một file kịch bản chuỗi nhiệm vụ (Quest Line) phức tạp thay vì chỉ viết Lorebook tĩnh.
- **Tích hợp Text-to-Image**: Gắn API tạo ảnh (như Stable Diffusion/Midjourney) để tự động sinh avatar cho các nhân vật được tạo ra trong Lorebook.

## 6. Lưu ý quan trọng
- Cấu trúc JSON được tuân thủ nghiêm ngặt theo chuẩn V3 của SillyTavern. Đặc biệt phần `extensions` sử dụng `List[Dict[str, Any]]` thay vì Pydantic model cứng để tránh `ValidationError`.
- Việc gọi AI đang ưu tiên dùng Gemini API (`gemini-3.1-pro-preview` và `gemini-2.5-flash`) thông qua `langchain_openai`. 
- Hãy lưu ý cấu hình thiết bị i3-1215u không chịu được tải đồng thời quá lớn. Mặc định xử lý tuần tự (sequential).
