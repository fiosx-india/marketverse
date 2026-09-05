"""
=========================================================
MarketVerse AI
Core Package Tests
=========================================================

Tests the actual implementation of:

- core.__init__
- Bootstrap
- StartupManager
- MarketVerseEngine

Architecture:

Bootstrap
    ↓
Structure Validation
    ↓
MarketVerseEngine
    ↓
StartupManager
    ↓
Guardian
=========================================================
"""

import unittest
from unittest.mock import patch

from core import (
    Bootstrap,
    StartupManager,
    MarketVerseEngine
)


# =========================================================
# BOOTSTRAP TESTS
# =========================================================

class TestBootstrap(unittest.TestCase):
    """
    Test MarketVerse project bootstrap.
    """

    def setUp(self):

        self.bootstrap = Bootstrap()


    def test_bootstrap_initializes(self):

        self.assertIsNotNone(
            self.bootstrap
        )


    def test_project_root_exists(self):

        self.assertTrue(
            self.bootstrap.project_root.exists()
        )


    def test_project_root_is_directory(self):

        self.assertTrue(
            self.bootstrap.project_root.is_dir()
        )


    def test_check_structure_returns_dictionary(self):

        result = self.bootstrap.check_structure()

        self.assertIsInstance(
            result,
            dict
        )


    def test_check_structure_has_success(self):

        result = self.bootstrap.check_structure()

        self.assertIn(
            "success",
            result
        )


    def test_check_structure_has_missing(self):

        result = self.bootstrap.check_structure()

        self.assertIn(
            "missing",
            result
        )


    def test_missing_is_list(self):

        result = self.bootstrap.check_structure()

        self.assertIsInstance(
            result["missing"],
            list
        )


    def test_success_is_boolean(self):

        result = self.bootstrap.check_structure()

        self.assertIsInstance(
            result["success"],
            bool
        )


    def test_initialize_returns_dictionary(self):

        result = self.bootstrap.initialize()

        self.assertIsInstance(
            result,
            dict
        )


    def test_initialize_has_status(self):

        result = self.bootstrap.initialize()

        self.assertIn(
            "status",
            result
        )


    def test_initialize_has_message(self):

        result = self.bootstrap.initialize()

        self.assertIn(
            "message",
            result
        )


    def test_initialize_status_is_valid(self):

        result = self.bootstrap.initialize()

        self.assertIn(

            result["status"],

            (
                "READY",
                "ERROR"
            )

        )


    def test_successful_initialize_has_ready_status(self):

        with patch.object(

            self.bootstrap,

            "check_structure",

            return_value={

                "success": True,

                "missing": []

            }

        ):

            result = self.bootstrap.initialize()

        self.assertEqual(
            result["status"],
            "READY"
        )

        self.assertEqual(

            result["message"],

            "MarketVerse initialized successfully."

        )


    def test_failed_initialize_has_error_status(self):

        missing_components = [

            "modules",

            "requirements.txt"

        ]

        with patch.object(

            self.bootstrap,

            "check_structure",

            return_value={

                "success": False,

                "missing": missing_components

            }

        ):

            result = self.bootstrap.initialize()

        self.assertEqual(
            result["status"],
            "ERROR"
        )

        self.assertEqual(

            result["message"],

            "Missing project components."

        )

        self.assertEqual(

            result["missing"],

            missing_components

        )


# =========================================================
# STARTUP MANAGER TESTS
# =========================================================

