"""
=========================================================
MarketVerse AI - Backtesting Engine
=========================================================
Tests trading strategy using historical market data.
=========================================================
"""

import pandas as pd


def run_backtest(df):
    """
    Run simple strategy backtest.
    Returns performance statistics.
    """

    if df is None or df.empty or len(df) < 2:
        return {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0,
            "net_profit": 0,
            "average_return": 0,
            "max_drawdown": 0,
            "profit_factor": 0
        }

    trades = []
    capital = 100000
    peak = capital
    max_drawdown = 0

    for i in range(1, len(df)):

        previous = float(df["Close"].iloc[i - 1])
        current = float(df["Close"].iloc[i])

        trade_return = ((current - previous) / previous) * 100
        trades.append(trade_return)

        capital *= (1 + trade_return / 100)

        if capital > peak:
            peak = capital

        drawdown = ((peak - capital) / peak) * 100

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    wins = len([x for x in trades if x > 0])
    losses = len([x for x in trades if x <= 0])

    total_trades = len(trades)

    win_rate = (
        round((wins / total_trades) * 100, 2)
        if total_trades else 0
    )

    net_profit = round(capital - 100000, 2)

    average_return = (
        round(sum(trades) / total_trades, 2)
        if total_trades else 0
    )

    gross_profit = sum(x for x in trades if x > 0)
    gross_loss = abs(sum(x for x in trades if x < 0))

    if gross_loss == 0:
        profit_factor = gross_profit
    else:
        profit_factor = round(
            gross_profit / gross_loss,
            2
        )

    return {
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "net_profit": net_profit,
        "average_return": average_return,
        "max_drawdown": round(max_drawdown, 2),
        "profit_factor": profit_factor,
        "final_capital": round(capital, 2)
    }


def print_report(result):
    """
    Display backtest report.
    """

    print("=" * 50)
    print("MarketVerse AI Backtest Report")
    print("=" * 50)

    print(f"Total Trades   : {result['total_trades']}")
    print(f"Wins           : {result['wins']}")
    print(f"Losses         : {result['losses']}")
    print(f"Win Rate       : {result['win_rate']} %")
    print(f"Net Profit     : ₹{result['net_profit']}")
    print(f"Average Return : {result['average_return']} %")
    print(f"Max Drawdown   : {result['max_drawdown']} %")
    print(f"Profit Factor  : {result['profit_factor']}")
    print(f"Final Capital  : ₹{result['final_capital']}")

    print("=" * 50)


if __name__ == "__main__":

    data = pd.DataFrame({
        "Close": [
            100,
            102,
            101,
            105,
            107,
            106,
            110,
            112,
            111,
            115
        ]
    })

    result = run_backtest(data)

    print_report(result)
