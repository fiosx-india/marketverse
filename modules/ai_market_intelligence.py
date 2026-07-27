"""
==========================================================
MarketVerse AI Market Intelligence Engine
Version : 1.0
==========================================================
"""

from dataclasses import dataclass
from datetime import datetime
from guardian.runtime_diagnostic import diagnostic

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
    def generate_signal(self, df):

        tech = self.technical_analysis(df)
        trend = self.trend_analysis(df)

        signal = "HOLD"
        confidence = 50
        sentiment = "NEUTRAL"
        risk = "MEDIUM"
        recommendation = "WAIT"

        try:

            rsi = tech.get("RSI")
            trend_name = trend.get("TREND")

            if (
                rsi is not None and
                trend_name == "STRONG_BULLISH" and
                rsi < 70
            ):
                signal = "BUY"
                confidence = 90
                sentiment = "BULLISH"
                risk = "LOW"
                recommendation = "BUY ON DIPS"

            elif (
                rsi is not None and
                trend_name == "STRONG_BEARISH"
            ):
                signal = "SELL"
                confidence = 90
                sentiment = "BEARISH"
                risk = "HIGH"
                recommendation = "EXIT OR SHORT"

        except Exception:
            pass

        return AISignal(
            signal=signal,
            confidence=confidence,
            sentiment=sentiment,
            risk=risk,
            recommendation=recommendation,
        )

    # ==========================================
    # SMART TRACKING
    # ==========================================
    def tracking(self, df):

        if df is None or len(df) < 20:
            return {
                "BREAKOUT": False,
                "BREAKDOWN": False,
                "GAPUP": False,
                "GAPDOWN": False,
                "HIGH_VOLUME": False,
                "UNUSUAL_MOVE": False,
            }

        try:
            current_close = float(df["Close"].iloc[-1])
            previous_close = float(df["Close"].iloc[-2])

            current_high = float(df["High"].iloc[-1])
            current_low = float(df["Low"].iloc[-1])

            previous_high = float(df["High"].iloc[-2])
            previous_low = float(df["Low"].iloc[-2])

            current_open = float(df["Open"].iloc[-1])

            current_volume = float(df["Volume"].iloc[-1])
            average_volume = float(
                df["Volume"].rolling(20).mean().iloc[-1]
            )

            breakout = current_close > previous_high
            breakdown = current_close < previous_low

            gapup = current_open > previous_high
            gapdown = current_open < previous_low

            high_volume = (
                current_volume > (average_volume * 2)
                if average_volume > 0
                else False
            )

            change_percent = abs(
                ((current_close - previous_close) / previous_close) * 100
            )

            unusual_move = change_percent >= 5

            return {
                "BREAKOUT": breakout,
                "BREAKDOWN": breakdown,
                "GAPUP": gapup,
                "GAPDOWN": gapdown,
                "HIGH_VOLUME": high_volume,
                "UNUSUAL_MOVE": unusual_move,
            }

        except Exception as e:
            return {
                "ERROR": str(e)
            }

    # ==========================================
    # NEWS AI
    # ==========================================
    def news_monitor(
            self,
            sebi=None,
            rbi=None,
            nse=None,
            mcx=None,
            company=None,
            global_news=None):

        sebi = sebi if sebi is not None else []
        rbi = rbi if rbi is not None else []
        nse = nse if nse is not None else []
        mcx = mcx if mcx is not None else []
        company = company if company is not None else []
        global_news = global_news if global_news is not None else []

        total_news = (
            len(sebi) +
            len(rbi) +
            len(nse) +
            len(mcx) +
            len(company) +
            len(global_news)
        )

        if total_news >= 20:
            sentiment = "HIGH_ACTIVITY"
        elif total_news >= 10:
            sentiment = "MODERATE_ACTIVITY"
        else:
            sentiment = "LOW_ACTIVITY"

        return {
            "SEBI": sebi,
            "RBI": rbi,
            "NSE": nse,
            "MCX": mcx,
            "COMPANY": company,
            "GLOBAL": global_news,
            "TOTAL_NEWS": total_news,
            "NEWS_STATUS": sentiment,
        }

    # ==========================================
    # OPTIONS AI
    # ==========================================
    def option_analysis(
            self,
            pcr=None,
            oi=None,
            max_pain=None,
            iv=None,
            gamma=None):

        sentiment = "NEUTRAL"

        if pcr is not None:
            if pcr > 1.2:
                sentiment = "BULLISH"
            elif pcr < 0.8:
                sentiment = "BEARISH"

        return {
            "PCR": pcr,
            "OI": oi,
            "MAX_PAIN": max_pain,
            "IV": iv,
            "GAMMA": gamma,
            "SENTIMENT": sentiment,
        }

    # ==========================================
    # RISK
    # ==========================================
    def risk_engine(self,
                    entry=None,
                    stoploss=None,
                    target=None,
                    capital=None,
                    risk_percent=1.0):

        if (
            entry is None or
            stoploss is None or
            target is None
        ):
            return {
                "STOPLOSS": stoploss,
                "TARGET": target,
                "RR_RATIO": None,
                "POSITION_SIZE": None,
                "RISK_AMOUNT": None,
            }

        risk = abs(entry - stoploss)
        reward = abs(target - entry)

        rr_ratio = round(
            reward / risk, 2
        ) if risk > 0 else None

        risk_amount = (
            capital * (risk_percent / 100)
            if capital is not None
            else None
        )

        position_size = (
            int(risk_amount / risk)
            if (
                risk_amount is not None and
                risk > 0
            )
            else None
        )

        return {
            "STOPLOSS": round(stoploss, 2),
            "TARGET": round(target, 2),
            "RR_RATIO": rr_ratio,
            "POSITION_SIZE": position_size,
            "RISK_AMOUNT": (
                round(risk_amount, 2)
                if risk_amount is not None
                else None
            ),
        }

    # ==========================================
    # PREDICTION
    # ==========================================
    def prediction(self, df):

        if df is None or len(df) < 20:
            return {
                "INTRADAY": None,
                "TOMORROW": None,
                "WEEKLY": None,
                "MONTHLY": None,
            }

        try:

            trend = self.trend_analysis(df)
            momentum = self.momentum_analysis(df)

            trend_name = trend.get("TREND")
            score = momentum.get("MOMENTUM_SCORE", 0)

            if trend_name == "STRONG_BULLISH" and score >= 70:
                signal = "BULLISH"
            elif trend_name == "STRONG_BEARISH":
                signal = "BEARISH"
            else:
                signal = "SIDEWAYS"

            return {
                "INTRADAY": signal,
                "TOMORROW": signal,
                "WEEKLY": signal,
                "MONTHLY": signal,
                "CONFIDENCE": score,
            }

        except Exception as e:
            return {
                "ERROR": str(e)
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
    def sector_analysis(self, symbol=None):

        sectors = {
            "RELIANCE": "ENERGY",
            "ONGC": "ENERGY",
            "IOC": "ENERGY",
            "SBIN": "BANKING",
            "HDFCBANK": "BANKING",
            "ICICIBANK": "BANKING",
            "AXISBANK": "BANKING",
            "INFY": "IT",
            "TCS": "IT",
            "WIPRO": "IT",
            "HCLTECH": "IT",
            "SUNPHARMA": "PHARMA",
            "DRREDDY": "PHARMA",
            "CIPLA": "PHARMA",
            "TATAMOTORS": "AUTO",
            "MARUTI": "AUTO",
            "M&M": "AUTO",
        }

        sector = sectors.get(
            symbol.upper(),
            "UNKNOWN"
        ) if symbol else "UNKNOWN"

        return {
            "SECTOR": sector,
            "SECTOR_STRENGTH": "NEUTRAL",
            "SECTOR_RANK": None,
            "LEADER": symbol if symbol else None,
        }

    # ==========================================
    # MARKET BREADTH
    # ==========================================
    def market_breadth(self, advances=None, declines=None,
                       new_highs=None, new_lows=None):

        advances = advances if advances is not None else 0
        declines = declines if declines is not None else 0
        new_highs = new_highs if new_highs is not None else 0
        new_lows = new_lows if new_lows is not None else 0

        ratio = (
            round(advances / declines, 2)
            if declines > 0
            else None
        )

        if ratio is None:
            status = "UNKNOWN"
        elif ratio >= 2:
            status = "STRONG_BULLISH"
        elif ratio >= 1:
            status = "BULLISH"
        elif ratio >= 0.5:
            status = "BEARISH"
        else:
            status = "STRONG_BEARISH"

        return {
            "ADVANCES": advances,
            "DECLINES": declines,
            "A_D_RATIO": ratio,
            "NEW_HIGHS": new_highs,
            "NEW_LOWS": new_lows,
            "MARKET_STATUS": status,
        }

    # ==========================================
    # INSTITUTIONAL ACTIVITY
    # ==========================================
    def institutional_activity(self, fii=None, dii=None):

        fii = fii if fii is not None else 0.0
        dii = dii if dii is not None else 0.0

        net_flow = fii + dii

        if net_flow > 1000:
            sentiment = "STRONG_BULLISH"
        elif net_flow > 0:
            sentiment = "BULLISH"
        elif net_flow < -1000:
            sentiment = "STRONG_BEARISH"
        elif net_flow < 0:
            sentiment = "BEARISH"
        else:
            sentiment = "NEUTRAL"

        return {
            "FII": round(fii, 2),
            "DII": round(dii, 2),
            "NET_FLOW": round(net_flow, 2),
            "SENTIMENT": sentiment,
        }

    # ==========================================
    # ECONOMIC EVENTS
    # ==========================================
    def economic_events(self,
                        rbi=None,
                        sebi=None,
                        fed=None,
                        cpi=None,
                        gdp=None):

        return {
            "RBI": rbi if rbi is not None else [],
            "SEBI": sebi if sebi is not None else [],
            "FED": fed if fed is not None else [],
            "CPI": cpi if cpi is not None else [],
            "GDP": gdp if gdp is not None else [],
            "EVENT_COUNT": (
                len(rbi if rbi else []) +
                len(sebi if sebi else []) +
                len(fed if fed else []) +
                len(cpi if cpi else []) +
                len(gdp if gdp else [])
            ),
        }

    # ==========================================
    # MARKET CORRELATION
    # ==========================================
    def market_correlation(
            self,
            nifty=None,
            banknifty=None,
            usdinr=None,
            gold=None,
            crude=None):

        return {
            "NIFTY": nifty,
            "BANKNIFTY": banknifty,
            "USDINR": usdinr,
            "GOLD": gold,
            "CRUDE": crude,
            "MARKET_SENTIMENT": (
                "BULLISH"
                if nifty is not None and nifty > 0
                else "BEARISH"
                if nifty is not None and nifty < 0
                else "NEUTRAL"
            ),
        }

    # ==========================================
    # LIQUIDITY ANALYSIS
    # ==========================================
    def liquidity_analysis(self, bid=None, ask=None):

        if bid is None or ask is None:
            return {
                "BID": bid,
                "ASK": ask,
                "SPREAD": None,
                "LIQUIDITY_SCORE": None,
                "STATUS": "UNKNOWN",
            }

        spread = ask - bid

        if spread <= 0.05:
            score = 100
            status = "EXCELLENT"
        elif spread <= 0.20:
            score = 80
            status = "GOOD"
        elif spread <= 0.50:
            score = 60
            status = "AVERAGE"
        else:
            score = 30
            status = "LOW"

        return {
            "BID": round(bid, 2),
            "ASK": round(ask, 2),
            "SPREAD": round(spread, 2),
            "LIQUIDITY_SCORE": score,
            "STATUS": status,
        }

    # ==========================================
    # WATCHLIST
    # ==========================================
    def watchlist_monitor(self,
                          watchlist=None,
                          breakouts=None,
                          alerts=None):

        watchlist = watchlist if watchlist is not None else []
        breakouts = breakouts if breakouts is not None else []
        alerts = alerts if alerts is not None else []

        return {
            "WATCHLIST": watchlist,
            "BREAKOUTS": breakouts,
            "ALERTS": alerts,
            "TOTAL_STOCKS": len(watchlist),
            "TOTAL_BREAKOUTS": len(breakouts),
            "TOTAL_ALERTS": len(alerts),
        }

    # ==========================================
    # SMART ALERTS
    # ==========================================
    def smart_alerts(
            self,
            buy=False,
            sell=False,
            breakout=False,
            breakdown=False,
            high_volume=False,
            news_alert=False):

        total_alerts = sum([
            buy,
            sell,
            breakout,
            breakdown,
            high_volume,
            news_alert
        ])

        if total_alerts >= 4:
            priority = "CRITICAL"
        elif total_alerts >= 2:
            priority = "HIGH"
        elif total_alerts == 1:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        return {
            "BUY": buy,
            "SELL": sell,
            "BREAKOUT": breakout,
            "BREAKDOWN": breakdown,
            "HIGH_VOLUME": high_volume,
            "NEWS_ALERT": news_alert,
            "TOTAL_ALERTS": total_alerts,
            "PRIORITY": priority,
        }

    # ==========================================
    # SYSTEM HEALTH
    # ==========================================
    def system_health(
            self,
            data_feed=True,
            nse=True,
            mcx=True,
            yfinance=True):

        services = [data_feed, nse, mcx, yfinance]
        healthy = sum(services)
        score = int((healthy / len(services)) * 100)

        if score == 100:
            status = "EXCELLENT"
        elif score >= 75:
            status = "GOOD"
        elif score >= 50:
            status = "WARNING"
        else:
            status = "CRITICAL"

        return {
            "STATUS": status,
            "HEALTH_SCORE": score,
            "DATA_FEED": data_feed,
            "NSE": nse,
            "MCX": mcx,
            "YFINANCE": yfinance,
            "LAST_UPDATE": datetime.now(),
        }

    # ==========================================
    # COMPLETE REPORT
    # ==========================================
    def run(self, symbol, dataframe):

        return {

            "market": self.market_status(),

            "technical": self.technical_analysis(dataframe),

            "signal": self.generate_signal(dataframe),

            "tracking": self.tracking(dataframe),

            "news": self.news_monitor(),

            "options": self.option_analysis(),

            "risk": self.risk_engine(),

            "prediction": self.prediction(dataframe),

            "volume": self.volume_analysis(dataframe),

            "trend": self.trend_analysis(dataframe),

            "volatility": self.volatility_analysis(dataframe),

            "momentum": self.momentum_analysis(dataframe),

            "support_resistance": self.support_resistance(dataframe),

            "sector": self.sector_analysis(symbol),

            "market_breadth": self.market_breadth(),

            "institutional": self.institutional_activity(),

            "economic": self.economic_events(),

            "correlation": self.market_correlation(),

            "liquidity": self.liquidity_analysis(),

            "watchlist": self.watchlist_monitor(),

            "alerts": self.smart_alerts(),

            "health": self.system_health(),
            
        }

        diagnostic.validate_signal(
                symbol=symbol,
                ai_signal=report["signal"].signal,
                news={
                    "sentiment": report["signal"].sentiment
                },
                technical={
                    "trend": report["trend"]["TREND"]
                },
                prediction={
                    "direction": report["prediction"]["TOMORROW"]
                },
                volume_alert=report["volume"]["VOLUME_SPIKE"]
            )

            return report


