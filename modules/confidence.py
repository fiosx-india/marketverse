"""
=========================================================
MarketVerse AI - Confidence Engine
=========================================================
Calculates AI Confidence Score (0-100)
=========================================================
"""

def calculate_confidence(
    market,
    technical,
    prediction,
    sentiment,
    strategy
):
    """
    Returns overall AI confidence score.
    """

    score = 0
    reasons = []

    # -----------------------------------
    # Strategy (40%)
    # -----------------------------------
    strategy_score = strategy.get("score", 0)

    if strategy_score >= 60:
        score += 40
        reasons.append("Strong strategy score")

    elif strategy_score >= 30:
        score += 30
        reasons.append("Good strategy score")

    # -----------------------------------
    # Prediction (20%)
    # -----------------------------------
    prediction_confidence = prediction.get("confidence", 50)

    score += int(prediction_confidence * 0.2)

    # -----------------------------------
    # Technical Trend (20%)
    # -----------------------------------
    ema20 = technical.get("ema20", 0)
    ema50 = technical.get("ema50", 0)

    if ema20 > ema50:
        score += 10
        reasons.append("EMA Bullish")

    macd = technical.get("macd", 0)
    macd_signal = technical.get("macd_signal", 0)

    if macd > macd_signal:
        score += 10
        reasons.append("MACD Bullish")

    # -----------------------------------
    # Market Trend (10%)
    # -----------------------------------
    if market.get("change_percent", 0) > 0:
        score += 10
        reasons.append("Positive Market")

    # -----------------------------------
    # Sentiment (10%)
    # -----------------------------------
    sentiment_score = sentiment.get("score", 50)

    if sentiment_score >= 70:
        score += 10
        reasons.append("Positive Sentiment")

    score = max(0, min(100, score))

    # -----------------------------------
    # Confidence Level
    # -----------------------------------
    if score >= 85:
        level = "VERY HIGH"

    elif score >= 70:
        level = "HIGH"

    elif score >= 50:
        level = "MEDIUM"

    else:
        level = "LOW"

    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }
