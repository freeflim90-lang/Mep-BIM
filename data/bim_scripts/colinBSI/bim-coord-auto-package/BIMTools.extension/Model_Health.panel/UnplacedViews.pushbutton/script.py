"""
UnplacedViews — Reports views not placed on any sheet.
Columns: RunDate, ModelName, ViewName, ViewType, Discipline, Level
Read-only. No model changes.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    View,
    ViewSheet,
    Viewport,
    BuiltInParameter,
)

from bim_utils import write_csv, today, get_views

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "unplaced_views_report.csv"
HEADERS = ["RunDate", "ModelName", "ViewName", "ViewType", "Discipline", "Level"]


def get_placed_view_ids():
    placed = set()
    for vp in FilteredElementCollector(doc).OfClass(Viewport).ToElements():
        placed.add(vp.ViewId)
    return placed


def get_param_value(elem, bip):
    p = elem.get_Parameter(bip)
    if p:
        return p.AsString() or p.AsValueString() or ""
    return ""


def run():
    placed_ids = get_placed_view_ids()
    views = get_views(doc, exclude_templates=True)

    unplaced = [v for v in views if v.Id not in placed_ids]

    if not unplaced:
        output.print_md("**All views are placed on sheets.**")
        return

    run_date = today()
    model_name = doc.Title
    rows = []
    for v in unplaced:
        discipline = get_param_value(v, BuiltInParameter.VIEW_DISCIPLINE)
        level = get_param_value(v, BuiltInParameter.PLAN_VIEW_LEVEL)
        rows.append([
            run_date, model_name,
            v.Name,
            str(v.ViewType),
            discipline,
            level,
        ])

    rows.sort(key=lambda r: r[3])
    path = write_csv(FILENAME, HEADERS, rows)
    output.print_md(
        "**Unplaced views report written:** `{}`  \n"
        "{} unplaced view(s) out of {}.".format(path, len(unplaced), len(views))
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
