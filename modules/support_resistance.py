"""
=========================================================
MarketVerse AI - Support & Resistance Engine
=========================================================
Calculates Support, Resistance,
Breakout and Breakdown levels.
=========================================================
"""

import pandas as pd


def analyze_support_resistance(df):
    """
    Analyze support and resistance levels.
    """

    if df is None or df.empty:
        return {
            "support": 0,
            "resistance": 0,
            "price": 0,
            "distance_to_support": 0,
            "distance_to_resistance": 0,
            "signal": "NO DATA"
        }

    lookback = 20

    support = float(df["Low"].tail(lookback).min())
    resistance = float(df["High"].tail(lookback).max())
    current_price = float(df["Close"].iloc[-1])

    distance_support = round(
        ((current_price - support) / current_price) * 100,
        2
    )

    distance_resistance = round(
        ((resistance - current_price) / current_price) * 100,
        2
    )

    if current_price > resistance:
        signal = "BREAKOUT"

    elif current_price < support:
        signal = "BREAKDOWN"

    elif distance_support < 2:
        signal = "NEAR SUPPORT"

    elif distance_resistance < 2:
        signal = "NEAR RESISTANCE"

    else:
        signal = "RANGE"

    return {
        "price": round(current_price, 2),
        "support": round(support, 2),
        "resistance": round(resistance, 2),
        "distance_to_support": distance_support,
        "distance_to_resistance": distance_resistance,
        "signal": signal
    }
