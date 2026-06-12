# BIM Package Reconciliation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reconcile 15 BIM coordination markdown files to eliminate scoring conflicts, workflow discrepancies, duplicates, and missing integration context.

**Architecture:** Six sequential priorities — each touching specific files with explicit before/after edits. No new code frameworks. Pure document editing with verification after each task.

**Tech Stack:** Markdown, Python (embedded in docs), pyRevit API references.

---

## PRIORITY 1 — Fix the Scoring System

### Task 1: Rewrite the Python scoring script in `BIM Score implementation Plan.md`

**Files:**
- Modify: `/Users/colin/BIM Coord Auto Package/BIM Score implementation Plan.md`

**Context:** The current script scores a max of 110 pts but the rubric defines 150 pts across 8 categories. Categories 4–8 are wrong or missing entirely.

**Step 1: Locate the scoring block**

Find the section starting with `# SCORING SYSTEM` (around line 207). It runs to approximately line 336.

**Step 2: Replace the entire scoring block**

Replace everything from `score = 0` through `score += 5  # Levels` with:

```python
score = 0

# 1. Model Warnings (25 pts)
if warnings < 100:
    score += 25
elif warnings < 500:
    score += 20
elif warnings < 1000:
    score += 15
elif warnings < 2000:
    score += 10
else:
    score += 5

# 2. Model Size & Performance (20 pts)
if file_size < 300:
    score += 20
elif file_size < 500:
    score += 15
elif file_size < 800:
    score += 10
else:
    score += 5

# 3. CAD & External Content (20 pts)
if cad_imports == 0:
    score += 20
elif cad_imports < 3:
    score += 15
elif cad_imports < 10:
    score += 10
else:
    score += 0

# 4. Families & Modeling Practices (25 pts)
if inplace == 0:
    score += 25
elif inplace <= 3:
    score += 15
else:
    score += 0

# 5. Views & Documentation (15 pts)
if view_count < 300:
    score += 15
elif view_count < 600:
    score += 10
elif view_count < 900:
    score += 5
else:
    score += 0

# 6. Worksets & Links (15 pts)
if 0 < workset_count <= 10:
    score += 10
elif workset_count <= 20:
    score += 7
else:
    score += 3
if link_count > 0:
    score += 5

# 7. Clash & Coordination Readiness (15 pts)
# Proxies: levels defined, links loaded, worksharing enabled
if level_count > 0:
    score += 5
if link_count > 0:
    score += 5
if workset_count > 0:
    score += 5

# 8. Automation & Data Standards (15 pts)
# Proxies: running this script = automation enabled (5),
#          clean model metrics = standards followed (5),
#          naming convention check (5)
auto_score = 5  # Running this script proves automation is enabled
if warnings < 1000 and cad_imports == 0:
    auto_score += 5
if len(model_name) > 5 and "_" in model_name:
    auto_score += 5
score += auto_score

# Max possible: 25+20+20+25+15+15+15+15 = 150
```

**Step 3: Fix the HEALTH STATUS block**

Find the block starting with `if score >= 130:` and replace with:

```python
if score >= 130:
    status = "ELITE"
elif score >= 115:
    status = "EXCELLENT"
elif score >= 100:
    status = "HEALTHY"
elif score >= 85:
    status = "NEEDS CLEANUP"
else:
    status = "CRITICAL"
```

**Step 4: Fix the minimum score standard note**

Find: `Minimum Health Score = 100`
Verify it already says 100. If it says anything else, change it to 100.

**Step 5: Verify max points add up**

Mentally verify: 25+20+20+25+15+15+15+15 = 150. ✓

**Step 6: Verify status labels match `BIM scoring system.md`**

Open `BIM scoring system.md` and confirm the label ranges match:
- Elite: 130–150 ✓
- Excellent: 115–129 ✓
- Healthy: 100–114 ✓
- Needs Cleanup: 85–99 ✓
- Critical: <85 ✓

---

### Task 2: Update score thresholds in `BIM Command Center.md`

