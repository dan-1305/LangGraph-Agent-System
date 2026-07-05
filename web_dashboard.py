import streamlit as st
import os
import sys
import io
import subprocess
import json
import uuid

# Ép kiểu UTF-8 cho stdout để tránh lỗi Unicode khi render Emojis trên Windows CMD
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from pathlib import Path
from datetime import datetime

# --- 1. CONFIG & SYSTEM ---
st.set_page_config(page_title="Master AI Dashboard", page_icon="🚀", layout="wide")

PROCESS_DB = Path("logs/running_processes.json")

def load_processes():
    if PROCESS_DB.exists():
        try:
            with open(PROCESS_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {}

def save_processes(procs):
    PROCESS_DB.parent.mkdir(exist_ok=True)
    # Dùng Temp File & Atomic Replace để chống Race Condition khi click liên tục
    tmp_path = PROCESS_DB.with_name(f"{PROCESS_DB.name}.{uuid.uuid4().hex[:8]}.tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(procs, f)
        os.replace(tmp_path, PROCESS_DB)
    except Exception:
        if tmp_path.exists():
            os.remove(tmp_path)

def is_process_running(pid):
    if os.name == 'nt':
        try:
            output = subprocess.check_output(f'tasklist /FI "PID eq {pid}" /NH', shell=True).decode(errors='ignore')
            return str(pid) in output
        except: return False
    else:
        try:
            import signal
            os.kill(pid, 0)
            return True
        except OSError: return False

def stop_process(script_path):
    procs = load_processes()
    if script_path in procs:
        pid = procs[script_path]
        if is_process_running(pid):
            try:
                if os.name == 'nt':
                    subprocess.run(f'taskkill /F /T /PID {pid}', shell=True, check=True)
                else:
                    import signal
                    os.kill(pid, signal.SIGTERM)
                st.toast(f"Đã tiêu diệt tiến trình: {script_path}", icon="🛑")
            except Exception as e:
                st.error(f"Lỗi khi dừng tác vụ: {e}")
        else:
            st.toast("Tiến trình đã kết thúc.", icon="ℹ️")
        del procs[script_path]
        save_processes(procs)
        st.rerun()

def run_script_bg(script_path):
    procs = load_processes()
    if script_path in procs:
        if is_process_running(procs[script_path]):
            st.warning("⚠️ Tác vụ này đang chạy! Vui lòng không bấm liên tục.")
            return
        else:
            del procs[script_path]
            
    full_path = os.path.join(os.getcwd(), script_path)
    
    # Bug Fix 1: Ghost Launch - Kiểm tra file có tồn tại không trước khi gọi OS
    if not os.path.exists(full_path):
        st.error(f"❌ Lỗi: File không tồn tại tại `{full_path}`. Vui lòng kiểm tra lại hệ thống!")
        return
        
    working_dir = os.path.dirname(full_path)
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"
    
    # Tính năng: Ghi log
    log_dir = os.path.join(os.getcwd(), "logs", "task_logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, f"{os.path.basename(script_path)}.log")
    log_file = open(log_file_path, "w", encoding="utf-8")
    
    try:
        if os.name == 'nt':
            p = subprocess.Popen([sys.executable, full_path], env=env, cwd=working_dir, stdout=log_file, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            p = subprocess.Popen([sys.executable, full_path], env=env, cwd=working_dir, stdout=log_file, stderr=subprocess.STDOUT)
        procs[script_path] = p.pid
        save_processes(procs)
        st.success(f"✅ Đã khởi chạy thành công (PID: {p.pid})")
    except Exception as e:
        st.error(f"Không thể khởi chạy: {e}")

def ensure_local_proxy_running():
    import urllib.request
    try:
        urllib.request.urlopen("http://localhost:8001/", timeout=1)
        return True
    except:
        script_path = "projects/local_proxy_server/main.py"
        full_path = os.path.join(os.getcwd(), script_path)
        if os.path.exists(full_path):
            env = os.environ.copy()
            working_dir = os.path.dirname(full_path)
            if os.name == 'nt':
                subprocess.Popen([sys.executable, full_path], env=env, cwd=working_dir, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen([sys.executable, full_path], env=env, cwd=working_dir)
        return False

ensure_local_proxy_running()

def load_json_safe(filepath):
    p = Path(filepath)
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {}

# --- 2. DATA (Danh sách 15+ Dự án) ---
FEATURES = [
    # 💰 Đầu Tư & Kiếm Tiền
    {"name": "AI Trading Live Advisor", "desc": "Phân bổ vốn & ra lệnh giao dịch tự động.", "script": "projects/ai_trading_agent/live_advisor.py", "cat": "💰 Đầu Tư & Kiếm Tiền", "keys": "trade crypto chứng khoán bot giao dịch"},
    {"name": "Cập nhật Dữ liệu Thị trường", "desc": "Cào giá, tin tức và on-chain.", "script": "projects/ai_trading_agent/src/data_fetcher.py", "cat": "💰 Đầu Tư & Kiếm Tiền", "keys": "cào data fetch crawl giá crypto"},
    {"name": "Chạy Backtest Mô phỏng", "desc": "Kiểm tra chiến lược bằng dữ liệu quá khứ.", "script": "projects/ai_trading_agent/backtest/offline_backtest.py", "cat": "💰 Đầu Tư & Kiếm Tiền", "keys": "backtest test chiến lược"},
    {"name": "Airdrop Guerrilla (Full Auto)", "desc": "Tự động cày Airdrop toàn diện (Zealy, X, Discord...).", "script": "projects/airdrop_guerrilla/src/modes/full_auto_cli.py", "cat": "💰 Đầu Tư & Kiếm Tiền", "keys": "airdrop bot auto zealy twitter discord free money tiền"},
    # 🎨 Sáng Tạo & Content
    {"name": "Auto-X Bot (Tạo & Đăng Tweet)", "desc": "Đọc tin tức và tự động viết Tweet câu view.", "script": "projects/auto_x_bot/main.py", "cat": "🎨 Sáng Tạo & Content", "keys": "twitter x bot tweet auto content mmo"},
    {"name": "Tạo Video TikTok Affiliate", "desc": "Tự động render video bán hàng/review.", "script": "projects/auto_affiliate_video/main.py", "cat": "🎨 Sáng Tạo & Content", "keys": "video tiktok affiliate mmo youtube shorts"},
    {"name": "Dịch Game (Godot Translator)", "desc": "Bản địa hóa game tự động.", "script": "projects/godot_translator/main.py", "cat": "🎨 Sáng Tạo & Content", "keys": "dịch game translate godot việt hóa"},
    {"name": "Web Tạo World Card (SillyTavern)", "desc": "Tạo thẻ nhân vật/truyện chuẩn SillyTavern.", "script": "projects/sillytavern_world_card_generator/ui/app.py", "cat": "🎨 Sáng Tạo & Content", "keys": "truyện card rp roleplay sillytavern"},
    {"name": "Trích xuất & Chuyển đổi Chat", "desc": "Lọc text truyện/chat.", "script": "projects/ExtractDoanChat/GiaoDien_ChuyenDoi_Truyen.py", "cat": "🎨 Sáng Tạo & Content", "keys": "truyện text chat extract"},
    # 🛠️ Tối Ưu & Trợ Lý AI
    {"name": "Vắt Kiệt API (Drip-Feeder)", "desc": "Chạy ngầm gọi AI từ từ, tiết kiệm API.", "script": "scheduler/drip_feed_worker.py", "cat": "🛠️ Tối Ưu & Trợ Lý AI", "keys": "api free tier drip feeder tối ưu"},
    {"name": "Nạp Sách (Ingest PDF -> RAG)", "desc": "Nhúng tài liệu vào não AI.", "script": "projects/knowledge_base_agent/src/ingest.py", "cat": "🛠️ Tối Ưu & Trợ Lý AI", "keys": "sách pdf tài liệu nạp rag vector"},
    {"name": "Hỏi đáp với Sách (RAG Agent)", "desc": "Trò chuyện với kho tài liệu.", "script": "projects/knowledge_base_agent/src/rag_agent.py", "cat": "🛠️ Tối Ưu & Trợ Lý AI", "keys": "chat hỏi đáp sách tài liệu"},
    {"name": "Trợ lý Jarvis RPG", "desc": "Hệ thống quản trị bằng RPG cá nhân.", "script": "projects/jarvis-rpg-assistant/main.py", "cat": "🛠️ Tối Ưu & Trợ Lý AI", "keys": "jarvis trợ lý rpg quản lý"},
    # ⚙️ Quản Trị Hệ Thống
    {"name": "Lập lịch Hệ thống (Main Scheduler)", "desc": "Hệ thống chạy hẹn giờ tự động.", "script": "scheduler/main_scheduler.py", "cat": "⚙️ Quản Trị Hệ Thống", "keys": "lịch cron schedule tự động"},
    {"name": "QA Chaos Agent (Săn Bug)", "desc": "Đặc vụ phá hoại tìm lỗi.", "script": "projects/qa_chaos_agent/src/fuzzer_engine.py", "cat": "⚙️ Quản Trị Hệ Thống", "keys": "bug lỗi test qa chaos fuzzer"},
    {"name": "Disk Cleaner (Dọn Rác)", "desc": "Dọn dẹp Temp, Cache, giải phóng ổ đĩa.", "script": "projects/disk_cleaner/run_cleaner.py", "cat": "⚙️ Quản Trị Hệ Thống", "keys": "disk cleaner dọn rác ổ c cache temp"},
    {"name": "Deep Scanner (Quét File Lớn)", "desc": "Tìm file nặng và xóa archive cũ.", "script": "projects/disk_cleaner/deep_scanner.py", "cat": "⚙️ Quản Trị Hệ Thống", "keys": "deep scan quét file nặng dung lượng"}
]

# --- 3. UI RENDERING ---
st.title("🚀 MASTER DASHBOARD V5.0 - INTENT DRIVEN")

# ONBOARDING GUIDE
if 'skip_guide' not in st.session_state:
    st.session_state['skip_guide'] = False

if not st.session_state['skip_guide']:
    st.info("""
    👋 **Chào mừng sếp đến với Trạm Kiểm Soát Không Gian LangGraph!**
    - Hệ thống được chia theo **Mục đích sử dụng** (Kiếm tiền, Sáng tạo, Trợ lý...).
    - Dùng thanh **Tìm kiếm 🔍** để tìm ngay tính năng đang cần.
    - Không bấm nút **Chạy 🚀** nhiều lần cho cùng 1 tác vụ. Bấm **Dừng 🛑** để dọn dẹp tiến trình khi xong việc.
    """)
    if st.button("⏭️ Đã hiểu (Bỏ qua hướng dẫn này)"):
        st.session_state['skip_guide'] = True
        st.rerun()

# LIVE METRICS
st.header("📊 Trạng thái Hệ thống")
colM1, colM2, colM3, colM4 = st.columns(4)

import urllib.request
try:
    urllib.request.urlopen("http://localhost:8001/", timeout=1)
    proxy_status = "🟢 Chạy ổn định"
except: proxy_status = "🟡 Đang khởi động"

drip_stats = load_json_safe("logs/drip_feed_stats.json")
colM1.metric("Lá chắn API (Local Proxy)", proxy_status, "Hỗ trợ Free Tier")
colM2.metric("API Drip-Feeder", f"{drip_stats.get('total_requests', 0)} Requests", "Tiết kiệm")
colM3.metric("Bảo vệ Bộ nhớ (RAM)", "Hoạt động", "Anti-Spam Bật")

# Tích hợp Dashboard PnL từ AI Trading (XGBoost/Não Trái)
ai_pnl_status = "N/A"
roi_text = "0.00%"
import sqlite3
import pandas as pd
db_path = Path("data/system_logs.db")
if db_path.exists():
    try:
        conn = sqlite3.connect(db_path, timeout=5.0)
        df_port = pd.read_sql("SELECT * FROM Paper_Trade_Portfolio ORDER BY id", conn)
        conn.close()
        if not df_port.empty:
            initial = df_port['total_usdt_value'].iloc[0]
            current = df_port['total_usdt_value'].iloc[-1]
            roi = (current - initial) / initial * 100 if initial > 0 else 0
            ai_pnl_status = f"${current:,.2f}"
            roi_text = f"{roi:+.2f}%"
    except Exception:
        pass
colM4.metric("AI Trading PnL (XGBoost)", ai_pnl_status, roi_text)

st.divider()

# GLOBAL SEARCH BAR
search_query = st.text_input("🔍 Tìm kiếm chức năng sếp cần (VD: dịch, trade, airdrop, video)...", "")

# Nút cập nhật trạng thái
if st.button("🔄 Cập nhật trạng thái", use_container_width=True):
    st.rerun()

procs_state = load_processes()

@st.dialog("Nội dung Log", width="large")
def show_log(script_path):
    log_file_path = os.path.join(os.getcwd(), "logs", "task_logs", f"{os.path.basename(script_path)}.log")
    if os.path.exists(log_file_path):
        try:
            with open(log_file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if content:
                st.code(content[-10000:], language="text") # Hiện tối đa 10k ký tự cuối
            else:
                st.info("File log đang trống. Tiến trình có thể chưa in ra dữ liệu nào.")
        except Exception as e:
            st.error(f"Lỗi khi đọc file log: {e}")
    else:
        st.warning("Chưa có log cho tiến trình này (Bạn cần bấm Chạy ít nhất 1 lần).")

def render_task_row(task, procs, key_suffix=""):
    c1, c2, c3, c4 = st.columns([5, 2, 2, 2])
    
    # Kiểm tra trạng thái
    pid = procs.get(task['script'])
    is_running = False
    if pid and is_process_running(pid):
        is_running = True
        
    status_badge = "🟢 Đang chạy" if is_running else "⚪ Đã dừng"
    
    with c1:
        st.write(f"**{task['name']}** - *{task['desc']}* - `{status_badge}`")
    with c2:
        if st.button("🚀 Chạy", key=f"run_{task['script']}_{key_suffix}", use_container_width=True):
            run_script_bg(task['script'])
    with c3:
        if st.button("🛑 Dừng", key=f"stop_{task['script']}_{key_suffix}", use_container_width=True):
            stop_process(task['script'])
    with c4:
        if st.button("📜 Xem Log", key=f"log_{task['script']}_{key_suffix}", use_container_width=True):
            show_log(task['script'])

if search_query:
    st.subheader(f"Kết quả tìm kiếm cho: '{search_query}'")
    query_lower = search_query.lower()
    found = False
    for task in FEATURES:
        if query_lower in task['name'].lower() or query_lower in task['desc'].lower() or query_lower in task['keys']:
            render_task_row(task, procs_state, "search")
            found = True
    if not found:
        st.warning("Không tìm thấy chức năng nào phù hợp. Sếp thử từ khóa khác nhé!")
else:
    st.subheader("🌟 Top Bật Nhiều Nhất (Quick Access)")
    quick_access_scripts = [
        "scheduler/drip_feed_worker.py",
        "scheduler/main_scheduler.py",
        "projects/ai_trading_agent/live_advisor.py",
        "projects/airdrop_guerrilla/src/modes/full_auto_cli.py"
    ]
    for task in FEATURES:
        if task['script'] in quick_access_scripts:
            render_task_row(task, procs_state, "quick")
    st.markdown("---")

    # INTENT-DRIVEN TABS
    cats = ["💰 Đầu Tư & Kiếm Tiền", "🎨 Sáng Tạo & Content", "🛠️ Tối Ưu & Trợ Lý AI", "⚙️ Quản Trị Hệ Thống", "⚙️ Infrastructure Config"]
    tabs = st.tabs(cats)
    
    for i, cat in enumerate(cats):
        with tabs[i]:
            if cat == "⚙️ Infrastructure Config":
                st.subheader("⚙️ Cấu Hình Hạ Tầng (Infrastructure Config)")
                st.markdown("Dán API Key (Gemini) và địa chỉ Ví Phụ USDT tại đây để hệ thống Local Proxy hoạt động.")
                
                env_path = ".env"
                env_content = ""
                if os.path.exists(env_path):
                    with open(env_path, "r", encoding="utf-8") as f:
                        env_content = f.read()
                        
                import re
                def extract_env(key):
                    match = re.search(fr"^{key}=(.*)$", env_content, re.MULTILINE)
                    if match:
                        val = match.group(1).strip()
                        if val.startswith('"') and val.endswith('"'): return val[1:-1]
                        if val.startswith("'") and val.endswith("'"): return val[1:-1]
                        return val
                    return ""

                api_keys = extract_env("GEMINI_API_KEYS")
                crypto_addr = extract_env("CRYPTO_PAYMENT_ADDRESS")
                
                new_api_keys = st.text_input("🔑 GEMINI_API_KEYS (Cách nhau bằng dấu phẩy)", value=api_keys, help="Dán 3 key Gemini Free Tier vào đây.")
                new_crypto_addr = st.text_input("💰 Địa chỉ Ví Phụ USDT (TRC-20/BSC)", value=crypto_addr, help="Ví phụ dùng để nhận tiền của khách.")
                
                if st.button("💾 Lưu Cấu Hình", use_container_width=True):
                    def set_env(key, val, content):
                        if re.search(fr"^{key}=.*$", content, re.MULTILINE):
                            return re.sub(fr"^{key}=.*$", f'{key}="{val}"', content, flags=re.MULTILINE)
                        else:
                            return content + f'\n{key}="{val}"\n'
                            
                    env_content = set_env("GEMINI_API_KEYS", new_api_keys, env_content)
                    env_content = set_env("CRYPTO_PAYMENT_ADDRESS", new_crypto_addr, env_content)
                    
                    with open(env_path, "w", encoding="utf-8") as f:
                        f.write(env_content)
                    st.success("✅ Đã lưu cấu hình thành công! Bạn nên khởi động lại proxy để nhận key mới.")
            else:
                for task in FEATURES:
                    if task['cat'] == cat:
                        render_task_row(task, procs_state, "tab")
                        st.markdown("---")
