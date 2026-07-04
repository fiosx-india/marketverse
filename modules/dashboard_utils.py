"""
=========================================================
MarketVerse AI - Dashboard Utilities
=========================================================
Helper functions for Streamlit Dashboard
=========================================================
"""


def signal_color(signal):
    """
    Return color based on trading signal.
    """

    signal = signal.upper()

    if signal == "BUY":
        return "green"

    elif signal == "SELL":
        return "red"

    return "orange"


def confidence_level(confidence):
    """
    Return confidence category.
    """

    if confidence >= 80:
        return "Very High"

    elif confidence >= 70:
        return "High"

    elif confidence >= 60:
        return "Medium"

    return "Low"


def risk_level(risk_reward):
    """
    Risk level display.
    """

    if risk_reward == "1:3":
        return "Low Risk"

    elif risk_reward == "1:2":
        return "Medium Risk"

    return "High Risk"


def profit_color(value):
    """
    Profit / Loss color.
    """

    if value > 0:
        return "green"

    elif value < 0:
        return "red"

    return "gray"


def market_status(change_percent):
    """
    Market trend.
    """

    if change_percent >= 1:
        return "Bullish"

    elif change_percent <= -1:
        return "Bearish"

    return "Sideways"


def dashboard_summary(
    signal,
    confidence,
    risk_reward,
    profit
):
    """
    Dashboard summary.
    """

    return {

        "signal": signal,

        "signal_color": signal_color(signal),

        "confidence": confidence,

        "confidence_level": confidence_level(confidence),

        "risk": risk_level(risk_reward),

        "profit_color": profit_color(profit)

    }


#########################################################
# TEST
#########################################################

if __name__ == "__main__":

    print(
        dashboard_summary(
            "BUY",
            86,
            "1:3",
            1250
        )
    )
