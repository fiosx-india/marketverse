from newsapi import NewsApiClient

# -----------------------------------------
# News API
# -----------------------------------------

API_KEY = "0ff63bf45b2c4e30be128d5362382ebe"

newsapi = NewsApiClient(api_key=API_KEY)


def get_market_news(symbol=None, limit=10):
    """
    Get latest market or stock news
    """

    try:

        if symbol:

            response = newsapi.get_everything(
                q=symbol,
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

        for article in response.get("articles", []):

            articles.append({

                "title": article.get("title"),

                "description": article.get("description"),

                "source": article["source"]["name"],

                "url": article.get("url"),

                "published": article.get("publishedAt")

            })

        return articles

    except Exception as e:

        print("News Error:", e)

        return []
