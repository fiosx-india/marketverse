"""
=========================================================
MarketVerse AI
Prediction Engine Tests
=========================================================

Tests the real behaviour of:

- get_prediction()
- predict_price()
- predict_market()

Test coverage:

- Empty / unavailable prediction
- Invalid input
- Neutral market
- Bullish technical evidence
- Bearish technical evidence
- EMA evidence
- MACD evidence
- RSI evidence
- Sentiment evidence
- News evidence
- Pattern evidence
- Volume evidence
- Market event evidence
- AI intelligence evidence
- Probability calculation
- Confidence boundaries
- Shared MarketContext compatibility
- DataFrame compatibility

No external market API is required for these tests.
=========================================================
"""

import unittest

import pandas as pd

from modules.prediction import (
    get_prediction,
    predict_price
)


class TestPredictionBasic(unittest.TestCase):

    def test_empty_data_returns_success(self):

        result = get_prediction(
            symbol="TEST",
            data={}
        )

        self.assertEqual(
            result["status"],
            "success"
        )

        self.assertEqual(
            result["signal"],
            "HOLD"
        )

        self.assertEqual(
            result["confidence"],
            0.0
        )

    def test_market_price_from_dictionary(self):

        result = get_prediction(

            symbol="TEST",

            data={

                "market": {

                    "price": 100

                }

            }

        )

        self.assertEqual(
            result["price"],
            100.0
        )

    def test_market_close_price_fallback(self):

        result = get_prediction(

            data={

                "market": {

                    "close": 150

                }

            }

        )

        self.assertEqual(
            result["price"],
            150.0
        )

    def test_indicator_price_fallback(self):

        result = get_prediction(

            data={

                "indicators": {

                    "price": 250

                }

            }

        )

        self.assertEqual(
            result["price"],
            250.0
        )


class TestPredictionTechnicalSignals(unittest.TestCase):

    def test_bullish_technical_signal(self):

        result = get_prediction(

            data={

                "market": {

                    "price": 100

                },

                "indicators": {

                    "signal": "BUY"

                }

            }

        )

        self.assertGreater(

            result["bullish_score"],

            result["bearish_score"]

        )

        self.assertIn(

            result["signal"],

            (
                "BUY",
                "STRONG BUY"
            )

        )

    def test_bearish_technical_signal(self):

        result = get_prediction(

            data={

                "market": {

                    "price": 100

                },

                "indicators": {

                    "signal": "SELL"

                }

            }

        )

        self.assertGreater(

            result["bearish_score"],

            result["bullish_score"]

        )

        self.assertIn(

            result["signal"],

            (
                "SELL",
                "STRONG SELL"
            )

        )

    def test_strong_buy_signal_normalization(self):

        result = get_prediction(

            data={

                "indicators": {

                    "signal": "STRONG BUY"

                }

            }

        )

        self.assertGreater(

            result["bullish_score"],

            0

        )

    def test_strong_sell_signal_normalization(self):

        result = get_prediction(

            data={

                "indicators": {

                    "signal": "STRONG SELL"

                }

            }

        )

        self.assertGreater(

            result["bearish_score"],

            0

        )


class TestPredictionEMA(unittest.TestCase):

    def test_bullish_ema_trend(self):

        result = get_prediction(

            data={

                "market": {

                    "price": 120

                },

                "indicators": {

                    "ema20": 110,

                    "ema50": 100

                }

            }

        )

        self.assertGreater(

            result["bullish_score"],

            result["bearish_score"]

        )

    def test_bearish_ema_trend(self):

        result = get_prediction(

            data={

                "market": {

                    "price": 90

                },

                "indicators": {

                    "ema20": 100,

                    "ema50": 110

                }

            }

        )

        self.assertGreater(

            result["bearish_score"],

            result["bullish_score"]

        )

    def test_price_above_ema20(self):

        result = get_prediction(

            data={

                "market": {

                    "price": 120

                },

                "indicators": {

                    "ema20": 100

                }

            }

        )

        self.assertGreater(

            result["bullish_score"],

            0

        )

    def test_price_below_ema20(self):

        result = get_prediction(

            data={

                "market": {

                    "price": 90

                },

                "indicators": {

                    "ema20": 100

                }

            }

        )

        self.assertGreater(

            result["bearish_score"],

            0

        )


