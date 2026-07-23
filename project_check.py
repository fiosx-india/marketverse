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

        import time

        start_time = time.time()
        TIME_LIMIT = 15   # 15 seconds

        print("=" * 60)
        print(" MARKETVERSE PROJECT CHECKER ")
        print("=" * 60)

        IGNORE_FOLDERS = {
            "__pycache__",
            ".git",
            "venv",
            ".venv",
            "build",
            "dist",
            ".idea",
            ".vscode",
        }

        ALLOWED_TOP_LEVEL = {
            "modules",
            "guardian",
            "core",
            "data",
            "tests"
        }

        ALLOWED_FILES = {
            "app.py",
            "project_check.py"
        }

        if time.time() - start_time > TIME_LIMIT:
            self.report["warnings"].append(
                "Project scan stopped after 15 seconds."
            )
            break
        
        for path in self.root.rglob("*.py"):

            relative = path.relative_to(self.root)
            top = relative.parts[0]

            if (
                top not in ALLOWED_TOP_LEVEL
                and path.name not in ALLOWED_FILES
            ):
                continue

            # Ignore unwanted folders
            if any(folder in path.parts for folder in IGNORE_FOLDERS):
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

# ---------------------------------------------------
# Architecture Analyzer
# Phase 2 - Part 9
# ---------------------------------------------------

def architecture_analysis(self):

    print("Running Architecture Analysis...")

    import_map = {}
    orphan_files = []

    # Build import map
    for file in self.report["python_files"]:

        try:

            module = file.stem
            imports = []

            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:
                        imports.append(alias.name.split(".")[0])

                elif isinstance(node, ast.ImportFrom):

                    if node.module:
                        imports.append(node.module.split(".")[0])

            import_map[module] = imports

        except:
            pass

    # -----------------------------------
    # Orphan Files
    # -----------------------------------

    all_imports = set()

    for items in import_map.values():
        all_imports.update(items)

    for module in import_map:

        if module not in all_imports:

            orphan_files.append(module)

            self.report["warnings"].append({

                "type": "Orphan Module",
                "module": module

            })

    # -----------------------------------
    # Integration Suggestions
    # -----------------------------------

    suggestions = []

    for module in orphan_files:

        name = module.lower()

        if "news" in name:

            suggestions.append(
                f"{module} → Consider integrating with app.py and intelligence_engine.py"
            )

        elif "risk" in name:

            suggestions.append(
                f"{module} → Consider integrating with prediction.py"
            )

        elif "ai" in name:

            suggestions.append(
                f"{module} → Review integration with intelligence_engine.py"
            )

        elif "guardian" in name:

            suggestions.append(
                f"{module} → Review integration with guardian controller"
            )

    self.report["info"].append({

        "Architecture": import_map

    })

    self.report["integration_suggestions"] = suggestions
# ---------------------------------------------------
# Final AI Review
# Phase 2 - Part 10
# ---------------------------------------------------

def final_ai_review(self):

    print("Running Final AI Review...")

    score = self.report["health"]

    errors = len(self.report["errors"])
    warnings = len(self.report["warnings"])

    review = []

    if errors == 0:
        review.append("✓ No syntax errors detected.")
    else:
        review.append(f"✗ {errors} error(s) require immediate attention.")

    if warnings == 0:
        review.append("✓ No warnings detected.")
    else:
        review.append(f"⚠ {warnings} warning(s) detected.")

    if score >= 95:
        grade = "A+"
    elif score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "D"

    self.report["grade"] = grade
    self.report["review"] = review

    # Auto Fix Suggestions
    fixes = []

    for error in self.report["errors"]:

        etype = error.get("type", "")

        if etype == "Syntax Error":
            fixes.append(
                f"Fix syntax in {error['file']} (line {error.get('line','?')})"
            )

        elif etype == "Missing Module":
            fixes.append(
                f"Install or verify module: {error.get('module','')}"
            )

    for warning in self.report["warnings"]:

        wtype = warning.get("type", "")

        if wtype == "Large File":
            fixes.append(
                f"Split {warning['file']} into smaller modules."
            )

        elif wtype == "Long Function":
            fixes.append(
                f"Refactor function {warning['name']}."
            )

        elif wtype == "Duplicate Import":
            fixes.append(
                f"Remove duplicate imports from {warning['file']}."
            )

    self.report["auto_fixes"] = fixes

# ---------------------------------------------------
# Project Change Tracker
# Phase 3 - Part 11
# ---------------------------------------------------

import hashlib

def project_snapshot(self):

    print("Creating Project Snapshot...")

    snapshot = {}

    for file in self.report["python_files"]:

        try:

            data = file.read_bytes()

            snapshot[str(file)] = {
                "hash": hashlib.md5(data).hexdigest(),
                "size": file.stat().st_size
            }

        except Exception:
            continue

    self.report["snapshot"] = snapshot


def compare_snapshot(self):

    import json

    report_dir = self.root / "reports"
    report_dir.mkdir(exist_ok=True)

    snapshot_file = report_dir / "snapshot.json"

    if not snapshot_file.exists():

        with open(snapshot_file, "w", encoding="utf-8") as f:
            json.dump(self.report["snapshot"], f, indent=4)

        print("First snapshot created.")
        return

    with open(snapshot_file, "r", encoding="utf-8") as f:
        old_snapshot = json.load(f)

    changed = []
    new_files = []

    for file, info in self.report["snapshot"].items():

        if file not in old_snapshot:
            new_files.append(file)

        elif old_snapshot[file]["hash"] != info["hash"]:
            changed.append(file)

    self.report["info"].append({
        "Changed Files": changed,
        "New Files": new_files
    })

    with open(snapshot_file, "w", encoding="utf-8") as f:
        json.dump(self.report["snapshot"], f, indent=4)

# ---------------------------------------------------
# AI Integration Advisor
# Phase 3 - Part 12
# ---------------------------------------------------

def integration_advisor(self):

    print("Running AI Integration Advisor...")

    suggestions = []

    known_files = {
        "app.py",
        "intelligence_engine.py",
        "prediction.py",
        "market_scanner.py",
        "news.py",
        "news_analysis.py",
        "risk_manager.py",
        "system_manager.py"
    }

    for file in self.report["python_files"]:

        name = file.name

        if name in known_files:
            continue

        module = file.stem.lower()

        advice = {
            "module": name,
            "import_in": [],
            "update_files": [],
            "reason": ""
        }

        if "ai" in module:
            advice["import_in"] = [
                "app.py",
                "intelligence_engine.py"
            ]
            advice["reason"] = "AI related module"

        elif "news" in module:
            advice["import_in"] = [
                "app.py",
                "news_analysis.py"
            ]
            advice["reason"] = "News processing module"

        elif "risk" in module:
            advice["import_in"] = [
                "prediction.py",
                "system_manager.py"
            ]
            advice["reason"] = "Risk management module"

        elif "scanner" in module:
            advice["import_in"] = [
                "app.py",
                "market_scanner.py"
            ]
            advice["reason"] = "Market scanner module"

        elif "manager" in module:
            advice["import_in"] = [
                "system_manager.py"
            ]
            advice["reason"] = "Manager component"

        else:
            advice["import_in"] = [
                "Review manually"
            ]
            advice["reason"] = "Unknown module type"

        suggestions.append(advice)

    self.report["integration_advisor"] = suggestions


# ---------------------------------------------------
# Dependency Graph Builder
# Phase 3 - Part 13
# ---------------------------------------------------

def build_dependency_graph(self):

    print("Building Dependency Graph...")

    graph = {}

    for file in self.report["python_files"]:

        module = file.stem
        graph[module] = []

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:

                        graph[module].append(alias.name)

                elif isinstance(node, ast.ImportFrom):

                    if node.module:

                        graph[module].append(node.module)

        except Exception:

            continue

    self.report["dependency_graph"] = graph

# ---------------------------------------------------
# Dependency Report
# ---------------------------------------------------

def show_dependency_graph(self):

    print("\nDEPENDENCY GRAPH")
    print("=" * 60)

    graph = self.report.get("dependency_graph", {})

    for module, deps in graph.items():

        print(f"\n{module}")

        if deps:

            for dep in sorted(set(deps)):
                print(f"   └── {dep}")

        else:

            print("   └── No Dependencies")

# ---------------------------------------------------
# Project Complexity
# ---------------------------------------------------

def calculate_complexity(self):

    graph = self.report.get("dependency_graph", {})

    total = 0

    for deps in graph.values():

        total += len(deps)

    average = 0

    if graph:

        average = total / len(graph)

    self.report["complexity"] = {

        "total_dependencies": total,
        "average_dependencies": round(average,2)

                        }
# ---------------------------------------------------
# Duplicate Logic Detector
# Phase 4 - Part 14
# ---------------------------------------------------

