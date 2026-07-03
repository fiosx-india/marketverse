import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# ==========================================
# Auto Refresh
# ==========================================

st_autorefresh(
    interval=60000,
    key="data_refresh"
)

# ==========================================
# Page Settings
# ==========================================

st.set_page_config(
    page_title="MarketVerse AI v3.0 RC",
    page_icon="🚀",
    layout="wide"
)

# ==========================================
# Download Market Data
# ==========================================

def get_data(symbol):

    df = yf.download(
        symbol,
        period="3mo",
        interval="1d",
        auto_adjust=True,
        progress=False
    )

    # Fix MultiIndex Columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if not df.empty:
        df.ta.rsi(length=14, append=True)
        df.ta.macd(append=True)
        df.ta.ema(length=20, append=True)

    return df
# ==========================================
# Sidebar
# ==========================================

st.sidebar.title("🎯 MarketVerse Control")

symbol = st.sidebar.text_input(
    "Enter NSE/BSE/Crypto Symbol",
    value="RELIANCE.NS"
)

st.sidebar.markdown("---")

st.sidebar.success("✅ Live Market")
st.sidebar.success("✅ AI Prediction")
st.sidebar.success("✅ Technical Analysis")
st.sidebar.success("✅ Auto Refresh : 60 Seconds")

# ==========================================
# Download Data
# ==========================================

try:
    data = get_data(symbol)

except Exception as e:
    st.error(f"Download Error : {e}")
    st.stop()

# ==========================================
# Main Header
# ==========================================

st.title("🚀 MarketVerse AI")

st.caption(
    "Professional Global Financial Intelligence Platform"
)

# ==========================================
# Tabs
# ==========================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "🤖 AI Prediction",
    "📰 News",
    "💼 Portfolio",
    "⚙️ Settings"
])
