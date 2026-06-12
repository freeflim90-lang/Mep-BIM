# BIM Coordinates Panel Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a `Coordinates.panel` (4 tools) and `ModelAlignment` to `Coordination.panel` in `BIMTools.extension`, backed by a shared `coord_utils.py` math/storage library.

**Architecture:** A new `lib/coord_utils.py` provides all coordinate math and Extensible Storage I/O. Five thin `script.py` files in their respective pushbutton folders import from it. Coordinate values are stored once in the Revit file via Extensible Storage and read by all tools.

**Tech Stack:** Python 2.7 (IronPython/pyRevit), Revit API, pyRevit forms/script, Autodesk.Revit.DB.ExtensibleStorage

**Design doc:** `docs/plans/2026-03-08-bim-coordinates-panel-design.md`

---

## Important Context

- This is a **pyRevit extension** running inside Revit under IronPython 2.7. No pytest. No external test runner.
- Verification = **read files back** after writing and check logic manually.
- Pure math functions in `coord_utils.py` can be verified with a standalone Python snippet (they have no Revit API dependencies).
- All scripts follow the existing pattern: `run()` wrapped in `try/except`, errors printed to output window.
- `from bim_utils import ...` works because pyRevit auto-adds `lib/` to sys.path.
- UnitUtils API changed in Revit 2022 — use the `try/except ImportError` pattern from `ExportGrids`.
- Extensible Storage requires `clr.AddReference("RevitAPI")` — already standard.
- `OUTPUT_DIR = r"C:\BIM_Automation\data\output"` — imported from `bim_utils`.

---

## Task 1: coord_utils.py — Shared Math + Storage Library

**Files:**
- Create: `BIMTools.extension/lib/coord_utils.py`

### Step 1: Write the file

```python
"""
coord_utils.py — Shared coordinate math and Extensible Storage I/O.

Import in any script with: from coord_utils import load_coords, to_survey, ...
"""
import math

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    DataStorage,
    Transaction,
)
from Autodesk.Revit.DB.ExtensibleStorage import (
    SchemaBuilder,
    AccessLevel,
    Entity,
    Schema,
)
import System

# ---------------------------------------------------------------------------
# Extensible Storage schema
# ---------------------------------------------------------------------------
_SCHEMA_GUID = System.Guid("4b7c9a2e-1f3d-4e8b-a5c6-d2e0f1b3a7c9")
_SCHEMA_NAME = "BIMCoordinates"

def _get_or_create_schema():
    existing = Schema.Lookup(_SCHEMA_GUID)
    if existing:
        return existing
    b = SchemaBuilder(_SCHEMA_GUID)
    b.SetSchemaName(_SCHEMA_NAME)
    b.SetReadAccessLevel(AccessLevel.Public)
    b.SetWriteAccessLevel(AccessLevel.Public)
    b.AddSimpleField("easting",      System.Double)
    b.AddSimpleField("northing",     System.Double)
    b.AddSimpleField("elevation",    System.Double)
    b.AddSimpleField("rotation_deg", System.Double)
    b.AddSimpleField("ref_grid",     System.String)
    return b.Finish()


def save_coords(doc, easting, northing, elevation, rotation_deg, ref_grid):
    """Store project coordinate values in Revit Extensible Storage."""
    schema = _get_or_create_schema()
    # Find existing DataStorage for this schema, or create one
    storage = None
    for ds in FilteredElementCollector(doc).OfClass(DataStorage).ToElements():
        if ds.GetEntity(schema).IsValid():
            storage = ds
            break
    t = Transaction(doc, "BIMTools: Save Coordinates")
    t.Start()
    if storage is None:
        storage = DataStorage.Create(doc)
    entity = Entity(schema)
    entity.Set("easting",      float(easting))
    entity.Set("northing",     float(northing))
    entity.Set("elevation",    float(elevation))
    entity.Set("rotation_deg", float(rotation_deg))
    entity.Set("ref_grid",     str(ref_grid))
    storage.SetEntity(entity)
    t.Commit()


def load_coords(doc):
    """
    Read project coordinate values from Extensible Storage.
    Returns dict with keys: easting, northing, elevation, rotation_deg, ref_grid
    Returns None if not set.
    """
    schema = Schema.Lookup(_SCHEMA_GUID)
    if schema is None:
        return None
    for ds in FilteredElementCollector(doc).OfClass(DataStorage).ToElements():
        entity = ds.GetEntity(schema)
        if entity.IsValid():
            return {
                "easting":      entity.Get[System.Double]("easting"),
                "northing":     entity.Get[System.Double]("northing"),
                "elevation":    entity.Get[System.Double]("elevation"),
                "rotation_deg": entity.Get[System.Double]("rotation_deg"),
                "ref_grid":     entity.Get[System.String]("ref_grid"),
            }
    return None


# ---------------------------------------------------------------------------
# Coordinate math
# ---------------------------------------------------------------------------

def to_model(easting, northing, elevation, ref_e, ref_n, base_z, rot_deg):
    """Convert survey coordinates to model (Revit internal) coordinates."""
    theta = math.radians(rot_deg)
    dx = easting  - ref_e
    dy = northing - ref_n
    x = dx * math.cos(theta) - dy * math.sin(theta)
    y = dx * math.sin(theta) + dy * math.cos(theta)
    z = elevation - base_z
    return round(x, 4), round(y, 4), round(z, 4)


def to_survey(x, y, z, ref_e, ref_n, base_z, rot_deg):
    """Convert model coordinates back to survey coordinates (reverse transform)."""
    theta = math.radians(rot_deg)
    e = ref_e + x * math.cos(theta) + y * math.sin(theta)
    n = ref_n - x * math.sin(theta) + y * math.cos(theta)
    elev = z + base_z
    return round(e, 4), round(n, 4), round(elev, 4)


def check_large_coords(easting, northing):
    """
    Return a warning string if survey coordinates are dangerously far from origin.
    Revit geometry becomes unstable beyond ~105,600 ft (20 miles).
    Returns None if coords are safe.
    """
    distance = math.sqrt(easting ** 2 + northing ** 2)
    if distance > 105600:
        shift_e = -(int(easting / 1000) * 1000)
        shift_n = -(int(northing / 1000) * 1000)
        return (
            "WARNING: Survey coordinates are {:.0f} ft from origin (limit ~105,600 ft).\n"
            "Recommended Revit origin shift: X={}, Y={}\n"
            "This keeps geometry stable while preserving survey values."
        ).format(distance, shift_e, shift_n)
    return None


def calc_rotation(e1, n1, e2, n2):
    """
    Calculate project north rotation (degrees) from two known grid points.
    Point 1 should be the reference (e.g. Grid A1), Point 2 a second known point.
    """
    return math.degrees(math.atan2(e2 - e1, n2 - n1))
```

### Step 2: Verify — read it back

Read `BIMTools.extension/lib/coord_utils.py` and confirm:
- Schema GUID is present and fixed
- `save_coords` creates a Transaction and uses `DataStorage.Create`
- `load_coords` returns `None` if schema not found
- `to_model` and `to_survey` are inverses of each other
- `check_large_coords` threshold is 105,600 ft

### Step 3: Verify math with a quick mental check

Forward: `to_model(748221.4, 2134556.2, 100, 748200, 2134500, 100, 0)` should give `(21.4, 56.2, 0.0)` (zero rotation, pure translation).

Reverse: `to_survey(21.4, 56.2, 0.0, 748200, 2134500, 100, 0)` should give back `(748221.4, 2134556.2, 100.0)`.

### Step 4: Commit

```bash
git add "BIMTools.extension/lib/coord_utils.py"
git commit -m "feat: add coord_utils.py — coordinate math and Extensible Storage I/O"
```

---

## Task 2: CoordinateSetup

**Files:**
- Create: `BIMTools.extension/Coordinates.panel/CoordinateSetup.pushbutton/script.py`

### Step 1: Write the file

```python
"""
CoordinateSetup — Enter and store project coordinate values in the Revit model.

Stores: Easting, Northing, Elevation, Rotation, Reference Grid
Uses Extensible Storage — values travel with the .rvt file.
Prints a coordinate setup report. No model geometry changes.
"""
import traceback
from pyrevit import revit, forms, script
from coord_utils import save_coords, check_large_coords, calc_rotation

doc   = revit.doc
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
```

### Step 2: Verify — read it back