def duplicate_logic_analysis(self):

    print("Running Duplicate Logic Analysis...")

    import hashlib

    fingerprints = {}

    for file in self.report["python_files"]:

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            for node in ast.walk(tree):

                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                    try:

                        code = ast.unparse(node)

                    except Exception:

                        continue

                    code = "\n".join(
                        line.strip()
                        for line in code.splitlines()
                        if line.strip()
                    )

                    digest = hashlib.sha256(
                        code.encode("utf-8")
                    ).hexdigest()

                    fingerprints.setdefault(digest, []).append({
                        "file": str(file),
                        "function": node.name,
                        "line": node.lineno
                    })

        except Exception:
            continue

    duplicates = []

    for items in fingerprints.values():

        if len(items) > 1:

            duplicates.append(items)

            self.report["warnings"].append({

                "type": "Duplicate Logic",
                "occurrences": items

            })

            self.report["health"] -= 2

    self.report["duplicate_logic"] = duplicates


# ---------------------------------------------------
# Project Health Inspector
# Phase 4 - Part 15
# ---------------------------------------------------

def health_inspector(self):

    print("Running Project Health Inspector...")

    file_scores = {}

    for file in self.report["python_files"]:

        score = 100

        for err in self.report["errors"]:
            if err.get("file") == str(file):
                score -= 15

        for warn in self.report["warnings"]:
            if warn.get("file") == str(file):
                score -= 5

        if score < 0:
            score = 0

        if score >= 90:
            status = "Excellent"
        elif score >= 75:
            status = "Good"
        elif score >= 60:
            status = "Needs Review"
        else:
            status = "Critical"

        file_scores[str(file)] = {
            "score": score,
            "status": status
        }

    self.report["file_health"] = file_scores

# ---------------------------------------------------
# Priority Report
# ---------------------------------------------------

def priority_report(self):

    print("\nHIGH PRIORITY FILES")
    print("=" * 60)

    health = self.report.get("file_health", {})

    critical = []

    for file, info in health.items():

        if info["score"] < 60:
            critical.append((file, info))

    if not critical:
        print("No critical files found.")
        return

    critical.sort(key=lambda x: x[1]["score"])

    for file, info in critical:

        print(f"{file}")
        print(f"   Score  : {info['score']}")
        print(f"   Status : {info['status']}")
        print()

# ---------------------------------------------------
# Performance Analyzer
# Phase 5 - Part 16
# ---------------------------------------------------

def performance_analysis(self):

    print("Running Performance Analysis...")

    for file in self.report["python_files"]:

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            imports = 0
            nested_loops = 0

            for node in ast.walk(tree):

                # Count imports
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports += 1

                # Detect nested loops
                if isinstance(node, (ast.For, ast.While)):

                    for child in ast.walk(node):

                        if child is node:
                            continue

                        if isinstance(child, (ast.For, ast.While)):
                            nested_loops += 1

            if imports > 30:

                self.report["warnings"].append({

                    "file": str(file),
                    "type": "Too Many Imports",
                    "count": imports

                })

            if nested_loops > 3:

                self.report["warnings"].append({

                    "file": str(file),
                    "type": "Heavy Nested Loops",
                    "count": nested_loops

                })

        except Exception as e:

            self.report["errors"].append({

                "file": str(file),
                "type": "Performance Analysis Error",
                "message": str(e)

            })


# ---------------------------------------------------
# Configuration Checker
# Phase 5 - Part 17
# ---------------------------------------------------

def configuration_check(self):

    print("Checking Project Configuration...")

    required_files = [
        "app.py",
        "requirements.txt",
        ".gitignore",
        "README.md"
    ]

    optional_files = [
        ".env",
        "LICENSE",
        "pyproject.toml",
        "setup.py"
    ]

    for filename in required_files:

        path = self.root / filename

        if not path.exists():

            self.report["errors"].append({

                "type": "Missing Required File",
                "file": filename

            })

            self.report["health"] -= 5

    for filename in optional_files:

        path = self.root / filename

        if not path.exists():

            self.report["warnings"].append({

                "type": "Optional File Missing",
                "file": filename

            })


# ---------------------------------------------------
# Python Version Check
# ---------------------------------------------------

def python_environment(self):

    import platform
    import sys

    self.report["info"].append({

        "Python Version": platform.python_version(),
        "Platform": platform.platform(),
        "Executable": sys.executable

    })


# ---------------------------------------------------
# Folder Structure
# ---------------------------------------------------

def folder_structure(self):

    folders = []

    for item in self.root.iterdir():

        if item.is_dir():

            folders.append(item.name)

    self.report["info"].append({

        "Folders": folders

    })


# ---------------------------------------------------
# Naming Convention Checker
# Phase 6 - Part 18
# ---------------------------------------------------

import re

