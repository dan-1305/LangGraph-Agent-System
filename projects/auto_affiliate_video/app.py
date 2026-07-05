from core_utilities.http_client import HTTPClient
import streamlit as st
import os
import sys
from pathlib import Path
import time
import asyncio

# Fix path for imports
base_dir = Path(__file__).resolve().parent
if str(base_dir.parent.parent) not in sys.path:
    sys.path.insert(0, str(base_dir.parent.parent))

from projects.auto_affiliate_video.src.script_generator import ScriptGenerator
from projects.auto_affiliate_video.src.tts_engine import TTSEngine
from projects.auto_affiliate_video.src.video_editor import VideoEditor

st.set_page_config(page_title="Auto Affiliate Video (Hero Product)", page_icon="🎥", layout="centered")

st.title("🎥 MÁY SẢN XUẤT VIDEO TIKTOK (1-CLICK)")
st.caption("Passed Release Standards V1.0 | Công cụ render video lồng tiếng AI bán tự động.")

# Tiêu chuẩn Tối giản UI: Chỉ có Input thiết yếu nhất
col_input1, col_input2 = st.columns([3, 1])

with col_input1:
    product_name = st.text_input(
        "📦 Nhập Tên Sản Phẩm / Chủ đề (VD: Robot Hút Bụi, Tin tức chấn động...)", 
        value=st.session_state.get("trend_title", ""),
        placeholder="Tên sản phẩm hoặc chủ đề..."
    )
with col_input2:
    st.write("") # Dóng hàng button
    st.write("")
    if st.button("🔥 Cào Trend Youtube"):
        import json
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("YOUTUBE_API_KEY") or os.getenv("YT_API_KEY")
        if not api_key:
            st.error("❌ Lỗi: Thiếu YOUTUBE_API_KEY trong .env")
        else:
            with st.spinner("Đang tìm Trend Youtube..."):
                url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=VN&maxResults=1&key={api_key}"
                try:
                    req = urllib.request.Request(url)
                    with urllib.request.urlopen(req, timeout=10) as response:
                        data = json.loads(response.read().decode('utf-8'))
                        items = data.get("items", [])
                        if items:
                            video = items[0]
                            snippet = video.get("snippet", {})
                            st.session_state["trend_title"] = snippet.get("title", "")
                            st.session_state["trend_features"] = f"Kênh: {snippet.get('channelTitle', '')}, {video.get('statistics', {}).get('viewCount', 0)} views"
                            st.rerun()
                        else:
                            st.warning("Không lấy được dữ liệu Trend.")
                except Exception as e:
                    st.error(f"Lỗi API: {str(e)}")

key_features = st.text_input(
    "✨ Tính năng nổi bật / Ngữ cảnh (Cách nhau dấu phẩy)", 
    value=st.session_state.get("trend_features", ""),
    placeholder="Pin trâu, siêu sạch, giá rẻ..."
)

bg_dir = base_dir / "data" / "background_videos"
bg_dir.mkdir(parents=True, exist_ok=True)
available_bgs = [f.name for f in bg_dir.glob("*.mp4")]

if not available_bgs:
    st.warning("⚠️ Chưa có video nền. Vui lòng bỏ file .mp4 vào thư mục `data/background_videos/`.")
else:
    bg_video = st.selectbox("🎞️ Chọn Video Nền (Background)", options=available_bgs)

st.write("🎯 Tùy Chọn Đầu Ra (Đa Năng):")
col_opt1, col_opt2, col_opt3 = st.columns(3)
with col_opt1:
    gen_script = st.checkbox("📝 1. Chỉ tạo Kịch Bản", value=True, help="Sinh text kịch bản để bạn tự copy xài.")
with col_opt2:
    gen_audio = st.checkbox("🎙️ 2. Tạo File Thu Âm", value=True, help="Sinh file Audio MP3 giọng AI.")
with col_opt3:
    gen_video = st.checkbox("🎬 3. Ghép Video & Sub", value=True, help="Render thẳng ra file MP4.")

