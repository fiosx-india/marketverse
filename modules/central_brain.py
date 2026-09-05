"""
=========================================================
MarketVerse AI
Central Brain Controller
=========================================================

Purpose
-------
CentralBrain is the single orchestration layer for the
MarketVerse AI intelligence pipeline.

Responsibilities
----------------
- Create and maintain one shared MarketContext
- Control intelligence execution order
- Pass evidence between modules
- Isolate module failures
- Coordinate the unified intelligence pipeline

CentralBrain does NOT
--------------------
- Perform technical analysis
- Perform prediction logic
- Perform risk calculations
- Make the final market decision
- Perform Guardian responsibilities

Architecture
------------

Market Data
    ↓
Scanner
    ↓
News
    ↓
News Analysis
    ↓
Market Events
    ↓
Technical Analysis
    ↓
Pattern Analysis
    ↓
Volume Analysis
    ↓
Sentiment Analysis
    ↓
Prediction
    ↓
AI Intelligence
    ↓
Strategy
    ↓
Risk
    ↓
DecisionCore
    ↓
Final Market Context
=========================================================
"""

from modules.ai_engine import analyze

from modules.market_scanner import (
    scan_market,
    scan_mcx
)

from modules.news import get_market_news
from modules.news_analysis import analyze_news
from modules.market_events import detect_market_events

from modules.pattern import detect_patterns
from modules.technical import technical_analysis
from modules.sentiment import sentiment_analysis
from modules.volume_analysis import volume_analysis

from modules.prediction import predict_price
from modules.strategy import generate_strategy

from modules.risk_manager import RiskManager
from modules.decision_core import DecisionCore

from modules.market_context import MarketContext
from modules.market_data import get_market_data


class CentralBrain:
    """
    Primary MarketVerse AI orchestration layer.

    All intelligence workflows must pass through
    CentralBrain.
    """

    def __init__(self):

        self.risk = RiskManager()

        self.decision = DecisionCore()

    # =====================================================
    # SAFE MODULE EXECUTION
    # =====================================================

    def _safe_execute(
        self,
        context,
        key,
        function,
        *args,
        default=None,
        **kwargs
    ):
        """
        Execute one module safely.

        CentralBrain controls execution order.

        A module failure should not automatically
        stop the entire intelligence pipeline.
        """

        try:

            result = function(
                *args,
                **kwargs
            )

            context.update(
                key,
                result
            )

            return result

        except Exception as error:

            fallback = (
                default
                if default is not None
                else {}
            )

            context.update(
                key,
                fallback
            )

            # Record error only when the current
            # MarketContext implementation supports it.
            try:

                context.record_error(
                    module=key,
                    error=error
                )

            except Exception:

                pass

            return fallback

    # =====================================================
    # DATAFRAME VALIDATION
    # =====================================================

    def _is_valid_dataframe(
        self,
        dataframe
    ):
        """
        Check whether market data is available.
        """

        try:

            return (
                dataframe is not None
                and not dataframe.empty
            )

        except Exception:

            return False

    # =====================================================
    # TECHNICAL ANALYSIS
    # =====================================================

    def _run_technical_analysis(
        self,
        symbol,
        dataframe
    ):
        """
        Prefer shared DataFrame.

        Fall back to symbol mode only when needed.
        """

        if self._is_valid_dataframe(
            dataframe
        ):

            return technical_analysis(
                dataframe
            )

        return technical_analysis(
            symbol
        )

    # =====================================================
    # PATTERN ANALYSIS
    # =====================================================

    def _run_pattern_analysis(
        self,
        symbol,
        dataframe
    ):
        """
        Prefer shared market data.

        Avoid unnecessary market data fetching.
        """

        if self._is_valid_dataframe(
            dataframe
        ):

            return detect_patterns(
                dataframe
            )

        return detect_patterns(
            symbol
        )

    # =====================================================
    # VOLUME ANALYSIS
    # =====================================================

    def _run_volume_analysis(
        self,
        symbol,
        dataframe
    ):
        """
        Prefer shared market DataFrame.
        """

        if self._is_valid_dataframe(
            dataframe
        ):

            return volume_analysis(
                dataframe
            )

        return volume_analysis(
            symbol
        )

    # =====================================================
    # NEWS HEADLINE EXTRACTION
    # =====================================================

    def _extract_headlines(
        self,
        news
    ):
        """
        Safely extract headlines from news results.
        """

        if not isinstance(
            news,
            dict
        ):

            return []

        articles = news.get(
            "articles",
            []
        )

        if not isinstance(
            articles,
            list
        ):

            return []

        headlines = []

        for article in articles:

            if not isinstance(
                article,
                dict
            ):

                continue

            title = article.get(
                "title"
            )

            if title:

                headlines.append(
                    title
                )

        return headlines

    # =====================================================
    # MARKET EVENTS INPUT
    # =====================================================

    def _run_market_events(
        self,
        news,
        headlines
    ):
        """
        Market events should operate on news evidence.

        Supports modules that expect either:
        - Articles
        - Headlines
        """

        if isinstance(
            news,
            dict
        ):

            articles = news.get(
                "articles",
                []
            )

            if articles:

                return detect_market_events(
                    articles
                )

        return detect_market_events(
            headlines
        )

    # =====================================================
    # SENTIMENT ANALYSIS
    # =====================================================

    def _run_sentiment_analysis(
        self,
        headlines
    ):
        """
        Sentiment should be derived from available
        market/news evidence.

        It should not receive a symbol unless the
        module explicitly supports symbol mode.
        """

        return sentiment_analysis(
            headlines
        )

    # =====================================================
    # RISK ANALYSIS
    # =====================================================

    def _run_risk_analysis(
        self,
        context
    ):
        """
        Execute RiskManager using the shared context.

        Supports both:
        - New evaluate(context)
        - Legacy calculate(...)
        """

        analysis = context.get()

        if hasattr(
            self.risk,
            "evaluate"
        ):

            return self.risk.evaluate(
                analysis
            )

        # ---------------------------------------------
        # LEGACY COMPATIBILITY
        # ---------------------------------------------

        strategy = analysis.get(
            "strategy",
            {}
        ) or {}

        prediction = analysis.get(
            "prediction",
            {}
        ) or {}

        technical = analysis.get(
            "technical",
            {}
        ) or {}

        signal = strategy.get(
            "action",
            prediction.get(
                "signal",
                "HOLD"
            )
        )

        confidence = prediction.get(
            "confidence",
            strategy.get(
                "confidence",
                50
            )
        )

        entry_price = technical.get(
            "price",
            prediction.get(
                "price",
                0
            )
        )

        if not entry_price:

            return {
                "status": "unavailable",
                "trade_allowed": False,
                "risk_level": "UNKNOWN",
                "message": "Entry price unavailable"
            }

        if hasattr(
            self.risk,
            "calculate"
        ):

            return self.risk.calculate(
                entry_price=entry_price,
                signal=signal,
                confidence=confidence
            )

        return {
            "status": "unavailable",
            "trade_allowed": False,
            "risk_level": "UNKNOWN"
        }

    # =====================================================
    # PIPELINE STATUS
    # =====================================================

    def _set_pipeline_status(
        self,
        context,
        status
    ):
        """
        Backward-compatible pipeline status update.
        """

        try:

            context.set_pipeline_status(
                status
            )

        except Exception:

            metadata = context.read(
                "metadata",
                {}
            ) or {}

            metadata[
                "pipeline_status"
            ] = status

            context.update(
                "metadata",
                metadata
            )

    # =====================================================
    # MAIN INTELLIGENCE PIPELINE
    # =====================================================

    def think(
        self,
        symbol
    ):
        """
        Execute the complete MarketVerse AI
        intelligence pipeline.

        Returns:
            Complete shared MarketContext dictionary.
        """

        # =================================================
        # CREATE SHARED MARKET CONTEXT
        # =================================================

        context = MarketContext(
            symbol
        )

        self._set_pipeline_status(
            context,
            "running"
        )

        # =================================================
        # 1. MARKET DATA
        # =================================================

        dataframe = self._safe_execute(

            context,

            "market_data",

            get_market_data,

            symbol,

            default=None

        )

        # =================================================
        # 2. MARKET SCANNER
        # =================================================

        self._safe_execute(

            context,

            "scanner",

            lambda: {

                "stocks": scan_market(

                    [

                        {

                            "symbol": symbol

                        }

                    ]

                ),

                "mcx": scan_mcx()

            },

            default={}

        )

        # =================================================
        # 3. NEWS
        # =================================================

        news = self._safe_execute(

            context,

            "news",

            get_market_news,

            symbol,

            default={}

        )

        # =================================================
        # 4. NEWS ANALYSIS
        # =================================================

        headlines = self._extract_headlines(
            news
        )

        self._safe_execute(

            context,

            "news_analysis",

            analyze_news,

            symbol,

            headlines,

            default={}

        )

        # =================================================
        # 5. MARKET EVENTS
        # =================================================

        self._safe_execute(

            context,

            "events",

            self._run_market_events,

            news,

            headlines,

            default={}

        )

        # =================================================
        # 6. TECHNICAL ANALYSIS
        # =================================================

        self._safe_execute(

            context,

            "technical",

            self._run_technical_analysis,

            symbol,

            dataframe,

            default={}

        )

        # =================================================
        # 7. PATTERN ANALYSIS
        # =================================================

        self._safe_execute(

            context,

            "pattern",

            self._run_pattern_analysis,

            symbol,

            dataframe,

            default={}

        )

        # =================================================
        # 8. VOLUME ANALYSIS
        # =================================================

        self._safe_execute(

            context,

            "volume",

            self._run_volume_analysis,

            symbol,

            dataframe,

            default={}

        )

        # =================================================
        # 9. SENTIMENT ANALYSIS
        # =================================================

        self._safe_execute(

            context,

            "sentiment",

            self._run_sentiment_analysis,

            headlines,

            default={}

        )

        # =================================================
        # 10. PREDICTION
        # =================================================
        #
        # Prediction receives existing intelligence
        # evidence from MarketContext.
        # =================================================

        self._safe_execute(

            context,

            "prediction",

            predict_price,

            context.get(),

            default={}

        )

        # =================================================
        # 11. AI INTELLIGENCE
        # =================================================
        #
        # AI Engine receives unified evidence.
        #
        # It does not orchestrate the pipeline.
        # =================================================

        self._safe_execute(

            context,

            "ai",

            analyze,

            symbol,

            context.get(),

            default={}

        )

        # =================================================
        # 12. STRATEGY
        # =================================================

        self._safe_execute(

            context,

            "strategy",

            generate_strategy,

            context.get(),

            default={}

        )

        # =================================================
        # 13. RISK
        # =================================================

        self._safe_execute(

            context,

            "risk",

            self._run_risk_analysis,

            context,

            default={}

        )

        # =================================================
        # 14. FINAL DECISION
        # =================================================

        self._safe_execute(

            context,

            "decision",

            self.decision.decide,

            context,

            default={}

        )

        # =================================================
        # PIPELINE COMPLETE
        # =================================================

        self._set_pipeline_status(
            context,
            "completed"
        )

        # =================================================
        # METADATA
        # =================================================

        metadata = context.read(
            "metadata",
            {}
        ) or {}

        metadata.update(

            {

                "pipeline":

                    "CentralBrain",

                "symbol":

                    symbol,

                "module_count":

                    14

            }

        )

        try:

            metadata[
                "error_count"
            ] = len(
                context.get_errors()
            )

        except Exception:

            metadata[
                "error_count"
            ] = 0

        context.update(

            "metadata",

            metadata

        )

        # =================================================
        # RETURN UNIFIED MARKET CONTEXT
        # =================================================

        return context.get()
