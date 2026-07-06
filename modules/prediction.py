from .risk_manager import calculate_risk


def get_prediction(symbol, data):
    market = data["market"]
    indicators = data["indicators"]
    news = data.get("news", [])

    price = market["price"]
    rsi = indicators["rsi"]
    sma20 = indicators["sma20"]
    ema20 = indicators["ema20"]
    macd = indicators["macd"]
    macd_signal = indicators["macd_signal"]

    signal = "HOLD"
    confidence = 50
    reason = []

    if (
        rsi < 30
        and macd > macd_signal
        and price > ema20
    ):
        signal = "STRONG BUY"
        confidence = 95
        reason.extend([
            "RSI Oversold",
            "MACD Bullish",
            "Price above EMA20"
        ])

    elif (
        rsi > 70
        and macd < macd_signal
        and price < ema20
    ):
        signal = "STRONG SELL"
        confidence = 95
        reason.extend([
            "RSI Overbought",
            "MACD Bearish",
            "Price below EMA20"
        ])

    elif price > sma20 and price > ema20:
        signal = "BUY"
        confidence = 80
        reason.append("Bullish Trend")

    elif price < sma20 and price < ema20:
        signal = "SELL"
        confidence = 80
        reason.append("Bearish Trend")

    else:
        signal = "HOLD"
        confidence = 55
        reason.append("Market is Neutral")

    risk = calculate_risk(price)

    return {
        "signal": signal,
        "confidence": confidence,
        "entry": risk["entry"],
        "stop_loss": risk["stop_loss"],
        "take_profit_1": risk["take_profit_1"],
        "take_profit_2": risk["take_profit_2"],
        "risk_reward": risk["risk_reward"],
        "reason": reason,
        "news_count": len(news)
    }
def predict_market(df):
    """
    Compatibility wrapper for SystemManager.
    """

    latest = df.iloc[-1]

    return {
        "signal": "BUY" if latest["Close"] > latest["EMA_20"] else "SELL",
        "confidence": 75,
        "price": float(latest["Close"])
    }

# =========================================
# Compatibility Wrapper for CentralBrain
# =========================================

def predict_price(df=None):
    """
    Safe compatibility wrapper for CentralBrain.
    """

    if df is None:
        return {
            "signal": "UNKNOWN",
            "confidence": 0,
            "price": 0
        }

    try:
        if df.empty:
            return {
                "signal": "UNKNOWN",
                "confidence": 0,
                "price": 0
            }

        return predict_market(df)

    except Exception:
        return {
            "signal": "UNKNOWN",
            "confidence": 0,
            "price": 0
        }
