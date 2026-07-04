"""
=========================================================
MarketVerse AI - Trade Executor
=========================================================
Paper Trading Engine
Future Ready for:
- Zerodha
- Upstox
- Angel One
=========================================================
"""

import json
import os
from datetime import datetime

TRADE_FILE = "trade_history.json"


class TradeExecutor:

    def __init__(self, initial_balance=100000):

        self.balance = initial_balance
        self.positions = {}
        self.history = []

        self.load()

    def load(self):

        if os.path.exists(TRADE_FILE):

            with open(TRADE_FILE, "r") as f:

                data = json.load(f)

                self.balance = data.get("balance", self.balance)
                self.positions = data.get("positions", {})
                self.history = data.get("history", [])

    def save(self):

        with open(TRADE_FILE, "w") as f:

            json.dump(
                {
                    "balance": self.balance,
                    "positions": self.positions,
                    "history": self.history
                },
                f,
                indent=4
            )
