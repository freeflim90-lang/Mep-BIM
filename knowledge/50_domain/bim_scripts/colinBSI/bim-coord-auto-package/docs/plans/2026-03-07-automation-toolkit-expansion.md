# BIM Automation Toolkit Expansion — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Expand the 4 stub scripts in `BIM Coordination Automation Toolkit.md` into production-ready Python modules documented in the package, plus update the toolkit doc to reference them.

**Architecture:** Modular scripts with a master runner. Each tool is its own `.py` file under `BIM_Automation/`. A `main.py` runner chains them in sequence. CSV-based input now; ACC API stubs marked for Phase 2.

**Tech Stack:** Python 3.x, `pandas`, `openpyxl`, `reportlab`, `logging`, `pathlib`, `csv`, `shutil`

---

## Context

- This is a **documentation-only package** — no git, no test runner.
- Verification = read files back after writing.
- Scripts are written as deployable examples that coordinators copy to their server.
- All files go under a new `BIM_Automation/` folder at the project root.
- After all scripts are written, update `BIM Coordination Automation Toolkit.md` to reference them.

---

### Task 1: Create folder structure

**Files:**
- Create: `BIM_Automation/clash_processing/` (directory marker file)
- Create: `BIM_Automation/reports/` (directory marker file)
- Create: `BIM_Automation/acc_integration/` (directory marker file)
- Create: `BIM_Automation/logs/` (directory marker file)
- Create: `BIM_Automation/data/input/` (directory marker file)
- Create: `BIM_Automation/data/output/` (directory marker file)
- Create: `BIM_Automation/data/archive/` (directory marker file)

**Step 1: Create a README in each subfolder**

Create `BIM_Automation/clash_processing/README.md`:
```
Clash grouping and prioritization modules.
```

Create `BIM_Automation/reports/README.md`:
```
Weekly report generator — outputs CSV, Excel, and PDF.
```

Create `BIM_Automation/acc_integration/README.md`:
```
ACC issue integration stub. Phase 2: replace with live Autodesk API calls.
```

Create `BIM_Automation/data/README.md`:
```
input/   — drop Navisworks CSV exports here before each run
output/  — pipeline writes reports here
archive/ — processed input CSVs are moved here after each run
```

**Step 2: Verify**

Read each README back to confirm it was written correctly.

---

### Task 2: Write `config.py`

**Files:**
- Create: `BIM_Automation/config.py`

**Step 1: Write the file**

```python
"""
config.py — Central configuration for BIM Automation Pipeline
Edit paths and thresholds here. Do not modify other modules for configuration.
"""

from pathlib import Path

# --- Directory paths ---
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
ARCHIVE_DIR = DATA_DIR / "archive"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"

# --- Clash priority rules ---
# Discipline pairs containing these strings are elevated to Critical or High.
CRITICAL_DISCIPLINES = {"Structure", "Structural"}
HIGH_DISCIPLINES = {"Mechanical", "Plumbing"}

# --- Report settings ---
REPORT_BASENAME = "weekly_coordination_report"  # extensions added automatically
PDF_TITLE = "BIM Weekly Coordination Summary"
EXCEL_SHEET_SUMMARY = "Summary"
EXCEL_SHEET_DISCIPLINE = "Discipline Breakdown"
EXCEL_SHEET_HIGHRISK = "High Risk Areas"
HIGH_RISK_THRESHOLD = 20  # groups with >= this many clashes appear in High Risk tab

# --- Logging ---
LOG_MAX_BYTES = 5 * 1024 * 1024   # 5 MB per log file
LOG_BACKUP_COUNT = 6               # ~30 days at weekly runs

# --- Phase 2 placeholders (not yet active) ---
# ACC_CLIENT_ID = ""
# ACC_CLIENT_SECRET = ""
# ACC_PROJECT_ID = ""
# ACC_ISSUE_ENDPOINT = "https://developer.api.autodesk.com/issues/v1/issues"
```

**Step 2: Verify**

Read `BIM_Automation/config.py` back.

---

### Task 3: Write `clash_processing/clash_grouper.py`

**Files:**
- Create: `BIM_Automation/clash_processing/clash_grouper.py`

**Step 1: Write the file**

