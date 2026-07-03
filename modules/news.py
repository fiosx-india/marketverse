from newsapi import NewsApiClient

API_KEY = "0ff63bf45b2c4e30be128d5362382ebe"

newsapi = NewsApiClient(api_key=API_KEY)

def get_market_news():
    try:
        news = newsapi.get_top_headlines(
            category="business",
            language="en",
            page_size=10
        )
        return news["articles"]

    except Exception as e:
        return [{"title": str(e)}]
