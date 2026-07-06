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

    def __init__(self, file_path, valid=True, error=None, warnings=None):
        self.file_path = file_path
        self.valid = valid
        self.error = error
        self.warnings = warnings or []


class ProjectValidator:
    """Validates Python files."""

    def validate(self, file_path):
        file_path = Path(file_path)
        warnings = []

        try:
            source = file_path.read_text(encoding="utf-8")

            if not source.strip():
                warnings.append("Empty file.")

            tree = ast.parse(source)

            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if hasattr(node.func, "id") and node.func.id in ("eval", "exec"):
                        warnings.append(f"Dangerous function: {node.func.id}")

            return ValidationResult(
                file_path=file_path,
                valid=True,
                warnings=warnings
            )

        except SyntaxError as e:
            return ValidationResult(
                file_path=file_path,
                valid=False,
                error=f"SyntaxError: {e}"
            )

        except UnicodeDecodeError:
            return ValidationResult(
                file_path=file_path,
                valid=False,
                error="Encoding Error"
            )

        except Exception as e:
            return ValidationResult(
                file_path=file_path,
                valid=False,
                error=str(e)
            )
