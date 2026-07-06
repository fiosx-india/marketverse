"""
Guardian Integration
App Monitor
"""

from pathlib import Path
import ast


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class AppMonitor:

    def __init__(self):
        self.app_file = PROJECT_ROOT / "app.py"

    def check(self):

        report = {
            "module": "app",
            "status": "OK",
            "exists": False,
            "syntax": False,
            "message": ""
        }

        # File Exists
        if not self.app_file.exists():
            report["status"] = "ERROR"
            report["message"] = "app.py not found"
            return report

        report["exists"] = True

        # Syntax Check
        try:
            source = self.app_file.read_text(encoding="utf-8")
            ast.parse(source)

            report["syntax"] = True
            report["message"] = "Application is healthy."

        except SyntaxError as e:

            report["status"] = "ERROR"
            report["message"] = (
                f"Syntax Error (Line {e.lineno}): {e.msg}"
            )

        return report
