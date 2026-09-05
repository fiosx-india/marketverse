"""
=========================================================
MarketVerse AI
News Analysis Engine
=========================================================

Purpose
-------
Analyzes market news headlines and converts raw news
into standardized intelligence evidence.

Responsibilities
----------------
- Analyze individual headlines
- Calculate positive and negative evidence
- Calculate overall news sentiment
- Generate bullish and bearish evidence
- Calculate confidence
- Support CentralBrain compatibility
- Return explainable news analysis

This module DOES NOT:
- Fetch news
- Fetch market data
- Make final market decisions
- Generate strategies
- Calculate risk
- Execute trades
- Orchestrate the intelligence pipeline

Architecture
------------

News Provider
      │
      ▼
Raw News Headlines
      │
      ▼
News Analysis Engine
      │
      ▼
News Evidence
      │
      ▼
Shared MarketContext
      │
      ├── Sentiment
      ├── Prediction
      ├── Strategy
      └── DecisionCore

CentralBrain remains responsible for orchestration.

Author : MarketVerse AI
Version : 2.0
=========================================================
"""

from datetime import datetime


# =========================================================
# SENTIMENT KEYWORDS
# =========================================================

POSITIVE_WORDS = {

    "gain",
    "gains",

    "growth",

    "profit",
    "profits",

    "bullish",

    "buy",

    "upgrade",

    "strong",

    "positive",

    "surge",

    "beat",

    "record",

    "expansion",

    "optimistic",

    "rise",
    "rises",

    "rally",

    "recovery",

    "improve",
    "improved",

    "outperform",

    "breakout"
}


NEGATIVE_WORDS = {

    "loss",
    "losses",

    "bearish",

    "sell",

    "downgrade",

    "weak",

    "drop",
    "drops",

    "fall",
    "falls",

    "crash",

    "decline",

    "fraud",

    "lawsuit",

    "bankruptcy",

    "negative",

    "miss",

    "warning",

    "risk",

    "pressure",

    "concern",
    "concerns",

    "collapse"
}


# =========================================================
# SAFE HELPERS
# =========================================================

def _safe_text(value):
    """
    Convert a value into clean text.
    """

    if value is None:
        return ""

    return str(value).strip()


def _normalize_headlines(headlines):
    """
    Normalize headline input safely.

    Supports:
    - list
    - tuple
    - None
    """

    if headlines is None:
        return []

    if not isinstance(
        headlines,
        (list, tuple)
    ):
        return []

    cleaned = []

    for headline in headlines:

        text = _safe_text(
            headline
        )

        if text:

            cleaned.append(
                text
            )

    return cleaned


# =========================================================
# INDIVIDUAL SENTIMENT ANALYSIS
# =========================================================

def calculate_sentiment(text):
    """
    Analyze a single headline.

    Returns:
    - score
    - sentiment
    - signal
    - confidence
    - positive_matches
    - negative_matches
    """

    text = _safe_text(
        text
    ).lower()

    # =====================================================
    # EMPTY TEXT
    # =====================================================

    if not text:

        return {

            "score": 0,

            "sentiment": "NEUTRAL",

            "signal": "HOLD",

            "confidence": 0,

            "positive_matches": 0,

            "negative_matches": 0
        }

    # =====================================================
    # COUNT POSITIVE
    # =====================================================

    positive = 0

    for word in POSITIVE_WORDS:

        if word in text:

            positive += 1

    # =====================================================
    # COUNT NEGATIVE
    # =====================================================

    negative = 0

    for word in NEGATIVE_WORDS:

        if word in text:

            negative += 1

    # =====================================================
    # SCORE
    # =====================================================

    score = positive - negative

    # =====================================================
    # SENTIMENT
    # =====================================================

    if score >= 2:

        sentiment = "VERY BULLISH"

        signal = "STRONG BUY"

    elif score == 1:

        sentiment = "BULLISH"

        signal = "BUY"

    elif score == 0:

        sentiment = "NEUTRAL"

        signal = "HOLD"

    elif score == -1:

        sentiment = "BEARISH"

        signal = "SELL"

    else:

        sentiment = "VERY BEARISH"

        signal = "STRONG SELL"

    # =====================================================
    # CONFIDENCE
    # =====================================================

    evidence_count = (
        positive
        +
        negative
    )

    if evidence_count == 0:

        confidence = 30

    else:

        confidence = min(

            100,

            max(
                40,
                abs(score) * 25 + 50
            )

        )

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "score": score,

        "sentiment": sentiment,

        "signal": signal,

        "confidence": round(
            confidence,
            2
        ),

        "positive_matches": positive,

        "negative_matches": negative
    }


# =========================================================
# MAIN NEWS ANALYSIS
# =========================================================

