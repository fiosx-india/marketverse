import yfinance as yf
import pandas as pd


def calculate_sma(data, period=20):
    return data["Close"].rolling(period).mean()


def calculate_ema(data, period=20):
    return data["Close"].ewm(span=period, adjust=False).mean()


def calculate_rsi(data, period=14):
    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_indicators(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="3mo")

        if data.empty:
            return {"error": "No technical data"}

        sma20 = calculate_sma(data).iloc[-1]
        ema20 = calculate_ema(data).iloc[-1]
        rsi14 = calculate_rsi(data).iloc[-1]

        return {
            "price": round(float(data["Close"].iloc[-1]), 2),
            "sma20": round(float(sma20), 2),
            "ema20": round(float(ema20), 2),
            "rsi": round(float(rsi14), 2)
        }

    except Exception as e:
        return {
            "error": str(e)
        }
