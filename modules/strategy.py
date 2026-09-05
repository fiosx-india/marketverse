"""
=========================================================
MarketVerse AI
Strategy Engine
=========================================================

Purpose
-------
Generates a strategy proposal from evidence already
available in the shared MarketContext.

Strategy Engine does NOT make the final market decision.

CentralBrain:
    Controls pipeline orchestration.

DecisionCore:
    Produces the final market decision.

Strategy Engine:
    Produces strategy evidence and a proposed action.

Architecture
------------

Shared MarketContext
        │
        ▼
Strategy Engine
        │
        ├── Technical Evidence
        ├── Prediction Evidence
        ├── AI Evidence
        ├── News Evidence
        ├── Pattern Evidence
        ├── Volume Evidence
        └── Sentiment Evidence
        │
        ▼
Strategy Proposal
        │
        ▼
Risk Manager
        │
        ▼
DecisionCore
=========================================================
"""


def _normalize_signal(value):
    """
    Convert supported signal formats into:

    BUY
    SELL
    HOLD
    """

    if value is None:
        return "HOLD"

    value = str(value).upper()

    if value in (
        "BUY",
        "STRONG BUY",
        "BULLISH",
        "VERY BULLISH",
        "UP",
        "POSITIVE"
    ):
        return "BUY"

    if value in (
        "SELL",
        "STRONG SELL",
        "BEARISH",
        "VERY BEARISH",
        "DOWN",
        "NEGATIVE"
    ):
        return "SELL"

    return "HOLD"


def _safe_dict(value):
    """
    Return a dictionary safely.
    """

    if isinstance(value, dict):
        return value

    return {}


def _get_confidence(source):
    """
    Safely read confidence.

    Returns None when unavailable.
    """

    if not isinstance(source, dict):
        return None

    value = source.get("confidence")

    if value is None:
        return None

    try:
        value = float(value)

        return max(
            0,
            min(value, 100)
        )

    except (
        TypeError,
        ValueError
    ):
        return None


# =========================================================
# STRATEGY CALCULATION
# =========================================================

