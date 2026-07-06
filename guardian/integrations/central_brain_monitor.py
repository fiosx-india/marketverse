"""
Guardian Integration
Central Brain Monitor
"""

import importlib


class CentralBrainMonitor:

    MODULES = [
        "modules.ai_engine",
        "modules.market_scanner",
        "modules.news",
        "modules.news_analysis",
        "modules.market_events",
        "modules.decision_core",
        "modules.pattern",
        "modules.technical",
        "modules.sentiment",
        "modules.volume_analysis",
        "modules.prediction",
        "modules.strategy",
        "modules.risk_manager",
        "modules.trade_executor",
        "modules.performance_tracker",
    ]

    def check(self):

        report = []

        for module in self.MODULES:

            item = {
                "module": module,
                "status": "OK",
                "message": ""
            }

            try:
                importlib.import_module(module)
                item["message"] = "Loaded successfully."

            except Exception as e:
                item["status"] = "ERROR"
                item["message"] = str(e)

            report.append(item)

        return report
