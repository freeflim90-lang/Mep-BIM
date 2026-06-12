"""
ClashSummary — Summarizes Clash_Status values from all model elements.
Columns: RunDate, ModelName, Status, Count
Outputs clash_summary_report.csv. Read-only.
"""
import traceback
from collections import Counter

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, StorageType

from bim_utils import write_csv, today

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "clash_summary_report.csv"
HEADERS = ["RunDate", "ModelName", "Status", "Count"]

KNOWN_STATUSES = ["Open", "In Progress", "Resolved"]


def run():
    all_elems = list(
        FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()
    )

    status_counts = Counter()
    for elem in all_elems:
        p = elem.LookupParameter("Clash_Status")
        if p and p.StorageType == StorageType.String:
            val = p.AsString()
            if val and val.strip():
                status_counts[val.strip()] += 1

    if not status_counts:
        output.print_md(
            "**No elements with Clash_Status found.** "
            "Run Clash Status Manager to tag elements first."
        )
        return

    run_date = today()
    model_name = doc.Title
    rows = []
    for status in KNOWN_STATUSES:
        rows.append([run_date, model_name, status, status_counts.get(status, 0)])
    # Include any unexpected status values
    for status, count in status_counts.items():
        if status not in KNOWN_STATUSES:
            rows.append([run_date, model_name, status, count])

    path = write_csv(FILENAME, HEADERS, rows)
    total = sum(status_counts.values())
    output.print_md(
        "**Clash summary written:** `{}`  \n"
        "Total tagged: {} — {}".format(
            path, total,
            " | ".join("{}: {}".format(s, status_counts.get(s, 0)) for s in KNOWN_STATUSES)
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
