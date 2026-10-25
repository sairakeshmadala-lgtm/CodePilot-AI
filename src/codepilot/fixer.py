
"""Fix suggestions for CodePilot AI."""

import ast


def suggest_fix(finding: dict) -> dict:
    """Return a suggested fix for a detected code issue."""
    rule = finding.get("rule", "")

    suggestions = {
        "SEC001": {
            "title": "Avoid eval()",
            "suggestion": (
                "Avoid eval() on untrusted input. "
                "Use explicit operations or a safe parser."
            ),
            "severity": "warning",
        },
        "DOC001": {
            "title": "Add a docstring",
            "suggestion": (
                "Add a descriptive triple-quoted docstring "
                "immediately inside the function."
            ),
            "severity": "info",
        },
        "PY001": {
            "title": "Fix the syntax error",
            "suggestion": (
                "Check the reported line for missing colons, "
                "brackets, or quotation marks."
            ),
            "severity": "error",
        },
        "ERR001": {
            "title": "Avoid bare except",
            "suggestion": (
                "Catch specific exception types instead of "
                "using a bare except."
            ),
            "severity": "warning",
        },
    }

    return suggestions.get(
        rule,
        {
            "title": "Review this finding",
            "suggestion": (
                "Review the message and inspect the reported line."
            ),
            "severity": "info",
        },
    )


def add_docstring(source: str, function_name: str = None) -> str:
    """Add a docstring to the selected function or public functions."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source

    lines = source.splitlines(keepends=True)
    insertions = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        if function_name and node.name != function_name:
            continue

        if node.name.startswith("_") or ast.get_docstring(node):
            continue

        if not node.body:
            continue

        first_statement = node.body[0]

        if (
            isinstance(first_statement, ast.Expr)
            and isinstance(first_statement.value, ast.Constant)
            and isinstance(first_statement.value.value, str)
        ):
               continue

        indent = " " * (node.col_offset + 4)
        docstring = f'{indent}"""TODO: Describe {node.name}."""\n'
        insertions.append((first_statement.lineno - 1, docstring))

    for index, text in sorted(insertions, reverse=True):
        lines.insert(index, text)

    return "".join(lines)