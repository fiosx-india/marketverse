"""
MarketVerse Guardian Runtime Diagnostic
Version : 1.0
Purpose : Runtime tracing, error detection and root-cause reporting
"""

from datetime import datetime
import traceback


class RuntimeDiagnostic:

    def __init__(self):
        self.events = []
        self.errors = []

    # -------------------------
    # Trace Variables
    # -------------------------
    def trace(self, name, value, source="Unknown"):
        self.events.append({
            "time": datetime.now(),
            "type": "TRACE",
            "source": source,
            "name": name,
            "value": value
        })

    # -------------------------
    # Trace Function Call
    # -------------------------
    def function(self, file, function):
        self.events.append({
            "time": datetime.now(),
            "type": "FUNCTION",
            "file": file,
            "function": function
        })

    # -------------------------
    # Log Error
    # -------------------------
    def error(self, file, function, error):

        self.errors.append({
            "time": datetime.now(),
            "file": file,
            "function": function,
            "error": str(error),
            "traceback": traceback.format_exc()
        })

    # -------------------------
    # Validate Market Symbol
    # -------------------------
    def validate_symbol(self, symbol):

        if not symbol:
            return False, "Empty Symbol"

        invalid = [
            "AUTOMOBILE",
            "BANKING",
            "IT",
            "POWER",
            "PHARMA",
            "ENERGY",
            "METALS",
            "PORTS",
            "DIVERSIFIED"
        ]

        if symbol.upper() in invalid:
            return False, f'"{symbol}" is a Sector, not a Market Symbol.'

        return True, "Valid"

    # -------------------------
    # Report
    # -------------------------
    def report(self):

        print("\n")
        print("=" * 70)
        print("GUARDIAN RUNTIME DIAGNOSTIC REPORT")
        print("=" * 70)

        print(f"Generated : {datetime.now()}")

        print("\nRuntime Trace")

        for item in self.events:

            if item["type"] == "TRACE":

                print(
                    f'[TRACE] {item["source"]} -> '
                    f'{item["name"]} = {item["value"]}'
                )

            elif item["type"] == "FUNCTION":

                print(
                    f'[CALL] {item["file"]} :: '
                    f'{item["function"]}'
                )

        print("\nErrors")

        if not self.errors:

            print("No Runtime Errors")

        else:

            for err in self.errors:

                print("-" * 60)
                print("File      :", err["file"])
                print("Function  :", err["function"])
                print("Error     :", err["error"])
                print("-" * 60)

        print("=" * 70)


diagnostic = RuntimeDiagnostic()
