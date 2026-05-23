"""
CreateWorksets — Creates 11 standard BIM coordination worksets.
Idempotent: skips worksets that already exist.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Transaction, WorksetKind, FilteredWorksetCollector

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

STANDARD_WORKSETS = [
    "Shared Levels & Grids",
    "Arch",
    "Structure",
    "Mechanical",
    "Electrical",
    "Plumbing",
    "Civil",
    "Plant",
    "Links",
    "Coordination",
    "Scan",
]


def run():
    if not doc.IsWorkshared:
        output.print_md("**Error:** This model is not workshared. Enable worksharing first.")
        return

    existing = {
        ws.Name
        for ws in FilteredWorksetCollector(doc)
        .OfKind(WorksetKind.UserWorkset)
        .ToWorksets()
    }

    to_create = [name for name in STANDARD_WORKSETS if name not in existing]

    if not to_create:
        output.print_md("**Done:** All 11 standard worksets already exist.")
        return

    with Transaction(doc, "Create Standard Worksets") as t:
        t.Start()
        for name in to_create:
            from Autodesk.Revit.DB import Workset as WS
            WS.Create(doc, name)
        t.Commit()

    output.print_md(
        "**Created {} workset(s):** {}".format(len(to_create), ", ".join(to_create))
    )
    skipped = len(STANDARD_WORKSETS) - len(to_create)
    if skipped:
        output.print_md("**Skipped {} already existing.**".format(skipped))


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
