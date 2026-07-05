import os
import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
MODULES_DIR = PROJECT_ROOT

def run_guardian():

    report = []

    for file in MODULES_DIR.glob("*.py"):

        if file.name == "guardian.py":
            continue

        try:
            source = file.read_text(encoding="utf-8")
            ast.parse(source)

            report.append(
                {
                    "file": file.name,
                    "status": "OK"
                }
            )

        except SyntaxError as e:

            report.append(
                {
                    "file": file.name,
                    "status": "ERROR",
                    "line": e.lineno,
                    "message": e.msg
                }
            )

    return report
