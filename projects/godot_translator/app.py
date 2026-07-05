import streamlit as st
import sys
import os
from pathlib import Path
import time
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx

# Thêm root dự án vào path để import đúng namespace 'projects.x.y'
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from projects.godot_translator.core.extractor import GodotExtractor
from projects.godot_translator.core.translator import GodotTranslator
from projects.godot_translator.core.injector import GodotInjector
from projects.godot_translator.core.cyber_security import InjectionGuard
from projects.godot_translator.core.pack_manager import PackManager, DRMError
from utils.ui_helper import ui_error_guard

# --- DICTIONARY ĐA NGÔN NGỮ (i18n) ---
LANG_DICT = {
    "vi": {
        "title": "🎮 CÔNG CỤ DỊCH GAME GODOT 1-CLICK",
        "caption": "Phiên bản B2C Thương Mại | Tự động Unpack -> Dịch -> Test -> Repack.",
        "step1_title": "### Bước 1: Chọn Game & Cấu Hình",
        "game_path_label": "📂 Nhập đường dẫn file Game (.exe hoặc .pck):",
        "game_path_ph": "Ví dụ: C:\\Games\\MyGame.exe",
        "target_lang_label": "🌐 Ngôn ngữ đích:",
        "ai_model_label": "🤖 AI Model:",
        "adv_options": "🔑 Tùy chọn nâng cao (Cho người dùng Pro)",
        "api_key_label": "Gemini API Key:",
        "api_key_help": "Nhập API Key Google AI Studio. Nếu để trống sẽ dùng hệ thống mặc định.",
        "api_key_cap": "Lấy API Key miễn phí tại: https://aistudio.google.com/app/apikey",
        "debug_mode_label": "🛠️ Chế độ Debug (Giữ lại file tạm để kiểm tra)",
        "debug_mode_help": "Khi bật, hệ thống sẽ KHÔNG xóa thư mục xả nén sau khi đóng gói, giúp bạn kiểm tra file .scn.",
        "enc_key_label": "Mã giải mã (Encryption Key - 64 ký tự Hex):",
        "enc_key_help": "Chỉ nhập khi game bị mã hóa (DRM). Lấy key bằng CheatEngine/x64dbg.",
        "btn_start": "🚀 BẮT ĐẦU MAGIC 1-CLICK",
        "err_no_file": "❌ Không tìm thấy file Game! Vui lòng kiểm tra lại đường dẫn.",
        "step2_title": "### Bước 2: AI Đang Làm Phép 🪄",
        "err_system": "❌ Lỗi hệ thống: {}",
        "btn_back": "⬅️ Quay lại",
        "step3_title": "### Bước 3: Nghiệm Thu",
        "step3_success": "🎉 Game đã dịch xong! Hãy nghiệm thu trong Sandbox an toàn.",
        "step3_info": "Bấm Chơi Thử để test. Nếu OK, bấm Đóng Gói (Repack).",
        "btn_test": "▶️ CHƠI THỬ (TEST GAME)",
        "toast_test": "Đang khởi chạy Sandbox Game...",
        "info_test": "Game đang chạy ở cửa sổ riêng. Khi test xong có thể đóng game và bấm Repack.",
        "btn_repack": "📦 XÁC NHẬN ĐÓNG GÓI",
        "spin_repack": "Đang đóng gói file Game mới...",
        "btn_reset": "⬅️ Làm lại từ đầu (Hủy & Xóa Temp)",
        "step4_success": "🎊 HOÀN TẤT! Game đã được lưu tại:\n\n`{}`",
        "step4_wish": "Chúc bạn chơi game vui vẻ!",
        "btn_home": "⬅️ Về Màn hình chính",
        "status_unpack": "📦 Đang xả nén file Game (Unpacking)...",
        "status_scan": "🔍 Đang quét cấu trúc hội thoại...",
        "status_trans": "🤖 Đang dịch sang {}...",
        "status_trans_file": "🤖 Đang dịch file {}/{}...",
        "status_inject": "✨ Hoàn tất tiêm mã (Injection)...",
        "drm_warning": "⛔ **BẢO VỆ BẢN QUYỀN (DRM DETECTED):** \nTựa game này đã được nhà phát triển mã hóa để chống can thiệp dữ liệu. Chúng tôi tôn trọng quyền sở hữu trí tuệ của tác giả. Nếu bạn là chủ sở hữu hoặc có mã giải mã (Encryption Key) hợp lệ, vui lòng mở mục **🔑 Tùy chọn nâng cao** ở Bước 1 để nhập mã và tiếp tục."
    },
    "en": {
        "title": "🎮 GODOT GAME TRANSLATOR 1-CLICK",
        "caption": "B2C Commercial Edition | Auto Unpack -> Translate -> Test -> Repack.",
        "step1_title": "### Step 1: Select Game & Config",
        "game_path_label": "📂 Enter Game file path (.exe or .pck):",
        "game_path_ph": "Example: C:\\Games\\MyGame.exe",
        "target_lang_label": "🌐 Target Language:",
        "ai_model_label": "🤖 AI Model:",
        "adv_options": "🔑 Advanced Options (For Pro Users)",
        "api_key_label": "Gemini API Key:",
        "api_key_help": "Enter Google AI Studio API Key. Leave blank to use default system key.",
        "api_key_cap": "Get free API Key at: https://aistudio.google.com/app/apikey",
        "debug_mode_label": "🛠️ Debug Mode (Keep temp files for inspection)",
        "debug_mode_help": "If enabled, the system will NOT delete the extracted directory after repacking, allowing you to inspect .scn files.",
        "enc_key_label": "Decryption Key (64 Hex chars):",
        "enc_key_help": "Only enter if game is DRM-encrypted. Find it using CheatEngine/x64dbg.",
        "btn_start": "🚀 START 1-CLICK MAGIC",
        "err_no_file": "❌ Game file not found! Please check the path.",
        "step2_title": "### Step 2: AI is working its magic 🪄",
        "err_system": "❌ System Error: {}",
        "btn_back": "⬅️ Go Back",
        "step3_title": "### Step 3: Acceptance Test",
        "step3_success": "🎉 Translation complete! Please test it in the safe Sandbox.",
        "step3_info": "Click Playtest to verify. If everything is fine, click Repack.",
        "btn_test": "▶️ PLAYTEST",
        "toast_test": "Launching Sandbox Game...",
        "info_test": "Game is running in a separate window. Close it when done and click Repack.",
        "btn_repack": "📦 CONFIRM REPACK",
        "spin_repack": "Repacking new Game files...",
        "btn_reset": "⬅️ Start Over (Cancel & Clear Temp)",
        "step4_success": "🎊 DONE! The Translated Game is saved at:\n\n`{}`",
        "step4_wish": "Have fun playing the game!",
        "btn_home": "⬅️ Return to Home",
        "status_unpack": "📦 Unpacking Game files...",
        "status_scan": "🔍 Scanning dialogue structures...",
        "status_trans": "🤖 Translating to {}...",
        "status_trans_file": "🤖 Translating file {}/{}...",
        "status_inject": "✨ Code injection completed...",
        "drm_warning": "⛔ **DRM PROTECTION DETECTED:** \nThis game has been encrypted by the developer to prevent data tampering. We respect intellectual property rights. If you are the owner or have a valid Encryption Key, please open **🔑 Advanced Options** in Step 1 to enter the key and proceed."
    }
}

