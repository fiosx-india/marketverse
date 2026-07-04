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

        return {
            "symbol": symbol,
            "price": current,
            "change": change,
            "change_percent": percent
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
