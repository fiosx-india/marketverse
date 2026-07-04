"""
=========================================================
MarketVerse AI - Performance Tracker
=========================================================
Tracks Trading Performance
=========================================================
"""


class PerformanceTracker:

    def __init__(self):

        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0

        self.total_profit = 0.0
        self.total_loss = 0.0

    ####################################################
    # ADD TRADE RESULT
    ####################################################

    def add_trade(self, profit):

        self.total_trades += 1

        if profit >= 0:

            self.winning_trades += 1
            self.total_profit += profit

        else:

            self.losing_trades += 1
            self.total_loss += abs(profit)

    ####################################################
    # WIN RATE
    ####################################################

    def win_rate(self):

        if self.total_trades == 0:
            return 0

        return round(
            (self.winning_trades / self.total_trades) * 100,
            2
        )

    ####################################################
    # NET PROFIT
    ####################################################

    def net_profit(self):

        return round(
            self.total_profit - self.total_loss,
            2
        )

    ####################################################
    # PROFIT FACTOR
    ####################################################

    def profit_factor(self):

        if self.total_loss == 0:
            return float("inf")

        return round(
            self.total_profit / self.total_loss,
            2
        )

    ####################################################
    # SUMMARY
    ####################################################

    def summary(self):

        return {

            "total_trades": self.total_trades,

            "winning_trades": self.winning_trades,

            "losing_trades": self.losing_trades,

            "win_rate": self.win_rate(),

            "total_profit": round(self.total_profit, 2),

            "total_loss": round(self.total_loss, 2),

            "net_profit": self.net_profit(),

            "profit_factor": self.profit_factor()

        }


####################################################
# TEST
####################################################

if __name__ == "__main__":

    tracker = PerformanceTracker()

    tracker.add_trade(1200)
    tracker.add_trade(-350)
    tracker.add_trade(900)
    tracker.add_trade(-200)
    tracker.add_trade(450)

    print(tracker.summary())
