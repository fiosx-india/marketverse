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
    warnings: int
    health_score: int
    last_scan: str
    integration_status: dict


class HealthMonitor:

    def generate(
        self,
        files,
        validation_results,
        integration_status=None
    ):

        if integration_status is None:
            integration_status = {}

        total = len(files)

        valid = sum(
            1
            for r in validation_results
            if r.valid
        )

        errors = total - valid

        warnings = sum(
            len(getattr(r, "warnings", []))
            for r in validation_results
        )

        if total == 0:
            health_score = 0
        else:
            health_score = round((valid / total) * 100)

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
            warnings=warnings,
            health_score=health_score,
            last_scan=datetime.now().isoformat(),
            integration_status=integration_status
        )
