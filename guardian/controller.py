"""
MarketVerse Guardian
controller.py

Purpose:
Coordinate all Guardian components.
"""

from .scanner import ProjectScanner
from .validator import ProjectValidator
from .dependency import DependencyAnalyzer
from .health import HealthMonitor
from .advisor import GuardianAdvisor
from .import_checker import ImportChecker

# ==========================
# Integration Monitors
# ==========================
from .integrations.app_monitor import AppMonitor
from .integrations.system_monitor import SystemMonitor
from .integrations.central_brain_monitor import CentralBrainMonitor
from .integrations.dashboard_monitor import DashboardMonitor


class GuardianController:

    def __init__(self):

        # Existing Guardian Components
        self.scanner = ProjectScanner()
        self.validator = ProjectValidator()
        self.dependency = DependencyAnalyzer()
        self.health = HealthMonitor()
        self.advisor = GuardianAdvisor()
        self.import_checker = ImportChecker()

        # Integration Monitors
        self.app_monitor = AppMonitor()
        self.system_monitor = SystemMonitor()
        self.central_brain_monitor = CentralBrainMonitor()
        self.dashboard_monitor = DashboardMonitor()

    def run(self, root="."):

        files = self.scanner.scan(root)

        results = []
        dependencies = {}
        validation_errors = []

        for file in files:

            result = self.validator.validate(file)
            results.append(result)

            if not result.valid:
                validation_errors.append({
                    "file": str(file),
                    "error": result.error
                })

            imports = self.dependency.analyze(file)

            dependencies[str(file)] = {
                "imports": imports,
                "check": self.import_checker.check(imports)
            }

        report = self.health.generate(
            files,
            results
        )

        advice = self.advisor.advise(report)

        # ==========================
        # Integration Health Report
        # ==========================
        integration_report = {
            "app": self.app_monitor.check(),
            "system": self.system_monitor.check(),
            "central_brain": self.central_brain_monitor.check(),
            "dashboard": self.dashboard_monitor.check()
        }

        return {
            "report": report,
            "advice": advice,
            "dependencies": dependencies,
            "validation_errors": validation_errors,
            "integrations": integration_report
        }
