"""
=========================================================
MarketVerse AI
AI Intelligence Engine
=========================================================

Purpose
-------
Transforms existing intelligence evidence into a unified
AI analysis result.

Responsibilities
----------------
- Combine available intelligence evidence
- Evaluate bullish evidence
- Evaluate bearish evidence
- Evaluate neutral evidence
- Measure evidence conflict
- Produce AI signal
- Produce confidence
- Produce directional probabilities
- Produce explainable AI reasoning

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
    ├── Pattern
    ├── Volume
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

CentralBrain remains the primary orchestrator.
=========================================================
"""


# =========================================================
# SAFE HELPERS
# =========================================================

def _safe_dict(value):
    """
    Return dictionary safely.
    """

    if isinstance(value, dict):
        return value

    return {}


def _normalize_signal(signal):
    """
    Normalize supported signal formats.

    Returns:
        BUY
        SELL
        HOLD
    """

    if signal is None:
        return "HOLD"

    signal = str(signal).strip().upper()

    if signal in (
        "STRONG BUY",
        "BUY",
        "BULLISH",
        "VERY BULLISH",
        "UP",
        "POSITIVE"
    ):
        return "BUY"

    if signal in (
        "STRONG SELL",
        "SELL",
        "BEARISH",
        "VERY BEARISH",
        "DOWN",
        "NEGATIVE"
    ):
        return "SELL"

    return "HOLD"


def _safe_confidence(
    value,
    default=50
):
    """
    Normalize confidence safely.
    """

    try:

        confidence = float(value)

        return max(
            0,
            min(
                confidence,
                100
            )
        )

    except (
        TypeError,
        ValueError
    ):

        return default


def _safe_number(
    value,
    default=0
):
    """
    Convert value safely to float.
    """

    try:

        if value is None:
            return default

        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return default


# =========================================================
# EVIDENCE REGISTRATION
# =========================================================

def _register_evidence(
    direction,
    weight,
    bullish_evidence,
    bearish_evidence,
    neutral_evidence,
    bullish_score,
    bearish_score,
    bullish_message,
    bearish_message,
    neutral_message
):
    """
    Register evidence consistently.

    Returns:
        bullish_score,
        bearish_score
    """

    if direction == "BUY":

        bullish_score += weight

        bullish_evidence.append(
            bullish_message
        )

    elif direction == "SELL":

        bearish_score += weight

        bearish_evidence.append(
            bearish_message
        )

    else:

        neutral_evidence.append(
            neutral_message
        )

    return (
        bullish_score,
        bearish_score
    )


# =========================================================
# SIGNAL RESOLUTION
# =========================================================

def _resolve_signal(
    bullish_score,
    bearish_score
):
    """
    Resolve AI signal using directional dominance.

    Strong signals require:
    - Enough directional evidence
    - Clear separation from conflicting evidence
    """

    difference = (

        bullish_score
        -
        bearish_score

    )

    total_directional = (

        bullish_score
        +
        bearish_score

    )

    # -----------------------------------------------------
    # NO DIRECTIONAL EVIDENCE
    # -----------------------------------------------------

    if total_directional <= 0:

        return "HOLD"

    # -----------------------------------------------------
    # STRONG BUY
    # -----------------------------------------------------

    if (

        bullish_score >= 5

        and difference >= 3

    ):

        return "STRONG BUY"

    # -----------------------------------------------------
    # BUY
    # -----------------------------------------------------

    if difference >= 2:

        return "BUY"

    # -----------------------------------------------------
    # STRONG SELL
    # -----------------------------------------------------

    if (

        bearish_score >= 5

        and difference <= -3

    ):

        return "STRONG SELL"

    # -----------------------------------------------------
    # SELL
    # -----------------------------------------------------

    if difference <= -2:

        return "SELL"

    # -----------------------------------------------------
    # MIXED
    # -----------------------------------------------------

    return "HOLD"


# =========================================================
# CONFIDENCE CALCULATION
# =========================================================