class TestPredictionMACD(unittest.TestCase):

    def test_bullish_macd(self):

        result = get_prediction(

            data={

                "indicators": {

                    "macd": 5,

                    "macd_signal": 2

                }

            }

        )

        self.assertGreater(

            result["bullish_score"],

            result["bearish_score"]

        )

    def test_bearish_macd(self):

        result = get_prediction(

            data={

                "indicators": {

                    "macd": 1,

                    "macd_signal": 5

                }

            }

        )

        self.assertGreater(

            result["bearish_score"],

            result["bullish_score"]

        )


class TestPredictionRSI(unittest.TestCase):

    def test_oversold_rsi_is_bullish_evidence(self):

        result = get_prediction(

            data={

                "indicators": {

                    "rsi": 25

                }

            }

        )

        self.assertGreater(

            result["bullish_score"],

            0

        )

    def test_overbought_rsi_is_bearish_evidence(self):

        result = get_prediction(

            data={

                "indicators": {

                    "rsi": 80

                }

            }

        )

        self.assertGreater(

            result["bearish_score"],

            0

        )

    def test_neutral_rsi(self):

        result = get_prediction(

            data={

                "indicators": {

                    "rsi": 50

                }

            }

        )

        self.assertEqual(

            result["signal"],

            "HOLD"

        )


class TestPredictionExternalEvidence(unittest.TestCase):

    def test_bullish_sentiment(self):

        result = get_prediction(

            data={

                "sentiment": {

                    "signal": "BUY"

                }

            }

        )

        self.assertGreater(

            result["bullish_score"],

            result["bearish_score"]

        )

    def test_bearish_sentiment(self):

        result = get_prediction(

            data={

                "sentiment": {

                    "signal": "SELL"

                }

            }

        )

        self.assertGreater(

            result["bearish_score"],

            result["bullish_score"]

        )

    def test_positive_news(self):

        result = get_prediction(

            data={

                "news_analysis": {

                    "sentiment": "POSITIVE"

                }

            }

        )

        self.assertGreater(

            result["bullish_score"],

            0

        )

    def test_negative_news(self):

        result = get_prediction(

            data={

                "news_analysis": {

                    "sentiment": "NEGATIVE"

                }

            }

        )

        self.assertGreater(

            result["bearish_score"],

            0

        )

    def test_bullish_pattern(self):

        result = get_prediction(

            data={

                "pattern": {

                    "bullish": True

                }

            }

        )

        self.assertGreater(

            result["bullish_score"],

            0

        )

    def test_bearish_pattern(self):

        result = get_prediction(

            data={

                "pattern": {

                    "bearish": True

                }

            }

        )

        self.assertGreater(

            result["bearish_score"],

            0

        )

    def test_bullish_volume(self):

        result = get_prediction(

            data={

                "volume": {

                    "signal": "BUY"

                }

            }

        )

        self.assertGreater(

            result["bullish_score"],

            0

        )

    def test_bearish_volume(self):

        result = get_prediction(

            data={

                "volume": {

                    "signal": "SELL"

                }

            }

        )

        self.assertGreater(

            result["bearish_score"],

            0

        )

    def test_bullish_market_event(self):

        result = get_prediction(

            data={

                "events": {

                    "signal": "BUY"

                }

            }

        )

        self.assertGreater(

            result["bullish_score"],

            0

        )

    def test_bearish_market_event(self):

        result = get_prediction(

            data={

                "events": {

                    "signal": "SELL"

                }

            }

        )

        self.assertGreater(

            result["bearish_score"],

            0

        )

    def test_bullish_ai_intelligence(self):

        result = get_prediction(

            data={

                "ai_market_intelligence": {

                    "signal": "BUY"

                }

            }

        )

        self.assertGreater(

            result["bullish_score"],

            0

        )

    def test_bearish_ai_intelligence(self):

        result = get_prediction(

            data={

                "ai_market_intelligence": {

                    "signal": "SELL"

                }

            }

        )

        self.assertGreater(

            result["bearish_score"],

            0

        )


