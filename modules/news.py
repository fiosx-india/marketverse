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

            if url in seen_urls:
                continue

            seen_urls.add(url)
