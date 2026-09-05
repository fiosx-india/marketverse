"""
=========================================================
MarketVerse AI
Prediction Engine
=========================================================

Purpose
-------
Generates prediction evidence from intelligence evidence
already collected by CentralBrain.

Prediction Engine combines multiple intelligence signals
into one probability-based market prediction.

Responsibilities
----------------
- Evaluate technical evidence
- Evaluate market structure evidence
- Evaluate sentiment evidence
- Evaluate news evidence
- Evaluate pattern evidence
- Evaluate volume evidence
- Evaluate market event evidence
- Estimate confidence
- Estimate directional probability
- Generate supporting evidence
- Generate conflicting evidence

This module DOES NOT:
- Orchestrate the pipeline
- Fetch market data during CentralBrain flow
- Generate strategy
- Calculate risk
- Make the final market decision

Architecture
------------

CentralBrain
    │
    ▼
Shared MarketContext
    │
    ├── Technical
    ├── News Analysis
    ├── Sentiment
    ├── Pattern
    ├── Volume
    ├── Events
    └── Market Intelligence
            │
            ▼
      Prediction Engine
            │
            ▼
    Prediction Evidence
            │
            ▼
      MarketContext
=========================================================
"""

import pandas as pd

from modules.market_data import get_market_data
from modules.technical import technical_analysis


# =========================================================
# SAFE HELPERS
# =========================================================

def _safe_dict(value):
    """Return dictionary safely."""

    if isinstance(value, dict):
        return value

    return {}


def _safe_float(value, default=0.0):
    """Safely convert values to float."""

    try:

        if value is None:

            return default

        if pd.isna(value):

            return default

        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return default


def _normalize_signal(value):
    """
    Normalize supported signals.

    Returns:
        BUY / SELL / HOLD
    """

    if value is None:

        return "HOLD"

    value = str(value).upper()

    if value in (
        "BUY",
        "STRONG BUY",
        "BULLISH",
        "VERY BULLISH",
        "POSITIVE",
        "UP"
    ):

        return "BUY"

    if value in (
        "SELL",
        "STRONG SELL",
        "BEARISH",
        "VERY BEARISH",
        "NEGATIVE",
        "DOWN"
    ):

        return "SELL"

    return "HOLD"


# =========================================================
# UNKNOWN PREDICTION
# =========================================================

def _unknown_prediction(message):
    """Return safe prediction result."""

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

        "reason": [

            message

        ]

    }


# =========================================================
# ADD SIGNAL EVIDENCE
# =========================================================

def _add_signal_evidence(
    signal,
    weight,
    bullish_score,
    bearish_score,
    supporting_evidence,
    conflicting_evidence,
    bullish_reason,
    bearish_reason
):
    """
    Add normalized directional evidence.
    """

    normalized = _normalize_signal(
        signal
    )

    if normalized == "BUY":

        bullish_score += weight

        supporting_evidence.append(
            bullish_reason
        )

    elif normalized == "SELL":

        bearish_score += weight

        conflicting_evidence.append(
            bearish_reason
        )

    return (

        bullish_score,

        bearish_score

    )


# =========================================================
# CORE PREDICTION ENGINE
# =========================================================

