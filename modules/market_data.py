"""
=========================================================
MarketVerse AI
Market Data Provider
=========================================================

Purpose
-------
Provides standardized market OHLC data to the
MarketVerse AI intelligence pipeline.

Responsibilities
----------------
- Fetch market data
- Validate returned OHLC data
- Normalize DataFrame columns
- Retry temporary data failures
- Preserve DataFrame compatibility

This module does NOT:
- Perform technical analysis
- Generate predictions
- Generate trading decisions
- Perform orchestration

CentralBrain remains responsible for orchestration.
Guardian remains responsible for system monitoring.
=========================================================
"""

import logging
import time

import pandas as pd
import yfinance as yf


# =========================================================
# LOGGER
# =========================================================

logger = logging.getLogger(__name__)


# =========================================================
# CONFIGURATION
# =========================================================

DEFAULT_PERIOD = "3mo"

DEFAULT_INTERVAL = "1d"

MAX_RETRIES = 3

RETRY_DELAY_SECONDS = 1


# =========================================================
# DATA VALIDATION
# =========================================================

def _normalize_dataframe(df):
    """
    Normalize market data returned by the provider.

    Ensures:
    - Pandas DataFrame
    - Flat column names
    - Required OHLC columns
    """

    if not isinstance(
        df,
        pd.DataFrame
    ):
        return None

    if df.empty:
        return None

    # -----------------------------------------------------
    # Fix MultiIndex Columns
    # -----------------------------------------------------

    if (
        hasattr(df.columns, "nlevels")
        and df.columns.nlevels > 1
    ):

        df = df.copy()

        df.columns = (
            df.columns.get_level_values(0)
        )

    # -----------------------------------------------------
    # Required Columns
    # -----------------------------------------------------

    required_columns = {

        "Open",

        "High",

        "Low",

        "Close"

    }

    if not required_columns.issubset(
        df.columns
    ):

        logger.warning(

            "Market data missing required columns: %s",

            required_columns

        )

        return None

    # -----------------------------------------------------
    # Remove Duplicate Index Entries
    # -----------------------------------------------------

    df = df.loc[
        ~df.index.duplicated(
            keep="last"
        )
    ]

    # -----------------------------------------------------
    # Sort by Time
    # -----------------------------------------------------

    df = df.sort_index()

    # -----------------------------------------------------
    # Remove Completely Empty Rows
    # -----------------------------------------------------

    df = df.dropna(
        how="all"
    )

    if df.empty:

        return None

    return df


# =========================================================
# MARKET DATA FETCHER
# =========================================================

def get_market_data(
    symbol,
    period=DEFAULT_PERIOD,
    interval=DEFAULT_INTERVAL
):
    """
    Fetch validated OHLC market data.

    Parameters
    ----------
    symbol : str
        Market symbol.

    period : str
        Historical period.

    interval : str
        Candle interval.

    Returns
    -------
    pandas.DataFrame | None

    Important
    ---------
    This function preserves the existing project contract.

    Existing modules expect a DataFrame, therefore:

        Success -> DataFrame

        Failure -> None
    """

    # -----------------------------------------------------
    # Validate Symbol
    # -----------------------------------------------------

    if not isinstance(
        symbol,
        str
    ):

        logger.error(

            "Invalid market symbol type: %s",

            type(symbol)

        )

        return None

    symbol = symbol.strip()

    if not symbol:

        logger.error(
            "Market symbol is empty"
        )

        return None

    # -----------------------------------------------------
    # Fetch with Retry
    # -----------------------------------------------------

    last_error = None

    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):

        try:

            logger.debug(

                "Fetching market data | "
                "symbol=%s attempt=%s/%s",

                symbol,

                attempt,

                MAX_RETRIES

            )

            df = yf.download(

                symbol,

                period=period,

                interval=interval,

                auto_adjust=True,

                progress=False,

                threads=False

            )

            df = _normalize_dataframe(
                df
            )

            if df is not None:

                logger.info(

                    "Market data loaded | "
                    "symbol=%s rows=%s",

                    symbol,

                    len(df)

                )

                return df

            logger.warning(

                "Empty or invalid market data | "
                "symbol=%s attempt=%s",

                symbol,

                attempt

            )

        except Exception as error:

            last_error = error

            logger.warning(

                "Market data fetch failed | "
                "symbol=%s attempt=%s error=%s",

                symbol,

                attempt,

                str(error)

            )

        # -------------------------------------------------
        # Retry Delay
        # -------------------------------------------------

        if attempt < MAX_RETRIES:

            time.sleep(
                RETRY_DELAY_SECONDS
            )

    # -----------------------------------------------------
    # Final Failure
    # -----------------------------------------------------

    if last_error:

        logger.error(

            "Market data unavailable after retries | "
            "symbol=%s error=%s",

            symbol,

            str(last_error)

        )

    else:

        logger.error(

            "Market data unavailable after retries | "
            "symbol=%s",

            symbol

        )

    return None


# =========================================================
# DASHBOARD DATA
# =========================================================

def get_dashboard_data():
    """
    Load default dashboard market data.

    This function preserves the existing dashboard API.
    """

    return {

        # ---------------------------------------------
        # Indian Indices
        # ---------------------------------------------

        "NIFTY50":

            get_market_data(
                "^NSEI"
            ),

        "SENSEX":

            get_market_data(
                "^BSESN"
            ),

        # ---------------------------------------------
        # Cryptocurrency
        # ---------------------------------------------

        "BTC":

            get_market_data(
                "BTC-USD"
            ),

        # ---------------------------------------------
        # Indian Equities
        # ---------------------------------------------

        "RELIANCE":

            get_market_data(
                "RELIANCE.NS"
            ),

        "TCS":

            get_market_data(
                "TCS.NS"
            ),

        "INFY":

            get_market_data(
                "INFY.NS"
            ),

        # ---------------------------------------------
        # Commodities
        # ---------------------------------------------

        "GOLD":

            get_market_data(
                "GC=F"
            ),

        "SILVER":

            get_market_data(
                "SI=F"
            ),

        "CRUDE_OIL":

            get_market_data(
                "CL=F"
            ),

        "NATURAL_GAS":

            get_market_data(
                "NG=F"
            ),

        "COPPER":

            get_market_data(
                "HG=F"
            ),

        "PLATINUM":

            get_market_data(
                "PL=F"
            )

    }
