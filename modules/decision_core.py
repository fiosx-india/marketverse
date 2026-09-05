"""
MarketVerse AI
Decision Core

Combines analysis evidence and produces
the final decision.
"""


class DecisionCore:
    """
    Final Decision Layer

    Supports both:

    1. Legacy analysis dictionary
    2. Shared MarketContext object

    This module does not perform market analysis.
    It combines evidence already produced by the
    intelligence pipeline.
    """

    def decide(self, analysis):

        # Resolve Dictionary or MarketContext
        analysis = self._resolve_analysis(analysis)

        # ---------------------------------
        # Read Analysis Sections
        # ---------------------------------

        technical = self._section(
            analysis,
            "technical"
        )

        ai = self._section(
            analysis,
            "ai"
        )

        news = self._section(
            analysis,
            "news_analysis"
        )

        pattern = self._section(
            analysis,
            "pattern"
        )

        # ---------------------------------
        # Decision Score
        # ---------------------------------

        score = 0
        reasons = []

        # ---------------------------------
        # Technical Analysis
        # ---------------------------------

        technical_signal = str(
            technical.get("signal", "")
        ).upper()

        if technical_signal == "BUY":

            score += 2

            reasons.append(
                "Technical indicators are Bullish"
            )

        elif technical_signal == "SELL":

            score -= 2

            reasons.append(
                "Technical indicators are Bearish"
            )

        # ---------------------------------
        # AI Prediction
        # ---------------------------------

        ai_prediction = str(
            ai.get("prediction", "")
        ).upper()

        if ai_prediction == "UP":

            score += 2

            reasons.append(
                "AI predicts upward movement"
            )

        elif ai_prediction == "DOWN":

            score -= 2

            reasons.append(
                "AI predicts downward movement"
            )

        # ---------------------------------
        # News Sentiment
        # ---------------------------------

        sentiment = str(
            news.get("sentiment", "")
        ).upper()

        if sentiment in (
            "POSITIVE",
            "BULLISH",
            "VERY BULLISH"
        ):

            score += 1

            reasons.append(
                "Positive market sentiment"
            )

        elif sentiment in (
            "NEGATIVE",
            "BEARISH",
            "VERY BEARISH"
        ):

            score -= 1

            reasons.append(
                "Negative market sentiment"
            )

        # ---------------------------------
        # Pattern Analysis
        # ---------------------------------

        if pattern.get("bullish"):

            score += 1

            reasons.append(
                "Bullish chart pattern detected"
            )

        if pattern.get("bearish"):

            score -= 1

            reasons.append(
                "Bearish chart pattern detected"
            )

        # ---------------------------------
        # Final Decision
        # ---------------------------------

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

        # ---------------------------------
        # Confidence
        # ---------------------------------

        confidence = min(
            abs(score) * 20 + 20,
            100
        )

        # ---------------------------------
        # Neutral Market
        # ---------------------------------

        if not reasons:

            reasons.append(
                "Market is neutral"
            )

        # ---------------------------------
        # Final Result
        # ---------------------------------

        return {

            "score": score,

            "decision": decision,

            "confidence": confidence,

            "reason": reasons
        }

    # =================================
    # Internal Helpers
    # =================================

    @staticmethod
    def _resolve_analysis(analysis):
        """
        Accept either:

        - Dictionary
        - MarketContext-like object
        """

        # Normal dictionary
        if isinstance(analysis, dict):

            return analysis

        # MarketContext
        get_context = getattr(
            analysis,
            "get",
            None
        )

        if callable(get_context):

            resolved = get_context()

            if isinstance(resolved, dict):

                return resolved

        raise TypeError(

            "DecisionCore.decide() expects "
            "a dictionary or MarketContext-like object"

        )

    @staticmethod
    def _section(analysis, key):
        """
        Safely read a section.
        """

        value = analysis.get(
            key,
            {}
        )

        if isinstance(value, dict):

            return value

        return {}
