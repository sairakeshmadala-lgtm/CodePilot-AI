# CodePilot AI — Autonomous Code Analysis Dashboard

A Python-based code analysis tool with an interactive Streamlit dashboard. It detects selected code issues, flags potentially unsafe patterns, suggests missing docstrings, and generates JSON reports.

## Features

- Static analysis of Python source code
- Detection of selected security risks, including `eval()` usage
- Missing function docstring detection and automated suggestions
- JSON report generation
- Streamlit dashboard for uploading and analyzing Python files
- Downloadable analysis reports
- Automated tests using pytest

## Technologies

Python · Streamlit · Python AST · Pytest · JSON · Git · GitHub

## Project Structure

```text
CodePilot-AI/
├── examples/
├── reports/
├── src/codepilot/
├── tests/
└── dashboard.py
```

## Run the Project

Clone this repository:

```bash
git clone https://github.com/sairakeshmadala-lgtm/CodePilot-AI.git
cd CodePilot-AI
```

Activate your existing virtual environment or create one:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project's required dependencies. If a `requirements.txt` file is available, run:

```powershell
pip install -r requirements.txt
```

Set the package path:

```powershell
$env:PYTHONPATH = "src"
```

Launch the dashboard:

```powershell
python -m streamlit run dashboard.py
```

Open the local URL shown in your terminal.

## Command-Line Usage

Analyze a sample file:

```powershell
python -m codepilot examples/sample.py
```

Run supported docstring fixes:

```powershell
python -m codepilot examples/sample.py --fix-docstrings
```

Run automated tests:

```powershell
python -m pytest -q
```

## Test Status

The current test suite passed 10 tests covering analysis, docstring fixes, and JSON report generation.

## Future Improvements

- Expand static-analysis and security rules
- Add safer fix previews and more automated fixes
- Improve dashboard filtering and report visualizations
- Add continuous integration

## Author

**Sai Rakesh Madala**

GitHub: [sairakeshmadala-lgtm](https://github.com/sairakeshmadala-lgtm)

---

*This tool provides heuristic findings and is not a replacement for a full security audit. Review suggested changes before applying them.*
