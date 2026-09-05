"""
=========================================================
MarketVerse AI
Pattern Detection Engine
=========================================================

Purpose
-------
Provides chart pattern evidence for the MarketVerse AI
intelligence pipeline.

Responsibilities
----------------
- Detect Double Top patterns
- Detect Double Bottom patterns
- Detect Breakouts
- Detect Breakdowns
- Produce bullish evidence
- Produce bearish evidence
- Calculate pattern confidence
- Return standardized pattern intelligence

This module DOES NOT:
- Fetch final market decisions
- Generate trading strategies
- Calculate risk
- Execute trades
- Orchestrate the intelligence pipeline

Architecture
------------

Market Data
    │
    ▼
Pattern Detection Engine
    │
    ▼
Pattern Evidence
    │
    ▼
Shared MarketContext
    │
    ▼
CentralBrain
    │
    ▼
DecisionCore

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
    Return a stable pattern result structure.
    """

    result = {

        "status": status,

        "pattern": "NONE",

        "signal": "HOLD",

        "strength": "LOW",

        "score": 50,

        "bullish": False,

        "bearish": False,

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
# DATA VALIDATION
# =========================================================

def _validate_dataframe(data):
    """
    Validate required OHLC data.
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

        "High",

        "Low",

        "Close"
    }

    if not required_columns.issubset(
        data.columns
    ):

        return False, (
            "Required OHLC columns are missing"
        )

    if len(data) < 30:

        return False, (
            "Not enough market data "
            "for pattern detection"
        )

    return True, None


# =========================================================
# SAFE PERCENT DIFFERENCE
# =========================================================

def _percent_difference(
    value_a,
    value_b
):
    """
    Calculate percentage difference safely.
    """

    try:

        if value_b == 0:

            return 0

        return abs(

            value_a
            -
            value_b

        ) / abs(value_b)

    except (

        TypeError,
        ValueError,
        ZeroDivisionError

    ):

        return 0


# =========================================================
# PATTERN ANALYSIS
# =========================================================

def analyze_pattern(source):
    """
    Analyze chart patterns.

    Supports:
    - Symbol
    - Pandas DataFrame

    Returns standardized pattern evidence.
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
        # PRICE SERIES
        # =================================================

        high = data["High"]

        low = data["Low"]

        close = data["Close"]

        last_close = float(

            close.iloc[-1]

        )

        # =================================================
        # DEFAULT VALUES
        # =================================================

        pattern = "NONE"

        signal = "HOLD"

        strength = "LOW"

        score = 50

        bullish = False

        bearish = False

        bullish_score = 0

        bearish_score = 0

        confidence = 40

        # =================================================
        # HISTORICAL WINDOWS
        #
        # Important:
        # Latest candle is excluded from breakout
        # resistance/support calculations.
        # =================================================

        previous_high = float(

            high.iloc[-20:-10].max()

        )

        recent_high = float(

            high.iloc[-10:-1].max()

        )

        previous_low = float(

            low.iloc[-20:-10].min()

        )

        recent_low = float(

            low.iloc[-10:-1].min()

        )

        resistance = float(

            high.iloc[-20:-1].max()

        )

        support = float(

            low.iloc[-20:-1].min()

        )

        # =================================================
        # DOUBLE TOP
        # =================================================

        high_difference = _percent_difference(

            recent_high,

            previous_high
        )

        double_top = (

            high_difference <= 0.02

            and last_close < recent_high
        )

        # =================================================
        # DOUBLE BOTTOM
        # =================================================

        low_difference = _percent_difference(

            recent_low,

            previous_low
        )

        double_bottom = (

            low_difference <= 0.02

            and last_close > recent_low
        )

        # =================================================
        # BREAKOUT
        # =================================================

        breakout = (

            last_close > resistance
        )

        # =================================================
        # BREAKDOWN
        # =================================================

        breakdown = (

            last_close < support
        )

        # =================================================
        # PATTERN PRIORITY
        #
        # Strong structural events receive priority.
        # =================================================

        if breakout:

            pattern = "BREAKOUT"

            signal = "STRONG BUY"

            strength = "VERY HIGH"

            score = 85

            bullish = True

            bullish_score = 3

            confidence = 85

        elif breakdown:

            pattern = "BREAKDOWN"

            signal = "STRONG SELL"

            strength = "VERY HIGH"

            score = 15

            bearish = True

            bearish_score = 3

            confidence = 85

        elif double_bottom:

            pattern = "DOUBLE BOTTOM"

            signal = "BUY"

            strength = "HIGH"

            score = 75

            bullish = True

            bullish_score = 2

            confidence = 70

        elif double_top:

            pattern = "DOUBLE TOP"

            signal = "SELL"

            strength = "HIGH"

            score = 25

            bearish = True

            bearish_score = 2

            confidence = 70

        # =================================================
        # RETURN PATTERN EVIDENCE
        # =================================================

        return {

            "status": "success",

            "pattern": pattern,

            "signal": signal,

            "strength": strength,

            "score": score,

            "bullish": bullish,

            "bearish": bearish,

            "bullish_score": bullish_score,

            "bearish_score": bearish_score,

            "confidence": confidence,

            "support": round(
                support,
                2
            ),

            "resistance": round(
                resistance,
                2
            )
        }

    except Exception as error:

        return _empty_result(

            status="error",

            error=str(error)
        )


# =========================================================
# BULLISH HELPER
# =========================================================

def is_bullish(pattern):
    """
    Return True if pattern evidence is bullish.
    """

    if not isinstance(
        pattern,
        dict
    ):

        return False

    return bool(

        pattern.get(
            "bullish",
            False
        )

    )


# =========================================================
# BEARISH HELPER
# =========================================================

def is_bearish(pattern):
    """
    Return True if pattern evidence is bearish.
    """

    if not isinstance(
        pattern,
        dict
    ):

        return False

    return bool(

        pattern.get(
            "bearish",
            False
        )

    )


# =========================================================
# CENTRAL BRAIN COMPATIBILITY
# =========================================================

def detect_patterns(source=None):
    """
    CentralBrain Pattern Detection Interface.

    Supports:
    - Symbol
    - Pandas DataFrame

    Returns standardized pattern evidence.
    """

    if source is None:

        return _empty_result(

            status="error",

            error=(
                "Pattern analysis source unavailable"
            )
        )

    return analyze_pattern(
        source
    )
