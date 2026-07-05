import streamlit as st
import os
import subprocess
from pathlib import Path
import glob

# Cấu hình trang cơ bản
st.set_page_config(
    page_title="JARVIS OBSERVABILITY DASHBOARD",
    page_icon="🤖",
    layout="wide"
)

# Thư mục chứa các script trigger
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# CSS Tuỳ chỉnh để giao diện "Lightweight" và rõ ràng hơn
st.markdown("""
<style>
    .reportview {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        color: #333;
    }
    .stButton button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 JARVIS OBSERVABILITY DASHBOARD")
st.markdown("*Kiểm soát vòng lặp, theo dõi Agent và đọc báo cáo hệ thống.*")

# Chia Layout
col_left, col_main = st.columns([1, 3])

with col_left:
    st.header("⚡ Triggers")
    st.markdown("Kích hoạt nhanh các luồng Agent.")
    
    # Custom Prompt System Override
    with st.container():
        st.markdown("### 🧠 GỌI PROMPT CHUNG")
        st.markdown("Truyền chỉ thị trực tiếp vào bộ não trung tâm (JARVIS).")
        custom_prompt = st.text_area("System Override Input:", height=100, placeholder="VD: Hãy quét lại file .env, sau đó kích hoạt AI Trading Agent.")
        if st.button("🚀 EXECUTE PROMPT", type="primary", use_container_width=True):
            if custom_prompt:
                st.success("Đang truyền lệnh vào Factory Core...")
                try:
                    subprocess.Popen(
                        ["uv", "run", "python", "src/factory/main.py", "--prompt", custom_prompt],
                        cwd=str(ROOT_DIR),
                        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
                    )
                except Exception as e:
                    st.error(f"Lỗi khởi chạy: {e}")
            else:
                st.warning("Vui lòng nhập lệnh.")

    st.markdown("---")
    st.subheader("📁 Module & Sub-Projects")

    # Dynamic Scanner: Quét thư mục projects/
    projects_dir = ROOT_DIR / "projects"
    if projects_dir.exists() and projects_dir.is_dir():
        valid_projects = [d for d in os.listdir(projects_dir) 
                         if os.path.isdir(projects_dir / d) 
                         and not d.startswith('.') 
                         and d not in ["__pycache__", "_template"]]
        
        if not valid_projects:
            st.info("Chưa tìm thấy Sub-Project nào.")
        else:
            for proj_name in sorted(valid_projects):
                display_name = proj_name.replace("_", " ").replace("-", " ").title()
                
                with st.expander(f"📦 {display_name}"):
                    st.caption(f"Trạng thái: Sẵn sàng | Path: `projects/{proj_name}`")
                    
                    # Schema-Driven UI Mapping (Mô phỏng đọc từ file config của mỗi project)
                    cmd_args = []
                    
                    # 1. AI TRADING AGENT
                    if proj_name == "ai_trading_agent":
                        t_symbol = st.selectbox("Cặp giao dịch (Symbol)", ["BTC/USDT", "ETH/USDT", "SOL/USDT"], key=f"sym_{proj_name}")
                        t_mode = st.radio("Môi trường", ["Paper Trading (Testnet)", "Live Trading (Real Money)"], key=f"mode_{proj_name}")
                        t_risk = st.slider("Mức chịu rủi ro (Risk %)", 1, 10, 2, key=f"risk_{proj_name}")
                        cmd_args = ["--symbol", t_symbol, "--mode", t_mode.split()[0].lower(), "--risk", str(t_risk)]
                        main_file_name = "main.py"
                    
                    # 2. AIRDROP GUERRILLA
                    elif proj_name == "airdrop_guerrilla":
                        a_network = st.selectbox("Mạng (Network)", ["Monad", "Soneium", "Inco"], key=f"net_{proj_name}")
                        # Bỏ nhập số lượng ví chạy đồng thời vì Airdrop thường chạy 1 profile/IP, hoặc có thể custom sau.
                        a_mode = st.selectbox("Chế độ chạy", ["Full Auto (CLI)", "Semi Auto (UI)"], key=f"mode_{proj_name}")
                        cmd_args = ["--network", a_network]
                        # Set đúng file chạy của Airdrop (không có file main.py ở thư mục gốc của nó)
                        if "Full" in a_mode:
                            main_file_name = "src/modes/full_auto_cli.py"
                        else:
                            main_file_name = "src/modes/semi_auto_ui.py"
                        
                    # 3. QA CHAOS AGENT
                    elif proj_name == "qa_chaos_agent":
                        q_target = st.selectbox("Mục tiêu tấn công (Target)", ["All", "Trading Module", "Telegram Bot", "Scheduler"], key=f"tar_{proj_name}")
                        q_intensity = st.select_slider("Cường độ Fuzzing", options=["Low", "Medium", "High", "Critical (May Crash)"], key=f"int_{proj_name}")
                        cmd_args = ["--target", q_target, "--intensity", q_intensity.split()[0].lower()]
                        main_file_name = "main.py"
                        
                    # FALLBACK: PROJECT CHƯA ĐƯỢC ĐỊNH NGHĨA SCHEMA
                    else:
                        st.info("Module này chưa có cấu hình UI Schema cụ thể. Sử dụng giao diện khởi chạy cơ bản.")
                        f_mode = st.selectbox("Chế độ", ["Default", "Debug", "Test"], key=f"fmode_{proj_name}")
                        f_args = st.text_input("Custom Arguments (ví dụ: --force --retry 3)", key=f"fargs_{proj_name}")
                        if f_args:
                            cmd_args = f_args.split()
                        else:
                            cmd_args = ["--mode", f_mode.lower()]
                        main_file_name = "main.py"
                    
                    # Nút bấm khởi chạy động
                    if st.button(f"▶ Bắt đầu: {display_name}", key=f"btn_{proj_name}"):
                        st.info(f"Đang chuẩn bị môi trường cho {display_name}...")
                        try:
                            main_file = projects_dir / proj_name / main_file_name
                            if main_file.exists():
                                cmd = ["uv", "run", "python", str(main_file)] + cmd_args
                                subprocess.Popen(
                                    cmd,
                                    cwd=str(ROOT_DIR),
                                    creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
                                )
                                st.success("✅ Đã mở tiến trình độc lập!")
                            else:
                                st.error(f"Lỗi: Không tìm thấy file `main.py` trong thư mục {proj_name}. Vui lòng tạo file chạy chính.")
                        except Exception as e:
                            st.error(f"Lỗi thực thi hệ thống: {e}")
    else:
        st.error("Lỗi kiến trúc: Mất kết nối tới thư mục `projects/` ở Root!")

with col_main:
    # Monitor Section
    st.header("🖥️ System Monitor (Live Log)")
    
    # Placeholder for live logs (would typically read from a log file or websocket)
    log_content = "Hệ thống đang rảnh (Idle). Chờ tín hiệu từ Scheduler hoặc User..."
    
    # Giả lập đọc log từ file nếu có
    log_file_path = ROOT_DIR / "logs" / "early_logs.txt"
    if log_file_path.exists():
        with open(log_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            log_content = "".join(lines[-10:]) if lines else log_content
            
    st.code(log_content, language="bash")
    
    st.markdown("---")
    
    # Artifact Viewer Section
    st.header("📄 Artifact Viewer (Tier 4 Reports)")
    st.markdown("Đọc nhanh các tệp báo cáo Markdown sinh ra trong quá trình chạy.")
    
    # Quét các file md trong thư mục reports và logs
    report_files = []
    
    reports_dir = ROOT_DIR / "reports"
    if reports_dir.exists():
        report_files.extend(glob.glob(f"{reports_dir}/*.md"))
        
    logs_dir = ROOT_DIR / "logs"
    if logs_dir.exists():
        report_files.extend(glob.glob(f"{logs_dir}/*.md"))
        
    if not report_files:
        st.info("Chưa có báo cáo nào được sinh ra.")
    else:
        # Tạo selectbox để chọn file đọc
        file_names = [os.path.basename(f) for f in report_files]
        selected_file_name = st.selectbox("Chọn báo cáo để đọc:", file_names)
        
        # Tìm path tương ứng
        selected_path = None
        for f in report_files:
            if os.path.basename(f) == selected_file_name:
                selected_path = f
                break
                
        if selected_path:
            with st.spinner("Đang tải nội dung..."):
                try:
                    with open(selected_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    st.markdown('<div class="reportview">', unsafe_allow_html=True)
                    st.markdown(content)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Không thể đọc file: {e}")
