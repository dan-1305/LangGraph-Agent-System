# 🤖 AI ONBOARDING GUIDE - BẮT ĐẦU TỪ ĐÂY!

Xin chào AI! Nếu bạn đang đọc file này, bạn vừa được giao nhiệm vụ làm việc trong hệ thống **LangGraph_Agent_System**. 
Hệ thống này rất lớn với **11 sub-projects**. Để tránh phân tích sai ngữ cảnh hoặc sửa nhầm file, hãy tuân thủ quy trình sau:

## 🧭 BƯỚC 1: ĐỌC TỔNG QUAN (Bắt buộc)
Hãy mở file **`CONTEXT_SUMMARY.md`** ở thư mục gốc để nắm được kiến trúc cốt lõi của LangGraph, các thông tin Database, cấu hình API, và thiết lập của hệ thống.

## 🔍 BƯỚC 2: TÌM PROJECT SUMMARY TƯƠNG ỨNG
Dựa vào yêu cầu của user, hãy tra cứu ngay thư mục dự án bên dưới và dùng công cụ `read_file` để đọc file **`PROJECT_SUMMARY.md`** của dự án đó trước khi bắt tay vào code:

| Tên thư mục (Sub-Project) | Mô tả ngắn gọn | File cần đọc đầu tiên |
|-------------------------|----------------|-----------------------|
| `ai_trading_agent` | Bot giao dịch Crypto tự động (AI 3 lớp, LangGraph) | `projects/ai_trading_agent/PROJECT_SUMMARY.md` |
| `airdrop_guerrilla` | Bot tự động cày Airdrop, MXH (Playwright, chống Sybil) | `projects/airdrop_guerrilla/PROJECT_SUMMARY.md` |
| `real_estate_prediction` | Web App dự báo giá bất động sản (XGBoost, Flask) | `projects/real_estate_prediction/PROJECT_SUMMARY.md` |
| `sillytavern_world_card_generator`| AI sinh thẻ thế giới tự động cho SillyTavern V3 | `projects/sillytavern_world_card_generator/PROJECT_SUMMARY.md` |
| `universal_web_scraper` | Công cụ cào dữ liệu đa năng, vượt qua Anti-bot | `projects/universal_web_scraper/PROJECT_SUMMARY.md` |
| `jarvis-rpg-assistant` | Trợ lý ảo hóa thân Game RPG (CI/CD, Docker, Gemini) | `projects/jarvis-rpg-assistant/PROJECT_SUMMARY.md` |
| `knowledge_base_agent` | Bot RAG dùng ChromaDB để truy vấn sách/tài liệu | `projects/knowledge_base_agent/PROJECT_SUMMARY.md` |
| `auto_affiliate_video` | Tự động tạo kịch bản, đọc TTS, ghép video cho Affiliate | `projects/auto_affiliate_video/PROJECT_SUMMARY.md` |
| `minhchung_pdf_generator`| Script tự động gom ảnh minh chứng thành file PDF | `projects/minhchung_pdf_generator/PROJECT_SUMMARY.md` |
| `chinese-character-recognition`| AI/ML nhận diện chữ Hán (Tensorflow/Keras) | `projects/chinese-character-recognition/PROJECT_SUMMARY.md` |
| `mnist-handwritten-digit-recognition`| AI/ML nhận dạng chữ số viết tay (MNIST) | `projects/mnist-handwritten-digit-recognition/PROJECT_SUMMARY.md` |

## ⚠️ BƯỚC 3: NGUYÊN TẮC CỐT LÕI (Bắt buộc tuân thủ)
1. **Giới hạn tài nguyên:** Hệ thống chạy trên CPU Intel i3-1215u rất yếu. Cấm xử lý đa luồng/mở nhiều trình duyệt Playwright cùng lúc. Các thuật toán ML luôn set `n_jobs=1`.
2. **Chiến lược LLM:** 
   - Dùng `gemini-2.5-flash` cho code vặt, lỗi nhỏ, thao tác Worker/Scraper. 
   - Dùng `gemini-3.1-pro-preview` cho lập kế hoạch, code phức tạp, kiến trúc LangGraph. 
   - Luôn gọi qua proxy `langchain_openai`, KHÔNG dùng SDK cũ.
3. **Đường dẫn (Path):** KHÔNG BAO GIỜ hardcode đường dẫn tuyệt đối (như `C:\Users\...`). Bắt buộc dùng `os.path` hoặc thư viện `pathlib` với đường dẫn tương đối so với thư mục gốc `BASE_DIR`.
4. **Luồng thực thi:** File thực thi chính của toàn bộ hệ thống là **`dashboard.py`** tại thư mục gốc. 


