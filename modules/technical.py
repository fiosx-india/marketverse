import yfinance as yf
import pandas as pd


def calculate_sma(data, period=20):
    return data["Close"].rolling(window=period).mean()


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


def calculate_macd(data):
    ema12 = data["Close"].ewm(span=12, adjust=False).mean()
    ema26 = data["Close"].ewm(span=26, adjust=False).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()

    return macd, signal


def calculate_bollinger(data):
    sma20 = data["Close"].rolling(20).mean()
    std = data["Close"].rolling(20).std()

    upper = sma20 + (std * 2)
    lower = sma20 - (std * 2)

    return upper, lower


def calculate_atr(data, period=14):

    high_low = data["High"] - data["Low"]

    high_close = (data["High"] - data["Close"].shift()).abs()

    low_close = (data["Low"] - data["Close"].shift()).abs()

    tr = pd.concat(
        [high_low, high_close, low_close],
        axis=1
    ).max(axis=1)

    atr = tr.rolling(period).mean()

    return atr


def calculate_indicators(symbol):

    try:

        stock = yf.Ticker(symbol)

        data = stock.history(period="6mo")

        if data.empty:
            return {
                "error": "No technical data"
            }

        sma20 = calculate_sma(data).iloc[-1]
        ema20 = calculate_ema(data).iloc[-1]
        rsi14 = calculate_rsi(data).iloc[-1]

        macd, macd_signal = calculate_macd(data)

        bb_upper, bb_lower = calculate_bollinger(data)

        atr = calculate_atr(data)

        return {

            "price": round(float(data["Close"].iloc[-1]), 2),

            "sma20": round(float(sma20), 2),

            "ema20": round(float(ema20), 2),

            "rsi": round(float(rsi14), 2),

            "macd": round(float(macd.iloc[-1]), 2),

            "macd_signal": round(float(macd_signal.iloc[-1]), 2),

            "bollinger_upper": round(float(bb_upper.iloc[-1]), 2),

            "bollinger_lower": round(float(bb_lower.iloc[-1]), 2),

            "atr": round(float(atr.iloc[-1]), 2)

        }

    except Exception as e:

        return {
            "error": str(e)
        }
