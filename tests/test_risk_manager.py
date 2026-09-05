"""
=========================================================
MarketVerse AI
RiskManager Tests
=========================================================

Tests:
- Invalid entry price
- HOLD signal
- BUY calculation
- SELL calculation
- Signal normalization
- Confidence normalization
- Risk amount
- Position sizing
- Risk reward
- Invalid MarketContext
- Entry price priority
- Strategy signal priority
- Prediction signal fallback
- AI signal fallback

These tests validate RiskManager behaviour only.

They do not fetch market data and do not execute
the CentralBrain pipeline.
=========================================================
"""

import unittest

from modules.risk_manager import (
    RiskManager,
    calculate_risk
)


class TestRiskCalculation(unittest.TestCase):
    """
    Direct calculate_risk() tests.
    """

    def test_invalid_entry_price_none(self):

        result = calculate_risk(
            entry_price=None
        )

        self.assertEqual(
            result["status"],
            "error"
        )

        self.assertFalse(
            result["trade_allowed"]
        )

    def test_invalid_entry_price_zero(self):

        result = calculate_risk(
            entry_price=0
        )

        self.assertEqual(
            result["status"],
            "error"
        )

        self.assertFalse(
            result["trade_allowed"]
        )

    def test_invalid_entry_price_negative(self):

        result = calculate_risk(
            entry_price=-100
        )

        self.assertEqual(
            result["status"],
            "error"
        )

        self.assertFalse(
            result["trade_allowed"]
        )

    def test_hold_signal(self):

        result = calculate_risk(

            entry_price=100,

            signal="HOLD",

            confidence=75

        )

        self.assertEqual(
            result["status"],
            "success"
        )

        self.assertEqual(
            result["signal"],
            "HOLD"
        )

        self.assertFalse(
            result["trade_allowed"]
        )

        self.assertEqual(
            result["entry"],
            100
        )

    def test_buy_calculation(self):

        result = calculate_risk(

            entry_price=100,

            signal="BUY",

            confidence=80,

            capital=100000,

            risk_percent=2

        )

        self.assertEqual(
            result["status"],
            "success"
        )

        self.assertEqual(
            result["signal"],
            "BUY"
        )

        self.assertTrue(
            result["trade_allowed"]
        )

        self.assertLess(
            result["stop_loss"],
            result["entry"]
        )

        self.assertGreater(
            result["target_1"],
            result["entry"]
        )

        self.assertGreater(
            result["target_2"],
            result["target_1"]
        )

    def test_sell_calculation(self):

        result = calculate_risk(

            entry_price=100,

            signal="SELL",

            confidence=80,

            capital=100000,

            risk_percent=2

        )

        self.assertEqual(
            result["status"],
            "success"
        )

        self.assertEqual(
            result["signal"],
            "SELL"
        )

        self.assertTrue(
            result["trade_allowed"]
        )

        self.assertGreater(
            result["stop_loss"],
            result["entry"]
        )

        self.assertLess(
            result["target_1"],
            result["entry"]
        )

        self.assertLess(
            result["target_2"],
            result["target_1"]
        )

    def test_risk_amount(self):

        result = calculate_risk(

            entry_price=100,

            signal="BUY",

            capital=100000,

            risk_percent=2

        )

        self.assertEqual(
            result["risk_amount"],
            2000
        )

    def test_position_size_positive(self):

        result = calculate_risk(

            entry_price=100,

            signal="BUY",

            capital=100000,

            risk_percent=2

        )

        self.assertGreater(
            result["quantity"],
            0
        )

    def test_expected_loss_does_not_exceed_risk_amount_significantly(self):

        result = calculate_risk(

            entry_price=100,

            signal="BUY",

            capital=100000,

            risk_percent=2

        )

        self.assertLessEqual(

            result["expected_loss"],

            result["risk_amount"]

        )

    def test_risk_reward_ratio_positive(self):

        result = calculate_risk(

            entry_price=100,

            signal="BUY"

        )

        self.assertGreater(
            result["risk_reward_ratio"],
            0
        )


class TestSignalNormalization(unittest.TestCase):
    """
    Signal normalization tests.
    """

    def test_bullish_becomes_buy(self):

        result = calculate_risk(

            entry_price=100,

            signal="BULLISH"

        )

        self.assertEqual(
            result["signal"],
            "BUY"
        )

    def test_bearish_becomes_sell(self):

        result = calculate_risk(

            entry_price=100,

            signal="BEARISH"

        )

        self.assertEqual(
            result["signal"],
            "SELL"
        )

    def test_strong_buy_becomes_buy(self):

        result = calculate_risk(

            entry_price=100,

            signal="STRONG BUY"

        )

        self.assertEqual(
            result["signal"],
            "BUY"
        )

    def test_strong_sell_becomes_sell(self):

        result = calculate_risk(

            entry_price=100,

            signal="STRONG SELL"

        )

        self.assertEqual(
            result["signal"],
            "SELL"
        )

    def test_unknown_signal_becomes_hold(self):

        result = calculate_risk(

            entry_price=100,

            signal="UNKNOWN"

        )

        self.assertEqual(
            result["signal"],
            "HOLD"
        )


