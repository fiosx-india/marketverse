"""
=========================================================
MarketVerse AI - System Manager
=========================================================
Central Integration Module
=========================================================
"""

from modules.market_data import get_market_data
from modules.technical import analyze_technical
from modules.news_analysis import calculate_sentiment
from modules.prediction import predict_market
from modules.strategy import generate_strategy
from modules.confidence import calculate_confidence
from modules.risk_manager import calculate_risk


class SystemManager:

    def __init__(self):
        pass

    def analyze(self, symbol):

        # Market Data
        df = get_stock_data(symbol)

        if df is None or len(df) == 0:
            return {
                "success": False,
                "error": "No market data available."
            }

        # Technical Analysis
        technical = analyze_technical(df)

        # News Sentiment
        sentiment = calculate_sentiment("")

        # AI Prediction
        prediction = predict_market(df)

        # Trading Strategy
        strategy = generate_strategy(
            technical,
            sentiment,
            prediction
        )

        # Confidence
        confidence = calculate_confidence(
            technical,
            sentiment,
            prediction
        )

        # Risk Management
        entry = df["Close"].iloc[-1]

        risk = calculate_risk(entry)

        return {

            "success": True,

            "symbol": symbol,

            "technical": technical,

            "sentiment": sentiment,

            "prediction": prediction,

            "strategy": strategy,

            "confidence": confidence,

            "risk": risk

        }


####################################################
# TEST
####################################################

if __name__ == "__main__":

    manager = SystemManager()

    result = manager.analyze("RELIANCE.NS")

    print(result)
