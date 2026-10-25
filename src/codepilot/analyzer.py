
"""Static code analyzer for CodePilot AI."""

import ast


def analyze_code(source: str) -> list[dict]:
    """Find basic Python syntax and code-quality issues."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [
            {
                "rule": "PY001",
                "severity": "error",
                "line": exc.lineno or 1,
                "message": f"Syntax error: {exc.msg}",
            }
        ]

    findings = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not node.name.startswith("_") and not ast.get_docstring(node):
                findings.append({
                    "rule": "DOC001",
                    "severity": "warning",
                    "line": node.lineno,
                    "message": f"Function '{node.name}' has no docstring.",
                })

        elif isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append({
                "rule": "ERR001",
                "severity": "warning",
                "line": node.lineno,
                "message": "Bare except catches all exceptions.",
            })

        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "eval":
                findings.append({
                    "rule": "SEC001",
                    "severity": "warning",
                    "line": node.lineno,
                    "message": "Use of eval() may execute untrusted expressions.",
                })

    return sorted(findings, key=lambda item: (item["line"], item["rule"]))
