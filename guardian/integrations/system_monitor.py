"""
Guardian Integration
System Monitor
"""

import importlib


class SystemMonitor:

    MODULES = [
        "modules.system_manager",
        "modules.system_controller",
        "modules.central_brain",
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
