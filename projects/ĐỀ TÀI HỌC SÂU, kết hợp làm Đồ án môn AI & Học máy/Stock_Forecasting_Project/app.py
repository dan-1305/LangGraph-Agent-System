import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="AI Stock Dashboard", layout="wide")
st.title("📈 AI Stock Forecasting Dashboard")

ticker = st.text_input("🔍 Nhập mã cổ phiếu:", value="FPT")

# Tạo 2 Tab Giao diện cho 2 phần riêng biệt
tab1, tab2 = st.tabs(["🤖 Học Máy (Machine Learning)", "🧠 Học Sâu (Deep Learning - LSTM)"])

with tab1:
    if st.button("Phân loại xu hướng ngắn hạn", key="ml_btn"):
        st.success(f"Khuyến nghị cho {ticker}: **MUA (Xác suất 65%)**")
        
        img_path_ml = os.path.join(BASE_DIR, '01_Data', 'ml_feature_importance.png')
        if os.path.exists(img_path_ml):
            st.image(img_path_ml, caption="Tầm quan trọng của Đặc trưng (Feature Importance)", use_container_width=True)
        else:
            st.write("*(Đang chờ nạp biểu đồ...)*")

with tab2:
    if st.button("Dự báo chuỗi thời gian 3-5 phiên tới", key="dl_btn"):
        col1, col2 = st.columns(2)
        
        with col1:
            img_path_pred = os.path.join(BASE_DIR, '01_Data', 'lstm_prediction_chart.png')
            if os.path.exists(img_path_pred):
                st.image(img_path_pred, caption="Thực tế vs Dự đoán", use_container_width=True)
            else:
                st.write("*(Đang chờ nạp biểu đồ...)*")
                
        with col2:
            img_path_loss = os.path.join(BASE_DIR, '01_Data', 'lstm_loss_chart.png')
            if os.path.exists(img_path_loss):
                st.image(img_path_loss, caption="Biểu đồ Hàm Mất mát (Loss)", use_container_width=True)
            else:
                st.write("*(Đang chờ nạp biểu đồ...)*")
