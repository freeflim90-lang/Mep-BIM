# README & Tool Documentation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a root README.md and 7 user-facing tool docs in docs/tools/ for BIM coordinators and Revit users.

**Architecture:** Root README covers overview, install, and workflow. Seven panel/pipeline docs in docs/tools/ each follow a consistent format: panel overview, prerequisites, per-tool sections (Purpose / When to use / How to use / Output), and tips.

**Tech Stack:** Markdown only. No code changes. Verification = read file back after writing.

---

### Task 1: Create docs/tools/ directory marker and README.md

**Files:**
- Create: `docs/tools/.gitkeep` (empty, ensures folder exists)
- Create: `README.md` (root)

**Step 1: Create docs/tools/ placeholder**

Write an empty file at `docs/tools/.gitkeep`.

**Step 2: Write README.md at repo root**

Full content:

```markdown
# BIM Coordination Auto Package

A complete BIM coordination system for Revit and Navisworks projects. Includes a pyRevit toolbar (22 scripts), a Python automation pipeline, and Power BI dashboard guides.

---

## What It Does

| Component | Description |
|---|---|
| **BIMTools pyRevit Toolbar** | 22 buttons across 5 panels — project setup, model health checks, clash coordination, reporting, and utilities |
| **BIM_Automation Pipeline** | Python script that runs every Wednesday, grouping and prioritizing clashes, then generating CSV/Excel/PDF reports |
| **Power BI Command Center** | 4 dashboards pulling from pipeline output CSVs — project health, clash heat map, coordination performance, model health trends |

---

## Prerequisites

| Requirement | Version / Notes |
|---|---|
| Autodesk Revit | 2021 or later (2022+ recommended) |
| pyRevit | 4.8+ — [pyrevitlabs.io](https://pyrevitlabs.io) |
| Python | 3.8+ (for the automation pipeline) |
| Python packages | `pandas`, `openpyxl`, `reportlab` |
| Power BI Desktop | Latest (optional — for dashboards) |
| Windows | Pipeline uses Windows Task Scheduler |

Install Python packages:
```bash
pip install pandas openpyxl reportlab
```

---

## Installation

### pyRevit Toolbar (BIMTools)

**Option A — Manual copy:**
1. Download or clone this repo
2. Copy the `BIMTools.extension` folder to your pyRevit extensions directory:
   ```
   C:\Users\<YourName>\AppData\Roaming\pyRevit\Extensions\
   ```
3. Reload pyRevit (pyRevit tab → Reload)

**Option B — Git clone directly into extensions:**
```bash
cd "C:\Users\<YourName>\AppData\Roaming\pyRevit\Extensions"
git clone https://github.com/colinBSI/bim-coord-auto-package.git BIMTools.extension
```
Then reload pyRevit.

### Python Pipeline (BIM_Automation)

1. Copy the `BIM_Automation` folder to `C:\BIM_Automation\`
2. Install dependencies: `pip install pandas openpyxl reportlab`
3. Schedule `main.py` in Windows Task Scheduler to run every Wednesday at 6:00 AM:
   - Action: `python C:\BIM_Automation\main.py`
   - Trigger: Weekly, Wednesday, 6:00 AM

---

## Folder Structure

```
BIM Coord Auto Package/
├── BIMTools.extension/          pyRevit toolbar (22 scripts)
│   ├── lib/bim_utils.py         Shared utilities
│   ├── Project_Setup.panel/     6 setup buttons
│   ├── Model_Health.panel/      6 health check buttons
│   ├── Coordination.panel/      6 clash workflow buttons
│   ├── Reporting.panel/         2 reporting buttons
│   └── Utilities.panel/         2 utility buttons
├── BIM_Automation/              Python pipeline
│   ├── main.py                  Master runner
│   ├── config.py                Paths and settings
│   ├── clash_processing/        Parser, grouper, prioritizer
│   ├── reports/                 Report generator (CSV/Excel/PDF)
│   ├── acc_integration/         ACC stub (Phase 2)
│   └── data/
│       ├── input/               Drop Navisworks exports here
│       └── output/              Reports written here
└── docs/
    ├── tools/                   Tool documentation (this folder)
    └── powerbi/                 Power BI build guide
```

---

## Weekly Workflow

| Day | Who | Action |
|---|---|---|
| **Monday** | BIM Coordinator | Upload Revit models to ACC |
| **Tuesday** | BIM Coordinator | Run Navisworks clash detection; export CSV and XML to `BIM_Automation\data\input\` |
| **Wednesday** | Automated (6 AM) | Pipeline runs: groups clashes, assigns priority, generates reports |
| **Wednesday** | BIM Coordinator | Run **ExportGrids** in Revit to refresh grid/level data |
| **Thursday** | BIM Coordinator | Review reports; create ACC issues for critical clashes |
| **Friday** | Team | Coordination meeting using Power BI dashboards + PDF report |

---

## Tool Documentation

| Doc | Panel / Component |
|---|---|
| [Project Setup](docs/tools/01-project-setup.md) | Initialize worksets, views, sheets, shared parameters |
| [Model Health](docs/tools/02-model-health.md) | Warnings, CAD imports, large families, unused elements |
| [Coordination](docs/tools/03-coordination.md) | Clash views, color overrides, clash status tracking |
| [Reporting](docs/tools/04-reporting.md) | Coordination reports and clash summaries |
| [Utilities](docs/tools/05-utilities.md) | ExportGrids and SyncAndClose |
| [Pipeline](docs/tools/06-pipeline.md) | Python automation pipeline reference |
| [Power BI](docs/tools/07-power-bi.md) | Dashboard setup and data sources |

---

## Model Health Score

The **HealthScore** button generates a 150-point score across 8 categories. Scores are logged to `model_health_scores.csv` for trend tracking in Power BI.

| Score | Rating |
|---|---|
| ≥ 130 | Elite |
| ≥ 115 | Excellent |
| ≥ 100 | Healthy |
| ≥ 85 | Needs Cleanup |
| < 85 | Critical |

> Minimum score of 100 required before a model enters active coordination.

---

## License

MIT
```

**Step 3: Read README.md back to verify it looks correct**

Read `README.md` and confirm all sections are present and links are correct.

**Step 4: Commit**

```bash
git add README.md docs/tools/.gitkeep
git commit -m "docs: add root README and docs/tools directory"
```

---

### Task 2: Write docs/tools/01-project-setup.md

**Files:**
- Create: `docs/tools/01-project-setup.md`

**Step 1: Write the file**

Full content:

```markdown
# Project Setup Panel

The Project Setup panel initializes a new Revit model with standard worksets, shared parameters, views, and sheets. Run these tools once at project start on each Revit model.

> All setup tools are **idempotent** — running them a second time skips items that already exist.

---

## Tools

### Initialize Project

**Purpose:** Master setup runner. Runs all other Project Setup tools in sequence.

**When to use:** Once at the start of a new project, on each discipline model.

**How to use:**
1. Open the Revit model (must be a workshared model)
2. Click **Initialize Project**
3. Confirm the dialog prompt
4. Wait for completion — check the pyRevit console for a summary

**What it does:**
1. Creates standard worksets
2. Loads coordination shared parameters
3. Creates standard 3D views
4. Creates standard sheets
5. Applies browser organization

> Requires confirmation before running. Takes 10–30 seconds depending on model size.

---

### Create Worksets

**Purpose:** Creates 11 standard worksets for discipline ownership and link management.

**When to use:** On any new workshared model before linking files.

**How to use:**
1. Click **Create Worksets**
2. Check pyRevit console for skipped (already exist) vs. created worksets

**Worksets created:**

| Workset | Purpose |
|---|---|
| Shared Levels & Grids | Levels and grids (all disciplines) |
| Arch | Architectural elements |
| Structure | Structural elements |
| Mechanical | HVAC elements |
| Electrical | Electrical elements |
| Plumbing | Plumbing elements |
| Civil | Civil/site elements |
| Plant | Equipment |
| Links | All linked Revit files |
| Coordination | Clash review elements |
| Scan | Point cloud files (RCP/RCS) |

---

### Load Shared Parameters

**Purpose:** Loads 6 coordination shared parameters into the model, bound to the Project Information category.

**When to use:** After worksets are created, before coordination begins.

**How to use:**
1. Click **Load Shared Parameters**
2. Check pyRevit console for confirmation

**Parameters loaded:**

| Parameter | Use |
|---|---|
| Clash_Status | Track clash resolution: Open / In Progress / Resolved |
| Issue_ID | ACC issue reference number |
| Issue_Status | ACC issue status |
| Coordination_Zone | Zone designation for clash grouping |
| Discipline | Discipline classification |
| Model_Author | Who owns this model |

---

### Setup Views

**Purpose:** Creates 7 standard 3D views for coordination and quality control.

**When to use:** After worksets are created.

**How to use:**
1. Click **Setup Views**
2. Views appear in the Project Browser under 3D Views

**Views created:**

| View Name | Purpose |
|---|---|
| 3D-Coordination | General coordination review |
| 3D-Navisworks | Export to Navisworks (NWC) |
| 3D-Clash Review | Active clash review sessions |
| 3D-Worksets | Color by workset visibility checks |
| 3D-Linked Models | All links visible |
| 3D-QAQC | Quality control review |
| 3D-Scan Reference | Point cloud overlay |

---

### Create Sheets

**Purpose:** Creates 5 baseline coordination sheets.

**When to use:** At project start for documentation structure.

**How to use:**
1. Click **Create Sheets**
2. Sheets appear in the Project Browser

**Sheets created:**

| Number | Name |
|---|---|
| G000 | Cover |
| G001 | General Notes |
| G100 | Level Plans |
| G200 | Sections |
| G300 | Coordination |

---

### Browser Organization

**Purpose:** Applies standard browser organization rules based on Discipline or Type parameters.

**When to use:** After views and sheets are created; or when browser organization looks disorganized.

**How to use:**
1. Click **Browser Org**
2. If a matching organization scheme is found (discipline- or type-based), it is applied automatically

---

## Tips

- Run **Initialize Project** instead of each tool individually when setting up a new model from scratch
- If a workset or view already exists with the correct name, the tool skips it — no duplicates are created
- Check the pyRevit console (pyRevit tab → Console) for a detailed log of what was created vs. skipped
```

**Step 2: Read file back to verify**

**Step 3: Commit**

```bash
git add docs/tools/01-project-setup.md
git commit -m "docs: add Project Setup panel documentation"
```

---

### Task 3: Write docs/tools/02-model-health.md

**Files:**
- Create: `docs/tools/02-model-health.md`

**Step 1: Write the file**

Full content:

```markdown
# Model Health Panel

The Model Health panel provides read-only diagnostic tools. Use these tools to audit a Revit model before coordination, after model receipt, or as part of a weekly health check.

> All Model Health tools are **read-only** — they never modify the model.

---

## Tools

### Warning Manager

**Purpose:** Exports all Revit warnings to a CSV, classified by severity.

**When to use:**
- Weekly health checks
- Before issuing a model health score
- After receiving a model from a subcontractor

**How to use:**
1. Open the Revit model
2. Click **Warning Manager**
3. Report is saved to `C:\BIM_Automation\data\output\warnings_report.csv`

**Output columns:** Warning message, element IDs, severity classification

**Severity classification:**

| Severity | Keywords |
|---|---|
| Critical | corrupt, overlap |
| High | duplicate, joins |
| Medium | all other warnings |

**Targets:**
- Ideal: fewer than 300 warnings
- Acceptable: fewer than 1,000 warnings

---

### Find CAD Imports

**Purpose:** Lists all CAD files that have been imported (not linked) into the model.

**When to use:** When auditing a model received from a subcontractor, or as part of setup QC.

**How to use:**
1. Click **Find CAD Imports**
2. Results appear in the pyRevit console

**Why it matters:** Imported CAD files increase file size and can cause performance issues. They should be linked instead.

**Action:** For each CAD import found, delete it and re-insert as a linked file (Insert → Link CAD).

---

### Find Large Families

**Purpose:** Identifies Revit families larger than 5 MB.

**When to use:**
- When model file size exceeds targets
- During model audits

**How to use:**
1. Click **Find Large Families**
2. Results appear in the pyRevit console with family name and size

**File size targets:**
- Ideal: under 300 MB total model size
- Acceptable: under 500 MB

**Action:** Replace oversized families with leaner versions, or purge unused types from within the family.

---

### Group Inspector

**Purpose:** Reports on all groups in the model — count, types, and nested groups.

**When to use:** When investigating model warnings related to groups, or during cleanup.

**How to use:**
1. Click **Group Inspector**
2. Results appear in the pyRevit console

**What to look for:** Large numbers of nested groups or ungrouped instances can cause warnings and slow performance.

---

### Unplaced Views

**Purpose:** Lists all views that exist in the model but are not placed on any sheet.

**When to use:** Before issuing a model for coordination or at project closeout.

**How to use:**
1. Click **Unplaced Views**
2. Results appear in the pyRevit console

**Action:** Delete views that are no longer needed, or place them on sheets if they are required for documentation.

---

### Unused Families

**Purpose:** Exports a list of families loaded into the model with zero placed instances.

**When to use:** Before model health scoring or when reducing file size.

**How to use:**
1. Click **Unused Families**
2. Report saved to `C:\BIM_Automation\data\output\unused_families_report.csv`

> This tool only **reports** — it does not purge. Use Revit's native Purge Unused (Manage tab) to remove families after reviewing the report.

---

## Model Health Score

The **HealthScore** button (BIM panel) runs all health checks automatically and generates a 150-point score. See the root [README](../../README.md#model-health-score) for score thresholds.

---

## Tips

- Run all Model Health tools when you first receive a model from a new subcontractor
- The Warning Manager and Unused Families reports feed into the Power BI Model Health Trends dashboard
- A model must score 100 or higher before entering active coordination
```

**Step 2: Read file back to verify**

**Step 3: Commit**

```bash
git add docs/tools/02-model-health.md
git commit -m "docs: add Model Health panel documentation"
```

---

### Task 4: Write docs/tools/03-coordination.md

**Files:**
- Create: `docs/tools/03-coordination.md`

**Step 1: Write the file**

Full content:

```markdown
# Coordination Panel

The Coordination panel supports active clash review workflows. Use these tools during weekly coordination sessions (Tuesday clash detection through Thursday ACC issue creation).

---

## Tools

### Create Clash Views

**Purpose:** Generates 15 standard 3D views, one per discipline pair, for clash review.

**When to use:** Once at project start, or when new discipline pairs are added to the project.

**How to use:**
1. Click **Create Clash Views**
2. Views appear in the Project Browser

**Views created (examples):**
- Clash - Arch vs Structure
- Clash - Structure vs Mechanical
- Clash - Mechanical vs Plumbing
- Clash - Arch vs Mechanical
- *(and 11 more discipline pairs)*

> Idempotent — if a view with that name already exists, it is skipped.

---

### Color By Workset

**Purpose:** Applies solid color overrides to all elements in the active view, grouped by workset.

**When to use:**
- To visually verify workset assignments
- To identify elements accidentally placed on the wrong workset

**How to use:**
1. Open a 3D view (e.g., 3D-Worksets)
2. Click **Color By Workset**
3. Each workset is assigned a unique solid fill color

> Overrides are applied to the active view only. Switch to a different view to remove them.

---

### Color By Discipline

**Purpose:** Applies solid color overrides to all elements in the active view, grouped by the Discipline parameter.

**When to use:**
- To visually verify discipline assignments on linked models
- During coordination meetings to distinguish disciplines quickly

**How to use:**
1. Open a 3D view
2. Click **Color By Discipline**
3. Up to 8 disciplines are assigned unique colors

---

### Clash Status Manager

**Purpose:** Updates the `Clash_Status` shared parameter on selected elements.

**When to use:** During clash review sessions to mark progress.

**How to use:**
1. Select the elements involved in a clash
2. Click **Clash Status Manager**
3. Choose a status from the dialog:
   - **Open** — newly identified, not yet assigned
   - **In Progress** — assigned and being resolved
   - **Resolved** — clash has been corrected

**Status values feed into:** Power BI Coordination Performance dashboard and weekly PDF report.

---

### Zone Checker

**Purpose:** Verifies that elements have a valid `Coordination_Zone` parameter value assigned.

**When to use:**
- After model setup to confirm zones are assigned
- Before running the Python pipeline (zones are used for clash grouping)

**How to use:**
1. Click **Zone Checker**
2. Results appear in the pyRevit console listing elements with missing or invalid zone values

---

### Interference Check

**Purpose:** Launches Revit's native Interference Check dialog.

**When to use:** For quick in-Revit clash detection without exporting to Navisworks.

**How to use:**
1. Click **Interference Check**
2. Revit's built-in Interference Check dialog opens
3. Select categories to check and run

> For full project coordination, use Navisworks for clash detection and the Python pipeline for processing results. Use this tool for quick spot checks only.

---

## Coordination Tolerances

| Type | Tolerance |
|---|---|
| Hard clash | 0 in |
| MEP clearance | 1–2 in |
| Equipment clearance | 24–36 in |

---

## Tips

- Use **Color By Workset** and **Color By Discipline** in the dedicated 3D views (3D-Worksets, 3D-Coordination) created by the Project Setup panel
- **Clash Status Manager** works on multi-selection — select all elements involved in a clash group before running
- The Zone Checker should pass before Tuesday's Navisworks export, so zones are valid in the clash report
```

**Step 2: Read file back to verify**

**Step 3: Commit**

```bash
git add docs/tools/03-coordination.md
git commit -m "docs: add Coordination panel documentation"
```

---

### Task 5: Write docs/tools/04-reporting.md

**Files:**
- Create: `docs/tools/04-reporting.md`

**Step 1: Write the file**

Full content:

```markdown
# Reporting Panel

The Reporting panel generates coordination reports directly from Revit. For the full weekly pipeline report (from Navisworks exports), see the [Pipeline](06-pipeline.md) documentation.

---

## Tools

### Coordination Report

**Purpose:** Generates a coordination status report combining model health metrics, clash data, warnings, and open issues.

**When to use:** On demand — before coordination meetings or when a status summary is needed.

**How to use:**
1. Click **Coord Report**
2. Report is saved to `C:\BIM_Automation\data\output\`

**Output:** CSV/Excel report with:
- Model health summary
- Clash metrics (open, in progress, resolved)
- Warning counts
- Open issues

---

### Clash Summary

**Purpose:** Generates a summary of open and resolved clashes grouped by discipline pair.

**When to use:**
- Friday coordination meetings
- Weekly status updates

**How to use:**
1. Click **Clash Summary**
2. Report is saved to `C:\BIM_Automation\data\output\`

**Output columns:** Discipline pair, total clashes, open, in progress, resolved

---

## Tips

- The Python pipeline (run automatically each Wednesday) generates a more complete report including prioritization and PDF output — see [Pipeline documentation](06-pipeline.md)
- Reporting panel tools pull live data from the open Revit model; the pipeline pulls from Navisworks CSV exports
- All outputs go to `C:\BIM_Automation\data\output\` — this is the same folder Power BI reads from
```

**Step 2: Read file back to verify**

**Step 3: Commit**

```bash
git add docs/tools/04-reporting.md
git commit -m "docs: add Reporting panel documentation"
```

---

### Task 6: Write docs/tools/05-utilities.md

**Files:**
- Create: `docs/tools/05-utilities.md`

**Step 1: Write the file**

Full content:

```markdown
# Utilities Panel

The Utilities panel contains infrastructure tools that support the broader automation pipeline.

---

## Tools

### Export Grids

**Purpose:** Exports grid line positions and level elevations from the active Revit model to CSV files used by the Python clash pipeline.

**When to use:** Every Wednesday before the automation pipeline runs — or any time grids or levels change.

**How to use:**
1. Open the Revit coordination model (the model containing grids and levels)
2. Click **Export Grids**
3. Two files are written to `C:\BIM_Automation\data\output\`

**Output files:**

| File | Contents |
|---|---|
| `grid_lines.csv` | Grid name, orientation (H/V), position in feet |
| `level_elevations.csv` | Level name, elevation in feet |

**Why it matters:** The Python pipeline uses these files to map each clash's XYZ coordinates to a grid zone and level name. Without up-to-date grid/level data, the clash heat map will be inaccurate.

> Compatible with Revit 2021 and 2022+ (handles the UnitUtils API change automatically).

---

### Sync and Close

**Purpose:** Saves and syncs the model to central, then closes it.

**When to use:**
- At the end of a work session
- Before handing a model off to another team member

**How to use:**
1. Click **Sync and Close**
2. Confirm the dialog prompt
3. The model syncs to central and closes automatically

> Requires confirmation before running. Do not use if you have unsaved work you want to discard — sync will commit all local changes.

---

## Tips

- Add **Export Grids** to your Wednesday morning checklist, before the 6 AM pipeline run
- If grid lines or levels were modified since the last export, re-run Export Grids and verify that `grid_lines.csv` and `level_elevations.csv` in the output folder have today's date
```

**Step 2: Read file back to verify**

**Step 3: Commit**

```bash
git add docs/tools/05-utilities.md
git commit -m "docs: add Utilities panel documentation"
```

---

### Task 7: Write docs/tools/06-pipeline.md

**Files:**
- Create: `docs/tools/06-pipeline.md`

**Step 1: Write the file**

Full content:

```markdown
# Python Automation Pipeline

The `BIM_Automation` pipeline is a Python script that runs automatically every Wednesday at 6:00 AM. It takes Navisworks clash exports from Tuesday, processes them, and generates reports for the Friday coordination meeting.

---

## Weekly Input / Output

### Inputs (drop to `C:\BIM_Automation\data\input\` by Tuesday EOD)

| File | Source | Required? |
|---|---|---|
| `*.csv` | Navisworks clash export (CSV format) | Yes |
| `clash_report.xml` | Navisworks clash export (XML format) | Optional (enables heat map) |

Also required in `C:\BIM_Automation\data\output\` (written by **Export Grids** pyRevit button):
- `grid_lines.csv`
- `level_elevations.csv`

### Outputs (written to `C:\BIM_Automation\data\output\`)

| File | Description |
|---|---|
| `weekly_coordination_report.csv` | Full enriched clash list with priority and group key |
| `weekly_coordination_report.xlsx` | 3-tab Excel: Summary, Discipline Breakdown, High Risk Areas |
| `weekly_coordination_report.pdf` | 1-page styled summary for Friday meeting |
| `clash_heatmap_data.csv` | Clash counts by grid zone and level (Power BI heat map source) |
| `pipeline_metadata.json` | Run status, timestamp, clash count |

---

## Pipeline Stages

| Stage | Module | Description |
|---|---|---|
| 0 | `clash_parser.py` | Parses Navisworks XML → heat map CSV (skipped if XML absent) |
| 1 | `clash_grouper.py` | Groups clashes by level, discipline pair, and grid zone |
| 2 | `clash_prioritizer.py` | Assigns priority: Critical / High / Medium / Low |
| 3 | `report_generator.py` | Writes CSV, Excel, and PDF reports |
| 4 | `issue_stub.py` | Simulates ACC issue creation (Phase 2: live API) |
| 5 | `metadata_writer.py` | Writes pipeline run metadata to JSON |

---

## Priority Classification

| Priority | Rule |
|---|---|
| **Critical** | Either discipline is Structure or Structural |
| **High** | Either discipline is Mechanical or Plumbing |
| **Medium** | All other discipline combinations |
| **Low** | Cosmetic pairs: Lighting/Ceiling, Lighting/Furniture, Ceiling/Furniture |

---

## Excel Report Tabs

**Summary tab:**
- Total clashes
- Count by priority (Critical / High / Medium / Low)
- Number of unique clash groups

**Discipline Breakdown tab:**
- Clash count per discipline pair, sorted descending

**High Risk Areas tab:**
- Clash groups with 20 or more clashes

---

## Scheduling (Windows Task Scheduler)

The pipeline is set to run weekly via Windows Task Scheduler:

- **Script:** `C:\BIM_Automation\main.py`
- **Trigger:** Weekly, Wednesday, 6:00 AM
- **Action:** `python C:\BIM_Automation\main.py`

To set up manually:
1. Open Task Scheduler
2. Create Basic Task → name it "BIM Automation Pipeline"
3. Trigger: Weekly → Wednesday → 6:00 AM
4. Action: Start a program → `python` → Arguments: `C:\BIM_Automation\main.py`

---

## Logs

Logs are written to `C:\BIM_Automation\logs\pipeline.log`.
- Rotating log: 5 MB per file, 6 weeks of history retained
- Check this file if the pipeline fails or reports are missing on Wednesday morning

---

## After the Pipeline Runs

1. Open Power BI Command Center and refresh the dataset
2. Review `weekly_coordination_report.xlsx` for Critical and High priority clashes
3. The PDF (`weekly_coordination_report.pdf`) is ready to distribute for the Friday meeting

---

## Troubleshooting

| Problem | Check |
|---|---|
| No output files | Check `logs/pipeline.log` for errors |
| Heat map not updated | Ensure `clash_report.xml` was dropped in `data/input/` |
| Wrong grid zones | Re-run **Export Grids** in Revit; verify `grid_lines.csv` is current |
| Pipeline didn't run | Check Task Scheduler — verify the task is enabled and the trigger fired |
| Missing clash records | Verify Navisworks CSV format matches expected columns |

---

## Phase 2 (Planned)

- Live ACC issue creation via Autodesk Issues API (replaces `issue_stub.py`)
- Automatic Power BI dataset push (replaces manual refresh)
- Email alert on pipeline failure
```

**Step 2: Read file back to verify**

**Step 3: Commit**

```bash
git add docs/tools/06-pipeline.md
git commit -m "docs: add Pipeline documentation"
```

---

### Task 8: Write docs/tools/07-power-bi.md and push

**Files:**
- Create: `docs/tools/07-power-bi.md`

**Step 1: Write the file**

Full content:

```markdown
# Power BI Command Center

The Power BI Command Center connects to the pipeline output CSVs and provides four dashboards for coordination tracking.

For the complete build guide (DAX measures, conditional formatting, step-by-step setup), see:

**[docs/powerbi/command-center-setup.md](../powerbi/command-center-setup.md)**

---

## Four Dashboards

| Dashboard | What It Shows |
|---|---|
| **Project Health** | Model health score by discipline, warning counts, file sizes |
| **Clash Heat Map** | Spatial clash density by grid zone and level |
| **Coordination Performance** | Open vs. resolved clashes over time; discipline pair breakdown |
| **Model Health Trends** | Health score history per model over time |

---

## Data Sources

All dashboards read from `C:\BIM_Automation\data\output\`:

| File | Used By |
|---|---|
| `weekly_coordination_report.csv` | Coordination Performance |
| `clash_heatmap_data.csv` | Clash Heat Map |
| `model_health_scores.csv` | Project Health, Model Health Trends |
| `warnings_report.csv` | Project Health |

---

## Refresh Schedule

Power BI does not refresh automatically in the current setup. After the Wednesday pipeline run:

1. Open Power BI Desktop
2. Click **Home → Refresh**
3. Verify all four dashboards update

> Phase 2 will add automatic dataset push from the Python pipeline — see [Pipeline docs](06-pipeline.md#phase-2-planned).

---

## Quick Start

1. Open Power BI Desktop
2. **Get Data → Text/CSV** → connect to each file in `C:\BIM_Automation\data\output\`
3. Follow the full setup guide: [command-center-setup.md](../powerbi/command-center-setup.md)
```

**Step 2: Read file back to verify**

**Step 3: Commit and push all docs**

```bash
git add docs/tools/07-power-bi.md
git commit -m "docs: add Power BI dashboard documentation"
git push
```

---

## Summary

8 tasks, 8 commits. All documentation is user-facing (BIM coordinators), plain English, consistent format across panel docs.
