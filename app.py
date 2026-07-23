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
from modules.portfolio import Portfolio
from modules.intelligence_engine import IntelligenceEngine

from project_check import ProjectChecker

import yfinance as yf
import pandas as pd
import ta

from modules.market_scanner import (
    scan_market,
    top_buy,
    top_sell,
    top_volume
)

from data.fno_stocks import FNO_STOCKS


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
engine = IntelligenceEngine()

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

if st.button("🔍 Run Project Check"):
    checker = ProjectChecker(".")
    checker.scan()

    st.session_state["project_report"] = checker.report

# ==========================================
# Download Data
# ==========================================

try:
    data = get_data(symbol)

    try:
        engine_result = engine.run(symbol)
        
        market_results = scan_market(FNO_STOCKS)

        buy_list = top_buy(market_results)

        sell_list = top_sell(market_results)

        volume_list = top_volume(market_results)
        
    except Exception as e:
        st.warning(f"Intelligence Engine: {e}")
        engine_result = {
            "signal": "N/A",
            "market": {},
            "news": {"sentiment": "Unknown"},
            "options": {"signal": "N/A"},
            "volume_alert": False,
            "volatility": 0.0
        }

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

if "project_report" in st.session_state:

    report = st.session_state["project_report"]

    st.subheader("📋 Project Report")

    st.metric("Health Score", f"{report['health']}%")
    st.metric("Files", report["total_files"])

    if report["errors"]:
        st.error(report["errors"])

    if report["warnings"]:
        st.warning(report["warnings"])

# ==========================================
# Dashboard
# ==========================================

with tab1:

    st.header("📊 Live Market Dashboard")
    
    st.subheader("🧠 Market Intelligence Engine")

    st.write(f"AI Signal : {engine_result['signal']}")

    st.write(f"Current Price : ₹{engine_result['market'].get('price', 'N/A')}")

    st.write(f"News Sentiment : {engine_result['news']['sentiment']}")

    st.write(f"Options Signal : {engine_result['options']['signal']}")

    st.write(f"Volume Alert : {engine_result['volume_alert']}")

    st.write(f"Volatility : {engine_result['volatility']:.2f}")

    st.markdown("---")

    st.subheader("📈 Market Scanner")

    col1, col2, col3 = st.columns(3)

with col1:
    st.write("### 🟢 Top Buy")
    st.dataframe(buy_list)

with col2:
    st.write("### 🔴 Top Sell")
    st.dataframe(sell_list)

with col3:
    st.write("### 🔵 Top Volume")
    st.dataframe(volume_list)
    
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
        
with tab4:
    
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = Portfolio()

    portfolio = st.session_state.portfolio

    st.subheader("➕ Add Stock")

    col1, col2, col3 = st.columns(3)

    with col1:
        stock_symbol = st.text_input(
            "Symbol",
            value="RELIANCE.NS",
            key="portfolio_symbol"
        )

    with col2:
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1
        )

    with col3:
        buy_price = st.number_input(
            "Buy Price",
            min_value=0.0,
            value=0.0,
            format="%.2f"
        )

    if st.button("➕ Add Stock"):
        portfolio.add_stock(
            stock_symbol,
            quantity,
            buy_price
        )
        st.success(f"{stock_symbol} added successfully.")

    st.markdown("---")

    st.subheader("📋 Portfolio Holdings")

    for symbol in portfolio.get_portfolio():

          try:
              live = yf.download(
                  symbol,
                  period="1d",
                  interval="1d",
                  auto_adjust=True,
                  progress=False
              )

              if not live.empty:
                  portfolio.update_price(
                      symbol,
                      float(live["Close"].iloc[-1])
                  )

          except Exception:
              pass

    holdings = portfolio.get_portfolio()

    if holdings:

        table = []

        for symbol, info in holdings.items():

            table.append({
                "Symbol": symbol,
                "Quantity": info["quantity"],
                "Buy Price": info["buy_price"],
                "Current Price": info.get("current_price", "-")
            })

        st.dataframe(
            pd.DataFrame(table),
            use_container_width=True
        )

        summary = portfolio.summary()

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Stocks",
            summary["stocks"]
        )

        c2.metric(
            "Portfolio Value",
            f"₹{summary['value']}"
        )

        c3.metric(
            "Profit / Loss",
            f"₹{summary['profit']}"
        )

        if st.button("🗑 Clear Portfolio"):
            portfolio.clear()
            st.rerun()

    else:
        st.info("No stocks added yet.")

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
# MarketVerse - Secure Categorized File Exporter & Pass Multiplier
# ==========================================
import os
import gc
import streamlit as st

st.subheader("🛡️ MarketVerse Project File Exporter & Downloader")
st.caption("Organized file selector: Core, Guardian, Modules & Root files auto-scanned from your repository structure.")

current_dir = os.getcwd()

root_files = []
core_files = []
guardian_files = []
module_files = []
other_files = []

ignore_dirs = {'.git', '.streamlit', '__pycache__', 'venv', 'env', 'build', 'dist', 'site-packages', 'lib', 'include', 'share'}

for root, dirs, files in os.walk(current_dir):
    dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('lib') and not d.startswith('python')]
    for file in files:
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(full_path, current_dir)
        
        if 'site-packages' in full_path or 'lib/python' in full_path:
            continue
            
        rel_lower = rel_path.lower()
        file_dir = os.path.dirname(rel_path)
        
        if rel_lower.startswith('core' + os.sep) or rel_lower.startswith('core/'):
            core_files.append(full_path)
        elif rel_lower.startswith('guardian' + os.sep) or rel_lower.startswith('guardian/'):
            guardian_files.append(full_path)
        elif rel_lower.startswith('modules' + os.sep) or rel_lower.startswith('modules/'):
            module_files.append(full_path)
        elif file_dir == '' or file_dir == '.':
            root_files.append(full_path)
        else:
            other_files.append(full_path)

