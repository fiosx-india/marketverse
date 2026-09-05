"""
=========================================================
MarketVerse AI
Portfolio Manager Tests
=========================================================

Tests the actual behaviour of modules.portfolio.Portfolio.

Coverage:
- Portfolio initialization
- Add stock
- Symbol normalization
- Multiple quantity additions
- Buy price updates
- Remove stock
- Update current price
- Get stock
- Get portfolio
- Total portfolio value
- Total profit and loss
- Portfolio summary
- Clear portfolio
=========================================================
"""

import unittest

from modules.portfolio import Portfolio


class TestPortfolioInitialization(unittest.TestCase):

    def test_portfolio_starts_empty(self):

        portfolio = Portfolio()

        self.assertEqual(
            portfolio.get_portfolio(),
            {}
        )

    def test_initial_total_value_is_zero(self):

        portfolio = Portfolio()

        self.assertEqual(
            portfolio.total_value(),
            0
        )

    def test_initial_profit_is_zero(self):

        portfolio = Portfolio()

        self.assertEqual(
            portfolio.total_profit(),
            0
        )


class TestAddStock(unittest.TestCase):

    def setUp(self):

        self.portfolio = Portfolio()

    def test_add_stock(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        stock = self.portfolio.get_stock(
            "RELIANCE"
        )

        self.assertIsNotNone(
            stock
        )

        self.assertEqual(
            stock["quantity"],
            10
        )

        self.assertEqual(
            stock["buy_price"],
            1000
        )

    def test_symbol_is_converted_to_uppercase(self):

        self.portfolio.add_stock(
            "reliance",
            10,
            1000
        )

        stock = self.portfolio.get_stock(
            "RELIANCE"
        )

        self.assertIsNotNone(
            stock
        )

    def test_get_stock_is_case_insensitive(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        stock = self.portfolio.get_stock(
            "reliance"
        )

        self.assertIsNotNone(
            stock
        )

        self.assertEqual(
            stock["quantity"],
            10
        )

    def test_multiple_additions_increase_quantity(self):

        self.portfolio.add_stock(
            "TCS",
            10,
            3000
        )

        self.portfolio.add_stock(
            "TCS",
            5
        )

        stock = self.portfolio.get_stock(
            "TCS"
        )

        self.assertEqual(
            stock["quantity"],
            15
        )

    def test_new_buy_price_updates_existing_stock(self):

        self.portfolio.add_stock(
            "INFY",
            10,
            1000
        )

        self.portfolio.add_stock(
            "INFY",
            5,
            1100
        )

        stock = self.portfolio.get_stock(
            "INFY"
        )

        self.assertEqual(
            stock["quantity"],
            15
        )

        self.assertEqual(
            stock["buy_price"],
            1100
        )

    def test_zero_buy_price_does_not_replace_existing_price(self):

        self.portfolio.add_stock(
            "SBIN",
            10,
            500
        )

        self.portfolio.add_stock(
            "SBIN",
            5,
            0
        )

        stock = self.portfolio.get_stock(
            "SBIN"
        )

        self.assertEqual(
            stock["buy_price"],
            500
        )

    def test_added_timestamp_exists(self):

        self.portfolio.add_stock(
            "HDFCBANK",
            10,
            1500
        )

        stock = self.portfolio.get_stock(
            "HDFCBANK"
        )

        self.assertIn(
            "added",
            stock
        )


class TestRemoveStock(unittest.TestCase):

    def setUp(self):

        self.portfolio = Portfolio()

    def test_remove_existing_stock(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        self.portfolio.remove_stock(
            "RELIANCE"
        )

        stock = self.portfolio.get_stock(
            "RELIANCE"
        )

        self.assertIsNone(
            stock
        )

    def test_remove_stock_is_case_insensitive(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        self.portfolio.remove_stock(
            "reliance"
        )

        self.assertIsNone(
            self.portfolio.get_stock(
                "RELIANCE"
            )
        )

    def test_remove_missing_stock_does_not_crash(self):

        self.portfolio.remove_stock(
            "UNKNOWN"
        )

        self.assertEqual(
            self.portfolio.get_portfolio(),
            {}
        )


class TestUpdatePrice(unittest.TestCase):

    def setUp(self):

        self.portfolio = Portfolio()

    def test_update_current_price(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        self.portfolio.update_price(
            "RELIANCE",
            1200
        )

        stock = self.portfolio.get_stock(
            "RELIANCE"
        )

        self.assertEqual(
            stock["current_price"],
            1200
        )

    def test_update_price_is_case_insensitive(self):

        self.portfolio.add_stock(
            "TCS",
            10,
            3000
        )

        self.portfolio.update_price(
            "tcs",
            3200
        )

        stock = self.portfolio.get_stock(
            "TCS"
        )

        self.assertEqual(
            stock["current_price"],
            3200
        )

    def test_update_missing_stock_does_not_create_stock(self):

        self.portfolio.update_price(
            "UNKNOWN",
            100
        )

        self.assertIsNone(
            self.portfolio.get_stock(
                "UNKNOWN"
            )
        )


class TestGetPortfolio(unittest.TestCase):

    def setUp(self):

        self.portfolio = Portfolio()

    def test_get_stock_returns_correct_stock(self):

        self.portfolio.add_stock(
            "INFY",
            10,
            1500
        )

        stock = self.portfolio.get_stock(
            "INFY"
        )

        self.assertEqual(
            stock["quantity"],
            10
        )

        self.assertEqual(
            stock["buy_price"],
            1500
        )

    def test_get_missing_stock_returns_none(self):

        stock = self.portfolio.get_stock(
            "UNKNOWN"
        )

        self.assertIsNone(
            stock
        )

    def test_get_portfolio_contains_multiple_stocks(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        self.portfolio.add_stock(
            "TCS",
            5,
            3000
        )

        holdings = self.portfolio.get_portfolio()

        self.assertEqual(
            len(holdings),
            2
        )

        self.assertIn(
            "RELIANCE",
            holdings
        )

        self.assertIn(
            "TCS",
            holdings
        )


class TestPortfolioValue(unittest.TestCase):

    def setUp(self):

        self.portfolio = Portfolio()

    def test_total_value_uses_buy_price_when_current_price_missing(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        self.assertEqual(
            self.portfolio.total_value(),
            10000
        )

    def test_total_value_uses_current_price(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        self.portfolio.update_price(
            "RELIANCE",
            1200
        )

        self.assertEqual(
            self.portfolio.total_value(),
            12000
        )

    def test_total_value_multiple_stocks(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        self.portfolio.add_stock(
            "TCS",
            5,
            3000
        )

        self.portfolio.update_price(
            "RELIANCE",
            1200
        )

        self.portfolio.update_price(
            "TCS",
            3200
        )

        expected_value = (

            10 * 1200

            +

            5 * 3200

        )

        self.assertEqual(
            self.portfolio.total_value(),
            expected_value
        )

    def test_total_value_rounding(self):

        self.portfolio.add_stock(
            "TEST",
            3,
            100.555
        )

        expected = round(
            3 * 100.555,
            2
        )

        self.assertEqual(
            self.portfolio.total_value(),
            expected
        )


class TestPortfolioProfit(unittest.TestCase):

    def setUp(self):

        self.portfolio = Portfolio()

    def test_profit_when_price_increases(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        self.portfolio.update_price(
            "RELIANCE",
            1200
        )

        self.assertEqual(
            self.portfolio.total_profit(),
            2000
        )

    def test_loss_when_price_decreases(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        self.portfolio.update_price(
            "RELIANCE",
            800
        )

        self.assertEqual(
            self.portfolio.total_profit(),
            -2000
        )

    def test_zero_profit_without_price_update(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        self.assertEqual(
            self.portfolio.total_profit(),
            0
        )

    def test_total_profit_multiple_stocks(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        self.portfolio.add_stock(
            "TCS",
            5,
            3000
        )

        self.portfolio.update_price(
            "RELIANCE",
            1200
        )

        self.portfolio.update_price(
            "TCS",
            2800
        )

        expected_profit = (

            (1200 - 1000) * 10

            +

            (2800 - 3000) * 5

        )

        self.assertEqual(
            self.portfolio.total_profit(),
            expected_profit
        )


class TestPortfolioSummary(unittest.TestCase):

    def setUp(self):

        self.portfolio = Portfolio()

    def test_empty_portfolio_summary(self):

        summary = self.portfolio.summary()

        self.assertEqual(
            summary["stocks"],
            0
        )

        self.assertEqual(
            summary["value"],
            0
        )

        self.assertEqual(
            summary["profit"],
            0
        )

    def test_portfolio_summary(self):

        self.portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        self.portfolio.update_price(
            "RELIANCE",
            1200
        )

        summary = self.portfolio.summary()

        self.assertEqual(
            summary["stocks"],
            1
        )

        self.assertEqual(
            summary["value"],
            12000
        )

        self.assertEqual(
            summary["profit"],
            2000
        )


class TestClearPortfolio(unittest.TestCase):

    def test_clear_portfolio(self):

        portfolio = Portfolio()

        portfolio.add_stock(
            "RELIANCE",
            10,
            1000
        )

        portfolio.add_stock(
            "TCS",
            5,
            3000
        )

        portfolio.clear()

        self.assertEqual(
            portfolio.get_portfolio(),
            {}
        )

        self.assertEqual(
            portfolio.total_value(),
            0
        )

        self.assertEqual(
            portfolio.total_profit(),
            0
        )

    def test_clear_empty_portfolio(self):

        portfolio = Portfolio()

        portfolio.clear()

        self.assertEqual(
            portfolio.get_portfolio(),
            {}
        )


if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )
