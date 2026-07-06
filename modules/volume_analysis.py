"""
=========================================================
MarketVerse AI - Volume Analysis Engine
=========================================================
Analyzes trading volume and buying pressure.
=========================================================
"""

import pandas as pd


def analyze_volume(df):
    """
    Analyze market volume.
    Returns volume strength.
    """

    if df is None or df.empty:
        return {
            "current_volume": 0,
            "average_volume": 0,
            "relative_volume": 0,
            "buy_pressure": 0,
            "sell_pressure": 0,
            "strength": "LOW",
            "score": 0
        }

    current_volume = float(df["Volume"].iloc[-1])

    average_volume = float(
        df["Volume"].rolling(20).mean().iloc[-1]
    )

    if average_volume == 0:
        relative_volume = 0
    else:
        relative_volume = current_volume / average_volume

    close = float(df["Close"].iloc[-1])
    open_price = float(df["Open"].iloc[-1])

    if close > open_price:
        buy_pressure = 100
        sell_pressure = 0
    elif close < open_price:
        buy_pressure = 0
        sell_pressure = 100
    else:
        buy_pressure = 50
        sell_pressure = 50

    score = 0

    if relative_volume >= 2:
        score += 50

    elif relative_volume >= 1.5:
        score += 35

    elif relative_volume >= 1:
        score += 20

    score += int(buy_pressure * 0.5)

    score = max(0, min(100, score))

    if score >= 80:
        strength = "VERY STRONG"

    elif score >= 60:
        strength = "STRONG"

    elif score >= 40:
        strength = "MEDIUM"

    else:
        strength = "WEAK"

    return {
        "current_volume": round(current_volume, 2),
        "average_volume": round(average_volume, 2),
        "relative_volume": round(relative_volume, 2),
        "buy_pressure": buy_pressure,
        "sell_pressure": sell_pressure,
        "strength": strength,
        "score": score
    }

# ==========================================
# Compatibility Wrapper for CentralBrain
# ==========================================

def volume_analysis(df=None):
    """
    Compatibility wrapper for CentralBrain.
    """
    if df is None:
        return {
            "current_volume": 0,
            "average_volume": 0,
            "relative_volume": 0,
            "buy_pressure": 0,
            "sell_pressure": 0,
            "strength": "LOW",
            "score": 0
        }

    return analyze_volume(df)
