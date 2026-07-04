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
    ####################################################
    # BUY ORDER
    ####################################################

    def buy(self, symbol, quantity, price):

        symbol = symbol.upper()

        cost = quantity * price

        if cost > self.balance:

            return {
                "success": False,
                "message": "Insufficient Balance"
            }

        self.balance -= cost

        if symbol not in self.positions:

            self.positions[symbol] = {
                "quantity": 0,
                "avg_price": 0
            }

        old_qty = self.positions[symbol]["quantity"]
        old_avg = self.positions[symbol]["avg_price"]

        new_qty = old_qty + quantity

        avg_price = (
            (old_qty * old_avg) +
            (quantity * price)
        ) / new_qty

        self.positions[symbol]["quantity"] = new_qty
        self.positions[symbol]["avg_price"] = round(avg_price, 2)

        self.history.append({
            "time": str(datetime.now()),
            "type": "BUY",
            "symbol": symbol,
            "quantity": quantity,
            "price": price
        })

        self.save()

        return {
            "success": True,
            "balance": round(self.balance, 2)
        }

    ####################################################
    # SELL ORDER
    ####################################################

    def sell(self, symbol, quantity, price):

        symbol = symbol.upper()

        if symbol not in self.positions:

            return {
                "success": False,
                "message": "No Position"
            }

        if quantity > self.positions[symbol]["quantity"]:

            return {
                "success": False,
                "message": "Insufficient Quantity"
            }

        self.positions[symbol]["quantity"] -= quantity

        self.balance += quantity * price

        self.history.append({
            "time": str(datetime.now()),
            "type": "SELL",
            "symbol": symbol,
            "quantity": quantity,
            "price": price
        })

        if self.positions[symbol]["quantity"] == 0:
            del self.positions[symbol]

        self.save()

        return {
            "success": True,
            "balance": round(self.balance, 2)
        }
