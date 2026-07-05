import streamlit as st
import sys
import os
from pathlib import Path
import time

# Thêm core vào path
base_dir = Path(__file__).resolve().parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from projects.godot_translator.core.extractor import GodotExtractor
from projects.godot_translator.core.translator import GodotTranslator
from projects.godot_translator.core.injector import GodotInjector

st.set_page_config(page_title="Godot Game Translator", page_icon="🎮", layout="centered")

st.title("🎮 CÔNG CỤ DỊCH GAME GODOT TỰ ĐỘNG")
st.caption("Passed Release Standards V1.0 | Dịch toàn bộ game Godot bằng AI.")

st.warning("⚠️ Ứng dụng yêu cầu bạn nhập đường dẫn thư mục chứa mã nguồn game Godot (thư mục có chứa các file .gd, .tscn).")

target_dir_str = st.text_input("📂 Nhập đường dẫn thư mục Game (Ví dụ: C:\\Games\\MyGodotGame):")
output_dir_str = st.text_input("💾 Nhập thư mục lưu Game đã dịch (Mặc định: translated_project):", value="translated_project")

col1, col2 = st.columns(2)
with col1:
    ai_model = st.selectbox("🤖 Chọn AI Model:", ["gemini-3.1-flash-lite", "gemini-2.5-flash", "gemini-3.5-flash"])
with col2:
    smart_skip = st.checkbox("Bật Smart Skip", value=True, help="Bỏ qua các file đã dịch thành công trước đó (Giúp Resume nếu lỡ rớt mạng).")

st.divider()

st.write("🎯 Chọn Đầu Ra Bạn Muốn (Đa Năng):")
col_opt1, col_opt2, col_opt3 = st.columns(3)
with col_opt1:
    mod_extract = st.checkbox("📥 1. Chỉ Trích Xuất (Ra CSV)", value=True, help="Quét toàn bộ text trong game và xuất ra file CSV để bạn tự xem/dịch bằng tay.")
with col_opt2:
    mod_translate = st.checkbox("🤖 2. Dịch Tự Động bằng AI", value=True, help="Gọi Gemini dịch toàn bộ file text sang tiếng Việt.")
with col_opt3:
    mod_inject = st.checkbox("📦 3. Đóng Gói Lại (Inject)", value=True, help="Bơm lại text đã dịch vào thư mục Game gốc để tạo ra bản Việt Hóa hoàn chỉnh.")

st.divider()

if st.button("🚀 BẮT ĐẦU XỬ LÝ", type="primary", use_container_width=True):
    if not target_dir_str or not os.path.exists(target_dir_str):
        st.error("❌ Đường dẫn thư mục Game không tồn tại! Vui lòng kiểm tra lại.")
    elif not mod_extract and not mod_translate and not mod_inject:
        st.warning("⚠️ Vui lòng chọn ít nhất 1 quy trình (Trích xuất / Dịch / Đóng gói).")
    else:
        target_dir = Path(target_dir_str)
        output_dir = Path(output_dir_str)
        
        if mod_inject and not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
            
        try:
            with st.status("🚀 Đang khởi động tiến trình...", expanded=True) as status:
                extractor = GodotExtractor(target_dir_str)
                translator = GodotTranslator(model_name=ai_model) if mod_translate else None
                injector = GodotInjector(target_root=target_dir, output_dir=output_dir_str) if mod_inject else None
                
                st.write("🔍 Đang quét danh sách file game...")
                all_files = [p for p in target_dir.rglob("*") if p.is_file()]
                total = len(all_files)
                
                if total == 0:
                    st.error("❌ Không tìm thấy file nào trong thư mục này!")
                else:
                    st.info(f"🔎 Đã tìm thấy tổng cộng {total} files.")
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    csv_export_data = [] # Lưu text nếu chọn chế độ trích xuất
                    
                    for i, file_path in enumerate(all_files):
                        rel_p = file_path.relative_to(target_dir)
                        status_text.text(f"Đang xử lý [{i+1}/{total}]: {rel_p}")
                        
                        if file_path.suffix in [".gd", ".tscn"]:
                            # 1. Trích xuất
                            texts = extractor.extract_from_file(file_path)
                            if texts and mod_extract:
                                for t in texts:
                                    csv_export_data.append({"File": str(rel_p), "Text": t})
                            
                            # 2 & 3. Dịch và Đóng gói
                            if mod_inject:
                                target_path = output_dir / rel_p
                                if smart_skip and target_path.exists() and mod_translate:
                                    pass # Đã có sẵn file đích, bỏ qua gọi AI
                                else:
                                    translations = {}
                                    if texts and mod_translate:
                                        translations = translator.translate_batch(texts)
                                    injector.inject(file_path, translations)
                        else:
                            # Nếu là hình ảnh, âm thanh... chỉ copy nếu bật chế độ Đóng gói
                            if mod_inject:
                                target_path = output_dir / rel_p
                                if not (smart_skip and target_path.exists()):
                                    injector.inject(file_path, {})
                                    
                        progress_bar.progress((i + 1) / total)
                        
                    status.update(label="✅ Hoàn tất tiến trình!", state="complete", expanded=False)
                    
                    # Báo cáo kết quả
                    if mod_extract and csv_export_data:
                        import pandas as pd
                        df = pd.DataFrame(csv_export_data)
                        csv_path = "extracted_game_texts.csv"
                        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                        st.success(f"📥 Trích xuất thành công {len(csv_export_data)} chuỗi văn bản. Đã lưu file `{csv_path}`")
                    
                    if mod_inject:
                        st.success(f"🎉 Tuyệt vời! Game đã được đóng gói và lưu tại: `{output_dir.absolute()}`")
                    
        except Exception as e:
            st.error(f"❌ Tiến trình bị lỗi: {str(e)}")
            st.info("💡 Mẹo: Nếu rớt mạng, hãy bấm CHẠY lại. Hệ thống sẽ tự động Resume nhờ tính năng Smart Skip.")
