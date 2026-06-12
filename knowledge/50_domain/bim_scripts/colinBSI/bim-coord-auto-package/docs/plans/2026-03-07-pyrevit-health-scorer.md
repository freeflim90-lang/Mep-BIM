# pyRevit Model Health Scorer — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a deployable pyRevit button that scores the current Revit model on a 150-point scale and appends one row to `model_health_scores.csv` for Power BI trend tracking.

**Architecture:** Single `script.py` in the pyRevit pushbutton folder. All Revit API calls are collected up front into a `model_data` dict. Each of the 8 rubric categories has its own scoring function returning `(points, max_points)`. Score assembly and CSV append run at the end. Silent operation — no dialog.

**Tech Stack:** pyRevit, Revit API (`DB`, `FilteredElementCollector`), Python standard library (`csv`, `os`, `datetime`)

---

## Context

- Project root: `/Users/colin/BIM Coord Auto Package`
- Documentation-only package — no git, no tests
- Verification = read files back after writing
- Output CSV feeds into `BIM_Automation/data/output/model_health_scores.csv` (same folder as pipeline reports)
- Canonical scoring thresholds from CLAUDE.md: Elite ≥130, Excellent ≥115, Healthy ≥100, Needs Cleanup ≥85, Critical <85
- Minimum score for coordination entry: 100

---

### Task 1: Create pyRevit extension folder structure

**Files:**
- Create: `BIMTools.extension/BIM.panel/HealthScore.pushbutton/README.md`

**Step 1: Write the README**

Create `/Users/colin/BIM Coord Auto Package/BIMTools.extension/BIM.panel/HealthScore.pushbutton/README.md` with this content:

```
pyRevit Model Health Scorer — 150-point scale

Button: BIM → Model Health Score
Script: script.py

Scores the current Revit model across 8 categories.
Appends one row to BIM_Automation/data/output/model_health_scores.csv.

Deploy by placing BIMTools.extension/ in your pyRevit extensions folder.
Set OUTPUT_DIR in script.py to match your server path.
```

**Step 2: Verify**

Read the README back to confirm it was written correctly.

---

### Task 2: Write `script.py`

**Files:**
- Create: `BIMTools.extension/BIM.panel/HealthScore.pushbutton/script.py`

**Step 1: Write the file**

```python
"""
script.py — pyRevit Model Health Scorer (150-point scale)

Button: BIM > Model Health Score
Runs from pyRevit inside Revit. Scores the current model across 8 categories.
Appends one row to model_health_scores.csv for Power BI trend tracking.

Silent operation — output visible in pyRevit console if open.

Deploy:
    1. Place BIMTools.extension/ in your pyRevit extensions folder.
    2. Update OUTPUT_DIR below to match your server path.
    3. Click BIM > Model Health Score to run.
"""

import os
import csv
from datetime import date

from pyrevit import revit, DB

# ---------------------------------------------------------------------------
# Config — update OUTPUT_DIR to match your deployment path
# ---------------------------------------------------------------------------

OUTPUT_DIR = r"C:\BIM_Automation\data\output"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "model_health_scores.csv")

CSV_HEADERS = [
    "RunDate", "ModelName", "TotalScore", "Status",
    "Warnings", "FileSizeMB", "CADImports", "InPlaceFamilies",
    "ViewCount", "WorksetCount", "LinkCount", "WorksharingEnabled",
    "Score_Warnings", "Score_FileSize", "Score_CAD", "Score_Families",
    "Score_Views", "Score_Worksets", "Score_Coordination", "Score_Standards",
]

# ---------------------------------------------------------------------------
# Data collection — all Revit API calls in one place
# ---------------------------------------------------------------------------

def collect_model_data(doc):
    """
    Collect all model metrics using the Revit API.
    Returns a dict of raw values used by all scoring functions.
    """
    data = {}
    data["model_name"] = doc.Title

    # --- Warnings ---
    all_warnings = doc.GetWarnings()
    data["warnings"] = len(all_warnings)

    critical_keywords = ["duplicate", "overlap", "room separation", "identical instances"]
    data["critical_warnings"] = sum(
        1 for w in all_warnings
        if any(kw in w.GetDescriptionText().lower() for kw in critical_keywords)
    )

    # --- File size ---
    file_path = doc.PathName
    if file_path and os.path.exists(file_path):
        data["file_size_mb"] = os.path.getsize(file_path) / (1024.0 * 1024.0)
    else:
        data["file_size_mb"] = 0.0  # Cloud model or unsaved — scored as unknown

    # --- CAD imports vs links ---
    import_instances = DB.FilteredElementCollector(doc)\
        .OfClass(DB.ImportInstance)\
        .WhereElementIsNotElementType()\
        .ToElements()
    data["cad_imports"] = sum(1 for i in import_instances if not i.IsLinked)
    data["cad_links"]   = sum(1 for i in import_instances if i.IsLinked)

    # --- Revit links ---
    revit_links = DB.FilteredElementCollector(doc)\
        .OfClass(DB.RevitLinkInstance)\
        .ToElements()
    data["link_count"] = len(revit_links)

    # --- In-place families ---
    inplace = 0
    for fi in DB.FilteredElementCollector(doc)\
            .OfClass(DB.FamilyInstance)\
            .WhereElementIsNotElementType()\
            .ToElements():
        try:
            if fi.Symbol.Family.IsInPlace:
                inplace += 1
        except Exception:
            pass
    data["inplace_families"] = inplace

    # --- Total loaded families (proxy for "unused families purged") ---
    data["total_families"] = len(
        DB.FilteredElementCollector(doc).OfClass(DB.Family).ToElements()
    )

    # --- Views (excluding templates) ---
    all_views = DB.FilteredElementCollector(doc)\
        .OfClass(DB.View)\
        .WhereElementIsNotElementType()\
        .ToElements()
    non_template = [v for v in all_views if not v.IsTemplate]
    data["view_count"] = len(non_template)
    data["views_with_template"] = sum(
        1 for v in non_template
        if v.ViewTemplateId != DB.ElementId.InvalidElementId
    )

    # --- Worksets ---
    if doc.IsWorkshared:
        worksets = DB.FilteredWorksetCollector(doc)\
            .OfKind(DB.WorksetKind.UserWorkset)\
            .ToWorksets()
        data["workset_count"]       = len(list(worksets))
        data["worksharing_enabled"] = True
    else:
        data["workset_count"]       = 0
        data["worksharing_enabled"] = False

    # --- Levels ---
    data["level_count"] = len(
        DB.FilteredElementCollector(doc).OfClass(DB.Level).ToElements()
    )

    # --- Shared coordinates (survey point displaced from origin) ---
    shared_coords = False
    for sp in DB.FilteredElementCollector(doc)\
            .OfCategory(DB.BuiltInCategory.OST_SharedBasePoint)\
            .ToElements():
        try:
            pos = sp.Position
            if abs(pos.X) > 0.01 or abs(pos.Y) > 0.01:
                shared_coords = True
                break
        except Exception:
            pass
    data["shared_coordinates"] = shared_coords

    return data


# ---------------------------------------------------------------------------
# Scoring functions — each returns (points_earned, max_points)
# Penalties floor at 0 per category.
# ---------------------------------------------------------------------------

def score_warnings(data):
    """Category 1: Model Warnings — 25 pts max"""
    w = data["warnings"]
    if w < 100:      pts = 25
    elif w < 500:    pts = 20
    elif w < 1000:   pts = 15
    elif w < 2000:   pts = 10
    elif w < 5000:   pts = 5
    else:            pts = 0

    if data["critical_warnings"] > 0:
        pts -= 5  # penalty for critical warnings

    return max(pts, 0), 25


def score_file_size(data):
    """Category 2: Model Size & Performance — 20 pts max"""
    mb = data["file_size_mb"]
    if mb == 0.0:    return 10, 20  # cloud/unsaved — mid-tier
    if mb < 300:     pts = 20
    elif mb < 500:   pts = 15
    elif mb < 800:   pts = 10
    elif mb < 1024:  pts = 5
    else:            pts = 0
    return max(pts, 0), 20


def score_cad(data):
    """Category 3: CAD & External Content — 20 pts max"""
    imports = data["cad_imports"]
    if imports == 0:     pts = 10
    elif imports <= 3:   pts = 7
    elif imports <= 10:  pts = 3
    else:                pts = 0

    # Bonus: using CAD links instead of imports
    if imports == 0 and data["cad_links"] > 0:
        pts += 5

    # Note: correct origin placement (+5) not automatable — skipped
    return max(pts, 0), 20


def score_families(data):
    """Category 4: Families & Modeling Practices — 25 pts max"""
    inplace = data["inplace_families"]
    if inplace == 0:    pts = 10
    elif inplace <= 3:  pts = 5
    else:               pts = 0

    # Proxy for "unused families purged": total family count < 500
    if data["total_families"] < 500:
        pts += 5

    # Note: nested family optimization, proper categories (+5 each) not automatable — skipped
    return max(pts, 0), 25


def score_views(data):
    """Category 5: Views & Documentation — 15 pts max"""
    vc = data["view_count"]
    if vc < 300:    pts = 10
    elif vc < 600:  pts = 7
    elif vc < 900:  pts = 4
    else:           pts = 0

    # Bonus: >80% of views have a view template applied
    if data["view_count"] > 0:
        ratio = data["views_with_template"] / data["view_count"]
        if ratio > 0.8:
            pts += 5

    return max(pts, 0), 15


def score_worksets(data):
    """Category 6: Worksets & Links — 15 pts max"""
    wc = data["workset_count"]
    pts = 0
    if wc > 0:               pts += 5  # logical worksets present
    if data["link_count"] > 0: pts += 5  # linked models attached
    if 0 < wc <= 20:         pts += 5  # workset count reasonable

    if wc > 25:
        pts -= 5  # penalty for excessive worksets

    return max(pts, 0), 15


def score_coordination(data):
    """Category 7: Clash & Coordination Readiness — 15 pts max"""
    pts = 0
    if data["level_count"] > 0:      pts += 5  # levels defined
    if data["shared_coordinates"]:   pts += 5  # shared coordinates established
    if data["link_count"] > 0:       pts += 5  # links loaded
    return max(pts, 0), 15


def score_standards(data):
    """Category 8: Automation & Data Standards — 15 pts max"""
    pts = 0
    if data["worksharing_enabled"]:  pts += 5  # worksharing enabled
    if "_" in data["model_name"]:    pts += 5  # naming convention: DISC_ProjectName
    if data["warnings"] < 1000:      pts += 5  # model clean enough for automation
    return max(pts, 0), 15


# ---------------------------------------------------------------------------
# Score assembly
# ---------------------------------------------------------------------------

SCORING_CATEGORIES = [
    ("Warnings",     score_warnings),
    ("FileSize",     score_file_size),
    ("CAD",          score_cad),
    ("Families",     score_families),
    ("Views",        score_views),
    ("Worksets",     score_worksets),
    ("Coordination", score_coordination),
    ("Standards",    score_standards),
]


def classify_status(score):
    if score >= 130:   return "Elite"
    elif score >= 115: return "Excellent"
    elif score >= 100: return "Healthy"
    elif score >= 85:  return "Needs Cleanup"
    else:              return "Critical"


def assemble_score(data):
    """Run all 8 scoring functions. Returns (total_score, scores_dict)."""
    scores = {}
    total = 0
    for name, fn in SCORING_CATEGORIES:
        pts, _ = fn(data)
        scores[name] = pts
        total += pts
    return max(total, 0), scores


# ---------------------------------------------------------------------------
# CSV export — appends one row, creates file+headers if needed
# ---------------------------------------------------------------------------

def export_csv(data, total_score, scores):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_exists = os.path.exists(OUTPUT_CSV)

    row = [
        date.today().isoformat(),
        data["model_name"],
        total_score,
        classify_status(total_score),
        data["warnings"],
        round(data["file_size_mb"], 2),
        data["cad_imports"],
        data["inplace_families"],
        data["view_count"],
        data["workset_count"],
        data["link_count"],
        data["worksharing_enabled"],
        scores["Warnings"],
        scores["FileSize"],
        scores["CAD"],
        scores["Families"],
        scores["Views"],
        scores["Worksets"],
        scores["Coordination"],
        scores["Standards"],
    ]

    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(CSV_HEADERS)
        writer.writerow(row)

    print("MODEL HEALTH SCORE: {}/150 — {}".format(total_score, classify_status(total_score)))
    print("Appended to: {}".format(OUTPUT_CSV))


# ---------------------------------------------------------------------------
# Main — pyRevit executes module-level code when the button is clicked
# ---------------------------------------------------------------------------

doc = revit.doc
model_data = collect_model_data(doc)
total_score, scores = assemble_score(model_data)
export_csv(model_data, total_score, scores)
```

**Step 2: Verify**

Read `BIMTools.extension/BIM.panel/HealthScore.pushbutton/script.py` back (first 80 lines) and confirm the config block, data collection function signature, and first two scoring functions are present.

---

### Task 3: Update `BIM Score implementation Plan.md`

**Files:**
- Overwrite: `BIM Score implementation Plan.md`

**Step 1: Rewrite the file**

Replace the entire file with this content:

```markdown
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

| Category | Max Points | Automated Checks |
|---|---|---|
| Model Warnings | 25 | Warning count tiers; −5 for critical warnings |
| Model Size & Performance | 20 | File size tiers; cloud models score mid-tier |
| CAD & External Content | 20 | Imported CAD count; +5 if using CAD links |
| Families & Modeling Practices | 25 | In-place family count; +5 if total families <500 |
| Views & Documentation | 15 | View count; +5 if >80% have view template |
| Worksets & Links | 15 | Workset count; link presence; −5 if >25 worksets |
| Clash & Coordination Readiness | 15 | Levels defined; shared coordinates; links loaded |
| Automation & Data Standards | 15 | Worksharing; naming convention; warnings <1000 |

**Total possible: 150 points**

Manual checks (origin placement, compact central, nested family optimization) are not automated — those bonus points are not awarded.

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
| Score_Warnings … Score_Standards | Per-category points (8 columns) |

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

For scanning multiple models in batch, a Dynamo workflow is documented below.

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

The Python scoring logic (warning tiers, size tiers, etc.) from `script.py` can be ported directly into a Dynamo Python node using the same thresholds.

---

## Phase 5 Upgrade Path

The pyRevit scoring script here exports results to a flat CSV — this is the **Phase 3 model health** layer.

`BIM compliance dashboard Requirements.md` (Phase 5) replaces this with the `FactModelHealth` append-only table, which adds:
- `RunId` and `RunDateTime` for time-series tracking
- `Portfolio_ProjectID` and `Portfolio_Discipline` for cross-project comparison
- Governance scoring and growth velocity metrics
- Cloud-model safe keying (does not rely on `doc.PathName`)
```

**Step 2: Verify**

Read the first 50 lines of `BIM Score implementation Plan.md` back to confirm formatting is intact.

---

## Roadmap (Not in scope now)

- pyRevit output dialog showing score breakdown (Phase 2)
- Dynamo multi-model batch scanner as a separate deliverable
- Phase 5 migration to `FactModelHealth` table (`BIM compliance dashboard Requirements.md`)
```
