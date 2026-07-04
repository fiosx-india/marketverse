import yfinance as yf


def get_market_data(symbol):
    """
    Returns live market data for any stock/crypto symbol.
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="5d", auto_adjust=True)

        if data.empty or len(data) < 2:
            return {
                "error": "Not enough market data"
            }

        current = round(data["Close"].iloc[-1], 2)
        previous = round(data["Close"].iloc[-2], 2)

        change = round(current - previous, 2)

        if previous != 0:
            percent = round((change / previous) * 100, 2)
        else:
            percent = 0

        # ===========================
        # Return Market Data
        # ===========================

        return {
            "symbol": symbol,
            "price": current,
            "open": round(data["Open"].iloc[-1], 2),
            "high": round(data["High"].iloc[-1], 2),
            "low": round(data["Low"].iloc[-1], 2),
            "close": round(data["Close"].iloc[-1], 2),
            "volume": int(data["Volume"].iloc[-1]),
            "change": change,
            "change_percent": percent,
            "timestamp": str(data.index[-1])
        }

    except Exception as e:
        return {
            "error": str(e)
        }


def get_dashboard_data():
    return {
        "NIFTY50": get_market_data("^NSEI"),
        "SENSEX": get_market_data("^BSESN"),
        "BTC": get_market_data("BTC-USD"),
        "RELIANCE": get_market_data("RELIANCE.NS"),
        "TCS": get_market_data("TCS.NS"),
        "INFY": get_market_data("INFY.NS"),
        "GOLD": get_market_data("GC=F"),
        "SILVER": get_market_data("SI=F")
    }
