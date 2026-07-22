"""
MarketVerse Core
bootstrap.py

Purpose:
Initialize the MarketVerse platform.
"""

from pathlib import Path


class Bootstrap:
    """Initialize project environment."""

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent

    def check_structure(self):
        required = [
            "core",
            "guardian",
            "modules",
            "app.py",
            "requirements.txt",
        ]

        missing = []

        for item in required:
            if not (self.project_root / item).exists():
                missing.append(item)

        return {
            "success": len(missing) == 0,
            "missing": missing,
        }

    def initialize(self):
        result = self.check_structure()

        if result["success"]:
            return {
                "status": "READY",
                "message": "MarketVerse initialized successfully."
            }

        return {
            "status": "ERROR",
            "message": "Missing project components.",
            "missing": result["missing"],
        }


# ==========================================
# SELF TEST
# ==========================================

if __name__ == "__main__":

    bootstrap = Bootstrap()

    print("=" * 50)
    print("MARKETVERSE BOOTSTRAP CHECK")
    print("=" * 50)

    result = bootstrap.initialize()

    print("Status :", result["status"])
    print("Message:", result["message"])

    if result["status"] == "ERROR":
        print("\nMissing Components:")
        for item in result.get("missing", []):
            print("-", item)

    print("=" * 50)
