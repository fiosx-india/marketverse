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


class GuardianController:

    def __init__(self):
        self.scanner = ProjectScanner()
        self.validator = ProjectValidator()
        self.dependency = DependencyAnalyzer()
        self.health = HealthMonitor()
        self.advisor = GuardianAdvisor()

    def run(self, root="."):
        files = self.scanner.scan(root)

        results = [
            self.validator.validate(file)
            for file in files
        ]

        report = self.health.generate(
            files,
            results
        )

        advice = self.advisor.advise(report)

        return {
            "report": report,
            "advice": advice
        }