Check:
- Imports `from coord_utils import save_coords, check_large_coords, calc_rotation`
- 5-value comma-separated input with parse error handling
- Optional second-point rotation path calls `calc_rotation`
- `save_coords` is called before the report
- Report covers Survey, Revit, and CAD sections
- `try/except` wraps `run()`

### Step 3: Commit

```bash
git add "BIMTools.extension/Coordinates.panel/CoordinateSetup.pushbutton/script.py"
git commit -m "feat: add CoordinateSetup — enter and store project coordinates"
```

---

## Task 3: CoordinateValidator

**Files:**
- Create: `BIMTools.extension/Coordinates.panel/CoordinateValidator.pushbutton/script.py`

### Step 1: Write the file

```python
"""
CoordinateValidator — Compare stored coordinate values against actual Revit model setup.

Reads stored values from Extensible Storage and compares against:
- Survey Point position
- Project Base Point offset
- True North rotation

Flags any delta beyond tolerance. Read-only, no model changes.
"""
import traceback
import math

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BasePoint

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
ROT_TOL_DEG = 0.05   # degrees
ELEV_TOL    = 0.02   # feet


def status(delta, tolerance):
    return "OK" if abs(delta) <= tolerance else "MISMATCH"


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
    pbp = None
    for bp in FilteredElementCollector(doc).OfClass(BasePoint).ToElements():
        if bp.IsShared:
            survey_pt = bp
        else:
            pbp = bp

    # Survey Point position (Revit internal → feet)
    sp_e = to_feet(survey_pt.Position.X) if survey_pt else None
    sp_n = to_feet(survey_pt.Position.Y) if survey_pt else None
    sp_z = to_feet(survey_pt.Position.Z) if survey_pt else None

    # True North angle (radians → degrees)
    try:
        angle_rad = doc.ActiveProjectLocation.GetProjectPosition(
            revit.doc.ActiveProjectLocation.GetProjectPosition.__self__
        ).Angle
    except Exception:
        # Fallback: access via project location
        try:
            from Autodesk.Revit.DB import XYZ
            pos = doc.ActiveProjectLocation.GetProjectPosition(XYZ.Zero)
            angle_rad = pos.Angle
        except Exception:
            angle_rad = None

    angle_deg = math.degrees(angle_rad) if angle_rad is not None else None

    # --- Build results table ---
    rows = []

    if sp_e is not None:
        delta_e = sp_e - coords["easting"]
        delta_n = sp_n - coords["northing"]
        delta_z = sp_z - coords["elevation"]
        rows.append(("Survey Point Easting",    coords["easting"],    sp_e,    delta_e, status(delta_e, TRANS_TOL)))
        rows.append(("Survey Point Northing",   coords["northing"],   sp_n,    delta_n, status(delta_n, TRANS_TOL)))
        rows.append(("Survey Point Elevation",  coords["elevation"],  sp_z,    delta_z, status(delta_z, ELEV_TOL)))
    else:
        rows.append(("Survey Point", "N/A", "Not found", "-", "UNKNOWN"))

    if angle_deg is not None:
        delta_r = angle_deg - coords["rotation_deg"]
        rows.append(("True North Rotation (°)", coords["rotation_deg"], angle_deg, delta_r, status(delta_r, ROT_TOL_DEG)))
    else:
        rows.append(("True North Rotation", "N/A", "Not found", "-", "UNKNOWN"))

    # --- Print table ---
    output.print_md("## Coordinate Validation Report\n")
    output.print_md(
        "| Check | Stored | Actual | Delta | Status |\n"
        "|---|---|---|---|---|"
    )
    for check, stored, actual, delta, st in rows:
        if isinstance(delta, float):
            delta_str = "{:.4f}".format(delta)
        else:
            delta_str = str(delta)
        mark = "" if st == "OK" else "**"
        output.print_md("| {} | {:.3f} | {:.3f} | {} | {}{}{} |".format(
            check,
            float(stored) if stored != "N/A" else 0,
            float(actual) if actual != "Not found" else 0,
            delta_str,
            mark, st, mark
        ))

    mismatches = [r for r in rows if r[4] not in ("OK", "UNKNOWN")]
    if mismatches:
        output.print_md(
            "\n**{} mismatch(es) found.** "
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
```

### Step 2: Verify — read it back

