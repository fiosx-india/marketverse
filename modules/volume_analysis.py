"""
=========================================================
MarketVerse AI
Volume Analysis Engine
=========================================================

Purpose
-------
Provides reusable volume intelligence for the
MarketVerse AI intelligence pipeline.

Responsibilities
----------------
- Analyze current trading volume
- Calculate average volume
- Calculate relative volume
- Detect volume spikes
- Estimate buying pressure
- Estimate selling pressure
- Detect volume trend
- Produce volume evidence

This module DOES NOT:
- Fetch final market decisions
- Generate trading strategies
- Calculate risk
- Make the final BUY / SELL decision
- Orchestrate the intelligence pipeline

Architecture
------------

Market Data
    │
    ▼
Volume Analysis Engine
    │
    ▼
Volume Evidence
    │
    ▼
Shared MarketContext
    │
    ▼
Prediction / Strategy / DecisionCore

CentralBrain remains responsible for orchestration.

Author : MarketVerse AI
Version : 2.0
=========================================================
"""

import pandas as pd

from modules.market_data import get_market_data


# =========================================================
# SAFE RESULT
# =========================================================

def _empty_result(
    status="success",
    error=None
):
    """
    Return a consistent empty volume result.

    This preserves a stable output structure for
    CentralBrain and MarketContext.
    """

    result = {

        "status": status,

        "current_volume": 0,

        "average_volume": 0,

        "relative_volume": 0,

        "volume_trend": "UNKNOWN",

        "volume_spike": False,

        "buy_pressure": 50,

        "sell_pressure": 50,

        "signal": "HOLD",

        "strength": "WEAK",

        "score": 0,

        "bullish_score": 0,

        "bearish_score": 0,

        "confidence": 0
    }

    if error:

        result["error"] = error

    return result


# =========================================================
# DATA RESOLUTION
# =========================================================

def _resolve_dataframe(source):
    """
    Resolve input into a Pandas DataFrame.

    Supports:
    - Symbol string
    - Pandas DataFrame
    """

    if isinstance(
        source,
        pd.DataFrame
    ):

        return source.copy()

    if isinstance(
        source,
        str
    ):

        return get_market_data(
            source
        )

    return None


# =========================================================
# INPUT VALIDATION
# =========================================================

def _validate_dataframe(data):
    """
    Validate required market data columns.
    """

    if (
        data is None
        or not isinstance(
            data,
            pd.DataFrame
        )
        or data.empty
    ):

        return False, (
            "Market data unavailable"
        )

    required_columns = {

        "Open",

        "Close",

        "Volume"
    }

    if not required_columns.issubset(
        data.columns
    ):

        return False, (
            "Required volume columns are missing"
        )

    if len(data) < 20:

        return False, (
            "Not enough market data for volume analysis"
        )

    return True, None


# =========================================================
# VOLUME ANALYSIS
# =========================================================

