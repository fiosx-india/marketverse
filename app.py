import streamlit as st
import yfinance as yf
import pandas as pd
import ta
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

        # RSI
        df["RSI_14"] = ta.momentum.RSIIndicator(
            close=df["Close"],
            window=14
        ).rsi()

        # MACD
        macd = ta.trend.MACD(close=df["Close"])

        df["MACD_12_26_9"] = macd.macd()
        df["MACDs_12_26_9"] = macd.macd_signal()

        # EMA
        df["EMA_20"] = ta.trend.EMAIndicator(
            close=df["Close"],
            window=20
        ).ema_indicator()

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
        # ==========================================
        # Candlestick Chart
        # ==========================================

        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data.index,
                    open=data["Open"],
                    high=data["High"],
                    low=data["Low"],
                    close=data["Close"]
                )
            ]
        )

        fig.update_layout(
            title="Price Trend",
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ==========================================
        # AI Prediction
        # ==========================================

        st.subheader("🤖 AI Prediction Engine")

        if (
            rsi is None
            or macd is None
            or macd_signal is None
            or ema20 is None
        ):

            st.warning(
                "AI Signal : Waiting for sufficient data..."
            )

        else:

            if (
                rsi < 30
                and macd > macd_signal
                and curr_price > ema20
            ):

                st.success("🟢 STRONG BUY")

            elif (
                rsi > 70
                and macd < macd_signal
                and curr_price < ema20
            ):

                st.error("🔴 STRONG SELL")

            else:

                st.info("🟡 HOLD (Neutral)")

            # ==========================================
            # AI Confidence Score
            # ==========================================

            score = 50

            if rsi < 30:
                score += 15
            elif rsi > 70:
                score += 15

            if macd > macd_signal:
                score += 15

            if curr_price > ema20:
                score += 10

            score = min(score, 100)

            st.write(f"**AI Confidence Score : {score}%**")

            st.progress(score)

            # ==========================================
            # Confidence Level
            # ==========================================

            if score >= 85:
                st.success("🟢 Very High Confidence")

            elif score >= 70:
                st.info("🔵 High Confidence")

            elif score >= 55:
                st.warning("🟡 Medium Confidence")

            else:
                st.error("🔴 Low Confidence")

            st.caption(
                "Confidence is calculated using RSI + MACD + EMA Trend."
            )

            # ==========================================
            # Reason for Prediction
            # ==========================================

            st.subheader("📋 Reason for Prediction")

            if rsi < 30:
                st.success("✔ RSI indicates Oversold condition.")

            elif rsi > 70:
                st.error("✔ RSI indicates Overbought condition.")

            else:
                st.info("✔ RSI is Neutral.")
            if macd > macd_signal:
                st.success("✔ MACD is Bullish.")
            else:
                st.warning("✔ MACD is Bearish.")

            if curr_price > ema20:
                st.success("✔ Price is above EMA 20.")
            else:
                st.warning("✔ Price is below EMA 20.")

    else:
        st.error("No data available for this symbol.")

# ==========================================
# NEWS TAB
# ==========================================

with tab2:

    st.header("📰 Global Financial News")

    st.info("Breaking Market News")
    st.info("Stock Market Updates")
    st.info("Crypto News")
    st.info("Forex News")
    st.info("Gold & Silver News")

# ==========================================
# PORTFOLIO TAB
# ==========================================

with tab3:

    st.header("💼 Portfolio")

    st.info("Portfolio module coming soon.")

# ==========================================
# SETTINGS TAB
# ==========================================

with tab4:

    st.header("⚙️ Settings")

    st.checkbox("Auto Refresh", True)
    st.checkbox("AI Prediction", True)
    st.checkbox("Technical Analysis", True)
    st.checkbox("News Module", True)

    st.success("MarketVerse AI v3.0 RC")
