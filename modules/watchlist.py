"""
=========================================================
MarketVerse AI
Sentiment Analysis Engine
=========================================================

Purpose
-------
Provides reusable market sentiment intelligence for the
MarketVerse AI intelligence pipeline.

Responsibilities
----------------
- Analyze market news sentiment
- Support raw headline lists
- Support Shared MarketContext dictionaries
- Calculate positive and negative evidence
- Produce bullish and bearish sentiment evidence
- Calculate sentiment confidence
- Return standardized sentiment intelligence

This module DOES NOT:
- Fetch market data
- Make final market decisions
- Generate trading strategies
- Calculate risk
- Execute trades
- Orchestrate the intelligence pipeline

Architecture
------------

News
    │
    ▼
News Analysis
    │
    ▼
Sentiment Engine
    │
    ▼
Sentiment Evidence
    │
    ▼
Shared MarketContext
    │
    ├── Prediction
    ├── Strategy
    └── DecisionCore

CentralBrain remains responsible for orchestration.

Author : MarketVerse AI
Version : 2.0
=========================================================
"""


# =========================================================
# SAFE RESULT
# =========================================================

def _empty_result(
    status="success",
    error=None
):
    """
    Return a stable sentiment result structure.
    """

    result = {

        "status": status,

        "score": 50,

        "label": "NEUTRAL",

        "sentiment": "NEUTRAL",

        "signal": "HOLD",

        "strength": "WEAK",

        "positive": 0,

        "negative": 0,

        "neutral": 0,

        "bullish_score": 0,

        "bearish_score": 0,

        "confidence": 0
    }

    if error:

        result["error"] = error

    return result


# =========================================================
# SAFE DICTIONARY
# =========================================================

def _safe_dict(value):
    """
    Return a dictionary safely.
    """

    if isinstance(value, dict):

        return value

    return {}


# =========================================================
# EXTRACT NEWS HEADLINES
# =========================================================

def _extract_news(source):
    """
    Extract news text from supported sources.

    Supports:

    1. List
    2. Tuple
    3. Shared MarketContext dictionary
    4. News dictionary
    5. News analysis dictionary
    """

    # =====================================================
    # LIST / TUPLE
    # =====================================================

    if isinstance(
        source,
        (list, tuple)
    ):

        return list(source)

    # =====================================================
    # CONTEXT / DICTIONARY
    # =====================================================

    if isinstance(
        source,
        dict
    ):

        headlines = []

        # -------------------------------------------------
        # RAW NEWS
        # -------------------------------------------------

        news = source.get(
            "news"
        )

        if isinstance(
            news,
            dict
        ):

            articles = news.get(
                "articles",
                []
            )

            if isinstance(
                articles,
                list
            ):

                for article in articles:

                    if isinstance(
                        article,
                        dict
                    ):

                        title = article.get(
                            "title"
                        )

                        if title:

                            headlines.append(
                                str(title)
                            )

                    elif article:

                        headlines.append(
                            str(article)
                        )

        # -------------------------------------------------
        # DIRECT ARTICLES
        # -------------------------------------------------

        articles = source.get(
            "articles"
        )

        if isinstance(
            articles,
            list
        ):

            for article in articles:

                if isinstance(
                    article,
                    dict
                ):

                    title = article.get(
                        "title"
                    )

                    if title:

                        headlines.append(
                            str(title)
                        )

                elif article:

                    headlines.append(
                        str(article)
                    )

        # -------------------------------------------------
        # DIRECT HEADLINES
        # -------------------------------------------------

        direct_headlines = source.get(
            "headlines"
        )

        if isinstance(
            direct_headlines,
            list
        ):

            for headline in direct_headlines:

                if headline:

                    headlines.append(
                        str(headline)
                    )

        return headlines

    return []


# =========================================================
# SENTIMENT KEYWORDS
# =========================================================

POSITIVE_WORDS = [

    "gain",
    "gains",

    "growth",

    "profit",
    "profits",

    "strong",

    "bullish",

    "surge",

    "rise",
    "rises",

    "positive",

    "record",

    "beat",

    "expansion",

    "upgrade",

    "recovery",

    "outperform",

    "breakout",

    "rally",

    "improve",

    "improved",

    "improvement"

]


NEGATIVE_WORDS = [

    "loss",
    "losses",

    "bearish",

    "crash",

    "fall",
    "falls",

    "drop",
    "drops",

    "decline",

    "warning",

    "downgrade",

    "weak",

    "risk",

    "lawsuit",

    "inflation",

    "recession",

    "selloff",

    "sell-off",

    "collapse",

    "concern",

    "concerns",

    "pressure"

]


