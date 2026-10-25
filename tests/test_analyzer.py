
from codepilot.analyzer import analyze_code


def test_detects_syntax_error():
    findings = analyze_code("def broken(:")
    assert findings[0]["rule"] == "PY001"
    assert findings[0]["severity"] == "error"


def test_detects_eval_usage():
    findings = analyze_code("result = eval('1 + 1')")
    assert any(item["rule"] == "SEC001" for item in findings)


def test_detects_missing_docstring():
    findings = analyze_code("def greet():\n    print('Hello')")
    assert any(item["rule"] == "DOC001" for item in findings)


def test_clean_code_has_no_findings():
    findings = analyze_code("x = 10\nprint(x)")
    assert findings == []
