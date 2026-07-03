import yfinance as yf

def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")

        if data.empty:
            return {
                "error": "No market data found"
            }

        return {
            "symbol": symbol,
            "price": round(float(data["Close"].iloc[-1]), 2),
            "high": round(float(data["High"].iloc[-1]), 2),
            "low": round(float(data["Low"].iloc[-1]), 2),
            "open": round(float(data["Open"].iloc[-1]), 2),
            "volume": int(data["Volume"].iloc[-1])
        }

    except Exception as e:
        return {
            "error": str(e)
        }
