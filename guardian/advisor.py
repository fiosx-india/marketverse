"""
MarketVerse Guardian
advisor.py

Purpose:
Provide recommendations based on project health.
"""


class GuardianAdvisor:

    def advise(self, report):

        if report.status == "GREEN":
            return [
                "Project is healthy.",
                "No action required."
            ]

        elif report.status == "YELLOW":
            return [
                "Review project warnings.",
                "Validate imports.",
                "Check missing modules."
            ]

        return [
            "Critical issues detected.",
            "Fix broken files immediately.",
            "Run full Guardian scan.",
            "Revalidate project."
        ]
