"""
=========================================================
MarketVerse AI
CentralBrain Tests
=========================================================

Tests:
- CentralBrain initialization
- Shared MarketContext orchestration
- Safe module execution
- Module failure isolation
- DataFrame routing
- Headline extraction
- Pipeline status handling
- RiskManager integration
- Full pipeline orchestration using mocks

CentralBrain remains the single orchestration layer.
Guardian responsibilities are not tested here.
=========================================================
"""

import unittest
from unittest.mock import Mock, patch

from modules.central_brain import CentralBrain
from modules.market_context import MarketContext


class FakeDataFrame:
    """
    Minimal DataFrame-compatible object.

    Used to test CentralBrain routing without requiring
    pandas in every unit test.
    """

    def __init__(self, empty=False):
        self.empty = empty


class TestCentralBrainInitialization(unittest.TestCase):

    def setUp(self):
        self.brain = CentralBrain()

    def test_central_brain_initializes(self):

        self.assertIsNotNone(
            self.brain
        )

    def test_risk_manager_exists(self):

        self.assertTrue(
            hasattr(
                self.brain,
                "risk"
            )
        )

    def test_decision_core_exists(self):

        self.assertTrue(
            hasattr(
                self.brain,
                "decision"
            )
        )


class TestSafeExecution(unittest.TestCase):

    def setUp(self):
        self.brain = CentralBrain()

    def test_safe_execute_success(self):

        context = MarketContext(
            "TEST"
        )

        result = self.brain._safe_execute(

            context,

            "technical",

            lambda: {
                "signal": "BUY"
            },

            default={}

        )

        self.assertEqual(

            result,

            {
                "signal": "BUY"
            }

        )

        self.assertEqual(

            context.read(
                "technical"
            ),

            {
                "signal": "BUY"
            }

        )

    def test_safe_execute_failure_uses_default(self):

        context = MarketContext(
            "TEST"
        )

        def failing_function():
            raise RuntimeError(
                "Test module failure"
            )

        result = self.brain._safe_execute(

            context,

            "technical",

            failing_function,

            default={}

        )

        self.assertEqual(
            result,
            {}
        )

        self.assertEqual(

            context.read(
                "technical"
            ),

            {}

        )

    def test_safe_execute_records_error(self):

        context = MarketContext(
            "TEST"
        )

        def failing_function():
            raise ValueError(
                "Failure"
            )

        self.brain._safe_execute(

            context,

            "prediction",

            failing_function,

            default={}

        )

        errors = context.get_errors()

        self.assertGreaterEqual(

            len(errors),

            1

        )


class TestDataFrameValidation(unittest.TestCase):

    def setUp(self):
        self.brain = CentralBrain()

    def test_valid_dataframe(self):

        dataframe = FakeDataFrame(
            empty=False
        )

        result = self.brain._is_valid_dataframe(
            dataframe
        )

        self.assertTrue(
            result
        )

    def test_empty_dataframe(self):

        dataframe = FakeDataFrame(
            empty=True
        )

        result = self.brain._is_valid_dataframe(
            dataframe
        )

        self.assertFalse(
            result
        )

    def test_none_dataframe(self):

        result = self.brain._is_valid_dataframe(
            None
        )

        self.assertFalse(
            result
        )