```python
"""
clash_grouper.py — Tool 1: Automatic Clash Grouping

Reads all CSV files from the input directory.
Groups clashes by Level + DisciplineA + DisciplineB.
Adds a GroupKey column to each row.
Returns a single consolidated DataFrame.

Expected input columns:
    ClashID, Level, Grid, DisciplineA, DisciplineB,
    ClashType, Description, Distance
"""

import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)


def load_clash_csvs(input_dir: Path) -> pd.DataFrame:
    """
    Load all CSV files from input_dir into a single DataFrame.
    Skips files that are missing required columns and logs a warning.
    Returns an empty DataFrame if no valid files are found.
    """
    required_columns = {
        "ClashID", "Level", "Grid",
        "DisciplineA", "DisciplineB",
        "ClashType", "Description", "Distance"
    }

    frames = []
    csv_files = list(input_dir.glob("*.csv"))

    if not csv_files:
        logger.warning("load_clash_csvs: no CSV files found in %s", input_dir)
        return pd.DataFrame()

    for path in csv_files:
        try:
            df = pd.read_csv(path)
            missing = required_columns - set(df.columns)
            if missing:
                logger.warning(
                    "Skipping %s — missing columns: %s", path.name, missing
                )
                continue
            df["_source_file"] = path.name
            frames.append(df)
            logger.info("Loaded %d rows from %s", len(df), path.name)
        except Exception as exc:
            logger.warning("Skipping %s — read error: %s", path.name, exc)

    if not frames:
        logger.warning("load_clash_csvs: no valid CSV files loaded.")
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    logger.info("load_clash_csvs: total %d clashes loaded from %d file(s)",
                len(combined), len(frames))
    return combined


def add_group_key(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a GroupKey column: Level_DisciplineA_vs_DisciplineB
    e.g. 'Level3_Mechanical_vs_Structure'

    Normalizes level names by removing spaces.
    """
    if df.empty:
        return df

    df = df.copy()
    level = df["Level"].str.replace(" ", "", regex=False)
    disc_a = df["DisciplineA"].str.strip()
    disc_b = df["DisciplineB"].str.strip()
    df["GroupKey"] = level + "_" + disc_a + "_vs_" + disc_b
    return df


def summarize_groups(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a summary DataFrame: one row per GroupKey with clash count.
    Sorted descending by count.
    """
    if df.empty:
        return pd.DataFrame(columns=["GroupKey", "ClashCount"])

    summary = (
        df.groupby("GroupKey")
        .size()
        .reset_index(name="ClashCount")
        .sort_values("ClashCount", ascending=False)
        .reset_index(drop=True)
    )
    logger.info("summarize_groups: %d unique groups identified", len(summary))
    return summary


def run(input_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Main entry point for clash grouping.

    Returns:
        detail_df  — full clash list with GroupKey column
        summary_df — one row per group with ClashCount
    """
    logger.info("clash_grouper: starting")
    detail_df = load_clash_csvs(input_dir)
    if detail_df.empty:
        logger.warning("clash_grouper: no data to process, exiting early")
        return detail_df, pd.DataFrame()

    detail_df = add_group_key(detail_df)
    summary_df = summarize_groups(detail_df)
    logger.info(
        "clash_grouper: complete — %d clashes in %d groups",
        len(detail_df), len(summary_df)
    )
    return detail_df, summary_df
```

**Step 2: Verify**

Read `BIM_Automation/clash_processing/clash_grouper.py` back.

---

### Task 4: Write `clash_processing/clash_prioritizer.py`

**Files:**
- Create: `BIM_Automation/clash_processing/clash_prioritizer.py`

**Step 1: Write the file**