tab_root, tab_guardian, tab_core, tab_modules, tab_other = st.tabs([
    "📄 Root Files (app.py, README)", 
    "🛡️ Guardian", 
    "⚙️ Core", 
    "📦 Modules", 
    "📂 Other Files"
])

def render_exporter_tab(file_list, tab_label):
    if not file_list:
        st.warning(f"⚠️ No files found in {tab_label}.")
        return
        
    st.success(f"✨ Found {len(file_list)} file(s) in {tab_label}.")
    selected = []
    
    for idx, f_path in enumerate(file_list):
        rel_name = os.path.relpath(f_path, current_dir)
        if st.checkbox(f"📁 {rel_name}", key=f"exp_{tab_label}_{idx}"):
            selected.append(f_path)
            
    if selected:
        st.markdown("---")
        st.success(f"🎯 {len(selected)} file(s) selected.")
        
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
        st.text_area(f"Copy {tab_label} Content:", combined, height=250, key=f"area_{tab_label}")
        
        st.download_button(
            label=f"📥 Download {tab_label} Bundle (.txt)",
            data=combined,
            file_name=f"{tab_label.lower().replace(' ', '_')}_bundle.txt",
            mime="text/plain",
            key=f"btn_{tab_label}"
        )
        
        st.info("🔒 **Auto-Erase Protection Active:** RAM memory cleared instantly after export.")
        del combined
        del bundle
        gc.collect()

with tab_root:
    render_exporter_tab(root_files, "Root Files")

with tab_guardian:
    render_exporter_tab(guardian_files, "Guardian")

with tab_core:
    render_exporter_tab(core_files, "Core")

with tab_modules:
    render_exporter_tab(module_files, "Modules")

with tab_other:
    render_exporter_tab(other_files, "Other Files")

# ==========================================
# Code Pass Multiplier & Shifting Tool (Fixed Shifting)
# ==========================================
import streamlit.components.v1 as components

st.markdown("---")
st.subheader("🔄 Code Pass Multiplier & Shifting Tool")
st.caption("Generate unified single block passes, control exact spacing from frame, copy cleanly, and delete output instantly.")

col_m1, col_m2 = st.columns([2, 1])

with col_m1:
    if "target_code_input" not in st.session_state:
        st.session_state["target_code_input"] = ""

    user_target_code = st.text_area(
        "Paste target code line or block:", 
        height=130, 
        key="target_code_input", 
        placeholder="Paste your code here..."
    )

with col_m2:
    selected_pass_count = st.selectbox(
        "Select Passes:", 
        [1, 2, 4, 8, 12, 16], 
        index=1
    )
    # Frame shifting spaces (4, 8, 12, 16, 20 spaces)
    pass_spacing_spaces = st.selectbox(
        "Spacing Points from Frame:", 
        [4, 8, 12, 16, 20, 24, 32], 
        index=3
    )

btn_col1, btn_col2 = st.columns([1, 1])

with btn_col1:
    generate_clicked = st.button("🚀 Generate Single Block")

with btn_col2:
    if st.button("🗑️ Clear / Delete Input"):
        st.session_state["target_code_input"] = ""
        if "generated_output" in st.session_state:
            st.session_state.generated_output = ""
        st.rerun()

if "generated_output" not in st.session_state:
    st.session_state.generated_output = ""

if generate_clicked:
    if user_target_code.strip():
        # Correctly shift each line by selected spaces for each pass
        indent_str = " " * pass_spacing_spaces
        raw_lines = user_target_code.strip().splitlines()
        
        generated_passes = []
        for p in range(1, selected_pass_count + 1):
            # Apply shifting spaces to every line of the block
            shifted_block = "\n".join([f"{indent_str}{line}" if line.strip() else "" for line in raw_lines])
            generated_passes.append(shifted_block)
            
        # Join passes with standard newlines so they stack cleanly
        st.session_state.generated_output = "\n\n".join(generated_passes)
        st.success(f"✨ Successfully generated **{selected_pass_count} Passes** shifted by {pass_spacing_spaces} points!")
    else:
        st.warning("⚠️ Please paste some code above to generate passes.")

# =================-----------------------------
# Output & Custom HTML Copy Component
# ---------------------------------------------
if st.session_state.generated_output:

    st.markdown("### 📋 Copy Output")

    components.html(
        f"""
        <textarea id="copyText"
            style="width:100%;height:280px;
            font-family:monospace;
            font-size:14px;
            padding:10px;
            background:#1e1e1e;
            color:#fff;
            border:1px solid #444;
            border-radius:6px;">{st.session_state.generated_output}</textarea>

        <br><br>

        <button
            onclick="
                navigator.clipboard.writeText(
                    document.getElementById('copyText').value
                );
                alert('✅ Code Copied Successfully!');
            "
            style="
                background:#4CAF50;
                color:white;
                border:none;
                padding:10px 18px;
                border-radius:6px;
                cursor:pointer;
                margin-right:10px;
            ">
            📋 Copy Output
        </button>
        """,
        height=380,
    )

    if st.button(
        "🗑 Delete Output",
        use_container_width=True
    ):
        st.session_state.generated_output = ""
        st.rerun()

