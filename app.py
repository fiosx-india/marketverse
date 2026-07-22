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
from modules.central_brain import CentralBrain
from modules.system_controller import SystemController

import yfinance as yf
import pandas as pd
import ta

# ==========================================
# Page Settings
# ==========================================
st.set_page_config(
    page_title="MarketVerse AI v3.0 RC",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# Guardian
# ==========================================
from guardian.controller import GuardianController

guardian = GuardianController()
guardian_result = guardian.run()

if guardian_result["report"].errors > 0:
    st.error("Guardian detected project errors.")

    with st.expander("Guardian Report"):
        st.write(guardian_result["report"])

        st.write("### Advice")
        for item in guardian_result["advice"]:
            st.write("•", item)

        st.write("### Validation Errors")
        st.json(guardian_result["validation_errors"])

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

    # Default values
    curr_price = None
    rsi = None
    macd = None
    macd_signal = None
    ema20 = None

    if not data.empty and "Close" in data.columns:
        curr_price = float(data["Close"].iloc[-1])

    if "RSI_14" in data.columns and pd.notna(data["RSI_14"].iloc[-1]):
        rsi = float(data["RSI_14"].iloc[-1])

    if "MACD_12_26_9" in data.columns and pd.notna(data["MACD_12_26_9"].iloc[-1]):
        macd = float(data["MACD_12_26_9"].iloc[-1])

    if "MACDs_12_26_9" in data.columns and pd.notna(data["MACDs_12_26_9"].iloc[-1]):
        macd_signal = float(data["MACDs_12_26_9"].iloc[-1])

    if "EMA_20" in data.columns and pd.notna(data["EMA_20"].iloc[-1]):
        ema20 = float(data["EMA_20"].iloc[-1])

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


# ==========================================
# Categorized Multi-File Selector & Exporter
# ==========================================
import os
import gc
import streamlit as st

st.subheader("🛡️ Categorized File Selector & Downloader")
st.caption("Select files by category (Mold, Core/Backend, UI/Frontend) to download bundles separately.")

current_dir = os.getcwd()

# Categorized lists
mold_files = []
core_files = []
frontend_files = []

ignore_dirs = {'.git', '.streamlit', '__pycache__', 'venv', 'env', 'build', 'dist', 'site-packages', 'lib', 'include', 'share'}

for root, dirs, files in os.walk(current_dir):
    dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('lib') and not d.startswith('python')]
    for file in files:
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(full_path, current_dir)
        
        if 'site-packages' in full_path or 'lib/python' in full_path:
            continue
            
        # Categorization logic
        if any(keyword in rel_path.lower() for keyword in ['.stl', '.step', '.iges', '.obj', '.dxf', 'mold']):
            mold_files.append(full_path)
        elif any(keyword in rel_path.lower() for keyword in ['app.py', 'core', 'guardian', 'backend']):
            core_files.append(full_path)
        else:
            frontend_files.append(full_path)

# Tabs for Categories
cat_tab1, cat_tab2, cat_tab3 = st.tabs(["📦 Mold Files", "⚙️ Core / Backend", "🖥️ Front / UI Files"])

def render_category_section(file_list, category_name):
    if not file_list:
        st.warning(f"⚠️ No files found in {category_name}.")
        return
        
    st.success(f"✨ Found {len(file_list)} file(s) in {category_name}.")
    selected = []
    
    for idx, f_path in enumerate(file_list):
        rel_name = os.path.relpath(f_path, current_dir)
        if st.checkbox(f"📁 {rel_name}", key=f"{category_name}_chk_{idx}"):
            selected.append(f_path)
            
    if selected:
        st.markdown("---")
        st.success(f"🎯 {len(selected)} file(s) selected from {category_name}.")
        
        bundle = []
        for f_path in selected:
            rel_path = os.path.relpath(f_path, current_dir)
            try:
                with open(f_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    sep = "=" * 50
                    bundle.append(f"\n\n{sep}\n# FILE: {rel_path}\n{sep}\n\n{content}")
            except Exception:
                continue
                
        combined = "".join(bundle)
        st.text_area(f"Copy {category_name} Content:", combined, height=200, key=f"{category_name}_area")
        
        st.download_button(
            label=f"📥 Download {category_name} Bundle (.txt)",
            data=combined,
            file_name=f"{category_name.lower().replace(' ', '_')}_bundle.txt",
            mime="text/plain",
            key=f"{category_name}_btn"
        )
        
        del combined
        del bundle
        gc.collect()

with cat_tab1:
    render_category_section(mold_files, "Mold Files")

with cat_tab2:
    render_category_section(core_files, "Core Files")

with cat_tab3:
    render_category_section(frontend_files, "Frontend Files")

