
import json

from codepilot.reporter import save_report


def test_saves_json_report(tmp_path):
    findings = [
        {
            "rule": "SEC001",
            "severity": "warning",
            "line": 1,
            "message": "Unsafe eval usage.",
        }
    ]

    output_file = tmp_path / "report.json"
    result = save_report(findings, str(output_file))

    assert result == str(output_file)
    assert output_file.exists()

    report = json.loads(output_file.read_text(encoding="utf-8"))
    assert report["tool"] == "CodePilot AI"
    assert report["total_findings"] == 1
    assert report["summary"]["warnings"] == 1
    assert report["findings"][0]["rule"] == "SEC001"


def test_saves_empty_report(tmp_path):
    output_file = tmp_path / "empty_report.json"
    save_report([], str(output_file))

    report = json.loads(output_file.read_text(encoding="utf-8"))
    assert report["total_findings"] == 0
    assert report["summary"]["errors"] == 0
    assert report["summary"]["warnings"] == 0
