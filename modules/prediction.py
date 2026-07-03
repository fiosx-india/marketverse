def get_prediction(symbol, data):
    market = data["market"]
    indicators = data["indicators"]
    news = data.get("news", [])

    price = market["price"]
    rsi = indicators["rsi"]
    sma20 = indicators["sma20"]
    ema20 = indicators["ema20"]

    signal = "HOLD"
    confidence = 50
    reason = []

    if price > sma20 and price > ema20 and rsi < 70:
        signal = "BUY"
        confidence = 80
        reason.append("Bullish trend")

    elif price < sma20 and price < ema20 and rsi > 30:
        signal = "SELL"
        confidence = 80
        reason.append("Bearish trend")

    else:
        reason.append("Market is neutral")

    return {
        "signal": signal,
        "confidence": confidence,
        "target": round(price * 1.03, 2),
        "stop_loss": round(price * 0.98, 2),
        "reason": reason,
        "news_count": len(news)
    }
