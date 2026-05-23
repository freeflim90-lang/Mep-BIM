"""
ColorByWorkset — Applies solid fill color overrides by workset in active view.
Active view only. Uses 8-color cycle. Resets on re-run.
No permanent model changes beyond view graphics overrides.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    FillPatternElement,
    FillPatternTarget,
    OverrideGraphicSettings,
    Color,
    Transaction,
    WorksetKind,
    FilteredWorksetCollector,
    ElementWorksetFilter,
)

from pyrevit import revit, script

doc = revit.doc
uidoc = revit.uidoc
output = script.get_output()

# 8-color palette (R, G, B)
COLORS = [
    (255, 99, 71),   # Tomato
    (70, 130, 180),  # Steel Blue
    (60, 179, 113),  # Medium Sea Green
    (255, 165, 0),   # Orange
    (147, 112, 219), # Medium Purple
    (0, 206, 209),   # Dark Turquoise
    (240, 128, 128), # Light Coral
    (154, 205, 50),  # Yellow Green
]


def get_solid_fill_id():
    for pat in FilteredElementCollector(doc).OfClass(FillPatternElement).ToElements():
        fp = pat.GetFillPattern()
        if fp.Target == FillPatternTarget.Drafting and fp.IsSolidFill:
            return pat.Id
    return None


def run():
    active_view = uidoc.ActiveView
    if active_view is None:
        output.print_md("**Error:** No active view.")
        return

    solid_id = get_solid_fill_id()
    if solid_id is None:
        output.print_md("**Error:** No solid fill pattern found in document.")
        return

    if not doc.IsWorkshared:
        output.print_md("**Error:** Model is not workshared — no worksets.")
        return

    worksets = list(
        FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
    )

    with Transaction(doc, "Color by Workset") as t:
        t.Start()
        for idx, ws in enumerate(worksets):
            r, g, b = COLORS[idx % len(COLORS)]
            ogs = OverrideGraphicSettings()
            ogs.SetSurfaceForegroundPatternId(solid_id)
            ogs.SetSurfaceForegroundPatternColor(Color(r, g, b))
            ogs.SetSurfaceForegroundPatternVisible(True)

            # Apply to all elements in this workset
            filt = ElementWorksetFilter(ws.Id, False)
            for elem in FilteredElementCollector(doc, active_view.Id).WherePasses(filt).ToElements():
                try:
                    active_view.SetElementOverrides(elem.Id, ogs)
                except Exception:
                    pass
        t.Commit()

    output.print_md(
        "**Color by Workset applied** to '{}' — {} workset(s).".format(
            active_view.Name, len(worksets)
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
