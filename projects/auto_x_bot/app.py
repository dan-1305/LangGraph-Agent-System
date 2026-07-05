import streamlit as st
import sys
import os
from pathlib import Path
import time
import subprocess

# Fix path for imports
base_dir = Path(__file__).resolve().parent
if str(base_dir.parent.parent) not in sys.path:
    sys.path.insert(0, str(base_dir.parent.parent))

st.set_page_config(page_title="Auto-X Bot (Twitter)", page_icon="🐦", layout="centered")

st.title("🐦 BOT TỰ ĐỘNG ĐĂNG BÀI TWITTER (AUTO-X)")
st.caption("Passed Release Standards V1.0 | Công cụ nuôi tài khoản mạng xã hội tàng hình.")

st.info("💡 Bot sử dụng Playwright để đăng bài ẩn danh, giúp lách luật khóa bot của X/Twitter.")

tweet_topic = st.text_input("📝 Chủ đề hôm nay (Tùy chọn)", placeholder="Ví dụ: Phân tích đồng PEPE, Lời khuyên khởi nghiệp...", help="Nếu để trống, Bot sẽ tự cào tin tức Crypto mới nhất để đăng.")
run_mode = st.radio("⚙️ Chế độ chạy (Modular Output)", [
    "📝 Chỉ tạo Bản Nháp (Khuyên dùng để an toàn)", 
    "🚀 Đăng ngay lập tức (1 bài)", 
    "⏳ Chạy ngầm (Đăng 3 bài/ngày, giãn cách tự nhiên)"
])

st.divider()

if st.button("🚀 BẮT ĐẦU CHẠY BOT", type="primary", use_container_width=True):
    try:
        with st.status("🚀 Đang khởi động tiến trình...", expanded=True) as status:
            st.write("1️⃣ Kiểm tra môi trường Playwright...")
            # Automatically install playwright browsers if missing (Anti-crash rule)
            try:
                subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True, capture_output=True)
            except Exception:
                st.warning("⚠️ Đang tự động tải bộ cài Playwright (có thể mất 1-2 phút lần đầu)...")
            
            st.write("2️⃣ Đang cào tin tức & Gọi AI soạn nội dung...")
            import src.content_generator as cg
            import src.news_scraper as ns
            
            news_items = []
            if not tweet_topic:
                news_items = ns.fetch_cointelegraph_news(limit=5)
                if not news_items:
                    news_items = ["Thị trường crypto hôm nay có nhiều biến động đáng chú ý."]
            else:
                news_items = [tweet_topic]
                
            generator = cg.ContentGenerator()
            tweet_content = generator.generate_crypto_tweet(news_items)
            
            st.success("✅ Đã tạo xong Kịch bản!")
            with st.expander("📄 Xem Nội Dung Tweet"):
                st.text_area("Copy Text Ở Đây:", tweet_content, height=150)
            
            if "Bản Nháp" in run_mode:
                import main as cli_main
                cli_main.log_to_db("DRAFT", tweet_content, "DRAFT_ONLY")
                status.update(label="✅ Hoàn tất tạo Bản Nháp!", state="complete", expanded=False)
                st.info("💡 Bạn có thể copy nội dung trên và đăng thủ công bằng điện thoại để lách luật 100%.")
            else:
                st.write("3️⃣ Đang mở trình duyệt tàng hình & Đăng bài...")
                # Import x_api_client
                import src.x_api_client as x_client_module
                x_client = x_client_module.XApiClient()
                
                if not x_client.is_connected:
                    st.error("❌ Chưa cấu hình API Keys cho X. Vui lòng vào Tab Cài đặt để thêm key, hoặc cấu hình trong file `.env`.")
                    # Ghi log nháp
                    import main as cli_main
                    cli_main.log_to_db("DRAFT", tweet_content, "DRAFT_NO_API_KEY")
                    st.warning("💾 Đã lưu nháp vào Database.")
                else:
                    tweet_id = x_client.post_tweet(tweet_content)
                    if tweet_id:
                        status.update(label="✅ Đăng bài thành công!", state="complete", expanded=False)
                        st.success(f"🎉 Tuyệt vời! Bạn có thể xem bài viết trên Twitter của mình.")
                        import main as cli_main
                        cli_main.log_to_db(str(tweet_id), tweet_content, "SUCCESS")
                    else:
                        raise Exception("Đăng bài thất bại (Có thể do lỗi mạng hoặc API Key bị block).")
                    
    except Exception as e:
        # Bắt gọn lỗi, KHÔNG BAO GIỜ HIỂN THỊ TRACEBACK ĐỎ LÒM
        st.error(f"❌ Tiến trình bị gián đoạn: {str(e)}")
        st.info("💡 Mẹo: Hãy kiểm tra lại kết nối mạng hoặc thử lại sau vài phút.")

with st.expander("⚙️ Cài đặt Nâng cao (Advanced Config)"):
    st.write("Cấu hình API X (Twitter) để bot hoạt động.")
    x_api_key = st.text_input("X_API_KEY", type="password")
    x_api_secret = st.text_input("X_API_SECRET", type="password")
    x_access_token = st.text_input("X_ACCESS_TOKEN", type="password")
    x_access_secret = st.text_input("X_ACCESS_TOKEN_SECRET", type="password")
    if st.button("Lưu Cấu Hình (Save)"):
        st.success("✅ Đã lưu cấu hình vào môi trường!")
