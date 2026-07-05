from newsapi import NewsApiClient
from datetime import datetime
from functools import lru_cache

# ==========================================
# Configuration
# ==========================================

API_KEY = "YOUR_NEWSAPI_KEY"

newsapi = NewsApiClient(api_key=API_KEY)

# ==========================================
# Helper Functions
# ==========================================

def clean_symbol(symbol):
    """
    Convert NSE/BSE symbols into search keyword.
    Example:
        RELIANCE.NS -> RELIANCE
        TCS.BO -> TCS
    """
    if not symbol:
        return None

    symbol = symbol.upper()

    if "." in symbol:
        symbol = symbol.split(".")[0]

    return symbol


def format_article(article):
    """
    Format NewsAPI article into standard structure.
    """
    return {
        "title": article.get("title", ""),
        "description": article.get("description", ""),
        "source": article.get("source", {}).get("name", ""),
        "url": article.get("url", ""),
        "published": article.get("publishedAt", ""),
    }


# ==========================================
# Main Function
# ==========================================

@lru_cache(maxsize=100)
def get_market_news(symbol=None, limit=10):

    try:

        query = clean_symbol(symbol)

        if query:

            response = newsapi.get_everything(
                q=query,
                language="en",
                sort_by="publishedAt",
                page_size=limit
            )

        else:

            response = newsapi.get_top_headlines(
                category="business",
                language="en",
                page_size=limit
            )

        articles = []
        seen_urls = set()

        # ==========================================
        # Process Articles
        # ==========================================

        positive_words = [
            "gain", "growth", "profit", "surge",
            "bullish", "beat", "strong", "upgrade"
        ]

        negative_words = [
            "loss", "fall", "drop", "bearish",
            "downgrade", "weak", "crash", "decline"
        ]

        for article in response.get("articles", []):

            url = article.get("url")

            if not url or url in seen_urls:
                continue

            seen_urls.add(url)

            item = format_article(article)

            text = (
                item["title"] + " " +
                item["description"]
            ).lower()

            sentiment = "Neutral"

            if any(word in text for word in positive_words):
                sentiment = "Positive"

            elif any(word in text for word in negative_words):
                sentiment = "Negative"

            item["sentiment"] = sentiment

            articles.append(item)

        # ==========================================
        # Relevance Score
        # ==========================================

        if query:

            keyword = query.lower()

            for article in articles:

                score = 0

                title = article["title"].lower()
                description = article["description"].lower()

                if keyword in title:
                    score += 70

                if keyword in description:
                    score += 30

                article["relevance_score"] = score

        else:

            for article in articles:

                article["relevance_score"] = 50

        # ==========================================
        # AI Confidence
        # ==========================================

        for article in articles:

            confidence = 50

            if article["sentiment"] == "Positive":
                confidence += 20

            elif article["sentiment"] == "Negative":
                confidence += 15

            confidence += article["relevance_score"] // 5

            article["ai_confidence"] = min(confidence, 100)


        # ==========================================
        # Category, Risk & Summary
        # ==========================================

        for article in articles:

            text = (
                article["title"] + " " +
                article["description"]
            ).lower()

            category = "General"

            if "earnings" in text or "results" in text:
                category = "Earnings"

            elif "dividend" in text:
                category = "Dividend"

            elif "ipo" in text:
                category = "IPO"

            elif "merger" in text or "acquisition" in text:
                category = "Merger"

            elif "upgrade" in text or "downgrade" in text:
                category = "Broker Action"

            elif "lawsuit" in text:
                category = "Legal"

            article["category"] = category

            if article["sentiment"] == "Positive":
                article["risk_level"] = "Low"

            elif article["sentiment"] == "Negative":
                article["risk_level"] = "High"

            else:
                article["risk_level"] = "Medium"

            summary = article["description"]

            if not summary:
                summary = article["title"]

            article["summary"] = summary[:200]

        # ==========================================
        # Trending & Quality Score
        # ==========================================

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

        for article in articles:

            text = (
                article["title"] + " " +
                article["description"]
            ).lower()

            trending_score = 0

            for keyword in trending_keywords:

                if keyword in text:
                    trending_score += 10

            article["trending_score"] = min(trending_score, 100)

            article["breaking"] = any(
                word in text
                for word in ["breaking", "urgent", "flash"]
            )

            quality = 50

            if article["description"]:
                quality += 20

            if article["source"]:
                quality += 15

            if article["url"]:
                quality += 15

            article["quality_score"] = min(quality, 100)

        # ==========================================
        # Final Ranking
        # ==========================================

        articles.sort(
            key=lambda x: (
                x["ai_confidence"] +
                x["quality_score"] +
                x["trending_score"]
            ),
            reverse=True
        )

        # ==========================================
        # Market Impact & Recommendation
        # ==========================================

        for article in articles:

            impact = (
                article["ai_confidence"] * 0.4 +
                article["quality_score"] * 0.2 +
                article["trending_score"] * 0.2 +
                article["relevance_score"] * 0.2
            )

            article["market_impact"] = round(impact, 2)

            recommendation = "HOLD"

            if (
                article["sentiment"] == "Positive"
                and impact >= 75
            ):
                recommendation = "BUY"

            elif (
                article["sentiment"] == "Negative"
                and impact >= 75
            ):
                recommendation = "SELL"

            article["recommendation"] = recommendation

        # ==========================================
        # Watchlist Priority
        # ==========================================

        watchlist = [
            "RELIANCE",
            "TCS",
            "INFY",
            "HDFCBANK",
            "ICICIBANK",
            "SBIN",
            "BTC",
            "ETH",
            "GOLD"
        ]

        for article in articles:

            priority = "Normal"

            title = article["title"].upper()

            for stock in watchlist:

                if stock in title:
                    priority = "High"
                    break

            article["priority"] = priority

        articles.sort(
            key=lambda x: (
                x["priority"] == "High",
                x["market_impact"],
                x["ai_confidence"]
            ),
            reverse=True
        )

        # ==========================================
        # Overall Analytics
        # ==========================================

        positive = sum(
            1 for a in articles
            if a["sentiment"] == "Positive"
        )

        negative = sum(
            1 for a in articles
            if a["sentiment"] == "Negative"
        )

        neutral = sum(
            1 for a in articles
            if a["sentiment"] == "Neutral"
        )

        total = len(articles)

        if total:

            bullish_percent = round((positive / total) * 100, 2)
            bearish_percent = round((negative / total) * 100, 2)
            neutral_percent = round((neutral / total) * 100, 2)

        else:

            bullish_percent = 0
            bearish_percent = 0
            neutral_percent = 0

        analytics = {

            "total_news": total,
            "positive_news": positive,
            "negative_news": negative,
            "neutral_news": neutral,

            "bullish_percent": bullish_percent,
            "bearish_percent": bearish_percent,
            "neutral_percent": neutral_percent,

            "generated_at": str(datetime.now())

        }

return {
    "articles": articles[:limit],
    "analytics": analytics
}

except Exception as e:
    return {
        "articles": [],
        "analytics": {
            "total_news": 0,
            "positive_news": 0,
            "negative_news": 0,
            "neutral_news": 0,
            "bullish_percent": 0,
            "bearish_percent": 0,
            "neutral_percent": 0,
            "generated_at": str(datetime.now())
        },
        "error": str(e)
    }
