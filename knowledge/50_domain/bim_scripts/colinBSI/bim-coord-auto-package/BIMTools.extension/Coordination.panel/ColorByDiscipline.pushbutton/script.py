"""
ColorByDiscipline — Applies solid fill color overrides by Discipline parameter in active view.
Active view only. Uses 8-color cycle keyed to unique Discipline values found.
No permanent model changes beyond view graphics overrides.
"""
import traceback
from collections import defaultdict

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    FillPatternElement,
    FillPatternTarget,
    OverrideGraphicSettings,
    Color,
    Transaction,
    StorageType,
)

from pyrevit import revit, script

doc = revit.doc
uidoc = revit.uidoc
output = script.get_output()

COLORS = [
    (255, 99, 71),
    (70, 130, 180),
    (60, 179, 113),
    (255, 165, 0),
    (147, 112, 219),
    (0, 206, 209),
    (240, 128, 128),
    (154, 205, 50),
]


def get_solid_fill_id():
    for pat in FilteredElementCollector(doc).OfClass(FillPatternElement).ToElements():
        fp = pat.GetFillPattern()
        if fp.Target == FillPatternTarget.Drafting and fp.IsSolidFill:
            return pat.Id
    return None


def get_discipline(elem):
    p = elem.LookupParameter("Discipline")
    if p and p.StorageType == StorageType.String:
        val = p.AsString()
        return val.strip() if val else ""
    return ""


def run():
    active_view = uidoc.ActiveView
    if active_view is None:
        output.print_md("**Error:** No active view.")
        return

    solid_id = get_solid_fill_id()
    if solid_id is None:
        output.print_md("**Error:** No solid fill pattern found.")
        return

    # Collect elements in view and group by Discipline
    all_elems = list(FilteredElementCollector(doc, active_view.Id).ToElements())
    discipline_map = defaultdict(list)
    for elem in all_elems:
        disc = get_discipline(elem)
        if disc:
            discipline_map[disc].append(elem)

    if not discipline_map:
        output.print_md(
            "**No elements with Discipline parameter found in active view.**"
        )
        return

    disciplines = sorted(discipline_map.keys())
    color_assignments = {disc: COLORS[i % len(COLORS)] for i, disc in enumerate(disciplines)}

    with Transaction(doc, "Color by Discipline") as t:
        t.Start()
        for disc, elems in discipline_map.items():
            r, g, b = color_assignments[disc]
            ogs = OverrideGraphicSettings()
            ogs.SetSurfaceForegroundPatternId(solid_id)
            ogs.SetSurfaceForegroundPatternColor(Color(r, g, b))
            ogs.SetSurfaceForegroundPatternVisible(True)
            for elem in elems:
                try:
                    active_view.SetElementOverrides(elem.Id, ogs)
                except Exception:
                    pass
        t.Commit()

    output.print_md(
        "**Color by Discipline applied** — {} discipline(s): {}".format(
            len(disciplines), ", ".join(disciplines)
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
