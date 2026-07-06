"""
MarketVerse Guardian
scanner.py

Purpose:
Scan the project and discover Python modules.
"""

from pathlib import Path


class ProjectScanner:
    """Scans the project directory for Python files."""

    def __init__(self, root_path="."):
        self.root_path = Path(root_path)

    def scan(self):
        """Return all Python files in the project."""
        files = []

        for file in self.root_path.rglob("*.py"):
            if "__pycache__" in str(file):
                continue

            files.append(file)

        return sorted(files)
