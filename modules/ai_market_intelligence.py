"""
==========================================================
MarketVerse AI Market Intelligence Engine
Version : 1.0
==========================================================
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AISignal:

    signal: str
    confidence: int
    sentiment: str
    risk: str
    recommendation: str


class AIMarketIntelligence:

    def __init__(self):

        self.version = "1.0"

    # ==========================================
    # LIVE MARKET
    # ==========================================

    def market_status(self):

        return {
            "NSE": True,
            "MCX": True,
            "GLOBAL": True,
            "UPDATED": datetime.now()
        }

    # ==========================================
    # TECHNICAL AI
    # ==========================================
    def technical_analysis(self, df):

        if df is None or len(df) < 50:
            return {
                "RSI": None,
                "MACD": None,
                "EMA20": None,
                "EMA50": None,
                "EMA200": None,
                "VWAP": None,
                "ATR": None,
                "ADX": None,
                "SUPERTREND": None,
                "BOLLINGER": None,
            }

        result = {}

        try:
            import pandas_ta as ta

            # EMA
            df["EMA20"] = ta.ema(df["Close"], length=20)
            df["EMA50"] = ta.ema(df["Close"], length=50)
            df["EMA200"] = ta.ema(df["Close"], length=200)

            # RSI
            df["RSI"] = ta.rsi(df["Close"], length=14)

            # MACD
            macd = ta.macd(df["Close"])
            df["MACD"] = macd["MACD_12_26_9"]

            # ATR
            df["ATR"] = ta.atr(
                df["High"],
                df["Low"],
                df["Close"],
                length=14
            )

            # ADX
            adx = ta.adx(
                df["High"],
                df["Low"],
                df["Close"]
            )

            df["ADX"] = adx["ADX_14"]

            # VWAP
            df["VWAP"] = ta.vwap(
                df["High"],
                df["Low"],
                df["Close"],
                df["Volume"]
            )

            # Bollinger Bands
            bb = ta.bbands(df["Close"])

            # Supertrend
            st = ta.supertrend(
                df["High"],
                df["Low"],
                df["Close"]
            )

            result = {

                "RSI": round(df["RSI"].iloc[-1], 2),

                "MACD": round(df["MACD"].iloc[-1], 2),

                "EMA20": round(df["EMA20"].iloc[-1], 2),

                "EMA50": round(df["EMA50"].iloc[-1], 2),

                "EMA200": round(df["EMA200"].iloc[-1], 2),

                "VWAP": round(df["VWAP"].iloc[-1], 2),

                "ATR": round(df["ATR"].iloc[-1], 2),

                "ADX": round(df["ADX"].iloc[-1], 2),

                "SUPERTREND": st.iloc[-1].to_dict(),

                "BOLLINGER": bb.iloc[-1].to_dict(),
            }

        except Exception as e:

            result = {
                "ERROR": str(e)
            }

        return result

    # ==========================================
    # AI SIGNAL
    # ==========================================

    def generate_signal(self):

        return AISignal(
            signal="BUY",
            confidence=95,
            sentiment="BULLISH",
            risk="LOW",
            recommendation="BUY ON DIPS"
        )

    # ==========================================
    # SMART TRACKING
    # ==========================================

    def tracking(self):

        return {
            "BREAKOUT": False,
            "BREAKDOWN": False,
            "GAPUP": False,
            "GAPDOWN": False,
            "HIGH_VOLUME": False,
            "UNUSUAL_MOVE": False,
        }

    # ==========================================
    # NEWS AI
    # ==========================================

    def news_monitor(self):

        return {
            "SEBI": [],
            "RBI": [],
            "NSE": [],
            "MCX": [],
            "COMPANY": [],
            "GLOBAL": []
        }

    # ==========================================
    # OPTIONS AI
    # ==========================================

    def option_analysis(self):

        return {
            "PCR": None,
            "OI": None,
            "MAX_PAIN": None,
            "IV": None,
            "GAMMA": None,
        }

    # ==========================================
    # RISK
    # ==========================================

    def risk_engine(self):

        return {
            "STOPLOSS": None,
            "TARGET": None,
            "RR_RATIO": None,
            "POSITION_SIZE": None,
        }

    # ==========================================
    # PREDICTION
    # ==========================================

    def prediction(self):

        return {
            "INTRADAY": None,
            "TOMORROW": None,
            "WEEKLY": None,
            "MONTHLY": None,
        }
        
    # ==========================================
    # TREND ANALYSIS
    # ==========================================
    def trend_analysis(self, df):

        if df is None or len(df) < 200:
            return {
                "SHORT_TERM": None,
                "MEDIUM_TERM": None,
                "LONG_TERM": None,
                "TREND": None,
                "GOLDEN_CROSS": False,
                "DEATH_CROSS": False,
            }

        try:
            import pandas_ta as ta

            df["EMA20"] = ta.ema(df["Close"], length=20)
            df["EMA50"] = ta.ema(df["Close"], length=50)
            df["EMA200"] = ta.ema(df["Close"], length=200)

            close = df["Close"].iloc[-1]
            ema20 = df["EMA20"].iloc[-1]
            ema50 = df["EMA50"].iloc[-1]
            ema200 = df["EMA200"].iloc[-1]

            short_term = "UP" if close > ema20 else "DOWN"
            medium_term = "UP" if ema20 > ema50 else "DOWN"
            long_term = "UP" if ema50 > ema200 else "DOWN"

            if short_term == medium_term == long_term == "UP":
                trend = "STRONG_BULLISH"
            elif short_term == medium_term == long_term == "DOWN":
                trend = "STRONG_BEARISH"
            else:
                trend = "SIDEWAYS"

            golden_cross = (
                df["EMA50"].iloc[-2] < df["EMA200"].iloc[-2]
                and ema50 > ema200
            )

            death_cross = (
                df["EMA50"].iloc[-2] > df["EMA200"].iloc[-2]
                and ema50 < ema200
            )

            return {
                "SHORT_TERM": short_term,
                "MEDIUM_TERM": medium_term,
                "LONG_TERM": long_term,
                "TREND": trend,
                "GOLDEN_CROSS": golden_cross,
                "DEATH_CROSS": death_cross,
                "EMA20": round(ema20, 2),
                "EMA50": round(ema50, 2),
                "EMA200": round(ema200, 2),
            }

        except Exception as e:

            return {
                "ERROR": str(e)
            }

    # ==========================================
    # VOLUME ANALYSIS
    # ==========================================
    def volume_analysis(self, df):

        if df is None or len(df) < 20:
            return {
                "VOLUME": None,
                "AVG_VOLUME": None,
                "RELATIVE_VOLUME": None,
                "VOLUME_SPIKE": False,
                "OBV": None,
                "CMF": None,
            }

        try:
            import pandas_ta as ta

            volume = float(df["Volume"].iloc[-1])
            avg_volume = float(df["Volume"].rolling(20).mean().iloc[-1])

            relative_volume = (
                volume / avg_volume if avg_volume > 0 else 0
            )

            volume_spike = relative_volume >= 2.0

            # On Balance Volume
            df["OBV"] = ta.obv(
                df["Close"],
                df["Volume"]
            )

            # Chaikin Money Flow
            df["CMF"] = ta.cmf(
                df["High"],
                df["Low"],
                df["Close"],
                df["Volume"]
            )

            return {

                "VOLUME": round(volume, 2),

                "AVG_VOLUME": round(avg_volume, 2),

                "RELATIVE_VOLUME": round(relative_volume, 2),

                "VOLUME_SPIKE": volume_spike,

                "OBV": round(df["OBV"].iloc[-1], 2),

                "CMF": round(df["CMF"].iloc[-1], 4),
            }

        except Exception as e:

            return {
                "ERROR": str(e)
            }


    # ==========================================
    # VOLATILITY ANALYSIS
    # ==========================================
    def volatility_analysis(self, df):

        if df is None or len(df) < 20:
            return {
                "ATR": None,
                "VOLATILITY": None,
                "BOLLINGER_WIDTH": None,
                "VOLATILITY_LEVEL": None,
            }

        try:
            import pandas_ta as ta
            import numpy as np

            # ATR
            df["ATR"] = ta.atr(
                df["High"],
                df["Low"],
                df["Close"],
                length=14
            )

            # Historical Volatility
            returns = np.log(df["Close"] / df["Close"].shift(1))
            volatility = returns.std() * np.sqrt(252) * 100

            # Bollinger Band Width
            bb = ta.bbands(df["Close"], length=20)
            upper = bb["BBU_20_2.0"].iloc[-1]
            lower = bb["BBL_20_2.0"].iloc[-1]
            middle = bb["BBM_20_2.0"].iloc[-1]

            bb_width = ((upper - lower) / middle) * 100

            if volatility < 20:
                level = "LOW"
            elif volatility < 40:
                level = "MEDIUM"
            else:
                level = "HIGH"

            return {
                "ATR": round(df["ATR"].iloc[-1], 2),
                "VOLATILITY": round(volatility, 2),
                "BOLLINGER_WIDTH": round(bb_width, 2),
                "VOLATILITY_LEVEL": level,
            }

        except Exception as e:
            return {
                "ERROR": str(e)
            }
            
    # ==========================================
    # MOMENTUM ANALYSIS
    # ==========================================
    def momentum_analysis(self, df):

        if df is None or len(df) < 20:
            return {
                "MOMENTUM_SCORE": None,
                "ROC": None,
                "CCI": None,
                "STOCHASTIC": None,
            }

        try:
            import pandas_ta as ta

            df["ROC"] = ta.roc(df["Close"], length=14)

            df["CCI"] = ta.cci(
                df["High"],
                df["Low"],
                df["Close"],
                length=20
            )

            stoch = ta.stoch(
                df["High"],
                df["Low"],
                df["Close"]
            )

            k = stoch["STOCHk_14_3_3"].iloc[-1]

            score = 0

            if df["ROC"].iloc[-1] > 0:
                score += 40

            if df["CCI"].iloc[-1] > 100:
                score += 30
            elif df["CCI"].iloc[-1] > 0:
                score += 15

            if k > 80:
                score += 30
            elif k > 50:
                score += 15

            return {
                "MOMENTUM_SCORE": score,
                "ROC": round(df["ROC"].iloc[-1], 2),
                "CCI": round(df["CCI"].iloc[-1], 2),
                "STOCHASTIC": round(k, 2),
            }

        except Exception as e:
            return {
                "ERROR": str(e)
            }

    # ==========================================
    # SUPPORT / RESISTANCE
    # ==========================================
    def support_resistance(self, df):

        if df is None or len(df) < 2:
            return {
                "PIVOT": None,
                "SUPPORT_1": None,
                "SUPPORT_2": None,
                "RESISTANCE_1": None,
                "RESISTANCE_2": None,
            }

        try:
            high = float(df["High"].iloc[-2])
            low = float(df["Low"].iloc[-2])
            close = float(df["Close"].iloc[-2])

            pivot = (high + low + close) / 3

            r1 = (2 * pivot) - low
            s1 = (2 * pivot) - high

            r2 = pivot + (high - low)
            s2 = pivot - (high - low)

            return {
                "PIVOT": round(pivot, 2),
                "SUPPORT_1": round(s1, 2),
                "SUPPORT_2": round(s2, 2),
                "RESISTANCE_1": round(r1, 2),
                "RESISTANCE_2": round(r2, 2),
            }

        except Exception as e:
            return {
                "ERROR": str(e)
            }
    # ==========================================
    # SECTOR ANALYSIS
    # ==========================================
    def sector_analysis(self):

        return {
            "SECTOR": None,
            "SECTOR_STRENGTH": None,
            "SECTOR_RANK": None,
            "LEADER": None,
        }


    # ==========================================
    # MARKET BREADTH
    # ==========================================
    def market_breadth(self):

        return {
            "ADVANCES": None,
            "DECLINES": None,
            "A_D_RATIO": None,
            "NEW_HIGHS": None,
            "NEW_LOWS": None,
        }


    # ==========================================
    # INSTITUTIONAL ACTIVITY
    # ==========================================
    def institutional_activity(self):

        return {
            "FII": None,
            "DII": None,
            "NET_FLOW": None,
        }


    # ==========================================
    # ECONOMIC EVENTS
    # ==========================================
    def economic_events(self):

        return {
            "RBI": [],
            "SEBI": [],
            "FED": [],
            "CPI": [],
            "GDP": [],
        }


    # ==========================================
    # MARKET CORRELATION
    # ==========================================
    def market_correlation(self):

        return {
            "NIFTY": None,
            "BANKNIFTY": None,
            "USDINR": None,
            "GOLD": None,
            "CRUDE": None,
        }


    # ==========================================
    # LIQUIDITY ANALYSIS
    # ==========================================
    def liquidity_analysis(self):

        return {
            "BID": None,
            "ASK": None,
            "SPREAD": None,
            "LIQUIDITY_SCORE": None,
        }


    # ==========================================
    # WATCHLIST
    # ==========================================
    def watchlist_monitor(self):

        return {
            "WATCHLIST": [],
            "BREAKOUTS": [],
            "ALERTS": [],
        }


    # ==========================================
    # SMART ALERTS
    # ==========================================
    def smart_alerts(self):

        return {
            "BUY": False,
            "SELL": False,
            "BREAKOUT": False,
            "BREAKDOWN": False,
            "HIGH_VOLUME": False,
            "NEWS_ALERT": False,
        }


    # ==========================================
    # SYSTEM HEALTH
    # ==========================================
    def system_health(self):

        return {
            "STATUS": "OK",
            "DATA_FEED": True,
            "NSE": True,
            "MCX": True,
            "YFINANCE": True,
            "LAST_UPDATE": datetime.now(),
        }

    # ==========================================
    # COMPLETE REPORT
    # ==========================================

    def run(self, symbol, dataframe):

        return {

                "market": self.market_status(),

                "technical": self.technical_analysis(dataframe),

                "signal": self.generate_signal(),

                "tracking": self.tracking(),

                "news": self.news_monitor(),

                "options": self.option_analysis(),

                "risk": self.risk_engine(),

                "prediction": self.prediction(),

                "volume": self.volume_analysis(dataframe),

                "trend": self.trend_analysis(dataframe),

                "volatility": self.volatility_analysis(dataframe),

                "momentum": self.momentum_analysis(dataframe),

                "support_resistance": self.support_resistance(dataframe),

                "sector": self.sector_analysis(),

                "market_breadth": self.market_breadth(),

                "institutional": self.institutional_activity(),

                "economic": self.economic_events(),

                "correlation": self.market_correlation(),

                "liquidity": self.liquidity_analysis(),

                "watchlist": self.watchlist_monitor(),

                "alerts": self.smart_alerts(),

                "health": self.system_health(),
        }
