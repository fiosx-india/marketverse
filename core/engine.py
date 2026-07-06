"""
MarketVerse Core
startup.py

Purpose:
Manage MarketVerse startup sequence.
"""

from datetime import datetime


class StartupManager:
    """Handles application startup."""

    def __init__(self):
        self.started_at = None

    def start(self):
        self.started_at = datetime.now()

        return {
            "status": "RUNNING",
            "started_at": self.started_at.strftime("%Y-%m-%d %H:%M:%S"),
            "message": "MarketVerse startup completed successfully."
        }

    def uptime(self):
        if self.started_at is None:
            return "Application has not started."

        elapsed = datetime.now() - self.started_at
        return str(elapsed)
