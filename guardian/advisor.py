"""
MarketVerse Guardian
advisor.py

Purpose:
Provide recommendations based on project health.
"""


class GuardianAdvisor:
    """Provides recommendations based on project health."""

    def advise(self, report):

        advice = []

        # ==========================
        # Overall Project Health
        # ==========================

        if report.status == "GREEN":
            advice.extend([
                "Project is healthy.",
                "Deployment is safe.",
                "No critical issues detected."
            ])

        elif report.status == "YELLOW":
            advice.extend([
                "Review project warnings.",
                "Validate imports.",
                "Check missing modules.",
                "Run project tests before deployment."
            ])

        else:
            advice.extend([
                "Critical issues detected.",
                "Fix broken files immediately.",
                "Run full Guardian scan.",
                "Revalidate project before deployment."
            ])

        # ==========================
        # Validation Summary
        # ==========================

        if hasattr(report, "errors") and report.errors > 0:
            advice.append(
                f"Detected {report.errors} file(s) with errors."
            )

        if hasattr(report, "warnings") and report.warnings > 0:
            advice.append(
                f"Detected {report.warnings} warning(s)."
            )

        if hasattr(report, "health_score"):
            advice.append(
                f"Health Score: {report.health_score}%"
            )

        # ==========================
        # Integration Monitor Report
        # ==========================

        if hasattr(report, "integration_status"):

            integrations = report.integration_status

            for name, result in integrations.items():

                if isinstance(result, list):

                    failed = [
                        item
                        for item in result
                        if item.get("status") != "OK"
                    ]

                    if failed:
                        advice.append(
                            f"{name.title()} Monitor: {len(failed)} issue(s) detected."
                        )

                elif isinstance(result, dict):

                    if result.get("status") != "OK":
                        advice.append(
                            f"{name.title()} Monitor: {result.get('message', 'Issue detected.')}"
                        )

        return advice
