"""
MarketVerse Core Package

Core engine initialization.
"""

from .bootstrap import Bootstrap
from .startup import StartupManager
from .engine import MarketVerseEngine
from marketverse.guardian import GuardianController
__all__ = [
    "Bootstrap",
    "StartupManager",
    "MarketVerseEngine",
]
def run_guardian():
    """Run Guardian system checks."""

    controller = GuardianController()

    return controller.run()

self.advisor = GuardianAdvisor()
self.import_checker = ImportChecker()
self.notifier = Notifier()
