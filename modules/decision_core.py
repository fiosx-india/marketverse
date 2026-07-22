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

        # -----------------------------
        # Technical Analysis
        # -----------------------------
        technical = analysis.get("technical", {})

        if technical.get("signal") == "BUY":
            score += 2

        elif technical.get("signal") == "SELL":
            score -= 2

        # -----------------------------
        # AI Prediction
        # -----------------------------
        ai = analysis.get("ai", {})

        if ai.get("prediction") == "UP":
            score += 2

        elif ai.get("prediction") == "DOWN":
            score -= 2

        # -----------------------------
        # News Sentiment
        # -----------------------------
        news = analysis.get("news_analysis", {})

        sentiment = news.get("sentiment")

        if sentiment == "POSITIVE":
            score += 1

        elif sentiment == "NEGATIVE":
            score -= 1

        # -----------------------------
        # Pattern Analysis
        # -----------------------------
        pattern = analysis.get("pattern", {})

        if pattern.get("bullish"):
            score += 1

        if pattern.get("bearish"):
            score -= 1

        # -----------------------------
        # Final Decision
        # -----------------------------
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

        # -----------------------------
        # Confidence Score
        # -----------------------------
        confidence = min(abs(score) * 20 + 20, 100)

        # -----------------------------
        # Reason Generator
        # -----------------------------
        reason = []

        if technical.get("signal") == "BUY":
            reason.append("Technical indicators are Bullish")

        elif technical.get("signal") == "SELL":
            reason.append("Technical indicators are Bearish")

        if ai.get("prediction") == "UP":
            reason.append("AI predicts upward movement")

        elif ai.get("prediction") == "DOWN":
            reason.append("AI predicts downward movement")

        if sentiment == "POSITIVE":
            reason.append("Positive market sentiment")

        elif sentiment == "NEGATIVE":
            reason.append("Negative market sentiment")

        if pattern.get("bullish"):
            reason.append("Bullish chart pattern detected")

        if pattern.get("bearish"):
            reason.append("Bearish chart pattern detected")

        if not reason:
            reason.append("Market is neutral")

        # -----------------------------
        # Return Result
        # -----------------------------
        return {
            "score": score,
            "decision": decision,
            "confidence": confidence,
            "reason": reason
        }
