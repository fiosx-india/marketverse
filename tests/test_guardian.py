"""
=========================================================
MarketVerse AI
Guardian Tests
=========================================================

Tests the actual Guardian infrastructure.

Coverage:
- Guardian package imports
- GuardianController initialization
- GuardianController integration monitors
- HealthMonitor
- HealthReport
- ProjectRegistry
- ModuleInfo
- RuntimeDiagnostic
- Symbol validation
- Signal validation
- Runtime errors and warnings
- Root cause analysis
- Health score
- Summary
=========================================================
"""

import unittest
import tempfile
from pathlib import Path

from guardian import (
    GuardianController,
    HealthMonitor,
    ProjectRegistry,
    ModuleInfo,
    run_guardian
)

from guardian.health import HealthReport
from guardian.runtime_diagnostic import RuntimeDiagnostic


# =========================================================
# TEST HELPERS
# =========================================================

class FakeValidationResult:
    """
    Minimal validation result compatible with HealthMonitor.
    """

    def __init__(
        self,
        valid=True,
        warnings=None
    ):

        self.valid = valid
        self.warnings = warnings or []


# =========================================================
# GUARDIAN PACKAGE TESTS
# =========================================================

class TestGuardianPackage(unittest.TestCase):

    def test_guardian_controller_imported(self):

        self.assertIsNotNone(
            GuardianController
        )

    def test_health_monitor_imported(self):

        self.assertIsNotNone(
            HealthMonitor
        )

    def test_project_registry_imported(self):

        self.assertIsNotNone(
            ProjectRegistry
        )

    def test_run_guardian_is_callable(self):

        self.assertTrue(
            callable(
                run_guardian
            )
        )


# =========================================================
# GUARDIAN CONTROLLER TESTS
# =========================================================

class TestGuardianController(unittest.TestCase):

    def setUp(self):

        self.guardian = GuardianController()

    def test_guardian_initializes(self):

        self.assertIsNotNone(
            self.guardian
        )

    def test_scanner_exists(self):

        self.assertTrue(
            hasattr(
                self.guardian,
                "scanner"
            )
        )

    def test_validator_exists(self):

        self.assertTrue(
            hasattr(
                self.guardian,
                "validator"
            )
        )

    def test_dependency_exists(self):

        self.assertTrue(
            hasattr(
                self.guardian,
                "dependency"
            )
        )

    def test_health_monitor_exists(self):

        self.assertTrue(
            hasattr(
                self.guardian,
                "health"
            )
        )

    def test_advisor_exists(self):

        self.assertTrue(
            hasattr(
                self.guardian,
                "advisor"
            )
        )

    def test_import_checker_exists(self):

        self.assertTrue(
            hasattr(
                self.guardian,
                "import_checker"
            )
        )


# =========================================================
# GUARDIAN INTEGRATION MONITOR TESTS
# =========================================================

class TestGuardianIntegrationMonitors(unittest.TestCase):

    def setUp(self):

        self.guardian = GuardianController()

    def test_app_monitor_exists(self):

        self.assertTrue(
            hasattr(
                self.guardian,
                "app_monitor"
            )
        )

    def test_system_monitor_exists(self):

        self.assertTrue(
            hasattr(
                self.guardian,
                "system_monitor"
            )
        )

    def test_central_brain_monitor_exists(self):

        self.assertTrue(
            hasattr(
                self.guardian,
                "central_brain_monitor"
            )
        )

    def test_dashboard_monitor_exists(self):

        self.assertTrue(
            hasattr(
                self.guardian,
                "dashboard_monitor"
            )
        )

    def test_app_monitor_has_check_method(self):

        self.assertTrue(
            callable(
                self.guardian.app_monitor.check
            )
        )

    def test_system_monitor_has_check_method(self):

        self.assertTrue(
            callable(
                self.guardian.system_monitor.check
            )
        )

    def test_central_brain_monitor_has_check_method(self):

        self.assertTrue(
            callable(
                self.guardian
                .central_brain_monitor
                .check
            )
        )

    def test_dashboard_monitor_has_check_method(self):

        self.assertTrue(
            callable(
                self.guardian
                .dashboard_monitor
                .check
            )
        )


# =========================================================
# GUARDIAN CONTROLLER RUNTIME TEST
# =========================================================

