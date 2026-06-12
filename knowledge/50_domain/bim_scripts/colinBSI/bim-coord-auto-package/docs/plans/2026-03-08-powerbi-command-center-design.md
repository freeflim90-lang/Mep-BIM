# Power BI Command Center — Design Document
**Date:** 2026-03-08
**Status:** Approved

---

## Overview

Build the BIM Command Center Power BI dashboard system. Three new components extend the existing pipeline: an ExportGrids pyRevit button, a Navisworks XML clash parser, and a four-dashboard Power BI setup guide.

---

## Architecture

```
ExportGrids button (new — Utilities.panel)
    → C:\BIM_Automation\data\output\grid_lines.csv
    → C:\BIM_Automation\data\output\level_elevations.csv

Navisworks XML export (manual, Tuesday workflow)
    + grid_lines.csv
    + level_elevations.csv
    → BIM_Automation/clash_processing/clash_parser.py  ← new pipeline Stage 0
    → clash_heatmap_data.csv

Existing CSVs (already produced by pipeline):
    model_health_scores.csv
    coordination_report.csv
    clash_summary_report.csv

Power BI Desktop (folder connection → output\)
    → Dashboard 1: Project Health
    → Dashboard 2: Clash Heat Map
    → Dashboard 3: Coordination Performance
    → Dashboard 4: Model Health Trends
```

---

## Component 1 — ExportGrids Pushbutton

**Location:** `BIMTools.extension/Utilities.panel/ExportGrids.pushbutton/script.py`

**Outputs:**
- `grid_lines.csv` — columns: `GridName`, `Orientation` (H/V), `Position` (feet)
- `level_elevations.csv` — columns: `LevelName`, `Elevation` (feet)

**Grid orientation detection:** A grid is vertical if ΔY > ΔX along its curve; its `Position` is the midpoint X coordinate. A grid is horizontal if ΔX > ΔY; its `Position` is the midpoint Y coordinate.

**Behaviour:** Read-only. No confirmation. Run once when grid layout is established; re-run if grids change.

---

## Component 2 — clash_parser.py

**Location:** `BIM_Automation/clash_processing/clash_parser.py`

**Input:**
- `data/input/clash_report.xml` — Navisworks XML export
- `data/output/grid_lines.csv`
- `data/output/level_elevations.csv`

**Output:** `data/output/clash_heatmap_data.csv`

**Columns:** `ClashID`, `Status`, `DisciplineA`, `DisciplineB`, `Level`, `GridZone`, `X`, `Y`, `Z`

**Algorithm:**
1. Parse XML — extract `ClashID`, `Status`, `X`, `Y`, `Z`, `DisciplineA`, `DisciplineB` per `<clashresult>`
2. Map Z → Level: find the highest level whose elevation ≤ Z. Below all levels → `"Below Grade"`
3. Map XY → GridZone:
   - Separate grid_lines into vertical grids (sorted by Position ascending) and horizontal grids (sorted by Position ascending)
   - For each clash, binary search to find the two bracketing vertical grids and two bracketing horizontal grids
   - Zone label: `"A-B/1-2"` format
   - Outside all grid extents → `"Outside Grid"`

**Edge cases:**
- `clash_report.xml` absent → stage skipped with log message (not an error)
- `grid_lines.csv` or `level_elevations.csv` absent → log warning, output raw X/Y/Z only, continue
- Clash outside grid extents → `GridZone = "Outside Grid"`
- Clash below all levels → `Level = "Below Grade"`

**Pipeline integration:** Added as Stage 0 in `main.py`. If XML absent, logs and continues to Stage 1.

---

## Component 3 — Power BI Dashboard Guide

**Location:** `docs/powerbi/command-center-setup.md`

**Format:** Step-by-step build guide (`.pbix` is binary — guide covers exact visual types, field assignments, DAX measures, color scales).

### Data Model

4 flat tables — no relationships needed:

| Table | Source CSV |
|---|---|
| ModelHealth | `model_health_scores.csv` |
| ClashHeatmap | `clash_heatmap_data.csv` |
| ClashSummary | `clash_summary_report.csv` |
| CoordReport | `coordination_report.csv` |

Connection: Power BI folder connector → `C:\BIM_Automation\data\output\`

### Dashboard 1 — Project Health

| Visual | Type | Fields |
|---|---|---|
| Total Models | Card | DISTINCTCOUNT(ModelHealth[ModelName]) |
| Avg Health Score | Card | AVERAGE(ModelHealth[TotalScore]) |
| Total Active Clashes | Card | COUNTROWS(ClashHeatmap where Status≠Resolved) |
| Model health table | Table | ModelName, TotalScore, Status (conditional color) |
| Score by model | Bar chart | ModelName vs TotalScore, reference line at 100 |

Status color rules: Elite=green (#107C41), Excellent=#0070C0, Healthy=#00B050, Needs Cleanup=#FFC000, Critical=#FF0000

### Dashboard 2 — Clash Heat Map

| Visual | Type | Fields |
|---|---|---|
| Heat map matrix | Matrix | Rows=Level, Columns=GridZone, Values=COUNTROWS |
| Discipline filter | Slicer | DisciplineA, DisciplineB |
| Status filter | Slicer | Status |
| Clash by discipline pair | Bar chart | DisciplineA & " vs " & DisciplineB vs count |

Matrix conditional formatting: 0=white, 1–10=green (#E2EFDA), 11–25=amber (#FFE699), 26+=red (#FF0000). Level rows sorted by elevation descending (top floor at top).

### Dashboard 3 — Coordination Performance

| Visual | Type | Fields |
|---|---|---|
| Clashes by discipline | Bar chart | DisciplineA vs COUNTROWS(ClashHeatmap) |
| Clash status breakdown | Stacked bar | Status vs count (from ClashSummary) |
| Clash trend over time | Line chart | RunDate vs total clash count |

### Dashboard 4 — Model Health Trends

| Visual | Type | Fields |
|---|---|---|
| Score over time | Line chart | RunDate vs TotalScore, one line per ModelName |
| Reference bands | Constant lines | 130 (Elite), 100 (Healthy min), 85 (Critical) |
| Model filter | Slicer | ModelName |

### DAX Measures

```dax
Active Clashes = COUNTROWS(FILTER(ClashHeatmap, ClashHeatmap[Status] <> "Resolved"))

Avg Health Score = AVERAGE(ModelHealth[TotalScore])

Models Below 100 = COUNTROWS(FILTER(ModelHealth, ModelHealth[TotalScore] < 100))

Clash Resolution Rate =
DIVIDE(
    COUNTROWS(FILTER(ClashSummary, ClashSummary[Status] = "Resolved")),
    SUM(ClashSummary[Count]),
    0
)
```

---

## Out of Scope

- Live ACC API data pull (Phase 4 stub — issue_stub.py)
- Phase 5 portfolio-level cross-project comparison
- Automated Power BI dataset refresh via gateway (document manually — requires Power BI Pro license)
- `.pbix` file distribution (binary format, not suitable for this package)