def analyze_news(
    symbol,
    headlines=None
):
    """
    Analyze market news headlines.

    Parameters
    ----------
    symbol : str
        Market symbol.

    headlines : list[str]
        News headlines.

    Returns
    -------
    dict
        Standardized news intelligence.
    """

    # =====================================================
    # SYMBOL
    # =====================================================

    if symbol is None:

        symbol = ""

    symbol = str(
        symbol
    ).upper()

    # =====================================================
    # NORMALIZE HEADLINES
    # =====================================================

    headlines = _normalize_headlines(
        headlines
    )

    # =====================================================
    # NO NEWS
    # =====================================================

    if not headlines:

        return {

            "status": "success",

            "symbol": symbol,

            "headline_count": 0,

            "overall_sentiment": "NO NEWS",

            "sentiment": "NEUTRAL",

            "signal": "HOLD",

            "confidence": 0,

            "score": 0,

            "bullish_score": 0,

            "bearish_score": 0,

            "positive_count": 0,

            "negative_count": 0,

            "neutral_count": 0,

            "headlines": [],

            "supporting_evidence": [],

            "conflicting_evidence": [],

            "updated": (
                datetime.now().isoformat()
            )
        }

    # =====================================================
    # STORAGE
    # =====================================================

    scores = []

    analysed = []

    positive_count = 0

    negative_count = 0

    neutral_count = 0

    supporting_evidence = []

    conflicting_evidence = []

    # =====================================================
    # ANALYZE HEADLINES
    # =====================================================

    for headline in headlines:

        result = calculate_sentiment(
            headline
        )

        score = result.get(
            "score",
            0
        )

        scores.append(
            score
        )

        sentiment = result.get(
            "sentiment",
            "NEUTRAL"
        )

        # -------------------------------------------------
        # CLASSIFICATION COUNTS
        # -------------------------------------------------

        if score > 0:

            positive_count += 1

        elif score < 0:

            negative_count += 1

        else:

            neutral_count += 1

        # -------------------------------------------------
        # EVIDENCE
        # -------------------------------------------------

        if score > 0:

            supporting_evidence.append(
                headline
            )

        elif score < 0:

            conflicting_evidence.append(
                headline
            )

        # -------------------------------------------------
        # STORE ANALYSIS
        # -------------------------------------------------

        analysed.append({

            "headline": headline,

            "sentiment": sentiment,

            "signal": result.get(
                "signal",
                "HOLD"
            ),

            "score": score,

            "confidence": result.get(
                "confidence",
                0
            ),

            "positive_matches": result.get(
                "positive_matches",
                0
            ),

            "negative_matches": result.get(
                "negative_matches",
                0
            )
        })

    # =====================================================
    # AVERAGE SCORE
    # =====================================================

    average = (

        sum(scores)
        /
        len(scores)

    )

    # =====================================================
    # OVERALL SENTIMENT
    # =====================================================

    if average >= 2:

        overall = "VERY BULLISH"

        sentiment = "BULLISH"

        signal = "STRONG BUY"

    elif average >= 0.5:

        overall = "BULLISH"

        sentiment = "BULLISH"

        signal = "BUY"

    elif average > -0.5:

        overall = "NEUTRAL"

        sentiment = "NEUTRAL"

        signal = "HOLD"

    elif average > -2:

        overall = "BEARISH"

        sentiment = "BEARISH"

        signal = "SELL"

    else:

        overall = "VERY BEARISH"

        sentiment = "BEARISH"

        signal = "STRONG SELL"

    # =====================================================
    # BULLISH / BEARISH SCORES
    # =====================================================

    total_directional = (

        positive_count
        +
        negative_count

    )

    if total_directional > 0:

        bullish_ratio = (

            positive_count
            /
            total_directional

        )

        bearish_ratio = (

            negative_count
            /
            total_directional

        )

        bullish_score = round(
            bullish_ratio * 3,
            2
        )

        bearish_score = round(
            bearish_ratio * 3,
            2
        )

    else:

        bullish_score = 0

        bearish_score = 0

    # =====================================================
    # CONFIDENCE
    # =====================================================

    directional_strength = abs(
        positive_count
        -
        negative_count
    )

    evidence_count = len(
        headlines
    )

    if evidence_count <= 0:

        confidence = 0

    else:

        confidence = (

            35

            +

            directional_strength * 10

            +

            min(
                evidence_count,
                10
            ) * 2

        )

        # Conflicting evidence reduces confidence.

        if (

            positive_count > 0

            and negative_count > 0

        ):

            confidence -= 10

        confidence = max(

            20,

            min(
                95,
                confidence
            )

        )

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "status": "success",

        "symbol": symbol,

        "headline_count": len(
            headlines
        ),

        "overall_sentiment": overall,

        "sentiment": sentiment,

        "signal": signal,

        "confidence": round(
            confidence,
            2
        ),

        "score": round(
            average,
            2
        ),

        "bullish_score": bullish_score,

        "bearish_score": bearish_score,

        "positive_count": positive_count,

        "negative_count": negative_count,

        "neutral_count": neutral_count,

        "headlines": analysed,

        "supporting_evidence": supporting_evidence,

        "conflicting_evidence": conflicting_evidence,

        "updated": (
            datetime.now().isoformat()
        )
    }


# =========================================================
# DEMO / DEVELOPMENT NEWS
# =========================================================

def get_dummy_news(symbol):
    """
    Demo headlines for development and testing.

    This function should not be treated as a live
    market news provider.
    """

    symbol = str(
        symbol
    ).upper()

    return [

        (
            f"{symbol} reports strong "
            "quarterly profit growth"
        ),

        (
            f"{symbol} receives "
            "broker upgrade"
        ),

        (
            f"Investors remain optimistic "
            f"about {symbol}"
        )
    ]


# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    symbol = "RELIANCE"

    news = get_dummy_news(
        symbol
    )

    result = analyze_news(
        symbol,
        news
    )

    from pprint import pprint

    pprint(
        result
    )
