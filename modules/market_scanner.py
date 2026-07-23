"""
=========================================================
MarketVerse AI - Market Scanner
=========================================================
Scans market data and identifies trading opportunities.
=========================================================
"""

from data.fno_stocks import FNO_STOCKS
from modules.intelligence_engine import IntelligenceEngine


def scan_market(stocks):

    engine = IntelligenceEngine()

    if not stocks:
        return []

    results = []

     for stock in stocks:

    symbol = stock["symbol"]

    try:
        result = engine.run(symbol)

        market = result["market"]

        price = market.get("price", 0)

        volume = market.get("volume", 0)

        confidence = result["news"].get("confidence", 50)

        change = result["volatility"]

    except Exception:
        continue

        signal = "HOLD"

        if change > 2 and confidence >= 70:
            signal = "BUY"

        elif change < -2 and confidence >= 70:
            signal = "SELL"

        results.append({

            "symbol": symbol,

            "price": price,

            "change_percent": round(change, 2),

            "volume": volume,

            "confidence": confidence,

            "signal": signal

        })

    return sorted(
        results,
        key=lambda x: x["confidence"],
        reverse=True
    )


def top_buy(results, limit=5):

    return [
        stock
        for stock in results
        if stock["signal"] == "BUY"
    ][:limit]


def top_sell(results, limit=5):

    return [
        stock
        for stock in results
        if stock["signal"] == "SELL"
    ][:limit]


def top_volume(results, limit=5):

    return sorted(
        results,
        key=lambda x: x["volume"],
        reverse=True
    )[:limit]


def top_volume(results, limit=5):

    return sorted(
        results,
        key=lambda x: x["volume"],
        reverse=True
    )[:limit]


if __name__ == "__main__":

    demo = [

        {
            "symbol": "RELIANCE",
            "price": 1500,
            "change_percent": 2.5,
            "volume": 150000,
            "confidence": 85
        },

        {
            "symbol": "TCS",
            "price": 3800,
            "change_percent": -2.8,
            "volume": 120000,
            "confidence": 82
        },

        {
            "symbol": "INFY",
            "price": 1700,
            "change_percent": 0.8,
            "volume": 80000,
            "confidence": 60
        }

    ]

    scanned = scan_market(demo)

    print("Top Buy")
    print(top_buy(scanned))

    print("Top Sell")
    print(top_sell(scanned))

    print("Top Volume")
    print(top_volume(scanned))

