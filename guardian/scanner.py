from pathlib import Path


class ProjectScanner:
    """Scans the project directory for Python files."""

    def __init__(self, root_path="."):
        self.root_path = Path(root_path)

    def scan(self, root_path=None):
        """Return all Python files in the project."""

        if root_path is None:
            root = self.root_path
        else:
            root = Path(root_path)

        files = []

        for file in root.rglob("*.py"):
            if "__pycache__" in str(file):
                continue

            files.append(file)

        return sorted(files)
