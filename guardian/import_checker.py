"""
MarketVerse Guardian
import_checker.py

Purpose:
Check whether imported modules are available.
"""

import importlib


class ImportChecker:
    """Checks if imported modules can be imported."""

    def check(self, imports):
        missing = []
        available = []

        for module in imports:
            if not module:
                continue

            # Skip relative imports
            if module.startswith("."):
                continue

            try:
                importlib.import_module(module)
                available.append(module)

            except Exception as e:
                missing.append({
                    "module": module,
                    "error": str(e)
                })

        return {
            "success": len(missing) == 0,
            "available": available,
            "missing": missing
        }
