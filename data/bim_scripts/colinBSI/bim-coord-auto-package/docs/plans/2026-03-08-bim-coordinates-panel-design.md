# BIM Coordinates Panel — Design Document

**Date:** 2026-03-08
**Status:** Approved

---

## Scope

Add a new `Coordinates.panel` (4 tools) to `BIMTools.extension` and one new tool (`ModelAlignment`) to the existing `Coordination.panel`.

### Not in scope (deferred)
- Writing to Revit Survey Point / PBP / True North via API
- Auto-align linked models
- Civil3D integration, BEP generator, visualization diagram
- Linked model coordinate push (Publish Shared Coordinates)

---

## Panel Structure

### New: `Coordinates.panel`

| Tool | Type | Purpose |
|---|---|---|
| `CoordinateSetup` | Read-only report | Enter/store project coords; display setup report |
| `CoordinateValidator` | Read-only diagnostic | Compare stored coords vs actual Revit survey point/PBP/true north |
| `GridCoordinateFinder` | Interactive/read-only | Click a point → get grid + level + survey coords |
| `ExportCADUCS` | File output | Generate `.scr`, `.txt`, and report from stored coords |

### Addition to existing: `Coordination.panel`

| Tool | Type | Purpose |
|---|---|---|
| `ModelAlignment` | Read-only report | Scan linked models for offset/rotation misalignment |

---

## Shared Math Library

New file: `BIMTools.extension/lib/coord_utils.py`

### Functions

| Function | Signature | Purpose |
|---|---|---|
| `save_coords` | `(doc, e, n, z, rot, grid)` | Write to Extensible Storage (inside Transaction) |
| `load_coords` | `(doc)` | Read from Extensible Storage; returns `None` if not set |
| `to_model` | `(e, n, z, ref_e, ref_n, base_z, rot_deg)` | Survey → model coords |
| `to_survey` | `(x, y, z, ref_e, ref_n, base_z, rot_deg)` | Model → survey coords (reverse transform) |
| `check_large_coords` | `(e, n)` | Returns warning string if distance from origin > 105,600 ft |
| `calc_rotation` | `(e1, n1, e2, n2)` | Compute rotation from two known grid points via `atan2` |

### Extensible Storage Schema

- **Schema name:** `BIMCoordinates`
- **Fixed GUID:** assigned at implementation time, never changes
- **Fields:** `easting` (float), `northing` (float), `elevation` (float), `rotation_deg` (float), `ref_grid` (str)
- **Access:** Public read/write
- **Safety:** Zero effect on geometry or model health. If schema is absent, tools return `None` and prompt gracefully.

### Math

```
# Forward: survey → model
dx = easting - ref_easting
dy = northing - ref_northing
x_model = dx * cos(θ) - dy * sin(θ)
y_model = dx * sin(θ) + dy * cos(θ)
z_model = elevation - base_elevation

# Reverse: model → survey
easting  = ref_e + x*cos(θ) + y*sin(θ)
northing = ref_n - x*sin(θ) + y*cos(θ)

# Rotation from two known points
θ = atan2(ΔEasting, ΔNorthing)

# Large coord warning threshold
distance = sqrt(e² + n²) > 105,600 ft  →  warn
```

---

## Tool Specifications

### 1. CoordinateSetup

**Location:** `Coordinates.panel/CoordinateSetup.pushbutton/script.py`

**Workflow:**
1. Dialog: Easting, Northing, Elevation, Rotation (degrees), Reference Grid name
2. Optional: second grid point (Easting2, Northing2) → auto-calculates rotation via `calc_rotation`, overrides manual rotation entry
3. Run `check_large_coords` → display warning if survey coords exceed Revit safe range
4. Save all 5 values to Extensible Storage via `save_coords`
5. Print "Coordinate Setup Report":
   - Survey coords as entered
   - What Revit Survey Point should be set to
   - What AutoCAD/Plant3D UCS origin should be set to
   - True North rotation value
6. **No model geometry changes**

---

### 2. CoordinateValidator

**Location:** `Coordinates.panel/CoordinateValidator.pushbutton/script.py`

**Workflow:**
1. Load stored coords via `load_coords` — if missing, print error and exit
2. Read actual Revit Survey Point position (via `BasePoint` element with `IsShared = True`)
3. Read actual True North angle (via `ProjectInfo.AngleFromProjectNorth` or equivalent)
4. Compare stored vs actual for each value
5. Flag any delta beyond tolerance:
   - Translation: 0.05 ft
   - Rotation: 0.05°