# =========================================================
# CORE SENTIMENT ANALYSIS
# =========================================================

def analyze_sentiment(
    news_list
):
    """
    Analyze news text and return standardized
    sentiment intelligence.
    """

    # =====================================================
    # VALIDATE INPUT
    # =====================================================

    if not isinstance(
        news_list,
        (list, tuple)
    ):

        return _empty_result(

            status="error",

            error=(
                "Sentiment analysis expects "
                "a list of news headlines"
            )
        )

    # =====================================================
    # EMPTY NEWS
    # =====================================================

    if not news_list:

        result = _empty_result()

        result["confidence"] = 20

        return result

    # =====================================================
    # INITIAL VALUES
    # =====================================================

    score = 50

    positive_count = 0

    negative_count = 0

    neutral_count = 0

    analyzed_items = 0

    # =====================================================
    # ANALYZE NEWS
    # =====================================================

    for news in news_list:

        if news is None:

            continue

        text = str(
            news
        ).lower()

        if not text.strip():

            continue

        analyzed_items += 1

        positive_matches = 0

        negative_matches = 0

        # -------------------------------------------------
        # POSITIVE WORDS
        # -------------------------------------------------

        for word in POSITIVE_WORDS:

            if word in text:

                positive_matches += 1

                positive_count += 1

                score += 5

        # -------------------------------------------------
        # NEGATIVE WORDS
        # -------------------------------------------------

        for word in NEGATIVE_WORDS:

            if word in text:

                negative_matches += 1

                negative_count += 1

                score -= 5

        # -------------------------------------------------
        # NEUTRAL ITEM
        # -------------------------------------------------

        if (

            positive_matches == 0

            and negative_matches == 0

        ):

            neutral_count += 1

    # =====================================================
    # NO VALID NEWS
    # =====================================================

    if analyzed_items == 0:

        result = _empty_result()

        result["confidence"] = 20

        return result

    # =====================================================
    # LIMIT SCORE
    # =====================================================

    score = max(

        0,

        min(
            100,
            score
        )

    )

    # =====================================================
    # LABEL
    # =====================================================

    if score >= 70:

        label = "POSITIVE"

        sentiment = "BULLISH"

        signal = "BUY"

        strength = "STRONG"

    elif score <= 30:

        label = "NEGATIVE"

        sentiment = "BEARISH"

        signal = "SELL"

        strength = "STRONG"

    else:

        label = "NEUTRAL"

        sentiment = "NEUTRAL"

        signal = "HOLD"

        strength = "MEDIUM"

    # =====================================================
    # BULLISH / BEARISH SCORES
    # =====================================================

    bullish_score = 0

    bearish_score = 0

    if positive_count > negative_count:

        difference = (

            positive_count
            -
            negative_count

        )

        bullish_score = min(

            3,

            max(
                1,
                difference
            )

        )

    elif negative_count > positive_count:

        difference = (

            negative_count
            -
            positive_count

        )

        bearish_score = min(

            3,

            max(
                1,
                difference
            )

        )

    # =====================================================
    # CONFIDENCE
    # =====================================================

    evidence_count = (

        positive_count
        +
        negative_count

    )

    if evidence_count == 0:

        confidence = 30

    else:

        dominant = max(

            positive_count,

            negative_count

        )

        conflicting = min(

            positive_count,

            negative_count

        )

        confidence = (

            35

            +

            dominant * 10

            -

            conflicting * 5

        )

        confidence = max(

            20,

            min(
                90,
                confidence
            )

        )

    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {

        "status": "success",

        "score": round(
            score,
            2
        ),

        "label": label,

        "sentiment": sentiment,

        "signal": signal,

        "strength": strength,

        "positive": positive_count,

        "negative": negative_count,

        "neutral": neutral_count,

        "bullish_score": bullish_score,

        "bearish_score": bearish_score,

        "confidence": round(
            confidence,
            2
        )

    }


# =========================================================
# CENTRAL BRAIN COMPATIBILITY
# =========================================================

def sentiment_analysis(
    source=None
):
    """
    CentralBrain Sentiment Analysis Interface.

    Supports:

    - List of news headlines
    - Shared MarketContext dictionary
    - News dictionary
    """

    # =====================================================
    # EXTRACT NEWS
    # =====================================================

    news_list = _extract_news(
        source
    )

    # =====================================================
    # ANALYZE SENTIMENT
    # =====================================================

    return analyze_sentiment(
        news_list
    )
