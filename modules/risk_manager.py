"""
=========================================================
MarketVerse AI
Risk Manager
=========================================================

Purpose
-------
Provides risk assessment and trade risk calculations
for the MarketVerse intelligence pipeline.

Responsibilities
----------------
- Stop Loss Calculation
- Target Calculation
- Position Size Calculation
- Capital Protection
- Risk Amount Calculation
- Risk / Reward Assessment

This module does NOT:

- Perform market analysis
- Generate market predictions
- Make the final market decision

CentralBrain:
    Orchestrates the workflow.

Strategy Engine:
    Provides strategy evidence.

RiskManager:
    Evaluates trade risk.

DecisionCore:
    Produces the final intelligence decision.
=========================================================
"""


DEFAULT_CAPITAL = 100000
DEFAULT_RISK_PERCENT = 2


# =========================================================
# CORE RISK CALCULATION
# =========================================================

def calculate_risk(
    entry_price,
    signal="HOLD",
    confidence=50,
    capital=DEFAULT_CAPITAL,
    risk_percent=DEFAULT_RISK_PERCENT
):
    """
    Calculate:

    - Stop Loss
    - Target 1
    - Target 2
    - Position Size
    - Risk Amount
    - Expected Profit
    - Expected Loss
    """

    # -----------------------------------------------------
    # Input Validation
    # -----------------------------------------------------

    try:

        entry_price = float(entry_price)

    except (TypeError, ValueError):

        return {

            "status": "error",

            "message": "Invalid entry price"

        }

    if entry_price <= 0:

        return {

            "status": "error",

            "message": "Entry price must be greater than zero"

        }

    signal = str(
        signal
    ).upper()

    try:

        confidence = float(
            confidence
        )

    except (TypeError, ValueError):

        confidence = 50

    try:

        capital = float(
            capital
        )

    except (TypeError, ValueError):

        capital = DEFAULT_CAPITAL

    try:

        risk_percent = float(
            risk_percent
        )

    except (TypeError, ValueError):

        risk_percent = DEFAULT_RISK_PERCENT

    # -----------------------------------------------------
    # HOLD
    # -----------------------------------------------------

    if signal not in (
        "BUY",
        "SELL"
    ):

        return {

            "status": "success",

            "signal": "HOLD",

            "entry": round(
                entry_price,
                2
            ),

            "confidence": round(
                confidence,
                2
            ),

            "risk_level": "LOW",

            "trade_allowed": False,

            "message": "No active trade strategy"

        }

    # -----------------------------------------------------
    # Risk Amount
    # -----------------------------------------------------

    risk_amount = capital * (
        risk_percent / 100
    )

    # -----------------------------------------------------
    # BUY Risk Calculation
    # -----------------------------------------------------

    if signal == "BUY":

        stop_loss = round(
            entry_price * 0.98,
            2
        )

        target1 = round(
            entry_price * 1.03,
            2
        )

        target2 = round(
            entry_price * 1.06,
            2
        )

    # -----------------------------------------------------
    # SELL Risk Calculation
    # -----------------------------------------------------

    else:

        stop_loss = round(
            entry_price * 1.02,
            2
        )

        target1 = round(
            entry_price * 0.97,
            2
        )

        target2 = round(
            entry_price * 0.94,
            2
        )

    # -----------------------------------------------------
    # Position Size
    # -----------------------------------------------------

    risk_per_unit = abs(
        entry_price - stop_loss
    )

    if risk_per_unit <= 0:

        quantity = 0

    else:

        quantity = int(
            risk_amount / risk_per_unit
        )

    # -----------------------------------------------------
    # Expected Profit / Loss
    # -----------------------------------------------------

    expected_profit = round(

        abs(
            target2 - entry_price
        ) * quantity,

        2

    )

    expected_loss = round(

        risk_per_unit * quantity,

        2

    )

    # -----------------------------------------------------
    # Risk Reward Ratio
    # -----------------------------------------------------

    if expected_loss > 0:

        risk_reward_ratio = round(

            expected_profit /
            expected_loss,

            2

        )

    else:

        risk_reward_ratio = 0

    # -----------------------------------------------------
    # Risk Classification
    # -----------------------------------------------------

    if confidence >= 80:

        risk_level = "LOW"

    elif confidence >= 60:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    # -----------------------------------------------------
    # Final Result
    # -----------------------------------------------------

    return {

        "status": "success",

        "signal": signal,

        "confidence": round(
            confidence,
            2
        ),

        "entry": round(
            entry_price,
            2
        ),

        "stop_loss": stop_loss,

        "target_1": target1,

        "target_2": target2,

        "quantity": quantity,

        "capital": round(
            capital,
            2
        ),

        "risk_percent": round(
            risk_percent,
            2
        ),

        "risk_amount": round(
            risk_amount,
            2
        ),

        "risk_per_unit": round(
            risk_per_unit,
            2
        ),

        "expected_profit": expected_profit,

        "expected_loss": expected_loss,

        "risk_reward_ratio": risk_reward_ratio,

        "risk_level": risk_level,

        "trade_allowed": True

    }


