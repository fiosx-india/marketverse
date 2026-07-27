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

        self._initialized = False

    def _initialize(self):
        """
        Create NSE session only once.
        """

        if self._initialized:
            return

        response = self.session.get(
            self.BASE_URL,
            timeout=10
        )

        print("Connecting to NSE...")
        print("Status Code:", response.status_code)
        
        if response.status_code == 200:
            self._initialized = True
            return True

        print(f"NSE unavailable (HTTP {response.status_code})")
        self._initialized = False
        return False
        
    def get_fno_symbols(self):
        """
        Returns

        [
            "RELIANCE.NS",
            "SBIN.NS",
            ...
        ]
        """
        try:

            self._initialize()

            if not self._initialized:
                return []

            response = self.session.get(
                self.FNO_API,
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            if "data" not in data:
                return []

            symbols = []

            for row in data.get("data", []):

                symbol = row.get("symbol")

                if symbol:
                    symbols.append(symbol + ".NS")

            return sorted(list(set(symbols)))

        except requests.exceptions.RequestException:

            return []

    def is_connected(self):

        try:
            return bool(self._initialize())

        except requests.exceptions.RequestException:
            return False

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

# ============================================================
# Lazy Singleton
# ============================================================

_nse = None


def get_nse():
    """
    Returns singleton NSEService.
    Creates it only when required.
    """

    global _nse

    if _nse is None:

        _nse = NSEService()

    return _nse


# ============================================================
# Standalone Test
# ============================================================

if __name__ == "__main__":

    nse = get_nse()

    print("=" * 50)

    print("NSE Connected :", nse.is_connected())

    print("=" * 50)

    stocks = nse.get_fno_symbols()

    if stocks:

        print("Total F&O :", len(stocks))

        print(stocks[:20])

    else:

        print("Unable to fetch F&O symbols.")
