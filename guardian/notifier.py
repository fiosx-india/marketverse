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
