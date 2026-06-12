# README & Tool Documentation Design

**Date:** 2026-03-08
**Audience:** BIM coordinators and Revit users (non-developer)
**Scope:** Root README + 7 panel/pipeline docs in docs/tools/

---

## Structure

### Root README.md
- Project overview and what it does
- Prerequisites (Revit version, pyRevit, Python 3.8+, pandas/reportlab)
- Installation: manual copy + git clone options
- Folder structure overview
- Weekly workflow (Mon–Fri cadence)
- Links to all panel and pipeline docs

### docs/tools/ (7 files)
| File | Covers |
|---|---|
| 01-project-setup.md | 6 Project_Setup panel buttons |
| 02-model-health.md | 6 Model_Health panel buttons |
| 03-coordination.md | 6 Coordination panel buttons |
| 04-reporting.md | 2 Reporting panel buttons + output files |
| 05-utilities.md | ExportGrids + SyncAndClose |
| 06-pipeline.md | Python automation pipeline, input/output, scheduling |
| 07-power-bi.md | Power BI quick summary + link to command-center-setup.md |

---

## Per-Panel Doc Format
Each doc follows the same structure:
1. Panel overview (1–2 sentences)
2. Prerequisites (if any)
3. Per-tool sections: Purpose | When to use | How to use | Output/result
4. Common issues / tips

---

## README Tone
- Plain English, no jargon beyond standard BIM terms
- Numbered steps for installation
- Table for weekly workflow
- Badges: Python version, pyRevit required, Revit version
