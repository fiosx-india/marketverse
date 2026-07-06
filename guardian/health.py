"""
MarketVerse Guardian
health.py

Purpose:
Project health monitoring.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class HealthReport:
    status: str
    files: int
    valid_files: int
    errors: int
    last_scan: str


class HealthMonitor:

    def generate(self, files, validation_results):
        total = len(files)

        valid = sum(
            1 for r in validation_results
            if r.valid
        )

        errors = total - valid

        if errors == 0:
            status = "GREEN"
        elif errors < 5:
            status = "YELLOW"
        else:
            status = "RED"

        return HealthReport(
            status=status,
            files=total,
            valid_files=valid,
            errors=errors,
            last_scan=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
