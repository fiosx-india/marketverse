"""
MarketVerse Core
engine.py

Purpose:
Core engine for MarketVerse.
"""

from .bootstrap import Bootstrap
from .startup import StartupManager


class MarketVerseEngine:
    """Main MarketVerse engine."""

    def __init__(self):
        self.bootstrap = Bootstrap()
        self.startup = StartupManager()

    def run(self):
        boot = self.bootstrap.initialize()

        if boot["status"] != "READY":
            return boot

        startup = self.startup.start()

        return {
            "bootstrap": boot,
            "startup": startup,
            "status": "ONLINE"
        }
