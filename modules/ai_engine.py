"""
=========================================================
MarketVerse AI - Professional Intelligence Engine v2.0
=========================================================

Engine Flow

1. Market Data
    ↓
2. Technical Analysis
    ↓
3. News Collection
    ↓
4. Market Sentiment Analysis
    ↓
5. AI Prediction Engine
    ↓
6. Risk Management
    ↓
7. Final Trading Decision
=========================================================
"""

from .market_data import get_market_data
from .technical import calculate_indicators
from .news import get_market_news
from .prediction import get_prediction
from .risk_manager import calculate_risk


def analyze(symbol):

    # -----------------------------
    # STEP 1 : LIVE MARKET DATA
    # -----------------------------
    market = get_market_data(symbol)

    if not market or "error" in market:
        return {
            "status": "error",
            "message": "Unable to fetch market data."
        }

    # -----------------------------
    # STEP 2 : TECHNICAL ANALYSIS
    # -----------------------------
    technical = calculate_indicators(symbol)

    if not technical or "error" in technical:
        return {
            "status": "error",
            "message": "Technical analysis failed."
        }

    # -----------------------------
    # STEP 3 : MARKET NEWS
    # -----------------------------
    news = get_market_news()

    # -----------------------------
    # STEP 4 : AI PREDICTION
    # -----------------------------
    prediction = get_prediction(
        symbol,
        {
            "market": market,
            "indicators": technical,
            "news": news
        }
    )

    # -----------------------------
    # STEP 5 : RISK MANAGEMENT
    # -----------------------------
    risk = calculate_risk(market["price"])

    # -----------------------------
    # STEP 6 : FINAL OUTPUT
    # -----------------------------
    return {

        "status": "success",

        "symbol": symbol,

        "market": market,

        "technical": technical,

        "news": news,

        "prediction": prediction,

        "risk": risk,

        "engine_version": "2.0",

        "engine_status": "READY",

        "analysis_complete": True

    }