def analyze_volume(source):
    """
    Analyze market volume intelligence.

    Accepts:
    - Symbol
    - OHLC Pandas DataFrame

    Returns standardized volume evidence.
    """

    try:

        # =================================================
        # RESOLVE DATA
        # =================================================

        data = _resolve_dataframe(
            source
        )

        # =================================================
        # VALIDATE DATA
        # =================================================

        valid, error = _validate_dataframe(
            data
        )

        if not valid:

            return _empty_result(

                status="error",

                error=error
            )

        # =================================================
        # SERIES
        # =================================================

        volume = data["Volume"]

        close = data["Close"]

        open_price = data["Open"]

        # =================================================
        # CURRENT VOLUME
        # =================================================

        current_volume = float(

            volume.iloc[-1]

        )

        # =================================================
        # AVERAGE VOLUME
        # =================================================

        average_volume = float(

            volume.tail(20).mean()

        )

        # =================================================
        # RELATIVE VOLUME
        # =================================================

        if average_volume > 0:

            relative_volume = (

                current_volume
                /
                average_volume

            )

        else:

            relative_volume = 0

        # =================================================
        # VOLUME TREND
        # =================================================

        recent_average = float(

            volume.tail(5).mean()

        )

        previous_average = float(

            volume.tail(20).head(15).mean()

        )

        if previous_average <= 0:

            volume_trend = "UNKNOWN"

        elif recent_average > (

            previous_average * 1.10

        ):

            volume_trend = "RISING"

        elif recent_average < (

            previous_average * 0.90

        ):

            volume_trend = "FALLING"

        else:

            volume_trend = "STABLE"

        # =================================================
        # VOLUME SPIKE
        # =================================================

        volume_spike = bool(

            relative_volume >= 1.5

        )

        # =================================================
        # BUY / SELL PRESSURE
        # =================================================

        latest_close = float(

            close.iloc[-1]

        )

        latest_open = float(

            open_price.iloc[-1]

        )

        buy_pressure = 50

        sell_pressure = 50

        # -------------------------------------------------
        # PRICE DIRECTION
        # -------------------------------------------------

        if latest_close > latest_open:

            buy_pressure += 25

            sell_pressure -= 25

        elif latest_close < latest_open:

            sell_pressure += 25

            buy_pressure -= 25

        # -------------------------------------------------
        # VOLUME CONFIRMATION
        # -------------------------------------------------

        if relative_volume >= 1.5:

            if latest_close > latest_open:

                buy_pressure += 15

                sell_pressure -= 15

            elif latest_close < latest_open:

                sell_pressure += 15

                buy_pressure -= 15

        # -------------------------------------------------
        # LIMIT VALUES
        # -------------------------------------------------

        buy_pressure = max(

            0,

            min(
                100,
                buy_pressure
            )

        )

        sell_pressure = max(

            0,

            min(
                100,
                sell_pressure
            )

        )

        # =================================================
        # BULLISH / BEARISH EVIDENCE
        # =================================================

        bullish_score = 0

        bearish_score = 0

        # -------------------------------------------------
        # BUY PRESSURE
        # -------------------------------------------------

        if buy_pressure >= 65:

            bullish_score += 1

        elif sell_pressure >= 65:

            bearish_score += 1

        # -------------------------------------------------
        # RELATIVE VOLUME
        # -------------------------------------------------

        if relative_volume >= 1.5:

            if latest_close > latest_open:

                bullish_score += 1

            elif latest_close < latest_open:

                bearish_score += 1

        # -------------------------------------------------
        # VOLUME TREND
        # -------------------------------------------------

        if volume_trend == "RISING":

            if latest_close > latest_open:

                bullish_score += 1

            elif latest_close < latest_open:

                bearish_score += 1

        # =================================================
        # VOLUME SIGNAL
        # =================================================

        if bullish_score >= 2:

            signal = "BUY"

        elif bearish_score >= 2:

            signal = "SELL"

        else:

            signal = "HOLD"

        # =================================================
        # VOLUME SCORE
        # =================================================

        score = 50

        # -------------------------------------------------
        # PRESSURE
        # -------------------------------------------------

        pressure_difference = (

            buy_pressure
            -
            sell_pressure

        )

        score += int(

            pressure_difference
            *
            0.30

        )

        # -------------------------------------------------
        # RELATIVE VOLUME
        # -------------------------------------------------

        if relative_volume >= 2:

            score += 20

        elif relative_volume >= 1.5:

            score += 10

        elif relative_volume < 0.7:

            score -= 10

        # -------------------------------------------------
        # CLAMP SCORE
        # -------------------------------------------------

        score = max(

            0,

            min(
                100,
                score
            )

        )

        # =================================================
        # VOLUME STRENGTH
        # =================================================

        if score >= 80:

            strength = "VERY STRONG"

        elif score >= 65:

            strength = "STRONG"

        elif score >= 45:

            strength = "MEDIUM"

        else:

            strength = "WEAK"

        # =================================================
        # CONFIDENCE
        # =================================================

        evidence_count = (

            bullish_score
            +
            bearish_score

        )

        if evidence_count == 0:

            confidence = 40

        else:

            dominant_score = max(

                bullish_score,

                bearish_score

            )

            conflicting_score = min(

                bullish_score,

                bearish_score

            )

            confidence = (

                45
                +
                dominant_score * 15
                -
                conflicting_score * 8

            )

            confidence = max(

                0,

                min(
                    90,
                    confidence
                )

            )

        # =================================================
        # RETURN STANDARDIZED EVIDENCE
        # =================================================

        return {

            "status": "success",

            "current_volume": round(

                current_volume,
                2

            ),

            "average_volume": round(

                average_volume,
                2

            ),

            "relative_volume": round(

                relative_volume,
                2

            ),

            "volume_trend": volume_trend,

            "volume_spike": volume_spike,

            "buy_pressure": round(

                buy_pressure,
                2

            ),

            "sell_pressure": round(

                sell_pressure,
                2

            ),

            "signal": signal,

            "strength": strength,

            "score": score,

            "bullish_score": bullish_score,

            "bearish_score": bearish_score,

            "confidence": round(

                confidence,
                2

            )

        }

    except Exception as error:

        return _empty_result(

            status="error",

            error=str(error)
        )


# =========================================================
# CENTRAL BRAIN COMPATIBILITY
# =========================================================

def volume_analysis(source=None):
    """
    CentralBrain Volume Analysis Interface.

    Supports:
    - Symbol
    - Pandas DataFrame

    Returns standardized volume evidence.
    """

    if source is None:

        return _empty_result(

            status="error",

            error=(
                "Volume analysis source unavailable"
            )
        )

    return analyze_volume(
        source
    )
