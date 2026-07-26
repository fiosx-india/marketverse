"""
MarketVerse - NSE Service
--------------------------------
Loads the current NSE F&O stock universe.

Author : MarketVerse
"""

from __future__ import annotations

import time
import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}


class NSEService:
    """
    Central NSE Service

    Responsible for:
        • NSE session
        • F&O list
        • Future expansion
    """

    BASE_URL = "https://www.nseindia.com"

    FNO_API = (
        "https://www.nseindia.com/api/liveEquity-derivatives"
    )

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update(HEADERS)

        self._initialize()

    def _initialize(self):
        """
        Create NSE session
        """

        self.session.get(
            self.BASE_URL,
            timeout=10
        )

    def get_fno_symbols(self):
        """
        Returns

        [
            "RELIANCE.NS",
            "SBIN.NS",
            ...
        ]
        """

        response = self.session.get(
            self.FNO_API,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        symbols = []

        for row in data.get("data", []):

            symbol = row.get("symbol")

            if symbol:
                symbols.append(symbol + ".NS")

        return sorted(list(set(symbols)))

    def is_connected(self):

        try:

            self.session.get(
                self.BASE_URL,
                timeout=5
            )

            return True

        except Exception:

            return False

    def retry_connection(
        self,
        retries=3
    ):

        for _ in range(retries):

            if self.is_connected():

                return True

            time.sleep(2)

        return False


# Singleton

nse = NSEService()


if __name__ == "__main__":

    print("=" * 50)

    print("NSE Connected :", nse.is_connected())

    print("=" * 50)

    stocks = nse.get_fno_symbols()

    print("Total F&O :", len(stocks))

    print(stocks[:20])
