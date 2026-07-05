import streamlit as st
import os
import sys
from pathlib import Path
from run_cleaner import DiskCleaner
from deep_scanner import DeepScanner

st.set_page_config(page_title="AI Disk Cleaner", page_icon="🧹", layout="centered")

st.title("🧹 AI DISK CLEANER")
st.caption("Commercial Version V1.0 | Giải phóng dung lượng ổ C cực nhanh")

st.info("💡 Đây là công cụ an toàn. Nó chỉ xóa các file tạm (Temp) và bộ nhớ đệm (Cache) dư thừa.")

tab1, tab2 = st.tabs(["🚀 Dọn dẹp nhanh", "🔍 Tầm soát tảng băng chìm"])

with tab1:
    st.subheader("Quy trình dọn dẹp hệ thống")
    col1, col2 = st.columns(2)
    with col1:
        clean_temp = st.checkbox("Xóa Temp Windows", value=True)
        clean_dev = st.checkbox("Dọn Cache Lập trình (pip, uv, npm)", value=True)
    with col2:
        clean_docker = st.checkbox("Dọn Docker (Dangling Images)", value=False)
        
    if st.button("🔥 BẮT ĐẦU DỌN DẸP", type="primary", use_container_width=True):
        cleaner = DiskCleaner()
        with st.status("🏗️ Đang xử lý...", expanded=True) as status:
            if clean_temp:
                st.write("Quét thư mục Temp...")
                cleaner.clean_temp_folders()
            if clean_dev:
                st.write("Dọn bộ nhớ đệm Dev...")
                cleaner.clean_dev_caches()
            if clean_docker:
                st.write("Giải phóng Docker...")
                cleaner.clean_docker()
            
            status.update(label="✅ Đã hoàn tất!", state="complete")
        
        st.success(f"🎉 Tuyệt vời! Đã giải phóng ước tính: {cleaner._format_size(cleaner.total_freed_bytes)}")
        st.balloons()

with tab2:
    st.subheader("Tìm kiếm file khổng lồ (>100MB)")
    scan_path = st.text_input("Đường dẫn cần quét (Mặc định là ổ C):", value="C:\\")
    
    if st.button("🔍 BẮT ĐẦU TẦM SOÁT", use_container_width=True):
        scanner = DeepScanner()
        with st.spinner("🕵️ Đang lùng sục toàn bộ ổ đĩa... (Có thể mất vài phút)"):
            large_files = scanner.scan(scan_path, min_size_mb=100)
            
        if not large_files:
            st.info("Không tìm thấy file nào lớn hơn 100MB.")
        else:
            st.warning(f"Tìm thấy {len(large_files)} file khổng lồ:")
            import pandas as pd
            df = pd.DataFrame(large_files, columns=["Đường dẫn", "Kích thước"])
            st.table(df)
            st.info("Mẹo: Hãy thủ công xóa các file này nếu bạn không còn dùng tới.")