def calculate_strategy(
    market=None,
    technical=None,
    prediction=None,
    sentiment=None,
    ai=None,
    news_analysis=None,
    pattern=None,
    volume=None
):
    """
    Generate strategy evidence.

    This function DOES NOT produce the final
    MarketVerse decision.

    It combines available evidence and proposes
    a strategy direction.
    """

    market = _safe_dict(market)

    technical = _safe_dict(technical)

    prediction = _safe_dict(prediction)

    sentiment = _safe_dict(sentiment)

    ai = _safe_dict(ai)

    news_analysis = _safe_dict(news_analysis)

    pattern = _safe_dict(pattern)

    volume = _safe_dict(volume)

    score = 0

    reasons = []

    confidence_sources = []

    # =====================================================
    # PREDICTION EVIDENCE
    # =====================================================

    prediction_signal = _normalize_signal(

        prediction.get(
            "signal"
        )

    )

    if prediction_signal == "BUY":

        score += 30

        reasons.append(
            "Prediction supports bullish movement"
        )

    elif prediction_signal == "SELL":

        score -= 30

        reasons.append(
            "Prediction supports bearish movement"
        )

    prediction_confidence = _get_confidence(
        prediction
    )

    if prediction_confidence is not None:

        confidence_sources.append(
            prediction_confidence
        )

    # =====================================================
    # AI EVIDENCE
    # =====================================================

    ai_signal = _normalize_signal(

        ai.get(
            "signal",

            ai.get(
                "prediction"
            )

        )

    )

    if ai_signal == "BUY":

        score += 20

        reasons.append(
            "AI intelligence supports bullish conditions"
        )

    elif ai_signal == "SELL":

        score -= 20

        reasons.append(
            "AI intelligence supports bearish conditions"
        )

    ai_confidence = _get_confidence(
        ai
    )

    if ai_confidence is not None:

        confidence_sources.append(
            ai_confidence
        )

    # =====================================================
    # TECHNICAL EVIDENCE
    # =====================================================

    technical_signal = _normalize_signal(

        technical.get(
            "signal"
        )

    )

    if technical_signal == "BUY":

        score += 20

        reasons.append(
            "Technical analysis supports bullish movement"
        )

    elif technical_signal == "SELL":

        score -= 20

        reasons.append(
            "Technical analysis supports bearish movement"
        )

    ema20 = technical.get(
        "ema20"
    )

    ema50 = technical.get(
        "ema50"
    )

    if (
        ema20 is not None
        and ema50 is not None
    ):

        try:

            if float(ema20) > float(ema50):

                score += 10

                reasons.append(
                    "EMA trend structure is bullish"
                )

            elif float(ema20) < float(ema50):

                score -= 10

                reasons.append(
                    "EMA trend structure is bearish"
                )

        except (
            TypeError,
            ValueError
        ):

            pass

    macd = technical.get(
        "macd"
    )

    macd_signal = technical.get(
        "macd_signal"
    )

    if (
        macd is not None
        and macd_signal is not None
    ):

        try:

            if float(macd) > float(macd_signal):

                score += 5

                reasons.append(
                    "MACD momentum is bullish"
                )

            elif float(macd) < float(macd_signal):

                score -= 5

                reasons.append(
                    "MACD momentum is bearish"
                )

        except (
            TypeError,
            ValueError
        ):

            pass

    rsi = technical.get(
        "rsi"
    )

    if rsi is not None:

        try:

            rsi = float(rsi)

            if rsi < 30:

                score += 5

                reasons.append(
                    "RSI indicates oversold conditions"
                )

            elif rsi > 70:

                score -= 5

                reasons.append(
                    "RSI indicates overbought conditions"
                )

        except (
            TypeError,
            ValueError
        ):

            pass

    technical_confidence = _get_confidence(
        technical
    )

    if technical_confidence is not None:

        confidence_sources.append(
            technical_confidence
        )

    # =====================================================
    # MARKET DATA EVIDENCE
    # =====================================================

    change_percent = market.get(
        "change_percent"
    )

    if change_percent is not None:

        try:

            change_percent = float(
                change_percent
            )

            if change_percent > 0:

                score += 5

                reasons.append(
                    "Market price movement is positive"
                )

            elif change_percent < 0:

                score -= 5

                reasons.append(
                    "Market price movement is negative"
                )

        except (
            TypeError,
            ValueError
        ):

            pass

    # =====================================================
    # SENTIMENT EVIDENCE
    # =====================================================

    sentiment_signal = _normalize_signal(

        sentiment.get(
            "signal",

            sentiment.get(
                "sentiment"
            )

        )

    )

    if sentiment_signal == "BUY":

        score += 10

        reasons.append(
            "Market sentiment is bullish"
        )

    elif sentiment_signal == "SELL":

        score -= 10

        reasons.append(
            "Market sentiment is bearish"
        )

    sentiment_confidence = _get_confidence(
        sentiment
    )

    if sentiment_confidence is not None:

        confidence_sources.append(
            sentiment_confidence
        )

    # =====================================================
    # NEWS ANALYSIS EVIDENCE
    # =====================================================

    news_signal = _normalize_signal(

        news_analysis.get(
            "sentiment"
        )

    )

    if news_signal == "BUY":

        score += 10

        reasons.append(
            "News analysis is positive"
        )

    elif news_signal == "SELL":

        score -= 10

        reasons.append(
            "News analysis is negative"
        )

    news_confidence = _get_confidence(
        news_analysis
    )

    if news_confidence is not None:

        confidence_sources.append(
            news_confidence
        )

    # =====================================================
    # PATTERN EVIDENCE
    # =====================================================

    if pattern.get(
        "bullish"
    ):

        score += 5

        reasons.append(
            "Bullish market pattern detected"
        )

    if pattern.get(
        "bearish"
    ):

        score -= 5

        reasons.append(
            "Bearish market pattern detected"
        )

    # =====================================================
    # VOLUME EVIDENCE
    # =====================================================

    volume_signal = _normalize_signal(

        volume.get(
            "signal"
        )

    )

    if volume_signal == "BUY":

        score += 5

        reasons.append(
            "Volume supports bullish movement"
        )

    elif volume_signal == "SELL":

        score -= 5

        reasons.append(
            "Volume supports bearish movement"
        )

    # =====================================================
    # STRATEGY CLASSIFICATION
    # =====================================================

    if score >= 60:

        decision = "STRONG BUY"

        action = "BUY"

        strength = "STRONG"

    elif score >= 25:

        decision = "BUY"

        action = "BUY"

        strength = "NORMAL"

    elif score <= -60:

        decision = "STRONG SELL"

        action = "SELL"

        strength = "STRONG"

    elif score <= -25:

        decision = "SELL"

        action = "SELL"

        strength = "NORMAL"

    else:

        decision = "HOLD"

        action = "HOLD"

        strength = "NEUTRAL"

    # =====================================================
    # STRATEGY CONFIDENCE
    # =====================================================

    evidence_confidence = min(

        50
        +
        abs(score) * 0.5,

        95

    )

    if confidence_sources:

        source_confidence = (

            sum(
                confidence_sources
            )

            /

            len(
                confidence_sources
            )

        )

        confidence = (

            evidence_confidence
            +
            source_confidence

        ) / 2

    else:

        confidence = evidence_confidence

    confidence = round(

        max(

            0,

            min(
                confidence,
                100
            )

        ),

        2

    )

    # =====================================================
    # DEFAULT REASON
    # =====================================================

    if not reasons:

        reasons.append(

            "Insufficient directional evidence"

        )

    # =====================================================
    # RETURN STRATEGY PROPOSAL
    # =====================================================

    return {

        "status": "success",

        "action": action,

        "strength": strength,

        "decision": decision,

        "score": score,

        "confidence": confidence,

        "reasons": reasons,

        "evidence_count": len(
            reasons
        )

    }