st.set_page_config(page_title="Godot Game Translator (1-Click B2C)", page_icon="🎮", layout="centered")

# --- QUẢN LÝ TRẠNG THÁI (STATE) ---
if 'step' not in st.session_state:
    st.session_state.step = 'SETUP'  # SETUP -> TRANSLATING -> TESTING -> REPACKED
if 'temp_extract_dir' not in st.session_state:
    st.session_state.temp_extract_dir = None
if 'game_exe_path' not in st.session_state:
    st.session_state.game_exe_path = None
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'status_text' not in st.session_state:
    st.session_state.status_text = "..."
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'error_msg' not in st.session_state:
    st.session_state.error_msg = None
if 'ui_lang' not in st.session_state:
    st.session_state.ui_lang = "vi"
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False
if 'cleanup_done' not in st.session_state:
    st.session_state.cleanup_done = False

# UI Header - Language Toggle
col_empty, col_lang = st.columns([4, 1])
with col_lang:
    ui_lang_sel = st.selectbox("Language / Ngôn ngữ", ["🇻🇳 Tiếng Việt", "🇬🇧 English"], index=0 if st.session_state.ui_lang == "vi" else 1)
    st.session_state.ui_lang = "vi" if "Tiếng Việt" in ui_lang_sel else "en"

t = LANG_DICT[st.session_state.ui_lang]

