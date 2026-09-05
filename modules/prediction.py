"""
=========================================================
MarketVerse AI
Prediction Engine
=========================================================

Purpose
-------
Generates prediction evidence from market and technical
analysis.

Responsibilities
----------------
- Market direction estimation
- Bullish / bearish evidence evaluation
- Prediction confidence estimation
- Supporting reasons
- Conflicting evidence

This module does NOT:
- Calculate trade risk
- Generate strategy
- Make the final market decision

Architecture
------------
CentralBrain
    ↓
Market Data / Technical Evidence
    ↓
Prediction Engine
    ↓
Prediction Evidence
    ↓
Strategy / Risk / DecisionCore
=========================================================
"""

import pandas as pd

from modules.market_data import get_market_data
from modules.technical import technical_analysis


# =========================================================
# HELPER
# =========================================================

def _safe_float(value, default=0.0):
    """
    Safely convert values to float.
    """

    try:
        if pd.isna(value):
            return default

        return float(value)

    except (TypeError, ValueError):
        return default


# =========================================================
# CORE PREDICTION
# =========================================================

def get_prediction(symbol=None, data=None):
    """
    Generate prediction evidence.

    Supports structured market intelligence input:

    {
        "market": {...},
        "indicators": {...},
        "news": {...}
    }

    Returns a standardized prediction result.
    """

    data = data or {}

    indicators = data.get(
        "indicators",
        {}
    ) or {}

    market = data.get(
        "market",
        {}
    )

    # -----------------------------------------------------
    # DataFrame Compatibility
    # -----------------------------------------------------

    if isinstance(market, pd.DataFrame):

        if market.empty:

            return _unknown_prediction(
                "Market data unavailable"
            )

        try:

            price = _safe_float(
                market["Close"].iloc[-1]
            )

        except Exception:

            return _unknown_prediction(
                "Close price unavailable"
            )

    elif isinstance(market, dict):

        price = _safe_float(
            market.get("price", 0)
        )

    else:

        price = 0

    # -----------------------------------------------------
    # Indicator Values
    # -----------------------------------------------------

    rsi = _safe_float(
        indicators.get(
            "rsi",
            50
        ),
        50
    )

    sma20 = _safe_float(
        indicators.get(
            "sma20",
            0
        )
    )

    ema20 = _safe_float(
        indicators.get(
            "ema20",
            0
        )
    )

    ema50 = _safe_float(
        indicators.get(
            "ema50",
            0
        )
    )

    macd = _safe_float(
        indicators.get(
            "macd",
            0
        )
    )

    macd_signal = _safe_float(
        indicators.get(
            "macd_signal",
            0
        )
    )

    # -----------------------------------------------------
    # Evidence
    # -----------------------------------------------------

    bullish_score = 0
    bearish_score = 0

    supporting_evidence = []
    conflicting_evidence = []

    # -----------------------------------------------------
    # EMA Trend
    # -----------------------------------------------------

    if ema20 > 0 and ema50 > 0:

        if ema20 > ema50:

            bullish_score += 1

            supporting_evidence.append(
                "EMA20 is above EMA50"
            )

        elif ema20 < ema50:

            bearish_score += 1

            conflicting_evidence.append(
                "EMA20 is below EMA50"
            )

    # -----------------------------------------------------
    # Price vs EMA20
    # -----------------------------------------------------

    if price > 0 and ema20 > 0:

        if price > ema20:

            bullish_score += 1

            supporting_evidence.append(
                "Price is above EMA20"
            )

        elif price < ema20:

            bearish_score += 1

            conflicting_evidence.append(
                "Price is below EMA20"
            )

    # -----------------------------------------------------
    # MACD Momentum
    # -----------------------------------------------------

    if macd > macd_signal:

        bullish_score += 1

        supporting_evidence.append(
            "MACD momentum is bullish"
        )

    elif macd < macd_signal:

        bearish_score += 1

        conflicting_evidence.append(
            "MACD momentum is bearish"
        )

    # -----------------------------------------------------
    # RSI
    # -----------------------------------------------------

    if rsi < 30:

        bullish_score += 1

        supporting_evidence.append(
            "RSI indicates oversold conditions"
        )

    elif rsi > 70:

        bearish_score += 1

        conflicting_evidence.append(
            "RSI indicates overbought conditions"
        )

    elif 45 <= rsi <= 60:

        supporting_evidence.append(
            "RSI is neutral"
        )

    # -----------------------------------------------------
    # Signal Classification
    # -----------------------------------------------------

    difference = (
        bullish_score -
        bearish_score
    )

    if bullish_score >= 3:

        signal = "STRONG BUY"

    elif difference >= 1:

        signal = "BUY"

    elif bearish_score >= 3:

        signal = "STRONG SELL"

    elif difference <= -1:

        signal = "SELL"

    else:

        signal = "HOLD"

    # -----------------------------------------------------
    # Confidence
    # -----------------------------------------------------

    total_evidence = (
        bullish_score +
        bearish_score
    )

    if total_evidence == 0:

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

    # -----------------------------------------------------
    # Probability
    # -----------------------------------------------------

    probability = round(
        confidence / 100,
        2
    )

    # -----------------------------------------------------
    # Default Reasons
    # -----------------------------------------------------

    if not supporting_evidence:

        supporting_evidence.append(
            "No strong bullish evidence detected"
        )

    if not conflicting_evidence:

        conflicting_evidence.append(
            "No strong bearish evidence detected"
        )

    # -----------------------------------------------------
    # Result
    # -----------------------------------------------------

    return {

        "status": "success",

        "symbol": symbol,

        "signal": signal,

        "confidence": confidence,

        "probability": probability,

        "price": round(
            price,
            2
        ),

        "bullish_score": bullish_score,

        "bearish_score": bearish_score,

        "supporting_evidence": (
            supporting_evidence
        ),

        "conflicting_evidence": (
            conflicting_evidence
        ),

        # Backward Compatibility

        "reason": (
            supporting_evidence +
            conflicting_evidence
        )

    }