class TestGuardianControllerRun(unittest.TestCase):

    def test_guardian_runs_on_empty_project(self):

        guardian = GuardianController()

        with tempfile.TemporaryDirectory() as temp_dir:

            result = guardian.run(
                temp_dir
            )

        self.assertIsInstance(
            result,
            dict
        )

        self.assertIn(
            "report",
            result
        )

        self.assertIn(
            "advice",
            result
        )

        self.assertIn(
            "dependencies",
            result
        )

        self.assertIn(
            "validation_errors",
            result
        )

        self.assertIn(
            "integrations",
            result
        )

    def test_guardian_report_has_health_data(self):

        guardian = GuardianController()

        with tempfile.TemporaryDirectory() as temp_dir:

            result = guardian.run(
                temp_dir
            )

        report = result["report"]

        self.assertIsNotNone(
            report
        )

        self.assertTrue(
            hasattr(
                report,
                "health_score"
            )
        )

        self.assertTrue(
            hasattr(
                report,
                "status"
            )
        )


# =========================================================
# HEALTH MONITOR TESTS
# =========================================================

class TestHealthMonitor(unittest.TestCase):

    def setUp(self):

        self.monitor = HealthMonitor()

    def test_empty_project_health_score(self):

        report = self.monitor.generate(

            files=[],

            validation_results=[]

        )

        self.assertEqual(
            report.health_score,
            0
        )

    def test_empty_project_status_green(self):

        report = self.monitor.generate(

            files=[],

            validation_results=[]

        )

        self.assertEqual(
            report.status,
            "GREEN"
        )

    def test_all_valid_files(self):

        files = [

            "file1.py",

            "file2.py",

            "file3.py"

        ]

        results = [

            FakeValidationResult(True),

            FakeValidationResult(True),

            FakeValidationResult(True)

        ]

        report = self.monitor.generate(

            files,

            results

        )

        self.assertEqual(
            report.files,
            3
        )

        self.assertEqual(
            report.valid_files,
            3
        )

        self.assertEqual(
            report.errors,
            0
        )

        self.assertEqual(
            report.health_score,
            100
        )

        self.assertEqual(
            report.status,
            "GREEN"
        )

    def test_one_invalid_file(self):

        files = [

            "file1.py",

            "file2.py"

        ]

        results = [

            FakeValidationResult(True),

            FakeValidationResult(False)

        ]

        report = self.monitor.generate(

            files,

            results

        )

        self.assertEqual(
            report.errors,
            1
        )

        self.assertEqual(
            report.status,
            "YELLOW"
        )

    def test_many_invalid_files(self):

        files = [

            "a.py",

            "b.py",

            "c.py",

            "d.py",

            "e.py"

        ]

        results = [

            FakeValidationResult(False),

            FakeValidationResult(False),

            FakeValidationResult(False),

            FakeValidationResult(False),

            FakeValidationResult(False)

        ]

        report = self.monitor.generate(

            files,

            results

        )

        self.assertEqual(
            report.errors,
            5
        )

        self.assertEqual(
            report.status,
            "RED"
        )

    def test_warning_count(self):

        files = [

            "a.py",

            "b.py"

        ]

        results = [

            FakeValidationResult(

                True,

                warnings=[
                    "warning1",
                    "warning2"
                ]

            ),

            FakeValidationResult(

                True,

                warnings=[
                    "warning3"
                ]

            )

        ]

        report = self.monitor.generate(

            files,

            results

        )

        self.assertEqual(
            report.warnings,
            3
        )

    def test_integration_status_is_preserved(self):

        integration_status = {

            "app": {

                "status": "OK"

            }

        }

        report = self.monitor.generate(

            files=[],

            validation_results=[],

            integration_status=integration_status

        )

        self.assertEqual(

            report.integration_status,

            integration_status

        )


# =========================================================
# HEALTH REPORT TESTS
# =========================================================

class TestHealthReport(unittest.TestCase):

    def test_health_report_fields(self):

        report = HealthReport(

            status="GREEN",

            files=10,

            valid_files=10,

            errors=0,

            warnings=0,

            health_score=100,

            last_scan="2026-01-01T00:00:00",

            integration_status={}

        )

        self.assertEqual(
            report.status,
            "GREEN"
        )

        self.assertEqual(
            report.files,
            10
        )

        self.assertEqual(
            report.health_score,
            100
        )