class TestConfidenceHandling(unittest.TestCase):
    """
    Confidence boundary tests.
    """

    def test_confidence_above_100(self):

        result = calculate_risk(

            entry_price=100,

            signal="BUY",

            confidence=150

        )

        self.assertEqual(
            result["confidence"],
            100
        )

    def test_confidence_below_zero(self):

        result = calculate_risk(

            entry_price=100,

            signal="BUY",

            confidence=-50

        )

        self.assertEqual(
            result["confidence"],
            0
        )

    def test_low_confidence_risk_level(self):

        result = calculate_risk(

            entry_price=100,

            signal="BUY",

            confidence=40

        )

        self.assertEqual(
            result["risk_level"],
            "HIGH"
        )

    def test_medium_confidence_risk_level(self):

        result = calculate_risk(

            entry_price=100,

            signal="BUY",

            confidence=65

        )

        self.assertEqual(
            result["risk_level"],
            "MEDIUM"
        )

    def test_high_confidence_risk_level(self):

        result = calculate_risk(

            entry_price=100,

            signal="BUY",

            confidence=85

        )

        self.assertEqual(
            result["risk_level"],
            "LOW"
        )


class TestRiskManagerInterface(unittest.TestCase):
    """
    RiskManager.calculate() interface tests.
    """

    def setUp(self):

        self.manager = RiskManager()

    def test_static_calculate(self):

        result = RiskManager.calculate(

            entry_price=100,

            signal="BUY"

        )

        self.assertEqual(
            result["status"],
            "success"
        )

        self.assertEqual(
            result["signal"],
            "BUY"
        )


class TestMarketContextEvaluation(unittest.TestCase):
    """
    RiskManager.evaluate() tests.

    Tests Shared MarketContext compatibility.
    """

    def setUp(self):

        self.manager = RiskManager()

    def test_invalid_context(self):

        result = self.manager.evaluate(
            None
        )

        self.assertEqual(
            result["status"],
            "error"
        )

        self.assertFalse(
            result["trade_allowed"]
        )

    def test_empty_context(self):

        result = self.manager.evaluate(
            {}
        )

        self.assertEqual(
            result["status"],
            "error"
        )

    def test_technical_price_priority(self):

        analysis = {

            "technical": {

                "price": 100

            },

            "market_data": {

                "price": 200

            },

            "market": {

                "price": 300

            },

            "strategy": {

                "action": "BUY",

                "confidence": 80

            }

        }

        result = self.manager.evaluate(
            analysis
        )

        self.assertEqual(
            result["entry"],
            100
        )

    def test_market_data_price_fallback(self):

        analysis = {

            "technical": {},

            "market_data": {

                "price": 200

            },

            "strategy": {

                "action": "BUY"

            }

        }

        result = self.manager.evaluate(
            analysis
        )

        self.assertEqual(
            result["entry"],
            200
        )

    def test_legacy_market_price_fallback(self):

        analysis = {

            "technical": {},

            "market": {

                "price": 300

            },

            "strategy": {

                "action": "BUY"

            }

        }

        result = self.manager.evaluate(
            analysis
        )

        self.assertEqual(
            result["entry"],
            300
        )

    def test_strategy_signal_priority(self):

        analysis = {

            "technical": {

                "price": 100

            },

            "strategy": {

                "action": "BUY",

                "confidence": 90

            },

            "prediction": {

                "signal": "SELL",

                "confidence": 70

            },

            "ai": {

                "signal": "SELL",

                "confidence": 60

            }

        }

        result = self.manager.evaluate(
            analysis
        )

        self.assertEqual(
            result["signal"],
            "BUY"
        )

    def test_prediction_signal_fallback(self):

        analysis = {

            "technical": {

                "price": 100

            },

            "strategy": {},

            "prediction": {

                "signal": "SELL",

                "confidence": 75

            }

        }

        result = self.manager.evaluate(
            analysis
        )

        self.assertEqual(
            result["signal"],
            "SELL"
        )

    def test_ai_signal_fallback(self):

        analysis = {

            "technical": {

                "price": 100

            },

            "strategy": {},

            "prediction": {},

            "ai": {

                "signal": "BUY",

                "confidence": 70

            }

        }

        result = self.manager.evaluate(
            analysis
        )

        self.assertEqual(
            result["signal"],
            "BUY"
        )

    def test_strategy_confidence_priority(self):

        analysis = {

            "technical": {

                "price": 100

            },

            "strategy": {

                "action": "BUY",

                "confidence": 90

            },

            "prediction": {

                "signal": "BUY",

                "confidence": 50

            },

            "ai": {

                "signal": "BUY",

                "confidence": 20

            }

        }

        result = self.manager.evaluate(
            analysis
        )

        self.assertEqual(
            result["confidence"],
            90
        )

    def test_hold_strategy_blocks_trade(self):

        analysis = {

            "technical": {

                "price": 100

            },

            "strategy": {

                "action": "HOLD",

                "confidence": 80

            }

        }

        result = self.manager.evaluate(
            analysis
        )

        self.assertEqual(
            result["signal"],
            "HOLD"
        )

        self.assertFalse(
            result["trade_allowed"]
        )


if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )
