"""
=========================================================
MarketVerse AI
Technical Analysis Engine
=========================================================

Purpose
-------
Provides reusable technical indicators for the
MarketVerse intelligence pipeline.

This module supports:

1. Symbol input
2. Raw OHLC DataFrame input
3. CentralBrain compatibility
4. AI Engine compatibility

The module performs technical analysis only.
It does not make the final market decision.

CentralBrain remains responsible for orchestration.
DecisionCore remains responsible for the final decision.
=========================================================
"""

import pandas as pd
import ta

from modules.market_data import get_market_data


# =========================================================
# INTERNAL DATA RESOLUTION
# =========================================================

def _resolve_dataframe(source):
    """
    Resolve either:

    - Symbol string
    - Pandas DataFrame

    into a valid OHLC DataFrame.
    """

    if isinstance(source, pd.DataFrame):
        return source.copy()

    if isinstance(source, str):
        return get_market_data(source)

    return None


# =========================================================
# CALCULATE INDICATORS
# =========================================================

def calculate_indicators(source):
    """
    Calculate professional technical indicators.

    Accepts:
    - Symbol
    - OHLC DataFrame

    Returns a standardized technical dictionary.
    """

    try:

        data = _resolve_dataframe(source)

        if data is None or data.empty:

            return {
                "error": "Market data unavailable"
            }

        required_columns = {
            "Close",
            "High",
            "Low",
            "Volume"
        }

        if not required_columns.issubset(data.columns):

            return {
                "error": "Required OHLC columns are missing"
            }

        if len(data) < 50:

            return {
                "error": "Not enough market data"
            }

        # -------------------------------------------------
        # Market Series
        # -------------------------------------------------

        close = data["Close"]
        high = data["High"]
        low = data["Low"]
        volume = data["Volume"]

        # -------------------------------------------------
        # Moving Averages
        # -------------------------------------------------

        sma20_series = ta.trend.SMAIndicator(
            close=close,
            window=20
        ).sma_indicator()

        sma50_series = ta.trend.SMAIndicator(
            close=close,
            window=50
        ).sma_indicator()

        ema20_series = ta.trend.EMAIndicator(
            close=close,
            window=20
        ).ema_indicator()

        ema50_series = ta.trend.EMAIndicator(
            close=close,
            window=50
        ).ema_indicator()

        # -------------------------------------------------
        # RSI
        # -------------------------------------------------

        rsi_series = ta.momentum.RSIIndicator(
            close=close,
            window=14
        ).rsi()

        # -------------------------------------------------
        # MACD
        # -------------------------------------------------

        macd_indicator = ta.trend.MACD(
            close=close
        )

        macd_series = macd_indicator.macd()

        macd_signal_series = (
            macd_indicator.macd_signal()
        )

        macd_histogram_series = (
            macd_indicator.macd_diff()
        )

        # -------------------------------------------------
        # Bollinger Bands
        # -------------------------------------------------

        bollinger = ta.volatility.BollingerBands(
            close=close
        )

        bb_upper = bollinger.bollinger_hband()

        bb_middle = bollinger.bollinger_mavg()

        bb_lower = bollinger.bollinger_lband()

        # -------------------------------------------------
        # ATR
        # -------------------------------------------------

        atr_series = ta.volatility.AverageTrueRange(
            high=high,
            low=low,
            close=close,
            window=14
        ).average_true_range()

        # -------------------------------------------------
        # ADX
        # -------------------------------------------------

        adx_series = ta.trend.ADXIndicator(
            high=high,
            low=low,
            close=close,
            window=14
        ).adx()

        # -------------------------------------------------
        # Latest Values
        # -------------------------------------------------

        latest_price = float(close.iloc[-1])

        sma20 = float(sma20_series.iloc[-1])
        sma50 = float(sma50_series.iloc[-1])

        ema20 = float(ema20_series.iloc[-1])
        ema50 = float(ema50_series.iloc[-1])

        rsi = float(rsi_series.iloc[-1])

        macd = float(macd_series.iloc[-1])
        macd_signal = float(
            macd_signal_series.iloc[-1]
        )

        macd_histogram = float(
            macd_histogram_series.iloc[-1]
        )

        atr = float(atr_series.iloc[-1])

        adx = float(adx_series.iloc[-1])

        # -------------------------------------------------
        # Support / Resistance
        # -------------------------------------------------

        support = float(
            low.tail(30).min()
        )

        resistance = float(
            high.tail(30).max()
        )

        # -------------------------------------------------
        # Volume Analysis
        # -------------------------------------------------

        latest_volume = int(
            volume.iloc[-1]
        )

        average_volume = int(
            volume.tail(20).mean()
        )

        if latest_volume > average_volume * 1.5:

            volume_strength = "HIGH"

        elif latest_volume < average_volume * 0.7:

            volume_strength = "LOW"

        else:

            volume_strength = "NORMAL"

        # -------------------------------------------------
        # Trend Detection
        # -------------------------------------------------

        if (
            latest_price > ema20
            and ema20 > ema50
        ):

            trend = "BULLISH"

        elif (
            latest_price < ema20
            and ema20 < ema50
        ):

            trend = "BEARISH"

        else:

            trend = "SIDEWAYS"

        # -------------------------------------------------
        # Technical Signal
        # -------------------------------------------------

        bullish_score = 0
        bearish_score = 0

        # EMA Structure

        if ema20 > ema50:
            bullish_score += 1

        elif ema20 < ema50:
            bearish_score += 1

        # Price Position

        if latest_price > ema20:
            bullish_score += 1

        elif latest_price < ema20:
            bearish_score += 1

        # MACD

        if macd > macd_signal:
            bullish_score += 1

        elif macd < macd_signal:
            bearish_score += 1

        # RSI

        if rsi < 30:
            bullish_score += 1

        elif rsi > 70:
            bearish_score += 1

        # -------------------------------------------------
        # Signal Result
        # -------------------------------------------------

        if bullish_score >= 3:

            signal = "BUY"

        elif bearish_score >= 3:

            signal = "SELL"

        else:

            signal = "HOLD"

        # -------------------------------------------------
        # Technical Confidence
        # -------------------------------------------------

        total_signals = (
            bullish_score
            + bearish_score
        )

        if total_signals == 0:

            confidence = 50

        else:

            dominant_score = max(
                bullish_score,
                bearish_score
            )

            confidence = min(
                50 + dominant_score * 12,
                90
            )

        # -------------------------------------------------
        # Return Standardized Result
        # -------------------------------------------------

        return {

            "status": "success",

            "price": round(
                latest_price,
                2
            ),

            # Moving Averages

            "sma20": round(
                sma20,
                2
            ),

            "sma50": round(
                sma50,
                2
            ),

            "ema20": round(
                ema20,
                2
            ),

            "ema50": round(
                ema50,
                2
            ),

            # Momentum

            "rsi": round(
                rsi,
                2
            ),

            "macd": round(
                macd,
                4
            ),

            "macd_signal": round(
                macd_signal,
                4
            ),

            "macd_histogram": round(
                macd_histogram,
                4
            ),

            # Bollinger Bands

            "bollinger_upper": round(
                float(bb_upper.iloc[-1]),
                2
            ),

            "bollinger_middle": round(
                float(bb_middle.iloc[-1]),
                2
            ),

            "bollinger_lower": round(
                float(bb_lower.iloc[-1]),
                2
            ),

            # Volatility

            "atr": round(
                atr,
                2
            ),

            # Trend Strength

            "adx": round(
                adx,
                2
            ),

            # Support Resistance

            "support": round(
                support,
                2
            ),

            "resistance": round(
                resistance,
                2
            ),

            # Volume

            "volume": latest_volume,

            "average_volume": average_volume,

            "volume_strength": volume_strength,

            # Intelligence Output

            "trend": trend,

            "signal": signal,

            "confidence": confidence,

            "bullish_score": bullish_score,

            "bearish_score": bearish_score

        }

    except Exception as error:

        return {

            "status": "error",

            "error": str(error)

        }


# =========================================================
# DATAFRAME TECHNICAL ANALYSIS
# =========================================================

def analyze_technical(df):
    """
    Backward-compatible DataFrame analysis.

    Delegates to the standardized indicator engine.
    """

    return calculate_indicators(df)


# =========================================================
# CENTRAL BRAIN COMPATIBILITY
# =========================================================

def technical_analysis(source):
    """
    CentralBrain Technical Analysis Interface.

    Accepts:
    - Symbol
    - DataFrame

    Returns standardized technical evidence.
    """

    return calculate_indicators(source)
