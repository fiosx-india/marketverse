"""
=========================================================
MarketVerse AI - Advanced Risk Manager
=========================================================
Dynamic Risk Management
Supports:
- BUY
- SELL
- HOLD
- Position Size
- Capital Protection
=========================================================
"""

DEFAULT_CAPITAL = 100000


def calculate_risk(
    entry_price,
    signal="HOLD",
    confidence=50,
    capital=DEFAULT_CAPITAL,
    risk_percent=2
):
    """
    Calculate Stop Loss, Targets and Position Size.
    """

    signal = signal.upper()

    risk_amount = capital * (risk_percent / 100)

    if signal == "BUY":

        stop_loss = round(entry_price * 0.98, 2)

        target1 = round(entry_price * 1.03, 2)

        target2 = round(entry_price * 1.06, 2)

    elif signal == "SELL":

        stop_loss = round(entry_price * 1.02, 2)

        target1 = round(entry_price * 0.97, 2)

        target2 = round(entry_price * 0.94, 2)

    else:

        return {
            "signal": "HOLD",
            "entry": entry_price,
            "confidence": confidence,
            "message": "No trade"
        }

    risk_per_share = abs(entry_price - stop_loss)

    if risk_per_share == 0:
        quantity = 0
    else:
        quantity = int(risk_amount / risk_per_share)

    expected_profit = round(
        abs(target2 - entry_price) * quantity,
        2
    )

    expected_loss = round(
        risk_per_share * quantity,
        2
    )

    return {

        "signal": signal,

        "confidence": confidence,

        "entry": entry_price,

        "stop_loss": stop_loss,

        "target_1": target1,

        "target_2": target2,

        "quantity": quantity,

        "capital": capital,

        "risk_percent": risk_percent,

        "risk_amount": round(risk_amount, 2),

        "expected_profit": expected_profit,

        "expected_loss": expected_loss,

        "risk_reward": "1:3"

    }
# ==========================================
# Compatibility Wrapper for CentralBrain
# ==========================================

class RiskManager:
    """
    Compatibility wrapper for CentralBrain.
    """

    @staticmethod
    def calculate(
        entry_price,
        signal="HOLD",
        confidence=50,
        capital=DEFAULT_CAPITAL,
        risk_percent=2
    ):
        return calculate_risk(
            entry_price=entry_price,
            signal=signal,
            confidence=confidence,
            capital=capital,
            risk_percent=risk_percent
        )