# =========================================================
# PROJECT REGISTRY TESTS
# =========================================================

class TestProjectRegistry(unittest.TestCase):

    def setUp(self):

        self.registry = ProjectRegistry()

    def test_registry_starts_empty(self):

        modules = self.registry.all_modules()

        self.assertEqual(
            modules,
            []
        )

    def test_register_module(self):

        module = ModuleInfo(

            name="RiskManager",

            path="modules/risk_manager.py",

            purpose="Risk management"

        )

        self.registry.register(
            module
        )

        result = self.registry.get(
            "RiskManager"
        )

        self.assertIsNotNone(
            result
        )

        self.assertEqual(

            result.name,

            "RiskManager"

        )

    def test_register_updates_existing_module(self):

        module1 = ModuleInfo(

            name="Prediction",

            path="modules/prediction.py",

            version="1.0.0"

        )

        module2 = ModuleInfo(

            name="Prediction",

            path="modules/prediction.py",

            version="2.0.0"

        )

        self.registry.register(
            module1
        )

        self.registry.register(
            module2
        )

        result = self.registry.get(
            "Prediction"
        )

        self.assertEqual(

            result.version,

            "2.0.0"

        )

    def test_get_missing_module(self):

        result = self.registry.get(
            "UNKNOWN"
        )

        self.assertIsNone(
            result
        )

    def test_all_modules(self):

        self.registry.register(

            ModuleInfo(

                name="ModuleA",

                path="a.py"

            )

        )

        self.registry.register(

            ModuleInfo(

                name="ModuleB",

                path="b.py"

            )

        )

        modules = self.registry.all_modules()

        self.assertEqual(

            len(modules),

            2

        )

    def test_remove_module(self):

        self.registry.register(

            ModuleInfo(

                name="ModuleA",

                path="a.py"

            )

        )

        self.registry.remove(
            "ModuleA"
        )

        result = self.registry.get(
            "ModuleA"
        )

        self.assertIsNone(
            result
        )

    def test_remove_missing_module_does_not_crash(self):

        self.registry.remove(
            "UNKNOWN"
        )

        self.assertEqual(

            self.registry.all_modules(),

            []

        )


# =========================================================
# RUNTIME DIAGNOSTIC TESTS
# =========================================================

class TestRuntimeDiagnostic(unittest.TestCase):

    def setUp(self):

        self.diagnostic = RuntimeDiagnostic()

    def test_starts_empty(self):

        summary = self.diagnostic.summary()

        self.assertEqual(

            summary["events"],

            0

        )

        self.assertEqual(

            summary["warnings"],

            0

        )

        self.assertEqual(

            summary["errors"],

            0

        )

        self.assertEqual(

            summary["health"],

            100

        )

    def test_trace_event(self):

        self.diagnostic.trace(

            name="price",

            value=100,

            source="test"

        )

        summary = self.diagnostic.summary()

        self.assertEqual(

            summary["events"],

            1

        )

    def test_function_event(self):

        self.diagnostic.function(

            file="test.py",

            function="test_function"

        )

        summary = self.diagnostic.summary()

        self.assertEqual(

            summary["events"],

            1

        )

    def test_warning(self):

        self.diagnostic.warning(

            file="test.py",

            function="test",

            message="Test warning"

        )

        summary = self.diagnostic.summary()

        self.assertEqual(

            summary["warnings"],

            1

        )

        self.assertEqual(

            summary["health"],

            98

        )

    def test_error(self):

        try:

            raise ValueError(
                "Test error"
            )

        except ValueError as error:

            self.diagnostic.error(

                file="test.py",

                function="test",

                error=error

            )

        summary = self.diagnostic.summary()

        self.assertEqual(

            summary["errors"],

            1

        )

        self.assertEqual(

            summary["health"],

            90

        )


# =========================================================
# SYMBOL VALIDATION TESTS
# =========================================================