6. Print table: one row per check, status = `OK` / `MISMATCH`

---

### 3. GridCoordinateFinder

**Location:** `Coordinates.panel/GridCoordinateFinder.pushbutton/script.py`

**Workflow:**
1. Load stored coords via `load_coords` — if missing, prompt user to run CoordinateSetup first
2. `uidoc.Selection.PickPoint("Click a point in the model")`
3. Collect all `Grid` elements live from model; collect all `Level` elements
4. Find nearest V-grid (smallest `|x - grid_x|`) and nearest H-grid (smallest `|y - grid_y|`)
5. Find nearest level by smallest `|z - level_elevation|`
6. Reverse-transform model XYZ → Easting/Northing/Elevation via `to_survey`
7. Print result:
   ```
   Grid Location:  C / 5
   Level:          Level 3
   Easting:        748350.120
   Northing:       2134677.900
   Elevation:      128.000 ft
   Model X/Y/Z:    130.12 / 245.44 / 28.00
   ```
8. Copy formatted one-liner to clipboard: `Grid C5 | Level 3 | E 748350.12 N 2134677.90 EL 128'-0"`

---

### 4. ExportCADUCS

**Location:** `Coordinates.panel/ExportCADUCS.pushbutton/script.py`

**Workflow:**
1. Load stored coords via `load_coords` — if missing, prompt user to run CoordinateSetup first
2. Write 3 files to `OUTPUT_DIR` (`C:\BIM_Automation\data\output\`):
   - `autocad_setup.scr` — runnable script for AutoCAD, Plant3D, CADWorx
   - `revit_coord_setup.txt` — human-readable Revit manual setup instructions
   - `coordinate_report.txt` — full project coordinate summary
3. Print output paths to output window

**autocad_setup.scr contents:**
```
UCS
W
UCS
Origin
{easting},{northing},{elevation}
UCS
Z
{rotation_deg}
PLAN
C
```

---

### 5. ModelAlignment

**Location:** `Coordination.panel/ModelAlignment.pushbutton/script.py`

**Workflow:**
1. Collect all `RevitLinkInstance` elements via `get_links(doc)` from `bim_utils`
2. For each link:
   - Extract `transform.Origin` (X, Y, Z)
   - Extract rotation: `math.degrees(math.atan2(transform.BasisX.Y, transform.BasisX.X))`
3. Compare against `Transform.Identity` (host = reference at 0,0,0 / 0°)
4. Apply tolerances:
   - Translation: 0.05 ft → flag `OFFSET`
   - Rotation: 0.05° → flag `ROTATION`
   - Both → `MISALIGNED`
   - Neither → `OK`
5. Print alignment report per link
6. **No auto-align in v1** — report only

**Tolerances:**
| Check | Tolerance | Flag |
|---|---|---|
| Translation (XY) | 0.05 ft | OFFSET |
| Elevation (Z) | 0.02 ft | ELEVATION |
| Rotation | 0.05° | ROTATION |

---

## File Structure After Build

```
BIMTools.extension/
├── lib/
│   ├── bim_utils.py                          (existing)
│   └── coord_utils.py                        (new)
├── Coordinates.panel/
│   ├── CoordinateSetup.pushbutton/
│   │   └── script.py
│   ├── CoordinateValidator.pushbutton/
│   │   └── script.py
│   ├── GridCoordinateFinder.pushbutton/
│   │   └── script.py
│   └── ExportCADUCS.pushbutton/
│       └── script.py
├── Coordination.panel/
│   ├── ... (existing 6 tools)
│   └── ModelAlignment.pushbutton/            (new)
│       └── script.py
└── ... (other panels unchanged)
```

---

## Error Handling Pattern

All scripts follow the existing extension pattern:
- Wrap `run()` in `try/except`
- Print traceback to output window on failure
- If `load_coords` returns `None`: print actionable message (`"Run CoordinateSetup first"`) and exit cleanly
- No modal error dialogs except for confirmation prompts

---

## Revit API Notes

- `BasePoint` with `IsShared = True` → Survey Point; `IsShared = False` → Project Base Point
- True North angle: `doc.ActiveProjectLocation.GetProjectPosition(XYZ.Zero).Angle`
- Grid proximity: use `grid.Curve.GetEndPoint(0)` midpoint for position detection (same as ExportGrids)
- UnitUtils: use existing `to_feet()` pattern from ExportGrids (handles Revit 2022 API change)
- Extensible Storage: requires `clr.AddReference("RevitAPI")` — already standard in all scripts
