"""
SetupViews — Creates 7 standard BIM coordination 3D views.
Idempotent: skips views that already exist by name.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    ViewFamilyType,
    ViewFamily,
    View3D,
    Transaction,
    View,
)

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

STANDARD_VIEWS = [
    "3D - Coordination",
    "3D - Navisworks",
    "3D - Clash Review",
    "3D - Worksets",
    "3D - Linked Models",
    "3D - QAQC",
    "3D - Scan Reference",
]


def get_3d_view_family_type():
    for vft in FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements():
        if vft.ViewFamily == ViewFamily.ThreeDimensional:
            return vft
    return None


def run():
    vft = get_3d_view_family_type()
    if vft is None:
        output.print_md("**Error:** No 3D ViewFamilyType found in this model.")
        return

    existing_names = {
        v.Name
        for v in FilteredElementCollector(doc).OfClass(View).ToElements()
        if not v.IsTemplate
    }

    to_create = [name for name in STANDARD_VIEWS if name not in existing_names]

    if not to_create:
        output.print_md("**Done:** All 7 standard 3D views already exist.")
        return

    with Transaction(doc, "Create Standard 3D Views") as t:
        t.Start()
        for name in to_create:
            view = View3D.CreateIsometric(doc, vft.Id)
            view.Name = name
        t.Commit()

    output.print_md(
        "**Created {} view(s):** {}".format(len(to_create), ", ".join(to_create))
    )
    skipped = len(STANDARD_VIEWS) - len(to_create)
    if skipped:
        output.print_md("**Skipped {} already existing.**".format(skipped))


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
