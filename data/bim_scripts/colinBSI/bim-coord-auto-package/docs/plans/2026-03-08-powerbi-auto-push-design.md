# Power BI Auto-Push Design

**Date:** 2026-03-08
**Status:** Approved

## Problem

The pipeline writes 4 CSVs to `data/output/` every Wednesday. Power BI Desktop has no
built-in scheduler — a user must manually click Refresh. The goal is for Power BI to
refresh automatically the next time the coordinator opens the `.pbix` file, with a
visible indicator that confirms the data is current.

## Scope

- Power BI Desktop (local `.pbix`), not Power BI Service
- `.pbix` does not yet exist; it will be built following the existing setup guide
- No UI automation or brittle scripting

## Out of Scope

- Power BI Service / cloud publishing
- Real-time streaming datasets
- Automatic pipeline-triggered refresh (requires open Power BI Desktop instance)

## Solution: Option B — Guide + Pipeline Metadata

### 1. Pipeline — Stage 5: Metadata Writer

**New file:** `BIM_Automation/pipeline_metadata/metadata_writer.py`

Appends one row per pipeline run to `data/output/pipeline_metadata.csv`.

**Schema:**

| Column | Type | Example |
|---|---|---|
| `RunDate` | Date | 2026-03-11 |
| `RunTimestamp` | Datetime | 2026-03-11 06:04:23 |
| `StagesCompleted` | Integer | 5 |
| `ClashesProcessed` | Integer | 142 |
| `InputFilesFound` | Integer | 3 |
| `PipelineStatus` | Text | Success |

Rows are appended (not overwritten) to preserve run history for trend display.

**Behaviour:**
- Non-blocking: Stage 5 failure logs a warning but does not fail the pipeline
- Creates the CSV with headers on first run if it does not exist
- `StagesCompleted` counts only stages that returned without exception

**`main.py` change:** Add Stage 5 call after Stage 4, wrapped in try/except.

### 2. Power BI Guide — New Sections

**`docs/powerbi/command-center-setup.md` additions:**

**Step 0 — Auto-Refresh Setup** (inserted before existing Step 1)
- Enable "Refresh data when opening the file":
  Options → Data Load → check "Refresh data in the background when opening reports"
- Set query timeout: Options → Data Load → Background data → 30 seconds
- Explanation: this causes Power BI Desktop to refresh all connected CSVs silently
  on file open, so the coordinator always sees current data without clicking Refresh

**Step 5 — Pipeline Status Card** (appended after existing Step 4)
- Load `pipeline_metadata.csv` as a 5th Power Query table named `PipelineStatus`
- Set `RunDate` → Date, `RunTimestamp` → Datetime, `StagesCompleted` → Whole Number
- DAX measure: `Last Pipeline Run = FORMAT(LASTDATE(PipelineStatus[RunTimestamp]), "ddd DD-MMM hh:MM AM/PM")`
- DAX measure: `Pipeline OK = IF(LASTNONBLANK(PipelineStatus[PipelineStatus], 1) = "Success", "OK", "CHECK PIPELINE")`
- Add to each of the 4 dashboards: two Card visuals in a shared top-right corner
  - Card 1: `Last Pipeline Run` — label "Data as of"
  - Card 2: `Pipeline OK` — conditional formatting: green (#107C10) = OK, red (#D13438) = CHECK PIPELINE

## File Changes

| File | Change |
|---|---|
| `BIM_Automation/pipeline_metadata/__init__.py` | New (empty) |
| `BIM_Automation/pipeline_metadata/metadata_writer.py` | New module |
| `BIM_Automation/main.py` | Add Stage 5 call |
| `docs/powerbi/command-center-setup.md` | Add Step 0 and Step 5 |
