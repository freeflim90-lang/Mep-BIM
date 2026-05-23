"""
GridCoordinateFinder — Click any point in the model to get its coordinates.

Reports:
- Nearest grid lines (V and H)
- Nearest level
- Survey coordinates (Easting, Northing, Elevation)
- Model XYZ coordinates (feet)

Requires CoordinateSetup to have been run first.
Read-only. No model changes.
"""
import traceback
import math

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Grid, Level

# UnitUtils API changed in Revit 2022
try:
    from Autodesk.Revit.DB import UnitUtils, UnitTypeId
    def to_feet(v):
        return UnitUtils.ConvertFromInternalUnits(v, UnitTypeId.Feet)
except ImportError:
    from Autodesk.Revit.DB import UnitUtils, DisplayUnitType
    def to_feet(v):
        return UnitUtils.ConvertFromInternalUnits(v, DisplayUnitType.DUT_DECIMAL_FEET)

from pyrevit import revit, script
from coord_utils import load_coords, to_survey

uidoc  = revit.uidoc
doc    = revit.doc
output = script.get_output()


def nearest_grid(grids, x, y):
    """Return (nearest_V_name, nearest_H_name) for a given model XY point (internal units)."""
    best_v = (None, float("inf"))
    best_h = (None, float("inf"))
    for g in grids:
        curve = g.Curve
        start = curve.GetEndPoint(0)
        end   = curve.GetEndPoint(1)
        dx = abs(end.X - start.X)
        dy = abs(end.Y - start.Y)
        if dy > dx:
            # Vertical grid (runs in Y direction) — compare X distance
            mid_x = (start.X + end.X) / 2.0
            dist = abs(x - mid_x)
            if dist < best_v[1]:
                best_v = (g.Name, dist)
        else:
            # Horizontal grid (runs in X direction) — compare Y distance
            mid_y = (start.Y + end.Y) / 2.0
            dist = abs(y - mid_y)
            if dist < best_h[1]:
                best_h = (g.Name, dist)
    return best_v[0], best_h[0]


def nearest_level(levels, z):
    """Return name of the level closest to z (internal units)."""
    best = min(levels, key=lambda lv: abs(lv.Elevation - z))
    return best.Name


def run():
    coords = load_coords(doc)
    if coords is None:
        output.print_md(
            "**No coordinate data found.**\n"
            "Run **CoordinateSetup** first."
        )
        return

    # Pick point in model
    try:
        point = uidoc.Selection.PickPoint("Click a point in the model")
    except Exception:
        return  # user cancelled

    x = point.X
    y = point.Y
    z = point.Z

    # Collect grids and levels live from model
    grids  = list(FilteredElementCollector(doc).OfClass(Grid).ToElements())
    levels = list(FilteredElementCollector(doc).OfClass(Level).ToElements())

    if not grids:
        output.print_md("**No grids found in model.**")
        return
    if not levels:
        output.print_md("**No levels found in model.**")
        return

    grid_v, grid_h = nearest_grid(grids, x, y)
    level_name     = nearest_level(levels, z)

    # Convert to feet for display and survey transform
    x_ft = round(to_feet(x), 3)
    y_ft = round(to_feet(y), 3)
    z_ft = round(to_feet(z), 3)

    # Reverse-transform model coords → survey coords
    e, n, elev = to_survey(
        x_ft, y_ft, z_ft,
        coords["easting"], coords["northing"], coords["elevation"],
        coords["rotation_deg"]
    )

    # Print result
    output.print_md("## Point Coordinates\n")
    output.print_md(
        "| Field | Value |\n|---|---|\n"
        "| Grid (V / H) | {} / {} |\n"
        "| Level | {} |\n"
        "| Easting | {:.3f} |\n"
        "| Northing | {:.3f} |\n"
        "| Elevation | {:.3f} ft |\n"
        "| Model X | {:.3f} ft |\n"
        "| Model Y | {:.3f} ft |\n"
        "| Model Z | {:.3f} ft |".format(
            grid_v or "?", grid_h or "?",
            level_name,
            e, n, elev,
            x_ft, y_ft, z_ft
        )
    )

    one_liner = "Grid {}{} | {} | E {:.3f} N {:.3f} EL {:.3f} ft".format(
        grid_v or "?", grid_h or "?", level_name, e, n, elev
    )
    output.print_md("\n**Copy-paste:**  `{}`".format(one_liner))

    # Copy to clipboard via .NET
    try:
        import System.Windows.Forms as WinForms
        WinForms.Clipboard.SetText(one_liner)
        output.print_md("*Copied to clipboard.*")
    except Exception:
        pass  # clipboard not available in all pyRevit contexts


try:
    run()
except Exception:
    output.print_md("**Error in GridCoordinateFinder:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
