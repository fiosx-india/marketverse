from .market_data import get_stock_price
from .technical import calculate_indicators
from .prediction import predict_market


def analyze(symbol):
    market = get_stock_price(symbol)

    if not market:
        return {"error": "Market data unavailable"}

    technical = calculate_indicators(symbol)

    prediction = predict_market(market, technical)

    return {
        "market": market,
        "technical": technical,
        "prediction": prediction
    }
