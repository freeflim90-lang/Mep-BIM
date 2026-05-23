"""
CoordinateSetup — Enter and store project coordinate values in the Revit model.

Stores: Easting, Northing, Elevation, Rotation, Reference Grid
Uses Extensible Storage — values travel with the .rvt file.
Prints a coordinate setup report. No model geometry changes.
"""
import traceback
from pyrevit import revit, forms, script
from coord_utils import save_coords, check_large_coords, calc_rotation

doc    = revit.doc
output = script.get_output()


def parse_float(s, label):
    try:
        return float(s.strip().replace(",", ""))
    except ValueError:
        forms.alert("Invalid value for {}: '{}'".format(label, s))
        return None


def run():
    # --- Primary inputs ---
    primary = forms.ask_for_string(
        default="748221.40, 2134556.20, 100.00, 12.5, A1",
        prompt=(
            "Enter project coordinates:\n"
            "Easting, Northing, Elevation, Rotation (deg), Reference Grid\n"
            "Example: 748221.40, 2134556.20, 100.00, 12.5, A1"
        ),
        title="CoordinateSetup"
    )
    if not primary:
        return

    parts = [p.strip() for p in primary.split(",")]
    if len(parts) != 5:
        forms.alert("Expected 5 values separated by commas.")
        return

    easting  = parse_float(parts[0], "Easting")
    northing = parse_float(parts[1], "Northing")
    elev     = parse_float(parts[2], "Elevation")
    rotation = parse_float(parts[3], "Rotation")
    ref_grid = parts[4].strip()

    if None in (easting, northing, elev, rotation):
        return

    # --- Optional: compute rotation from two grid points ---
    use_two = forms.alert(
        "Do you want to calculate rotation from two known grid points?\n"
        "(More accurate than manual entry)",
        yes=True, no=True
    )
    if use_two:
        pt2 = forms.ask_for_string(
            default="748300.00, 2134556.20",
            prompt=(
                "Enter second grid point (Easting2, Northing2):\n"
                "This will override the manual rotation entry."
            ),
            title="Second Grid Point"
        )
        if pt2:
            pts = [p.strip() for p in pt2.split(",")]
            if len(pts) == 2:
                e2 = parse_float(pts[0], "Easting2")
                n2 = parse_float(pts[1], "Northing2")
                if e2 is not None and n2 is not None:
                    rotation = calc_rotation(easting, northing, e2, n2)
                    output.print_md(
                        "**Rotation calculated from two points:** {:.4f}°".format(rotation)
                    )

    # --- Large coordinate warning ---
    warning = check_large_coords(easting, northing)
    if warning:
        output.print_md("**{}**".format(warning))

    # --- Save to Extensible Storage ---
    save_coords(doc, easting, northing, elev, rotation, ref_grid)

    # --- Print setup report ---
    output.print_md("## Coordinate Setup Report\n")
    output.print_md("**Reference Grid:** {}".format(ref_grid))
    output.print_md("\n### Survey Coordinates")
    output.print_md(
        "| Field | Value |\n|---|---|\n"
        "| Easting | {:.3f} |\n"
        "| Northing | {:.3f} |\n"
        "| Elevation | {:.3f} ft |\n"
        "| Rotation | {:.4f}° |".format(easting, northing, elev, rotation)
    )
    output.print_md("\n### Revit — What to set manually")
    output.print_md(
        "Survey Point:  E={:.3f}  N={:.3f}  Z={:.3f}\n"
        "Project Base Point:  0, 0, 0\n"
        "True North Rotation:  {:.4f}°".format(easting, northing, elev, rotation)
    )
    output.print_md("\n### AutoCAD / Plant3D / CADWorx — UCS")
    output.print_md(
        "Origin:  {:.3f}, {:.3f}, {:.3f}\n"
        "Rotation (Z):  {:.4f}°".format(easting, northing, elev, rotation)
    )
    output.print_md(
        "\n*Coordinate values saved to model. "
        "Run ExportCADUCS to generate setup files.*"
    )


try:
    run()
except Exception:
    output.print_md("**Error in CoordinateSetup:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
