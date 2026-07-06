"""
MarketVerse Guardian
validator.py

Purpose:
Validate Python source files.
"""

import ast
from pathlib import Path


class ValidationResult:
    """Stores validation result."""

    def __init__(self, file_path, valid=True, error=None):
        self.file_path = file_path
        self.valid = valid
        self.error = error


class ProjectValidator:
    """Validates Python files."""

    def validate(self, file_path):
        file_path = Path(file_path)

        try:
            source = file_path.read_text(encoding="utf-8")
            ast.parse(source)

            return ValidationResult(
                file_path=file_path,
                valid=True
            )

        except Exception as e:
            return ValidationResult(
                file_path=file_path,
                valid=False,
                error=str(e)
            )
