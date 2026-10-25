
"""Generate JSON reports for CodePilot AI findings."""

import json
from pathlib import Path

from codepilot.fixer import suggest_fix


def save_report(
    findings: list[dict],
    output_path: str = "reports/report.json",
) -> str:
    """Save findings and suggested fixes to a JSON report."""
    enriched_findings = []

    for finding in findings:
        item = finding.copy()
        item["suggested_fix"] = suggest_fix(finding)
        enriched_findings.append(item)

    report = {
        "tool": "CodePilot AI",
        "total_findings": len(enriched_findings),
        "summary": {
            "errors": sum(
                item["severity"] == "error"
                for item in enriched_findings
            ),
            "warnings": sum(
                item["severity"] == "warning"
                for item in enriched_findings
            ),
        },
        "findings": enriched_findings,
    }

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    return str(path)

