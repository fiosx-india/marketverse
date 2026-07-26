import yfinance as yf
import time

def get_market_data(symbol):
    """
    Returns OHLC DataFrame for analysis.
    """
    try:
        for attempt in range(3):
            df = yf.download(
                symbol,
                period="3mo",
                interval="1d",
                auto_adjust=True,
                progress=False
            )

            if not df.empty:
                break

            time.sleep(1)

        if df.empty:
            return None

        # Fix MultiIndex columns
        if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)

        return df

    except Exception:
        return None


def get_dashboard_data():
    return {
        "NIFTY50": get_market_data("^NSEI"),
        "SENSEX": get_market_data("^BSESN"),

        "BTC": get_market_data("BTC-USD"),

        "RELIANCE": get_market_data("RELIANCE.NS"),
        "TCS": get_market_data("TCS.NS"),
        "INFY": get_market_data("INFY.NS"),

        # Commodities
        "GOLD": get_market_data("GC=F"),
        "SILVER": get_market_data("SI=F"),
        "CRUDE_OIL": get_market_data("CL=F"),
        "NATURAL_GAS": get_market_data("NG=F"),
        "COPPER": get_market_data("HG=F"),
        "PLATINUM": get_market_data("PL=F"),
    }
