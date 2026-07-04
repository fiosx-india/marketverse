"""
=========================================================
MarketVerse AI - Watchlist Manager
=========================================================
Manage favourite Stocks, Crypto, Forex and Commodities.
=========================================================
"""

import json
import os

WATCHLIST_FILE = "watchlist.json"


def load_watchlist():
    """
    Load watchlist from file.
    """

    if not os.path.exists(WATCHLIST_FILE):
        return {
            "stocks": [],
            "crypto": [],
            "forex": [],
            "commodities": []
        }

    with open(WATCHLIST_FILE, "r") as file:
        return json.load(file)


def save_watchlist(data):
    """
    Save watchlist.
    """

    with open(WATCHLIST_FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_symbol(category, symbol):
    """
    Add symbol to watchlist.
    """

    data = load_watchlist()

    if category not in data:
        data[category] = []

    symbol = symbol.upper()

    if symbol not in data[category]:
        data[category].append(symbol)

    save_watchlist(data)

    return data


def remove_symbol(category, symbol):
    """
    Remove symbol.
    """

    data = load_watchlist()

    symbol = symbol.upper()

    if category in data and symbol in data[category]:
        data[category].remove(symbol)

    save_watchlist(data)

    return data


def get_symbols(category):
    """
    Get symbols from category.
    """

    data = load_watchlist()

    return data.get(category, [])


def clear_watchlist():
    """
    Remove everything.
    """

    data = {
        "stocks": [],
        "crypto": [],
        "forex": [],
        "commodities": []
    }

    save_watchlist(data)

    return data


def total_symbols():
    """
    Returns total watchlist count.
    """

    data = load_watchlist()

    total = 0

    for symbols in data.values():
        total += len(symbols)

    return total


if __name__ == "__main__":

    add_symbol("stocks", "RELIANCE")
    add_symbol("stocks", "TCS")
    add_symbol("crypto", "BTC-USD")
    add_symbol("forex", "USDINR=X")
    add_symbol("commodities", "GC=F")

    print(load_watchlist())
    print("Total Symbols:", total_symbols())
