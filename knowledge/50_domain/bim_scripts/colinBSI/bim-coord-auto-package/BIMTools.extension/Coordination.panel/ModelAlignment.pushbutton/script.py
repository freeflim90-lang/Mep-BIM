"""
ModelAlignment — Scan all linked Revit models and report alignment vs host.

Compares each RevitLinkInstance transform against Identity (host = reference at 0,0,0 / 0°).
Flags offsets and rotation differences beyond tolerance.

Tolerances:
  Translation XY:  0.05 ft
  Elevation Z:     0.02 ft
  Rotation:        0.05 degrees

Read-only. No model changes. No auto-align in v1.
"""
import traceback
import math

import clr
clr.AddReference("RevitAPI")

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
from bim_utils import get_links

doc    = revit.doc
output = script.get_output()

TRANS_TOL   = 0.05   # ft
ELEV_TOL    = 0.02   # ft
ROT_TOL_DEG = 0.05   # degrees


def classify(offset_xy, offset_z, rot_deg):
    flags = []
    if abs(offset_xy) > TRANS_TOL:
        flags.append("OFFSET")
    if abs(offset_z) > ELEV_TOL:
        flags.append("ELEVATION")
    if abs(rot_deg) > ROT_TOL_DEG:
        flags.append("ROTATION")
    return " + ".join(flags) if flags else "OK"


def run():
    links = get_links(doc)

    if not links:
        output.print_md("**No linked models found in this file.**")
        return

    output.print_md("## Model Alignment Report\n")
    output.print_md(
        "| Linked Model | Offset XY (ft) | Offset Z (ft) | Rotation (°) | Status |\n"
        "|---|---|---|---|---|"
    )

    any_issues = False
    for link in links:
        transform = link.GetTransform()

        x_ft = round(to_feet(transform.Origin.X), 4)
        y_ft = round(to_feet(transform.Origin.Y), 4)
        z_ft = round(to_feet(transform.Origin.Z), 4)

        offset_xy = round(math.sqrt(x_ft ** 2 + y_ft ** 2), 4)
        rotation  = round(
            math.degrees(math.atan2(transform.BasisX.Y, transform.BasisX.X)), 4
        )

        st = classify(offset_xy, z_ft, rotation)
        if st != "OK":
            any_issues = True

        mark = "**" if st != "OK" else ""
        output.print_md(
            "| {} | {} | {} | {} | {}{}{} |".format(
                link.Name,
                offset_xy,
                z_ft,
                rotation,
                mark, st, mark
            )
        )

    if any_issues:
        output.print_md(
            "\n**Misaligned models detected.**  \n"
            "Coordinate with model owners to realign using Shared Coordinates.  \n"
            "Tolerances: XY={} ft  |  Z={} ft  |  Rotation={}°".format(
                TRANS_TOL, ELEV_TOL, ROT_TOL_DEG
            )
        )
    else:
        output.print_md("\n**All linked models are aligned within tolerance.**")


try:
    run()
except Exception:
    output.print_md("**Error in ModelAlignment:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
