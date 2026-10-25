from codepilot.fixer import suggest_fix, add_docstring


def test_eval_suggestion():
    finding = {"rule": "SEC001"}
    result = suggest_fix(finding)

    assert result["title"] == "Avoid eval()"
    assert "untrusted input" in result["suggestion"]


def test_docstring_suggestion():
    finding = {"rule": "DOC001"}
    result = suggest_fix(finding)

    assert result["title"] == "Add a docstring"
    



def test_add_docstring_to_function():
    source = "def hello():\n    print('Hi')\n"

    result = add_docstring(source, "hello")

    assert '"""TODO: Describe hello."""' in result
    assert "print('Hi')" in result


def test_does_not_duplicate_docstring():
    source = 'def hello():\n    """Say hello."""\n    print("Hi")\n'

    result = add_docstring(source, "hello")

    assert result == source
