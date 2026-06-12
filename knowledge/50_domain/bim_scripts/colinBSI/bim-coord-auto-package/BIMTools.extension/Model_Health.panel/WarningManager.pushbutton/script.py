"""
WarningManager — Exports model warnings summary to warnings_report.csv.
Columns: Description, Count, Severity
Read-only. No model changes.
"""
import traceback
from collections import defaultdict

from bim_utils import write_csv, today

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "warnings_report.csv"
HEADERS = ["RunDate", "ModelName", "Description", "Count", "Severity"]


def classify_severity(description):
    desc_lower = description.lower()
    if any(kw in desc_lower for kw in ["error", "corrupt", "missing", "unresolved"]):
        return "Critical"
    if any(kw in desc_lower for kw in ["overlap", "duplicate", "identical"]):
        return "High"
    return "Medium"


def run():
    warnings = list(doc.GetWarnings())

    if not warnings:
        output.print_md("**No warnings found in this model.**")
        return

    counts = defaultdict(int)
    for w in warnings:
        counts[w.GetDescriptionText()] += 1

    run_date = today()
    model_name = doc.Title
    rows = []
    for desc, count in sorted(counts.items(), key=lambda x: -x[1]):
        rows.append([run_date, model_name, desc, count, classify_severity(desc)])

    path = write_csv(FILENAME, HEADERS, rows)
    output.print_md(
        "**Warnings report written:** `{}`  \n"
        "Total warnings: {} across {} unique descriptions.".format(
            path, len(warnings), len(counts)
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
