"""
MarketVerse AI
Central Brain Controller
"""

from modules.ai_engine import analyze
from modules.market_scanner import scan_market
from modules.news import get_market_news
from modules.news_analysis import analyze_news
from modules.market_events import detect_market_events
from modules.decision_core import DecisionCore

from modules.pattern import detect_patterns
from modules.technical import technical_analysis
from modules.sentiment import sentiment_analysis
from modules.volume_analysis import volume_analysis

from modules.prediction import predict_price
from modules.strategy import generate_strategy
from modules.risk_manager import RiskManager

from modules.trade_executor import TradeExecutor
from modules.performance_tracker import PerformanceTracker


class CentralBrain:

    def __init__(self):

        self.risk = RiskManager()
        self.executor = TradeExecutor()
        self.tracker = PerformanceTracker()
        self.decision = DecisionCore()

    def think(self, symbol):

        result = {}


        # Market Scan
        result["scanner"] = scan_market(symbol)

        # AI Analysis
        result["ai"] = analyze(symbol)

        # News
        news = get_market_news(symbol)
        result["news"] = news

        # News Analysis
        result["news_analysis"] = analyze_news(news)

        # Market Events
        result["events"] = detect_market_events(symbol)

        # Technical
        result["technical"] = technical_analysis(symbol)

        # Pattern
        result["pattern"] = detect_patterns(symbol)

        # Volume
        result["volume"] = volume_analysis(symbol)

        # Sentiment
        result["sentiment"] = sentiment_analysis(symbol)

        # Prediction
        result["prediction"] = predict_price(symbol)

        # Strategy
        result["strategy"] = generate_strategy(result)
        # Risk
        result["risk"] = self.risk.evaluate(result)

        # Final Decision
        result["decision"] = self.decision.evaluate(result)

        # Confidence
        result["confidence"] = result["decision"].get("confidence", 0)

        return result
