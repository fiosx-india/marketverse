"""
=========================================
MarketVerse AI - Sentiment Engine
=========================================
Analyzes market news sentiment and
returns a sentiment score (0-100)
=========================================
"""

def analyze_sentiment(news_list):
    """
    Analyze news headlines and return sentiment.
    """

    positive_words = [
        "gain", "gains", "growth", "profit", "profits",
        "strong", "bullish", "surge", "rise", "positive",
        "record", "beat", "expansion", "upgrade"
    ]

    negative_words = [
        "loss", "losses", "bearish", "crash", "fall",
        "drop", "decline", "warning", "downgrade",
        "weak", "risk", "lawsuit", "inflation"
    ]

    score = 50

    if not news_list:
        return {
            "score": 50,
            "label": "NEUTRAL",
            "positive": 0,
            "negative": 0
        }

    positive_count = 0
    negative_count = 0

    for news in news_list:

        text = str(news).lower()

        for word in positive_words:
            if word in text:
                positive_count += 1
                score += 5

        for word in negative_words:
            if word in text:
                negative_count += 1
                score -= 5

    score = max(0, min(100, score))

    if score >= 70:
        label = "POSITIVE"

    elif score <= 30:
        label = "NEGATIVE"

    else:
        label = "NEUTRAL"

    return {
        "score": score,
        "label": label,
        "positive": positive_count,
        "negative": negative_count
    }
