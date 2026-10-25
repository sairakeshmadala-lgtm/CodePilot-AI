
"""Command-line interface for CodePilot AI."""

import argparse
from pathlib import Path

from codepilot.analyzer import analyze_code
from codepilot.reporter import save_report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze Python code with CodePilot AI."
    )
    parser.add_argument("file", help="Python file to analyze")
    parser.add_argument(
        "--output",
        default="reports/report.json",
        help="Path for the JSON report",
    )
    args = parser.parse_args()

    source_path = Path(args.file)

    if not source_path.is_file():
        parser.error(f"File not found: {source_path}")

    source = source_path.read_text(encoding="utf-8")
    findings = analyze_code(source)
    report_path = save_report(findings, args.output)

    print(f"Analyzed: {source_path}")
    print(f"Findings: {len(findings)}")
    print(f"JSON report: {report_path}")

    return 1 if any(
        item["severity"] == "error" for item in findings
    ) else 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Command-line interface for CodePilot AI."""

import argparse
import ast
from pathlib import Path

from codepilot.analyzer import analyze_code
from codepilot.fixer import add_docstring
from codepilot.reporter import save_report


def main() -> int:
    """Run CodePilot AI from the command line."""
    parser = argparse.ArgumentParser(
        description="Analyze Python code with CodePilot AI."
    )
    parser.add_argument("file", help="Python file to analyze")
    parser.add_argument(
        "--output",
        default="reports/report.json",
        help="Path for the JSON report",
    )
    parser.add_argument(
        "--fix-docstrings",
        action="store_true",
        help="Add basic docstrings to functions that need them",
    )
    args = parser.parse_args()

    source_path = Path(args.file)

    if not source_path.is_file():
        parser.error(f"File not found: {source_path}")

    source = source_path.read_text(encoding="utf-8")

    if args.fix_docstrings:
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            parser.error(f"Cannot fix syntax errors: {exc}")

        function_names = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and not node.name.startswith("_")
            and not ast.get_docstring(node)
        ]

        if function_names:
            backup_path = source_path.with_suffix(
                source_path.suffix + ".bak"
            )
            backup_path.write_text(source, encoding="utf-8")

            for function_name in function_names:
                source = add_docstring(source, function_name)

            source_path.write_text(source, encoding="utf-8")
            print(f"Backup created: {backup_path}")
            print(f"Docstrings added: {len(function_names)}")
        else:
            print("No missing docstrings found.")

    findings = analyze_code(source)
    report_path = save_report(findings, args.output)

    print(f"Analyzed: {source_path}")
    print(f"Findings: {len(findings)}")
    print(f"JSON report: {report_path}")

    return 1 if any(
        item["severity"] == "error" for item in findings
    ) else 0


if __name__ == "__main__":
    raise SystemExit(main())
