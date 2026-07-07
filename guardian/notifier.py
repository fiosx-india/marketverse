"""
MarketVerse Guardian
notifier.py

Purpose:
Generate project notifications.
"""


class Notification:

    def __init__(self, level, title, message):
        self.level = level
        self.title = title
        self.message = message

    def __str__(self):
        return f"[{self.level}] {self.title}: {self.message}"


class Notifier:

    def info(self, message):
        return Notification(
            "INFO",
            "Information",
            message
        )

    def warning(self, message):
        return Notification(
            "WARNING",
            "Warning",
            message
        )

    def error(self, message):
        return Notification(
            "ERROR",
            "Error",
            message
        )

    def success(self, message):
        return Notification(
            "SUCCESS",
            "Success",
            message
        )

    def integration_notifications(self, integration_report):

        notifications = []

        for name, result in integration_report.items():

            if isinstance(result, dict):

                status = result.get("status", "UNKNOWN")

                if status == "OK":
                    notifications.append(
                        self.success(
                            f"{name} monitor is healthy."
                        )
                    )

                else:
                    notifications.append(
                        self.error(
                            f"{name} monitor failed: "
                            f"{result.get('message', '')}"
                        )
                    )

            elif isinstance(result, list):

                failed = [
                    item for item in result
                    if item.get("status") != "OK"
                ]

                if failed:

                    notifications.append(
                        self.warning(
                            f"{name}: {len(failed)} module(s) failed."
                        )
                    )

                else:

                    notifications.append(
                        self.success(
                            f"{name}: All modules loaded successfully."
                        )
                    )

        return notifications

def guardian_summary(self, report):

    score = report.get("health_score", 0)

    if score >= 90:
        return self.success("Guardian Health: GREEN")

    elif score >= 70:
        return self.warning("Guardian Health: YELLOW")

    return self.error("Guardian Health: RED")
