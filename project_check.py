"""
MarketVerse Project Checker
Part 1 - Core Scanner

Author: ChatGPT
"""

import ast
import os
from pathlib import Path
from datetime import datetime


class ProjectChecker:

    def __init__(self, root="."):
        self.root = Path(root)

        self.report = {
            "project": self.root.name,
            "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_files": 0,
            "python_files": [],
            "errors": [],
            "warnings": [],
            "info": [],
            "health": 100,
        }

    # ---------------------------------------------------
    # Scan Project
    # ---------------------------------------------------

    def scan(self):

        print("=" * 60)
        print(" MARKETVERSE PROJECT CHECKER ")
        print("=" * 60)

        for path in self.root.rglob("*.py"):

            if "__pycache__" in str(path):
                continue

            if ".git" in str(path):
                continue

            self.report["python_files"].append(path)
            self.report["total_files"] += 1

            self.check_empty(path)
            self.check_syntax(path)

        print(f"Python Files : {self.report['total_files']}")
        print()

    # ---------------------------------------------------
    # Empty File
    # ---------------------------------------------------

    def check_empty(self, file):

        try:

            if file.stat().st_size == 0:

                self.report["warnings"].append({
                    "file": str(file),
                    "type": "Empty File"
                })

                self.report["health"] -= 2

        except Exception as e:

            self.report["errors"].append({
                "file": str(file),
                "error": str(e)
            })

    # ---------------------------------------------------
    # Syntax Checker
    # ---------------------------------------------------

    def check_syntax(self, file):

        try:

            source = file.read_text(encoding="utf-8")

            ast.parse(source)

        except SyntaxError as e:

            self.report["errors"].append({

                "file": str(file),
                "line": e.lineno,
                "type": "Syntax Error",
                "message": e.msg

            })

            self.report["health"] -= 5

        except Exception as e:

            self.report["errors"].append({

                "file": str(file),
                "type": "Read Error",
                "message": str(e)

            })

            self.report["health"] -= 2

    # ---------------------------------------------------
    # Print Report
    # ---------------------------------------------------

    def show(self):

        print("=" * 60)
        print("SCAN REPORT")
        print("=" * 60)

        print(f"Project        : {self.report['project']}")
        print(f"Files          : {self.report['total_files']}")
        print(f"Health Score   : {self.report['health']}%")
        print()

        print("ERRORS")

        if not self.report["errors"]:
            print("  None")

        for item in self.report["errors"]:
            print(item)

        print()

        print("WARNINGS")

        if not self.report["warnings"]:
            print("  None")

        for item in self.report["warnings"]:
            print(item)

        print()

        print("=" * 60)


if __name__ == "__main__":

    checker = ProjectChecker(".")

    checker.scan()

    checker.show()

# ---------------------------------------------------
# Import Checker
# ---------------------------------------------------

def check_imports(self):

    print("Checking imports...")

    for file in self.report["python_files"]:

        try:

            source = file.read_text(encoding="utf-8")

            tree = ast.parse(source)

            imports = []
            names = []

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:

                        imports.append(alias.name)

                elif isinstance(node, ast.ImportFrom):

                    if node.module:

                        imports.append(node.module)

            duplicate = []

            for item in imports:

                if item in names:
                    duplicate.append(item)

                else:
                    names.append(item)

            if duplicate:

                self.report["warnings"].append({

                    "file": str(file),
                    "type": "Duplicate Import",
                    "imports": duplicate

                })

                self.report["health"] -= 1

            for module in imports:

                try:

                    __import__(module.split(".")[0])

                except Exception:

                    self.report["errors"].append({

                        "file": str(file),
                        "type": "Missing Module",
                        "module": module

                    })

                    self.report["health"] -= 2

        except Exception as e:

            self.report["errors"].append({

                "file": str(file),
                "type": "Import Scan Error",
                "message": str(e)

            })


# ---------------------------------------------------
# File Statistics
# ---------------------------------------------------

def file_statistics(self):

    print("Collecting statistics...")

    total_lines = 0

    for file in self.report["python_files"]:

        try:

            lines = file.read_text(
                encoding="utf-8",
                errors="ignore"
            ).splitlines()

            count = len(lines)

            total_lines += count

            if count == 0:

                continue

            if count > 800:

                self.report["warnings"].append({

                    "file": str(file),
                    "type": "Large File",
                    "lines": count

                })

        except:

            pass

    self.report["info"].append({

        "Total Lines": total_lines

    })

# ---------------------------------------------------
# Code Quality Checker
# ---------------------------------------------------

def check_code_quality(self):

    print("Checking code quality...")

    function_names = {}

    for file in self.report["python_files"]:

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            # TODO / FIXME
            for line_no, line in enumerate(source.splitlines(), start=1):

                text = line.upper()

                if "TODO" in text or "FIXME" in text:

                    self.report["warnings"].append({

                        "file": str(file),
                        "line": line_no,
                        "type": "TODO/FIXME",
                        "text": line.strip()

                    })

            tree = ast.parse(source)

            for node in ast.walk(tree):

                # Duplicate function names
                if isinstance(node, ast.FunctionDef):

                    if node.name not in function_names:
                        function_names[node.name] = []

                    function_names[node.name].append(str(file))

                    # Empty function
                    if len(node.body) == 1:

                        stmt = node.body[0]

                        if isinstance(stmt, ast.Pass):

                            self.report["warnings"].append({

                                "file": str(file),
                                "line": node.lineno,
                                "type": "Empty Function",
                                "name": node.name

                            })

                # Empty class
                if isinstance(node, ast.ClassDef):

                    if len(node.body) == 1:

                        stmt = node.body[0]

                        if isinstance(stmt, ast.Pass):

                            self.report["warnings"].append({

                                "file": str(file),
                                "line": node.lineno,
                                "type": "Empty Class",
                                "name": node.name

                            })

        except Exception as e:

            self.report["errors"].append({

                "file": str(file),
                "type": "Quality Scan Error",
                "message": str(e)

            })

    # Duplicate function report
    for name, files in function_names.items():

        if len(files) > 1:

            self.report["warnings"].append({

                "type": "Duplicate Function Name",
                "function": name,
                "files": files

            })

            self.report["health"] -= 1


# ---------------------------------------------------
# AI Recommendation Engine
# ---------------------------------------------------

def ai_recommendations(self):

    recommendations = []

    if self.report["errors"]:

        recommendations.append(
            "Fix all syntax and import errors before deployment."
        )

    if self.report["health"] < 80:

        recommendations.append(
            "Project health is below 80%. Review warnings carefully."
        )

    if len(self.report["warnings"]) > 10:

        recommendations.append(
            "Large number of warnings detected. Consider code cleanup."
        )

    if not recommendations:

        recommendations.append(
            "Project looks healthy. Continue development."
        )

    self.report["recommendations"] = recommendations

# ---------------------------------------------------
# Save Reports
# ---------------------------------------------------

import json