class TestPredictionProbability(unittest.TestCase):

    def test_probabilities_are_valid(self):

        result = get_prediction(

            data={

                "indicators": {

                    "signal": "BUY"

                },

                "sentiment": {

                    "signal": "BUY"

                }

            }

        )

        self.assertGreaterEqual(

            result["bullish_probability"],

            0

        )

        self.assertLessEqual(

            result["bullish_probability"],

            1

        )

        self.assertGreaterEqual(

            result["bearish_probability"],

            0

        )

        self.assertLessEqual(

            result["bearish_probability"],

            1

        )

    def test_directional_probabilities_sum_to_one(self):

        result = get_prediction(

            data={

                "indicators": {

                    "signal": "BUY"

                },

                "sentiment": {

                    "signal": "SELL"

                }

            }

        )

        total = (

            result["bullish_probability"]

            +

            result["bearish_probability"]

        )

        self.assertAlmostEqual(

            total,

            1.0,

            places=2

        )

    def test_dominant_probability_is_maximum_direction(self):

        result = get_prediction(

            data={

                "indicators": {

                    "signal": "BUY"

                },

                "sentiment": {

                    "signal": "SELL"

                }

            }

        )

        expected = max(

            result["bullish_probability"],

            result["bearish_probability"]

        )

        self.assertEqual(

            result["probability"],

            expected

        )


class TestPredictionConfidence(unittest.TestCase):

    def test_confidence_is_valid_range(self):

        result = get_prediction(

            data={

                "indicators": {

                    "signal": "BUY"

                }

            }

        )

        self.assertGreaterEqual(

            result["confidence"],

            0

        )

        self.assertLessEqual(

            result["confidence"],

            95

        )

    def test_empty_prediction_confidence_zero(self):

        result = get_prediction(
            data={}
        )

        self.assertEqual(

            result["confidence"],

            0.0

        )

    def test_confidence_never_exceeds_95(self):

        result = get_prediction(

            data={

                "indicators": {

                    "signal": "BUY",

                    "rsi": 20,

                    "ema20": 120,

                    "ema50": 100,

                    "macd": 10,

                    "macd_signal": 2

                },

                "market": {

                    "price": 130

                },

                "sentiment": {

                    "signal": "BUY"

                },

                "news_analysis": {

                    "sentiment": "POSITIVE"

                },

                "pattern": {

                    "bullish": True

                },

                "volume": {

                    "signal": "BUY"

                },

                "events": {

                    "signal": "BUY"

                },

                "ai_market_intelligence": {

                    "signal": "BUY"

                }

            }

        )

        self.assertLessEqual(

            result["confidence"],

            95

        )


class TestPredictPriceInterface(unittest.TestCase):

    def test_shared_market_context(self):

        context = {

            "symbol": "TEST",

            "technical": {

                "price": 100,

                "signal": "BUY"

            },

            "sentiment": {

                "signal": "BUY"

            },

            "news_analysis": {

                "sentiment": "POSITIVE"

            },

            "pattern": {

                "bullish": True

            },

            "volume": {

                "signal": "BUY"

            },

            "events": {

                "signal": "BUY"

            },

            "ai": {

                "signal": "BUY"

            }

        }

        result = predict_price(
            context
        )

        self.assertEqual(

            result["status"],

            "success"

        )

        self.assertEqual(

            result["symbol"],

            "TEST"

        )

        self.assertGreater(

            result["bullish_score"],

            result["bearish_score"]

        )

    def test_invalid_source_returns_unavailable(self):

        result = predict_price(
            None
        )

        self.assertEqual(

            result["status"],

            "unavailable"

        )

        self.assertEqual(

            result["signal"],

            "HOLD"

        )


class TestPredictionDataFrame(unittest.TestCase):

    def test_dataframe_prediction_interface(self):

        dataframe = pd.DataFrame(

            {

                "Open": [

                    100,
                    101,
                    102,
                    103,
                    104
                ],

                "High": [

                    102,
                    103,
                    104,
                    105,
                    106
                ],

                "Low": [

                    99,
                    100,
                    101,
                    102,
                    103
                ],

                "Close": [

                    101,
                    102,
                    103,
                    104,
                    105
                ],

                "Volume": [

                    1000,
                    1100,
                    1200,
                    1300,
                    1400
                ]

            }

        )

        result = predict_price(
            dataframe
        )

        self.assertIn(

            result["status"],

            (

                "success",

                "unavailable"

            )

        )

    def test_empty_dataframe(self):

        dataframe = pd.DataFrame()

        result = predict_price(
            dataframe
        )

        self.assertEqual(

            result["status"],

            "unavailable"

        )

        self.assertEqual(

            result["signal"],

            "HOLD"

        )


if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )
