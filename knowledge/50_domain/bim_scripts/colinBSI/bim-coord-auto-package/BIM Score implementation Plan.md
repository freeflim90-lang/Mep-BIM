# BIM Score Implementation Plan

This document describes the 150-point pyRevit model health scoring system. The production script is in `BIMTools.extension/`.

---

## What It Does

Scores the current Revit model across 8 categories and appends one row to `BIM_Automation/data/output/model_health_scores.csv` for Power BI trend tracking.

One click → full audit → CSV row appended.

---

## Script Location

```
BIMTools.extension/
└── BIM.panel/
    └── HealthScore.pushbutton/
        └── script.py
```

Button label: **BIM → Model Health Score**

---

## Scoring Categories

| Category | Max Points | Automatable Max | Automated Checks |
|---|---|---|---|
| Model Warnings | 25 | 25 | Warning count tiers; −5 for critical warnings |
| Model Size & Performance | 20 | 20 | File size tiers; cloud models score mid-tier (10) |
| CAD & External Content | 20 | 15 | Imported CAD count; +5 if using CAD links |
| Families & Modeling Practices | 25 | 15 | In-place family count; +5 if total families <500 |
| Views & Documentation | 15 | 15 | View count; +5 if >80% have view template |
| Worksets & Links | 15 | 15 | Workset count; link presence; −5 if >25 worksets |
| Clash & Coordination Readiness | 15 | 15 | Levels defined; shared coordinates; links loaded |
| Automation & Data Standards | 15 | 15 | Worksharing; naming convention; warnings <1000 |
| **Total** | **150** | **~135** | |

Manual checks not automated: origin placement (+5), nested family optimization (+5), proper family categories (+5), compact central model (+5). Elite status (≥130) is still reachable on a well-maintained model.

---

## Score Thresholds

| Score | Status | Action |
|---|---|---|
| 130–150 | Elite | No action needed |
| 115–129 | Excellent | Monitor |
| 100–114 | Healthy | Minimum for coordination entry |
| 85–99 | Needs Cleanup | Notify team; remediate before next cycle |
| <85 | Critical | Reject from coordination |

---

## CSV Output

Appends to `BIM_Automation/data/output/model_health_scores.csv`.

| Column | Description |
|---|---|
| RunDate | Date script was run |
| ModelName | Revit document title |
| TotalScore | 0–150 |
| Status | Elite / Excellent / Healthy / Needs Cleanup / Critical |
| Warnings | Raw warning count |
| FileSizeMB | Model file size |
| CADImports | Number of imported CAD files |
| InPlaceFamilies | Count of in-place families |
| ViewCount | Non-template view count |
| WorksetCount | User workset count |
| LinkCount | Revit link count |
| WorksharingEnabled | True/False |
| Score_Warnings | Warnings category points |
| Score_FileSize | Model Size category points |
| Score_CAD | CAD & External Content category points |
| Score_Families | Families category points |
| Score_Views | Views & Documentation category points |
| Score_Worksets | Worksets & Links category points |
| Score_Coordination | Clash & Coordination Readiness category points |
| Score_Standards | Automation & Data Standards category points |

The CSV appends — never overwrites — so Power BI can track score trends over time.

---

## Deployment

1. Copy `BIMTools.extension/` to your pyRevit extensions folder
2. Open pyRevit Settings → Extensions → reload
3. Update `OUTPUT_DIR` in `script.py` to your server path
4. Click **BIM → Model Health Score** on any open model

---

## Weekly Workflow

| Day | Activity |
|---|---|
| Monday | Run health score on all uploaded models |
| Monday | Models below 100 are notified for cleanup |
| Wednesday | Pipeline runs; CSV feeds Power BI dashboard |
| Friday | Coordination meeting — models below 100 excluded |

---

## Dynamo Multi-Model Scanner

For scanning multiple models in batch, a Dynamo workflow can be used.

**Workflow:**
1. Open Dynamo
2. Select folder containing models
3. Open each model in sequence
4. Run health checks
5. Export scores

**Core Dynamo nodes:**
- `Directory.Contents`
- `File.Path`
- `Document.Open`
- `All Elements of Category`
- `Element.Count`
- `Data.ExportCSV`

The Python scoring logic from `script.py` can be ported directly into a Dynamo Python node using the same thresholds.

---

## Phase 5 Upgrade Path

The pyRevit scoring script here exports results to a flat CSV — this is the **Phase 3 model health** layer.

`BIM compliance dashboard Requirements.md` (Phase 5) replaces this with the `FactModelHealth` append-only table, which adds:
- `RunId` and `RunDateTime` for time-series tracking
- `Portfolio_ProjectID` and `Portfolio_Discipline` for cross-project comparison
- Governance scoring and growth velocity metrics
- Cloud-model safe keying (does not rely on `doc.PathName`)
