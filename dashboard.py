import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
"""Streamlit dashboard for CodePilot AI."""

import streamlit as st
from pathlib import Path

from codepilot.analyzer import analyze_code
from codepilot.reporter import save_report

st.set_page_config(
    page_title="CodePilot AI",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 CodePilot AI")
st.subheader("Autonomous Code Analysis Dashboard")
st.write(
    "Analyze Python code, detect issues, and review suggested fixes."
)

uploaded_file = st.file_uploader(
    "Upload a Python file",
    type=["py"],
)

if uploaded_file is not None:
    source = uploaded_file.getvalue().decode("utf-8")

    if st.button("Analyze Code", type="primary"):
        findings = analyze_code(source)

        report_path = Path("reports/dashboard_report.json")
        save_report(findings, str(report_path))

        errors = sum(
            item["severity"] == "error" for item in findings
        )
        warnings = sum(
            item["severity"] == "warning" for item in findings
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Findings", len(findings))
        col2.metric("Errors", errors)
        col3.metric("Warnings", warnings)

        if not findings:
            st.success("No issues detected!")

        for item in findings:
            with st.expander(
                f"{item['rule']} · Line {item['line']} · "
                f"{item['message']}"
            ):
                st.write("**Severity:**", item["severity"])

                suggestion = item.get("suggested_fix", {})
                st.write(
                    "**Suggested fix:**",
                    suggestion.get(
                        "suggestion",
                        "Review this issue manually.",
                    ),
                )

        st.download_button(
            "Download JSON Report",
            data=report_path.read_text(encoding="utf-8"),
            file_name="codepilot_report.json",
            mime="application/json",
        )
