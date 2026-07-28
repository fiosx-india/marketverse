"""
MarketVerse - MW Securities F&O

Loads the local MW Securities F&O list.
"""

from pathlib import Path
import pandas as pd

CSV_FILE = Path(__file__).with_name("MW-SECURITIES-IN-F&O-28-Jul-2026.csv")


def load_fno_stocks():

    if not CSV_FILE.exists():
        return []

    df = pd.read_csv(CSV_FILE)

    stocks = []

    for _, row in df.iterrows():

        symbol = str(row["SYMBOL"]).strip()

        stocks.append({
            "name": symbol,
            "symbol": f"{symbol}.NS",
            "sector": row["SECTOR"] if "SECTOR" in df.columns else "Unknown"
        })

    return stocks


FNO_STOCKS = load_fno_stocks()


def get_symbols():
    return [s["symbol"] for s in FNO_STOCKS]


def get_names():
    return [s["name"] for s in FNO_STOCKS]


def get_stock(symbol):
    for stock in FNO_STOCKS:
        if stock["symbol"] == symbol:
            return stock
    return None


def search_stock(keyword):
    keyword = keyword.lower()

    return [
        stock
        for stock in FNO_STOCKS
        if keyword in stock["name"].lower()
        or keyword in stock["symbol"].lower()
    ]


def get_all_sectors():
    return sorted({stock["sector"] for stock in FNO_STOCKS})