```python
"""
clash_prioritizer.py — Tool 4: Clash Prioritization Engine

Takes the enriched clash DataFrame (with GroupKey) from clash_grouper.
Adds a Priority column to each row: Critical, High, Medium, or Low.

Priority logic (based on construction risk):
    Critical — either discipline is structural
    High     — either discipline is mechanical or plumbing
    Medium   — all other combinations
    Low      — cosmetic clashes (Lighting vs Ceiling, etc.)

Low-priority overrides: defined in LOW_PRIORITY_PAIRS below.
"""

import logging
import pandas as pd

from config import CRITICAL_DISCIPLINES, HIGH_DISCIPLINES

logger = logging.getLogger(__name__)

# Frozensets so order doesn't matter: {"Lighting", "Ceiling"} matches either direction
LOW_PRIORITY_PAIRS = [
    frozenset({"Lighting", "Ceiling"}),
    frozenset({"Lighting", "Furniture"}),
    frozenset({"Ceiling", "Furniture"}),
]


def classify_priority(discipline_a: str, discipline_b: str) -> str:
    """
    Return the priority string for a clash between two disciplines.
    """
    pair = frozenset({discipline_a.strip(), discipline_b.strip()})

    if pair in LOW_PRIORITY_PAIRS:
        return "Low"
    if CRITICAL_DISCIPLINES & pair:
        return "Critical"
    if HIGH_DISCIPLINES & pair:
        return "High"
    return "Medium"


def add_priority(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a Priority column to the clash DataFrame.
    Operates row-by-row using classify_priority().
    Returns the modified DataFrame.
    """
    if df.empty:
        logger.warning("add_priority: received empty DataFrame, skipping")
        return df

    df = df.copy()
    df["Priority"] = df.apply(
        lambda row: classify_priority(row["DisciplineA"], row["DisciplineB"]),
        axis=1
    )

    counts = df["Priority"].value_counts().to_dict()
    logger.info("add_priority: priority distribution — %s", counts)
    return df


def run(detail_df: pd.DataFrame) -> pd.DataFrame:
    """
    Main entry point for clash prioritization.

    Args:
        detail_df — enriched clash DataFrame from clash_grouper.run()

    Returns:
        detail_df with Priority column added
    """
    logger.info("clash_prioritizer: starting")
    result = add_priority(detail_df)
    logger.info("clash_prioritizer: complete — %d clashes prioritized", len(result))
    return result
```

**Step 2: Verify**

Read `BIM_Automation/clash_processing/clash_prioritizer.py` back.

---

### Task 5: Write `reports/report_generator.py`

**Files:**
- Create: `BIM_Automation/reports/report_generator.py`

**Step 1: Write the file**

