import streamlit as st
import sys
import os

# Thêm đường dẫn thư mục gốc để import module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.world_card_generator import WorldCardGenerator
from src.models.world_card_v3 import UserIdeaInput

# --- CẤU HÌNH PAGE ---
st.set_page_config(
    page_title="🛠️ AI World Card Generator V3",
    page_icon="🌍",
    layout="wide"
)

st.title("AI World Card Generator for SillyTavern V3")
st.markdown("""
Tại đây, bạn có thể nhập ý tưởng về thế giới game mà bạn muốn tạo. 
AI sẽ tự động sinh ra đầy đủ **System Prompt**, **Lorebook**, và **Extensions (Regex/CSS/JS)**.
""")

# --- SIDEBAR: INPUT ---
with st.sidebar:
    st.header("📝 Nhập Ý Tưởng (Input)")
    
    user_theme = st.text_input("Tên Thế Giới / Chủ Đề (Theme)", placeholder="Ví dụ: Cyberpunk Cultivator")
    user_details = st.text_area("Mô Tả Chi Tiết", placeholder="Ví dụ: Một thành phố ngầm nơi tu tiên cấy ghép phần thân...", height=150)
    
    # Multi-select cho tính năng
    available_features = [
        "Stat Bars (Thanh HP/MP)",
        "Gacha System (Hệ thống rút thẻ)",
        "Class Selection (Chọn lớp nhân vật)",
        "Inventory System (Kho đồ)",
        "Quest Log (Nhật ký nhiệm vụ)"
    ]
    user_features = st.multiselect("Tính Năng Mong Muốn (Features)", available_features, default=["Stat Bars (Thanh HP/MP)", "Gacha System (Hệ thống rút thẻ)"])
    
    user_style = st.selectbox("Phong Cách", ["Epic", "Dark", "Humorous", "Mysterious"], index=0)
    
    st.divider()
    st.header("🧠 Tùy Chọn AI Nâng Cao (Giai Đoạn 1)")
    
    # Lấy danh sách các file mẫu trong thư mục world_card
    template_dir = os.path.join(os.path.dirname(__file__), "..", "data", "templates", "world_card")
    template_files = ["Không"]
    if os.path.exists(template_dir):
        template_files.extend([f for f in os.listdir(template_dir) if f.endswith('.json')])
        
    user_template = st.selectbox("Học Lỏm File Mẫu (RAG Thu Nhỏ)", template_files, help="AI sẽ đọc file này để bắt chước văn phong và cách chia mục Lorebook.")
    user_balance = st.checkbox("Tự Động Cân Bằng Chỉ Số (Auto-Balancing)", value=False, help="Áp dụng quy tắc cân bằng RPG để tránh các chỉ số quá OP hoặc quá phế.")
    
    st.info("Nhấn nút bên dưới để AI bắt đầu sinh dữ liệu.")

# --- MAIN AREA: OUTPUT ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Điểu khiển (Status)")
    placeholder_card = {
        "card_name": "Chưa có dữ liệu...",
        "card_description": "Nhập ý tưởng và bấm Generate...",
        "tags": [],
        "system_prompt": "System prompt sẽ hiện ở đây...",
        "first_message": "...",
        "lorebook": [],
        "extensions": []
    }

    if 'current_card' not in st.session_state:
        st.session_state.current_card = placeholder_card

# Nút GENERATE
    if st.button("🚀 GENERATE WORLD CARD", type="primary", use_container_width=False, width='stretch'):
        st.session_state.generating = True
        st.rerun()

    # Xử lý logic sinh dữ liệu (Mocking API Call)
    if st.session_state.get('generating', False):
        with st.spinner("🤖️ AI đang tư duy và viết code..."):
            # 1. Gom input
            # Sửa lại để đảm bảo features map với các regex key (VD: "Class Selection", "Gacha", "Stat")
            idea = UserIdeaInput(
                theme=user_theme if user_theme else "Mặc định",
                details=user_details,
                features=[f.split('(')[0].strip() for f in user_features], # Extract raw feature name
                style=user_style,
                template_reference=user_template,
                auto_balance=user_balance
            )
            # 2. Chạy Generator
            generator = WorldCardGenerator()
            generated_card = generator.generate(idea)
            
            # 3. Lưu vào session
            st.session_state.current_card = generated_card.model_dump()
            st.session_state.generating = False

# Hiển thị kết quả
card_data = st.session_state.current_card