def _calculate_confidence(
    bullish_score,
    bearish_score,
    confidence_sources,
    available_sources
):
    """
    Calculate confidence from:

    1. Evidence coverage
    2. Directional dominance
    3. Source confidence
    4. Conflict penalty

    Confidence does not equal probability.
    """

    total_directional = (

        bullish_score
        +
        bearish_score

    )

    # -----------------------------------------------------
    # NO DIRECTIONAL EVIDENCE
    # -----------------------------------------------------

    if total_directional <= 0:

        return 50.0

    dominant_score = max(

        bullish_score,
        bearish_score

    )

    conflicting_score = min(

        bullish_score,
        bearish_score

    )

    # -----------------------------------------------------
    # DIRECTIONAL DOMINANCE
    # -----------------------------------------------------

    dominance_ratio = (

        dominant_score
        /
        total_directional

    )

    dominance_score = (

        dominance_ratio
        *
        35

    )

    # -----------------------------------------------------
    # EVIDENCE STRENGTH
    # -----------------------------------------------------

    evidence_strength = min(

        total_directional * 4,

        25

    )

    # -----------------------------------------------------
    # SOURCE COVERAGE
    # -----------------------------------------------------

    maximum_sources = 6

    coverage_ratio = min(

        available_sources
        /
        maximum_sources,

        1

    )

    coverage_score = (

        coverage_ratio
        *
        20

    )

    # -----------------------------------------------------
    # SOURCE CONFIDENCE
    # -----------------------------------------------------

    if confidence_sources:

        average_source_confidence = (

            sum(
                confidence_sources
            )

            /
            len(
                confidence_sources
            )

        )

    else:

        average_source_confidence = 50

    source_confidence_score = (

        average_source_confidence
        *
        0.20

    )

    # -----------------------------------------------------
    # CONFLICT PENALTY
    # -----------------------------------------------------

    conflict_ratio = (

        conflicting_score
        /
        total_directional

    )

    conflict_penalty = (

        conflict_ratio
        *
        20

    )

    # -----------------------------------------------------
    # FINAL
    # -----------------------------------------------------

    confidence = (

        25

        +

        dominance_score

        +

        evidence_strength

        +

        coverage_score

        +

        source_confidence_score

        -

        conflict_penalty

    )

    confidence = max(

        0,

        min(
            confidence,
            95
        )

    )

    return round(
        confidence,
        2
    )


# =========================================================
# DIRECTIONAL PROBABILITIES
# =========================================================

def _calculate_probabilities(
    bullish_score,
    bearish_score
):
    """
    Calculate directional probability distribution.

    Returns:

    bullish_probability
    bearish_probability
    neutral_probability

    Total is approximately 1.0.
    """

    total_directional = (

        bullish_score
        +
        bearish_score

    )

    # -----------------------------------------------------
    # NO DIRECTIONAL EVIDENCE
    # -----------------------------------------------------

    if total_directional <= 0:

        return {

            "bullish_probability": 0.25,

            "bearish_probability": 0.25,

            "neutral_probability": 0.50

        }

    # -----------------------------------------------------
    # DIRECTIONAL PROBABILITY
    # -----------------------------------------------------

    bullish_ratio = (

        bullish_score
        /
        total_directional

    )

    bearish_ratio = (

        bearish_score
        /
        total_directional

    )

    # -----------------------------------------------------
    # EVIDENCE STRENGTH
    # -----------------------------------------------------

    evidence_strength = min(

        total_directional
        /
        10,

        1

    )

    # -----------------------------------------------------
    # NEUTRAL PROBABILITY
    # -----------------------------------------------------

    neutral_probability = (

        0.45
        *
        (
            1
            -
            evidence_strength
        )
    )

    # -----------------------------------------------------
    # AVAILABLE DIRECTIONAL SPACE
    # -----------------------------------------------------

    directional_space = (

        1
        -
        neutral_probability

    )

    bullish_probability = (

        bullish_ratio
        *
        directional_space

    )

    bearish_probability = (

        bearish_ratio
        *
        directional_space

    )

    # -----------------------------------------------------
    # ROUND
    # -----------------------------------------------------

    bullish_probability = round(

        bullish_probability,
        4

    )

    bearish_probability = round(

        bearish_probability,
        4

    )

    neutral_probability = round(

        neutral_probability,
        4

    )

    return {

        "bullish_probability":

            bullish_probability,

        "bearish_probability":

            bearish_probability,

        "neutral_probability":

            neutral_probability

    }


