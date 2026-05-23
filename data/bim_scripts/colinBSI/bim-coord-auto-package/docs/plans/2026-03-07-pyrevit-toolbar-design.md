# pyRevit BIM Coordinator Toolbar — Design Document
**Date:** 2026-03-07
**Status:** Approved

---

## Overview

Build 21 production pyRevit scripts across 5 panels of `BIMTools.extension/`, plus a shared utility library. The health scorer (BIM.panel) is already built.

---

## Architecture

**Pattern:** Shared lib + thin script.py per button (Option B)

```
BIMTools.extension/
├── BIM.panel/
│   └── HealthScore.pushbutton/script.py   ← already built
├── lib/
│   ├── __init__.py
│   └── bim_utils.py                        ← shared utilities
├── Project_Setup.panel/                    ← 6 tools
├── Model_Health.panel/                     ← 6 tools
├── Coordination.panel/                     ← 6 tools
├── Reporting.panel/                        ← 2 tools
└── Utilities.panel/                        ← 1 tool
```

---

## Shared Library (`lib/bim_utils.py`)

Provides to all scripts:
- `OUTPUT_DIR` — `C:\BIM_Automation\data\output`
- `append_csv(filename, headers, row)` — creates file+headers if needed, appends row
- `confirm(message)` — pyRevit TaskDialog, returns True/False
- `get_warnings(doc)` — returns all FailureMessage objects
- `get_views(doc, exclude_templates=True)` — returns non-template View list
- `get_families(doc)` — returns all Family elements
- `get_links(doc)` — returns all RevitLinkInstance elements
- `get_import_instances(doc)` — returns all ImportInstance elements
- `get_worksets(doc)` — returns all user worksets (requires workshared model)

---

## Panel 1 — Project Setup (6 tools)

All tools are **idempotent** — safe to run twice (skip if element already exists).

| Tool | Folder | Confirmation | What it does |
|---|---|---|---|
| Initialize Project | `InitializeProject.pushbutton` | Yes | Runs all 5 setup tools in sequence |
| Create Worksets | `CreateWorksets.pushbutton` | No | Creates 11 standard worksets |
| Load Shared Parameters | `LoadSharedParams.pushbutton` | No | Adds 6 parameters to Project Information |
| Setup Coordination Views | `SetupViews.pushbutton` | No | Creates 7 standard 3D views |
| Create Standard Sheets | `CreateSheets.pushbutton` | No | Creates 5 standard sheets |
| Setup Browser Org | `BrowserOrg.pushbutton` | No | Applies browser organization by Type/Discipline |

**Standard worksets (11):** Shared Levels & Grids, Arch, Structure, Mechanical, Electrical, Plumbing, Civil, Plant, Links, Coordination, Scan

**Standard parameters (6):** Clash_Status, Issue_ID, Issue_Status, Coordination_Zone, Discipline, Model_Author

**Standard 3D views (7):** 3D - Coordination, 3D - Navisworks, 3D - Clash Review, 3D - Worksets, 3D - Linked Models, 3D - QAQC, 3D - Scan Reference

**Standard sheets (5):** G000 Cover, G001 General Notes, G100 Level Plans, G200 Sections, G300 Coordination

---

## Panel 2 — Model Health (6 tools)

All tools are **read-only** — no confirmation needed. Output CSV to `BIM_Automation/data/output/`.

| Tool | Folder | Output CSV | Key columns |
|---|---|---|---|
| Warning Manager | `WarningManager.pushbutton` | `warnings_report.csv` | Description, Count, Severity |
| Find CAD Imports | `FindCADImports.pushbutton` | `cad_imports_report.csv` | ElementID, Name, Workset, ViewName |
| Find Large Families | `FindLargeFamilies.pushbutton` | `large_families_report.csv` | FamilyName, Category, SizeMB |
| Group Inspector | `GroupInspector.pushbutton` | `groups_report.csv` | GroupName, Type, InstanceCount, NestedCount |
| Unplaced Views Finder | `UnplacedViews.pushbutton` | `unplaced_views_report.csv` | ViewName, ViewType, Discipline, Level |
| Unused Families Cleaner | `UnusedFamilies.pushbutton` | `unused_families_report.csv` | FamilyName, Category, TypeCount |

Unused Families Cleaner is **list-only** — no automatic purge.

---

## Panel 3 — Coordination (6 tools)

| Tool | Folder | Confirmation | What it does |
|---|---|---|---|
| Create Clash Views | `CreateClashViews.pushbutton` | No | Creates one 3D view per discipline pair: `3D - Clash - DISC_A vs DISC_B` |
| Color by Workset | `ColorByWorkset.pushbutton` | No | Solid fill color overrides by workset in active view |
| Color by Discipline | `ColorByDiscipline.pushbutton` | No | Solid fill color overrides by Discipline parameter in active view |
| Clash Status Manager | `ClashStatusManager.pushbutton` | No | Sets Clash_Status on selected elements via dialog (Open/In Progress/Resolved) |
| Zone Checker | `ZoneChecker.pushbutton` | No | Lists elements with missing Coordination_Zone → `zone_check_report.csv` |
| Interference Check | `InterferenceCheck.pushbutton` | No | Runs Revit built-in interference check on links vs model |

Color tools apply to **active view only** — no model changes.

---

## Panel 8 — Reporting (2 tools)

| Tool | Folder | Output CSV | Source |
|---|---|---|---|
| Coordination Report | `CoordReport.pushbutton` | `coordination_report.csv` | Compiles from existing output CSVs (health score, warnings, unplaced views, CAD imports) |
| Clash Summary Report | `ClashSummary.pushbutton` | `clash_summary_report.csv` | Reads Clash_Status parameter from model elements |

Coordination Report reads from existing CSVs rather than re-querying Revit API. Missing source CSVs show "N/A".

---

## Panel 9 — Utilities (1 tool)

| Tool | Folder | Confirmation | What it does |
|---|---|---|---|
| Sync and Close | `SyncAndClose.pushbutton` | Yes | Sync with central, relinquish all worksets, close document |

---

## Confirmation Behaviour

- **Destructive/irreversible actions:** Initialize Project, Sync and Close → confirm dialog required
- **All other tools:** silent (output visible in pyRevit console / CSV)

---

## Out of Scope

- Panels 4 (Model Fixing), 5 (Sheets & Views), 6 (Links & Imports), 7 (Navisworks) — not in this build
- Automatic purge in Unused Families Cleaner
- Phase 5 `Portfolio_` parameter migration