with col2:
    st.subheader("📜 Kết Quả (Output)")
    
    # Lấy data theo chuẩn mới của V3
    inner_data = card_data.get("data", {})
    
    # Tab 1: Tổng quan
    with st.expander("1. Tổng Quan", expanded=True):
        st.json({
            "card_name": card_data.get("name", ""),
            "card_description": card_data.get("description", ""),
            "tags": card_data.get("tags", []),
            "version": card_data.get("spec_version", ""),
            "spec": card_data.get("spec", "")
        })
    
    # Tab 2: System Prompt
    with st.expander("2. System Prompt & First Message"):
        st.text_area("System Prompt:", card_data.get("description", ""), height=150)
        st.text_area("First Message:", card_data.get("first_mes", ""), height=200)
        
    # Tab 3: Lorebook
    with st.expander("3. Lorebook (Danh mục)"):
        char_book = inner_data.get("character_book", {})
        if char_book and char_book.get("entries"):
            import pandas as pd
            # Flatten data để hiển thị bảng
            table_data = []
            for entry in char_book["entries"]:
                table_data.append({
                    "ID": entry.get("id"),
                    "Key (Tên)": entry.get("comment"),
                    "Từ Khóa (Trigger)": ", ".join(entry.get("keys", [])),
                    "Nội dung": entry.get("content")
                })
            df = pd.DataFrame(table_data)
            
            # Sử dụng st.data_editor để người dùng chỉnh sửa
            edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="lorebook_editor")
            
            # Cập nhật lại dữ liệu vào session state khi có sự thay đổi
            if st.button("💾 Lưu thay đổi Lorebook", type="secondary"):
                new_entries = []
                # Lấy extensions mặc định từ entry đầu tiên để copy sang
                default_extensions = char_book["entries"][0].get("extensions", {}) if len(char_book["entries"]) > 0 else {}
                
                for idx, row in edited_df.iterrows():
                    keys_list = [k.strip() for k in str(row["Từ Khóa (Trigger)"]).split(",") if k.strip()]
                    new_entry = {
                        "id": int(row["ID"]) if not pd.isna(row["ID"]) else idx,
                        "keys": keys_list,
                        "secondary_keys": [],
                        "comment": str(row["Key (Tên)"]),
                        "content": str(row["Nội dung"]),
                        "constant": False,
                        "selective": True,
                        "insertion_order": 100,
                        "enabled": True,
                        "position": "before_char",
                        "use_regex": True,
                        "extensions": default_extensions
                    }
                    new_entries.append(new_entry)
                
                st.session_state.current_card["data"]["character_book"]["entries"] = new_entries
                st.success("✅ Đã lưu thay đổi! Bạn có thể tải file JSON ở bên dưới.")
        else:
            st.write("Chưa có dữ liệu Lorebook.")
            
    # Tab 4: Extensions (Code)
    with st.expander("4. Extensions (Code/Regex)"):
        ext_data = inner_data.get("extensions", {}).get("regex_scripts", [])
        if ext_data:
            for ext in ext_data:
                st.code(f"// Tên Script: {ext.get('scriptName')}\n// Find: {ext.get('findRegex')}\n{ext.get('replaceString')}", language="javascript")
        else:
            st.write("Chưa có dữ liệu Extensions.")

    # Tab 5: 🎨 Image Prompts (Avatar)
    if user_image_prompt:
        with st.expander("5. 🎨 Image Prompts (Copy để vẽ Avatar)"):
            st.write("Copy các đoạn text dưới đây ném vào Midjourney hoặc Stable Diffusion để vẽ hình cho nhân vật:")
            for entry in char_book.get("entries", []):
                import re
                content = entry.get("content", "")
                match = re.search(r"\[Image Prompt:(.*?)\]", content)
                if match:
                    st.text_area(f"🎨 {entry.get('comment')}", match.group(1).strip(), height=80)

    # Tab 6: Tùy biến giao diện (Theme Customizer)
    with st.expander("6. 🖌️ Tùy biến giao diện (CSS Customizer)"):
        st.write("Thay đổi màu sắc khung chat cho SillyTavern.")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            bg_color = st.color_picker("Màu nền (Background)", "#1a1a1a")
        with col_c2:
            text_color = st.color_picker("Màu chữ (Text)", "#e8e8e8")
        with col_c3:
            primary_color = st.color_picker("Màu chủ đạo (Primary)", "#3b82f6")
            
        if st.button("✨ Áp dụng Theme"):
            theme_css = f"""<style>
:root {{
    --bg-card: {bg_color} !important;
    --text-primary: {text_color} !important;
    --accent-1: {primary_color} !important;
}}
</style>"""
            # Tìm xem đã có regex theme chưa
            ext_list = st.session_state.current_card.get("data", {}).get("extensions", {}).get("regex_scripts", [])
            
            theme_regex = {
                "id": "custom_theme_css_injection",
                "scriptName": "Tùy biến giao diện (Theme)",
                "disabled": False,
                "runOnEdit": True,
                "findRegex": "/<StatusPlaceHolderImpl\\/>/g", 
                "replaceString": theme_css,
                "trimStrings": [],
                "placement": [1, 2],
                "substituteRegex": 0,
                "minDepth": None,
                "maxDepth": None,
                "markdownOnly": True,
                "promptOnly": False
            }
            
            # Update current card
            existing = [e for e in ext_list if e.get("id") != "custom_theme_css_injection"]
            existing.append(theme_regex)
            
            if "data" not in st.session_state.current_card:
                st.session_state.current_card["data"] = {}
            if "extensions" not in st.session_state.current_card["data"]:
                st.session_state.current_card["data"]["extensions"] = {}
                
            st.session_state.current_card["data"]["extensions"]["regex_scripts"] = existing
            
            # Cần đảm bảo First Message có chứa thẻ <StatusPlaceHolderImpl/>
            fm = st.session_state.current_card.get("first_mes", "")
            if "<StatusPlaceHolderImpl/>" not in fm:
                st.session_state.current_card["first_mes"] = fm + "\n<StatusPlaceHolderImpl/>"
                st.session_state.current_card["data"]["first_mes"] = st.session_state.current_card["first_mes"]
                
            st.success("✅ Đã áp dụng Theme! Khi xuất file nạp vào ST, giao diện sẽ đổi màu.")

# Nút DOWNLOAD JSON
import json
json_str = json.dumps(card_data, indent=2, ensure_ascii=False)
st.download_button(
    label="📥 Tải về File JSON (SillyTavern V3)",
    data=json_str,
    file_name="world_card_generated.json",
    mime="application/json",
    use_container_width=False,
)

# Footer
st.markdown("---")
st.caption("AI System powered by Streamlit + Python. Made by LangGraph Agent.")