Check:
- `BasePoint` collector with `IsShared` distinguishes Survey Point from PBP
- `to_feet()` uses the 2022-compatible pattern
- `GetProjectPosition(XYZ.Zero).Angle` for true north
- Table rows cover Easting, Northing, Elevation, Rotation
- Tolerances match design doc (0.05 ft, 0.05°, 0.02 ft)

### Step 3: Commit

```bash
git add "BIMTools.extension/Coordinates.panel/CoordinateValidator.pushbutton/script.py"
git commit -m "feat: add CoordinateValidator — compare stored coords vs Revit model"
```

---

## Task 4: GridCoordinateFinder

**Files:**
- Create: `BIMTools.extension/Coordinates.panel/GridCoordinateFinder.pushbutton/script.py`

### Step 1: Write the file

```python
"""
GridCoordinateFinder — Click any point in the model to get its coordinates.

Reports:
- Nearest grid lines (H and V)
- Nearest level
- Survey coordinates (Easting, Northing, Elevation)
- Model XYZ coordinates

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
    """Return (nearest_V_name, nearest_H_name) for a given model XY point."""
    best_v = (None, float("inf"))  # (name, distance)
    best_h = (None, float("inf"))
    for g in grids:
        curve  = g.Curve
        start  = curve.GetEndPoint(0)
        end    = curve.GetEndPoint(1)
        dx = abs(end.X - start.X)
        dy = abs(end.Y - start.Y)
        if dy > dx:
            # Vertical grid (runs in Y) — compare X distance
            mid_x = (start.X + end.X) / 2.0
            dist = abs(x - mid_x)
            if dist < best_v[1]:
                best_v = (g.Name, dist)
        else:
            # Horizontal grid (runs in X) — compare Y distance
            mid_y = (start.Y + end.Y) / 2.0
            dist = abs(y - mid_y)
            if dist < best_h[1]:
                best_h = (g.Name, dist)
    return best_v[0], best_h[0]


def nearest_level(levels, z):
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

    # Collect grids and levels
    grids  = list(FilteredElementCollector(doc).OfClass(Grid).ToElements())
    levels = list(FilteredElementCollector(doc).OfClass(Level).ToElements())

    grid_v, grid_h = nearest_grid(grids, x, y)
    level_name     = nearest_level(levels, z)

    # Convert model coords to survey
    e, n, elev = to_survey(
        to_feet(x), to_feet(y), to_feet(z),
        coords["easting"], coords["northing"], coords["elevation"],
        coords["rotation_deg"]
    )

    x_ft = round(to_feet(x), 3)
    y_ft = round(to_feet(y), 3)
    z_ft = round(to_feet(z), 3)

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
            grid_v, grid_h, level_name,
            e, n, elev,
            x_ft, y_ft, z_ft
        )
    )

    # Clipboard-friendly one-liner
    one_liner = "Grid {}{} | {} | E {:.3f} N {:.3f} EL {:.3f} ft".format(
        grid_v or "?", grid_h or "?", level_name, e, n, elev
    )
    output.print_md("\n**Copy-paste:**  `{}`".format(one_liner))

    # Copy to clipboard (IronPython / .NET)
    try:
        import System.Windows.Forms as WinForms
        WinForms.Clipboard.SetText(one_liner)
        output.print_md("*Copied to clipboard.*")
    except Exception:
        pass  # clipboard not available in all environments


try:
    run()
except Exception:
    output.print_md("**Error in GridCoordinateFinder:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

### Step 2: Verify — read it back

Check:
- `nearest_grid` splits grids into V (dy > dx) and H correctly
- `PickPoint` is wrapped in try/except so cancel doesn't crash
- `to_feet()` is applied to Revit internal units before passing to `to_survey`
- Clipboard copy is wrapped in try/except (not available in all pyRevit contexts)
- Output table matches design doc format

### Step 3: Commit

```bash
git add "BIMTools.extension/Coordinates.panel/GridCoordinateFinder.pushbutton/script.py"
git commit -m "feat: add GridCoordinateFinder — click point to get survey coordinates"
```

---

## Task 5: ExportCADUCS

**Files:**
- Create: `BIMTools.extension/Coordinates.panel/ExportCADUCS.pushbutton/script.py`

### Step 1: Write the file

```python
"""
ExportCADUCS — Generate CAD coordinate setup files from stored project coordinates.

Outputs to C:\BIM_Automation\data\output\:
  autocad_setup.scr         — Runnable AutoCAD/Plant3D/CADWorx script
  revit_coord_setup.txt     — Human-readable Revit manual setup instructions
  coordinate_report.txt     — Full project coordinate summary

Requires CoordinateSetup to have been run first.
No model changes.
"""
import traceback
import os
from datetime import date

