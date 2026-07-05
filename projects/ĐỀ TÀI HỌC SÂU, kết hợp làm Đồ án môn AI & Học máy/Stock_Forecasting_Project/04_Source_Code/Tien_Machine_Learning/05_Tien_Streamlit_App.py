import streamlit as st
import pandas as pd
import numpy as np

# Title and Description
st.title("Stock Trend Prediction Web App")
st.write("Dự án do Nguyễn Công Tiến phát triển (Phần Giao diện UI và Machine Learning cơ bản).")
st.write("---")

# Sidebar for User Inputs
st.sidebar.header("Tùy chọn Cổ Phiếu")
ticker = st.sidebar.selectbox(
    "Chọn mã cổ phiếu VN30:",
    ("FPT", "HPG", "MBB", "MWG", "VIC", "VNM")
)

st.sidebar.write("*(Đây là bản Demo, trong thực tế sẽ gọi Model đã được train để phân loại xu hướng Tăng/Giảm)*")

# Main Content
st.header(f"Phân tích Cổ phiếu: {ticker}")

st.info("Đang tích hợp mô hình Machine Learning... Vui lòng xem các Notebook (Tien_Machine_Learning) để biết thêm chi tiết về quá trình Training.")

# Dummy Data for Visualization
st.subheader("Biểu đồ Giá mô phỏng")
dates = pd.date_range('20230101', periods=100)
df = pd.DataFrame(np.random.randn(100, 1).cumsum(), index=dates, columns=['Price'])
st.line_chart(df)

st.success("Kết luận Mô hình ML (Mô phỏng): DỰ BÁO TĂNG (65%)")