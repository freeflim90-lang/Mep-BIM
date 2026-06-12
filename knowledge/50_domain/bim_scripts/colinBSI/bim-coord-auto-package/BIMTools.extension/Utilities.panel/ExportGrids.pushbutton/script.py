"""
ExportGrids — Exports grid line positions and level elevations to CSV.

Outputs (to C:\BIM_Automation\data\output\):
  grid_lines.csv       — GridName, Orientation (H/V), Position (feet)
  level_elevations.csv — LevelName, Elevation (feet)

Run once when grid layout is established. Re-run if grids change.
Used by clash_parser.py to map clash XYZ to GridZone and Level.
Read-only. No model changes.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Grid, Level

# UnitUtils API changed in Revit 2022 — handle both
try:
    from Autodesk.Revit.DB import UnitUtils, UnitTypeId
    def to_feet(v):
        return UnitUtils.ConvertFromInternalUnits(v, UnitTypeId.Feet)
except ImportError:
    from Autodesk.Revit.DB import UnitUtils, DisplayUnitType
    def to_feet(v):
        return UnitUtils.ConvertFromInternalUnits(v, DisplayUnitType.DUT_DECIMAL_FEET)

from bim_utils import write_csv
from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

GRID_FILE = "grid_lines.csv"
LEVEL_FILE = "level_elevations.csv"
GRID_HEADERS = ["GridName", "Orientation", "Position"]
LEVEL_HEADERS = ["LevelName", "Elevation"]


def get_orientation_and_position(grid):
    """Return ('V', x_midpoint) or ('H', y_midpoint) for a Grid element."""
    curve = grid.Curve
    start = curve.GetEndPoint(0)
    end = curve.GetEndPoint(1)
    dx = abs(end.X - start.X)
    dy = abs(end.Y - start.Y)
    mid_x = (start.X + end.X) / 2.0
    mid_y = (start.Y + end.Y) / 2.0
    if dy > dx:
        # Runs mostly in Y direction — vertical grid line, position = X
        return "V", round(to_feet(mid_x), 4)
    else:
        # Runs mostly in X direction — horizontal grid line, position = Y
        return "H", round(to_feet(mid_y), 4)


def run():
    # Export grids
    grids = list(FilteredElementCollector(doc).OfClass(Grid).ToElements())
    grid_rows = []
    for g in grids:
        orientation, position = get_orientation_and_position(g)
        grid_rows.append([g.Name, orientation, position])
    grid_rows.sort(key=lambda r: (r[1], r[2]))
    grid_path = write_csv(GRID_FILE, GRID_HEADERS, grid_rows)

    # Export levels
    levels = list(FilteredElementCollector(doc).OfClass(Level).ToElements())
    level_rows = []
    for lv in levels:
        level_rows.append([lv.Name, round(to_feet(lv.Elevation), 4)])
    level_rows.sort(key=lambda r: r[1])
    level_path = write_csv(LEVEL_FILE, LEVEL_HEADERS, level_rows)

    output.print_md(
        "**Grid lines exported:** `{}` — {} grid(s)  \n"
        "**Level elevations exported:** `{}` — {} level(s)".format(
            grid_path, len(grid_rows),
            level_path, len(level_rows),
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
