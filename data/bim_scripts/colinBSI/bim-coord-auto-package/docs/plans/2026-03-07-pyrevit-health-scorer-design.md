# pyRevit 150-Point Model Health Scorer — Design Document
**Date:** 2026-03-07
**Status:** Approved

---

## Overview

Create a production-ready pyRevit button that scores the current Revit model on a 150-point scale, then appends one row to a shared CSV for Power BI trend tracking.

---

## File Structure

```
BIMTools.extension/
└── BIM.panel/
    └── HealthScore.pushbutton/
        └── script.py
```

---

## Architecture

`script.py` structure (top to bottom):
1. **Config block** — output folder path (`BIM_Automation/data/output/`), constants
2. **Data collection** — all Revit API calls up front, stored in a `model_data` dict
3. **8 scoring functions** — one per rubric category, each returns `(points, max_points, detail_str)`
4. **Score assembly** — sums categories, clamps each to 0 floor, applies status threshold
5. **CSV export** — appends one row to `model_health_scores.csv`

Silent operation — no dialog shown after run.

---

## Scoring Coverage

| Category | Max | Automated Checks |
|---|---|---|
| Model Warnings | 25 | Warning count tiers; −5 penalty if critical warnings present |
| Model Size & Performance | 20 | File size tiers |
| CAD & External Content | 20 | Imported CAD count tiers; +5 if zero imports and ≥1 CAD link |
| Families & Modeling Practices | 25 | In-place family count tiers; +5 if total family count <500 (unused purged proxy) |
| Views & Documentation | 15 | View count tiers; +5 if >80% of views have view template applied |
| Worksets & Links | 15 | Workset count; link presence; −5 penalty if >25 worksets |
| Clash & Coordination Readiness | 15 | Levels defined; shared coordinates set; links loaded |
| Automation & Data Standards | 15 | Worksharing enabled; model name has `_`; warnings <1000 |

Manual checks (origin placement, compact central, nested family optimization) are skipped — those bonus points are simply not awarded.

Penalties floor at 0 per category. Total score floors at 0.

---

## Status Thresholds

| Score | Status |
|---|---|
| 130–150 | Elite |
| 115–129 | Excellent |
| 100–114 | Healthy |
| 85–99 | Needs Cleanup |
| <85 | Critical |

Minimum for coordination entry: 100

---

## CSV Output

Appends one row per run to `BIM_Automation/data/output/model_health_scores.csv`.

| Column | Example |
|---|---|
| `RunDate` | 2026-03-07 |
| `ModelName` | MECH_TowerA |
| `TotalScore` | 112 |
| `Status` | Healthy |
| `Warnings` | 247 |
| `FileSizeMB` | 284.3 |
| `CADImports` | 0 |
| `InPlaceFamilies` | 2 |
| `ViewCount` | 198 |
| `WorksetCount` | 8 |
| `LinkCount` | 4 |
| `WorksharingEnabled` | True |
| `Score_Warnings` | 20 |
| `Score_FileSize` | 20 |
| `Score_CAD` | 15 |
| `Score_Families` | 18 |
| `Score_Views` | 15 |
| `Score_Worksets` | 12 |
| `Score_Coordination` | 10 |
| `Score_Standards` | 12 |

---

## Out of Scope

- UI dialog / results window (Phase 2)
- Dynamo multi-model scanner (separate tool)
- Power BI dashboard (covered in `BIM Command Center.md`)
- Manual checks: origin placement, compact central, nested family optimization
