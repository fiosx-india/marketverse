"""
Guardian Integration
Dashboard Monitor
"""

import importlib


class DashboardMonitor:

    MODULES = [
        "modules.dashboard_utils",
        "modules.performance_tracker",
        "modules.news",
        "modules.market_scanner",
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
