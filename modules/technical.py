import yfinance as yf
import pandas as pd
import ta


def calculate_indicators(symbol):
    try:
        stock = yf.Ticker(symbol)
                data = stock.history(
            period="6mo",
            auto_adjust=True
        )

        if data.empty or len(data) < 50:
            return {
                "error": "Not enough market data"
            }

        close = data["Close"]
        high = data["High"]
        low = data["Low"]
        volume = data["Volume"]
        # ==========================
        # Moving Averages
        # ==========================
        sma20 = ta.trend.SMAIndicator(close, window=20).sma_indicator()
        sma50 = ta.trend.SMAIndicator(close, window=50).sma_indicator()

        ema20 = ta.trend.EMAIndicator(close, window=20).ema_indicator()
        ema50 = ta.trend.EMAIndicator(close, window=50).ema_indicator()

        # ==========================
        # RSI
        # ==========================
        rsi = ta.momentum.RSIIndicator(close, window=14).rsi()

        # ==========================
        # MACD
        # ==========================
        macd = ta.trend.MACD(close)

        macd_line = macd.macd()
        macd_signal = macd.macd_signal()
        macd_hist = macd.macd_diff()

        # ==========================
        # Bollinger Bands
        # ==========================
        bb = ta.volatility.BollingerBands(close)

        bb_upper = bb.bollinger_hband()
        bb_middle = bb.bollinger_mavg()
        bb_lower = bb.bollinger_lband()

        # ==========================
        # ATR
        # ==========================
        atr = ta.volatility.AverageTrueRange(
            high,
            low,
            close
        ).average_true_range()

        # ==========================
        # ADX
        # ==========================
        adx = ta.trend.ADXIndicator(
            high,
            low,
            close
        ).adx()

        # ==========================
        # Support / Resistance
        # ==========================
        support = low.tail(30).min()
        resistance = high.tail(30).max()

        # ==========================
        # Trend Detection
        # ==========================
        latest_price = close.iloc[-1]

        if latest_price > ema20.iloc[-1] > ema50.iloc[-1]:
            trend = "Strong Bullish"

        elif latest_price < ema20.iloc[-1] < ema50.iloc[-1]:
            trend = "Strong Bearish"

        else:
            trend = "Sideways"

        # ==========================
        # Volume
        # ==========================
        latest_volume = int(volume.iloc[-1])
        avg_volume = int(volume.tail(20).mean())

        volume_strength = (
            "High"
            if latest_volume > avg_volume
            else "Normal"
        )

        # ==========================
        # Return
        # ==========================
        return {

            "price": round(float(latest_price), 2),

            "sma20": round(float(sma20.iloc[-1]), 2),
            "sma50": round(float(sma50.iloc[-1]), 2),

            "ema20": round(float(ema20.iloc[-1]), 2),
            "ema50": round(float(ema50.iloc[-1]), 2),

            "rsi": round(float(rsi.iloc[-1]), 2),

            "macd": round(float(macd_line.iloc[-1]), 4),
            "macd_signal": round(float(macd_signal.iloc[-1]), 4),
            "macd_histogram": round(float(macd_hist.iloc[-1]), 4),

            "bollinger_upper": round(float(bb_upper.iloc[-1]), 2),
            "bollinger_middle": round(float(bb_middle.iloc[-1]), 2),
            "bollinger_lower": round(float(bb_lower.iloc[-1]), 2),

            "atr": round(float(atr.iloc[-1]), 2),

            "adx": round(float(adx.iloc[-1]), 2),

            "support": round(float(support), 2),
            "resistance": round(float(resistance), 2),

            "volume": latest_volume,
            "average_volume": avg_volume,
            "volume_strength": volume_strength,

            "trend": trend

        }

    except Exception as e:
        return {
            "error": str(e)
        }