def translation_worker(exe_path, target_lang, ai_model, api_key, encryption_key="", lang_code="vi"):
    """Luồng dịch ngầm (Thread) để tránh block UI."""
    try:
        pm = PackManager()
        t_w = LANG_DICT[lang_code]
        
        # Phase 1: Unpack
        st.session_state.status_text = t_w["status_unpack"]
        st.session_state.progress = 10
        temp_dir = pm.unpack(exe_path, key=encryption_key)
        st.session_state.temp_extract_dir = temp_dir
        st.session_state.progress = 25
        
        # Phase 2: Quét file
        st.session_state.status_text = t_w["status_scan"]
        extractor = GodotExtractor(str(temp_dir))
        all_files = [p for p in temp_dir.rglob("*") if p.is_file() and p.suffix in [".gd", ".tscn", ".csv"]]
        total_files = len(all_files)
        st.session_state.progress = 40
        
        # Phase 3: Dịch thuật
        st.session_state.status_text = t_w["status_trans"].format(target_lang)
        if total_files > 0:
            translator = GodotTranslator(model_name=ai_model, api_key=api_key)
            injector = GodotInjector(target_root=temp_dir, output_dir=str(temp_dir))
            
            for i, fpath in enumerate(all_files):
                texts = extractor.extract_from_file(fpath)
                if texts:
                    translations = translator.translate_batch(texts)
                    injector.inject(fpath, translations)
                
                pct = 40 + int((i + 1) / total_files * 50)
                st.session_state.progress = pct
                st.session_state.status_text = t_w["status_trans_file"].format(i+1, total_files)
        else:
            st.session_state.progress = 90
            
        st.session_state.status_text = t_w["status_inject"]
        st.session_state.progress = 100
        time.sleep(1) # Chờ UI cập nhật
        
        st.session_state.is_running = False
        st.session_state.step = 'TESTING'
        
    except DRMError:
        st.session_state.error_msg = "DRM_DETECTED"
        st.session_state.is_running = False
    except Exception as e:
        st.session_state.error_msg = str(e)
        st.session_state.is_running = False

st.title(t["title"])
st.caption(t["caption"])

# --- BƯỚC 1: CẤU HÌNH VÀ CHỌN FILE ---
if st.session_state.step == 'SETUP':
    st.write(t["step1_title"])
    game_file_str = st.text_input(t["game_path_label"], placeholder=t["game_path_ph"])
    
    col1, col2 = st.columns(2)
    with col1:
        target_lang = st.selectbox(t["target_lang_label"], ["Tiếng Việt", "English", "中文", "日本語"])
    with col2:
        ai_model = st.selectbox(t["ai_model_label"], ["gemini-3.1-flash-lite", "gemini-2.5-flash", "gemini-3.1-pro-preview"])
    
    with st.expander(t["adv_options"]):
        user_api_key = st.text_input(t["api_key_label"], type="password", help=t["api_key_help"])
        st.caption(t["api_key_cap"])
        
        st.session_state.debug_mode = st.checkbox(t["debug_mode_label"], value=st.session_state.debug_mode, help=t["debug_mode_help"])
        
        encryption_key = st.text_input(t["enc_key_label"], help=t["enc_key_help"])
    
    st.divider()
    
    if st.button(t["btn_start"], type="primary", use_container_width=True):
        game_file_clean = game_file_str.strip().strip('"').strip("'")
        if not game_file_clean or not os.path.exists(game_file_clean):
            st.error(t["err_no_file"])
        else:
            st.session_state.game_exe_path = game_file_clean
            st.session_state.target_lang = target_lang
            st.session_state.ai_model = ai_model
            st.session_state.api_key = user_api_key
            st.session_state.encryption_key = encryption_key
            st.session_state.progress = 0
            st.session_state.error_msg = None
            st.session_state.is_running = True
            st.session_state.step = 'TRANSLATING'
            
            # Khởi tạo Thread an toàn cho Streamlit
            worker_t = threading.Thread(target=translation_worker, args=(
                game_file_clean, target_lang, ai_model, user_api_key, encryption_key, st.session_state.ui_lang
            ))
            add_script_run_ctx(worker_t)
            worker_t.start()
            
            # Đợi 0.5s để Thread kịp update state khởi tạo trước khi rerun
            time.sleep(0.5)
            st.rerun()

