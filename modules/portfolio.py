"""
MarketVerse AI - Portfolio Manager
"""

from datetime import datetime


class Portfolio:

    def __init__(self):
        self.holdings = {}

    def add_stock(self, symbol, quantity, buy_price=0):
        symbol = symbol.upper()

        if symbol not in self.holdings:
            self.holdings[symbol] = {
                "quantity": 0,
                "buy_price": buy_price,
                "added": str(datetime.now())
            }

        self.holdings[symbol]["quantity"] += quantity

        if buy_price > 0:
            self.holdings[symbol]["buy_price"] = buy_price

    def remove_stock(self, symbol):
        symbol = symbol.upper()

        if symbol in self.holdings:
            del self.holdings[symbol]

    def update_price(self, symbol, price):
        symbol = symbol.upper()

        if symbol in self.holdings:
            self.holdings[symbol]["current_price"] = price

    def get_stock(self, symbol):
        return self.holdings.get(symbol.upper())

    def get_portfolio(self):
        return self.holdings

    def total_value(self):
        total = 0

        for stock in self.holdings.values():

            qty = stock.get("quantity", 0)
            price = stock.get(
                "current_price",
                stock.get("buy_price", 0)
            )

            total += qty * price

        return round(total, 2)

    def total_profit(self):

        profit = 0

        for stock in self.holdings.values():

            qty = stock.get("quantity", 0)

            buy = stock.get("buy_price", 0)

            current = stock.get(
                "current_price",
                buy
            )

            profit += (current - buy) * qty

        return round(profit, 2)

    def summary(self):

        return {
            "stocks": len(self.holdings),
            "value": self.total_value(),
            "profit": self.total_profit()
        }

    def clear(self):
        self.holdings.clear()