def naming_convention_check(self):

    print("Checking Naming Conventions...")

    snake_case = re.compile(r'^[a-z][a-z0-9_]*$')
    pascal_case = re.compile(r'^[A-Z][A-Za-z0-9]*$')

    for file in self.report["python_files"]:

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            for node in ast.walk(tree):

                # Class Names
                if isinstance(node, ast.ClassDef):

                    if not pascal_case.match(node.name):

                        self.report["warnings"].append({

                            "file": str(file),
                            "line": node.lineno,
                            "type": "Class Naming",
                            "name": node.name

                        })

                # Function Names
                elif isinstance(node, ast.FunctionDef):

                    if not snake_case.match(node.name):

                        self.report["warnings"].append({

                            "file": str(file),
                            "line": node.lineno,
                            "type": "Function Naming",
                            "name": node.name

                        })

        except Exception:
            continue


# ---------------------------------------------------
# File Size Analyzer
# ---------------------------------------------------

def file_size_analysis(self):

    print("Checking File Sizes...")

    for file in self.report["python_files"]:

        try:

            size_kb = file.stat().st_size / 1024

            if size_kb > 200:

                self.report["warnings"].append({

                    "file": str(file),
                    "type": "Large Source File",
                    "size_kb": round(size_kb,2)

                })

        except:
            pass


# ---------------------------------------------------
# Documentation Checker
# ---------------------------------------------------

def documentation_check(self):

    print("Checking Documentation...")

    for file in self.report["python_files"]:

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            if '"""' not in source:

                self.report["warnings"].append({

                    "file": str(file),
                    "type": "Missing Module Docstring"

                })

        except:
            pass


# ---------------------------------------------------
# Code Smell Detector
# Phase 6 - Part 19
# ---------------------------------------------------

def code_smell_analysis(self):

    print("Running Code Smell Analysis...")

    for file in self.report["python_files"]:

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            for node in ast.walk(tree):

                # Function with too many arguments
                if isinstance(node, ast.FunctionDef):

                    arg_count = len(node.args.args)

                    if arg_count > 6:

                        self.report["warnings"].append({

                            "file": str(file),
                            "line": node.lineno,
                            "type": "Too Many Parameters",
                            "function": node.name,
                            "count": arg_count

                        })

                # Deep nesting
                if isinstance(node, (ast.If, ast.For, ast.While)):

                    depth = len(list(ast.walk(node)))

                    if depth > 120:

                        self.report["warnings"].append({

                            "file": str(file),
                            "line": getattr(node, "lineno", 0),
                            "type": "Complex Block"

                        })

        except Exception as e:

            self.report["errors"].append({

                "file": str(file),
                "type": "Code Smell Error",
                "message": str(e)

            })

# ---------------------------------------------------
# Comment Density
# ---------------------------------------------------

def comment_analysis(self):

    print("Checking Comments...")

    for file in self.report["python_files"]:

        try:

            lines = file.read_text(
                encoding="utf-8",
                errors="ignore"
            ).splitlines()

            if not lines:
                continue

            comments = sum(
                1 for line in lines
                if line.strip().startswith("#")
            )

            ratio = comments / len(lines)

            if ratio < 0.02:

                self.report["warnings"].append({

                    "file": str(file),
                    "type": "Low Comment Density",
                    "ratio": round(ratio, 2)

                })

        except:
            pass

# ---------------------------------------------------
# Project Risk Analyzer
# Phase 7 - Part 20
# ---------------------------------------------------

def project_risk_analysis(self):

    print("Running Project Risk Analysis...")

    risk_report = []

    for file in self.report["python_files"]:

        risk = 0

        # Error count
        for err in self.report["errors"]:
            if err.get("file") == str(file):
                risk += 10

        # Warning count
        for warn in self.report["warnings"]:
            if warn.get("file") == str(file):
                risk += 3

        # File size
        try:
            if file.stat().st_size > 300 * 1024:
                risk += 5
        except:
            pass

        # Risk Level
        if risk >= 25:
            level = "HIGH"
        elif risk >= 10:
            level = "MEDIUM"
        else:
            level = "LOW"

        risk_report.append({
            "file": str(file),
            "risk": risk,
            "level": level
        })

    risk_report.sort(
        key=lambda x: x["risk"],
        reverse=True
    )

    self.report["risk_report"] = risk_report


# ---------------------------------------------------
# Show Risk Report
# ---------------------------------------------------

def show_risk_report(self):

    print("\nPROJECT RISK REPORT")
    print("=" * 60)

    for item in self.report.get("risk_report", [])[:10]:

        print(
            f"{item['level']:6} | "
            f"{item['risk']:3} | "
            f"{item['file']}"
        )

