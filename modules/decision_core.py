"""
=========================================================
MarketVerse AI
Decision Core
=========================================================

Purpose
-------
Combines independent intelligence evidence from the
Shared MarketContext and produces one final explainable
market decision.

DecisionCore is the final decision fusion layer.

Architecture Rules
------------------
- CentralBrain remains the only orchestrator.
- DecisionCore does not fetch or analyze market data.
- DecisionCore does not generate predictions.
- DecisionCore does not generate strategies.
- RiskManager does not determine market direction.
- Market direction and trade eligibility remain separate.
- Raw evidence is weighted independently.
- Derived intelligence is used carefully to reduce
  double-counting.

Pipeline
--------
Analysis Modules
        │
        ▼
Shared MarketContext
        │
        ├── Raw Evidence
        │     ├── Technical
        │     ├── Pattern
        │     ├── Volume
        │     ├── Sentiment
        │     └── News
        │
        ├── Derived Intelligence
        │     ├── Prediction
        │     ├── AI
        │     └── Strategy
        │
        ▼
RiskManager
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

    Responsibilities
    ----------------
    - Fuse independent market evidence
    - Evaluate bullish and bearish evidence
    - Detect evidence conflicts
    - Calculate explainable confidence
    - Calculate directional probability
    - Respect RiskManager trade restrictions
    - Produce one final explainable decision

    Supports
    --------
    1. Dictionary
    2. MarketContext-like object with get()
    """

    # =====================================================
    # MAIN DECISION
    # =====================================================

    def decide(self, analysis):

        analysis = self._resolve_analysis(analysis)

        # =================================================
        # READ CONTEXT
        # =================================================

        technical = self._section(analysis, "technical")
        prediction = self._section(analysis, "prediction")
        ai = self._section(analysis, "ai")
        news = self._section(analysis, "news_analysis")
        pattern = self._section(analysis, "pattern")
        volume = self._section(analysis, "volume")
        sentiment = self._section(analysis, "sentiment")
        strategy = self._section(analysis, "strategy")
        risk = self._section(analysis, "risk")

        # =================================================
        # SCORE INITIALIZATION
        # =================================================

        bullish_score = 0.0
        bearish_score = 0.0

        supporting_evidence = []
        conflicting_evidence = []
        neutral_evidence = []

        confidence_sources = []

        assumptions = []

        evidence_sources = 0
        directional_sources = 0

        # =================================================
        # RAW EVIDENCE
        #
        # Raw evidence receives the primary weight.
        # =================================================

        # =================================================
        # TECHNICAL
        # =================================================

        technical_signal = self._normalize_signal(
            technical.get("signal")
        )

        if technical_signal == "BUY":

            bullish_score += 2.0
            evidence_sources += 1
            directional_sources += 1

            supporting_evidence.append(
                "Technical analysis supports bullish conditions"
            )

        elif technical_signal == "SELL":

            bearish_score += 2.0
            evidence_sources += 1
            directional_sources += 1

            conflicting_evidence.append(
                "Technical analysis supports bearish conditions"
            )

        elif technical:

            evidence_sources += 1

            neutral_evidence.append(
                "Technical analysis provides no strong directional signal"
            )

        self._collect_confidence(
            technical,
            confidence_sources
        )

        # =================================================
        # PATTERN
        # =================================================

        pattern_bullish = bool(
            pattern.get("bullish")
        )

        pattern_bearish = bool(
            pattern.get("bearish")
        )

        if pattern_bullish:

            bullish_score += 1.0
            evidence_sources += 1
            directional_sources += 1

            supporting_evidence.append(
                "Bullish chart pattern detected"
            )

        if pattern_bearish:

            bearish_score += 1.0

            if not pattern_bullish:
                evidence_sources += 1

            directional_sources += 1

            conflicting_evidence.append(
                "Bearish chart pattern detected"
            )

        if (
            pattern
            and not pattern_bullish
            and not pattern_bearish
        ):

            evidence_sources += 1

            neutral_evidence.append(
                "No strong directional chart pattern detected"
            )

        self._collect_confidence(
            pattern,
            confidence_sources
        )

        # =================================================
        # VOLUME
        # =================================================

        volume_signal = self._normalize_signal(
            volume.get("signal")
        )

        if volume_signal == "BUY":

            bullish_score += 1.0
            evidence_sources += 1
            directional_sources += 1

            supporting_evidence.append(
                "Volume supports bullish movement"
            )

        elif volume_signal == "SELL":

            bearish_score += 1.0
            evidence_sources += 1
            directional_sources += 1

            conflicting_evidence.append(
                "Volume supports bearish movement"
            )

        elif volume:

            evidence_sources += 1

            neutral_evidence.append(
                "Volume provides no strong directional confirmation"
            )

        self._collect_confidence(
            volume,
            confidence_sources
        )

        # =================================================
        # SENTIMENT
        # =================================================

        sentiment_signal = self._normalize_signal(

            sentiment.get(
                "signal",
                sentiment.get("sentiment")
            )

        )

        if sentiment_signal == "BUY":

            bullish_score += 1.0
            evidence_sources += 1
            directional_sources += 1

            supporting_evidence.append(
                "Market sentiment supports bullish conditions"
            )

        elif sentiment_signal == "SELL":

            bearish_score += 1.0
            evidence_sources += 1
            directional_sources += 1

            conflicting_evidence.append(
                "Market sentiment supports bearish conditions"
            )

        elif sentiment:

            evidence_sources += 1

            neutral_evidence.append(
                "Market sentiment provides no strong directional confirmation"
            )

        self._collect_confidence(
            sentiment,
            confidence_sources
        )

        # =================================================
        # NEWS
        # =================================================

        news_signal = self._normalize_signal(
            news.get("sentiment")
        )

        if news_signal == "BUY":

            bullish_score += 1.0
            evidence_sources += 1
            directional_sources += 1

            supporting_evidence.append(
                "News sentiment is positive"
            )

        elif news_signal == "SELL":

            bearish_score += 1.0
            evidence_sources += 1
            directional_sources += 1

            conflicting_evidence.append(
                "News sentiment is negative"
            )

        elif news:

            evidence_sources += 1

            neutral_evidence.append(
                "News analysis provides no strong directional confirmation"
            )

        self._collect_confidence(
            news,
            confidence_sources
        )

        # =================================================
        # DERIVED INTELLIGENCE
        #
        # Prediction, AI and Strategy may already use
        # raw evidence. Therefore they receive smaller
        # confirmation weights.
        # =================================================

        # =================================================
        # PREDICTION
        # =================================================

        prediction_signal = self._normalize_signal(
            prediction.get("signal")
        )

        if prediction_signal == "BUY":

            bullish_score += 1.0
            evidence_sources += 1
            directional_sources += 1

            supporting_evidence.append(
                "Prediction confirms upward probability"
            )

        elif prediction_signal == "SELL":

            bearish_score += 1.0
            evidence_sources += 1
            directional_sources += 1

            conflicting_evidence.append(
                "Prediction confirms downward probability"
            )

        elif prediction:

            evidence_sources += 1

            neutral_evidence.append(
                "Prediction provides no strong directional confirmation"
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
                ai.get("prediction")
            )

        )

        if ai_signal == "BUY":

            bullish_score += 1.5
            evidence_sources += 1
            directional_sources += 1

            supporting_evidence.append(
                "AI intelligence supports bullish movement"
            )

        elif ai_signal == "SELL":

            bearish_score += 1.5
            evidence_sources += 1
            directional_sources += 1

            conflicting_evidence.append(
                "AI intelligence supports bearish movement"
            )

        elif ai:

            evidence_sources += 1

            neutral_evidence.append(
                "AI intelligence provides no strong directional confirmation"
            )

        self._collect_confidence(
            ai,
            confidence_sources
        )

        # =================================================
        # STRATEGY CONFIRMATION
        #
        # Strategy is the most derived layer before risk.
        # It receives only a light confirmation weight.
        # =================================================

        strategy_signal = self._normalize_signal(

            strategy.get(
                "action",
                strategy.get("decision")
            )

        )

        if strategy_signal == "BUY":

            bullish_score += 0.5
            evidence_sources += 1
            directional_sources += 1

            supporting_evidence.append(
                "Strategy aligns with a bullish position"
            )

        elif strategy_signal == "SELL":

            bearish_score += 0.5
            evidence_sources += 1
            directional_sources += 1

            conflicting_evidence.append(
                "Strategy aligns with a bearish position"
            )

        elif strategy:

            evidence_sources += 1

            neutral_evidence.append(
                "Strategy does not provide directional confirmation"
            )

        self._collect_confidence(
            strategy,
            confidence_sources
        )

        # =================================================
        # SCORE ANALYSIS
        # =================================================

        total_score = (
            bullish_score
            +
            bearish_score
        )

        difference = (
            bullish_score
            -
            bearish_score
        )

        # =================================================
        # CONFLICT DETECTION
        # =================================================

        evidence_conflict = (

            bullish_score > 0
            and bearish_score > 0

        )

        if evidence_conflict:

            conflicting_evidence.append(
                "Bullish and bearish evidence are both present"
            )

        # =================================================
        # MARKET DECISION
        #
        # Direction is determined independently from risk.
        # =================================================

        if total_score <= 0:

            market_decision = "HOLD"

        elif (
            bullish_score >= 4.5
            and difference >= 3
        ):

            market_decision = "STRONG BUY"

        elif difference >= 1.5:

            market_decision = "BUY"

        elif (
            bearish_score >= 4.5
            and difference <= -3
        ):

            market_decision = "STRONG SELL"

        elif difference <= -1.5:

            market_decision = "SELL"

        else:

            market_decision = "HOLD"

        # =================================================
        # RISK VALIDATION
        # =================================================

        trade_allowed_value = risk.get(
            "trade_allowed"
        )

        risk_level = str(

            risk.get(
                "risk_level",
                "UNKNOWN"
            )

        ).upper()

        risk_restricted = False

        risk_status = str(
            risk.get(
                "status",
                ""
            )
        ).lower()

        # Explicit risk rejection only

        if trade_allowed_value is False:

            risk_restricted = True

            conflicting_evidence.append(
                "Risk management does not allow an active trade"
            )

        # Risk calculation failure

        if risk_status == "error":

            risk_restricted = True

            conflicting_evidence.append(
                "Risk assessment could not validate trade eligibility"
            )

        # HIGH risk is a warning, not automatically
        # a market-direction override.

        if risk_level == "HIGH":

            conflicting_evidence.append(
                "High risk conditions detected"
            )

        # =================================================
        # FINAL ACTION
        #
        # Market direction and trading action are separate.
        # =================================================

        if risk_restricted:

            final_action = "HOLD"

        else:

            final_action = market_decision

        # =================================================
        # CONFIDENCE
        # =================================================

        confidence = self._calculate_confidence(

            bullish_score=bullish_score,

            bearish_score=bearish_score,

            evidence_sources=evidence_sources,

            directional_sources=directional_sources,

            confidence_sources=confidence_sources,

            evidence_conflict=evidence_conflict

        )

        # =================================================
        # DIRECTIONAL PROBABILITY
        # =================================================

        probability = self._calculate_probability(

            bullish_score,

            bearish_score,

            market_decision

        )

        # =================================================
        # ASSUMPTIONS
        # =================================================

        if not confidence_sources:

            assumptions.append(
                "Source confidence values were unavailable; confidence relies on evidence balance and coverage"
            )

        if evidence_sources == 0:

            assumptions.append(
                "No usable intelligence evidence was available"
            )

        elif directional_sources == 0:

            assumptions.append(
                "Available evidence does not provide a strong directional signal"
            )

        if evidence_conflict:

            assumptions.append(
                "Confidence is reduced because evidence sources disagree"
            )

        if risk_restricted:

            assumptions.append(
                "Market direction may differ from the final trading action because risk restrictions are active"
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

        if not neutral_evidence:

            neutral_evidence.append(
                "No major neutral evidence recorded"
            )

        # =================================================
        # DATA FRESHNESS
        # =================================================

        metadata = analysis.get(
            "metadata",
            {}
        )

        if not isinstance(
            metadata,
            dict
        ):

            metadata = {}

        data_freshness = {

            "timestamp": metadata.get("timestamp"),

            "market_data_timestamp": metadata.get(
                "market_data_timestamp"
            ),

            "data_age_seconds": metadata.get(
                "data_age_seconds"
            ),

            "source": metadata.get(
                "source"
            )

        }

        # =================================================
        # FINAL RESULT
        # =================================================

        return {

            "status": "success",

            # =============================================
            # MARKET INTELLIGENCE
            # =============================================

            "decision": market_decision,

            "signal": market_decision,

            "market_direction": market_decision,

            # =============================================
            # TRADING ACTION
            # =============================================

            "final_action": final_action,

            "trade_action": final_action,

            # =============================================
            # SCORES
            # =============================================

            "bullish_score": round(
                bullish_score,
                2
            ),

            "bearish_score": round(
                bearish_score,
                2
            ),

            "score": round(
                difference,
                2
            ),

            "total_evidence_score": round(
                total_score,
                2
            ),

            "evidence_sources": evidence_sources,

            "directional_sources": directional_sources,

            # =============================================
            # CONFIDENCE
            # =============================================

            "confidence": confidence,

            # =============================================
            # PROBABILITY
            # =============================================

            "probability": probability,

            # =============================================
            # CONFLICT
            # =============================================

            "evidence_conflict": evidence_conflict,

            # =============================================
            # RISK
            # =============================================

            "risk_restricted": risk_restricted,

            "risk_level": risk_level,

            "trade_allowed": (

                not risk_restricted

            ),

            # =============================================
            # EXPLAINABILITY
            # =============================================

            "supporting_evidence":

                supporting_evidence,

            "conflicting_evidence":

                conflicting_evidence,

            "neutral_evidence":

                neutral_evidence,

            "assumptions":

                assumptions,

            # =============================================
            # DATA FRESHNESS
            # =============================================

            "data_freshness":

                data_freshness,

            # =============================================
            # BACKWARD COMPATIBILITY
            # =============================================

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

        if signal is None:

            return "HOLD"

        signal = str(
            signal
        ).upper().strip()

        if signal in (

            "BUY",
            "STRONG BUY",
            "LONG",
            "BULLISH",
            "VERY BULLISH",
            "UP",
            "POSITIVE"

        ):

            return "BUY"

        if signal in (

            "SELL",
            "STRONG SELL",
            "SHORT",
            "BEARISH",
            "VERY BEARISH",
            "DOWN",
            "NEGATIVE"

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

        evidence_sources,

        directional_sources,

        confidence_sources,

        evidence_conflict=False

    ):

        total_score = (
            bullish_score
            +
            bearish_score
        )

        # ---------------------------------------------
        # Direction agreement
        # ---------------------------------------------

        if total_score <= 0:

            agreement_score = 50

        else:

            dominant_score = max(
                bullish_score,
                bearish_score
            )

            agreement_ratio = (
                dominant_score
                /
                total_score
            )

            agreement_score = (
                40
                +
                (
                    agreement_ratio
                    *
                    50
                )
            )

        # ---------------------------------------------
        # Evidence coverage
        # ---------------------------------------------

        coverage_ratio = min(
            directional_sources / 6,
            1
        )

        coverage_score = (
            coverage_ratio
            *
            15
        )

        # ---------------------------------------------
        # Base confidence
        # ---------------------------------------------

        evidence_confidence = (
            agreement_score
            +
            coverage_score
        )

        # ---------------------------------------------
        # Conflict penalty
        # ---------------------------------------------

        if evidence_conflict:

            evidence_confidence -= 12

        evidence_confidence = max(
            0,
            min(
                evidence_confidence,
                95
            )
        )

        # ---------------------------------------------
        # Source confidence
        # ---------------------------------------------

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
                *
                0.60

            ) + (

                source_confidence
                *
                0.40

            )

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

    # =====================================================
    # DIRECTIONAL PROBABILITY
    # =====================================================

    @staticmethod
    def _calculate_probability(

        bullish_score,

        bearish_score,

        decision

    ):

        total = (

            bullish_score
            +
            bearish_score

        )

        if total <= 0:

            return {

                "up": 0.50,

                "down": 0.50,

                "direction": "NEUTRAL"

            }

        up_probability = (

            bullish_score
            /
            total

        )

        down_probability = (

            bearish_score
            /
            total

        )

        return {

            "up": round(
                up_probability,
                2
            ),

            "down": round(
                down_probability,
                2
            ),

            "direction": decision

                }
