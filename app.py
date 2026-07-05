import streamlit as st
from modules.news import get_market_news
from modules.news_analysis import analyze_news
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

from modules.ai_engine import analyze
from modules.market_scanner import scan_market
from modules.performance_tracker import PerformanceTracker
from modules.trade_executor import TradeExecutor
from modules.system_manager import SystemManager
from modules.dashboard_utils import dashboard_summary
from modules.market_events import detect_market_events
from modules.ai_engine import analyze

import yfinance as yf
import pandas as pd
import ta

# ==========================================
# Page Settings
# ==========================================

st.set_page_config(
    page_title="MarketVerse AI v3.0 RC",
    page_icon="🚀",
    layout="wide"
)

# ==========================================
# Auto Refresh
# ==========================================

st_autorefresh(
    interval=60000,
    key="data_refresh"
)

# ==========================================
# Initialize Modules
# ==========================================

tracker = PerformanceTracker()
executor = TradeExecutor()
system = SystemManager()

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

    # ==========================================
    # Dashboard Summary
    # ==========================================

    try:
        dashboard_summary()
    except Exception:
        pass

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

        volume = (
    int(data["Volume"].iloc[-1])
    if pd.notna(data["Volume"].iloc[-1])
    else 0
)

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
# AI PREDICTION TAB
# ==========================================

with tab2:

    st.header("🤖 AI Prediction")

    if not data.empty:

        st.subheader("AI Trading Signal")

        score = 0

        if rsi is not None:
            if rsi < 30:
                score += 2
            elif rsi > 70:
                score -= 2

        if macd is not None and macd_signal is not None:
            if macd > macd_signal:
                score += 2
            else:
                score -= 2

        if curr_price > ema20:
            score += 2
        else:
            score -= 2

        if score >= 4:
            prediction = "🟢 STRONG BUY"
            confidence = 92
        elif score >= 2:
            prediction = "🟢 BUY"
            confidence = 80
        elif score <= -4:
            prediction = "🔴 STRONG SELL"
            confidence = 92
        elif score <= -2:
            prediction = "🔴 SELL"
            confidence = 80
        else:
            prediction = "🟡 HOLD"
            confidence = 65

        st.metric("Prediction", prediction)
        st.metric("Confidence", f"{confidence}%")

        st.progress(confidence / 100)

        st.write("### AI Explanation")

        if prediction == "🟢 STRONG BUY":
            st.success("Trend is bullish. Momentum and indicators support buying.")

        elif prediction == "🟢 BUY":
            st.success("Indicators are mostly bullish. Buy opportunity detected.")

        elif prediction == "🟡 HOLD":
            st.warning("Market is neutral. Wait for confirmation before trading.")

        elif prediction == "🔴 SELL":
            st.error("Indicators are turning bearish. Selling pressure detected.")

        else:
            st.error("Strong bearish trend. Avoid fresh buying.")

    else:
        st.warning("No market data available.")

# ==========================================
# NEWS TAB
# ==========================================

with tab3:

    st.header("📰 Global Financial News")

    news_data = get_market_news(symbol)

    news = news_data["articles"]
    analytics = news_data["analytics"]

    market_events = detect_market_events(news)

    if not news:
        st.warning("No news available.")

    else:

        headlines = []

        for item in news:

            st.subheader(item["title"])

            if item["description"]:
                st.write(item["description"])

            st.caption(
                f'{item["source"]} | {item["published"]}'
            )

            st.markdown("---")

            headlines.append(item["title"])

        sentiment = analyze_news(symbol, headlines)

        st.success(
            f"Overall Sentiment : {sentiment['overall_sentiment']}"
        )

        st.metric(
            "Confidence",
            f"{sentiment['confidence']}%"
        )

# ==========================================
# PORTFOLIO TAB
# ==========================================

with tab4:

    st.header("💼 Portfolio")

    st.info("Portfolio module coming soon.")

# ==========================================
# SETTINGS TAB
# ==========================================

with tab5:

    st.header("⚙️ Settings")

    st.checkbox("Auto Refresh", True)
    st.checkbox("AI Prediction", True)
    st.checkbox("Technical Analysis", True)
    st.checkbox("News Module", True)

    st.success("MarketVerse AI v3.0 RC")