class TestGuardianSymbolValidation(unittest.TestCase):

    def setUp(self):

        self.diagnostic = RuntimeDiagnostic()

    def test_valid_symbol(self):

        valid, message = (

            self.diagnostic.validate_symbol(

                "RELIANCE"

            )

        )

        self.assertTrue(
            valid
        )

        self.assertEqual(

            message,

            "Valid"

        )

    def test_none_symbol(self):

        valid, message = (

            self.diagnostic.validate_symbol(

                None

            )

        )

        self.assertFalse(
            valid
        )

        self.assertEqual(

            message,

            "Symbol is None"

        )

    def test_empty_symbol(self):

        valid, message = (

            self.diagnostic.validate_symbol(

                ""

            )

        )

        self.assertFalse(
            valid
        )

        self.assertEqual(

            message,

            "Empty Symbol"

        )

    def test_sector_is_rejected(self):

        valid, message = (

            self.diagnostic.validate_symbol(

                "BANKING"

            )

        )

        self.assertFalse(
            valid
        )

        self.assertIn(

            "Sector Name",

            message

        )

    def test_sector_validation_is_case_insensitive(self):

        valid, message = (

            self.diagnostic.validate_symbol(

                "it"

            )

        )

        self.assertFalse(
            valid
        )

        self.assertIn(

            "Sector Name",

            message

        )


# =========================================================
# SIGNAL VALIDATION TESTS
# =========================================================

class TestGuardianSignalValidation(unittest.TestCase):

    def setUp(self):

        self.diagnostic = RuntimeDiagnostic()

    def test_bullish_buy_signal(self):

        report = (

            self.diagnostic.validate_signal(

                symbol="RELIANCE",

                ai_signal="BUY",

                news={

                    "sentiment": "BULLISH"

                },

                technical={

                    "trend": "STRONG_BULLISH"

                },

                prediction={

                    "direction": "BULLISH"

                },

                volume_alert=True

            )

        )

        self.assertEqual(

            report["symbol"],

            "RELIANCE"

        )

        self.assertEqual(

            report["signal"],

            "BUY"

        )

        self.assertGreaterEqual(

            report["score"],

            60

        )

    def test_bearish_news_conflicts_with_buy(self):

        report = (

            self.diagnostic.validate_signal(

                symbol="TEST",

                ai_signal="BUY",

                news={

                    "sentiment": "BEARISH"

                },

                technical={},

                prediction=None,

                volume_alert=False

            )

        )

        self.assertEqual(

            report["status"],

            "WEAK"

        )

        self.assertIn(

            "Bearish News",

            report["issues"]

        )

    def test_bullish_news_conflicts_with_sell(self):

        report = (

            self.diagnostic.validate_signal(

                symbol="TEST",

                ai_signal="SELL",

                news={

                    "sentiment": "BULLISH"

                },

                technical={},

                prediction=None,

                volume_alert=False

            )

        )

        self.assertEqual(

            report["status"],

            "WEAK"

        )

    def test_weak_signal(self):

        report = (

            self.diagnostic.validate_signal(

                symbol="TEST",

                ai_signal="HOLD",

                news={},

                technical={},

                prediction=None,

                volume_alert=False

            )

        )

        self.assertEqual(

            report["status"],

            "WEAK"

        )


# =========================================================
# ROOT CAUSE ANALYSIS TESTS
# =========================================================

class TestGuardianRootCause(unittest.TestCase):

    def setUp(self):

        self.diagnostic = RuntimeDiagnostic()

    def _add_error(

        self,

        message

    ):

        try:

            raise Exception(
                message
            )

        except Exception as error:

            self.diagnostic.error(

                file="test.py",

                function="test",

                error=error

            )

    def test_import_error_root_cause(self):

        self._add_error(

            "ImportError"

        )

        causes = (

            self.diagnostic.root_cause()

        )

        self.assertEqual(

            causes[0]["reason"],

            "Module Import Failed."

        )

    def test_key_error_root_cause(self):

        self._add_error(

            "KeyError"

        )

        causes = (

            self.diagnostic.root_cause()

        )

        self.assertEqual(

            causes[0]["reason"],

            "Dictionary key missing."

        )

    def test_attribute_error_root_cause(self):

        self._add_error(

            "AttributeError"

        )

        causes = (

            self.diagnostic.root_cause()

        )

        self.assertEqual(

            causes[0]["reason"],

            "Object attribute missing."

        )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )
