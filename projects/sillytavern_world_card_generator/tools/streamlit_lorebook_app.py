import streamlit as st
import json
import requests
import re
from typing import Dict, List, Optional

# --- Ollama AI Extractor Logic ---
class OllamaLorebookExtractor:
    def __init__(self, api_url: str = "http://localhost:11434"):
        self.api_url = api_url.rstrip("/")

    def get_available_models(self) -> List[str]:
        """Fetches available models from the Ollama instance."""
        try:
            response = requests.get(f"{self.api_url}/api/tags", timeout=5)
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except requests.exceptions.RequestException as e:
            st.error(f"Lỗi kết nối đến Ollama API: {e}")
            return []

    def extract_with_ai(self, text: str, model_name: str, char_name: Optional[str] = None) -> Dict:
        """Sends text to Ollama and expects a JSON response formatted for SillyTavern."""
        
        system_prompt = """
        Bạn là một chuyên gia phân tích văn học và tạo Lorebook cho ứng dụng SillyTavern.
        Nhiệm vụ của bạn là đọc đoạn văn bản được cung cấp và trích xuất thông tin chi tiết về các nhân vật.
        
        YÊU CẦU ĐẦU RA BẮT BUỘC:
        Bạn CHỈ ĐƯỢC PHÉP trả về một chuỗi JSON hợp lệ, không có markdown formatting (như ```json), không có giải thích thêm.
        Định dạng JSON phải chính xác như sau:
        {
          "entries": {
            "0": {
              "uid": 0,
              "key": ["Tên Nhân Vật 1", "Biệt danh 1"],
              "keysecondary": [],
              "comment": "Tên Nhân Vật 1",
              "content": "{\\"character_profile\\\": {\\"basic_info\\\": {\\"name\\\": \\\"Tên Nhân Vật 1\\\"}, \\\"appearance\\\": \\\"Mô tả ngoại hình chi tiết...\\\", \\\"personality\\\": \\\"Mô tả tính cách chi tiết...\\\", \\\"clothing\\\": \\\"Mô tả trang phục...\\\"}}",
              "constant": false,
              "vectorized": false,
              "selective": true,
              "selectiveLogic": 0,
              "addMemo": true,
              "order": 100,
              "position": 0,
              "disable": false,
              "ignoreBudget": false,
              "excludeRecursion": false,
              "preventRecursion": false,
              "probability": 100,
              "useProbability": true,
              "depth": 4,
              "displayIndex": 0
            }
            // Thêm các mục "1", "2"... nếu có nhiều nhân vật
          }
        }
        
        Lưu ý cực kỳ quan trọng: Phần "content" bên trong mỗi entry PHẢI LÀ MỘT CHUỖI JSON ĐƯỢC ESCAPE (Stringified JSON), không phải là một object.
        """

        user_prompt = f"Vui lòng phân tích đoạn văn sau và tạo Lorebook JSON."
        if char_name:
             user_prompt += f" Tập trung vào nhân vật tên là: {char_name}."
        user_prompt += f"\n\nĐoạn văn:\n{text}"

        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "format": "json" # Ollama support forcing JSON output
        }

        try:
            response = requests.post(f"{self.api_url}/api/chat", json=payload, timeout=120)
            response.raise_for_status()
            result_json_str = response.json().get("message", {}).get("content", "")
            
            # Basic cleanup in case model returns markdown despite instructions
            result_json_str = re.sub(r'```json\n|\n```', '', result_json_str).strip()
            
            return json.loads(result_json_str)
        except requests.exceptions.RequestException as e:
            st.error(f"Lỗi khi gửi yêu cầu tới AI: {e}")
            return None
        except json.JSONDecodeError as e:
            st.error(f"Lỗi phân tích JSON từ AI. AI đã trả về định dạng không hợp lệ:\n\n{result_json_str}")
            return None

# --- Streamlit UI ---
st.set_page_config(page_title="AI Lorebook Extractor", layout="wide")

st.title("🤖 SillyTavern Lorebook Extractor (Ollama Local AI)")
st.write("Công cụ trích xuất thông tin nhân vật từ truyện và tạo Lorebook JSON chuẩn SillyTavern bằng **Local LLM** qua Ollama.")
st.write("*Bảo mật 100%, không lo kiểm duyệt (Uncensored).*")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Cấu hình Ollama")
    api_url = st.text_input("Ollama API URL", value="http://localhost:11434")
    
    extractor = OllamaLorebookExtractor(api_url=api_url)
    models = extractor.get_available_models()
    
    if not models:
        st.error("Không tìm thấy model nào. Hãy chắc chắn Ollama đang chạy.")
        selected_model = None
    else:
        st.success(f"Kết nối thành công. Tìm thấy {len(models)} models.")
        selected_model = st.selectbox("Chọn Model AI", options=models)
        
    st.divider()
    st.markdown("### Hướng dẫn")
    st.markdown("1. Bật Ollama trên máy tính của bạn.\n2. Tải một model uncensored (VD: `ollama run llama3`).\n3. Tải file truyện `.txt` vào khung bên phải.\n4. Bấm 'Tạo Lorebook'.")

# Main Content
uploaded_file = st.file_uploader("Tải lên file truyện (.txt) hoặc dán văn bản", type=["txt"])
text_input = st.text_area("Hoặc dán trực tiếp đoạn truyện vào đây (Tối đa ~2000 từ để AI xử lý tốt nhất):", height=200)

target_character = st.text_input("Tên nhân vật cụ thể muốn trích xuất (Tùy chọn, để trống AI sẽ tự tìm):")

if st.button("Tạo Lorebook bằng AI", type="primary", disabled=not selected_model):
    content_to_process = ""
    if text_input.strip():
        content_to_process = text_input.strip()
    elif uploaded_file is not None:
        content_to_process = uploaded_file.read().decode("utf-8")
        
    if not content_to_process:
        st.warning("Vui lòng tải lên file hoặc dán văn bản truyện.")
    else:
        # Prevent context window overflow for local models
        if len(content_to_process) > 15000:
            st.warning("Văn bản khá dài. Đã tự động cắt xuống 15,000 ký tự đầu tiên để tránh tràn RAM AI.")
            content_to_process = content_to_process[:15000]

        with st.spinner(f'Đang nhờ {selected_model} đọc truyện và trích xuất Lorebook... Vui lòng đợi (có thể mất 1-3 phút)'):
            lorebook_data = extractor.extract_with_ai(content_to_process, selected_model, target_character)
            
            if lorebook_data:
                st.success("Tạo Lorebook thành công!")
                
                json_str = json.dumps(lorebook_data, ensure_ascii=False, indent=2)
                
                st.subheader("Xem trước kết quả")
                st.json(lorebook_data)
                
                st.download_button(
                    label="⬇️ Tải xuống Lorebook.json",
                    data=json_str,
                    file_name="AI_Extracted_Lorebook.json",
                    mime="application/json",
                    use_container_width=True
                )