"""
FindLargeFamilies — Reports families sorted by instance count (size proxy).
Columns: RunDate, ModelName, FamilyName, Category, SymbolCount, InstanceCount
Read-only. No model changes.

Note: Revit API does not expose raw family file size in bytes.
Instance and symbol counts are the best available size proxy via API.
"""
import traceback
from collections import defaultdict

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstance

from bim_utils import write_csv, today, get_families

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "large_families_report.csv"
HEADERS = [
    "RunDate", "ModelName", "FamilyName", "Category",
    "SymbolCount", "InstanceCount",
]


def run():
    families = get_families(doc)

    # Count instances per family name
    instance_counts = defaultdict(int)
    for inst in FilteredElementCollector(doc).OfClass(FamilyInstance).ToElements():
        try:
            fam_name = inst.Symbol.Family.Name
            instance_counts[fam_name] += 1
        except Exception:
            pass

    run_date = today()
    model_name = doc.Title
    rows = []
    for fam in families:
        cat_name = fam.FamilyCategory.Name if fam.FamilyCategory else "Unknown"
        symbol_count = fam.GetFamilySymbolIds().Count
        inst_count = instance_counts.get(fam.Name, 0)
        rows.append([
            run_date, model_name,
            fam.Name, cat_name, symbol_count, inst_count,
        ])

    # Sort by instance count descending
    rows.sort(key=lambda r: -r[5])

    path = write_csv(FILENAME, HEADERS, rows)
    output.print_md(
        "**Large families report written:** `{}`  \n"
        "{} families listed.".format(path, len(rows))
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
