"""
MarketVerse Core
startup.py

Purpose:
Startup manager for MarketVerse.
"""

from guardian import run_guardian


class StartupManager:
    """Handles application startup."""

    def start(self):

        # Run Guardian before startup
        guardian_report = run_guardian()

        return {
            "status": "READY",
            "message": "Startup completed successfully.",
            "guardian": guardian_report
        }
