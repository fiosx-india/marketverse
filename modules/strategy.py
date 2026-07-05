def calculate_strategy(market, technical, prediction, sentiment=None):
    """
    Professional Strategy Engine
    Combines Market + Technical + AI + Sentiment
    """

    score = 0
    reasons = []

    # ==========================
    # AI Prediction (40%)
    # ==========================
    confidence = prediction.get("confidence", 50)
    signal = prediction.get("signal", "HOLD")

    if signal == "STRONG BUY":
        score += 40
        reasons.append("AI Strong Buy")

    elif signal == "BUY":
        score += 30
        reasons.append("AI Buy")

    elif signal == "SELL":
        score -= 30
        reasons.append("AI Sell")

    elif signal == "STRONG SELL":
        score -= 40
        reasons.append("AI Strong Sell")

    # ==========================
    # Technical Analysis (35%)
    # ==========================
    ema20 = technical.get("ema20", 0)
    ema50 = technical.get("ema50", 0)
    macd = technical.get("macd", 0)
    macd_signal = technical.get("macd_signal", 0)
    rsi = technical.get("rsi", 50)

    if ema20 > ema50:
        score += 20
        reasons.append("EMA Bullish")
    else:
        score -= 10
        reasons.append("EMA Bearish")

    if macd > macd_signal:
        score += 10
        reasons.append("MACD Bullish")
    else:
        score -= 10
        reasons.append("MACD Bearish")

    if rsi < 30:
        score += 5
        reasons.append("RSI Oversold")

    elif rsi > 70:
        score -= 5
        reasons.append("RSI Overbought")

    # ==========================
    # Market Trend (15%)
    # ==========================
    change = market.get("change_percent", 0)

    if change > 0:
        score += 10
        reasons.append("Positive Market")

    elif change < 0:
        score -= 10
        reasons.append("Negative Market")

    # ==========================
    # News Sentiment (10%)
    # ==========================
    if sentiment:
        sentiment_score = sentiment.get("score", 50)

        if sentiment_score > 70:
            score += 10
            reasons.append("Positive Sentiment")

        elif sentiment_score < 30:
            score -= 10
            reasons.append("Negative Sentiment")

    # ==========================
    # Final Decision
    # ==========================
    if score >= 60:
        decision = "STRONG BUY"

    elif score >= 30:
        decision = "BUY"

    elif score <= -60:
        decision = "STRONG SELL"

    elif score <= -30:
        decision = "SELL"

    else:
        decision = "HOLD"

    return {
        "decision": decision,
        "score": score,
        "confidence": confidence,
        "reasons": reasons
    }
def generate_strategy(technical, sentiment, prediction):
    """
    Compatibility wrapper for SystemManager.
    """

    signal = prediction.get("signal", "HOLD")

    if signal == "STRONG BUY":
        return {
            "action": "BUY",
            "strength": "Strong"
        }

    elif signal == "STRONG SELL":
        return {
            "action": "SELL",
            "strength": "Strong"
        }

    elif signal == "BUY":
        return {
            "action": "BUY",
            "strength": "Normal"
        }

    elif signal == "SELL":
        return {
            "action": "SELL",
            "strength": "Normal"
        }

    return {
        "action": "HOLD",
        "strength": "Neutral"
    }
