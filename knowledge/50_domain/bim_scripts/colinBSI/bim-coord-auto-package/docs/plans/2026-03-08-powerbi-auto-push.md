# Power BI Auto-Push Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a Stage 5 metadata writer to the pipeline and extend the Power BI setup guide with auto-refresh-on-open configuration and a Pipeline Status Card.

**Architecture:** A new `pipeline_metadata/metadata_writer.py` module appends one row per run to `pipeline_metadata.csv`. `main.py` calls it as a non-blocking Stage 5. The Power BI guide gains Step 0 (auto-refresh setting) and Step 7 (Pipeline Status Card), with Step 7 (Refresh Schedule) renumbered to Step 8.

**Tech Stack:** Python 3, pandas, pathlib. Power BI Desktop (no Service required). No new pip dependencies.

---

### Task 1: Create `pipeline_metadata/` package

**Files:**
- Create: `BIM_Automation/pipeline_metadata/__init__.py`
- Create: `BIM_Automation/pipeline_metadata/metadata_writer.py`

**Step 1: Create the empty `__init__.py`**

File: `BIM_Automation/pipeline_metadata/__init__.py`
Contents: empty file (zero bytes).

**Step 2: Create `metadata_writer.py`**

File: `BIM_Automation/pipeline_metadata/metadata_writer.py`

```python
"""
metadata_writer.py — Stage 5: Pipeline Metadata Writer

Appends one row per pipeline run to pipeline_metadata.csv in the output directory.
Rows accumulate over time so Power BI can show run history and a "last updated" card.

Called by main.py as a non-blocking Stage 5.
"""

import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)

METADATA_FILE = "pipeline_metadata.csv"

COLUMNS = [
    "RunDate",
    "RunTimestamp",
    "StagesCompleted",
    "ClashesProcessed",
    "InputFilesFound",
    "PipelineStatus",
]


def run(
    output_dir: Path,
    stages_completed: int,
    clashes_processed: int,
    input_files_found: int,
    status: str,
) -> None:
    """Append a metadata row for this pipeline run."""
    now = datetime.now()
    row = {
        "RunDate": now.strftime("%Y-%m-%d"),
        "RunTimestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "StagesCompleted": stages_completed,
        "ClashesProcessed": clashes_processed,
        "InputFilesFound": input_files_found,
        "PipelineStatus": status,
    }

    dest = output_dir / METADATA_FILE

    if dest.exists():
        existing = pd.read_csv(dest)
        updated = pd.concat([existing, pd.DataFrame([row])], ignore_index=True)
    else:
        updated = pd.DataFrame([row], columns=COLUMNS)

    updated.to_csv(dest, index=False)
    log.info("Stage 5 complete: metadata appended to %s (%d rows total)", METADATA_FILE, len(updated))
```

**Step 3: Verify by reading both files back**

Confirm `__init__.py` is empty and `metadata_writer.py` matches the above exactly.

---

### Task 2: Wire Stage 5 into `main.py`

**Files:**
- Modify: `BIM_Automation/main.py`

**Step 1: Add the import**

After the existing import block (line 38, after `from acc_integration import issue_stub`), add:

```python
from pipeline_metadata import metadata_writer
```

**Step 2: Add stage tracking variables**

In `run_pipeline()`, add these three variables immediately after the `OUTPUT_DIR.mkdir` call (after line 102):

```python
    stages_completed = 0
    clashes_processed = 0
    input_files_found = len(list(INPUT_DIR.glob("*.csv")))
```

**Step 3: Increment `stages_completed` after each successful stage**

After the Stage 0 success log (line 108, after `logger.info("Stage 0 complete: ...")`), add:
```python
        stages_completed += 1
```

After the Stage 1 success log (line 122, after `logger.info("Stage 1 complete: ...")`), add:
```python
    stages_completed += 1
    clashes_processed = len(detail_df)
```

After the Stage 2 success log (line 127), add:
```python
        stages_completed += 1
```

After the Stage 3 success log (line 131), add:
```python
        stages_completed += 1
```

After the Stage 4 success log (line 135), add:
```python
        stages_completed += 1
```

**Step 4: Add Stage 5 call after the try/except block**

The existing try/except for stages 2–4 ends at line 141 (the `finally` archive block).
After the `archive_inputs` call (after line 141), add Stage 5 as a non-blocking call:

```python
    # Stage 5: Pipeline Metadata (non-blocking)
    try:
        metadata_writer.run(
            output_dir=OUTPUT_DIR,
            stages_completed=stages_completed,
            clashes_processed=clashes_processed,
            input_files_found=input_files_found,
            status="Success",
        )
    except Exception:
        logger.exception("Stage 5 failed — metadata not written, pipeline still complete")
```

Also add a "Failed" status call in the except block for stages 2–4. Replace the existing `except Exception:` block:

```python
    except Exception:
        logger.exception("Pipeline failed — see traceback above. Input CSVs left in place for retry.")
        try:
            metadata_writer.run(
                output_dir=OUTPUT_DIR,
                stages_completed=stages_completed,
                clashes_processed=clashes_processed,
                input_files_found=input_files_found,
                status="Failed",
            )
        except Exception:
            logger.exception("Stage 5 also failed — metadata not written")
        return
```

**Step 5: Update the docstring**

At the top of `main.py`, update the pipeline stage list in the docstring to add:
```
    5. Pipeline Metadata  (pipeline_metadata/metadata_writer.py) ← always runs
```

**Step 6: Verify by reading `main.py` back**

Confirm imports, stage tracking variables, increments, and Stage 5 call are all present and correct.

---

### Task 3: Extend the Power BI guide — Step 0 (Auto-Refresh)

**Files:**
- Modify: `docs/powerbi/command-center-setup.md`

**Step 1: Insert Step 0 before the existing Step 1**

Find the line `## Step 1 — Connect to Data Folder` and insert this block immediately before it:

```markdown
## Step 0 — Auto-Refresh Setup

Do this once when you first open the `.pbix` file. It makes Power BI refresh all
connected CSVs automatically every time you open the file — no manual Refresh click needed.

1. **Options → Data Load:**
   Power BI Desktop → **File → Options and settings → Options → Data Load**
   - Check: **"Refresh data in the background when opening reports"**
   - Set query timeout: under **Background data**, set to **30 seconds**
2. Click **OK**.

> **Result:** Every time you open the `.pbix` on Wednesday morning after the pipeline
> has run, the data automatically reflects the latest CSVs from `C:\BIM_Automation\data\output\`.

---

```

**Step 2: Verify by reading the file back**

Confirm Step 0 appears before Step 1 and the rest of the document is unchanged.

---

### Task 4: Extend the Power BI guide — Pipeline Status Card

**Files:**
- Modify: `docs/powerbi/command-center-setup.md`

**Step 1: Rename existing Step 7 to Step 8**

Find `## Step 7 — Refresh Schedule` and replace it with `## Step 8 — Refresh Schedule`.

**Step 2: Insert the new Step 7 before Step 8**

Find `## Step 8 — Refresh Schedule` (after the rename) and insert this block immediately before it:

```markdown
## Step 7 — Pipeline Status Card

Add two status cards to each of the 4 dashboard pages so you always know when the
data was last updated and whether the pipeline succeeded.

### Load the metadata table

In **Power Query (Transform Data)**, load `pipeline_metadata.csv` from the output folder.
Rename the query: `PipelineStatus`.

**Data types to set:**
- `PipelineStatus[RunDate]` → Date
- `PipelineStatus[RunTimestamp]` → Datetime (use locale: en-US, format: yyyy-MM-dd HH:mm:ss)
- `PipelineStatus[StagesCompleted]` → Whole Number
- `PipelineStatus[ClashesProcessed]` → Whole Number
- `PipelineStatus[InputFilesFound]` → Whole Number

Click **Close & Apply**.

### DAX measures

Add these two measures to the `_Measures` table:

```dax
Last Pipeline Run =
"Data as of: " &
FORMAT(
    CALCULATE(MAX(PipelineStatus[RunTimestamp]), LASTDATE(PipelineStatus[RunDate])),
    "ddd DD-MMM h:MM AM/PM"
)

Pipeline OK =
IF(
    CALCULATE(
        LASTNONBLANK(PipelineStatus[PipelineStatus], 1),
        LASTDATE(PipelineStatus[RunDate])
    ) = "Success",
    "Pipeline OK",
    "CHECK PIPELINE"
)
```

### Add cards to each dashboard page

Repeat for each of the 4 pages (Project Health, Clash Heat Map, Coordination Performance, Model Health Trends):

1. Add a **Card** visual to the top-right corner.
   - Field: `[Last Pipeline Run]` measure
   - Format → Callout value → Font size: 11

2. Add a second **Card** visual below the first.
   - Field: `[Pipeline OK]` measure
   - Format → Callout value → **Conditional formatting → Font color**:
     - Rule: If value = "Pipeline OK" → `#107C10` (green)
     - Rule: If value = "CHECK PIPELINE" → `#D13438` (red)

> **Tip:** Build it on the first page, then copy both cards (Ctrl+C) and paste them
> onto each remaining page (Ctrl+V) — they retain their field bindings.

---

```

**Step 3: Update the Weekly Workflow table**

Find this row in the Weekly Workflow table:
```
| Wednesday AM | Open Power BI Desktop → Refresh |
```

Replace it with:
```
| Wednesday AM | Open Power BI Desktop — auto-refreshes on open (Step 0) |
```

**Step 4: Verify by reading the full guide back**

Confirm: Step 0 present, Steps 1–6 unchanged, Step 7 (Pipeline Status Card) present, Step 8 (Refresh Schedule) present, Weekly Workflow table updated.

---
