"""
=========================================================
MarketVerse AI - News Analysis Engine
=========================================================

Fetches news headlines and calculates sentiment.

Future Ready:
- NewsAPI
- Finnhub
- Alpha Vantage News
- AI Summarization

=========================================================
"""

from datetime import datetime


POSITIVE_WORDS = {
    "gain", "growth", "profit", "profits",
    "bullish", "buy", "upgrade",
    "strong", "positive", "surge",
    "beat", "record", "expansion",
    "optimistic", "rise", "rally"
}

NEGATIVE_WORDS = {
    "loss", "losses", "bearish",
    "sell", "downgrade", "weak",
    "drop", "fall", "crash",
    "decline", "fraud", "lawsuit",
    "bankruptcy", "negative",
    "miss", "warning"
}


def calculate_sentiment(text):

    text = text.lower()

    positive = 0
    negative = 0

    for word in POSITIVE_WORDS:
        if word in text:
            positive += 1

    for word in NEGATIVE_WORDS:
        if word in text:
            negative += 1

    score = positive - negative

    if score >= 2:
        sentiment = "VERY BULLISH"

    elif score == 1:
        sentiment = "BULLISH"

    elif score == 0:
        sentiment = "NEUTRAL"

    elif score == -1:
        sentiment = "BEARISH"

    else:
        sentiment = "VERY BEARISH"

    confidence = min(
        100,
        max(40, abs(score) * 25 + 50)
    )

    return {
        "score": score,
        "sentiment": sentiment,
        "confidence": confidence
    }


def analyze_news(symbol, headlines=None):
    """
    Analyze news sentiment.

    Parameters
    ----------
    symbol : str

    headlines : list[str]
        Optional headline list.
    """

    if headlines is None:
        headlines = []

    if len(headlines) == 0:
        return {
            "symbol": symbol,
            "headline_count": 0,
            "overall_sentiment": "NO NEWS",
            "confidence": 0,
            "score": 0,
            "headlines": [],
            "updated": str(datetime.now())
        }

    scores = []

    analysed = []

    for headline in headlines:

        result = calculate_sentiment(headline)

        scores.append(result["score"])

        analysed.append({
            "headline": headline,
            "sentiment": result["sentiment"],
            "score": result["score"]
        })

    average = sum(scores) / len(scores)

    if average >= 2:
        overall = "VERY BULLISH"

    elif average >= 1:
        overall = "BULLISH"

    elif average > -1:
        overall = "NEUTRAL"

    elif average > -2:
        overall = "BEARISH"

    else:
        overall = "VERY BEARISH"

    confidence = min(
        100,
        max(50, abs(average) * 25 + 50)
    )

    return {

        "symbol": symbol,

        "headline_count": len(headlines),

        "overall_sentiment": overall,

        "confidence": round(confidence, 2),

        "score": round(average, 2),

        "headlines": analysed,

        "updated": str(datetime.now())
    }


def get_dummy_news(symbol):
    """
    Demo headlines.
    """

    return [

        f"{symbol} reports strong quarterly profit growth",

        f"{symbol} receives broker upgrade",

        f"Investors remain optimistic about {symbol}"
    ]


if __name__ == "__main__":

    symbol = "RELIANCE"

    news = get_dummy_news(symbol)

    result = analyze_news(symbol, news)

    from pprint import pprint

    pprint(result)
