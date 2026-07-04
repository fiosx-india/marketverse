import json
import os

PORTFOLIO_FILE = "portfolio.json"


class Portfolio:

    def __init__(self):
        self.holdings = self.load()

    def load(self):
        if os.path.exists(PORTFOLIO_FILE):
            with open(PORTFOLIO_FILE, "r") as f:
                return json.load(f)
        return {}

    def save(self):
        with open(PORTFOLIO_FILE, "w") as f:
            json.dump(self.holdings, f, indent=4)

    def add_stock(self, symbol, quantity, buy_price):

        symbol = symbol.upper()

        if symbol in self.holdings:

            old_qty = self.holdings[symbol]["quantity"]
            old_price = self.holdings[symbol]["buy_price"]

            new_qty = old_qty + quantity

            avg_price = (
                old_qty * old_price +
                quantity * buy_price
            ) / new_qty

            self.holdings[symbol] = {
                "quantity": new_qty,
                "buy_price": round(avg_price, 2)
            }

        else:

            self.holdings[symbol] = {
                "quantity": quantity,
                "buy_price": buy_price
            }

        self.save()

    def remove_stock(self, symbol):

        symbol = symbol.upper()

        if symbol in self.holdings:
            del self.holdings[symbol]
            self.save()

    def update_quantity(self, symbol, quantity):

        symbol = symbol.upper()

        if symbol in self.holdings:
            self.holdings[symbol]["quantity"] = quantity
            self.save()

    def get_stock(self, symbol):

        return self.holdings.get(symbol.upper())

    def get_portfolio(self):

        return self.holdings

    def calculate_value(self, prices):

        total_value = 0

        details = {}

        for symbol, data in self.holdings.items():

            qty = data["quantity"]
            buy_price = data["buy_price"]

            current_price = prices.get(symbol, buy_price)

            invested = qty * buy_price
            current = qty * current_price

            profit = current - invested
            percent = (
                profit / invested * 100
                if invested else 0
            )

            total_value += current

            details[symbol] = {
                "quantity": qty,
                "buy_price": buy_price,
                "current_price": current_price,
                "invested": round(invested, 2),
                "current_value": round(current, 2),
                "profit": round(profit, 2),
                "profit_percent": round(percent, 2)
            }

        return {
            "portfolio_value": round(total_value, 2),
            "stocks": details
        }
