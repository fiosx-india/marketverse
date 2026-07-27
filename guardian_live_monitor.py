"""
Guardian Live Monitor
MarketVerse Guardian Monitoring Engine

Purpose:
- Track module status
- Record warnings and errors
- Show live health
- Future-ready monitoring engine
"""

from datetime import datetime


class GuardianLiveMonitor:
    def __init__(self):
        self.modules = {}

    def update(self, module, status, message=""):
        self.modules[module] = {
            "status": status,
            "message": message,
            "time": datetime.now().strftime("%H:%M:%S")
        }

    def ready(self, module):
        self.update(module, "READY", "Module running normally")

    def waiting(self, module, message="Waiting for data"):
        self.update(module, "WAITING", message)

    def warning(self, module, message):
        self.update(module, "WARNING", message)

    def error(self, module, message):
        self.update(module, "ERROR", message)

    def health(self):
        total = len(self.modules)

        if total == 0:
            return 100

        errors = sum(
            1 for m in self.modules.values()
            if m["status"] == "ERROR"
        )

        warnings = sum(
            1 for m in self.modules.values()
            if m["status"] == "WARNING"
        )

        score = max(
            0,
            100 - (errors * 20) - (warnings * 5)
        )

        return score

    def report(self):
        return {
            "health": self.health(),
            "modules": self.modules
        }


live_monitor = GuardianLiveMonitor()
