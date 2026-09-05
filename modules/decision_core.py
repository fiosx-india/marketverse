"""
=========================================================
MarketVerse AI
Decision Core
=========================================================

Purpose
-------
Combines intelligence evidence produced by the
MarketVerse AI pipeline and produces one final
explainable decision.

DecisionCore is the final decision layer.

It DOES:
- Combine intelligence evidence
- Evaluate bullish and bearish evidence
- Consider confidence
- Consider risk restrictions
- Produce one final decision
- Produce explainable reasoning

It DOES NOT:
- Fetch market data
- Perform technical analysis
- Generate predictions
- Generate strategies
- Calculate risk
- Orchestrate the pipeline

Architecture
------------

Analysis Modules
        │
        ▼
Shared MarketContext
        │
        ▼
AI Intelligence
        │
        ▼
Strategy
        │
        ▼
Risk
        │
        ▼
DecisionCore
        │
        ▼
Final Explainable Decision
=========================================================
"""


class DecisionCore:
    """
    Final MarketVerse AI decision layer.

    Supports:

    1. Shared MarketContext object
    2. Standard analysis dictionary
    """

    # =====================================================
    # MAIN DECISION
    # =====================================================

    def decide(self, analysis):

        analysis = self._resolve_analysis(
            analysis
        )

        # =================================================
        # READ INTELLIGENCE SECTIONS
        # =================================================

        technical = self._section(
            analysis,
            "technical"
        )

        prediction = self._section(
            analysis,
            "prediction"
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

        volume = self._section(
            analysis,
            "volume"
        )

        sentiment = self._section(
            analysis,
            "sentiment"
        )

        strategy = self._section(
            analysis,
            "strategy"
        )

        risk = self._section(
            analysis,
            "risk"
        )

        # =================================================
        # DECISION SCORE
        # =================================================

        bullish_score = 0

        bearish_score = 0

        supporting_evidence = []

        conflicting_evidence = []

        confidence_sources = []

        # =================================================
        # TECHNICAL EVIDENCE
        # =================================================

        technical_signal = self._normalize_signal(
            technical.get(
                "signal"
            )
        )

        if technical_signal == "BUY":

            bullish_score += 2

            supporting_evidence.append(
                "Technical analysis is bullish"
            )

        elif technical_signal == "SELL":

            bearish_score += 2

            conflicting_evidence.append(
                "Technical analysis is bearish"
            )

        self._collect_confidence(
            technical,
            confidence_sources
        )

        # =================================================
        # PREDICTION EVIDENCE
        # =================================================

        prediction_signal = self._normalize_signal(
            prediction.get(
                "signal"
            )
        )

        if prediction_signal == "BUY":

            bullish_score += 2

            supporting_evidence.append(
                "Prediction supports upward movement"
            )

        elif prediction_signal == "SELL":

            bearish_score += 2

            conflicting_evidence.append(
                "Prediction supports downward movement"
            )

        self._collect_confidence(
            prediction,
            confidence_sources
        )

        # =================================================
        # AI INTELLIGENCE
        # =================================================

        ai_signal = self._normalize_signal(
            ai.get(
                "signal",

                ai.get(
                    "prediction"
                )
            )
        )

        if ai_signal == "BUY":

            bullish_score += 3

            supporting_evidence.append(
                "AI intelligence supports bullish movement"
            )

        elif ai_signal == "SELL":

            bearish_score += 3

            conflicting_evidence.append(
                "AI intelligence supports bearish movement"
            )

        self._collect_confidence(
            ai,
            confidence_sources
        )

        # =================================================
        # NEWS ANALYSIS
        # =================================================

        news_signal = self._normalize_signal(
            news.get(
                "sentiment"
            )
        )

        if news_signal == "BUY":

            bullish_score += 1

            supporting_evidence.append(
                "News sentiment is positive"
            )

        elif news_signal == "SELL":

            bearish_score += 1

            conflicting_evidence.append(
                "News sentiment is negative"
            )

        self._collect_confidence(
            news,
            confidence_sources
        )

        # =================================================
        # PATTERN ANALYSIS
        # =================================================

        if pattern.get(
            "bullish"
        ):

            bullish_score += 1

            supporting_evidence.append(
                "Bullish chart pattern detected"
            )

        if pattern.get(
            "bearish"
        ):

            bearish_score += 1

            conflicting_evidence.append(
                "Bearish chart pattern detected"
            )

        # =================================================
        # VOLUME ANALYSIS
        # =================================================

        volume_signal = self._normalize_signal(
            volume.get(
                "signal"
            )
        )

        if volume_signal == "BUY":

            bullish_score += 1

            supporting_evidence.append(
                "Volume supports bullish movement"
            )

        elif volume_signal == "SELL":

            bearish_score += 1

            conflicting_evidence.append(
                "Volume supports bearish movement"
            )

        # =================================================
        # MARKET SENTIMENT
        # =================================================

        sentiment_signal = self._normalize_signal(

            sentiment.get(

                "signal",

                sentiment.get(
                    "sentiment"
                )

            )

        )

        if sentiment_signal == "BUY":

            bullish_score += 1

            supporting_evidence.append(
                "Market sentiment supports bullish conditions"
            )

        elif sentiment_signal == "SELL":

            bearish_score += 1

            conflicting_evidence.append(
                "Market sentiment supports bearish conditions"
            )

        # =================================================
        # STRATEGY EVIDENCE
        # =================================================

        strategy_signal = self._normalize_signal(

            strategy.get(

                "action",

                strategy.get(
                    "decision"
                )

            )

        )

        if strategy_signal == "BUY":

            bullish_score += 1

            supporting_evidence.append(
                "Strategy supports a BUY position"
            )

        elif strategy_signal == "SELL":

            bearish_score += 1

            conflicting_evidence.append(
                "Strategy supports a SELL position"
            )

        self._collect_confidence(
            strategy,
            confidence_sources
        )

        # =================================================
        # RISK VALIDATION
        # =================================================

        trade_allowed = risk.get(
            "trade_allowed"
        )

        risk_level = str(

            risk.get(
                "risk_level",
                ""
            )

        ).upper()

        # =================================================
        # FINAL DECISION
        # =================================================

        difference = (

            bullish_score
            -
            bearish_score

        )

        if bullish_score >= 6:

            decision = "STRONG BUY"

        elif difference >= 2:

            decision = "BUY"

        elif bearish_score >= 6:

            decision = "STRONG SELL"

        elif difference <= -2:

            decision = "SELL"

        else:

            decision = "HOLD"

        # =================================================
        # RISK OVERRIDE
        # =================================================
        #
        # RiskManager does not decide market direction.
        #
        # It can only restrict trade execution.
        # =================================================

        risk_restricted = False

        if trade_allowed is False:

            risk_restricted = True

            conflicting_evidence.append(

                "Risk management does not allow an active trade"

            )

        if risk_level == "HIGH":

            conflicting_evidence.append(

                "High risk conditions detected"

            )

        # =================================================
        # CONFIDENCE
        # =================================================

        confidence = self._calculate_confidence(

            bullish_score,

            bearish_score,

            confidence_sources

        )

        probability = round(

            confidence / 100,

            2

        )

        # =================================================
        # DEFAULT EVIDENCE
        # =================================================

        if not supporting_evidence:

            supporting_evidence.append(

                "No strong bullish evidence detected"

            )

        if not conflicting_evidence:

            conflicting_evidence.append(

                "No strong bearish evidence detected"

            )

        # =================================================
        # FINAL RESULT
        # =================================================

        return {

            "status": "success",

            "decision": decision,

            "signal": decision,

            "bullish_score": bullish_score,

            "bearish_score": bearish_score,

            "score": difference,

            "confidence": confidence,

            "probability": probability,

            "risk_restricted": risk_restricted,

            "risk_level": (

                risk_level
                or "UNKNOWN"

            ),

            "supporting_evidence":

                supporting_evidence,

            "conflicting_evidence":

                conflicting_evidence,

            # Backward Compatibility

            "reason":

                supporting_evidence
                +
                conflicting_evidence

        }

    # =====================================================
    # ANALYSIS RESOLUTION
    # =====================================================

    @staticmethod
    def _resolve_analysis(analysis):

        """
        Accept:

        - Dictionary
        - MarketContext-like object
        """

        if isinstance(
            analysis,
            dict
        ):

            return analysis

        get_context = getattr(

            analysis,

            "get",

            None

        )

        if callable(
            get_context
        ):

            resolved = get_context()

            if isinstance(
                resolved,
                dict
            ):

                return resolved

        raise TypeError(

            "DecisionCore.decide() expects "
            "a dictionary or MarketContext-like object"

        )

    # =====================================================
    # SAFE SECTION
    # =====================================================

    @staticmethod
    def _section(
        analysis,
        key
    ):

        value = analysis.get(

            key,

            {}

        )

        if isinstance(
            value,
            dict
        ):

            return value

        return {}

    # =====================================================
    # SIGNAL NORMALIZATION
    # =====================================================

    @staticmethod
    def _normalize_signal(signal):

        if not signal:

            return "HOLD"

        signal = str(
            signal
        ).upper()

        if signal in (

            "BUY",

            "STRONG BUY",

            "BULLISH",

            "VERY BULLISH",

            "UP"

        ):

            return "BUY"

        if signal in (

            "SELL",

            "STRONG SELL",

            "BEARISH",

            "VERY BEARISH",

            "DOWN"

        ):

            return "SELL"

        return "HOLD"

    # =====================================================
    # CONFIDENCE COLLECTION
    # =====================================================

    @staticmethod
    def _collect_confidence(
        source,
        confidence_sources
    ):

        if not isinstance(
            source,
            dict
        ):

            return

        value = source.get(
            "confidence"
        )

        if value is None:

            return

        try:

            confidence = float(
                value
            )

            confidence = max(

                0,

                min(
                    confidence,
                    100
                )

            )

            confidence_sources.append(
                confidence
            )

        except (

            TypeError,

            ValueError

        ):

            pass

    # =====================================================
    # CONFIDENCE CALCULATION
    # =====================================================

    @staticmethod
    def _calculate_confidence(

        bullish_score,

        bearish_score,

        confidence_sources

    ):

        total_score = (

            bullish_score
            +
            bearish_score

        )

        if total_score == 0:

            evidence_confidence = 50

        else:

            dominant_score = max(

                bullish_score,

                bearish_score

            )

            evidence_confidence = min(

                50
                +
                dominant_score * 5,

                95

            )

        if confidence_sources:

            source_confidence = (

                sum(
                    confidence_sources
                )

                /
                len(
                    confidence_sources
                )

            )

            confidence = (

                evidence_confidence
                +
                source_confidence

            ) / 2

        else:

            confidence = evidence_confidence

        return round(

            max(

                0,

                min(
                    confidence,
                    100
                )

            ),

            2

        )
