"""
=========================================================
MarketVerse AI
News Intelligence Provider
=========================================================

Purpose
-------
Fetches and prepares market news evidence for the
MarketVerse AI intelligence pipeline.

Responsibilities
----------------
- Fetch market news
- Normalize articles
- Remove duplicates
- Calculate relevance
- Calculate basic news metadata
- Produce analytics

This module DOES NOT
--------------------
- Make final market decisions
- Generate trading strategies
- Calculate portfolio risk
- Orchestrate the pipeline

CentralBrain remains the orchestration layer.
=========================================================
"""

from datetime import datetime
from functools import lru_cache
import os


# =========================================================
# OPTIONAL NEWSAPI IMPORT
# =========================================================

try:

    from newsapi import NewsApiClient

except ImportError:

    NewsApiClient = None


# =========================================================
# CONFIGURATION
# =========================================================

NEWS_API_KEY = os.getenv(
    "NEWS_API_KEY",
    ""
)


# =========================================================
# SAFE HELPERS
# =========================================================

def clean_symbol(symbol):
    """
    Convert market symbols into search keywords.

    Examples:
        RELIANCE.NS -> RELIANCE
        TCS.BO      -> TCS
    """

    if not symbol:

        return None

    symbol = str(
        symbol
    ).upper().strip()

    if "." in symbol:

        symbol = symbol.split(
            "."
        )[0]

    return symbol


def _safe_text(value):
    """
    Convert values into safe text.
    """

    if value is None:

        return ""

    return str(
        value
    ).strip()


def _empty_analytics(
    error=None
):
    """
    Return stable analytics structure.
    """

    analytics = {

        "total_news": 0,

        "positive_news": 0,

        "negative_news": 0,

        "neutral_news": 0,

        "bullish_percent": 0,

        "bearish_percent": 0,

        "neutral_percent": 0,

        "market_mood": "Unknown",

        "confidence": 0,

        "signal": "HOLD",

        "economic_events": 0,

        "earnings_news": 0,

        "ipo_news": 0,

        "crypto_news": 0,

        "institutional_news": 0,

        "generated_at": (
            datetime.now().isoformat()
        )
    }

    if error:

        analytics["error"] = str(
            error
        )

    return analytics


def _result(
    articles,
    analytics,
    status="success",
    error=None
):
    """
    Return standardized news result.
    """

    result = {

        "status": status,

        "articles": articles,

        "analytics": analytics,

        "updated": (
            datetime.now().isoformat()
        )
    }

    if error:

        result["error"] = str(
            error
        )

    return result


# =========================================================
# SENTIMENT
# =========================================================

POSITIVE_WORDS = [

    "gain",
    "gains",

    "growth",

    "profit",
    "profits",

    "surge",

    "bullish",

    "beat",

    "strong",

    "upgrade",

    "rally",

    "recovery",

    "breakout",

    "outperform"

]


NEGATIVE_WORDS = [

    "loss",
    "losses",

    "fall",
    "falls",

    "drop",
    "drops",

    "bearish",

    "downgrade",

    "weak",

    "crash",

    "decline",

    "selloff",

    "sell-off",

    "lawsuit",

    "warning"

]


def _calculate_basic_sentiment(
    text
):
    """
    Basic news sentiment classification.

    NewsAnalysis and SentimentEngine remain the
    detailed intelligence modules.
    """

    text = _safe_text(
        text
    ).lower()

    positive = sum(

        word in text

        for word in POSITIVE_WORDS

    )

    negative = sum(

        word in text

        for word in NEGATIVE_WORDS

    )

    if positive > negative:

        return (
            "Positive",
            positive,
            negative
        )

    if negative > positive:

        return (
            "Negative",
            positive,
            negative
        )

    return (
        "Neutral",
        positive,
        negative
    )


# =========================================================
# ARTICLE NORMALIZATION
# =========================================================

def _normalize_article(
    article
):
    """
    Normalize raw provider article.
    """

    if not isinstance(
        article,
        dict
    ):

        return None

    title = _safe_text(
        article.get(
            "title"
        )
    )

    description = _safe_text(
        article.get(
            "description"
        )
    )

    source = article.get(
        "source",
        {}
    )

    if isinstance(
        source,
        dict
    ):

        source_name = _safe_text(
            source.get(
                "name"
            )
        )

    else:

        source_name = _safe_text(
            source
        )

    url = _safe_text(
        article.get(
            "url"
        )
    )

    published = _safe_text(
        article.get(
            "publishedAt",
            article.get(
                "published"
            )
        )
    )

    # Ignore completely empty articles.

    if not title and not description:

        return None

    text = (

        title
        +
        " "
        +
        description

    )

    sentiment, positive_count, negative_count = (
        _calculate_basic_sentiment(
            text
        )
    )

    return {

        "title": title,

        "description": description,

        "source": source_name,

        "url": url,

        "published": published,

        "sentiment": sentiment,

        "positive_matches": positive_count,

        "negative_matches": negative_count
    }


# =========================================================
# ARTICLE ENRICHMENT
# =========================================================

def _enrich_articles(
    articles,
    symbol=None
):
    """
    Add relevance and intelligence metadata.
    """

    keyword = clean_symbol(
        symbol
    )

    if keyword:

        keyword = keyword.lower()

    trending_keywords = [

        "ai",

        "earnings",

        "results",

        "profit",

        "revenue",

        "merger",

        "acquisition",

        "ipo",

        "fed",

        "inflation",

        "interest rate",

        "bitcoin",

        "gold"

    ]

    enriched = []

    for article in articles:

        article = dict(
            article
        )

        title = _safe_text(
            article.get(
                "title"
            )
        )

        description = _safe_text(
            article.get(
                "description"
            )
        )

        text = (

            title
            +
            " "
            +
            description

        ).lower()

        # =================================================
        # RELEVANCE
        # =================================================

        if keyword:

            relevance_score = 0

            if keyword in title.lower():

                relevance_score += 70

            if keyword in description.lower():

                relevance_score += 30

        else:

            relevance_score = 50

        relevance_score = min(
            relevance_score,
            100
        )

        article[
            "relevance_score"
        ] = relevance_score

        # =================================================
        # CATEGORY
        # =================================================

        category = "General"

        if (

            "earnings" in text

            or "results" in text

            or "quarterly" in text

        ):

            category = "Earnings"

        elif "dividend" in text:

            category = "Dividend"

        elif (

            "acquisition" in text

            or "merger" in text

        ):

            category = "Merger"

        elif "ipo" in text:

            category = "IPO"

        elif "lawsuit" in text:

            category = "Legal"

        elif (

            "upgrade" in text

            or "downgrade" in text

        ):

            category = "Broker Action"

        article[
            "category"
        ] = category

        # =================================================
        # TRENDING SCORE
        # =================================================

        trending_score = sum(

            10

            for keyword_item
            in trending_keywords

            if keyword_item in text

        )

        trending_score = min(
            trending_score,
            100
        )

        article[
            "trending_score"
        ] = trending_score

        # =================================================
        # BREAKING NEWS
        # =================================================

        article[
            "breaking"
        ] = any(

            word in text

            for word in (

                "breaking",

                "urgent",

                "flash"

            )

        )

        # =================================================
        # QUALITY SCORE
        # =================================================

        quality_score = 50

        if description:

            quality_score += 20

        if article.get(
            "source"
        ):

            quality_score += 15

        if article.get(
            "url"
        ):

            quality_score += 15

        quality_score = min(
            quality_score,
            100
        )

        article[
            "quality_score"
        ] = quality_score

        # =================================================
        # AI CONFIDENCE
        # =================================================

        confidence = 50

        sentiment = article.get(
            "sentiment"
        )

        if sentiment == "Positive":

            confidence += 20

        elif sentiment == "Negative":

            confidence += 15

        confidence += int(
            relevance_score / 5
        )

        confidence = min(
            confidence,
            100
        )

        article[
            "ai_confidence"
        ] = confidence

        # =================================================
        # MARKET IMPACT
        # =================================================

        impact = (

            confidence * 0.4

            +

            quality_score * 0.2

            +

            trending_score * 0.2

            +

            relevance_score * 0.2

        )

        article[
            "market_impact"
        ] = round(
            impact,
            2
        )

        article[
            "impact_score"
        ] = round(
            impact,
            2
        )

        # =================================================
        # RISK LEVEL
        # =================================================

        if sentiment == "Positive":

            risk_level = "Low"

        elif sentiment == "Negative":

            risk_level = "High"

        else:

            risk_level = "Medium"

        article[
            "risk_level"
        ] = risk_level

        # =================================================
        # SUMMARY
        # =================================================

        summary = description or title

        article[
            "summary"
        ] = summary[:200]

        # =================================================
        # RECOMMENDATION
        # =================================================

        if (

            sentiment == "Positive"

            and relevance_score >= 50

        ):

            recommendation = "BULLISH"

        elif (

            sentiment == "Negative"

            and relevance_score >= 50

        ):

            recommendation = "BEARISH"

        else:

            recommendation = "NEUTRAL"

        article[
            "recommendation"
        ] = recommendation

        enriched.append(
            article
        )

    # =====================================================
    # SORT
    # =====================================================

    enriched.sort(

        key=lambda item: (

            item.get(
                "market_impact",
                0
            ),

            item.get(
                "published",
                ""
            )

        ),

        reverse=True

    )

    return enriched


# =========================================================
# ANALYTICS
# =========================================================

def _build_analytics(
    articles
):
    """
    Build aggregate news analytics.
    """

    analytics = _empty_analytics()

    total = len(
        articles
    )

    analytics[
        "total_news"
    ] = total

    if total == 0:

        return analytics

    positive = sum(

        article.get(
            "sentiment"
        ) == "Positive"

        for article in articles

    )

    negative = sum(

        article.get(
            "sentiment"
        ) == "Negative"

        for article in articles

    )

    neutral = (

        total
        -
        positive
        -
        negative

    )

    analytics[
        "positive_news"
    ] = positive

    analytics[
        "negative_news"
    ] = negative

    analytics[
        "neutral_news"
    ] = neutral

    analytics[
        "bullish_percent"
    ] = round(

        (
            positive
            /
            total
        )
        *
        100,

        2

    )

    analytics[
        "bearish_percent"
    ] = round(

        (
            negative
            /
            total
        )
        *
        100,

        2

    )

    analytics[
        "neutral_percent"
    ] = round(

        (
            neutral
            /
            total
        )
        *
        100,

        2

    )

    # =====================================================
    # MARKET MOOD
    # =====================================================

    if positive > negative:

        mood = "Bullish"

        signal = "BUY"

    elif negative > positive:

        mood = "Bearish"

        signal = "SELL"

    else:

        mood = "Neutral"

        signal = "HOLD"

    analytics[
        "market_mood"
    ] = mood

    analytics[
        "signal"
    ] = signal

    # =====================================================
    # CONFIDENCE
    # =====================================================

    directional = abs(
        positive
        -
        negative
    )

    confidence = (

        30

        +

        directional * 8

        +

        min(
            total,
            10
        ) * 3

    )

    if positive > 0 and negative > 0:

        confidence -= 10

    analytics[
        "confidence"
    ] = max(

        0,

        min(
            confidence,
            95
        )

    )

    # =====================================================
    # EVENT COUNTERS
    # =====================================================

    economic_keywords = [

        "inflation",

        "interest rate",

        "fed",

        "gdp",

        "recession",

        "central bank"

    ]

    earnings_keywords = [

        "earnings",

        "quarterly",

        "results",

        "revenue",

        "profit",

        "eps"

    ]

    ipo_keywords = [

        "ipo",

        "listing",

        "subscription",

        "allotment"

    ]

    crypto_keywords = [

        "bitcoin",

        "ethereum",

        "crypto",

        "blockchain"

    ]

    fii_keywords = [

        "fii",

        "dii",

        "foreign investor",

        "institutional investor"

    ]

    for article in articles:

        text = (

            _safe_text(
                article.get(
                    "title"
                )
            )

            +

            " "

            +

            _safe_text(
                article.get(
                    "description"
                )
            )

        ).lower()

        if any(

            keyword in text

            for keyword
            in economic_keywords

        ):

            analytics[
                "economic_events"
            ] += 1

        if any(

            keyword in text

            for keyword
            in earnings_keywords

        ):

            analytics[
                "earnings_news"
            ] += 1

        if any(

            keyword in text

            for keyword
            in ipo_keywords

        ):

            analytics[
                "ipo_news"
            ] += 1

        if any(

            keyword in text

            for keyword
            in crypto_keywords

        ):

            analytics[
                "crypto_news"
            ] += 1

        if any(

            keyword in text

            for keyword
            in fii_keywords

        ):

            analytics[
                "institutional_news"
            ] += 1

    return analytics


# =========================================================
# NEWS CLIENT
# =========================================================

def _create_news_client():
    """
    Create NewsAPI client safely.
    """

    if NewsApiClient is None:

        return None

    if not NEWS_API_KEY:

        return None

    return NewsApiClient(

        api_key=NEWS_API_KEY

    )


# =========================================================
# MAIN NEWS FUNCTION
# =========================================================

@lru_cache(
    maxsize=100
)
def get_market_news(
    symbol=None,
    limit=10
):
    """
    Fetch and prepare latest market news.

    Returns a stable structure:

    {
        "status": "...",
        "articles": [...],
        "analytics": {...}
    }
    """

    # =====================================================
    # VALIDATE LIMIT
    # =====================================================

    try:

        limit = int(
            limit
        )

    except (
        TypeError,
        ValueError
    ):

        limit = 10

    limit = max(

        1,

        min(
            limit,
            100
        )

    )

    # =====================================================
    # CREATE CLIENT
    # =====================================================

    client = _create_news_client()

    if client is None:

        analytics = _empty_analytics(

            error=(
                "NewsAPI unavailable or "
                "NEWS_API_KEY is not configured"
            )

        )

        return _result(

            articles=[],

            analytics=analytics,

            status="unavailable"

        )

    try:

        # =================================================
        # FETCH NEWS
        # =================================================

        if symbol:

            query = clean_symbol(
                symbol
            )

            response = client.get_everything(

                q=query,

                language="en",

                sort_by="publishedAt",

                page_size=limit

            )

        else:

            response = client.get_top_headlines(

                category="business",

                language="en",

                page_size=limit

            )

        # =================================================
        # NORMALIZE
        # =================================================

        articles = []

        seen_urls = set()

        for raw_article in response.get(
            "articles",
            []
        ):

            article = _normalize_article(
                raw_article
            )

            if article is None:

                continue

            url = article.get(
                "url"
            )

            unique_key = (

                url

                or

                article.get(
                    "title"
                )

            )

            if unique_key in seen_urls:

                continue

            seen_urls.add(
                unique_key
            )

            articles.append(
                article
            )

        # =================================================
        # ENRICH
        # =================================================

        articles = _enrich_articles(

            articles,

            symbol=symbol

        )

        # =================================================
        # ANALYTICS
        # =================================================

        analytics = _build_analytics(

            articles

        )

        # =================================================
        # RETURN
        # =================================================

        return _result(

            articles=articles,

            analytics=analytics,

            status="success"

        )

    except Exception as error:

        analytics = _empty_analytics(

            error=error

        )

        return _result(

            articles=[],

            analytics=analytics,

            status="error",

            error=error

        )


# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    result = get_market_news(

        "RELIANCE.NS"

    )

    print(

        "Status:",

        result.get(
            "status"
        )

    )

    print(

        "Articles:",

        len(
            result.get(
                "articles",
                []
            )
        )

    )

    print(

        "Analytics:",

        result.get(
            "analytics"
        )

        )
