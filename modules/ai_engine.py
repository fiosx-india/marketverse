"""
=========================================================
MarketVerse AI
AI Intelligence Engine
=========================================================

Purpose
-------
Transforms existing intelligence evidence into a unified
AI analysis result.

CentralBrain remains the primary orchestrator.

This module:
- Consumes Shared MarketContext evidence
- Combines directional evidence
- Measures evidence coverage and conflict
- Produces probability-based AI intelligence
- Produces explainable reasoning

This module does NOT:
- Fetch market data independently
- Orchestrate the workflow
- Generate strategies
- Calculate risk
- Make the final market decision
=========================================================
"""


# =========================================================
# SAFE HELPERS
# =========================================================

def _safe_dict(value):
    """Return dictionary safely."""

    return value if isinstance(value, dict) else {}


def _safe_number(value, default=0.0):
    """Convert value safely to float."""

    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_confidence(value, default=50.0):
    """Normalize confidence to 0-100."""

    confidence = _safe_number(value, default)

    return max(
        0.0,
        min(confidence, 100.0)
    )


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

    value = str(signal).strip().upper()

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
    """Register directional evidence."""

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

    return bullish_score, bearish_score


# =========================================================
# SIGNAL RESOLUTION
# =========================================================

def _resolve_signal(
    bullish_score,
    bearish_score,
    available_sources
):
    """
    Resolve signal conservatively.

    Strong signals require:
    - Minimum 4 available evidence sources
    - Strong directional score
    - Clear separation from conflicting evidence
    """

    total_directional = (
        bullish_score
        +
        bearish_score
    )

    if total_directional <= 0:
        return "HOLD"

    difference = (
        bullish_score
        -
        bearish_score
    )

    # =====================================================
    # STRONG SIGNALS
    #
    # Important:
    # Low evidence coverage cannot generate STRONG signals.
    # =====================================================

    if available_sources >= 4:

        if (
            bullish_score >= 6
            and difference >= 4
        ):
            return "STRONG BUY"

        if (
            bearish_score >= 6
            and difference <= -4
        ):
            return "STRONG SELL"

    # =====================================================
    # NORMAL BUY
    # =====================================================

    if difference >= 2:
        return "BUY"

    # =====================================================
    # NORMAL SELL
    # =====================================================

    if difference <= -2:
        return "SELL"

    # =====================================================
    # MIXED MARKET
    # =====================================================

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
    Calculate confidence conservatively.

    Components:
    - Evidence coverage
    - Directional dominance
    - Source confidence
    - Conflict penalty

    Confidence caps prevent low evidence from producing
    unrealistic high confidence.
    """

    total_directional = (
        bullish_score
        +
        bearish_score
    )

    # =====================================================
    # NO DIRECTIONAL EVIDENCE
    # =====================================================

    if total_directional <= 0:

        if available_sources == 0:
            return 0.0

        return 50.0

    dominant_score = max(
        bullish_score,
        bearish_score
    )

    conflicting_score = min(
        bullish_score,
        bearish_score
    )

    # =====================================================
    # DIRECTIONAL DOMINANCE
    # =====================================================

    dominance_ratio = (
        dominant_score
        /
        total_directional
    )

    # Maximum 30 points.
    dominance_component = (
        dominance_ratio
        *
        30
    )

    # =====================================================
    # EVIDENCE COVERAGE
    # =====================================================

    maximum_sources = 6

    coverage_ratio = min(
        available_sources
        /
        maximum_sources,
        1.0
    )

    # Maximum 30 points.
    coverage_component = (
        coverage_ratio
        *
        30
    )

    # =====================================================
    # SOURCE CONFIDENCE
    # =====================================================

    if confidence_sources:

        average_source_confidence = (
            sum(confidence_sources)
            /
            len(confidence_sources)
        )

    else:

        average_source_confidence = 50.0

    # Maximum 25 points.
    source_component = (
        average_source_confidence
        *
        0.25
    )

    # =====================================================
    # EVIDENCE STRENGTH
    # =====================================================

    evidence_strength_component = min(
        total_directional
        *
        2,
        10
    )

    # =====================================================
    # CONFLICT PENALTY
    # =====================================================

    conflict_ratio = (
        conflicting_score
        /
        total_directional
    )

    # Maximum 20 point penalty.
    conflict_penalty = (
        conflict_ratio
        *
        20
    )

    # =====================================================
    # RAW CONFIDENCE
    # =====================================================

    confidence = (

        10

        +

        dominance_component

        +

        coverage_component

        +

        source_component

        +

        evidence_strength_component

        -

        conflict_penalty

    )

    # =====================================================
    # COVERAGE CAPS
    #
    # Prevent artificial confidence when only a few
    # intelligence sources are available.
    # =====================================================

    if available_sources <= 1:

        confidence_cap = 55

    elif available_sources == 2:

        confidence_cap = 65

    elif available_sources == 3:

        confidence_cap = 75

    elif available_sources == 4:

        confidence_cap = 85

    elif available_sources == 5:

        confidence_cap = 92

    else:

        confidence_cap = 95

    confidence = min(
        confidence,
        confidence_cap
    )

    confidence = max(
        0,
        min(confidence, 95)
    )

    return round(
        confidence,
        2
    )


# =========================================================
# PROBABILITY DISTRIBUTION
# =========================================================

def _calculate_probabilities(
    bullish_score,
    bearish_score,
    available_sources
):
    """
    Calculate directional probability distribution.

    Probability is separate from confidence.

    Returns:
    - bullish_probability
    - bearish_probability
    - neutral_probability
    """

    total_directional = (
        bullish_score
        +
        bearish_score
    )

    # =====================================================
    # NO DIRECTIONAL EVIDENCE
    # =====================================================

    if total_directional <= 0:

        return {

            "bullish_probability": 0.25,

            "bearish_probability": 0.25,

            "neutral_probability": 0.50

        }

    # =====================================================
    # RAW DIRECTION RATIOS
    # =====================================================

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

    # =====================================================
    # EVIDENCE COVERAGE
    # =====================================================

    coverage_ratio = min(
        available_sources
        /
        6,
        1.0
    )

    # =====================================================
    # NEUTRAL UNCERTAINTY
    #
    # Low source coverage increases neutral uncertainty.
    # =====================================================

    neutral_probability = (

        0.40
        *
        (
            1
            -
            coverage_ratio
        )

    )

    # =====================================================
    # DIRECTIONAL PROBABILITY SPACE
    # =====================================================

    directional_space = (
        1.0
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

    # =====================================================
    # NORMALIZATION
    # =====================================================

    total = (

        bullish_probability
        +
        bearish_probability
        +
        neutral_probability

    )

    if total > 0:

        bullish_probability /= total

        bearish_probability /= total

        neutral_probability /= total

    return {

        "bullish_probability": round(
            bullish_probability,
            4
        ),

        "bearish_probability": round(
            bearish_probability,
            4
        ),

        "neutral_probability": round(
            neutral_probability,
            4
        )

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
    Classify evidence relative to final signal.
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
# MAIN AI INTELLIGENCE ENGINE
# =========================================================

def analyze(
    symbol=None,
    evidence=None
):
    """
    Generate AI intelligence analysis.

    Parameters
    ----------
    symbol:
        Market symbol.

    evidence:
        Shared MarketContext dictionary provided by
        CentralBrain.

    Supported sections:
    - technical
    - prediction
    - news_analysis
    - sentiment
    - pattern
    - volume
    """

    # =====================================================
    # INPUT NORMALIZATION
    # =====================================================

    evidence = _safe_dict(
        evidence
    )

    # =====================================================
    # READ MARKET CONTEXT
    # =====================================================

    technical = _safe_dict(
        evidence.get("technical")
    )

    prediction = _safe_dict(
        evidence.get("prediction")
    )

    news_analysis = _safe_dict(
        evidence.get("news_analysis")
    )

    sentiment = _safe_dict(
        evidence.get("sentiment")
    )

    pattern = _safe_dict(
        evidence.get("pattern")
    )

    volume = _safe_dict(
        evidence.get("volume")
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
    # TECHNICAL
    # =====================================================

    if technical:

        available_sources += 1

        direction = _normalize_signal(
            technical.get("signal")
        )

        bullish_score, bearish_score = _register_evidence(

            direction=direction,

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
    # PREDICTION
    # =====================================================

    if prediction:

        available_sources += 1

        direction = _normalize_signal(
            prediction.get("signal")
        )

        bullish_score, bearish_score = _register_evidence(

            direction=direction,

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

        direction = _normalize_signal(

            news_analysis.get(
                "signal",
                news_analysis.get("sentiment")
            )

        )

        bullish_score, bearish_score = _register_evidence(

            direction=direction,

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
    # SENTIMENT
    # =====================================================

    if sentiment:

        available_sources += 1

        direction = _normalize_signal(

            sentiment.get(
                "signal",
                sentiment.get("sentiment")
            )

        )

        bullish_score, bearish_score = _register_evidence(

            direction=direction,

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
    # PATTERN
    # =====================================================

    if pattern:

        available_sources += 1

        direction = _normalize_signal(
            pattern.get("signal")
        )

        if direction == "HOLD":

            if pattern.get("bullish"):
                direction = "BUY"

            elif pattern.get("bearish"):
                direction = "SELL"

        bullish_score, bearish_score = _register_evidence(

            direction=direction,

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
    # VOLUME
    # =====================================================

    if volume:

        available_sources += 1

        direction = _normalize_signal(
            volume.get("signal")
        )

        bullish_score, bearish_score = _register_evidence(

            direction=direction,

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
    # FINAL SIGNAL
    # =====================================================

    signal = _resolve_signal(

        bullish_score=bullish_score,

        bearish_score=bearish_score,

        available_sources=available_sources

    )

    # =====================================================
    # CONFIDENCE
    # =====================================================

    confidence = _calculate_confidence(

        bullish_score=bullish_score,

        bearish_score=bearish_score,

        confidence_sources=confidence_sources,

        available_sources=available_sources

    )

    # =====================================================
    # PROBABILITIES
    # =====================================================

    probabilities = _calculate_probabilities(

        bullish_score=bullish_score,

        bearish_score=bearish_score,

        available_sources=available_sources

    )

    # =====================================================
    # EVIDENCE CLASSIFICATION
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
    # EXPLANATION FALLBACKS
    # =====================================================

    if not supporting_evidence:

        supporting_evidence.append(

            "Insufficient dominant directional "
            "evidence for a high-conviction signal"

        )

    if not conflicting_evidence:

        conflicting_evidence.append(

            "No significant conflicting directional "
            "evidence detected"

        )

    # =====================================================
    # PREDICTION LABEL
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

            (
                min(
                    bullish_score,
                    bearish_score
                )
                /
                total_directional
            )
            *
            100,

            2

        )

    else:

        conflict_score = 0.0

    # =====================================================
    # FINAL RESULT
    # =====================================================

    return {

        "status": "success",

        "symbol": symbol,

        # Direction

        "signal": signal,

        "prediction": prediction_label,

        # Confidence

        "confidence": confidence,

        # Probability distribution

        "probability": max(

            probabilities[
                "bullish_probability"
            ],

            probabilities[
                "bearish_probability"
            ],

            probabilities[
                "neutral_probability"
            ]

        ),

        "bullish_probability":

            probabilities[
                "bullish_probability"
            ],

        "bearish_probability":

            probabilities[
                "bearish_probability"
            ],

        "neutral_probability":

            probabilities[
                "neutral_probability"
            ],

        # Evidence scores

        "bullish_score":

            bullish_score,

        "bearish_score":

            bearish_score,

        "conflict_score":

            conflict_score,

        "available_sources":

            available_sources,

        # Explainability

        "supporting_evidence":

            supporting_evidence,

        "conflicting_evidence":

            conflicting_evidence,

        "neutral_evidence":

            neutral_evidence,

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
        }

    }

    result = analyze(

        symbol="TEST",

        evidence=sample_evidence

    )

    from pprint import pprint

    pprint(result)