def get_prediction(
    symbol=None,
    data=None
):
    """
    Generate prediction evidence.

    Expected structured data:

    {
        "market": {},
        "indicators": {},
        "sentiment": {},
        "news_analysis": {},
        "pattern": {},
        "volume": {},
        "events": {},
        "ai_market_intelligence": {}
    }
    """

    data = data or {}

    indicators = _safe_dict(

        data.get(
            "indicators"
        )

    )

    market = data.get(
        "market"
    )

    sentiment = _safe_dict(

        data.get(
            "sentiment"
        )

    )

    news_analysis = _safe_dict(

        data.get(
            "news_analysis"
        )

    )

    pattern = _safe_dict(

        data.get(
            "pattern"
        )

    )

    volume = _safe_dict(

        data.get(
            "volume"
        )

    )

    events = _safe_dict(

        data.get(
            "events"
        )

    )

    ai_market_intelligence = _safe_dict(

        data.get(
            "ai_market_intelligence"
        )

    )

    # =====================================================
    # PRICE RESOLUTION
    # =====================================================

    price = 0.0

    if isinstance(
        market,
        pd.DataFrame
    ):

        if market.empty:

            return _unknown_prediction(

                "Market data unavailable"

            )

        try:

            price = _safe_float(

                market[
                    "Close"
                ].iloc[-1]

            )

        except Exception:

            price = 0.0

    elif isinstance(
        market,
        dict
    ):

        price = _safe_float(

            market.get(
                "price",

                market.get(
                    "close",

                    0

                )

            )

        )

    if price <= 0:

        price = _safe_float(

            indicators.get(
                "price",
                0
            )

        )

    # =====================================================
    # TECHNICAL INDICATORS
    # =====================================================

    rsi = _safe_float(

        indicators.get(
            "rsi",
            50
        ),

        50

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

    # =====================================================
    # EVIDENCE INITIALIZATION
    # =====================================================

    bullish_score = 0

    bearish_score = 0

    supporting_evidence = []

    conflicting_evidence = []

    # =====================================================
    # TECHNICAL SIGNAL
    # =====================================================

    technical_signal = _normalize_signal(

        indicators.get(
            "signal"
        )

    )

    (
        bullish_score,
        bearish_score

    ) = _add_signal_evidence(

        technical_signal,

        2,

        bullish_score,

        bearish_score,

        supporting_evidence,

        conflicting_evidence,

        "Technical analysis supports bullish movement",

        "Technical analysis supports bearish movement"

    )

    # =====================================================
    # EMA TREND
    # =====================================================

    if ema20 > 0 and ema50 > 0:

        if ema20 > ema50:

            bullish_score += 2

            supporting_evidence.append(

                "EMA20 is above EMA50"

            )

        elif ema20 < ema50:

            bearish_score += 2

            conflicting_evidence.append(

                "EMA20 is below EMA50"

            )

    # =====================================================
    # PRICE VS EMA20
    # =====================================================

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

    # =====================================================
    # MACD
    # =====================================================

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

    # =====================================================
    # RSI
    # =====================================================

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

    # =====================================================
    # SENTIMENT EVIDENCE
    # =====================================================

    sentiment_signal = _normalize_signal(

        sentiment.get(

            "signal",

            sentiment.get(
                "sentiment"
            )

        )

    )

    (
        bullish_score,
        bearish_score

    ) = _add_signal_evidence(

        sentiment_signal,

        2,

        bullish_score,

        bearish_score,

        supporting_evidence,

        conflicting_evidence,

        "Market sentiment is bullish",

        "Market sentiment is bearish"

    )

    # =====================================================
    # NEWS EVIDENCE
    # =====================================================

    news_signal = _normalize_signal(

        news_analysis.get(
            "sentiment"
        )

    )

    (
        bullish_score,
        bearish_score

    ) = _add_signal_evidence(

        news_signal,

        2,

        bullish_score,

        bearish_score,

        supporting_evidence,

        conflicting_evidence,

        "News analysis is positive",

        "News analysis is negative"

    )

    # =====================================================
    # PATTERN EVIDENCE
    # =====================================================

    if pattern.get(
        "bullish"
    ):

        bullish_score += 2

        supporting_evidence.append(

            "Bullish market pattern detected"

        )

    if pattern.get(
        "bearish"
    ):

        bearish_score += 2

        conflicting_evidence.append(

            "Bearish market pattern detected"

        )

    # =====================================================
    # VOLUME EVIDENCE
    # =====================================================

    volume_signal = _normalize_signal(

        volume.get(
            "signal"
        )

    )

    (
        bullish_score,
        bearish_score

    ) = _add_signal_evidence(

        volume_signal,

        1,

        bullish_score,

        bearish_score,

        supporting_evidence,

        conflicting_evidence,

        "Volume supports bullish movement",

        "Volume supports bearish movement"

    )

    # =====================================================
    # MARKET EVENT EVIDENCE
    # =====================================================

    event_signal = _normalize_signal(

        events.get(

            "signal",

            events.get(
                "sentiment"
            )

        )

    )

    (
        bullish_score,
        bearish_score

    ) = _add_signal_evidence(

        event_signal,

        2,

        bullish_score,

        bearish_score,

        supporting_evidence,

        conflicting_evidence,

        "Market events support bullish conditions",

        "Market events indicate bearish risk"

    )

    # =====================================================
    # AI MARKET INTELLIGENCE
    # =====================================================

    intelligence_signal = _normalize_signal(

        ai_market_intelligence.get(

            "signal",

            ai_market_intelligence.get(
                "prediction"
            )

        )

    )

    (
        bullish_score,
        bearish_score

    ) = _add_signal_evidence(

        intelligence_signal,

        2,

        bullish_score,

        bearish_score,

        supporting_evidence,

        conflicting_evidence,

        "Market intelligence supports bullish conditions",

        "Market intelligence supports bearish conditions"

    )

    # =====================================================
    # SIGNAL CLASSIFICATION
    # =====================================================

    difference = (

        bullish_score
        -
        bearish_score

    )

    total_directional_evidence = (

        bullish_score
        +
        bearish_score

    )

    if total_directional_evidence == 0:

        signal = "HOLD"

    elif bullish_score >= bearish_score + 4:

        signal = "STRONG BUY"

    elif bullish_score > bearish_score:

        signal = "BUY"

    elif bearish_score >= bullish_score + 4:

        signal = "STRONG SELL"

    elif bearish_score > bullish_score:

        signal = "SELL"

    else:

        signal = "HOLD"

    # =====================================================
    # CONFIDENCE
    # =====================================================

    if total_directional_evidence == 0:

        confidence = 0

    else:

        dominance = abs(
            difference
        )

        dominance_ratio = (

            dominance
            /
            total_directional_evidence

        )

        evidence_strength = min(

            total_directional_evidence
            *
            5,

            30

        )

        confidence = (

            50
            +
            dominance_ratio * 30
            +
            evidence_strength

        )

        confidence = min(

            confidence,

            95

        )

    confidence = round(

        confidence,

        2

    )

    # =====================================================
    # PROBABILITY
    # =====================================================

    if total_directional_evidence == 0:

        probability = 0.5

    else:

        probability = round(

            max(
                bullish_score,
                bearish_score
            )

            /

            total_directional_evidence,

            2

        )

    # =====================================================
    # DEFAULT EVIDENCE
    # =====================================================

    if not supporting_evidence:

        supporting_evidence.append(

            "No strong bullish evidence detected"

        )

    if not conflicting_evidence:

        conflicting_evidence.append(

            "No strong bearish evidence detected"

        )

    # =====================================================
    # FINAL RESULT
    # =====================================================

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

        "supporting_evidence":
            supporting_evidence,

        "conflicting_evidence":
            conflicting_evidence,

        "reason":
            supporting_evidence
            +
            conflicting_evidence

    }


