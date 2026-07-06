"""
MarketVerse Guardian
dependency.py

Purpose:
Build a dependency map for Python modules.
"""

import ast
from pathlib import Path


class DependencyAnalyzer:
    """Analyze Python imports."""

    def analyze(self, file_path):
        file_path = Path(file_path)

        try:
            source = file_path.read_text(encoding="utf-8")
            tree = ast.parse(source)

            imports = []

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):
                    for item in node.names:
                        imports.append(item.name)

                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""

                    # Handle relative imports
                    if node.level > 0:
                        module = "." * node.level + module

                    imports.append(module)

            return {
                "success": True,
                "imports": sorted(set(imports))
            }

        except Exception as e:
            return {
                "success": False,
                "imports": [],
                "error": str(e)
            }
