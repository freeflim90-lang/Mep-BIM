"""
CoordinateValidator — Compare stored coordinate values against actual Revit model setup.

Reads stored values from Extensible Storage and compares against:
- Survey Point position
- True North rotation

Flags any delta beyond tolerance. Read-only, no model changes.
Tolerances: translation 0.05 ft, elevation 0.02 ft, rotation 0.05 degrees.
"""
import traceback
import math

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BasePoint, XYZ

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
from coord_utils import load_coords

doc    = revit.doc
output = script.get_output()

TRANS_TOL   = 0.05   # feet
ELEV_TOL    = 0.02   # feet
ROT_TOL_DEG = 0.05   # degrees


def status(delta, tolerance):
    return "OK" if abs(delta) <= tolerance else "**MISMATCH**"


def run():
    coords = load_coords(doc)
    if coords is None:
        output.print_md(
            "**No coordinate data found.**\n"
            "Run **CoordinateSetup** first to store project coordinates."
        )
        return

    # --- Read Survey Point (IsShared = True) ---
    survey_pt = None
    for bp in FilteredElementCollector(doc).OfClass(BasePoint).ToElements():
        if bp.IsShared:
            survey_pt = bp
            break

    sp_e = to_feet(survey_pt.Position.X) if survey_pt else None
    sp_n = to_feet(survey_pt.Position.Y) if survey_pt else None
    sp_z = to_feet(survey_pt.Position.Z) if survey_pt else None

    # --- Read True North angle ---
    angle_deg = None
    try:
        pos = doc.ActiveProjectLocation.GetProjectPosition(XYZ.Zero)
        angle_deg = math.degrees(pos.Angle)
    except Exception:
        pass

    # --- Build results ---
    rows = []

    if sp_e is not None:
        delta_e = sp_e - coords["easting"]
        delta_n = sp_n - coords["northing"]
        delta_z = sp_z - coords["elevation"]
        rows.append(("Survey Point Easting",   "{:.3f}".format(coords["easting"]),   "{:.3f}".format(sp_e),   "{:.4f}".format(delta_e), status(delta_e, TRANS_TOL)))
        rows.append(("Survey Point Northing",  "{:.3f}".format(coords["northing"]),  "{:.3f}".format(sp_n),   "{:.4f}".format(delta_n), status(delta_n, TRANS_TOL)))
        rows.append(("Survey Point Elevation", "{:.3f}".format(coords["elevation"]), "{:.3f}".format(sp_z),   "{:.4f}".format(delta_z), status(delta_z, ELEV_TOL)))
    else:
        rows.append(("Survey Point", "N/A", "Not found in model", "-", "UNKNOWN"))

    if angle_deg is not None:
        delta_r = angle_deg - coords["rotation_deg"]
        rows.append(("True North Rotation (°)", "{:.4f}".format(coords["rotation_deg"]), "{:.4f}".format(angle_deg), "{:.4f}".format(delta_r), status(delta_r, ROT_TOL_DEG)))
    else:
        rows.append(("True North Rotation", "N/A", "Not found", "-", "UNKNOWN"))

    # --- Print table ---
    output.print_md("## Coordinate Validation Report\n")
    output.print_md(
        "| Check | Stored | Actual | Delta | Status |\n"
        "|---|---|---|---|---|"
    )
    for check, stored, actual, delta, st in rows:
        output.print_md("| {} | {} | {} | {} | {} |".format(
            check, stored, actual, delta, st
        ))

    mismatches = [r for r in rows if "MISMATCH" in r[4]]
    if mismatches:
        output.print_md(
            "\n**{} mismatch(es) found.**  \n"
            "Update Revit Survey Point and/or True North to match stored values, "
            "or re-run CoordinateSetup with corrected inputs.".format(len(mismatches))
        )
    else:
        output.print_md("\n**All checks passed.**")


try:
    run()
except Exception:
    output.print_md("**Error in CoordinateValidator:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
