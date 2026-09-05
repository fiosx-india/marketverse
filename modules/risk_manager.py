"""
=========================================================
MarketVerse AI
Risk Manager
=========================================================

Purpose
-------
Provides risk assessment and trade risk calculations
for the MarketVerse AI intelligence pipeline.

RiskManager converts existing intelligence and strategy
evidence into risk information.

Responsibilities
----------------
- Validate trade eligibility
- Resolve entry price
- Calculate stop loss
- Calculate targets
- Calculate position size
- Calculate risk amount
- Calculate risk / reward
- Assess risk level

RiskManager DOES NOT:
- Fetch market data
- Perform market analysis
- Generate predictions
- Generate strategies
- Make the final market decision
- Orchestrate the pipeline

Architecture
------------

CentralBrain
    │
    ▼
Shared MarketContext
    │
    ├── Technical
    ├── Prediction
    ├── AI
    └── Strategy
            │
            ▼
        RiskManager
            │
            ▼
      Risk Assessment
            │
            ▼
       DecisionCore
=========================================================
"""

DEFAULT_CAPITAL = 100000
DEFAULT_RISK_PERCENT = 2


# =========================================================
# SAFE HELPERS
# =========================================================

def _safe_dict(value):
    """Return a dictionary safely."""

    if isinstance(value, dict):
        return value

    return {}


def _safe_number(value, default=None):
    """Convert a value to float safely."""

    try:

        if value is None:
            return default

        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return default


def _normalize_signal(signal):
    """
    Normalize supported signals.

    Returns:
        BUY / SELL / HOLD
    """

    if signal is None:
        return "HOLD"

    signal = str(signal).upper().strip()

    if signal in (
        "BUY",
        "STRONG BUY",
        "LONG",
        "BULLISH",
        "VERY BULLISH",
        "UP"
    ):
        return "BUY"

    if signal in (
        "SELL",
        "STRONG SELL",
        "SHORT",
        "BEARISH",
        "VERY BEARISH",
        "DOWN"
    ):
        return "SELL"

    return "HOLD"


# =========================================================
# DATAFRAME PRICE RESOLUTION
# =========================================================

