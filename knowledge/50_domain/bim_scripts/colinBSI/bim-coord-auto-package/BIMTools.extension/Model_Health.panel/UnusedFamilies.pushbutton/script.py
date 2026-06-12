"""
UnusedFamilies — Lists families with no placed instances.
Columns: RunDate, ModelName, FamilyName, Category, TypeCount
List-only: no automatic purge. Outputs unused_families_report.csv.
Read-only. No model changes.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstance

from bim_utils import write_csv, today, get_families

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "unused_families_report.csv"
HEADERS = ["RunDate", "ModelName", "FamilyName", "Category", "TypeCount"]


def run():
    # Collect all family names that have at least one placed instance
    placed_family_names = set()
    for inst in FilteredElementCollector(doc).OfClass(FamilyInstance).ToElements():
        try:
            placed_family_names.add(inst.Symbol.Family.Name)
        except Exception:
            pass

    families = get_families(doc)
    unused = [f for f in families if f.Name not in placed_family_names]

    if not unused:
        output.print_md("**No unused families found.**")
        return

    run_date = today()
    model_name = doc.Title
    rows = []
    for fam in unused:
        cat_name = fam.FamilyCategory.Name if fam.FamilyCategory else "Unknown"
        type_count = fam.GetFamilySymbolIds().Count
        rows.append([run_date, model_name, fam.Name, cat_name, type_count])

    rows.sort(key=lambda r: r[3])
    path = write_csv(FILENAME, HEADERS, rows)
    output.print_md(
        "**Unused families report written:** `{}`  \n"
        "{} unused familie(s) found. No automatic purge performed.".format(
            path, len(unused)
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