from pyrevit import revit, script
from bim_utils import OUTPUT_DIR
from coord_utils import load_coords

doc    = revit.doc
output = script.get_output()


def write_autocad_script(coords, path):
    content = (
        "; AutoCAD / Plant3D / CADWorx coordinate setup script\n"
        "; Generated by BIMTools ExportCADUCS — {date}\n"
        "; Run in AutoCAD: type SCRIPT and select this file\n"
        "\n"
        "UCS\nW\n"
        "UCS\nOrigin\n"
        "{e},{n},{z}\n"
        "UCS\nZ\n"
        "{rot}\n"
        "PLAN\nC\n"
    ).format(
        date=date.today().isoformat(),
        e=round(coords["easting"],      3),
        n=round(coords["northing"],     3),
        z=round(coords["elevation"],    3),
        rot=round(coords["rotation_deg"], 4),
    )
    with open(path, "w") as f:
        f.write(content)


def write_revit_setup(coords, path):
    content = (
        "REVIT COORDINATE SETUP INSTRUCTIONS\n"
        "Generated: {date}\n"
        "Reference Grid: {grid}\n"
        "=" * 50 + "\n\n"
        "1. Open Manage > Project Location > Specify Coordinates at a Point\n"
        "   OR manually move the Survey Point (unclip it first):\n\n"
        "   Survey Point\n"
        "   E (X):  {e:.3f} ft\n"
        "   N (Y):  {n:.3f} ft\n"
        "   Elev:   {z:.3f} ft\n\n"
        "2. Project Base Point: set to 0, 0, 0\n\n"
        "3. True North:\n"
        "   Manage > Project Location > Position > Rotate True North\n"
        "   Angle from Project North to True North: {rot:.4f} degrees\n\n"
        "4. Clip the Survey Point after setup.\n"
    ).format(
        date=date.today().isoformat(),
        grid=coords["ref_grid"],
        e=coords["easting"],
        n=coords["northing"],
        z=coords["elevation"],
        rot=coords["rotation_deg"],
    )
    with open(path, "w") as f:
        f.write(content)


def write_coord_report(coords, path):
    content = (
        "PROJECT COORDINATE REPORT\n"
        "Generated: {date}\n"
        "=" * 50 + "\n\n"
        "Reference Grid:    {grid}\n\n"
        "Survey Coordinates\n"
        "  Easting:         {e:.3f}\n"
        "  Northing:        {n:.3f}\n"
        "  Elevation:       {z:.3f} ft\n\n"
        "Project North Rotation\n"
        "  True North:      {rot:.4f} degrees\n\n"
        "Revit Setup\n"
        "  Survey Point =   {e:.3f}, {n:.3f}, {z:.3f}\n"
        "  Project Base Point = 0, 0, 0\n\n"
        "CAD Setup\n"
        "  UCS Origin =     {e:.3f}, {n:.3f}, {z:.3f}\n"
        "  UCS Rotation =   {rot:.4f} degrees\n"
    ).format(
        date=date.today().isoformat(),
        grid=coords["ref_grid"],
        e=coords["easting"],
        n=coords["northing"],
        z=coords["elevation"],
        rot=coords["rotation_deg"],
    )
    with open(path, "w") as f:
        f.write(content)


def run():
    coords = load_coords(doc)
    if coords is None:
        output.print_md(
            "**No coordinate data found.**\n"
            "Run **CoordinateSetup** first."
        )
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    scr_path    = os.path.join(OUTPUT_DIR, "autocad_setup.scr")
    revit_path  = os.path.join(OUTPUT_DIR, "revit_coord_setup.txt")
    report_path = os.path.join(OUTPUT_DIR, "coordinate_report.txt")

    write_autocad_script(coords, scr_path)
    write_revit_setup(coords,   revit_path)
    write_coord_report(coords,  report_path)

    output.print_md("## CAD Coordinate Package Exported\n")
    output.print_md(
        "| File | Path |\n|---|---|\n"
        "| AutoCAD script | `{}` |\n"
        "| Revit setup guide | `{}` |\n"
        "| Coordinate report | `{}` |".format(scr_path, revit_path, report_path)
    )
    output.print_md(
        "\n**AutoCAD / Plant3D / CADWorx:** type `SCRIPT` and select `autocad_setup.scr`"
    )


