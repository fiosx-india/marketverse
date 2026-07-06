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

class GuardianController:

    def __init__(self):
        self.scanner = ProjectScanner()
        self.validator = ProjectValidator()
        self.dependency = DependencyAnalyzer()
        self.health = HealthMonitor()
        self.advisor = GuardianAdvisor()

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

            dependencies[str(file)] = self.dependency.analyze(file)

        report = self.health.generate(
            files,
            results
        )

        advice = self.advisor.advise(report)

        return {
            "report": report,
            "advice": advice,
            "dependencies": dependencies,
            "validation_errors": validation_errors
        }
