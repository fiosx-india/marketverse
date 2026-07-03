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
