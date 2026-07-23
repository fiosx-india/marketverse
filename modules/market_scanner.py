"""
=========================================================
MarketVerse AI - Market Scanner
=========================================================
Scans market data and identifies trading opportunities.
=========================================================
"""

from modules.intelligence_engine import IntelligenceEngine


def scan_market(stocks):

    if not stocks:
        return []

    engine = IntelligenceEngine()
    results = []

    for stock in stocks:

        symbol = stock.get("symbol")
        if not symbol:
            continue

        try:
            result = engine.run(symbol)

            market = result.get("market", {})
            news = result.get("news", {})

            price = market.get("price", 0)
            volume = market.get("volume", 0)
            confidence = news.get("confidence", 50)
            volatility = result.get("volatility", 0)

            if price <= 0:
                continue

            signal = "HOLD"

            rsi = market.get("rsi", 50)

            if rsi < 30:
                signal = "BUY"

            elif rsi > 70:
                signal = "SELL"

            elif confidence >= 70 and volatility >= 1.5:
                signal = "BUY"

            elif confidence >= 70 and volatility <= 0.7:
                signal = "SELL"

            results.append({
                "symbol": symbol,
                "price": round(price, 2),
                "change_percent": round(volatility, 2),
                "volume": volume,
                "confidence": confidence,
                "signal": signal
            })

        except Exception:
            continue

    results.sort(
        key=lambda x: (x["confidence"], x["volume"]),
        reverse=True
    )

    return results


def top_buy(results, limit=5):
    return [x for x in results if x["signal"] == "BUY"][:limit]


def top_sell(results, limit=5):
    return [x for x in results if x["signal"] == "SELL"][:limit]


def top_volume(results, limit=5):
    return sorted(
        results,
        key=lambda x: x["volume"],
        reverse=True
    )[:limit]


if __name__ == "__main__":

    demo = [
        {"symbol": "RELIANCE.NS"},
        {"symbol": "TCS.NS"},
        {"symbol": "INFY.NS"},
        {"symbol": "HDFCBANK.NS"},
        {"symbol": "ICICIBANK.NS"},
    ]

    scanned = scan_market(demo)

    print("\nTop Buy")
    print(top_buy(scanned))

    print("\nTop Sell")
    print(top_sell(scanned))

    print("\nTop Volume")
    print(top_volume(scanned))