# =========================================================
# DATAFRAME COMPATIBILITY
# =========================================================

def predict_market(df):
    """
    Backward-compatible DataFrame interface.
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

    technical = technical_analysis(
        df
    )

    if not isinstance(
        technical,
        dict
    ):

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
# LEGACY SYMBOL COMPATIBILITY
# =========================================================

def _predict_from_symbol(symbol):
    """
    Legacy compatibility path.

    This path is only for external callers that still
    provide a symbol.
    """

    dataframe = get_market_data(
        symbol
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

        symbol=symbol,

        data={

            "market": dataframe,

            "indicators": technical

        }

    )


# =========================================================
# CENTRAL BRAIN INTERFACE
# =========================================================

def predict_price(source=None):
    """
    Prediction interface.

    Supports:

    1. Shared MarketContext dictionary
    2. Raw DataFrame
    3. Symbol string for backward compatibility

    Preferred CentralBrain usage:

        predict_price(context.get())
    """

    # =====================================================
    # SHARED CONTEXT MODE
    # =====================================================

    if isinstance(
        source,
        dict
    ):

        technical = _safe_dict(

            source.get(
                "technical"
            )

        )

        market_data = source.get(
            "market_data"
        )

        sentiment = _safe_dict(

            source.get(
                "sentiment"
            )

        )

        news_analysis = _safe_dict(

            source.get(
                "news_analysis"
            )

        )

        pattern = _safe_dict(

            source.get(
                "pattern"
            )

        )

        volume = _safe_dict(

            source.get(
                "volume"
            )

        )

        events = _safe_dict(

            source.get(
                "events"
            )

        )

        ai_market_intelligence = _safe_dict(

            source.get(
                "ai_market_intelligence"
            )

        )

        # =================================================
        # MARKET DATA RESOLUTION
        # =================================================

        market = {}

        if isinstance(
            market_data,
            pd.DataFrame
        ):

            market = market_data

        elif isinstance(
            market_data,
            dict
        ):

            market = market_data

        elif technical:

            market = {

                "price":

                    technical.get(
                        "price",
                        0
                    )

            }

        return get_prediction(

            symbol=source.get(
                "symbol"
            ),

            data={

                "market": market,

                "indicators": technical,

                "sentiment": sentiment,

                "news_analysis": news_analysis,

                "pattern": pattern,

                "volume": volume,

                "events": events,

                "ai_market_intelligence":

                    ai_market_intelligence

            }

        )

    # =====================================================
    # DATAFRAME MODE
    # =====================================================

    if isinstance(
        source,
        pd.DataFrame
    ):

        return predict_market(
            source
        )

    # =====================================================
    # SYMBOL MODE
    # =====================================================

    if isinstance(
        source,
        str
    ):

        return _predict_from_symbol(
            source
        )

    # =====================================================
    # NO INPUT
    # =====================================================

    return _unknown_prediction(

        "Prediction input unavailable"

    )
