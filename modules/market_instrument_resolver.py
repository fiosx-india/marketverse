"""
MarketVerse AI
Market Instrument Resolver

Purpose
-------
Provides one canonical place for converting a UI selection into a
normalized instrument identity before any market intelligence pipeline
is executed.

This module does NOT fetch market data and does NOT perform analysis.
CentralBrain remains responsible for orchestration.

It helps prevent stale stock symbols from being used after switching
to an MCX commodity (for example, Gold).

Version: 1.0
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class Instrument:
    """Normalized instrument identity used by the intelligence pipeline."""

    display_name: str
    symbol: str
    asset_type: str
    exchange: str
    provider_symbol: Optional[str] = None

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "display_name": self.display_name,
            "symbol": self.symbol,
            "asset_type": self.asset_type,
            "exchange": self.exchange,
            "provider_symbol": self.provider_symbol,
        }


class MarketInstrumentResolver:
    """
    Resolves a selected company or commodity into one normalized
    Instrument object.

    Important:
    Provider symbols vary by market-data provider. Commodity symbols
    should therefore be supplied through a mapping/configuration layer
    rather than guessed here.
    """

    def resolve_company(
        self,
        company_name: str,
        symbol: str,
        exchange: str = "NSE",
        provider_symbol: Optional[str] = None,
    ) -> Instrument:
        return Instrument(
            display_name=company_name,
            symbol=symbol,
            asset_type="EQUITY",
            exchange=exchange,
            provider_symbol=provider_symbol or symbol,
        )

    def resolve_commodity(
        self,
        commodity_name: str,
        symbol: str,
        exchange: str = "MCX",
        provider_symbol: Optional[str] = None,
    ) -> Instrument:
        return Instrument(
            display_name=commodity_name,
            symbol=symbol,
            asset_type="COMMODITY",
            exchange=exchange,
            provider_symbol=provider_symbol or symbol,
        )

    def resolve(
        self,
        display_name: str,
        symbol: str,
        asset_type: str,
        exchange: str,
        provider_symbol: Optional[str] = None,
    ) -> Instrument:
        asset_type = asset_type.upper()

        if asset_type == "COMMODITY":
            return self.resolve_commodity(
                commodity_name=display_name,
                symbol=symbol,
                exchange=exchange,
                provider_symbol=provider_symbol,
            )

        return self.resolve_company(
            company_name=display_name,
            symbol=symbol,
            exchange=exchange,
            provider_symbol=provider_symbol,
        )
