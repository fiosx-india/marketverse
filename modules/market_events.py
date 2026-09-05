"""
=========================================================
MarketVerse AI
Market Events Engine
=========================================================

Purpose
-------
Detects potentially market-moving events from existing
news evidence.

This module converts raw news articles into structured
event intelligence.

Responsibilities
----------------
- Read news articles
- Detect high-impact events
- Detect medium-impact events
- Detect low-impact events
- Assess market alert level
- Assess event risk level
- Generate event signal
- Calculate confidence
- Return explainable event evidence

This module DOES NOT:
- Fetch news
- Fetch market prices
- Generate predictions
- Generate strategies
- Make final decisions
- Calculate trade risk
- Orchestrate the pipeline

Architecture
------------

News Provider
      │
      ▼
News Evidence
      │
      ▼
Market Events Engine
      │
      ▼
Event Intelligence
      │
      ▼
Shared MarketContext
      │
      ├── Prediction
      ├── Strategy
      ├── RiskManager
      └── DecisionCore

CentralBrain remains the single orchestration layer.

Author : MarketVerse AI
Version : 2.0
=========================================================
"""

from datetime import datetime


# =========================================================
# EVENT KEYWORDS
# =========================================================

HIGH_IMPACT_KEYWORDS = [

    "interest rate",
    "fed",
    "federal reserve",
    "rbi",
    "inflation",
    "budget",
    "war",
    "recession",
    "bankruptcy",
    "default",
    "covid",
    "crash",
    "sanction",

    "rate hike",
    "rate cut",

    "emergency",

    "financial crisis",

    "market collapse",

    "global conflict"
]


MEDIUM_IMPACT_KEYWORDS = [

    "earnings",
    "results",
    "profit",
    "revenue",

    "ipo",
    "listing",

    "merger",
    "acquisition",

    "dividend",
    "buyback",

    "guidance",

    "quarterly",

    "investment",

    "expansion",

    "restructuring"
]


# =========================================================
# SAFE HELPERS
# =========================================================

def _safe_text(value):
    """Convert a value to safe text."""

    if value is None:

        return ""

    return str(value).strip()


def _safe_dict(value):
    """Return dictionary safely."""

    if isinstance(value, dict):

        return value

    return {}


# =========================================================
# EMPTY RESULT
# =========================================================

def _empty_result(
    status="success",
    error=None
):
    """
    Return stable Market Events result structure.
    """

    result = {

        "status": status,

        "high_impact": [],

        "medium_impact": [],

        "low_impact": [],

        "high_impact_count": 0,

        "medium_impact_count": 0,

        "low_impact_count": 0,

        "total_events": 0,

        "market_alert": "NORMAL",

        "risk_level": "LOW",

        "signal": "HOLD",

        "confidence": 0,

        "bullish_events": 0,

        "bearish_events": 0,

        "neutral_events": 0,

        "supporting_evidence": [],

        "conflicting_evidence": [],

        "generated_at": (
            datetime.now().isoformat()
        )
    }

    if error:

        result["error"] = str(
            error
        )

    return result


# =========================================================
# EXTRACT ARTICLES
# =========================================================

def _extract_articles(source):
    """
    Extract articles from supported input formats.

    Supports:

    1. List of articles
    2. News result dictionary
    3. Shared MarketContext dictionary
    4. Symbol string

    Symbol strings intentionally return an empty list.

    MarketEvents must NOT fetch news independently.
    CentralBrain should provide News evidence through
    MarketContext.
    """

    # =====================================================
    # LIST
    # =====================================================

    if isinstance(source, list):

        return source

    # =====================================================
    # TUPLE
    # =====================================================

    if isinstance(source, tuple):

        return list(source)

    # =====================================================
    # DICTIONARY
    # =====================================================

    if isinstance(source, dict):

        # -----------------------------------------------
        # DIRECT ARTICLES
        # -----------------------------------------------

        articles = source.get(
            "articles"
        )

        if isinstance(articles, list):

            return articles

        # -----------------------------------------------
        # NEWS SECTION
        # -----------------------------------------------

        news = source.get(
            "news"
        )

        if isinstance(news, dict):

            articles = news.get(
                "articles"
            )

            if isinstance(
                articles,
                list
            ):

                return articles

        return []

    # =====================================================
    # UNSUPPORTED / SYMBOL STRING
    # =====================================================

    return []


# =========================================================
# ARTICLE TEXT
# =========================================================

def _article_text(article):
    """
    Extract searchable text from an article.
    """

    if isinstance(article, dict):

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

        summary = _safe_text(

            article.get(
                "summary"
            )

        )

        return (

            title
            +
            " "
            +
            description
            +
            " "
            +
            summary

        ).lower()

    return _safe_text(
        article
    ).lower()


# =========================================================
# EVENT DIRECTION
# =========================================================

def _event_direction(
    article
):
    """
    Resolve event direction from existing article evidence.

    This avoids creating a separate prediction engine.

    Returns:
        BULLISH
        BEARISH
        NEUTRAL
    """

    if not isinstance(
        article,
        dict
    ):

        return "NEUTRAL"

    recommendation = _safe_text(

        article.get(
            "recommendation"
        )

    ).upper()

    sentiment = _safe_text(

        article.get(
            "sentiment"
        )

    ).upper()

    if recommendation in (

        "BULLISH",

        "BUY",

        "STRONG BUY"

    ):

        return "BULLISH"

    if recommendation in (

        "BEARISH",

        "SELL",

        "STRONG SELL"

    ):

        return "BEARISH"

    if sentiment in (

        "POSITIVE",

        "BULLISH",

        "VERY BULLISH"

    ):

        return "BULLISH"

    if sentiment in (

        "NEGATIVE",

        "BEARISH",

        "VERY BEARISH"

    ):

        return "BEARISH"

    return "NEUTRAL"


# =========================================================
# EVENT CLASSIFICATION
# =========================================================

def _classify_article(
    article
):
    """
    Classify article impact.

    Returns:
        HIGH
        MEDIUM
        LOW
    """

    text = _article_text(
        article
    )

    # =====================================================
    # HIGH IMPACT
    # =====================================================

    for keyword in HIGH_IMPACT_KEYWORDS:

        if keyword in text:

            return "HIGH"

    # =====================================================
    # MEDIUM IMPACT
    # =====================================================

    for keyword in MEDIUM_IMPACT_KEYWORDS:

        if keyword in text:

            return "MEDIUM"

    # =====================================================
    # LOW IMPACT
    # =====================================================

    return "LOW"


# =========================================================
# CORE EVENT DETECTION
# =========================================================

def detect_market_events(
    source=None
):
    """
    Detect important market events.

    Parameters
    ----------
    source : list | dict | str | None

        Supported:
        - List of news articles
        - News result dictionary
        - Shared MarketContext dictionary

    Returns
    -------
    dict
        Standardized Market Events intelligence.

    Important
    ---------
    If a symbol string is passed directly, this engine
    returns a safe empty result because MarketEvents does
    not independently fetch news.
    """

    result = _empty_result()

    # =====================================================
    # EXTRACT ARTICLES
    # =====================================================

    articles = _extract_articles(
        source
    )

    # =====================================================
    # NO ARTICLES
    # =====================================================

    if not articles:

        if isinstance(
            source,
            str
        ):

            result["message"] = (

                "No news evidence supplied. "
                "CentralBrain should pass the News "
                "section or Shared MarketContext."
            )

        else:

            result["message"] = (

                "No market events detected "
                "because no news articles were available."
            )

        return result

    # =====================================================
    # ANALYZE ARTICLES
    # =====================================================

    for article in articles:

        # -------------------------------------------------
        # NORMALIZE
        # -------------------------------------------------

        if not isinstance(
            article,
            dict
        ):

            article = {

                "title": _safe_text(
                    article
                )

            }

        # -------------------------------------------------
        # IMPACT
        # -------------------------------------------------

        impact = _classify_article(
            article
        )

        event = dict(
            article
        )

        event[
            "event_impact"
        ] = impact

        # -------------------------------------------------
        # DIRECTION
        # -------------------------------------------------

        direction = _event_direction(
            article
        )

        event[
            "event_direction"
        ] = direction

        # -------------------------------------------------
        # STORE
        # -------------------------------------------------

        if impact == "HIGH":

            result[
                "high_impact"
            ].append(
                event
            )

        elif impact == "MEDIUM":

            result[
                "medium_impact"
            ].append(
                event
            )

        else:

            result[
                "low_impact"
            ].append(
                event
            )

        # -------------------------------------------------
        # DIRECTION COUNTS
        # -------------------------------------------------

        if direction == "BULLISH":

            result[
                "bullish_events"
            ] += 1

        elif direction == "BEARISH":

            result[
                "bearish_events"
            ] += 1

        else:

            result[
                "neutral_events"
            ] += 1

    # =====================================================
    # COUNTS
    # =====================================================

    high = len(
        result[
            "high_impact"
        ]
    )

    medium = len(
        result[
            "medium_impact"
        ]
    )

    low = len(
        result[
            "low_impact"
        ]
    )

    total = (

        high
        +
        medium
        +
        low

    )

    result[
        "high_impact_count"
    ] = high

    result[
        "medium_impact_count"
    ] = medium

    result[
        "low_impact_count"
    ] = low

    result[
        "total_events"
    ] = total

    # =====================================================
    # MARKET ALERT
    # =====================================================

    if high >= 3:

        result[
            "market_alert"
        ] = "HIGH IMPACT"

        result[
            "risk_level"
        ] = "HIGH"

    elif high >= 1:

        result[
            "market_alert"
        ] = "WATCH MARKET"

        result[
            "risk_level"
        ] = "MEDIUM"

    elif medium >= 5:

        result[
            "market_alert"
        ] = "ACTIVE NEWS"

        result[
            "risk_level"
        ] = "MEDIUM"

    else:

        result[
            "market_alert"
        ] = "NORMAL"

        result[
            "risk_level"
        ] = "LOW"

    # =====================================================
    # SIGNAL
    # =====================================================

    bullish = result[
        "bullish_events"
    ]

    bearish = result[
        "bearish_events"
    ]

    directional = bullish + bearish

    if bullish > bearish:

        if (

            bullish >= 3

            and bullish >= bearish * 2

        ):

            signal = "STRONG BUY"

        else:

            signal = "BUY"

    elif bearish > bullish:

        if (

            bearish >= 3

            and bearish >= bullish * 2

        ):

            signal = "STRONG SELL"

        else:

            signal = "SELL"

    else:

        signal = "HOLD"

    result[
        "signal"
    ] = signal

    # =====================================================
    # CONFIDENCE
    # =====================================================

    if total <= 0:

        confidence = 0

    else:

        dominant = max(
            bullish,
            bearish
        )

        conflicting = min(
            bullish,
            bearish
        )

        impact_strength = (

            high * 15

            +

            medium * 8

            +

            low * 2

        )

        confidence = (

            25

            +

            dominant * 10

            +

            impact_strength

            -

            conflicting * 5

        )

        confidence = min(

            95,

            max(
                20,
                confidence
            )

        )

    result[
        "confidence"
    ] = round(
        confidence,
        2
    )

    # =====================================================
    # EXPLAINABLE EVIDENCE
    # =====================================================

    for event in (

        result[
            "high_impact"
        ]

        +

        result[
            "medium_impact"
        ]

    ):

        title = _safe_text(

            event.get(
                "title"
            )

        )

        direction = event.get(
            "event_direction"
        )

        if not title:

            continue

        if direction == "BULLISH":

            result[
                "supporting_evidence"
            ].append(
                title
            )

        elif direction == "BEARISH":

            result[
                "conflicting_evidence"
            ].append(
                title
            )

    return result


# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    sample_articles = [

        {

            "title": (
                "RBI announces interest rate decision"
            ),

            "description": (
                "Markets react to inflation outlook"
            ),

            "sentiment": "Neutral"

        },

        {

            "title": (
                "Company reports strong quarterly profit"
            ),

            "description": (
                "Revenue growth beats expectations"
            ),

            "sentiment": "Positive"

        }

    ]

    result = detect_market_events(
        sample_articles
    )

    from pprint import pprint

    pprint(
        result
    )