st.divider()

if st.button("🚀 BẮT ĐẦU TẠO", use_container_width=True, type="primary"):
    if not product_name:
        st.error("❌ Vui lòng nhập Tên Sản Phẩm!")
    elif gen_video and not available_bgs:
        st.error("❌ Thiếu file Video nền. Hãy nạp file MP4 trước nếu muốn render Video.")
    elif not gen_script and not gen_audio and not gen_video:
        st.warning("⚠️ Bạn phải chọn ít nhất 1 đầu ra (Kịch Bản / Thu Âm / Video) chứ!")
    else:
        try:
            with st.status("🚀 Đang khởi động tiến trình...", expanded=True) as status:
                output_dir = base_dir / "data" / "output"
                output_dir.mkdir(parents=True, exist_ok=True)
                
                # 1. Kịch bản
                script = ""
                if gen_script or gen_audio or gen_video:
                    st.write("1️⃣ Đang dùng AI (Gemini) để viết kịch bản...")
                    sg = ScriptGenerator()
                    script = sg.generate_short_video_script(product_name, key_features)
                    st.success("✅ Đã có Kịch bản!")
                    with st.expander("📄 Xem Kịch Bản"):
                        st.text_area("Copy Kịch Bản Tại Đây:", script, height=150)
                
                # 2. Audio
                audio_path = ""
                if gen_audio or gen_video:
                    st.write("2️⃣ Đang thu âm giọng đọc AI (Edge-TTS)...")
                    tts = TTSEngine()
                    audio_filename = f"{product_name.replace(' ', '_').lower()}_audio.mp3"
                    audio_path = str(output_dir / audio_filename)
                    audio_path = tts.generate_audio(script, audio_path)
                    
                    if not audio_path or not os.path.exists(audio_path):
                        raise Exception("Lỗi khi tạo Audio, không tìm thấy file!")
                    st.success("✅ Đã tạo Audio!")
                    st.audio(audio_path)
                    
                # 3. Video
                if gen_video:
                    st.write("3️⃣ Đang render Video & Phụ đề (Tiến trình này khá nặng, hãy kiên nhẫn)...")
                    bg_path = str(bg_dir / bg_video)
                    editor = VideoEditor()
                    output_video_name = f"tiktok_{int(time.time())}.mp4"
                    
                    success = editor.create_short_video(audio_path, bg_path, output_video_name)
                    
                    if success:
                        status.update(label="✅ Hoàn tất toàn bộ tiến trình!", state="complete", expanded=False)
                        video_file = output_dir / output_video_name
                        if video_file.exists():
                            st.success("🎉 TẠO VIDEO THÀNH CÔNG!")
                            st.video(str(video_file))
                            st.caption("Hãy tải video này lên TikTok và đính kèm link Affiliate của bạn.")
                    else:
                        raise Exception("Lỗi trong quá trình Render Video (MoviePy error).")
                else:
                    status.update(label="✅ Hoàn tất!", state="complete", expanded=False)
                    
        except Exception as e:
            # Bắt gọn lỗi, KHÔNG BAO GIỜ HIỂN THỊ TRACEBACK ĐỎ LÒM
            st.error(f"❌ Tiến trình bị gián đoạn: {str(e)}")
            st.info("💡 Mẹo: Hãy kiểm tra lại kết nối mạng hoặc thử đổi Video nền khác.")

with st.expander("⚙️ Cài đặt Nâng cao (Advanced Config)"):
    st.write("*(Bạn không cần chỉnh nếu không rành kỹ thuật)*")
    st.selectbox("Giọng đọc (Voice)", ["vi-VN-HoaiMyNeural (Nữ)", "vi-VN-NamMinhNeural (Nam)"])
    st.slider("Tốc độ đọc", -50, 50, 0, step=10)
    st.text_area("Prompt viết Kịch Bản (System Prompt)", "Viết 1 đoạn kịch bản ngắn dưới 60s để bán hàng trên Tiktok, nội dung giật gân, nhắm vào sự khan hiếm.")