class TestAnalysisRouting(unittest.TestCase):

    def setUp(self):
        self.brain = CentralBrain()

    @patch(
        "modules.central_brain.technical_analysis"
    )
    def test_technical_uses_dataframe_when_available(

        self,

        mock_technical

    ):

        dataframe = FakeDataFrame(
            empty=False
        )

        mock_technical.return_value = {

            "signal": "BUY"

        }

        result = self.brain._run_technical_analysis(

            "RELIANCE",

            dataframe

        )

        mock_technical.assert_called_once_with(
            dataframe
        )

        self.assertEqual(

            result["signal"],

            "BUY"

        )

    @patch(
        "modules.central_brain.technical_analysis"
    )
    def test_technical_uses_symbol_when_dataframe_missing(

        self,

        mock_technical

    ):

        mock_technical.return_value = {}

        self.brain._run_technical_analysis(

            "RELIANCE",

            None

        )

        mock_technical.assert_called_once_with(
            "RELIANCE"
        )

    @patch(
        "modules.central_brain.detect_patterns"
    )
    def test_pattern_uses_dataframe(

        self,

        mock_pattern

    ):

        dataframe = FakeDataFrame(
            empty=False
        )

        mock_pattern.return_value = {}

        self.brain._run_pattern_analysis(

            "RELIANCE",

            dataframe

        )

        mock_pattern.assert_called_once_with(
            dataframe
        )

    @patch(
        "modules.central_brain.volume_analysis"
    )
    def test_volume_uses_dataframe(

        self,

        mock_volume

    ):

        dataframe = FakeDataFrame(
            empty=False
        )

        mock_volume.return_value = {}

        self.brain._run_volume_analysis(

            "RELIANCE",

            dataframe

        )

        mock_volume.assert_called_once_with(
            dataframe
        )


class TestHeadlineExtraction(unittest.TestCase):

    def setUp(self):
        self.brain = CentralBrain()

    def test_extract_headlines(self):

        news = {

            "articles": [

                {
                    "title": "Market rises"
                },

                {
                    "title": "Bank stocks gain"
                }

            ]

        }

        headlines = self.brain._extract_headlines(
            news
        )

        self.assertEqual(

            headlines,

            [

                "Market rises",

                "Bank stocks gain"

            ]

        )

    def test_extract_headlines_ignores_invalid_articles(self):

        news = {

            "articles": [

                {
                    "title": "Valid headline"
                },

                "invalid",

                {},

                {
                    "description": "No title"
                }

            ]

        }

        headlines = self.brain._extract_headlines(
            news
        )

        self.assertEqual(

            headlines,

            [

                "Valid headline"

            ]

        )

    def test_extract_headlines_invalid_news(self):

        headlines = self.brain._extract_headlines(
            None
        )

        self.assertEqual(
            headlines,
            []
        )


class TestMarketEventsRouting(unittest.TestCase):

    def setUp(self):
        self.brain = CentralBrain()

    @patch(
        "modules.central_brain.detect_market_events"
    )
    def test_market_events_prefers_articles(

        self,

        mock_events

    ):

        articles = [

            {
                "title": "News"
            }

        ]

        news = {

            "articles": articles

        }

        self.brain._run_market_events(

            news,

            ["News"]

        )

        mock_events.assert_called_once_with(
            articles
        )

    @patch(
        "modules.central_brain.detect_market_events"
    )
    def test_market_events_falls_back_to_headlines(

        self,

        mock_events

    ):

        self.brain._run_market_events(

            {},

            [

                "Headline"

            ]

        )

        mock_events.assert_called_once_with(

            [

                "Headline"

            ]

        )


class TestRiskIntegration(unittest.TestCase):

    def setUp(self):
        self.brain = CentralBrain()

    def test_risk_evaluate_is_used_when_available(self):

        context = MarketContext(
            "TEST"
        )

        expected_result = {

            "status": "success",

            "risk_level": "LOW"

        }

        self.brain.risk.evaluate = Mock(

            return_value=expected_result

        )

        result = self.brain._run_risk_analysis(
            context
        )

        self.brain.risk.evaluate.assert_called_once()

        self.assertEqual(

            result,

            expected_result

        )


class TestPipelineStatus(unittest.TestCase):

    def setUp(self):
        self.brain = CentralBrain()

    def test_set_pipeline_status(self):

        context = MarketContext(
            "TEST"
        )

        self.brain._set_pipeline_status(

            context,

            "running"

        )

        self.assertEqual(

            context.get_pipeline_status(),

            "running"

        )


