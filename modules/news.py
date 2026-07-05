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