**Files:**
- Modify: `/Users/colin/BIM Coord Auto Package/BIM Command Center.md`

**Context:** The Command Center uses a 0–100 scale with a 75-trigger. Replace with the 150-pt thresholds.

**Step 1: Find the threshold reference**

Search for: `Anything below 75 triggers coordination review`

**Step 2: Replace it**

Replace with:
```
Model health is scored out of 150 points using the standard BIM scoring rubric:
- 130–150: Elite
- 115–129: Excellent
- 100–114: Healthy (minimum for coordination entry)
- 85–99: Needs Cleanup (flag for review before coordination)
- Below 85: Critical (reject from coordination)
```

**Step 3: Find the example scoring table**

Find the table:
```
|Metric|Weight|
|Warnings|20|
...
|Unresolved Issues|10|
```

Add a note above it:
```
> Note: The weights below are illustrative for dashboard display. The authoritative 150-point scoring rubric and automated implementation are in `BIM scoring system.md` and `BIM Score implementation Plan.md`.
```

**Step 4: Verify**

Confirm no other references to score thresholds (e.g., "75", "0–100") remain uncorrected in the file.

---

## PRIORITY 2 — Canonical Weekly Workflow

**Canonical schedule (from BIM Coordination Automation Toolkit):**
- Mon — Teams upload models
- Tue — Clash tests run
- Wed — Automation scripts process clashes
- Thu — ACC issues created automatically
- Fri — Coordination meeting using dashboards

### Task 3: Update weekly workflow in `BIM Coordination 101.md`

**Files:**
- Modify: `/Users/colin/BIM Coord Auto Package/BIM Coordination 101.md`

**Step 1: Find the existing timeline table**

Find:
```
|Day|Task|
|Monday|Model uploads|
|Tuesday|Model validation|
|Wednesday|Clash detection|
|Thursday|Coordination meeting|
|Friday|Issue resolution|
```

**Step 2: Replace with canonical schedule**

```
|Day|Task|
|---|---|
|Monday|Model uploads (deadline for all disciplines)|
|Tuesday|Clash tests run in Navisworks|
|Wednesday|Automation scripts process clashes; clash groups generated|
|Thursday|ACC issues created automatically from clash groups|
|Friday|Coordination meeting using dashboards and heat maps|
```

**Step 3: Verify no other day-based schedule tables exist in the file**

Search for "Monday" — confirm only one schedule table.

---

### Task 4: Update weekly workflow in `BIM clash heat map.md`

**Files:**
- Modify: `/Users/colin/BIM Coord Auto Package/BIM clash heat map.md`

**Step 1: Find the Weekly Automated Workflow section**

Find:
```
Monday
Run clash tests
Tuesday
Export clash XML
Wednesday
Run heat map script
Thursday
Power BI dashboard refresh
Friday
Coordination meeting using heat map
```

**Step 2: Replace with canonical schedule**

```
Monday
Teams upload models

Tuesday
Clash tests run in Navisworks; clash XML exported

Wednesday
Heat map script processes clash data; automation scripts group clashes

Thursday
Power BI dashboard refreshed; ACC issues created automatically

Friday
Coordination meeting using heat maps and dashboards
```

---

### Task 5: Update weekly workflow in `BIM Command Center.md`

**Files:**
- Modify: `/Users/colin/BIM Coord Auto Package/BIM Command Center.md`

**Step 1: Find the Command Center Weekly Workflow section**

Find:
```
Monday
Model health check runs automatically.
Tuesday
Clash tests run in Navisworks.
Wednesday
Clash groups generated and exported.
Thursday
ACC issues automatically created.
Friday
Power BI dashboard updated and reviewed.
```

**Step 2: Replace with canonical schedule**

```
Monday
Teams upload models; model health checks run automatically.

Tuesday
Clash tests run in Navisworks.

Wednesday
Automation scripts process clashes; clash groups generated and exported; heat map data updated.

Thursday
ACC issues created automatically from clash groups; Power BI dashboard refreshed.

Friday
Coordination meeting using Command Center dashboards and heat maps.
```

---