# =========================================================
# UNKNOWN PREDICTION
# =========================================================

def _unknown_prediction(message):
    """
    Return a safe prediction result.
    """

    return {

        "status": "unavailable",

        "signal": "HOLD",

        "confidence": 0,

        "probability": 0.0,

        "price": 0,

        "bullish_score": 0,

        "bearish_score": 0,

        "supporting_evidence": [],

        "conflicting_evidence": [],

        "reason": [message]

    }


# =========================================================
# DATAFRAME COMPATIBILITY
# =========================================================

def predict_market(df):
    """
    Compatibility interface for DataFrame callers.

    Performs technical analysis first and then
    generates prediction evidence.
    """

    if not isinstance(
        df,
        pd.DataFrame
    ):

        return _unknown_prediction(
            "Invalid market DataFrame"
        )

    if df.empty:

        return _unknown_prediction(
            "Market DataFrame is empty"
        )

    technical = technical_analysis(df)

    if technical.get(
        "status"
    ) == "error":

        return _unknown_prediction(
            "Technical analysis failed"
        )

    return get_prediction(

        data={

            "market": df,

            "indicators": technical

        }

    )


# =========================================================
# CENTRAL BRAIN INTERFACE
# =========================================================

def predict_price(source=None):
    """
    Prediction interface for CentralBrain.

    Supports:

    1. Symbol string
    2. OHLC DataFrame

    Example:

        predict_price("RELIANCE.NS")

        predict_price(dataframe)
    """

    # -----------------------------------------------------
    # SYMBOL MODE
    # -----------------------------------------------------

    if isinstance(
        source,
        str
    ):

        dataframe = get_market_data(
            source
        )

        if (
            dataframe is None
            or dataframe.empty
        ):

            return _unknown_prediction(
                "Market data unavailable"
            )

        technical = technical_analysis(
            dataframe
        )

        return get_prediction(

            symbol=source,

            data={

                "market": dataframe,

                "indicators": technical

            }

        )

    # -----------------------------------------------------
    # DATAFRAME MODE
    # -----------------------------------------------------

    if isinstance(
        source,
        pd.DataFrame
    ):

        return predict_market(
            source
        )

    # -----------------------------------------------------
    # NO INPUT
    # -----------------------------------------------------

    return _unknown_prediction(
        "Prediction input unavailable"
    )