```python
"""
report_generator.py — Tool 3: Weekly Coordination Report Generator

Produces three output files from the enriched, prioritized clash DataFrame:
    1. weekly_coordination_report.csv   — full enriched clash list
    2. weekly_coordination_report.xlsx  — 3 tabs: Summary, Discipline Breakdown, High Risk Areas
    3. weekly_coordination_report.pdf   — 1-page summary for Friday coordination meeting

Dependencies:
    pip install pandas openpyxl reportlab
"""

import logging
from datetime import date
from pathlib import Path

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors

from config import (
    REPORT_BASENAME,
    PDF_TITLE,
    EXCEL_SHEET_SUMMARY,
    EXCEL_SHEET_DISCIPLINE,
    EXCEL_SHEET_HIGHRISK,
    HIGH_RISK_THRESHOLD,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# CSV output
# ---------------------------------------------------------------------------

def write_csv(detail_df: pd.DataFrame, output_dir: Path) -> Path:
    """Write full enriched clash list to CSV."""
    path = output_dir / f"{REPORT_BASENAME}.csv"
    detail_df.to_csv(path, index=False)
    logger.info("write_csv: wrote %d rows to %s", len(detail_df), path.name)
    return path


# ---------------------------------------------------------------------------
# Excel output
# ---------------------------------------------------------------------------

def _build_summary_df(detail_df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "Metric": [
            "Total Clashes",
            "Critical",
            "High",
            "Medium",
            "Low",
            "Unique Groups",
        ],
        "Value": [
            len(detail_df),
            (detail_df["Priority"] == "Critical").sum(),
            (detail_df["Priority"] == "High").sum(),
            (detail_df["Priority"] == "Medium").sum(),
            (detail_df["Priority"] == "Low").sum(),
            detail_df["GroupKey"].nunique(),
        ],
    })


def _build_discipline_df(detail_df: pd.DataFrame) -> pd.DataFrame:
    return (
        detail_df
        .groupby(["DisciplineA", "DisciplineB"])
        .agg(ClashCount=("ClashID", "count"))
        .reset_index()
        .sort_values("ClashCount", ascending=False)
        .reset_index(drop=True)
    )


def _build_highrisk_df(detail_df: pd.DataFrame, threshold: int) -> pd.DataFrame:
    group_counts = detail_df.groupby("GroupKey").size().reset_index(name="ClashCount")
    high_risk = group_counts[group_counts["ClashCount"] >= threshold].copy()
    return high_risk.sort_values("ClashCount", ascending=False).reset_index(drop=True)


def write_excel(detail_df: pd.DataFrame, output_dir: Path) -> Path:
    """Write 3-tab Excel report."""
    path = output_dir / f"{REPORT_BASENAME}.xlsx"

    summary_df = _build_summary_df(detail_df)
    discipline_df = _build_discipline_df(detail_df)
    highrisk_df = _build_highrisk_df(detail_df, HIGH_RISK_THRESHOLD)

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name=EXCEL_SHEET_SUMMARY, index=False)
        discipline_df.to_excel(writer, sheet_name=EXCEL_SHEET_DISCIPLINE, index=False)
        highrisk_df.to_excel(writer, sheet_name=EXCEL_SHEET_HIGHRISK, index=False)

    logger.info("write_excel: wrote 3-tab report to %s", path.name)
    return path


# ---------------------------------------------------------------------------
# PDF output
# ---------------------------------------------------------------------------

def write_pdf(detail_df: pd.DataFrame, output_dir: Path) -> Path:
    """Write 1-page PDF summary for the Friday coordination meeting."""
    path = output_dir / f"{REPORT_BASENAME}.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=letter,
                            topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(PDF_TITLE, styles["Title"]))
    story.append(Paragraph(f"Generated: {date.today().strftime('%B %d, %Y')}", styles["Normal"]))
    story.append(Spacer(1, 0.2 * inch))

    # Summary table
    story.append(Paragraph("Project Summary", styles["Heading2"]))
    summary_df = _build_summary_df(detail_df)
    summary_data = [summary_df.columns.tolist()] + summary_df.values.tolist()
    summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F5496")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F8")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.2 * inch))

    # Discipline breakdown (top 10)
    story.append(Paragraph("Discipline Clash Breakdown (Top 10)", styles["Heading2"]))
    disc_df = _build_discipline_df(detail_df).head(10)
    disc_data = [disc_df.columns.tolist()] + disc_df.values.tolist()
    disc_table = Table(disc_data, colWidths=[2.5 * inch, 2.5 * inch, 1.5 * inch])
    disc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F5496")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F8")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(disc_table)
    story.append(Spacer(1, 0.2 * inch))

    # High risk areas
    highrisk_df = _build_highrisk_df(detail_df, HIGH_RISK_THRESHOLD)
    if not highrisk_df.empty:
        story.append(Paragraph(
            f"High Risk Areas (≥{HIGH_RISK_THRESHOLD} clashes)", styles["Heading2"]
        ))
        hr_data = [highrisk_df.columns.tolist()] + highrisk_df.values.tolist()
        hr_table = Table(hr_data, colWidths=[4 * inch, 2 * inch])
        hr_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C00000")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FFF0F0")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(hr_table)

    doc.build(story)
    logger.info("write_pdf: wrote PDF summary to %s", path.name)
    return path


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run(detail_df: pd.DataFrame, output_dir: Path) -> dict[str, Path]:
    """
    Generate all three report formats.

    Args:
        detail_df  — enriched, prioritized clash DataFrame
        output_dir — directory to write outputs

    Returns:
        dict with keys 'csv', 'excel', 'pdf' mapping to output Paths
    """
    logger.info("report_generator: starting")
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "csv": write_csv(detail_df, output_dir),
        "excel": write_excel(detail_df, output_dir),
        "pdf": write_pdf(detail_df, output_dir),
    }

    logger.info("report_generator: complete — 3 files written to %s", output_dir)
    return outputs
```

**Step 2: Verify**

Read `BIM_Automation/reports/report_generator.py` back.

---

### Task 6: Write `acc_integration/issue_stub.py`

**Files:**
- Create: `BIM_Automation/acc_integration/issue_stub.py`

**Step 1: Write the file**

