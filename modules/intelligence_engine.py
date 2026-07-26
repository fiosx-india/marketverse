"""
MarketVerse Intelligence Engine
Version: 1.0
"""

import yfinance as yf
import pandas as pd
from modules.news_analysis import analyze_news, get_dummy_news
from guardian.runtime_diagnostic import diagnostic
import ta

class IntelligenceEngine:

    def __init__(self):
        self.results = {}

    # -------------------------------
    # Symbol Mapping
    # -------------------------------
    def get_live_symbol(self, symbol):

        mapping = {
            "GOLD": "GC=F",
            "SILVER": "SI=F",
            "CRUDEOIL": "CL=F",
            "NATURALGAS": "NG=F",
            "COPPER": "HG=F"
        }

        return mapping.get(symbol, symbol)

    # -------------------------------
    # Live Market Data
    # -------------------------------
    def fetch_market_data(self, symbol):

        live_symbol = self.get_live_symbol(symbol)


        diagnostic.trace(
            "Input Symbol",
            symbol,
            "IntelligenceEngine.fetch_market_data"
        )

        diagnostic.trace(
            "Live Symbol",
            live_symbol,
            "IntelligenceEngine.fetch_market_data"
        )

        ok, message = diagnostic.validate_symbol(live_symbol)

        if not ok:
            print(message)

        try:

            stock = yf.Ticker(live_symbol)

            df = stock.history(
                period="6mo",
                interval="1d",
                auto_adjust=True
            )

            if df.empty:
                print(f"No data found for {live_symbol}")
                return pd.DataFrame()

            return df

        except Exception as e:
            
            diagnostic.error(
                    __file__,
                    "fetch_market_data",
                    e
            )
            
            print(f"Market data error ({live_symbol}): {e}")

            return pd.DataFrame()
    # -------------------------------
    # Technical Analysis
    # -------------------------------
    def technical_analysis(self, df):

        result = {}

        if df.empty:
            return result

        result["price"] = float(df["Close"].iloc[-1])
        result["high"] = float(df["High"].max())
        result["low"] = float(df["Low"].min())
        result["volume"] = int(df["Volume"].iloc[-1])

        # EMA 20
        result["ema20"] = float(
            df["Close"].ewm(span=20).mean().iloc[-1]
        )

        # EMA 50
        result["ema50"] = float(
            df["Close"].ewm(span=50).mean().iloc[-1]
        )


        # RSI 14
        delta = df["Close"].diff()

        gain = delta.where(delta > 0, 0).rolling(14).mean()

        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()

        rs = gain / loss

        result["rsi"] = float(
            (100 - (100 / (1 + rs))).iloc[-1]
        )

        return result

    # -------------------------------
    # Volume Surveillance
    # -------------------------------
    def volume_surveillance(self, df):

        if df.empty:
            return False

        sma20 = df["Volume"].rolling(20).mean()

        return bool(
            df["Volume"].iloc[-1] >
            sma20.iloc[-1] * 2
        )

    # -------------------------------
    # Volatility
    # -------------------------------
    def volatility(self, df):

        if df.empty:
            return 0

        pct = df["Close"].pct_change() * 100

        return float(
            pct.rolling(20).std().iloc[-1]
        )

    # -------------------------------
    # News Analysis
    # -------------------------------
    def news_analysis(self, symbol):

        headlines = get_dummy_news(symbol)

        result = analyze_news(symbol, headlines)

        return {
            "sentiment": result["overall_sentiment"],
            "confidence": result["confidence"]
        }

    # -------------------------------
    # Options Analysis
    # -------------------------------
    def options_analysis(self, symbol):

        return {
            "signal": "HOLD"
        }

    # -------------------------------
    # AI Decision
    # -------------------------------
    def ai_decision(self, market, news):

        signal = "HOLD"

        rsi = market.get("rsi", 50)

        if rsi < 30:
            signal = "BUY"

        elif rsi > 70:
            signal = "SELL"

        elif news.get("sentiment") in ("BULLISH", "VERY BULLISH"):
            signal = "BUY"

        elif news.get("sentiment") in ("BEARISH", "VERY BEARISH"):
            signal = "SELL"

        return signal

    # -------------------------------
    # Run Engine
    # -------------------------------
    def run(self, symbol):

        diagnostic.function(
                __file__,
                "run"
            )

            diagnostic.trace(
                "Run Symbol",
                symbol,
                "IntelligenceEngine.run"
            )

        df = self.fetch_market_data(symbol)

        market = self.technical_analysis(df)

        news = self.news_analysis(symbol)

        options = self.options_analysis(symbol)
        
        signal = self.ai_decision(market, news)
        
        print("Market:", market)
        print("News:", news)
        print("Signal:", signal)

        return {
            "market": market,
            "news": news,
            "options": options,
            "signal": signal,
            "confidence": news["confidence"],
            "volume_alert": self.volume_surveillance(df),
            "volatility": self.volatility(df)
        }