# =========================================================
# CENTRAL BRAIN INTEGRATION
# =========================================================

def generate_strategy(
    analysis,
    sentiment=None,
    prediction=None
):
    """
    Strategy interface.

    Supports:

    1. CentralBrain Shared MarketContext dictionary.

    2. Legacy calling style:

       generate_strategy(
           technical,
           sentiment,
           prediction
       )
    """

    # =====================================================
    # CENTRAL BRAIN MODE
    # =====================================================

    if isinstance(
        analysis,
        dict
    ):

        # -------------------------------------------------
        # SHARED MARKET CONTEXT
        # -------------------------------------------------

        technical = _safe_dict(

            analysis.get(
                "technical"
            )

        )

        prediction_data = _safe_dict(

            analysis.get(
                "prediction"
            )

        )

        sentiment_data = _safe_dict(

            analysis.get(
                "sentiment",

                analysis.get(
                    "news_analysis",
                    {}
                )

            )

        )

        ai_data = _safe_dict(

            analysis.get(
                "ai"
            )

        )

        news_data = _safe_dict(

            analysis.get(
                "news_analysis"
            )

        )

        pattern_data = _safe_dict(

            analysis.get(
                "pattern"
            )

        )

        volume_data = _safe_dict(

            analysis.get(
                "volume"
            )

        )

        # -------------------------------------------------
        # MARKET DATA RESOLUTION
        # -------------------------------------------------

        market_data = analysis.get(
            "market_data"
        )

        market = {}

        # DataFrame is intentionally not passed directly
        # into the strategy engine.

        if isinstance(
            market_data,
            dict
        ):

            market = market_data

        # -------------------------------------------------
        # LEGACY MARKET COMPATIBILITY
        # -------------------------------------------------

        if not market:

            market = _safe_dict(

                analysis.get(
                    "market"
                )

            )

        # -------------------------------------------------
        # FALLBACK MARKET INFORMATION
        # -------------------------------------------------

        if not market:

            market = {

                "price":

                    technical.get(
                        "price",
                        0
                    ),

                "change_percent":

                    technical.get(
                        "change_percent",
                        0
                    )

            }

        # -------------------------------------------------
        # CALCULATE STRATEGY
        # -------------------------------------------------

        return calculate_strategy(

            market=market,

            technical=technical,

            prediction=prediction_data,

            sentiment=sentiment_data,

            ai=ai_data,

            news_analysis=news_data,

            pattern=pattern_data,

            volume=volume_data

        )

    # =====================================================
    # LEGACY COMPATIBILITY MODE
    # =====================================================

    technical = _safe_dict(
        analysis
    )

    sentiment_data = _safe_dict(
        sentiment
    )

    prediction_data = _safe_dict(
        prediction
    )

    return calculate_strategy(

        market={},

        technical=technical,

        prediction=prediction_data,

        sentiment=sentiment_data

            )
