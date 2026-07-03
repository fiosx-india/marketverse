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

# ==========================================
# Dashboard
# ==========================================

with tab1:

    st.header("📊 Live Market Dashboard")

    if not data.empty and "Close" in data.columns:

        curr_price = float(data["Close"].iloc[-1])

        rsi = float(data["RSI_14"].iloc[-1]) \
            if pd.notna(data["RSI_14"].iloc[-1]) else None

        macd = float(data["MACD_12_26_9"].iloc[-1]) \
            if pd.notna(data["MACD_12_26_9"].iloc[-1]) else None

        macd_signal = float(data["MACDs_12_26_9"].iloc[-1]) \
            if pd.notna(data["MACDs_12_26_9"].iloc[-1]) else None

        ema20 = float(data["EMA_20"].iloc[-1]) \
            if pd.notna(data["EMA_20"].iloc[-1]) else None

        volume = int(data["Volume"].iloc[-1])

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Current Price",
            f"₹{curr_price:.2f}"
        )

        c2.metric(
            "RSI",
            f"{rsi:.2f}" if rsi is not None else "N/A"
        )

        c3.metric(
            "EMA 20",
            f"{ema20:.2f}" if ema20 is not None else "N/A"
        )

        c4.metric(
            "Volume",
            f"{volume:,}"
        )
