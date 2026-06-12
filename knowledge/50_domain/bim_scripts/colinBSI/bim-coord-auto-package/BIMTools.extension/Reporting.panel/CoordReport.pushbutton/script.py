"""
CoordReport — Compiles coordination summary from existing output CSVs.
Source CSVs (from BIM_Automation/data/output/):
  model_health_scores.csv, warnings_report.csv,
  unplaced_views_report.csv, cad_imports_report.csv
Output: coordination_report.csv
Missing source CSVs show N/A — not an error.
"""
import traceback
import csv
import os

from bim_utils import write_csv, today, OUTPUT_DIR

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "coordination_report.csv"
HEADERS = [
    "RunDate", "ModelName",
    "HealthScore", "HealthStatus",
    "WarningCount",
    "UnplacedViewCount",
    "CADImportCount",
]

SOURCE_FILES = {
    "health": "model_health_scores.csv",
    "warnings": "warnings_report.csv",
    "unplaced": "unplaced_views_report.csv",
    "cad": "cad_imports_report.csv",
}


def read_csv_rows(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        return None
    rows = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def latest_for_model(rows, model_name_col, model_name):
    """Return last matching row for this model, or None."""
    if not rows:
        return None
    matches = [r for r in rows if r.get(model_name_col, "") == model_name]
    return matches[-1] if matches else None


def run():
    model_name = doc.Title

    health_rows = read_csv_rows(SOURCE_FILES["health"])
    warning_rows = read_csv_rows(SOURCE_FILES["warnings"])
    unplaced_rows = read_csv_rows(SOURCE_FILES["unplaced"])
    cad_rows = read_csv_rows(SOURCE_FILES["cad"])

    # Health score
    health_row = latest_for_model(health_rows, "ModelName", model_name)
    health_score = health_row["TotalScore"] if health_row else "N/A"
    health_status = health_row["Status"] if health_row else "N/A"

    # Warning count from warnings_report
    if warning_rows is not None:
        model_warnings = [r for r in warning_rows if r.get("ModelName") == model_name]
        warning_count = sum(int(r.get("Count", 0)) for r in model_warnings)
    else:
        warning_count = "N/A"

    # Unplaced view count
    if unplaced_rows is not None:
        unplaced_count = sum(
            1 for r in unplaced_rows if r.get("ModelName") == model_name
        )
    else:
        unplaced_count = "N/A"

    # CAD import count
    if cad_rows is not None:
        cad_count = sum(1 for r in cad_rows if r.get("ModelName") == model_name)
    else:
        cad_count = "N/A"

    row = [
        today(), model_name,
        health_score, health_status,
        warning_count, unplaced_count, cad_count,
    ]

    path = write_csv(FILENAME, HEADERS, [row])
    output.print_md("**Coordination report written:** `{}`".format(path))
    output.print_md(
        "Health: {} ({}) | Warnings: {} | Unplaced views: {} | CAD imports: {}".format(
            health_score, health_status, warning_count, unplaced_count, cad_count
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