class TestStartupManager(unittest.TestCase):
    """
    Test application startup behaviour.
    """

    def setUp(self):

        self.startup = StartupManager()


    def test_startup_manager_initializes(self):

        self.assertIsNotNone(
            self.startup
        )


    @patch(
        "core.startup.run_guardian"
    )
    def test_start_runs_guardian(

        self,

        mock_run_guardian

    ):

        guardian_result = {

            "status": "OK"

        }

        mock_run_guardian.return_value = (

            guardian_result

        )

        result = self.startup.start()

        mock_run_guardian.assert_called_once()


        self.assertIsInstance(
            result,
            dict
        )


        self.assertEqual(

            result["status"],

            "READY"

        )


        self.assertEqual(

            result["guardian"],

            guardian_result

        )


    @patch(
        "core.startup.run_guardian"
    )
    def test_start_has_expected_message(

        self,

        mock_run_guardian

    ):

        mock_run_guardian.return_value = {}

        result = self.startup.start()

        self.assertEqual(

            result["message"],

            "Startup completed successfully."

        )


    @patch(
        "core.startup.run_guardian"
    )
    def test_guardian_report_is_preserved(

        self,

        mock_run_guardian

    ):

        guardian_report = {

            "report": {

                "health_score": 100

            },

            "advice": []

        }

        mock_run_guardian.return_value = (

            guardian_report

        )

        result = self.startup.start()

        self.assertEqual(

            result["guardian"],

            guardian_report

        )


# =========================================================
# MARKETVERSE ENGINE TESTS
# =========================================================

class TestMarketVerseEngine(unittest.TestCase):
    """
    Test main core engine.
    """

    def setUp(self):

        self.engine = MarketVerseEngine()


    def test_engine_initializes(self):

        self.assertIsNotNone(
            self.engine
        )


    def test_engine_has_bootstrap(self):

        self.assertTrue(

            hasattr(

                self.engine,

                "bootstrap"

            )

        )


    def test_engine_has_startup(self):

        self.assertTrue(

            hasattr(

                self.engine,

                "startup"

            )

        )


    def test_bootstrap_is_bootstrap_instance(self):

        self.assertIsInstance(

            self.engine.bootstrap,

            Bootstrap

        )


    def test_startup_is_startup_manager_instance(self):

        self.assertIsInstance(

            self.engine.startup,

            StartupManager

        )


    def test_engine_stops_when_bootstrap_fails(self):

        failure_result = {

            "status": "ERROR",

            "message": "Missing project components.",

            "missing": [

                "modules"

            ]

        }

        with patch.object(

            self.engine.bootstrap,

            "initialize",

            return_value=failure_result

        ):

            with patch.object(

                self.engine.startup,

                "start"

            ) as mock_start:

                result = self.engine.run()


        self.assertEqual(

            result,

            failure_result

        )


        mock_start.assert_not_called()


    def test_engine_runs_startup_when_bootstrap_ready(self):

        bootstrap_result = {

            "status": "READY",

            "message": "MarketVerse initialized successfully."

        }


        startup_result = {

            "status": "READY",

            "message": "Startup completed successfully."

        }


        with patch.object(

            self.engine.bootstrap,

            "initialize",

            return_value=bootstrap_result

        ):

            with patch.object(

                self.engine.startup,

                "start",

                return_value=startup_result

            ) as mock_start:

                result = self.engine.run()


        mock_start.assert_called_once()


        self.assertEqual(

            result["bootstrap"],

            bootstrap_result

        )


        self.assertEqual(

            result["startup"],

            startup_result

        )


        self.assertEqual(

            result["status"],

            "ONLINE"

        )


    def test_engine_online_status_after_successful_run(self):

        with patch.object(

            self.engine.bootstrap,

            "initialize",

            return_value={

                "status": "READY"

            }

        ):

            with patch.object(

                self.engine.startup,

                "start",

                return_value={

                    "status": "READY"

                }

            ):

                result = self.engine.run()


        self.assertEqual(

            result["status"],

            "ONLINE"

        )


# =========================================================
# CORE PACKAGE IMPORT TESTS
# =========================================================

class TestCorePackage(unittest.TestCase):
    """
    Test core package exports.
    """

    def test_bootstrap_import(self):

        self.assertIsNotNone(
            Bootstrap
        )


    def test_startup_manager_import(self):

        self.assertIsNotNone(
            StartupManager
        )


    def test_engine_import(self):

        self.assertIsNotNone(
            MarketVerseEngine
        )


    def test_core_classes_are_callable(self):

        self.assertTrue(
            callable(Bootstrap)
        )

        self.assertTrue(
            callable(StartupManager)
        )

        self.assertTrue(
            callable(MarketVerseEngine)
        )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
        )
