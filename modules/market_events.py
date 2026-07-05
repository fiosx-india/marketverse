"""
Market Events Engine
Detects major market moving events from news articles.
"""

from datetime import datetime


def detect_market_events(articles):
    """
    Detect important market events.

    Returns:
        {
            "high_impact": [...],
            "medium_impact": [...],
            "low_impact": [...],
            "market_alert": str,
            "risk_level": str
        }
    """

    result = {
        "high_impact": [],
        "medium_impact": [],
        "low_impact": [],
        "market_alert": "NORMAL",
        "risk_level": "LOW",
        "generated_at": str(datetime.now())
    }

    high_keywords = [
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
        "sanction"
    ]

    medium_keywords = [
        "earnings",
        "results",
        "profit",
        "revenue",
        "ipo",
        "listing",
        "merger",
        "acquisition",
        "dividend",
        "buyback"
    ]

    for article in articles:

        text = (
            article.get("title", "") +
            " " +
            article.get("description", "")
        ).lower()

        matched = False

        for word in high_keywords:
            if word in text:
                result["high_impact"].append(article)
                matched = True
                break

        if matched:
            continue

        for word in medium_keywords:
            if word in text:
                result["medium_impact"].append(article)
                matched = True
                break

        if not matched:
            result["low_impact"].append(article)

    high = len(result["high_impact"])
    medium = len(result["medium_impact"])

    if high >= 3:
        result["market_alert"] = "HIGH IMPACT"
        result["risk_level"] = "HIGH"

    elif high >= 1:
        result["market_alert"] = "WATCH MARKET"
        result["risk_level"] = "MEDIUM"

    elif medium >= 5:
        result["market_alert"] = "ACTIVE NEWS"
        result["risk_level"] = "MEDIUM"

    return result
