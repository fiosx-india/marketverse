def calculate_strategy(market, technical, prediction, sentiment=None):
    """
    Professional Strategy Engine
    Combines Market + Technical + AI + Sentiment
    """

    score = 0
    reasons = []

    # AI Prediction (40%)
    confidence = prediction.get("confidence", 50)

    if prediction["signal"] == "STRONG BUY":
        score += 40
        reasons.append("AI Strong Buy")

    elif prediction["signal"] == "BUY":
        score += 30
        reasons.append("AI Buy")

    elif prediction["signal"] == "SELL":
        score -= 30
        reasons.append("AI Sell")

    elif prediction["signal"] == "STRONG SELL":
        score -= 40
        reasons.append("AI Strong Sell")

    # Technical Trend (35%)
    if technical["ema20"] > technical["ema50"]:
        score += 20
        reasons.append("EMA Bullish")

    if technical["macd"] > technical["macd_signal"]:
        score += 10
        reasons.append("MACD Bullish")

    if technical["rsi"] < 30:
        score += 5
        reasons.append("RSI Oversold")

    elif technical["rsi"] > 70:
        score -= 5
        reasons.append("RSI Overbought")

    # Market Move (15%)
    if market["change_percent"] > 0:
        score += 10
    else:
        score -= 10

    # Sentiment (10%)
    if sentiment:
        if sentiment["score"] > 70:
            score += 10
            reasons.append("Positive Sentiment")

        elif sentiment["score"] < 30:
            score -= 10
            reasons.append("Negative Sentiment")

    # Final Decision
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
