def predict_market(data, technical):
    score = 0

    if technical.get("rsi", 50) < 30:
        score += 20

    if technical.get("macd", 0) > 0:
        score += 20

    if technical.get("trend") == "Bullish":
        score += 30

    confidence = min(score, 100)

    if confidence >= 70:
        signal = "BUY"
    elif confidence >= 40:
        signal = "HOLD"
    else:
        signal = "SELL"

    return {
        "signal": signal,
        "confidence": confidence
    }
