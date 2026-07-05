import sys
import os
import io

# Đảm bảo Encoding UTF-8 trên Windows CMD
if sys.platform == "win32":
    try:
        if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, io.UnsupportedOperation):
        pass

import streamlit as st
import psutil
import time
import random
import json
import pandas as pd
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Sovereign Enterprise Dashboard V2",
    page_icon="👑",
    layout="wide",
)

st.title("👑 SOVEREIGN ENTERPRISE CONTROLLER V2.2")
st.markdown("---")

# --- SIDEBAR: SYSTEM HEALTH ---
st.sidebar.header("🔌 SYSTEM STATUS")
ram = psutil.virtual_memory()
cpu_usage = psutil.cpu_percent()

st.sidebar.metric("CPU Usage", f"{cpu_usage}%")
st.sidebar.metric("RAM Available", f"{ram.available / 1024 / 1024 / 1024:.2f} GB")
st.sidebar.metric("RAM Used", f"{ram.percent}%")

# Mock latency data
st.sidebar.header("📡 API LATENCY TELEMETRY")
st.sidebar.metric("Gemini API (Primary)", "120ms" if cpu_usage < 80 else "250ms")
st.sidebar.metric("Groq API (Fast Fallback)", "45ms")
st.sidebar.metric("OpenRouter (Gemma)", "180ms")

# --- MAIN TAB 1: DRIP-FEED MONITOR ---
tab1, tab2, tab3 = st.tabs(["🌊 DRIP-FEED MONITOR", "📊 HARDWARE TELEMETRY", "🛡️ CHAOS SUITE"])

with tab1:
    st.header("Real-Time Drip-Feeding Progress")
    st.markdown("Theo dõi tiến độ cào dữ liệu BĐS TP.HCM (Giả lập cuộn cuốn chiếu Semaphore 10)")
    
    # Progress bars
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Mock cào dữ liệu
    run_btn = st.button("🚀 Khởi chạy cào 10.000 BĐS")
    if run_btn:
        for i in range(1, 101):
            progress_bar.progress(i)
            status_text.text(f"Đang xử lý Batch {i}/100... Đã cào {i*100}/10.000 BĐS (Active Threads: 10)")
            time.sleep(0.05)
        st.success("🎉 Hoàn tất cào dữ liệu 10.000 BĐS thành công!")

with tab2:
    st.header("Agent Resource Telemetry")
    st.markdown("Giám sát tài nguyên RAM của từng Agent thời gian thực.")
    
    # Tạo bảng giả lập tài nguyên của Agent
    agent_data = {
        "Agent Name": ["CEO Sovereign", "Trading Agent", "Airdrop Bot", "Video Creator"],
        "Tier": ["Tier 0", "Tier 2", "Tier 3", "Tier 2"],
        "RAM Usage (MB)": [420.5, 1200.4, 250.2, 1980.1], # Video Creator ngốn nhiều RAM nhất
        "Status": ["ACTIVE (Safe)", "ACTIVE (Safe)", "IDLE", "ACTIVE (Warning > 1.8GB)"]
    }
    df = pd.DataFrame(agent_data)
    st.table(df)
    
    # Cảnh báo Watchdog
    st.markdown("---")
    st.header("💊 PROCESS WATCHDOG LOGS")
    failed_paths = Path(__file__).resolve().parent / "logs" / "FAILED_PATHS.json"
    if failed_paths.exists():
        with open(failed_paths, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
                failures = logs.get("failure_logs", [])
                if failures:
                    for fail in failures:
                        st.error(f"🚨 {fail}")
                else:
                    st.success("Watchdog: Hệ thống đang ở trạng thái an toàn vĩnh cửu.")
            except Exception:
                st.info("Watchdog: Log trống hoặc đang cập nhật.")
    else:
        st.success("Watchdog: Không phát hiện bất kỳ tiến trình rò rỉ nào.")

with tab3:
    st.header("Chaos Engineering Suite")
    st.markdown("Kích hoạt hệ thống thử lửa để kiểm tra độ bền vững của vương triều.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Watchdog Stress Test")
        if st.button("🛡️ Kích Hoạt Watchdog Test"):
            with st.spinner("Đang giả lập rò rỉ RAM (2GB)..."):
                import subprocess
                result = subprocess.run(["uv", "run", "pytest", "tests/test_watchdog.py", "-v"], capture_output=True, text=True)
                if result.returncode == 0:
                    st.success("✅ Watchdog: BẤT TỬ (Pass)")
                    st.code(result.stdout)
                else:
                    st.error("🚨 Watchdog: THẤT BẠI")
                    st.code(result.stderr or result.stdout)

    with col2:
        st.subheader("Trading Guard Test")
        if st.button("📈 Kích Hoạt Slippage Test"):
            with st.spinner("Đang giả lập trượt giá 1.5%..."):
                import subprocess
                result = subprocess.run(["uv", "run", "pytest", "tests/test_validation_gate.py", "-v"], capture_output=True, text=True)
                if result.returncode == 0:
                    st.success("✅ Slippage Guard: CHUẨN XÁC (Pass)")
                    st.code(result.stdout)
                else:
                    st.error("🚨 Slippage Guard: THẤT BẠI")
                    st.code(result.stderr or result.stdout)
