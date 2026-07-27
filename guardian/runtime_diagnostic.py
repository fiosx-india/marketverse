"""
MarketVerse Guardian Runtime Diagnostic
Version : 2.0.0
Purpose : Runtime tracing, validation, root cause analysis,
          health monitoring and diagnostic reporting.
"""

from datetime import datetime
import traceback


class RuntimeDiagnostic:

    def __init__(self):
        self.events = []
        self.errors = []
        self.warnings = []
        self.signal_reports = []
              
    # -------------------------------------------------
    # Trace Variables
    # -------------------------------------------------

    def trace(self, name, value, source="Unknown"):

        self.events.append({
            "time": datetime.now(),
            "type": "TRACE",
            "source": source,
            "name": name,
            "value": value
        })

    # -------------------------------------------------
    # Trace Function Call
    # -------------------------------------------------

    def function(self, file, function):

        self.events.append({
            "time": datetime.now(),
            "type": "FUNCTION",
            "file": file,
            "function": function
        })

    # -------------------------------------------------
    # Warning
    # -------------------------------------------------

    def warning(self, file, function, message):

        self.warnings.append({
            "time": datetime.now(),
            "file": file,
            "function": function,
            "message": message
        })

    # -------------------------------------------------
    # Error
    # -------------------------------------------------

    def error(self, file, function, error):

        self.errors.append({

            "time": datetime.now(),
            "file": file,
            "function": function,
            "error": str(error),
            "traceback": traceback.format_exc()
        })

    # -------------------------------------------------
    # Validate Symbol
    # -------------------------------------------------

    def validate_symbol(self, symbol):

        if symbol is None:

            self.warning(
                "Unknown",
                "validate_symbol",
                "Symbol is None"
            )

            return False, "Symbol is None"

        symbol = str(symbol).strip()

        if symbol == "":

            self.warning(
                "Unknown",
                "validate_symbol",
                "Empty Symbol"
            )

            return False, "Empty Symbol"

        invalid = {

            "AUTOMOBILE",
            "BANKING",
            "IT",
            "POWER",
            "ENERGY",
            "PHARMA",
            "METALS",
            "PORTS",
            "DIVERSIFIED",
            "MINING",
            "TELECOM",
            "INFRASTRUCTURE"

        }

        if symbol.upper() in invalid:

            self.warning(
                "Unknown",
                "validate_symbol",
                f"{symbol} is a sector."
            )

            return (
                False,
                f'"{symbol}" is a Sector Name, not a Yahoo Finance Symbol.'
            )

        return True, "Valid"

    # -------------------------------------------------
    # Signal Validation
    # -------------------------------------------------
    def validate_signal(
        self,
        symbol,
        ai_signal,
        news,
        technical,
        prediction=None,
        volume_alert=False
    ):
        """
        Validate AI signal against news, technicals,
        prediction and volume.
        """

        report = {
            "symbol": symbol,
            "signal": ai_signal,
            "status": "VERIFIED",
            "score": 0,
            "checks": [],
            "issues": []
        }

        # News
        sentiment = str(news.get("sentiment", "UNKNOWN")).upper()

        if sentiment == "BULLISH":
            report["score"] += 20
            report["checks"].append("Bullish News")

        elif sentiment == "BEARISH":
            report["issues"].append("Bearish News")

        # Trend
        trend = str(
            technical.get("trend", "UNKNOWN")
        ).upper()

        if trend == "UPTREND":
            report["score"] += 20
            report["checks"].append("Uptrend")

        elif trend == "DOWNTREND":
            report["issues"].append("Downtrend")

        # Volume

        if volume_alert:
            report["score"] += 20
            report["checks"].append("Volume Spike")

        # Prediction

        if prediction:

            direction = str(
                prediction.get("direction", "")
            ).upper()

            if direction == "UP":
                report["score"] += 20
                report["checks"].append("Prediction Up")

            elif direction == "DOWN":
                report["issues"].append("Prediction Down")

        # AI Signal

        if str(ai_signal).upper() == "BUY":
            report["score"] += 20

        elif str(ai_signal).upper() == "SELL":
            report["score"] += 20

        # Conflict Detection

        if (
            ai_signal == "BUY"
            and sentiment == "BEARISH"
        ):
            report["status"] = "CONFLICT"

        if (
            ai_signal == "SELL"
            and sentiment == "BULLISH"
        ):
            report["status"] = "CONFLICT"

        if report["score"] < 60:
            report["status"] = "WEAK"

        self.signal_reports.append(report)

        return report

    # -------------------------------------------------
    # Root Cause
    # -------------------------------------------------

    def root_cause(self):

        result = []

        for err in self.errors:

            reason = "Unknown"

            fix = "Check manually."

            text = err["error"]

            if "404" in text:

                reason = "Yahoo Finance returned HTTP 404."

                fix = "Verify the market symbol."

            elif "No data found" in text:

                reason = "Yahoo Finance returned empty data."

                fix = "Verify symbol or market session."

            elif "possibly delisted" in text:

                reason = "Invalid or unsupported symbol."

                fix = "Replace with a valid Yahoo Finance symbol."

            elif "unexpected indent" in text:

                reason = "Python indentation error."

                fix = "Fix code indentation."

            elif "ImportError" in text:

                reason = "Module Import Failed."

                fix = "Verify imports."

            elif "KeyError" in text:

                reason = "Dictionary key missing."

                fix = "Verify dictionary structure."

            elif "AttributeError" in text:

                reason = "Object attribute missing."

                fix = "Verify object initialization."

            result.append({

                "file": err["file"],
                "function": err["function"],
                "reason": reason,
                "suggestion": fix

            })

        return result

    # -------------------------------------------------
    # Health Score
    # -------------------------------------------------

    def health_score(self):

        score = 100

        score -= len(self.errors) * 10

        score -= len(self.warnings) * 2

        return max(score, 0)

    # -------------------------------------------------
    # Summary
    # -------------------------------------------------

    def summary(self):

        return {

            "events": len(self.events),
            "warnings": len(self.warnings),
            "errors": len(self.errors),
            "signal_reports": len(self.signal_reports),
            "health": self.health_score()

        }

    # -------------------------------------------------
    # Report
    # -------------------------------------------------

    def report(self):

        print()
        print("=" * 70)
        print("MARKETVERSE GUARDIAN RUNTIME DIAGNOSTIC REPORT")
        print("=" * 70)

        print("Generated :", datetime.now())

        print()
        print("Runtime Events")

        for item in self.events:

            if item["type"] == "TRACE":

                print(
                    f'[TRACE] '
                    f'{item["source"]} -> '
                    f'{item["name"]} = {item["value"]}'
                )

            elif item["type"] == "FUNCTION":

                print(
                    f'[CALL] '
                    f'{item["file"]} :: '
                    f'{item["function"]}'
                )

        print()
        print("Warnings")

        if not self.warnings:

            print("No Warnings")

        else:

            for item in self.warnings:

                print("-" * 60)
                print("File      :", item["file"])
                print("Function  :", item["function"])
                print("Message   :", item["message"])

        print()
        print("Errors")

        if not self.errors:

            print("No Runtime Errors")

        else:

            for item in self.errors:

                print("-" * 60)
                print("File      :", item["file"])
                print("Function  :", item["function"])
                print("Error     :", item["error"])

        print()
        print("Root Cause Analysis")

        causes = self.root_cause()

        if not causes:

            print("No Root Cause Detected")

        else:

            for item in causes:

                print("-" * 60)
                print("File       :", item["file"])
                print("Function   :", item["function"])
                print("Reason     :", item["reason"])
                print("Suggestion :", item["suggestion"])

        print()
        print("=" * 70)
        print("SIGNAL VALIDATION REPORT")
        print("=" * 70)

        if not self.signal_reports:

            print("No Signal Validation")

        else:

            for item in self.signal_reports:

                print("-" * 60)
                print("Symbol :", item["symbol"])
                print("Signal :", item["signal"])
                print("Status :", item["status"])
                print("Score  :", item["score"])

                if item["checks"]:

                    print("Checks :")

                    for check in item["checks"]:
                        print("  ✔", check)

                if item["issues"]:

                    print("Issues :")

                    for issue in item["issues"]:
                        print("  ✘", issue)


        print()
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)

        summary = self.summary()

        print("Runtime Events :", summary["events"])
        print("Warnings       :", summary["warnings"])
        print("Errors         :", summary["errors"])
        print("Health Score   :", f'{summary["health"]}%')
        print("Signal Reports :", summary["signal_reports"])

        print("=" * 70)


diagnostic = RuntimeDiagnostic()