# =========================================================
# FINAL EVIDENCE CLASSIFICATION
# =========================================================

def _classify_final_evidence(
    signal,
    bullish_evidence,
    bearish_evidence,
    neutral_evidence
):
    """
    Classify evidence relative to final AI signal.

    BUY:
        Bullish -> Supporting
        Bearish -> Conflicting

    SELL:
        Bearish -> Supporting
        Bullish -> Conflicting

    HOLD:
        Mixed evidence remains neutral/conflicting.
    """

    supporting_evidence = []

    conflicting_evidence = []

    # =====================================================
    # BUY
    # =====================================================

    if signal in (

        "BUY",
        "STRONG BUY"

    ):

        supporting_evidence.extend(

            bullish_evidence

        )

        conflicting_evidence.extend(

            bearish_evidence

        )

    # =====================================================
    # SELL
    # =====================================================

    elif signal in (

        "SELL",
        "STRONG SELL"

    ):

        supporting_evidence.extend(

            bearish_evidence

        )

        conflicting_evidence.extend(

            bullish_evidence

        )

    # =====================================================
    # HOLD
    # =====================================================

    else:

        conflicting_evidence.extend(

            bullish_evidence

        )

        conflicting_evidence.extend(

            bearish_evidence

        )

    return (

        supporting_evidence,

        conflicting_evidence,

        neutral_evidence

    )


# =========================================================
# AI INTELLIGENCE ENGINE
# =========================================================

