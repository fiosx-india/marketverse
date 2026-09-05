"""
=========================================================
MarketVerse AI
AI Intelligence Engine
=========================================================

Purpose
-------
Transforms intelligence evidence into a unified AI
analysis result.

Responsibilities
----------------
- Combine available intelligence evidence
- Evaluate bullish evidence
- Evaluate bearish evidence
- Produce AI confidence
- Produce explainable AI reasoning
- Report supporting and conflicting evidence

This module does NOT:
- Fetch market data independently
- Orchestrate the intelligence workflow
- Calculate risk
- Generate trading strategy
- Make the final market decision

Architecture
------------

CentralBrain
    │
    ├── Market Data
    ├── Technical Analysis
    ├── News Analysis
    ├── Sentiment
    └── Prediction
            │
            ▼
      AI Intelligence Engine
            │
            ▼
      AI Evidence
            │
            ▼
      Strategy Engine
            │
            ▼
        RiskManager
            │
            ▼
       DecisionCore
=========================================================
"""


def _normalize_signal(signal):
    """
    Normalize different signal formats.
    """

    if not signal:
        return "HOLD"

    signal = str(signal).upper()

    if signal in (
        "STRONG BUY",
        "BUY",
        "BULLISH",
        "UP"
    ):
        return "BUY"

    if signal in (
        "STRONG SELL",
        "SELL",
        "BEARISH",
        "DOWN"
    ):
        return "SELL"

    return "HOLD"


def _safe_confidence(value, default=50):
    """
    Safely normalize confidence.
    """

    try:

        confidence = float(value)

        return max(
            0,
            min(confidence, 100)
        )

    except (
        TypeError,
        ValueError
    ):

        return default