class TestCentralBrainPipeline(unittest.TestCase):

    """
    Full CentralBrain pipeline test.

    All external intelligence modules are mocked.

    This verifies orchestration order and shared context
    integration without fetching real market data.
    """

    def setUp(self):
        self.brain = CentralBrain()

    @patch(
        "modules.central_brain.get_market_data"
    )
    @patch(
        "modules.central_brain.scan_market"
    )
    @patch(
        "modules.central_brain.scan_mcx"
    )
    @patch(
        "modules.central_brain.get_market_news"
    )
    @patch(
        "modules.central_brain.analyze_news"
    )
    @patch(
        "modules.central_brain.detect_market_events"
    )
    @patch(
        "modules.central_brain.technical_analysis"
    )
    @patch(
        "modules.central_brain.detect_patterns"
    )
    @patch(
        "modules.central_brain.volume_analysis"
    )
    @patch(
        "modules.central_brain.sentiment_analysis"
    )
    @patch(
        "modules.central_brain.predict_price"
    )
    @patch(
        "modules.central_brain.analyze"
    )
    @patch(
        "modules.central_brain.generate_strategy"
    )
    def test_complete_pipeline(

        self,

        mock_strategy,

        mock_ai,

        mock_prediction,

        mock_sentiment,

        mock_volume,

        mock_pattern,

        mock_technical,

        mock_events,

        mock_news_analysis,

        mock_news,

        mock_scan_mcx,

        mock_scan_market,

        mock_market_data

    ):

        dataframe = FakeDataFrame(
            empty=False
        )

        mock_market_data.return_value = dataframe

        mock_scan_market.return_value = []
        mock_scan_mcx.return_value = []

        mock_news.return_value = {

            "articles": [

                {

                    "title":

                        "Market shows strength"

                }

            ]

        }

        mock_news_analysis.return_value = {

            "sentiment": "BULLISH"

        }

        mock_events.return_value = {}

        mock_technical.return_value = {

            "price": 100,

            "signal": "BUY"

        }

        mock_pattern.return_value = {}

        mock_volume.return_value = {}

        mock_sentiment.return_value = {

            "sentiment": "BULLISH"

        }

        mock_prediction.return_value = {

            "signal": "BUY",

            "confidence": 75

        }

        mock_ai.return_value = {

            "signal": "BUY",

            "confidence": 80

        }

        mock_strategy.return_value = {

            "action": "BUY",

            "confidence": 80

        }

        self.brain.risk.evaluate = Mock(

            return_value={

                "status": "success",

                "risk_level": "MEDIUM"

            }

        )

        self.brain.decision.decide = Mock(

            return_value={

                "decision": "BUY"

            }

        )

        result = self.brain.think(
            "RELIANCE"
        )

        self.assertIsInstance(
            result,
            dict
        )

        self.assertIn(
            "market_data",
            result
        )

        self.assertIn(
            "scanner",
            result
        )

        self.assertIn(
            "news",
            result
        )

        self.assertIn(
            "technical",
            result
        )

        self.assertIn(
            "prediction",
            result
        )

        self.assertIn(
            "ai",
            result
        )

        self.assertIn(
            "strategy",
            result
        )

        self.assertIn(
            "risk",
            result
        )

        self.assertIn(
            "decision",
            result
        )

        self.assertIn(
            "metadata",
            result
        )

        self.assertEqual(

            result["metadata"]

            .get(

                "pipeline_status"

            ),

            "completed"

        )

        self.assertEqual(

            result["metadata"]

            .get(

                "pipeline"

            ),

            "CentralBrain"

        )

        self.assertEqual(

            result["metadata"]

            .get(

                "symbol"

            ),

            "RELIANCE"

        )

        self.assertEqual(

            result["metadata"]

            .get(

                "module_count"

            ),

            14

        )


if __name__ == "__main__":

    unittest.main(
        verbosity=2
  )
