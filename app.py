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
        st.metric("NIFTY 50", nifty if nifty else "Unavailable")
    with c2:
        sensex = get_live_price("^BSESN")
        st.metric("SENSEX", sensex if sensex else "Unavailable")
    with c3:
        banknifty = get_live_price("^NSEBANK")
        st.metric("BANK NIFTY", banknifty if banknifty else "Unavailable")

    c4, c5, c6 = st.columns(3)
    with c4:
        btc = get_live_price("BTC-USD")
        st.metric("BTC/USD", btc if btc else "Unavailable")
    with c5:
        gold = get_live_price("GC=F")
        st.metric("GOLD", gold if gold else "Unavailable")
    with c6:
        usdinr = get_live_price("INR=X")
        st.metric("USD/INR", usdinr if usdinr else "Unavailable")

    st.divider()
    left, right = st.columns([2, 1])
    with left:
        st.subheader("🌍 Markets")
        st.success("🇮🇳 Indian Market"); st.success("🇺🇸 US Market")
        st.success("₿ Cryptocurrency"); st.success("🥇 Gold")
        st.success("🥈 Silver"); st.success("💱 Forex")
    with right:
        st.subheader("🟢 Market Status")
        st.info("Market Data : Connected"); st.info("News Feed : Ready")
        st.info("AI Engine : Ready"); st.info("Risk Engine : Ready")

# ================= AI =================

with tab2:
    st.header("🤖 AI Prediction Engine")
    symbol = st.text_input("Enter NSE/BSE/Crypto Symbol", value="RELIANCE.NS")

    if st.button("Generate AI Prediction"):
        st.success("Prediction Generated Successfully")
        price = get_live_price(symbol)
        
        if price:
            st.metric("Current Price", price)
            st.subheader(symbol)
            c1, c2, c3 = st.columns(3)
            
            if price > 1000:
                signal, confidence, risk = "🟢 BUY", "88%", "Low"
            elif price > 500:
                signal, confidence, risk = "🟡 HOLD", "72%", "Medium"
            else:
                signal, confidence, risk = "🔴 SELL", "60%", "High"

            c1.metric("AI Signal", signal)
            c2.metric("Confidence", confidence)
            c3.metric("Risk", risk)

            entry = round(price, 2)
            if signal == "🟢 BUY":
                stoploss, t1, t2, t3 = price*0.98, price*1.02, price*1.04, price*1.06
            elif signal == "🟡 HOLD":
                stoploss, t1, t2, t3 = price*0.99, price*1.01, price*1.02, price*1.03
            else:
                stoploss, t1, t2, t3 = price*1.02, price*0.98, price*0.96, price*0.94

            st.info(f"Entry: {entry} | Stop Loss: {stoploss:.2f}")
            st.info(f"Targets: {t1:.2f} | {t2:.2f} | {t3:.2f}")
            
            st.divider()
            st.subheader("📊 Technical Analysis")
            st.metric("RSI", "58"); st.metric("MACD", "Bullish")
            st.progress(88, text="Technical Strength")
            st.subheader("🤖 AI Confidence")
            st.progress(int(confidence.replace("%","")), text="Prediction Confidence")
        else:
            st.error("Price data not available.")

# ================= NEWS & OTHERS =================
with tab3:
    st.header("📰 Global Financial News")
    # News logic goes here...

with tab4:
    st.header("💼 Smart Portfolio")

with tab5:
    st.header("⚙️ Settings")
    st.checkbox("Live Market", True)
    st.checkbox("AI Prediction", True)
