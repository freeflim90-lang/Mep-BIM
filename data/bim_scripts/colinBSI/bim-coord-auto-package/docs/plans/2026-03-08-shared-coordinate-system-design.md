# Shared Coordinate System — Design Doc

**Date:** 2026-03-08
**Status:** Approved

---

## Problem

AutoCAD, Plant 3D, CADWorx Plant, and Civil 3D models frequently arrive misaligned with the Revit federated model — causing false clashes, missed real clashes, and incorrect clash locations in Navisworks. No automated enforcement or validation exists.

---

## Approach

Hybrid: pyRevit handles Revit-side coordinate setup (requires live Revit API); the pipeline handles DWG validation (headless, runs Wednesday automatically).

> ACC workflow: each Revit discipline model acquires shared coordinates independently from the Civil 3D DWG. No "Publish Coordinates" step — that is a desktop/server workflow incompatible with ACC.

---

## Authoritative Source

**Civil 3D DWG** — provided by the civil engineer, uploaded to ACC. Downloaded locally for reference during setup. All coordinate alignment derives from this file.

---

## Components

### 1 — pyRevit CoordSync Panel (2 buttons)

**SetupCoordinates**
- Links Civil 3D DWG into active Revit model with Shared Coordinates positioning
- Acquires coordinates from it (Survey Point + Project Base Point)
- Pins Survey Point and Project Base Point
- Exports `coord_seed.csv` to `data/output/`:
  - Survey point N/E/Z
  - Project base point N/E/Z
  - True north rotation angle
  - Grid origins and bearings (from ExportGrids data)
  - Level elevations
- Exports `_CoordRef.dwg` to `data/output/`:
  - Grids as reference lines
  - Levels as reference lines
  - Coordinate data block (N/E/Z + rotation)
  - Non-Revit teams XREF this file to align their authoring environment

> Each Revit discipline model (Arch, Structure, MEP) on ACC runs SetupCoordinates independently against the same Civil DWG.

**ValidateAlignment**
- Triggers `coord_sync/` pipeline stage against `data/input/dwg_submissions/`
- Displays pass/fail summary in pyRevit dialog
- Full report written to `data/output/`

---

### 2 — Pipeline coord_sync/ Module

Runs as Stage 0 of `main.py` (Wednesday 6AM, non-blocking).

**coord_extractor.py**
- Reads `coord_seed.csv` as the validation reference

**dwg_validator.py**
- Uses `ezdxf` to parse each DWG in `data/input/dwg_submissions/`
- Checks per file:
  - UCS origin vs. seed N/E/Z
  - Grid line intersections vs. exported grid data
  - Model units (must be feet)
  - True north rotation angle vs. seed

**fix_instructions.py**
- Platform-specific correction templates (AutoCAD, Civil 3D, Plant 3D, CADWorx)
- Injected into report for each failed check

**report output:**
- `coord_validation_report.csv` — one row per file, pass/fail per check, delta values
- `coord_validation_report.pdf` — human-readable with per-platform fix instructions

---

## Tolerances

| Check | Tolerance | Severity |
|---|---|---|
| UCS origin (N/E/Z) off > 1 ft | — | Hard fail — model rejected |
| UCS origin (N/E/Z) off 0.01–1 ft | ±0.01 ft | Warning |
| Grid intersection | ±1/8" (0.0104 ft) | Warning |
| True north rotation | ±0.1° | Warning |
| Model units (not feet) | Exact | Hard fail |

---

## Platform-Specific Fix Instructions

**AutoCAD / Plant 3D / CADWorx:**
1. Drawing Settings → Units → set to Feet
2. Identify known grid intersection in model
3. `MOVE` all geometry: base = grid intersection, destination = seed N/E/Z
4. `ROTATE` all geometry: base = origin, angle = seed true north delta
5. Save and re-export NWC

**Civil 3D:**
1. Drawing Settings → Units and Zone → set coordinate system to project CRS (in coord_seed.csv header)
2. Verify alignment object origin matches seed N/E values
3. Re-export NWC with "Export Civil Objects" enabled

**CADWorx Plant:**
1. Project Setup → Coordinate System → enter N/E/Z from coord_seed.csv
2. Verify pipe spec origin point matches grid intersection
3. Re-export NWC or IFC

---

## Data Flow

```
Civil 3D DWG (from ACC)
        │
        ▼
[pyRevit: SetupCoordinates]
        │
        ├── Revit acquires shared coordinates (Survey Point pinned)
        │
        ├── coord_seed.csv ──────────────────────────────────────┐
        │   (N/E/Z, true north, grids, levels)                   │
        │                                                         │
        └── _CoordRef.dwg ──► Non-Revit teams XREF this          │
            (grids + levels + coord data block)                   │
                                                                  │
Discipline teams submit DWGs                                      │
(AutoCAD / Plant 3D / Civil 3D / CADWorx)                        │
        │                                                         │
        ▼                                                         │
data/input/dwg_submissions/                                       │
        │                                                         ▼
        └──► [Pipeline: coord_sync/ — Wednesday 6AM] ◄───────────┘
                    │
                    ├── coord_validation_report.csv
                    └── coord_validation_report.pdf
```

---

## File Structure Changes

```
BIM_Automation/
├── coord_sync/                         NEW
│   ├── coord_extractor.py
│   ├── dwg_validator.py
│   └── fix_instructions.py
├── data/
│   ├── input/
│   │   └── dwg_submissions/            NEW — discipline teams drop DWGs here
│   └── output/
│       ├── coord_seed.csv              written by pyRevit SetupCoordinates
│       ├── _CoordRef.dwg               written by pyRevit SetupCoordinates
│       ├── coord_validation_report.csv NEW
│       └── coord_validation_report.pdf NEW

BIMTools.extension/
└── CoordSync.panel/                    NEW
    ├── SetupCoordinates.pushbutton/
    │   └── script.py
    └── ValidateAlignment.pushbutton/
        └── script.py
```

---

## Integration Points

**main.py stage order (updated):**
- Stage 0 — coord_sync (NEW, non-blocking)
- Stage 1 — clash_parser (existing)
- Stage 2 — clash_grouper (existing)
- Stage 3 — clash_prioritizer (existing)
- Stage 4 — report_generator (existing + new Coord Validation tab)

**report_generator.py:** adds 4th Excel tab `Coord Validation` (pass/fail per DWG)

**bim_utils.py additions:**
- `COORD_SUBMISSIONS_DIR`
- `COORD_SEED_PATH`
- `COORD_REF_DWG_PATH`

**Dependencies:**
- `ezdxf` — added to pipeline requirements (pure Python)
- No new Revit API references beyond existing InitializeProject usage

---

## Out of Scope

- Automatic geometry correction of submitted DWGs (report + instructions only)
- ACC API integration for coordinate data (future Phase 2 work)
- Dynamo-based coordinate workflows
