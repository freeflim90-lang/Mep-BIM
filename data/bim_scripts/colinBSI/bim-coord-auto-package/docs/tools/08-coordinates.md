# Coordinates Panel

The Coordinates panel manages project coordinate setup across all BIM platforms. Use these tools at project start to establish a shared coordinate system, and throughout the project for clash location reporting, field coordination, and CAD handoffs.

Coordinate values are stored directly inside the Revit model using Extensible Storage — they travel with the `.rvt` file and are shared automatically when the model is distributed to other teams.

---

## Tools

### Coordinate Setup

**Purpose:** Enter the project's survey coordinates and store them in the Revit model. Generates a setup report showing the correct values for Revit, AutoCAD, Plant3D, and CADWorx.

**When to use:**
- Once at project start, after receiving survey control points from the civil engineer
- Any time the coordinate system is updated or corrected

**How to use:**
1. Click **Coordinate Setup**
2. Enter the five project values in the dialog (comma-separated):
   - Easting, Northing, Elevation, Rotation (degrees), Reference Grid
   - Example: `748221.40, 2134556.20, 100.00, 12.5, A1`
3. Optional: click **Yes** to calculate rotation automatically from two known grid points (more accurate than manual entry)
   - Enter a second grid point (Easting2, Northing2) and rotation is computed via `atan2`
4. Review the output report

**Output:**
- Values saved to Extensible Storage in the `.rvt` file
- Setup report showing:
  - Survey coordinates as entered
  - What to set Revit Survey Point to (manually)
  - AutoCAD / Plant3D / CADWorx UCS origin and rotation

> If your survey coordinates are very large (e.g. State Plane values like E 748221, N 2134556), the tool will automatically warn you and recommend a Revit origin shift to keep geometry stable. Revit becomes unreliable beyond ~105,600 ft from the internal origin.

> Run **Coordinate Validator** after manually updating the Revit Survey Point to confirm everything matches.

---

### Coordinate Validator

**Purpose:** Compares the stored coordinate values against the actual Revit model setup — Survey Point position and True North rotation — and flags any mismatches.

**When to use:**
- After manually updating the Revit Survey Point or True North angle
- When onboarding a model received from another team
- As a QC check before distributing the model

**How to use:**
1. Click **Coordinate Validator**
2. Review the validation table in the output window

**Output:**

| Check | Tolerance | Status |
|---|---|---|
| Survey Point Easting | 0.05 ft | OK / MISMATCH |
| Survey Point Northing | 0.05 ft | OK / MISMATCH |
| Survey Point Elevation | 0.02 ft | OK / MISMATCH |
| True North Rotation | 0.05° | OK / MISMATCH |

> If mismatches are found, update the Revit Survey Point and True North manually to match the stored values, or re-run **Coordinate Setup** with corrected inputs.

---

### Grid Coordinate Finder

**Purpose:** Click any point in the model to instantly see its nearest grid intersection, level, survey coordinates (Easting/Northing/Elevation), and model XYZ coordinates. Result is copied to clipboard for pasting into RFIs, clash reports, and issue trackers.

**When to use:**
- During clash review to report clash locations in survey coordinates
- For RFI responses that require field-verifiable coordinates
- During construction coordination meetings

**Requires:** Coordinate Setup must have been run first.

**How to use:**
1. Open a 3D or plan view
2. Click **Grid Coordinate Finder**
3. Click any point in the model
4. Coordinates appear in the output window and are copied to clipboard

**Output example:**

| Field | Value |
|---|---|
| Grid (V / H) | C / 5 |
| Level | Level 3 |
| Easting | 748350.123 |
| Northing | 2134677.900 |
| Elevation | 128.000 ft |
| Model X | 130.123 ft |
| Model Y | 245.440 ft |
| Model Z | 28.000 ft |

**Clipboard one-liner:** `Grid C5 | Level 3 | E 748350.123 N 2134677.900 EL 128.000 ft`

> Best used in a 3D coordination view. In plan views, click on elements rather than empty space for more accurate Z positioning.

---

### Export CAD UCS

**Purpose:** Generates a ready-to-run AutoCAD script and a full coordinate reference package from the stored project coordinates.

**When to use:**
- When handing off coordinate data to AutoCAD, Plant3D, or CADWorx teams
- At project start when spinning up CAD disciplines
- Any time the coordinate system changes and CAD teams need updated setup files

**Requires:** Coordinate Setup must have been run first.

**How to use:**
1. Click **Export CAD UCS**
2. Three files are written to `C:\BIM_Automation\data\output\`

**Output files:**

| File | Contents |
|---|---|
| `autocad_setup.scr` | Runnable AutoCAD script — sets UCS origin and rotation |
| `revit_coord_setup.txt` | Step-by-step Revit manual setup instructions |
| `coordinate_report.txt` | Full project coordinate summary (survey, Revit, CAD) |

**To run the AutoCAD script:**
1. Open AutoCAD, Plant3D, or CADWorx
2. Type `SCRIPT` and press Enter
3. Browse to and select `autocad_setup.scr`
4. The UCS origin and rotation are set automatically

> The script resets to World UCS first (`UCS W`) before applying the new origin, so it is safe to run multiple times.

---

## Workflow

**Project start (do once):**
1. Receive survey control points from civil engineer
2. Run **Coordinate Setup** — enter the 5 values, save to model
3. Manually set Revit Survey Point and True North to match the report
4. Run **Coordinate Validator** — confirm all checks pass
5. Run **Export CAD UCS** — distribute setup files to CAD teams

**Ongoing:**
- Use **Grid Coordinate Finder** during clash review and coordination meetings
- Re-run **Coordinate Validator** when receiving updated models from other disciplines
- Re-run **Export CAD UCS** if the coordinate system changes

---

## Tips

- The coordinate values are stored in the `.rvt` file itself — they are preserved when the model is synced, copied, or sent to other teams
- If a tool reports "No coordinate data found", run **Coordinate Setup** first — this is always the first step
- For State Plane coordinates (large E/N values), always use the recommended origin shift when warned — ignoring it can cause geometry instability and precision errors in Revit
- The two-point rotation calculation in **Coordinate Setup** eliminates the most common source of coordinate errors: manually entering an incorrect project north rotation