# =========================================================
# RISK MANAGER
# =========================================================

class RiskManager:
    """
    Risk Management Interface.

    Supports:

    1. Direct Risk Calculation
    2. CentralBrain Shared Analysis Evaluation
    """

    # =====================================================
    # DIRECT CALCULATION
    # =====================================================

    @staticmethod
    def calculate(
        entry_price,
        signal="HOLD",
        confidence=50,
        capital=DEFAULT_CAPITAL,
        risk_percent=DEFAULT_RISK_PERCENT
    ):
        """
        Direct risk calculation interface.
        """

        return calculate_risk(

            entry_price=entry_price,

            signal=signal,

            confidence=confidence,

            capital=capital,

            risk_percent=risk_percent

        )

    # =====================================================
    # CENTRAL BRAIN INTEGRATION
    # =====================================================

    def evaluate(
        self,
        analysis
    ):
        """
        Evaluate risk using CentralBrain analysis.

        Expected analysis sections:

        - technical
        - strategy
        - prediction
        - decision

        This method does not make a market decision.

        It only converts existing strategy evidence
        into risk parameters.
        """

        if not isinstance(
            analysis,
            dict
        ):

            return {

                "status": "error",

                "message": (
                    "RiskManager expects "
                    "a dictionary analysis"
                )

            }

        # -------------------------------------------------
        # Read Sections
        # -------------------------------------------------

        technical = analysis.get(

            "technical",

            {}

        ) or {}

        strategy = analysis.get(

            "strategy",

            {}

        ) or {}

        prediction = analysis.get(

            "prediction",

            {}

        ) or {}

        # -------------------------------------------------
        # Entry Price
        # -------------------------------------------------

        entry_price = technical.get(

            "price"

        )

        # Compatibility with alternative structures

        if entry_price is None:

            market = analysis.get(

                "market",

                {}

            ) or {}

            entry_price = market.get(

                "price"

            )

        # -------------------------------------------------
        # No Entry Price
        # -------------------------------------------------

        if entry_price is None:

            return {

                "status": "error",

                "message": (
                    "Entry price unavailable "
                    "for risk calculation"
                )

            }

        # -------------------------------------------------
        # Signal Resolution
        # -------------------------------------------------

        signal = strategy.get(

            "action"

        )

        if not signal:

            signal = strategy.get(

                "decision"

            )

        if not signal:

            signal = prediction.get(

                "signal",

                "HOLD"

            )

        # Normalize strong signals

        signal = str(
            signal
        ).upper()

        if signal == "STRONG BUY":

            signal = "BUY"

        elif signal == "STRONG SELL":

            signal = "SELL"

        # -------------------------------------------------
        # Confidence Resolution
        # -------------------------------------------------

        confidence = strategy.get(

            "confidence"

        )

        if confidence is None:

            confidence = prediction.get(

                "confidence",

                50

            )

        # -------------------------------------------------
        # Risk Calculation
        # -------------------------------------------------

        return calculate_risk(

            entry_price=entry_price,

            signal=signal,

            confidence=confidence

        )