try:
    run()
except Exception:
    output.print_md("**Error in ExportCADUCS:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

### Step 2: Verify — read it back

Check:
- `autocad_setup.scr` has correct UCS command sequence with `W` reset first
- `revit_coord_setup.txt` gives step-by-step manual instructions (not API calls)
- `coordinate_report.txt` covers all five stored values
- All three file writes are in separate functions
- `os.makedirs(OUTPUT_DIR, exist_ok=True)` guards against missing directory

### Step 3: Commit

```bash
git add "BIMTools.extension/Coordinates.panel/ExportCADUCS.pushbutton/script.py"
git commit -m "feat: add ExportCADUCS — generate AutoCAD script and coordinate package"
```

---

## Task 6: ModelAlignment (Coordination.panel)

**Files:**
- Create: `BIMTools.extension/Coordination.panel/ModelAlignment.pushbutton/script.py`

### Step 1: Write the file

```python
"""
ModelAlignment — Scan all linked Revit models and report alignment vs host.

Compares each RevitLinkInstance transform against Identity (host = reference).
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
from Autodesk.Revit.DB import Transform

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

        status = classify(offset_xy, z_ft, rotation)
        if status != "OK":
            any_issues = True

        mark = "**" if status != "OK" else ""
        output.print_md(
            "| {} | {} | {} | {} | {}{}{} |".format(
                link.Name,
                x_ft if abs(x_ft) >= abs(y_ft) else y_ft,
                z_ft,
                rotation,
                mark, status, mark
            )
        )

    if any_issues:
        output.print_md(
            "\n**Misaligned models detected.** "
            "Coordinate with model owners to realign using Shared Coordinates.\n"
            "Tolerances: XY={} ft, Z={} ft, Rotation={}°".format(
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
```

### Step 2: Verify — read it back

Check:
- `get_links(doc)` from `bim_utils` — already returns `RevitLinkInstance` list
- `link.GetTransform()` not `link.GetLinkDocument()` — correct API
- `math.atan2(BasisX.Y, BasisX.X)` extracts rotation from transform basis vector
- `classify()` checks all three tolerances independently (can have multiple flags)
- Empty links list is handled gracefully

### Step 3: Commit

```bash
git add "BIMTools.extension/Coordination.panel/ModelAlignment.pushbutton/script.py"
git commit -m "feat: add ModelAlignment — scan linked models for alignment issues"
```

---

## Task 7: Final Verification

### Step 1: Verify folder structure

Run:
```bash
find "BIMTools.extension" -name "script.py" | sort
```

Expected to see all previous scripts PLUS:
```
BIMTools.extension/Coordinates.panel/CoordinateSetup.pushbutton/script.py
BIMTools.extension/Coordinates.panel/CoordinateValidator.pushbutton/script.py
BIMTools.extension/Coordinates.panel/GridCoordinateFinder.pushbutton/script.py
BIMTools.extension/Coordinates.panel/ExportCADUCS.pushbutton/script.py
BIMTools.extension/Coordination.panel/ModelAlignment.pushbutton/script.py
BIMTools.extension/lib/coord_utils.py
```

### Step 2: Check all imports resolve

Each script imports `from coord_utils import ...`. Verify `coord_utils.py` exports:
- `save_coords` ✓
- `load_coords` ✓
- `to_model` ✓
- `to_survey` ✓
- `check_large_coords` ✓
- `calc_rotation` ✓

### Step 3: Check no script imports anything not in `bim_utils` or `coord_utils`

Scan for unexpected imports that would fail at runtime.

### Step 4: Update MEMORY.md

Add the new Coordinates.panel and coord_utils.py to the project memory.

### Step 5: Final commit

```bash
git add docs/plans/2026-03-08-bim-coordinates-panel.md
git add docs/plans/2026-03-08-bim-coordinates-panel-design.md
git commit -m "docs: add BIM Coordinates Panel design doc and implementation plan"
```