def analyze(
    symbol=None,
    evidence=None
):
    """
    Generate AI intelligence evidence.

    Parameters
    ----------
    symbol:
        Market symbol.

    evidence:
        Shared MarketContext dictionary.

    Supported evidence sections:

        {
            "technical": {},
            "prediction": {},
            "news_analysis": {},
            "sentiment": {},
            "pattern": {},
            "volume": {}
        }

    CentralBrain provides the evidence.

    This function:
    - Does not fetch data
    - Does not orchestrate modules
    - Does not make final market decisions
    """

    # =====================================================
    # INPUT NORMALIZATION
    # =====================================================

    evidence = _safe_dict(
        evidence
    )

    # =====================================================
    # READ EVIDENCE
    # =====================================================

    technical = _safe_dict(

        evidence.get(
            "technical"
        )

    )

    prediction = _safe_dict(

        evidence.get(
            "prediction"
        )

    )

    news_analysis = _safe_dict(

        evidence.get(
            "news_analysis"
        )

    )

    sentiment = _safe_dict(

        evidence.get(
            "sentiment"
        )

    )

    pattern = _safe_dict(

        evidence.get(
            "pattern"
        )

    )

    volume = _safe_dict(

        evidence.get(
            "volume"
        )

    )

    # =====================================================
    # SCORE STORAGE
    # =====================================================

    bullish_score = 0

    bearish_score = 0

    bullish_evidence = []

    bearish_evidence = []

    neutral_evidence = []

    confidence_sources = []

    available_sources = 0

    # =====================================================
    # TECHNICAL EVIDENCE
    # =====================================================

    if technical:

        available_sources += 1

        technical_signal = _normalize_signal(

            technical.get(
                "signal"
            )

        )

        (
            bullish_score,
            bearish_score

        ) = _register_evidence(

            direction=technical_signal,

            weight=2,

            bullish_evidence=bullish_evidence,

            bearish_evidence=bearish_evidence,

            neutral_evidence=neutral_evidence,

            bullish_score=bullish_score,

            bearish_score=bearish_score,

            bullish_message=(
                "Technical analysis supports "
                "bullish conditions"
            ),

            bearish_message=(
                "Technical analysis supports "
                "bearish conditions"
            ),

            neutral_message=(
                "Technical analysis is neutral"
            )

        )

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

    if prediction:

        available_sources += 1

        prediction_signal = _normalize_signal(

            prediction.get(
                "signal"
            )

        )

        (
            bullish_score,
            bearish_score

        ) = _register_evidence(

            direction=prediction_signal,

            weight=3,

            bullish_evidence=bullish_evidence,

            bearish_evidence=bearish_evidence,

            neutral_evidence=neutral_evidence,

            bullish_score=bullish_score,

            bearish_score=bearish_score,

            bullish_message=(
                "Prediction engine indicates "
                "bullish movement"
            ),

            bearish_message=(
                "Prediction engine indicates "
                "bearish movement"
            ),

            neutral_message=(
                "Prediction engine indicates "
                "neutral conditions"
            )

        )

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

    if news_analysis:

        available_sources += 1

        news_signal = _normalize_signal(

            news_analysis.get(
                "signal",

                news_analysis.get(
                    "sentiment"
                )

            )

        )

        (
            bullish_score,
            bearish_score

        ) = _register_evidence(

            direction=news_signal,

            weight=1,

            bullish_evidence=bullish_evidence,

            bearish_evidence=bearish_evidence,

            neutral_evidence=neutral_evidence,

            bullish_score=bullish_score,

            bearish_score=bearish_score,

            bullish_message=(
                "News analysis supports "
                "bullish conditions"
            ),

            bearish_message=(
                "News analysis supports "
                "bearish conditions"
            ),

            neutral_message=(
                "News analysis is neutral"
            )

        )

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

    if sentiment:

        available_sources += 1

        sentiment_signal = _normalize_signal(

            sentiment.get(
                "signal",

                sentiment.get(
                    "sentiment"
                )

            )

        )

        (
            bullish_score,
            bearish_score

        ) = _register_evidence(

            direction=sentiment_signal,

            weight=1,

            bullish_evidence=bullish_evidence,

            bearish_evidence=bearish_evidence,

            neutral_evidence=neutral_evidence,

            bullish_score=bullish_score,

            bearish_score=bearish_score,

            bullish_message=(
                "Market sentiment supports "
                "bullish conditions"
            ),

            bearish_message=(
                "Market sentiment supports "
                "bearish conditions"
            ),

            neutral_message=(
                "Market sentiment is neutral"
            )

        )

        confidence_sources.append(

            _safe_confidence(

                sentiment.get(
                    "confidence",
                    50
                )

            )

        )

    # =====================================================
    # PATTERN EVIDENCE
    # =====================================================

    if pattern:

        available_sources += 1

        pattern_signal = _normalize_signal(

            pattern.get(
                "signal"
            )

        )

        if pattern_signal == "HOLD":

            if pattern.get(
                "bullish"
            ):

                pattern_signal = "BUY"

            elif pattern.get(
                "bearish"
            ):

                pattern_signal = "SELL"

        (
            bullish_score,
            bearish_score

        ) = _register_evidence(

            direction=pattern_signal,

            weight=1,

            bullish_evidence=bullish_evidence,

            bearish_evidence=bearish_evidence,

            neutral_evidence=neutral_evidence,

            bullish_score=bullish_score,

            bearish_score=bearish_score,

            bullish_message=(
                "Bullish market pattern detected"
            ),

            bearish_message=(
                "Bearish market pattern detected"
            ),

            neutral_message=(
                "No directional market pattern detected"
            )

        )

        confidence_sources.append(

            _safe_confidence(

                pattern.get(
                    "confidence",
                    50
                )

            )

        )

    # =====================================================
    # VOLUME EVIDENCE
    # =====================================================

    if volume:

        available_sources += 1

        volume_signal = _normalize_signal(

            volume.get(
                "signal"
            )

        )

        (
            bullish_score,
            bearish_score

        ) = _register_evidence(

            direction=volume_signal,

            weight=1,

            bullish_evidence=bullish_evidence,

            bearish_evidence=bearish_evidence,

            neutral_evidence=neutral_evidence,

            bullish_score=bullish_score,

            bearish_score=bearish_score,

            bullish_message=(
                "Volume activity supports "
                "bullish movement"
            ),

            bearish_message=(
                "Volume activity supports "
                "bearish movement"
            ),

            neutral_message=(
                "Volume activity is neutral"
            )

        )

        confidence_sources.append(

            _safe_confidence(

                volume.get(
                    "confidence",
                    50
                )

            )

        )

    # =====================================================
    # AI SIGNAL
    # =====================================================

    signal = _resolve_signal(

        bullish_score,

        bearish_score

    )

    # =====================================================
    # AI CONFIDENCE
    # =====================================================

    confidence = _calculate_confidence(

        bullish_score=bullish_score,

        bearish_score=bearish_score,

        confidence_sources=confidence_sources,

        available_sources=available_sources

    )

    # =====================================================
    # PROBABILITY DISTRIBUTION
    # =====================================================

    probabilities = _calculate_probabilities(

        bullish_score,

        bearish_score

    )

    bullish_probability = probabilities.get(

        "bullish_probability",

        0.25

    )

    bearish_probability = probabilities.get(

        "bearish_probability",

        0.25

    )

    neutral_probability = probabilities.get(

        "neutral_probability",

        0.50

    )

    # =====================================================
    # FINAL EVIDENCE CLASSIFICATION
    # =====================================================

    (

        supporting_evidence,

        conflicting_evidence,

        neutral_evidence

    ) = _classify_final_evidence(

        signal=signal,

        bullish_evidence=bullish_evidence,

        bearish_evidence=bearish_evidence,

        neutral_evidence=neutral_evidence

    )

    # =====================================================
    # DEFAULT EXPLANATION
    # =====================================================

    if not supporting_evidence:

        supporting_evidence.append(

            "No dominant directional evidence "
            "supports a high-conviction AI signal"

        )

    if not conflicting_evidence:

        conflicting_evidence.append(

            "No significant conflicting directional "
            "evidence detected"

        )

    # =====================================================
    # FINAL PREDICTION LABEL
    # =====================================================

    if signal in (

        "BUY",

        "STRONG BUY"

    ):

        prediction_label = "UP"

    elif signal in (

        "SELL",

        "STRONG SELL"

    ):

        prediction_label = "DOWN"

    else:

        prediction_label = "NEUTRAL"

    # =====================================================
    # CONFLICT SCORE
    # =====================================================

    total_directional = (

        bullish_score

        +

        bearish_score

    )

    if total_directional > 0:

        conflict_score = round(

            min(
                bullish_score,
                bearish_score
            )

            /

            total_directional

            *

            100,

            2

        )

    else:

        conflict_score = 0.0

    # =====================================================
    # RETURN AI INTELLIGENCE
    # =====================================================

    return {

        "status": "success",

        "symbol": symbol,

        # -----------------------------------------------
        # AI DIRECTION
        # -----------------------------------------------

        "signal": signal,

        "prediction": prediction_label,

        # -----------------------------------------------
        # CONFIDENCE
        # -----------------------------------------------

        "confidence": confidence,

        # -----------------------------------------------
        # DIRECTIONAL PROBABILITIES
        # -----------------------------------------------

        "probability": max(

            bullish_probability,

            bearish_probability,

            neutral_probability

        ),

        "bullish_probability":

            bullish_probability,

        "bearish_probability":

            bearish_probability,

        "neutral_probability":

            neutral_probability,

        # -----------------------------------------------
        # EVIDENCE SCORES
        # -----------------------------------------------

        "bullish_score":

            bullish_score,

        "bearish_score":

            bearish_score,

        "conflict_score":

            conflict_score,

        "available_sources":

            available_sources,

        # -----------------------------------------------
        # EXPLAINABILITY
        # -----------------------------------------------

        "supporting_evidence":

            supporting_evidence,

        "conflicting_evidence":

            conflicting_evidence,

        "neutral_evidence":

            neutral_evidence,

        # -----------------------------------------------
        # COMBINED REASONING
        # -----------------------------------------------

        "reason": {

            "supporting":

                supporting_evidence,

            "conflicting":

                conflicting_evidence,

            "neutral":

                neutral_evidence

        }

    }


# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    sample_evidence = {

        "technical": {

            "signal": "BUY",

            "confidence": 70

        },

        "prediction": {

            "signal": "BUY",

            "confidence": 75

        },

        "news_analysis": {

            "sentiment": "BULLISH",

            "confidence": 65

        },

        "sentiment": {

            "sentiment": "NEUTRAL",

            "confidence": 50

        },

        "pattern": {

            "bullish": True,

            "confidence": 60

        },

        "volume": {

            "signal": "BUY",

            "confidence": 70

        }

    }

    result = analyze(

        symbol="TEST",

        evidence=sample_evidence

    )

    from pprint import pprint

    pprint(result)
