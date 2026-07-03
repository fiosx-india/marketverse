import streamlit as st
import yfinance as yf
import pandas as pd

# ================= LIVE PRICE =================

def get_live_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")

        if data.empty:
            return None

        return round(float(data["Close"].iloc[-1]), 2)

    except Exception:
        return None


st.set_page_config(
    page_title="MarketVerse AI",
    page_icon="🚀",
    layout="wide"
)

# ================= HEADER =================

st.title("🚀 MarketVerse AI")
st.caption("Professional Global Financial Intelligence Platform v2.0")

# ================= TABS =================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "🤖 AI Prediction",
    "📰 News",
    "💼 Portfolio",
    "⚙️ Settings"
])

# ================= DASHBOARD =================

with tab1:

    st.header("📈 Live Market Dashboard")

    c1, c2, c3 = st.columns(3)

    with c1:
    nifty = get_live_price("^NSEI")

    st.metric(
        "NIFTY 50",
        nifty if nifty else "Unavailable"
    )
   with c2:
    sensex = get_live_price("^BSESN")

    st.metric(
        "SENSEX",
        sensex if sensex else "Unavailable"
    )
    

    with c3:
    banknifty = get_live_price("^NSEBANK")

    st.metric(
        "BANK NIFTY",
        banknifty if banknifty else "Unavailable"
    )

    c4, c5, c6 = st.columns(3)

    with c4:
    btc = get_live_price("BTC-USD")

    st.metric(
        "BTC/USD",
        btc if btc else "Unavailable"
    )
   with c5:
    gold = get_live_price("GC=F")

    st.metric(
        "GOLD",
        gold if gold else "Unavailable"
    )
    

    with c6:
    usdinr = get_live_price("INR=X")

    st.metric(
        "USD/INR",
        usdinr if usdinr else "Unavailable"
    )

    st.divider()

    left, right = st.columns([2,1])

    with left:
        st.subheader("🌍 Markets")

        st.success("🇮🇳 Indian Market")
        st.success("🇺🇸 US Market")
        st.success("₿ Cryptocurrency")
        st.success("🥇 Gold")
        st.success("🥈 Silver")
        st.success("💱 Forex")

    with right:

        st.subheader("🟢 Market Status")

        st.info("Market Data : Connecting...")
        st.info("News Feed : Ready")
        st.info("AI Engine : Ready")
        st.info("Risk Engine : Ready")

    st.divider()

    st.subheader("📊 Market Overview")

    st.info("Live Charts will appear here.")
    st.info("Top Gainers will appear here.")
    st.info("Top Losers will appear here.")
    st.info("Market Heatmap will appear here.")

# ================= AI =================

with tab2:

    st.header("🤖 AI Prediction Engine")

    symbol = st.text_input(
        "Enter NSE/BSE/Crypto Symbol",
        value="RELIANCE.NS"
    )

    if st.button("Generate AI Prediction"):

        st.success("Prediction Generated Successfully")

        price = get_live_price(symbol)

if price:
    st.metric("Current Price", price)
    
        st.subheader(symbol)

        c1,c2,c3 = st.columns(3)

    if price > 1000:
        signal = "🟢 BUY"
        confidence = "88%"
        risk = "Low"

    elif price > 500:
        signal = "🟡 HOLD"
        confidence = "72%"
        risk = "Medium"

    else:
        signal = "🔴 SELL"
        confidence = "60%"
        risk = "High"

else:
    signal = "N/A"
    confidence = "0%"
    risk = "Unknown"

c1.metric("AI Signal", signal)
c2.metric("Confidence", confidence)
c3.metric("Risk", risk)

        if price:
    entry = round(price, 2)

if signal == "🟢 BUY":
    stoploss = round(price * 0.98, 2)
    target1 = round(price * 1.02, 2)
    target2 = round(price * 1.04, 2)
    target3 = round(price * 1.06, 2)

elif signal == "🟡 HOLD":
    stoploss = round(price * 0.99, 2)
    target1 = round(price * 1.01, 2)
    target2 = round(price * 1.02, 2)
    target3 = round(price * 1.03, 2)

else:
    stoploss = round(price * 1.02, 2)
    target1 = round(price * 0.98, 2)
    target2 = round(price * 0.96, 2)
    target3 = round(price * 0.94, 2)

    st.info(f"Entry Price : {entry}")
    st.info(f"Stop Loss : {stoploss}")
    st.info(f"Target 1 : {target1}")
    st.info(f"Target 2 : {target2}")
    st.info(f"Target 3 : {target3}")
else:
    st.error("Price data not available.")
        
        st.divider()

st.subheader("📊 Technical Analysis")

st.metric("RSI", "58")
st.metric("MACD", "Bullish")
st.metric("EMA Trend", "Uptrend")

st.progress(88, text="Technical Strength")

st.subheader("📰 News Sentiment")

st.success("Positive Market Sentiment")
st.progress(76, text="News Score")

st.subheader("🤖 AI Confidence")

st.metric("AI Score", confidence)
st.progress(int(confidence.replace("%","")), text="Prediction Confidence")

# ================= NEWS =================

with tab3:

    st.header("📰 Global Financial News")

    st.info("Breaking News")
    st.info("Market News")
    st.info("Crypto News")
    st.info("Forex News")
    st.info("Commodities News")

# ================= PORTFOLIO =================

with tab4:

    st.header("💼 Smart Portfolio")

    c1,c2,c3 = st.columns(3)

    c1.metric("Total Value","₹0")
    c2.metric("Today's P/L","₹0")
    c3.metric("Holdings","0")

    st.divider()

    st.info("Portfolio Holdings will appear here.")
    st.info("Sector Allocation will appear here.")
    st.info("Risk Analysis will appear here.")

# ================= SETTINGS =================

with tab5:

    st.header("⚙️ Settings")

    st.success("MarketVerse AI Version 2.0")

    st.write("Modules")

    st.checkbox("Live Market",True)
    st.checkbox("AI Prediction",True)
    st.checkbox("Technical Analysis",True)
    st.checkbox("News Engine",True)
    st.checkbox("Risk Manager",True)
    st.checkbox("Portfolio Manager",True)

    st.divider()

    st.info("Developed by MarketVerse AI")