def save_reports(self):

    print("Saving reports...")

    report_dir = self.root / "reports"
    report_dir.mkdir(exist_ok=True)

    # JSON Report
    json_report = {
        "project": self.report["project"],
        "scan_time": self.report["scan_time"],
        "health": self.report["health"],
        "total_files": self.report["total_files"],
        "errors": self.report["errors"],
        "warnings": self.report["warnings"],
        "info": self.report["info"],
        "recommendations": self.report.get("recommendations", [])
    }

    with open(report_dir / "project_report.json",
              "w",
              encoding="utf-8") as f:

        json.dump(json_report, f, indent=4)

    # Text Report
    with open(report_dir / "project_report.txt",
              "w",
              encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write("MARKETVERSE PROJECT REPORT\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Project : {self.report['project']}\n")
        f.write(f"Health  : {self.report['health']}%\n")
        f.write(f"Files   : {self.report['total_files']}\n\n")

        f.write("ERRORS\n")
        f.write("-" * 60 + "\n")

        if self.report["errors"]:
            for item in self.report["errors"]:
                f.write(str(item) + "\n")
        else:
            f.write("None\n")

        f.write("\nWARNINGS\n")
        f.write("-" * 60 + "\n")

        if self.report["warnings"]:
            for item in self.report["warnings"]:
                f.write(str(item) + "\n")
        else:
            f.write("None\n")

        f.write("\nRECOMMENDATIONS\n")
        f.write("-" * 60 + "\n")

        for item in self.report.get("recommendations", []):
            f.write("- " + item + "\n")

    print("Reports saved in reports/")

# ---------------------------------------------------
# Dependency Checker
# ---------------------------------------------------

def dependency_summary(self):

    dependency_count = {}

    for file in self.report["python_files"]:

        try:
            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:

                        name = alias.name.split(".")[0]

                        dependency_count[name] = (
                            dependency_count.get(name, 0) + 1
                        )

                elif isinstance(node, ast.ImportFrom):

                    if node.module:

                        name = node.module.split(".")[0]

                        dependency_count[name] = (
                            dependency_count.get(name, 0) + 1
                        )

        except Exception:
            pass

    self.report["info"].append({
        "Dependencies": dependency_count
    })


# ---------------------------------------------------
# Project Readiness
# ---------------------------------------------------

def project_status(self):

    health = self.report["health"]
    errors = len(self.report["errors"])

    if errors > 0:
        status = "NEEDS FIXES"

    elif health >= 95:
        status = "PRODUCTION READY"

    elif health >= 85:
        status = "GOOD"

    elif health >= 70:
        status = "FAIR"

    else:
        status = "NEEDS IMPROVEMENT"

    self.report["status"] = status


# ---------------------------------------------------
# Final Summary
# ---------------------------------------------------

def final_summary(self):

    print("=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)

    print(f"Project       : {self.report['project']}")
    print(f"Health Score  : {self.report['health']}%")
    print(f"Status        : {self.report['status']}")
    print(f"Files Scanned : {self.report['total_files']}")
    print(f"Errors        : {len(self.report['errors'])}")
    print(f"Warnings      : {len(self.report['warnings'])}")

    print("=" * 60)

# ---------------------------------------------------
# Advanced Import Analysis
# Phase 2 - Part 6
# ---------------------------------------------------

def advanced_import_analysis(self):

    print("Running Advanced Import Analysis...")

    import_map = {}

    for file in self.report["python_files"]:

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            current = file.stem

            import_map[current] = []

            for node in ast.walk(tree):

                # import x
                if isinstance(node, ast.Import):

                    for alias in node.names:

                        name = alias.name.split(".")[0]

                        import_map[current].append(name)

                # from x import y
                elif isinstance(node, ast.ImportFrom):

                    # Wildcard import
                    if any(a.name == "*" for a in node.names):

                        self.report["warnings"].append({

                            "file": str(file),
                            "line": node.lineno,
                            "type": "Wildcard Import",
                            "module": node.module

                        })

                        self.report["health"] -= 1

                    # Relative import
                    if node.level > 0:

                        self.report["warnings"].append({

                            "file": str(file),
                            "line": node.lineno,
                            "type": "Relative Import",
                            "module": node.module

                        })

                    if node.module:

                        import_map[current].append(
                            node.module.split(".")[0]
                        )

        except Exception as e:

            self.report["errors"].append({

                "file": str(file),
                "type": "Import Analysis Error",
                "message": str(e)

            })

    # -------------------------------
    # Circular Import Detection
    # -------------------------------

    checked = set()

    for module, deps in import_map.items():

        for dep in deps:

            if dep in import_map:

                if module in import_map.get(dep, []):

                    key = tuple(sorted([module, dep]))

                    if key not in checked:

                        checked.add(key)

                        self.report["warnings"].append({

                            "type": "Circular Import",
                            "module1": module,
                            "module2": dep

                        })

                        self.report["health"] -= 3

    self.report["info"].append({

        "Import Map": import_map

    })

# ---------------------------------------------------
# Advanced Code Analyzer
# Phase 2 - Part 7
# ---------------------------------------------------

def advanced_code_analysis(self):

    print("Running Advanced Code Analysis...")

    functions = {}
    classes = {}
    called_functions = set()

    for file in self.report["python_files"]:

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            for node in ast.walk(tree):

                # Function definitions
                if isinstance(node, ast.FunctionDef):

                    functions.setdefault(node.name, []).append({
                        "file": str(file),
                        "line": node.lineno,
                        "lines": (
                            getattr(node, "end_lineno", node.lineno)
                            - node.lineno + 1
                        )
                    })

                    # Very long function
                    if getattr(node, "end_lineno", node.lineno) - node.lineno > 80:

                        self.report["warnings"].append({

                            "file": str(file),
                            "line": node.lineno,
                            "type": "Long Function",
                            "name": node.name

                        })

                # Class definitions
                elif isinstance(node, ast.ClassDef):

                    classes.setdefault(node.name, []).append({
                        "file": str(file),
                        "line": node.lineno
                    })

                # Function calls
                elif isinstance(node, ast.Call):

                    if isinstance(node.func, ast.Name):
                        called_functions.add(node.func.id)

                    elif isinstance(node.func, ast.Attribute):
                        called_functions.add(node.func.attr)

        except Exception as e:

            self.report["errors"].append({

                "file": str(file),
                "type": "Advanced Analysis Error",
                "message": str(e)

            })

    # -----------------------------------------
    # Duplicate Classes
    # -----------------------------------------

    for cls, locations in classes.items():

        if len(locations) > 1:

            self.report["warnings"].append({

                "type": "Duplicate Class",
                "class": cls,
                "locations": locations

            })

            self.report["health"] -= 1

    # -----------------------------------------
    # Unused Functions
    # -----------------------------------------

    for func, locations in functions.items():

        if func.startswith("__"):
            continue

        if func not in called_functions:

            self.report["warnings"].append({

                "type": "Unused Function",
                "function": func,
                "locations": locations

            })

    # Save statistics
    self.report["info"].append({

        "Functions": len(functions),
        "Classes": len(classes),
        "Called Functions": len(called_functions)

    })
# ---------------------------------------------------
# Security Analyzer
# Phase 2 - Part 8
# ---------------------------------------------------

def security_analysis(self):

    print("Running Security Analysis...")

    import re

    dangerous_calls = {
        "eval",
        "exec",
        "compile",
        "os.system",
        "subprocess.call",
        "subprocess.Popen",
        "pickle.loads"
    }

    secret_patterns = [
        r"AKIA[0-9A-Z]{16}",              # AWS Key
        r"AIza[0-9A-Za-z\-_]{35}",        # Google API
        r"sk-[A-Za-z0-9]{20,}",           # OpenAI Style Key
        r"ghp_[A-Za-z0-9]{20,}",          # GitHub Token
    ]

    for file in self.report["python_files"]:

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            # ----------------------------------
            # Hardcoded Secrets
            # ----------------------------------

            for line_no, line in enumerate(
                source.splitlines(),
                start=1
            ):

                for pattern in secret_patterns:

                    if re.search(pattern, line):

                        self.report["errors"].append({

                            "file": str(file),
                            "line": line_no,
                            "type": "Possible Secret",
                            "text": line.strip()

                        })

                        self.report["health"] -= 5

            # ----------------------------------
            # Dangerous Functions
            # ----------------------------------

            for node in ast.walk(tree):

                if isinstance(node, ast.Call):

                    call_name = ""

                    if isinstance(node.func, ast.Name):
                        call_name = node.func.id

                    elif isinstance(node.func, ast.Attribute):

                        if isinstance(node.func.value, ast.Name):

                            call_name = (
                                node.func.value.id
                                + "."
                                + node.func.attr
                            )

                    if call_name in dangerous_calls:

                        self.report["warnings"].append({

                            "file": str(file),
                            "line": node.lineno,
                            "type": "Dangerous Call",
                            "function": call_name

                        })

                        self.report["health"] -= 2

        except Exception as e:

            self.report["errors"].append({

                "file": str(file),
                "type": "Security Scan Error",
                "message": str(e)

            })