```python
"""
issue_stub.py — Tool 2: ACC Issue Creation (Phase 2 Stub)

This module is a placeholder for the Autodesk Construction Cloud (ACC)
issue creation integration. In Phase 2, this module will:
    1. Authenticate with ACC using OAuth 2.0 (Client Credentials flow)
    2. Iterate over Critical and High priority clashes
    3. Create a coordination issue in ACC for each clash
    4. Assign the issue to the responsible trade
    5. Set a due date (7 days from creation)

Current behavior:
    - Logs what would be created without making any API calls
    - Returns a list of simulated issue dicts for pipeline visibility

Phase 2 implementation checklist:
    TODO (Phase 2): Set ACC_CLIENT_ID and ACC_CLIENT_SECRET in config.py
    TODO (Phase 2): Set ACC_PROJECT_ID in config.py
    TODO (Phase 2): Implement _get_access_token() using requests + OAuth
    TODO (Phase 2): Implement _create_issue() using ACC Issues API v1
    TODO (Phase 2): Add retry logic for API rate limits (429 responses)
    TODO (Phase 2): Add email alert on authentication failure
    TODO (Phase 2): Replace simulated_issues return with live API responses

ACC API reference:
    https://aps.autodesk.com/en/docs/acc/v1/reference/http/issues-v1-issues-POST/
"""

import logging
from datetime import date, timedelta
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

ISSUE_DISCIPLINES = {"Critical", "High"}
DEFAULT_DUE_DAYS = 7


def _discipline_to_trade(discipline_a: str, discipline_b: str) -> str:
    """
    Map a discipline pair to the responsible trade for assignment.
    In Phase 2, this will resolve against ACC project members.
    """
    # TODO (Phase 2): resolve against ACC project member list
    priority_discipline = discipline_a if discipline_a != "Structure" else discipline_b
    return f"{priority_discipline} Contractor"


def run(detail_df: pd.DataFrame) -> list[dict[str, Any]]:
    """
    Simulate ACC issue creation for Critical and High priority clashes.

    Args:
        detail_df — enriched, prioritized clash DataFrame

    Returns:
        List of simulated issue dicts (what would be sent to ACC API)
    """
    logger.info("issue_stub: starting (Phase 2 stub — no API calls made)")

    if detail_df.empty:
        logger.warning("issue_stub: empty DataFrame, no issues to create")
        return []

    actionable = detail_df[detail_df["Priority"].isin(ISSUE_DISCIPLINES)].copy()
    logger.info(
        "issue_stub: %d clashes qualify for issue creation (%s)",
        len(actionable), ", ".join(ISSUE_DISCIPLINES)
    )

    due_date = (date.today() + timedelta(days=DEFAULT_DUE_DAYS)).isoformat()
    simulated_issues = []

    for _, row in actionable.iterrows():
        trade = _discipline_to_trade(row["DisciplineA"], row["DisciplineB"])
        issue = {
            "title": f"{row['DisciplineA']} vs {row['DisciplineB']} Clash — {row['Level']} Grid {row['Grid']}",
            "description": row["Description"],
            "status": "open",
            "priority": row["Priority"].lower(),
            "assignedTo": trade,
            "dueDate": due_date,
            "clashId": row["ClashID"],
            "groupKey": row["GroupKey"],
        }
        simulated_issues.append(issue)
        logger.info(
            "issue_stub: [SIMULATED] would create issue — %s | %s | due %s",
            issue["title"], trade, due_date
        )

    logger.info(
        "issue_stub: complete — %d issues simulated (Phase 2: replace with live API calls)",
        len(simulated_issues)
    )
    return simulated_issues
```

**Step 2: Verify**

Read `BIM_Automation/acc_integration/issue_stub.py` back.

---

### Task 7: Write `main.py`

**Files:**
- Create: `BIM_Automation/main.py`

**Step 1: Write the file**

