import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_guardian():

    report = []

    for file in PROJECT_ROOT.rglob("*.py"):

        if "__pycache__" in str(file):
            continue

        try:
            source = file.read_text(encoding="utf-8")
            ast.parse(source)

            report.append({
                "file": str(file.relative_to(PROJECT_ROOT)),
                "status": "OK"
            })

        except SyntaxError as e:

            report.append({
                "file": str(file.relative_to(PROJECT_ROOT)),
                "status": "ERROR",
                "line": e.lineno,
                "message": e.msg
            })

    return report
