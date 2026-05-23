"""
script.py — pyRevit Model Health Scorer (150-point scale)

Button: BIM > Model Health Score
Runs from pyRevit inside Revit. Scores the current model across 8 categories.
Appends one row to model_health_scores.csv for Power BI trend tracking.

Silent operation — output visible in pyRevit console if open.

Note: Some rubric checks are not automatable (origin placement, nested family
optimization, compact central model). The effective automatable ceiling is
~135/150. Elite status (>=130) is still reachable on a well-maintained model.

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

    # --- Shared coordinates ---
    # Proxy: site location name is non-default, indicating shared coordinates were set.
    # More reliable than reading survey point position, which is unreliable when clipped.
    try:
        site_name = doc.SiteLocation.PlaceName
        data["shared_coordinates"] = bool(site_name and site_name.strip())
    except Exception:
        data["shared_coordinates"] = False

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
    # Effective max automatable: 15/20 pts
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
    # Effective max automatable: 15/25 pts
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
    if wc > 0:                 pts += 5  # logical worksets present
    if data["link_count"] > 0: pts += 5  # linked models attached
    if 0 < wc <= 20:           pts += 5  # workset count reasonable

    if wc > 25:
        pts -= 5  # penalty for excessive worksets

    return max(pts, 0), 15


def score_coordination(data):
    """Category 7: Clash & Coordination Readiness — 15 pts max"""
    pts = 0
    if data["level_count"] > 0:    pts += 5  # levels defined
    if data["shared_coordinates"]: pts += 5  # shared coordinates established
    if data["link_count"] > 0:     pts += 5  # links loaded
    return max(pts, 0), 15


def score_standards(data):
    """Category 8: Automation & Data Standards — 15 pts max"""
    pts = 0
    if data["worksharing_enabled"]: pts += 5  # worksharing enabled
    if "_" in data["model_name"]:   pts += 5  # naming convention: DISC_ProjectName
    if data["warnings"] < 1000:     pts += 5  # model clean enough for automation
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

import traceback

try:
    doc = revit.doc
    model_data = collect_model_data(doc)
    total_score, scores = assemble_score(model_data)
    export_csv(model_data, total_score, scores)
except Exception:
    print("ERROR: Model Health Scorer failed. Details below:")
    print(traceback.format_exc())
    print("Check OUTPUT_DIR path and Revit model state, then try again.")
