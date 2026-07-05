from newsapi import NewsApiClient
from datetime import datetime
from functools import lru_cache
import requests

# ==========================================
# Configuration
# ==========================================

API_KEY = "0ff63bf45b2c4e30be128d5362382ebe"

newsapi = NewsApiClient(api_key=API_KEY)

# ==========================================
# Helper Functions
# ==========================================

def clean_symbol(symbol):
    """
    Convert NSE/BSE symbols into company keyword
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

    return {
        "title": article.get("title", ""),
        "description": article.get("description", ""),
        "source": article.get("source", {}).get("name", ""),
        "url": article.get("url", ""),
        "published": article.get("publishedAt", ""),
    }


@lru_cache(maxsize=100)
def get_market_news(symbol=None, limit=10):
    """
    Download latest market news
    """

    try:

        if symbol:

            query = clean_symbol(symbol)

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

        # ==========================================
        # Convert Articles
        # ==========================================

        articles = []

        seen_urls = set()

        for article in response.get("articles", []):

            url = article.get("url")

            # Skip duplicate news
            if url in seen_urls:
                continue

            seen_urls.add(url)

            title = article.get("title") or ""
            description = article.get("description") or ""

            text = (title + " " + description).lower()

            # Basic Sentiment
            positive_words = [
                "gain", "growth", "profit", "surge",
                "bullish", "beat", "strong", "upgrade"
            ]

            negative_words = [
                "loss", "fall", "drop", "bearish",
                "downgrade", "weak", "crash", "decline"
            ]

            sentiment = "Neutral"

            if any(word in text for word in positive_words):
                sentiment = "Positive"

            elif any(word in text for word in negative_words):
                sentiment = "Negative"

            # Impact Score
            impact = 50

            if sentiment == "Positive":
                impact = 80

            elif sentiment == "Negative":
                impact = 75

            articles.append({

                "title": title,

                "description": description,

                "source": article.get("source", {}).get("name", ""),

                "url": url,

                "published": article.get("publishedAt"),

                "sentiment": sentiment,

                "impact_score": impact

            })

        # ==========================================
        # Sort News (Latest First)
        # ==========================================

        articles = sorted(
            articles,
            key=lambda x: x.get("published", ""),
            reverse=True
        )

        # ==========================================
        # Relevance Score
        # ==========================================

        if symbol:

            keyword = clean_symbol(symbol).lower()

            for article in articles:

                score = 0

                title = article["title"].lower()
                desc = article["description"].lower()

                if keyword in title:
                    score += 70

                if keyword in desc:
                    score += 30

                article["relevance_score"] = score

        else:

            for article in articles:
                article["relevance_score"] = 50

        # ==========================================
        # AI Confidence Score
        # ==========================================

        for article in articles:

            confidence = 50

            if article["sentiment"] == "Positive":
                confidence += 20

            elif article["sentiment"] == "Negative":
                confidence += 15

            confidence += article["relevance_score"] // 5

            article["ai_confidence"] = min(confidence, 100)

        return articles

        # ==========================================
        # News Category & Risk
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

            elif "acquisition" in text or "merger" in text:
                category = "Merger"

            elif "ipo" in text:
                category = "IPO"

            elif "lawsuit" in text:
                category = "Legal"

            elif "upgrade" in text or "downgrade" in text:
                category = "Broker Action"

            article["category"] = category

            # Risk Level

            risk = "Medium"

            if article["sentiment"] == "Positive":
                risk = "Low"

            elif article["sentiment"] == "Negative":
                risk = "High"

            article["risk_level"] = risk

            # Short AI Summary

            summary = article["description"]

            if not summary:
                summary = article["title"]

            article["summary"] = summary[:200]

        # ==========================================
        # Trending / Freshness / Quality Score
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

            # ==========================================
            # Breaking News
            # ==========================================

            breaking = False

            if (
                "breaking" in text
                or "urgent" in text
                or "flash" in text
            ):
                breaking = True

            article["breaking"] = breaking

            # ==========================================
            # News Quality Score
            # ==========================================

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
        # Market Impact Rating
        # ==========================================

        for article in articles:

            impact = 0

            impact += article.get("ai_confidence", 50) * 0.4
            impact += article.get("quality_score", 50) * 0.2
            impact += article.get("trending_score", 0) * 0.2
            impact += article.get("relevance_score", 0) * 0.2

            article["market_impact"] = round(impact, 2)

            # ==========================================
            # Trading Recommendation
            # ==========================================

            recommendation = "HOLD"

            if (
                article["sentiment"] == "Positive"
                and article["market_impact"] >= 75
            ):
                recommendation = "BUY"

            elif (
                article["sentiment"] == "Negative"
                and article["market_impact"] >= 75
            ):
                recommendation = "SELL"

            article["recommendation"] = recommendation

        # ==========================================
        # Portfolio Watchlist Priority
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

        # ==========================================
        # Final Sort
        # ==========================================

        articles.sort(

            key=lambda x: (
                x["priority"] == "High",
                x["market_impact"],
                x["ai_confidence"]
            ),

            reverse=True

        )

        # ==========================================
        # Overall News Analytics
        # ==========================================

        positive = 0
        negative = 0
        neutral = 0

        for article in articles:

            if article["sentiment"] == "Positive":
                positive += 1

            elif article["sentiment"] == "Negative":
                negative += 1

            else:
                neutral += 1

        total = len(articles)

        if total > 0:

            bullish_percent = round(
                (positive / total) * 100,
                2
            )

            bearish_percent = round(
                (negative / total) * 100,
                2
            )

            neutral_percent = round(
                (neutral / total) * 100,
                2
            )

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

            "articles": articles,

            "analytics": analytics

        }

        # ==========================================
        # AI Market Mood
        # ==========================================

        if bullish_percent >= 70:
            market_mood = "🟢 Strong Bullish"

        elif bullish_percent >= 55:
            market_mood = "🟢 Bullish"

        elif bearish_percent >= 70:
            market_mood = "🔴 Strong Bearish"

        elif bearish_percent >= 55:
            market_mood = "🔴 Bearish"

        else:
            market_mood = "🟡 Neutral"

        analytics["market_mood"] = market_mood

        # ==========================================
        # Confidence Score
        # ==========================================

        confidence = 50

        confidence += bullish_percent * 0.30
        confidence -= bearish_percent * 0.20

        confidence = max(0, min(100, round(confidence, 2)))

        analytics["confidence"] = confidence

        # ==========================================
        # Trading Signal
        # ==========================================

        if confidence >= 80:
            analytics["signal"] = "STRONG BUY"

        elif confidence >= 65:
            analytics["signal"] = "BUY"

        elif confidence <= 25:
            analytics["signal"] = "STRONG SELL"

        elif confidence <= 40:
            analytics["signal"] = "SELL"

        else:
            analytics["signal"] = "HOLD"

        # ==========================================
        # Market Event Detection
        # ==========================================

        economic_keywords = [
            "inflation",
            "interest rate",
            "federal reserve",
            "fed",
            "rbi",
            "gdp",
            "cpi",
            "repo",
            "budget",
            "policy"
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

        analytics["economic_events"] = 0
        analytics["earnings_news"] = 0
        analytics["ipo_news"] = 0
        analytics["crypto_news"] = 0
        analytics["institutional_news"] = 0

        for article in articles:

            text = (
                article["title"] + " " +
                article["description"]
            ).lower()

            if any(k in text for k in economic_keywords):
                analytics["economic_events"] += 1

            if any(k in text for k in earnings_keywords):
                analytics["earnings_news"] += 

        # ==========================================
        # Source Reliability Score
        # ==========================================

        trusted_sources = [

            "Reuters",
            "Bloomberg",
            "CNBC",
            "Moneycontrol",
            "Economic Times",
            "Business Standard",
            "Yahoo Finance",
            "MarketWatch",
            "Financial Times"

        ]

        analytics["trusted_news"] = 0

        for article in articles:

            source = article.get("source", "")

            reliability = 60

            if source in trusted_sources:

                reliability = 95

                analytics["trusted_news"] += 1

            article["reliability_score"] = reliability

        # ==========================================
        # Overall Market Risk
        # ==========================================

        risk_score = (
            analytics["bearish_percent"] * 0.5 +
            analytics["economic_events"] * 3 +
            analytics["institutional_news"] * 2
        )

        if risk_score >= 70:

            analytics["market_risk"] = "HIGH"

        elif risk_score >= 40:

            analytics["market_risk"] = "MEDIUM"

        else:
            
            analytics["market_risk"] = "LOW"

        # ==========================================
        # AI Trading Recommendation
        # ==========================================

        buy_score = 0
        sell_score = 0

        buy_score += analytics["bullish_percent"]
        sell_score += analytics["bearish_percent"]

        buy_score += analytics["trusted_news"] * 2
        sell_score += analytics["economic_events"]

        if analytics["market_risk"] == "LOW":
            buy_score += 10

        elif analytics["market_risk"] == "HIGH":
            sell_score += 15

        if buy_score >= sell_score + 20:

            analytics["ai_recommendation"] = "🟢 BUY"

        elif sell_score >= buy_score + 20:

            analytics["ai_recommendation"] = "🔴 SELL"

        else:

            analytics["ai_recommendation"] = "🟡 HOLD"

        analytics["buy_score"] = round(buy_score, 2)
        analytics["sell_score"] = round(sell_score, 2)

        # ==========================================
        # News Engine Version
        # ==========================================

        analytics["engine"] = "MarketVerse AI News Engine v4.0"
