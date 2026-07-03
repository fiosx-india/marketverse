def calculate_risk(entry_price):
    stop_loss = round(entry_price * 0.98, 2)
    take_profit_1 = round(entry_price * 1.03, 2)
    take_profit_2 = round(entry_price * 1.06, 2)

    return {
        "entry": entry_price,
        "stop_loss": stop_loss,
        "take_profit_1": take_profit_1,
        "take_profit_2": take_profit_2,
        "risk_reward": "1:3"
    }