# --- BƯỚC 2: TIẾN TRÌNH AUTO PIPELINE (OBSERVER) ---
elif st.session_state.step == 'TRANSLATING':
    st.write(t["step2_title"])
    
    if st.session_state.error_msg:
        if st.session_state.error_msg == "DRM_DETECTED":
            st.warning(t["drm_warning"])
        else:
            st.error(t["err_system"].format(st.session_state.error_msg))
            
        if st.button(t["btn_back"]):
            PackManager().cleanup_temp()
            st.session_state.step = 'SETUP'
            st.rerun()
    else:
        st.progress(st.session_state.progress)
        st.info(st.session_state.status_text)
        
        if st.session_state.is_running:
            time.sleep(1.5) # Polling interval an toàn
            st.rerun()
        else:
            # Ngay khi thread xong, nó tự đổi step -> TESTING, ta chỉ cần rerun
            time.sleep(0.5)
            st.rerun()

# --- BƯỚC 3: NGHIỆM THU & REPACK ---
elif st.session_state.step == 'TESTING':
    st.success(t["step3_success"])
    
    st.write(t["step3_title"])
    st.info(t["step3_info"])
    
    pm = PackManager()
    
    col_play, col_pack = st.columns(2)
    
    with col_play:
        if st.button(t["btn_test"], use_container_width=True):
            st.toast(t["toast_test"])
            pm.test_run(st.session_state.game_exe_path, st.session_state.temp_extract_dir)
            st.info(t["info_test"])
            
    with col_pack:
        if st.button(t["btn_repack"], type="primary", use_container_width=True):
            status_container = st.empty()
            def repack_cb(msg):
                status_container.info(msg)
                
            with st.spinner(t["spin_repack"]):
                out_path = pm.repack(
                    st.session_state.game_exe_path, 
                    st.session_state.temp_extract_dir, 
                    key=st.session_state.get('encryption_key', ''),
                    progress_callback=repack_cb
                )
                if not st.session_state.debug_mode:
                    pm.cleanup_temp() # Chỉ dọn dẹp nếu không ở chế độ Debug
                else:
                    st.success("✅ Đã giữ lại file tạm cho Dev tại: " + str(st.session_state.temp_extract_dir))
            st.session_state.out_path = out_path
            st.session_state.step = 'DONE'
            st.rerun()
            
    st.divider()
    col_reset, col_cleanup = st.columns(2)
    with col_reset:
        if st.button(t["btn_reset"], use_container_width=True):
            pm.cleanup_temp()
            st.session_state.step = 'SETUP'
            st.rerun()
    with col_cleanup:
        if st.session_state.debug_mode:
            if st.button("🗑️ DỌN DẸP THỦ CÔNG", use_container_width=True):
                pm.cleanup_temp()
                st.session_state.cleanup_done = True
                st.toast("Đã dọn dẹp file tạm!")
                st.rerun()

    if st.session_state.cleanup_done:
        st.success("✅ Đã dọn dẹp sạch sẽ thư mục tạm.")
        st.session_state.cleanup_done = False

# --- BƯỚC 4: HOÀN THÀNH ---
elif st.session_state.step == 'DONE':
    st.balloons()
    st.success(t["step4_success"].format(st.session_state.out_path))
    st.write(t["step4_wish"])
    
    if st.button(t["btn_home"], type="primary"):
        st.session_state.clear()
        st.rerun()
