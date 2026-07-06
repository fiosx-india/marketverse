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

        except Exception as e:

            report.append({
                "file": str(file.relative_to(PROJECT_ROOT)),
                "status": "ERROR",
                "message": str(e)
            })

    return {
        "status": "OK" if all(r["status"] == "OK" for r in report) else "ERROR",
        "total_files": len(report),
        "errors": sum(1 for r in report if r["status"] == "ERROR"),
        "report": report
    }
