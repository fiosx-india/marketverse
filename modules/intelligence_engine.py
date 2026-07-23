"""
MarketVerse Intelligence Engine
Version: 1.0
"""

import yfinance as yf
import pandas as pd


class IntelligenceEngine:

    def __init__(self):
        self.results = {}

    # -------------------------------
    # Live Market Data
    # -------------------------------
    def fetch_market_data(self, symbol):

        stock = yf.Ticker(symbol)

        df = stock.history(
            period="6mo",
            interval="1d"
            
        )

        return df

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
    # News Placeholder
    # -------------------------------
    def news_analysis(self, symbol):

        return {
            "sentiment": "Neutral",
            "confidence": 50
        }

    # -------------------------------
    # Options Placeholder
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

        if news["sentiment"] == "Positive":
            signal = "BUY"

        elif news["sentiment"] == "Negative":
            signal = "SELL"

        return signal

    # -------------------------------
    # Run Engine
    # -------------------------------
    def run(self, symbol):

        df = self.fetch_market_data(symbol)

        market = self.technical_analysis(df)

        news = self.news_analysis(symbol)

        options = self.options_analysis(symbol)

        signal = self.ai_decision(
            market,
            news
        )

        return {

            "market": market,

            "news": news,

            "options": options,

            "signal": signal,

            "volume_alert":
                self.volume_surveillance(df),

            "volatility":
                self.volatility(df)

        }
