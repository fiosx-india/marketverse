class Portfolio:
    def __init__(self):
        self.holdings = {}

    def add_stock(self, symbol, quantity):
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity

    def remove_stock(self, symbol):
        if symbol in self.holdings:
            del self.holdings[symbol]

    def get_portfolio(self):
        return self.holdings
