import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
import plotly.express as px
import os
from dotenv import load_dotenv

st.set_page_config(page_title="AI Trading Agent Dashboard", layout="wide")

# Load môi trường để lấy tickers
base_dir_env = Path(__file__).resolve().parent.parent.parent
load_dotenv(base_dir_env / ".env")

db_path = base_dir_env / "data" / "system_logs.db"
market_db_path = base_dir_env / "data" / "trading_market.db"

def get_paper_trade_data():
    if not db_path.exists():
        return pd.DataFrame()
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM Paper_Trade_Portfolio ORDER BY id", conn)
    conn.close()
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def get_decisions():
    if not db_path.exists():
        return pd.DataFrame()
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM Trading_Decisions ORDER BY id DESC LIMIT 50", conn)
    conn.close()
    return df

st.title("🤖 AI Trading Agent - Dashboard")

tab1, tab2 = st.tabs(["📊 PnL & Portfolio", "🧠 AI Decisions"])

with tab1:
    df_portfolio = get_paper_trade_data()
    if df_portfolio.empty:
        st.warning("Chưa có dữ liệu Portfolio. Vui lòng chạy live_advisor.py")
    else:
        st.subheader("Biểu đồ tăng trưởng tài sản (USDT)")
        fig = px.line(df_portfolio, x='timestamp', y='total_usdt_value', 
                      title='Total USDT Value Over Time', markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Assets", f"${df_portfolio['total_usdt_value'].iloc[-1]:,.2f}")
        with col2:
            initial = df_portfolio['total_usdt_value'].iloc[0]
            current = df_portfolio['total_usdt_value'].iloc[-1]
            roi = (current - initial) / initial * 100 if initial > 0 else 0
            st.metric("ROI (%)", f"{roi:+.2f}%")
            
        st.subheader("Lịch sử Portfolio")
        st.dataframe(df_portfolio.tail(10))

with tab2:
    df_decisions = get_decisions()
    if df_decisions.empty:
        st.warning("Chưa có quyết định nào từ AI.")
    else:
        st.subheader("50 Quyết định giao dịch gần nhất")
        for idx, row in df_decisions.iterrows():
            with st.expander(f"{row['timestamp']} - Confidence: {row['confidence']}/10"):
                st.write("**Action / Allocation:**")
                st.code(row['action'], language='json')
                st.write("**Lý do (Reasoning):**")
                st.write(row['reasoning'])

st.sidebar.markdown("---")
st.sidebar.info("Dashboard cập nhật realtime mỗi khi live_advisor.py chạy.")
st.sidebar.button("🔄 Refresh Data")