### Task 6: Update weekly workflow in `BIM Score implementation Plan.md`

**Files:**
- Modify: `/Users/colin/BIM Coord Auto Package/BIM Score implementation Plan.md`

**Step 1: Find the Weekly Automated Workflow section**

Find:
```
Monday
Teams run pyRevit health check
Tuesday
Results exported to ACC
Wednesday
Power BI dashboard refresh
Thursday
Coordination meeting using dashboard
Friday
Low-scoring teams fix issues
```

**Step 2: Replace with canonical schedule**

```
Monday
Teams upload models; pyRevit health check runs on each model; results exported to ACC.

Tuesday
Clash tests run in Navisworks.

Wednesday
Automation scripts process clashes; teams with health score below 85 are notified and begin fixing issues.

Thursday
ACC issues created automatically; Power BI dashboard refreshed.

Friday
Coordination meeting using Command Center dashboards. Models below 100 are flagged for cleanup before next cycle.
```

---

## PRIORITY 3 — Remove Duplicates

### Task 7: Delete `BIM Troubleshooter.md`

**Files:**
- Delete: `/Users/colin/BIM Coord Auto Package/BIM Troubleshooter.md`

**Context:** `BIM Troubleshooting Mega-Guide.md` is the canonical version with proper Markdown. The plain-text version is redundant.

**Step 1: Confirm both files have identical content**

Open both. Confirm the decision trees cover the same 5 problem categories (A–E) with the same fixes.

**Step 2: Delete**

```bash
rm "/Users/colin/BIM Coord Auto Package/BIM Troubleshooter.md"
```

**Step 3: Verify**

```bash
ls "/Users/colin/BIM Coord Auto Package/"
```

Confirm `BIM Troubleshooter.md` is gone and `BIM Troubleshooting Mega-Guide.md` remains.

---

### Task 8: Remove duplicate content from `BIM Coordination Advanced.md`

**Files:**
- Modify: `/Users/colin/BIM Coord Auto Package/BIM Coordination Advanced.md`

**Context:** The file contains the full 10-module course twice. The second copy starts around line 566 with the text `"Greetings from the BIM Pure special AI brain!"`.

**Step 1: Find the duplicate boundary**

Search for: `Greetings from the BIM Pure special AI brain!`

This line marks the start of the duplicate. Everything from this line to the end of the file is repeated content.

**Step 2: Find the true end of the first copy**

The first copy ends just before that greeting line, after:
```
Those three resources are what typically separate **average BIM teams from the top BIM teams in the US.**
```

**Step 3: Delete everything from the greeting line to end of file**

Remove all content from `Greetings from the BIM Pure special AI brain!` to end of file.

**Step 4: Verify**

Confirm the file ends with:
```
Those three resources are what typically separate **average BIM teams from the top BIM teams in the US.**
```
And that the 10-module course table appears only once.

---

## PRIORITY 4 — Bridge the Compliance Dashboard

### Task 9: Add Phase 5 preamble to `BIM compliance dashboard Requirements.md`

**Files:**
- Modify: `/Users/colin/BIM Coord Auto Package/BIM compliance dashboard Requirements.md`

**Step 1: Add preamble at the very top of the file**

Insert before any existing content:

```markdown
# BIM Portfolio Governance Exporter — Phase 5 (Advanced Tier)

> **Phase context:** This document describes the most advanced layer of the BIM Coordination Automation Package. It is intended for implementation **after** Phases 1–4 are operational (see `BIM Coordination Package - Index.md`).
>
> This system supersedes the simpler CSV export approach used in the Phase 1–4 tools. The data model defined here (append-only fact tables, DimModel, DimRun, Portfolio_ shared parameters) is the authoritative long-term standard for BIM portfolio intelligence.
>
> **Prerequisites before implementing this phase:**
> - pyRevit BIM Coordinator Toolbar deployed (Phase 2)
> - Model health scoring automated (Phase 3)
> - Clash automation and ACC issue creation operational (Phase 3–4)
> - Power BI Command Center dashboard live (Phase 4)

---
```

---

### Task 10: Add forward references to four automation files

Add a "Phase 5 Upgrade Path" note at the bottom of each of these four files.

**Files:**
- Modify: `/Users/colin/BIM Coord Auto Package/BIM automation plan.md`
- Modify: `/Users/colin/BIM Coord Auto Package/BIM Coordination Automation Toolkit.md`
- Modify: `/Users/colin/BIM Coord Auto Package/BIM Score implementation Plan.md`
- Modify: `/Users/colin/BIM Coord Auto Package/BIM Command Center.md`

**Step 1: Append to end of `BIM automation plan.md`**

```markdown

---

## Phase 5 Upgrade Path

The tools in this document represent **Phase 1–2 automation** using simple CSV exports to the Desktop or ACC folder.

When your team is ready to scale to portfolio-wide BIM governance, refer to `BIM compliance dashboard Requirements.md` for the Phase 5 system, which replaces ad-hoc CSV exports with:
- Append-only fact tables (FactModelHealth, FactCADLinks, FactSheetMeta, etc.)
- Per-run JSON audit packages
- Governance scoring and predictive velocity tracking
- DimModel and DimRun dimension tables for clean Power BI relationships
```

**Step 2: Append to end of `BIM Coordination Automation Toolkit.md`**

```markdown

---

## Phase 5 Upgrade Path

This toolkit automates clash grouping, ACC issue creation, and weekly reports using flat CSV outputs — this is the **Phase 3–4 automation** layer.

For portfolio-scale coordination intelligence, see `BIM compliance dashboard Requirements.md` (Phase 5), which introduces:
- Structured fact tables replacing ad-hoc CSVs
- Link placement tracking and coordinate drift detection
- Sheet and view governance with predictive velocity metrics
```

**Step 3: Append to end of `BIM Score implementation Plan.md`**

```markdown

---

## Phase 5 Upgrade Path

The pyRevit scoring script here exports results to a simple CSV — this is the **Phase 3 model health** layer.

`BIM compliance dashboard Requirements.md` (Phase 5) replaces this with the `FactModelHealth` append-only table, which adds:
- `RunId` and `RunDateTime` for time-series tracking
- `Portfolio_ProjectID` and `Portfolio_Discipline` for cross-project comparison
- Governance scoring and growth velocity metrics
- Cloud-model safe keying (does not rely on `doc.PathName`)
```

**Step 4: Append to end of `BIM Command Center.md`**

```markdown

---

## Phase 5 Upgrade Path

The Command Center dashboard described here uses flat CSV files from pyRevit and Navisworks exports — this is the **Phase 4** intelligence layer.

`BIM compliance dashboard Requirements.md` (Phase 5) provides a production data warehouse that feeds a more powerful version of this dashboard, with:
- Cross-project model health comparison via `DimModel`
- Coordinate signature tracking and link drift detection
- Sheet issuance velocity and delivery risk forecasting
- Full audit trail via per-run JSON packages
```

---

## PRIORITY 5 — Parameter Naming Migration Notes

### Task 11: Add migration notes to three files using old parameter names

**Files:**
- Modify: `/Users/colin/BIM Coord Auto Package/BIM Revit model setup automation.md`
- Modify: `/Users/colin/BIM Coord Auto Package/BIM Coordination Toolbar design doc.md`
- Modify: `/Users/colin/BIM Coord Auto Package/BIM Autpmatic Coordination System.md`

**Migration note text to insert after every shared parameter list in these files:**

```markdown
> **Parameter naming note:** The parameters listed above (`BIM_Status`, `Clash_Status`, `Issue_ID`, `Issue_Status`, `Coordination_Zone`, `Model_Author`) are the **Phase 1–4 standard**.
>
> In Phase 5 (see `BIM compliance dashboard Requirements.md`), these are superseded by the `Portfolio_` parameter convention (`Portfolio_ProjectID`, `Portfolio_Discipline`, `Sheet_Status`, `View_Status`, `QA_Modelled`, etc.). Plan a migration when implementing Phase 5.
```

**Step 1: In `BIM Revit model setup automation.md`**

Find the shared parameters list under "Step 1 — Build a Strong Revit Template":
```
BIM_Status
Clash_Status
Issue_ID
...
```
Insert the migration note immediately after this list.

Find the second parameter list under "Step 11 — Automatic Parameter Setup":
```
Issue_ID
Issue_Status
Clash_Status
...
```
Insert the migration note after this list too.

**Step 2: In `BIM Coordination Toolbar design doc.md`**

Find the "Load Shared Parameters" tool description listing:
```
Clash_Status
Issue_ID
Issue_Status
Coordination_Zone
Discipline
Model_Author
```
Insert the migration note after this list.

**Step 3: In `BIM Autpmatic Coordination System.md`**

Find the "Load Shared Parameters" section listing:
```
BIM_Status
Clash_Status
Issue_ID
Issue_Status
Coordination_Zone
Discipline
Model_Author
```
Insert the migration note after this list.

---

## PRIORITY 6 — Master Index File

### Task 12: Create `BIM Coordination Package - Index.md`

**Files:**
- Create: `/Users/colin/BIM Coord Auto Package/BIM Coordination Package - Index.md`

**Step 1: Write the file**

```markdown
# BIM Coordination Automation Package — Master Index

This index defines the reading order, implementation phases, and purpose of each document in this package. Start here.

---

## Implementation Phases

### Phase 1 — Standards and Templates
Establish standards before any automation. No scripting required.

| Action | Reference |
|---|---|
| Define coordination workflow and weekly schedule | `BIM Coordination 101.md` |
| Establish clash matrix and Navisworks rule templates | `BIM Coordination 101.md` |
| Build Revit project template (.RTE) with worksets, views, view templates | `BIM Revit model setup automation.md` (Steps 1–2) |
| Set up ACC folder structure and permissions | `BIM Autpmatic Coordination System.md` (Part 10) |
| Define BIM Standards Manual | `BIM Autpmatic Coordination System.md` (Part 12) |

---

### Phase 2 — pyRevit Toolbar and Project Setup Automation
Deploy the coordinator toolbar and automate new project initialization.

| Action | Reference |
|---|---|
| Build pyRevit BIM Coordinator Toolbar (40 tools) | `BIM Coordination Toolbar design doc.md` |
| Script: Initialize Project (worksets, views, sheets, links, coordinates) | `BIM Revit model setup automation.md` (Steps 3–14) |
| Train team on BIM coordination fundamentals | `BIM Coordination 101.md` |
| Train senior coordinators on advanced workflows | `BIM Coordination Advanced.md` |
| Troubleshooting reference | `BIM Troubleshooting Mega-Guide.md` |

---

### Phase 3 — Model Health Scoring and Clash Automation
Automate quality checks and clash processing.

| Action | Reference |
|---|---|
| Deploy pyRevit 150-point model health scorer | `BIM Score implementation Plan.md` |
| Scoring rubric reference | `BIM scoring system.md` |
| Script: Navisworks clash grouping (Python) | `BIM Coordination Automation Toolkit.md` (Tool 1) |
| Script: Clash prioritization engine | `BIM Coordination Automation Toolkit.md` (Tool 4) |
| Script: Model health checker (simpler version) | `BIM automation plan.md` (Section 1) |

---

### Phase 4 — ACC Issue Automation and Command Center Dashboard
Close the loop from clash to issue to dashboard.

| Action | Reference |
|---|---|
| Script: Automatic ACC issue creation | `BIM Coordination Automation Toolkit.md` (Tool 2) |
| Script: Weekly coordination report generator | `BIM Coordination Automation Toolkit.md` (Tool 3) |
| Build Power BI Command Center dashboard | `BIM Command Center.md` |
| Build clash heat map visualization | `BIM clash heat map.md` |
| Full system architecture overview | `BIM Autpmatic Coordination System.md` |

---

### Phase 5 — Portfolio Governance and Predictive Intelligence *(Advanced Tier)*
Enterprise-scale BIM governance across multiple projects.

| Action | Reference |
|---|---|
| Deploy pyRevit CPython portfolio exporter (all fact tables) | `BIM compliance dashboard Requirements.md` |
| Migrate shared parameters to `Portfolio_` convention | `BIM compliance dashboard Requirements.md` (Shared Parameters section) |
| Build governance scoring engine in Power BI | `BIM compliance dashboard Requirements.md` (Governance Engine section) |
| Build predictive velocity measures | `BIM compliance dashboard Requirements.md` (Predictive Engine section) |

> **Note:** Phase 5 supersedes the simple CSV exports from Phases 3–4 and introduces the `Portfolio_` shared parameter convention. See the migration note in each earlier file.

---

## Canonical Standards (Quick Reference)

### Weekly Workflow

| Day | Activity |
|---|---|
| Monday | Model uploads (all disciplines) |
| Tuesday | Clash tests run in Navisworks |
| Wednesday | Automation scripts process clashes; clash groups generated; heat map updated |
| Thursday | ACC issues created automatically; Power BI dashboard refreshed |
| Friday | Coordination meeting using dashboards and heat maps |

### Model Health Score Thresholds (150-point scale)

| Score | Status | Action |
|---|---|---|
| 130–150 | Elite | No action needed |
| 115–129 | Excellent | Monitor |
| 100–114 | Healthy | Minimum for coordination entry |
| 85–99 | Needs Cleanup | Flag; notify team to remediate |
| Below 85 | Critical | Reject from coordination |

### Warning Count Target
`< 300` — ideal. `300–1,000` — acceptable. `> 1,000` — flag for cleanup.

### Clash Tolerance Standards

| Test Type | Tolerance |
|---|---|
| Hard clash (structural vs MEP) | 0 inches |
| MEP internal clearance | 1–2 inches |
| Equipment maintenance clearance | 24–36 inches |

### Model File Size Target
`< 300 MB` — ideal. `< 500 MB` — acceptable. `> 500 MB` — flag for cleanup.

---

## File Map

| File | Type | Phase |
|---|---|---|
| `BIM Coordination Package - Index.md` | Master index | All |
| `BIM Coordination 101.md` | Training | 1–2 |
| `BIM Coordination Advanced.md` | Training | 2 |
| `BIM Troubleshooting Mega-Guide.md` | Reference | 2+ |
| `BIM Autpmatic Coordination System.md` | System overview | 1–4 |
| `BIM Revit model setup automation.md` | Implementation | 2 |
| `BIM Coordination Toolbar design doc.md` | Implementation | 2 |
| `BIM scoring system.md` | Standard/rubric | 3 |
| `BIM Score implementation Plan.md` | Implementation | 3 |
| `BIM automation plan.md` | Implementation | 3 |
| `BIM Coordination Automation Toolkit.md` | Implementation | 3–4 |
| `BIM clash heat map.md` | Implementation | 4 |
| `BIM Command Center.md` | Implementation | 4 |
| `BIM compliance dashboard Requirements.md` | Implementation | 5 |
```

**Step 2: Verify the file was created**

```bash
ls "/Users/colin/BIM Coord Auto Package/"
```

Confirm `BIM Coordination Package - Index.md` appears.

---

## Final Verification Checklist

After all tasks are complete, verify:

- [ ] `BIM Score implementation Plan.md` script categories sum to 150
- [ ] `BIM Score implementation Plan.md` status labels match `BIM scoring system.md`
- [ ] `BIM Command Center.md` no longer references a score of 75 as threshold
- [ ] All 4 files with weekly workflows use Mon=uploads, Fri=meeting
- [ ] `BIM Troubleshooter.md` is deleted
- [ ] `BIM Coordination Advanced.md` course content appears exactly once
- [ ] `BIM compliance dashboard Requirements.md` has Phase 5 preamble at top
- [ ] 4 automation files have Phase 5 Upgrade Path section at bottom
- [ ] 3 files with old param names have migration notes after each parameter list
- [ ] `BIM Coordination Package - Index.md` exists and references all 14 remaining files
