"""
=========================================================
MarketVerse AI - Pattern Detection Engine
=========================================================
Detects common chart patterns.
=========================================================
"""

import pandas as pd


def analyze_pattern(df):
    """
    Detect chart patterns.
    Returns pattern information.
    """

    if df is None or df.empty or len(df) < 30:
        return {
            "pattern": "NO DATA",
            "signal": "HOLD",
            "strength": "LOW",
            "score": 0
        }

    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    recent_high = high.tail(10).max()
    previous_high = high.tail(20).head(10).max()

    recent_low = low.tail(10).min()
    previous_low = low.tail(20).head(10).min()

    last_close = float(close.iloc[-1])

    pattern = "NONE"
    signal = "HOLD"
    strength = "LOW"
    score = 50

    # -----------------------------
    # Double Top
    # -----------------------------
    if abs(recent_high - previous_high) / previous_high < 0.02:
        pattern = "DOUBLE TOP"
        signal = "SELL"
        strength = "HIGH"
        score = 25

    # -----------------------------
    # Double Bottom
    # -----------------------------
    elif abs(recent_low - previous_low) / previous_low < 0.02:
        pattern = "DOUBLE BOTTOM"
        signal = "BUY"
        strength = "HIGH"
        score = 75

    # -----------------------------
    # Breakout
    # -----------------------------
    elif last_close > recent_high:
        pattern = "BREAKOUT"
        signal = "STRONG BUY"
        strength = "VERY HIGH"
        score = 100

    # -----------------------------
    # Breakdown
    # -----------------------------
    elif last_close < recent_low:
        pattern = "BREAKDOWN"
        signal = "STRONG SELL"
        strength = "VERY HIGH"
        score = 0

    return {
        "pattern": pattern,
        "signal": signal,
        "strength": strength,
        "score": score
    }


def is_bullish(pattern):
    """
    Returns True for bullish patterns.
    """
    return pattern.get("signal") in [
        "BUY",
        "STRONG BUY"
    ]


def is_bearish(pattern):
    """
    Returns True for bearish patterns.
    """
    return pattern.get("signal") in [
        "SELL",
        "STRONG SELL"
    ]

def detect_patterns(df):
    """
    Compatibility wrapper for CentralBrain.
    """
    return analyze_pattern(df)