def _extract_dataframe_price(market_data):
    """
    Extract latest closing price from a
    pandas DataFrame without making pandas
    a direct dependency of this module.
    """

    try:

        if market_data is None:
            return None

        if not hasattr(market_data, "empty"):
            return None

        if market_data.empty:
            return None

        if "Close" in market_data.columns:

            return _safe_number(
                market_data["Close"].iloc[-1]
            )

        if "close" in market_data.columns:

            return _safe_number(
                market_data["close"].iloc[-1]
            )

    except Exception:

        return None

    return None


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
    Calculate risk parameters.

    Returns:
    - Entry
    - Stop Loss
    - Target 1
    - Target 2
    - Position Size
    - Risk Amount
    - Expected Profit
    - Expected Loss
    - Risk Reward Ratio
    """

    # =====================================================
    # INPUT VALIDATION
    # =====================================================

    entry_price = _safe_number(entry_price)

    if (
        entry_price is None
        or entry_price <= 0
    ):

        return {

            "status": "error",

            "trade_allowed": False,

            "risk_level": "UNKNOWN",

            "message": (
                "Valid entry price unavailable "
                "for risk calculation"
            )

        }

    signal = _normalize_signal(signal)

    confidence = _safe_number(
        confidence,
        50
    )

    confidence = max(
        0,
        min(
            confidence,
            100
        )
    )

    capital = _safe_number(
        capital,
        DEFAULT_CAPITAL
    )

    if capital <= 0:

        capital = DEFAULT_CAPITAL

    risk_percent = _safe_number(
        risk_percent,
        DEFAULT_RISK_PERCENT
    )

    if risk_percent <= 0:

        risk_percent = DEFAULT_RISK_PERCENT

    # =====================================================
    # HOLD
    # =====================================================

    if signal == "HOLD":

        return {

            "status": "success",

            "signal": "HOLD",

            "confidence": round(
                confidence,
                2
            ),

            "entry": round(
                entry_price,
                2
            ),

            "risk_level": "LOW",

            "trade_allowed": False,

            "message": (
                "No active trade strategy"
            )

        }

    # =====================================================
    # RISK AMOUNT
    # =====================================================

    risk_amount = capital * (
        risk_percent / 100
    )

    # =====================================================
    # BUY
    # =====================================================

    if signal == "BUY":

        stop_loss = entry_price * 0.98

        target1 = entry_price * 1.03

        target2 = entry_price * 1.06

    # =====================================================
    # SELL
    # =====================================================

    else:

        stop_loss = entry_price * 1.02

        target1 = entry_price * 0.97

        target2 = entry_price * 0.94

    # =====================================================
    # POSITION SIZE
    # =====================================================

    risk_per_unit = abs(
        entry_price - stop_loss
    )

    if risk_per_unit <= 0:

        quantity = 0

    else:

        quantity = int(
            risk_amount / risk_per_unit
        )

    # =====================================================
    # EXPECTED PROFIT / LOSS
    # =====================================================

    expected_profit = abs(
        target2 - entry_price
    ) * quantity

    expected_loss = (
        risk_per_unit * quantity
    )

    # =====================================================
    # RISK REWARD
    # =====================================================

    if expected_loss > 0:

        risk_reward_ratio = (
            expected_profit /
            expected_loss
        )

    else:

        risk_reward_ratio = 0

    # =====================================================
    # RISK LEVEL
    # =====================================================

    if confidence >= 80:

        risk_level = "LOW"

    elif confidence >= 60:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    # =====================================================
    # TRADE ELIGIBILITY
    # =====================================================

    trade_allowed = (

        signal in (
            "BUY",
            "SELL"
        )

        and quantity > 0

    )

    # =====================================================
    # RETURN RESULT
    # =====================================================

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

        "stop_loss": round(
            stop_loss,
            2
        ),

        "target_1": round(
            target1,
            2
        ),

        "target_2": round(
            target2,
            2
        ),

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

        "expected_profit": round(
            expected_profit,
            2
        ),

        "expected_loss": round(
            expected_loss,
            2
        ),

        "risk_reward_ratio": round(
            risk_reward_ratio,
            2
        ),

        "risk_level": risk_level,

        "trade_allowed": trade_allowed

    }


# =========================================================
# RISK MANAGER
# =========================================================

class RiskManager:
    """
    Risk Management interface.

    Supports:

    1. Direct calculation
    2. CentralBrain Shared MarketContext evaluation
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

        return calculate_risk(

            entry_price=entry_price,

            signal=signal,

            confidence=confidence,

            capital=capital,

            risk_percent=risk_percent

        )

    # =====================================================
    # CENTRAL BRAIN EVALUATION
    # =====================================================

    def evaluate(
        self,
        analysis
    ):
        """
        Evaluate risk using existing
        Shared MarketContext evidence.

        Signal priority:

        Strategy
            ↓
        Prediction
            ↓
        AI

        Entry price priority:

        Technical price
            ↓
        Market Data Dictionary
            ↓
        Market Data DataFrame
            ↓
        Legacy Market price
        """

        if not isinstance(
            analysis,
            dict
        ):

            return {

                "status": "error",

                "trade_allowed": False,

                "risk_level": "UNKNOWN",

                "message": (
                    "RiskManager expects "
                    "Shared MarketContext dictionary"
                )

            }

        # =================================================
        # READ CONTEXT SECTIONS
        # =================================================

        technical = _safe_dict(
            analysis.get("technical")
        )

        strategy = _safe_dict(
            analysis.get("strategy")
        )

        prediction = _safe_dict(
            analysis.get("prediction")
        )

        ai = _safe_dict(
            analysis.get("ai")
        )

        market_data = analysis.get(
            "market_data"
        )

        market = _safe_dict(
            analysis.get("market")
        )

        # =================================================
        # ENTRY PRICE
        # =================================================

        entry_price = technical.get(
            "price"
        )

        # -------------------------------------------------
        # MARKET DATA DICTIONARY
        # -------------------------------------------------

        if entry_price is None:

            if isinstance(
                market_data,
                dict
            ):

                entry_price = market_data.get(
                    "price"
                )

        # -------------------------------------------------
        # MARKET DATA DATAFRAME
        # -------------------------------------------------

        if entry_price is None:

            entry_price = _extract_dataframe_price(
                market_data
            )

        # -------------------------------------------------
        # LEGACY MARKET
        # -------------------------------------------------

        if entry_price is None:

            entry_price = market.get(
                "price"
            )

        # =================================================
        # VALIDATE ENTRY
        # =================================================

        entry_price = _safe_number(
            entry_price
        )

        if (
            entry_price is None
            or entry_price <= 0
        ):

            return {

                "status": "error",

                "trade_allowed": False,

                "risk_level": "UNKNOWN",

                "message": (
                    "Entry price unavailable "
                    "from MarketContext"
                )

            }

        # =================================================
        # SIGNAL RESOLUTION
        # =================================================

        signal = strategy.get(
            "action"
        )

        if not signal:

            signal = strategy.get(
                "decision"
            )

        if not signal:

            signal = prediction.get(
                "signal"
            )

        if not signal:

            signal = ai.get(
                "signal"
            )

        if not signal:

            signal = ai.get(
                "prediction"
            )

        signal = _normalize_signal(
            signal
        )

        # =================================================
        # CONFIDENCE RESOLUTION
        # =================================================

        confidence = strategy.get(
            "confidence"
        )

        if confidence is None:

            confidence = prediction.get(
                "confidence"
            )

        if confidence is None:

            confidence = ai.get(
                "confidence"
            )

        if confidence is None:

            confidence = 50

        # =================================================
        # RISK CALCULATION
        # =================================================

        return calculate_risk(

            entry_price=entry_price,

            signal=signal,

            confidence=confidence

        )
