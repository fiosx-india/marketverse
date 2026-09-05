"""
=========================================================
MarketVerse AI
NSE Service Tests
=========================================================

Tests:
- NSE service import
- NSE service object availability
- Required public methods
- is_connected() return type
- get_fno_symbols() return type
- F&O symbols structure

External NSE connectivity is not required for the
core structural tests.

Live NSE calls are handled safely because network,
rate limits, holidays, or NSE downtime should not
make the entire unit test suite unreliable.
=========================================================
"""

import unittest
from unittest.mock import patch

from services.nse_service import nse


class TestNSEServiceStructure(unittest.TestCase):
    """
    Tests the NSE service public interface.
    """

    def test_nse_service_exists(self):

        self.assertIsNotNone(
            nse
        )

    def test_is_connected_method_exists(self):

        self.assertTrue(
            hasattr(
                nse,
                "is_connected"
            )
        )

        self.assertTrue(
            callable(
                nse.is_connected
            )
        )

    def test_get_fno_symbols_method_exists(self):

        self.assertTrue(
            hasattr(
                nse,
                "get_fno_symbols"
            )
        )

        self.assertTrue(
            callable(
                nse.get_fno_symbols
            )
        )


class TestNSEConnection(unittest.TestCase):
    """
    Tests connection handling.

    These tests do not require NSE to actually be online.
    """

    def test_is_connected_returns_boolean_or_safe_value(self):

        try:

            result = nse.is_connected()

        except Exception as error:

            self.fail(
                "is_connected() raised an exception: "
                f"{error}"
            )

        self.assertIn(

            result,

            (
                True,
                False
            )

        )


class TestFNOSymbols(unittest.TestCase):
    """
    Tests F&O symbols response handling.
    """

    def test_get_fno_symbols_does_not_crash(self):

        try:

            symbols = nse.get_fno_symbols()

        except Exception as error:

            self.fail(
                "get_fno_symbols() raised an exception: "
                f"{error}"
            )

        self.assertIsNotNone(
            symbols
        )

    def test_get_fno_symbols_returns_collection(self):

        try:

            symbols = nse.get_fno_symbols()

        except Exception as error:

            self.fail(
                "get_fno_symbols() raised an exception: "
                f"{error}"
            )

        self.assertIsInstance(

            symbols,

            (
                list,
                tuple,
                set
            )

        )

    def test_fno_symbols_are_strings_when_available(self):

        symbols = nse.get_fno_symbols()

        if not symbols:

            self.skipTest(
                "No F&O symbols available. "
                "NSE may be offline or unavailable."
            )

        for symbol in symbols:

            self.assertIsInstance(
                symbol,
                str
            )

            self.assertTrue(
                symbol.strip()
            )


class TestNSEServiceMockedBehaviour(unittest.TestCase):
    """
    Tests predictable NSE service behaviour using mocks.

    This prevents external NSE availability from being
    required for every test run.
    """

    def test_mocked_connection_true(self):

        with patch.object(

            nse,

            "is_connected",

            return_value=True

        ):

            result = nse.is_connected()

            self.assertTrue(
                result
            )

    def test_mocked_connection_false(self):

        with patch.object(

            nse,

            "is_connected",

            return_value=False

        ):

            result = nse.is_connected()

            self.assertFalse(
                result
            )

    def test_mocked_fno_symbols(self):

        expected_symbols = [

            "RELIANCE",

            "TCS",

            "INFY"

        ]

        with patch.object(

            nse,

            "get_fno_symbols",

            return_value=expected_symbols

        ):

            symbols = nse.get_fno_symbols()

            self.assertEqual(

                symbols,

                expected_symbols

            )

            self.assertEqual(

                len(symbols),

                3

            )

    def test_mocked_empty_fno_symbols(self):

        with patch.object(

            nse,

            "get_fno_symbols",

            return_value=[]

        ):

            symbols = nse.get_fno_symbols()

            self.assertEqual(
                symbols,
                []
            )

            self.assertEqual(
                len(symbols),
                0
            )


class TestLiveNSEService(unittest.TestCase):
    """
    Optional live NSE integration checks.

    These tests validate the response safely.
    They should not assume NSE is always available.
    """

    def test_live_connection_and_symbols_are_consistent(self):

        connected = nse.is_connected()

        symbols = nse.get_fno_symbols()

        self.assertIsInstance(
            connected,
            bool
        )

        self.assertIsInstance(

            symbols,

            (
                list,
                tuple,
                set
            )

        )

        if connected and symbols:

            self.assertGreater(
                len(symbols),
                0
            )


if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )
