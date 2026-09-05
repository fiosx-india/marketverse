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
- Coordinate intelligence modules
- Maintain one shared MarketContext
- Control execution order
- Pass intelligence evidence between modules
- Build the unified intelligence pipeline

CentralBrain does NOT:
- Perform technical analysis itself
- Perform prediction logic itself
- Perform risk calculations itself
- Replace DecisionCore
- Perform Guardian responsibilities

Architecture
------------

Market Data
    ↓
Scanner
    ↓
News / Events
    ↓
Technical
    ↓
Pattern / Volume / Sentiment
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

from modules.trade_executor import TradeExecutor
from modules.performance_tracker import PerformanceTracker

from modules.market_context import MarketContext
from modules.market_data import get_market_data

from modules.ai_market_intelligence import (
    AIMarketIntelligence
)


class CentralBrain:
    """
    Primary MarketVerse AI orchestration layer.

    Every intelligence workflow should pass through
    CentralBrain.
    """

    def __init__(self):

        self.risk = RiskManager()

        self.executor = TradeExecutor()

        self.tracker = PerformanceTracker()

        self.decision = DecisionCore()

        self.ai_market = AIMarketIntelligence()

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
        Execute one intelligence module safely.

        CentralBrain controls execution.

        MarketContext stores:
        - Result
        - Module status
        - Error information

        Guardian remains responsible for:
        - Diagnostics
        - Monitoring
        - Validation
        - Recovery
        - Self-healing
        """

        try:

            result = function(
                *args,
                **kwargs
            )

            context.update(
                key,
                result,
                source=key,
                status="success"
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
                fallback,
                source=key,
                status="failed"
            )

            context.record_error(
                module=key,
                error=error
            )

            return fallback

    # =====================================================
    # TECHNICAL ANALYSIS RESOLUTION
    # =====================================================

    def _run_technical_analysis(
        self,
        symbol,
        dataframe
    ):
        """
        Supports both:

        - DataFrame-based technical analysis
        - Legacy symbol-based technical analysis
        """

        try:

            if dataframe is not None:

                return technical_analysis(
                    dataframe
                )

        except Exception:

            pass

        return technical_analysis(
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
        Safely extract news headlines.
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

        context.set_pipeline_status(
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
        # 3. MARKET INTELLIGENCE
        # =================================================

        self._safe_execute(

            context,

            "ai_market_intelligence",

            self.ai_market.run,

            symbol,

            dataframe,

            default={}

        )

        # =================================================
        # 4. NEWS
        # =================================================

        news = self._safe_execute(

            context,

            "news",

            get_market_news,

            symbol,

            default={}

        )

        # =================================================
        # 5. NEWS ANALYSIS
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
        # 6. MARKET EVENTS
        # =================================================

        self._safe_execute(

            context,

            "events",

            detect_market_events,

            symbol,

            default={}

        )

        # =================================================
        # 7. TECHNICAL ANALYSIS
        # =================================================

        technical = self._safe_execute(

            context,

            "technical",

            self._run_technical_analysis,

            symbol,

            dataframe,

            default={}

        )

        # =================================================
        # 8. PATTERN ANALYSIS
        # =================================================

        self._safe_execute(

            context,

            "pattern",

            detect_patterns,

            symbol,

            default={}

        )

        # =================================================
        # 9. VOLUME ANALYSIS
        # =================================================

        self._safe_execute(

            context,

            "volume",

            volume_analysis,

            symbol,

            default={}

        )

        # =================================================
        # 10. SENTIMENT ANALYSIS
        # =================================================

        self._safe_execute(

            context,

            "sentiment",

            sentiment_analysis,

            symbol,

            default={}

        )

        # =================================================
        # 11. PREDICTION
        # =================================================
        #
        # IMPORTANT:
        #
        # Prediction receives existing intelligence
        # evidence from MarketContext.
        #
        # It does NOT fetch market data again.
        # =================================================

        self._safe_execute(

            context,

            "prediction",

            predict_price,

            context.get(),

            default={}

        )

        # =================================================
        # 12. AI INTELLIGENCE
        # =================================================
        #
        # AI Engine receives unified evidence.
        #
        # CentralBrain remains the only orchestrator.
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
        # 13. STRATEGY
        # =================================================

        self._safe_execute(

            context,

            "strategy",

            generate_strategy,

            context.get(),

            default={}

        )

        # =================================================
        # 14. RISK
        # =================================================

        self._safe_execute(

            context,

            "risk",

            self.risk.evaluate,

            context.get(),

            default={}

        )

        # =================================================
        # 15. FINAL DECISION
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

        context.set_pipeline_status(
            "completed"
        )

        metadata = context.read(
            "metadata",
            {}
        ) or {}

        metadata["pipeline"] = (
            "CentralBrain"
        )

        metadata["symbol"] = symbol

        metadata["module_count"] = 15

        metadata["error_count"] = len(

            context.get_errors()

        )

        context.update(

            "metadata",

            metadata,

            source="CentralBrain",

            status="completed"

        )

        # =================================================
        # RETURN UNIFIED MARKET CONTEXT
        # =================================================

        return context.get()
