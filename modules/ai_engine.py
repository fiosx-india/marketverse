from .market_data import get_stock_price
from .technical import calculate_indicators
from .prediction import get_prediction
from .news import get_market_news


def analyze(symbol):
    # Market Data
    market = get_stock_price(symbol)

    if not market or "error" in market:
        return {
            "status": "error",
            "message": "Market data unavailable"
        }

    # Technical Analysis
    technical = calculate_indicators(symbol)

    if not technical or "error" in technical:
        return {
            "status": "error",
            "message": "Technical analysis failed"
        }

    # News
    news = get_market_news()

    # AI Prediction
    prediction = get_prediction(symbol, {
        "market": market,
        "indicators": technical,
        "news": news
    })

    return {
        "status": "success",
        "symbol": symbol,
        "market": market,
        "technical": technical,
        "news": news,
        "prediction": prediction
    }
