"""
MarketVerse AI
Decision Core
Combines all analysis and produces the final decision.
"""

class DecisionCore:

    def __init__(self):
        pass

    def decide(self, analysis):

        score = 0

        # Technical
        technical = analysis.get("technical", {})
        if technical.get("signal") == "BUY":
            score += 2
        elif technical.get("signal") == "SELL":
            score -= 2

        # AI Prediction
        ai = analysis.get("ai", {})
        if ai.get("prediction") == "UP":
            score += 2
        elif ai.get("prediction") == "DOWN":
            score -= 2

        # News Sentiment
        news = analysis.get("news_analysis", {})
        sentiment = news.get("sentiment")

        if sentiment == "POSITIVE":
            score += 1
        elif sentiment == "NEGATIVE":
            score -= 1

        # Pattern
        pattern = analysis.get("pattern", {})
        if pattern.get("bullish"):
            score += 1
        if pattern.get("bearish"):
            score -= 1

        # Final Decision
        if score >= 4:
            decision = "STRONG BUY"
        elif score >= 2:
            decision = "BUY"
        elif score <= -4:
            decision = "STRONG SELL"
        elif score <= -2:
            decision = "SELL"
        else:
            decision = "HOLD"

        return {
            "score": score,
            "decision": decision
        }