def analyze(symbol=None, evidence=None):
    """
    Generate AI intelligence evidence.

    Parameters
    ----------

    symbol:
        Market symbol.

    evidence:
        Shared intelligence evidence dictionary.

    Expected sections:

        {
            "technical": {},
            "prediction": {},
            "news_analysis": {},
            "sentiment": {},
            "pattern": {},
            "volume": {}
        }

    CentralBrain should provide the evidence.

    This function does NOT orchestrate the pipeline.
    """

    evidence = evidence or {}

    # =====================================================
    # READ EVIDENCE
    # =====================================================

    technical = evidence.get(
        "technical",
        {}
    ) or {}

    prediction = evidence.get(
        "prediction",
        {}
    ) or {}

    news_analysis = evidence.get(
        "news_analysis",
        {}
    ) or {}

    sentiment = evidence.get(
        "sentiment",
        {}
    ) or {}

    pattern = evidence.get(
        "pattern",
        {}
    ) or {}

    volume = evidence.get(
        "volume",
        {}
    ) or {}

    # =====================================================
    # AI SCORING
    # =====================================================

    bullish_score = 0
    bearish_score = 0

    supporting_evidence = []
    conflicting_evidence = []

    confidence_sources = []

    # =====================================================
    # TECHNICAL EVIDENCE
    # =====================================================

    technical_signal = _normalize_signal(
        technical.get(
            "signal"
        )
    )

    if technical_signal == "BUY":

        bullish_score += 2

        supporting_evidence.append(
            "Technical analysis is bullish"
        )

    elif technical_signal == "SELL":

        bearish_score += 2

        conflicting_evidence.append(
            "Technical analysis is bearish"
        )

    if technical:

        confidence_sources.append(

            _safe_confidence(

                technical.get(
                    "confidence",
                    50
                )

            )

        )

    # =====================================================
    # PREDICTION EVIDENCE
    # =====================================================

    prediction_signal = _normalize_signal(

        prediction.get(
            "signal"
        )

    )

    if prediction_signal == "BUY":

        bullish_score += 3

        supporting_evidence.append(

            "Prediction engine indicates bullish movement"

        )

    elif prediction_signal == "SELL":

        bearish_score += 3

        conflicting_evidence.append(

            "Prediction engine indicates bearish movement"

        )

    if prediction:

        confidence_sources.append(

            _safe_confidence(

                prediction.get(
                    "confidence",
                    50
                )

            )

        )

    # =====================================================
    # NEWS ANALYSIS
    # =====================================================

    news_signal = _normalize_signal(

        news_analysis.get(
            "sentiment"
        )

    )

    if news_signal == "BUY":

        bullish_score += 1

        supporting_evidence.append(

            "News sentiment is positive"

        )

    elif news_signal == "SELL":

        bearish_score += 1

        conflicting_evidence.append(

            "News sentiment is negative"

        )

    if news_analysis:

        confidence_sources.append(

            _safe_confidence(

                news_analysis.get(
                    "confidence",
                    50
                )

            )

        )

    # =====================================================
    # MARKET SENTIMENT
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

        bullish_score += 1

        supporting_evidence.append(

            "Market sentiment supports bullish conditions"

        )

    elif sentiment_signal == "SELL":

        bearish_score += 1

        conflicting_evidence.append(

            "Market sentiment supports bearish conditions"

        )

    # =====================================================
    # PATTERN EVIDENCE
    # =====================================================

    if pattern.get("bullish"):

        bullish_score += 1

        supporting_evidence.append(

            "Bullish market pattern detected"

        )

    if pattern.get("bearish"):

        bearish_score += 1

        conflicting_evidence.append(

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

        bullish_score += 1

        supporting_evidence.append(

            "Volume activity supports bullish movement"

        )

    elif volume_signal == "SELL":

        bearish_score += 1

        conflicting_evidence.append(

            "Volume activity supports bearish movement"

        )

    # =====================================================
    # AI SIGNAL
    # =====================================================

    difference = (

        bullish_score -
        bearish_score

    )

    if bullish_score >= 5:

        signal = "STRONG BUY"

    elif difference >= 2:

        signal = "BUY"

    elif bearish_score >= 5:

        signal = "STRONG SELL"

    elif difference <= -2:

        signal = "SELL"

    else:

        signal = "HOLD"

    # =====================================================
    # AI CONFIDENCE
    # =====================================================

    total_evidence = (

        bullish_score +
        bearish_score

    )

    if total_evidence == 0:

        evidence_confidence = 50

    else:

        dominant_score = max(

            bullish_score,
            bearish_score

        )

        evidence_confidence = min(

            50 +
            dominant_score * 7,

            90

        )

    # -----------------------------------------------------
    # Confidence Sources
    # -----------------------------------------------------

    if confidence_sources:

        average_source_confidence = (

            sum(confidence_sources)
            /
            len(confidence_sources)

        )

        confidence = round(

            (
                evidence_confidence
                +
                average_source_confidence
            )
            / 2,

            2

        )

    else:

        confidence = evidence_confidence

    # =====================================================
    # PROBABILITY
    # =====================================================

    probability = round(

        confidence / 100,

        2

    )

    # =====================================================
    # DEFAULT EVIDENCE
    # =====================================================

    if not supporting_evidence:

        supporting_evidence.append(

            "No strong bullish evidence available"

        )

    if not conflicting_evidence:

        conflicting_evidence.append(

            "No strong bearish evidence available"

        )

    # =====================================================
    # RETURN AI INTELLIGENCE
    # =====================================================

    return {

        "status": "success",

        "symbol": symbol,

        "signal": signal,

        "prediction": (

            "UP"

            if signal in (
                "BUY",
                "STRONG BUY"
            )

            else

            "DOWN"

            if signal in (
                "SELL",
                "STRONG SELL"
            )

            else

            "NEUTRAL"

        ),

        "confidence": confidence,

        "probability": probability,

        "bullish_score": bullish_score,

        "bearish_score": bearish_score,

        "supporting_evidence":

            supporting_evidence,

        "conflicting_evidence":

            conflicting_evidence,

        "reason":

            supporting_evidence +
            conflicting_evidence

    }
