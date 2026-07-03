from newsapi import NewsApiClient

# உங்கள் NewsAPI Key-ஐ இங்கே இடுங்கள்
API_KEY = "YOUR_NEWS_API_KEY"

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