```python
"""
main.py — BIM Automation Pipeline Master Runner

Runs the full coordination pipeline in sequence:
    1. Clash Grouping      (clash_processing/clash_grouper.py)
    2. Clash Prioritization (clash_processing/clash_prioritizer.py)
    3. Report Generation   (reports/report_generator.py)
    4. ACC Issue Stub      (acc_integration/issue_stub.py)

Schedule this script with Windows Task Scheduler to run every Wednesday.
Entry point: python main.py

Logs to: logs/pipeline.log (rotating, 30-day retention)

Setup:
    pip install pandas openpyxl reportlab
    Place Navisworks CSV exports in: data/input/
    Reports are written to:         data/output/
    Processed CSVs are archived to: data/archive/
"""

import logging
import shutil
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Add BIM_Automation root to path so modules can import config
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    INPUT_DIR, OUTPUT_DIR, ARCHIVE_DIR, LOG_DIR, LOG_FILE,
    LOG_MAX_BYTES, LOG_BACKUP_COUNT
)
from clash_processing import clash_grouper, clash_prioritizer
from reports import report_generator
from acc_integration import issue_stub


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    # Also log to console when running manually
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    root_logger.addHandler(console)


# ---------------------------------------------------------------------------
# Archive helpers
# ---------------------------------------------------------------------------

def archive_inputs(input_dir: Path, archive_dir: Path) -> None:
    """Move processed CSV files from input/ to archive/ with a timestamp prefix."""
    archive_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    moved = 0
    for csv_file in input_dir.glob("*.csv"):
        dest = archive_dir / f"{timestamp}_{csv_file.name}"
        shutil.move(str(csv_file), dest)
        logging.getLogger(__name__).info("Archived %s → %s", csv_file.name, dest.name)
        moved += 1
    logging.getLogger(__name__).info("archive_inputs: %d file(s) archived", moved)


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline() -> None:
    logger = logging.getLogger(__name__)
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("BIM Automation Pipeline — starting at %s", start_time.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("=" * 60)

    # Ensure directories exist
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Stage 1: Clash Grouping
    detail_df, summary_df = clash_grouper.run(INPUT_DIR)

    if detail_df.empty:
        logger.warning("Pipeline halted — no clash data found in %s", INPUT_DIR)
        logger.warning("Place Navisworks CSV exports in the input folder and re-run.")
        return

    logger.info("Stage 1 complete: %d clashes, %d groups", len(detail_df), len(summary_df))

    # Stage 2: Clash Prioritization
    detail_df = clash_prioritizer.run(detail_df)
    logger.info("Stage 2 complete: priorities assigned")

    # Stage 3: Report Generation
    outputs = report_generator.run(detail_df, OUTPUT_DIR)
    logger.info("Stage 3 complete: reports written — %s", ", ".join(outputs.keys()))

    # Stage 4: ACC Issue Stub
    issues = issue_stub.run(detail_df)
    logger.info("Stage 4 complete: %d issues simulated", len(issues))

    # Archive processed inputs
    archive_inputs(INPUT_DIR, ARCHIVE_DIR)

    elapsed = (datetime.now() - start_time).total_seconds()
    logger.info("=" * 60)
    logger.info("Pipeline complete in %.1f seconds", elapsed)
    logger.info("Reports: %s", OUTPUT_DIR)
    logger.info("=" * 60)


if __name__ == "__main__":
    setup_logging()
    run_pipeline()
```

**Step 2: Verify**

Read `BIM_Automation/main.py` back.

---

### Task 8: Update `BIM Coordination Automation Toolkit.md`

**Files:**
- Modify: `BIM Coordination Automation Toolkit.md`

**Step 1: Replace the stub scripts section**

Replace the existing stub Python code blocks in the toolkit document with a reference section that:
- Points to the production scripts in `BIM_Automation/`
- Shows the key function signatures and what each module does
- Preserves the conceptual explanation (grouping logic, priority table, weekly workflow, folder structure)
- Adds a "Deployment" section explaining how to schedule via Task Scheduler
- Adds a "Dependencies" section listing `pip install pandas openpyxl reportlab`

**Step 2: Verify**

Read the updated toolkit document back from the top to confirm formatting is intact.

---

## Roadmap (Phase 2 — Not in scope now)

These are documented as `# TODO (Phase 2):` comments in the code:
- Replace CSV drop with ACC API pull (authenticated, scheduled)
- Email alert on pipeline failure
- Fault-tolerant per-record error skipping with detailed logging
- Live ACC issue creation via Autodesk API (OAuth 2.0 + Issues API v1)
- Power BI direct dataset push via REST API

---

## Deployment Reference (for Task 8)

**Windows Task Scheduler setup:**
1. Open Task Scheduler → Create Basic Task
2. Name: `BIM Coordination Pipeline`
3. Trigger: Weekly, Wednesday, 6:00 AM (before coordinator arrives)
4. Action: Start a Program
   - Program: `python`
   - Arguments: `C:\BIM_Automation\main.py`
   - Start in: `C:\BIM_Automation\`
5. Run whether user is logged on or not

**Dependencies:**
```
pip install pandas openpyxl reportlab
```
