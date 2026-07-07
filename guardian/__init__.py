"""
MarketVerse Guardian

Guardian package initializer.
"""

from .controller import GuardianController
from .scanner import ProjectScanner
from .validator import ProjectValidator
from .dependency import DependencyAnalyzer
from .health import HealthMonitor
from .advisor import GuardianAdvisor
from .import_checker import ImportChecker
from .notifier import Notifier
from .registry import ProjectRegistry, ModuleInfo
from .registry_sync import RegistrySync

__all__ = [
    "GuardianController",
    "ProjectScanner",
    "ProjectValidator",
    "DependencyAnalyzer",
    "HealthMonitor",
    "GuardianAdvisor",
    "ImportChecker",
    "Notifier",
    "ProjectRegistry",
    "ModuleInfo",
    "RegistrySync",
]

__version__ = "2.0.0"
"notifications": notifications,
self.notifier = Notifier()
notifications = self.notifier.integration_notifications(integration_report)
notifications.append(
    self.notifier.guardian_summary(report)
)
