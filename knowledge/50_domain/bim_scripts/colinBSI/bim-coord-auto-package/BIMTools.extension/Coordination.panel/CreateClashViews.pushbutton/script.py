"""
CreateClashViews — Creates one 3D view per discipline pair for clash review.
View names: "3D - Clash - DISC_A vs DISC_B"
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
    View,
    Transaction,
)

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

DISCIPLINES = ["Arch", "Structure", "Mechanical", "Electrical", "Plumbing", "Civil"]


def get_pairs(disciplines):
    pairs = []
    for i, a in enumerate(disciplines):
        for b in disciplines[i + 1:]:
            pairs.append((a, b))
    return pairs


def get_3d_vft():
    for vft in FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements():
        if vft.ViewFamily == ViewFamily.ThreeDimensional:
            return vft
    return None


def run():
    vft = get_3d_vft()
    if vft is None:
        output.print_md("**Error:** No 3D ViewFamilyType found.")
        return

    existing_names = {
        v.Name
        for v in FilteredElementCollector(doc).OfClass(View).ToElements()
        if not v.IsTemplate
    }

    pairs = get_pairs(DISCIPLINES)
    to_create = []
    for a, b in pairs:
        name = "3D - Clash - {} vs {}".format(a, b)
        if name not in existing_names:
            to_create.append((name,))

    if not to_create:
        output.print_md(
            "**Done:** All {} clash views already exist.".format(len(pairs))
        )
        return

    with Transaction(doc, "Create Clash Views") as t:
        t.Start()
        for (name,) in to_create:
            view = View3D.CreateIsometric(doc, vft.Id)
            view.Name = name
        t.Commit()

    output.print_md(
        "**Created {} clash view(s).**".format(len(to_create))
    )
    skipped = len(pairs) - len(to_create)
    if skipped:
        output.print_md("**Skipped {} already existing.**".format(skipped))


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
