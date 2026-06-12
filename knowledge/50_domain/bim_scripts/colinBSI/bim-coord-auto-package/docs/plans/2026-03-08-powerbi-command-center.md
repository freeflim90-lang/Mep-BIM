# Power BI Command Center Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add an ExportGrids pyRevit button, a Navisworks XML clash parser, and a comprehensive Power BI build guide to complete the BIM Command Center dashboard system.

**Architecture:** Three components extend the existing pipeline: (1) a new pyRevit button exports grid line and level elevation data from Revit; (2) `clash_parser.py` reads Navisworks XML + those CSVs to produce `clash_heatmap_data.csv` with Level and GridZone columns; (3) a Power BI build guide documents all four dashboards with exact visual types, field assignments, and DAX measures.

**Tech Stack:** Python 3 (standard library only: xml.etree.ElementTree, csv, bisect, os), IronPython/pyRevit (Revit API: Grid, Level, UnitUtils), Power BI Desktop (Matrix visual, conditional formatting, DAX), Markdown.

---

## Task 1: ExportGrids pyRevit Button

**Files:**
- Create: `BIMTools.extension/Utilities.panel/ExportGrids.pushbutton/script.py`

Exports grid line positions and level elevations from the active Revit model. Used by `clash_parser.py` to map clash XYZ coordinates to GridZone and Level labels.

**Step 1: Write the file**

```python
"""
ExportGrids — Exports grid line positions and level elevations to CSV.

Outputs (to C:\BIM_Automation\data\output\):
  grid_lines.csv       — GridName, Orientation (H/V), Position (feet)
  level_elevations.csv — LevelName, Elevation (feet)

Run once when grid layout is established. Re-run if grids change.
Used by clash_parser.py to map clash XYZ to GridZone and Level.
Read-only. No model changes.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Grid, Level

# UnitUtils API changed in Revit 2022 — handle both
try:
    from Autodesk.Revit.DB import UnitUtils, UnitTypeId
    def to_feet(v):
        return UnitUtils.ConvertFromInternalUnits(v, UnitTypeId.Feet)
except ImportError:
    from Autodesk.Revit.DB import UnitUtils, DisplayUnitType
    def to_feet(v):
        return UnitUtils.ConvertFromInternalUnits(v, DisplayUnitType.DUT_DECIMAL_FEET)

from bim_utils import write_csv
from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

GRID_FILE = "grid_lines.csv"
LEVEL_FILE = "level_elevations.csv"
GRID_HEADERS = ["GridName", "Orientation", "Position"]
LEVEL_HEADERS = ["LevelName", "Elevation"]


def get_orientation_and_position(grid):
    """Return ('V', x_midpoint) or ('H', y_midpoint) for a Grid element."""
    curve = grid.Curve
    start = curve.GetEndPoint(0)
    end = curve.GetEndPoint(1)
    dx = abs(end.X - start.X)
    dy = abs(end.Y - start.Y)
    mid_x = (start.X + end.X) / 2.0
    mid_y = (start.Y + end.Y) / 2.0
    if dy > dx:
        # Runs mostly in Y direction — vertical grid line, position = X
        return "V", round(to_feet(mid_x), 4)
    else:
        # Runs mostly in X direction — horizontal grid line, position = Y
        return "H", round(to_feet(mid_y), 4)


def run():
    # Export grids
    grids = list(FilteredElementCollector(doc).OfClass(Grid).ToElements())
    grid_rows = []
    for g in grids:
        orientation, position = get_orientation_and_position(g)
        grid_rows.append([g.Name, orientation, position])
    grid_rows.sort(key=lambda r: (r[1], r[2]))
    grid_path = write_csv(GRID_FILE, GRID_HEADERS, grid_rows)

    # Export levels
    levels = list(FilteredElementCollector(doc).OfClass(Level).ToElements())
    level_rows = []
    for lv in levels:
        level_rows.append([lv.Name, round(to_feet(lv.Elevation), 4)])
    level_rows.sort(key=lambda r: r[1])
    level_path = write_csv(LEVEL_FILE, LEVEL_HEADERS, level_rows)

    output.print_md(
        "**Grid lines exported:** `{}` — {} grid(s)  \n"
        "**Level elevations exported:** `{}` — {} level(s)".format(
            grid_path, len(grid_rows),
            level_path, len(level_rows),
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 2: Verify**

Read `BIMTools.extension/Utilities.panel/ExportGrids.pushbutton/script.py` — confirm `get_orientation_and_position` returns V/H, `to_feet` try/except for Revit 2022 compatibility, both CSVs written via `write_csv`.

---

## Task 2: clash_parser.py

**Files:**
- Create: `BIM_Automation/clash_processing/clash_parser.py`

Parses Navisworks XML clash report. Maps Z coordinates to Level names using `level_elevations.csv`. Maps XY to GridZone using `grid_lines.csv`. Outputs `clash_heatmap_data.csv` for Power BI.

**Step 1: Write the file**

```python
"""
clash_parser.py — Parse Navisworks XML clash report into heatmap CSV.

Input:
  data/input/clash_report.xml        — Navisworks XML export
  data/output/grid_lines.csv         — from ExportGrids pyRevit button
  data/output/level_elevations.csv   — from ExportGrids pyRevit button

Output:
  data/output/clash_heatmap_data.csv
  Columns: ClashID, Status, DisciplineA, DisciplineB, Level, GridZone, X, Y, Z

Called as Stage 0 in main.py. If clash_report.xml is absent, logs and
returns immediately — not an error (XML export is a manual Tuesday step).

Discipline pair is extracted from the clash test name (e.g. "Arch vs Structure").
Level is the highest level whose elevation <= clash Z. Below all levels = "Below Grade".
GridZone is "VertGrid1-VertGrid2/HorizGrid1-HorizGrid2". Outside grid = "Outside Grid".
"""
import bisect
import csv
import logging
import os
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

XML_FILENAME = "clash_report.xml"
HEATMAP_FILENAME = "clash_heatmap_data.csv"
GRID_FILENAME = "grid_lines.csv"
LEVEL_FILENAME = "level_elevations.csv"

HEADERS = [
    "ClashID", "Status", "DisciplineA", "DisciplineB",
    "Level", "GridZone", "X", "Y", "Z",
]


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_grid_lines(output_dir):
    """Return (vertical_grids, horizontal_grids) sorted by Position.
    Each list contains (position_float, name_str) tuples.
    Returns (None, None) if file is missing."""
    path = os.path.join(output_dir, GRID_FILENAME)
    if not os.path.exists(path):
        logger.warning("grid_lines.csv not found — GridZone will show 'No Grid Data'")
        return None, None
    vertical, horizontal = [], []
    with open(path, "r") as f:
        for row in csv.DictReader(f):
            pos = float(row["Position"])
            name = row["GridName"]
            if row["Orientation"] == "V":
                vertical.append((pos, name))
            else:
                horizontal.append((pos, name))
    vertical.sort()
    horizontal.sort()
    return vertical, horizontal


def load_levels(output_dir):
    """Return list of (elevation_float, level_name_str) sorted by elevation asc.
    Returns None if file is missing."""
    path = os.path.join(output_dir, LEVEL_FILENAME)
    if not os.path.exists(path):
        logger.warning("level_elevations.csv not found — Level will show raw Z")
        return None
    levels = []
    with open(path, "r") as f:
        for row in csv.DictReader(f):
            levels.append((float(row["Elevation"]), row["LevelName"]))
    levels.sort()
    return levels


# ---------------------------------------------------------------------------
# Coordinate mappers
# ---------------------------------------------------------------------------

def map_level(z, levels):
    """Return level name for given Z elevation.
    Finds the highest level whose elevation <= z."""
    if levels is None:
        return str(round(z, 2))
    elevations = [lv[0] for lv in levels]
    idx = bisect.bisect_right(elevations, z) - 1
    if idx < 0:
        return "Below Grade"
    return levels[idx][1]


def find_bracket(pos, grids):
    """Return 'Name1-Name2' for the bay pos falls in, or edge labels."""
    if not grids:
        return "?"
    positions = [g[0] for g in grids]
    names = [g[1] for g in grids]
    idx = bisect.bisect_right(positions, pos) - 1
    if idx < 0:
        return "<" + names[0]
    if idx >= len(grids) - 1:
        return ">" + names[-1]
    return names[idx] + "-" + names[idx + 1]


def map_grid_zone(x, y, vertical, horizontal):
    """Return GridZone string like 'A-B/1-2'."""
    if vertical is None or horizontal is None:
        return "No Grid Data"
    v_zone = find_bracket(x, vertical)
    h_zone = find_bracket(y, horizontal)
    return "{}/{}".format(v_zone, h_zone)


# ---------------------------------------------------------------------------
# XML parser
# ---------------------------------------------------------------------------

def parse_discipline_pair(test_name):
    """Extract DisciplineA, DisciplineB from test name like 'Arch vs Structure'."""
    if " vs " in test_name:
        parts = test_name.split(" vs ", 1)
        return parts[0].strip(), parts[1].strip()
    return test_name.strip(), "Unknown"


def parse_xml(xml_path, vertical, horizontal, levels):
    """Parse Navisworks XML and return list of rows matching HEADERS."""
    rows = []
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for clashtest in root.iter("clashtest"):
        test_name = clashtest.get("name", "Unknown")
        disc_a, disc_b = parse_discipline_pair(test_name)

        for clash in clashtest.iter("clashresult"):
            clash_id = clash.get("name", "")
            status = clash.get("status", "active")

            pos = clash.find(".//clashpoint/pos3f")
            if pos is None:
                continue  # skip clashes with no position data

            x = float(pos.get("x", 0))
            y = float(pos.get("y", 0))
            z = float(pos.get("z", 0))

            level = map_level(z, levels)
            grid_zone = map_grid_zone(x, y, vertical, horizontal)

            rows.append([
                clash_id, status, disc_a, disc_b,
                level, grid_zone,
                round(x, 4), round(y, 4), round(z, 4),
            ])

    return rows


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(input_dir=None, output_dir=None):
    """Run the clash parser. Called from main.py as Stage 0.
    Accepts optional path overrides for testing."""
    from config import INPUT_DIR, OUTPUT_DIR
    input_dir = str(input_dir or INPUT_DIR)
    output_dir = str(output_dir or OUTPUT_DIR)

    xml_path = os.path.join(input_dir, XML_FILENAME)
    if not os.path.exists(xml_path):
        logger.info(
            "clash_report.xml not found in %s — skipping clash parser "
            "(place Navisworks XML export there on Tuesday)", input_dir
        )
        return 0

    vertical, horizontal = load_grid_lines(output_dir)
    levels = load_levels(output_dir)

    logger.info("Parsing %s", xml_path)
    rows = parse_xml(xml_path, vertical, horizontal, levels)

    out_path = os.path.join(output_dir, HEATMAP_FILENAME)
    os.makedirs(output_dir, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        w.writerows(rows)

    logger.info("clash_heatmap_data.csv written — %d clashes", len(rows))
    return len(rows)


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent))
    run()
```

**Step 2: Verify**

Read `BIM_Automation/clash_processing/clash_parser.py` — confirm `bisect.bisect_right` used for both level and grid mapping, `parse_discipline_pair` splits on `" vs "`, `run()` accepts optional path overrides, XML-absent early return logs and returns 0.

---

## Task 3: Update main.py — Add Stage 0

**Files:**
- Modify: `BIM_Automation/main.py`

Add Stage 0 (clash parser) before Stage 1. Stage 0 is non-blocking — if it fails or the XML is absent, the pipeline continues.

**Step 1: Add import**

In `main.py`, find the existing import block:
```python
from clash_processing import clash_grouper, clash_prioritizer
```

Replace with:
```python
from clash_processing import clash_grouper, clash_prioritizer, clash_parser
```

**Step 2: Update docstring**

Find:
```python
Runs the full coordination pipeline in sequence:
    1. Clash Grouping      (clash_processing/clash_grouper.py)
    2. Clash Prioritization (clash_processing/clash_prioritizer.py)
    3. Report Generation   (reports/report_generator.py)
    4. ACC Issue Stub      (acc_integration/issue_stub.py)
```

Replace with:
```python
Runs the full coordination pipeline in sequence:
    0. Clash XML Parser    (clash_processing/clash_parser.py)   ← skipped if no XML
    1. Clash Grouping      (clash_processing/clash_grouper.py)
    2. Clash Prioritization (clash_processing/clash_prioritizer.py)
    3. Report Generation   (reports/report_generator.py)
    4. ACC Issue Stub      (acc_integration/issue_stub.py)
```

**Step 3: Add Stage 0 call in run_pipeline()**

Find:
```python
    # Stage 1: Clash Grouping
    detail_df, summary_df = clash_grouper.run(INPUT_DIR)
```

Insert before it:
```python
    # Stage 0: Clash XML Parser (non-blocking — skipped if clash_report.xml absent)
    try:
        clash_count = clash_parser.run(INPUT_DIR, OUTPUT_DIR)
        if clash_count:
            logger.info("Stage 0 complete: %d clashes parsed to clash_heatmap_data.csv", clash_count)
        else:
            logger.info("Stage 0 skipped: clash_report.xml not found")
    except Exception:
        logger.exception("Stage 0 failed — continuing pipeline without heatmap data")

```

**Step 4: Verify**

Read `BIM_Automation/main.py` — confirm Stage 0 is inside its own try/except (not inside the Stage 1–4 try block), runs before `clash_grouper.run`, and passes `INPUT_DIR, OUTPUT_DIR` to `clash_parser.run`.

---

## Task 4: Power BI Build Guide

**Files:**
- Create: `docs/powerbi/command-center-setup.md`

Step-by-step guide to build all four Power BI dashboards from the pipeline CSV outputs.

**Step 1: Create the directory marker and write the guide**

```markdown
# BIM Command Center — Power BI Setup Guide

## Overview

Build four dashboards in Power BI Desktop that connect to the CSV files produced
by the BIM Automation Pipeline. All data lives in `C:\BIM_Automation\data\output\`.

**Dashboards:**
1. Project Health — model scores + clash totals
2. Clash Heat Map — Level × GridZone matrix
3. Coordination Performance — discipline breakdown + trend
4. Model Health Trends — score over time per model

---

## Prerequisites

- Power BI Desktop installed (free — download from microsoft.com/power-bi)
- Pipeline has run at least once (CSVs exist in output folder)
- ExportGrids button has been run on the coordination model (grid_lines.csv exists)

---

## Step 1 — Connect to Data Folder

1. Open Power BI Desktop → **Get Data → Folder**
2. Path: `C:\BIM_Automation\data\output`
3. Click **OK → Transform Data**

In Power Query, you will see all CSV files listed. Load only these four:

| Table Name (rename in Power Query) | Source File |
|---|---|
| `ModelHealth` | `model_health_scores.csv` |
| `ClashHeatmap` | `clash_heatmap_data.csv` |
| `ClashSummary` | `clash_summary_report.csv` |
| `CoordReport` | `coordination_report.csv` |

**To load a specific file:** Right-click a row in the folder view →
**Combine → Combine & Load** → select the file.
Rename the query in the right-hand panel to the Table Name above.

**Data types to set in Power Query:**
- `ModelHealth[RunDate]` → Date
- `ModelHealth[TotalScore]` → Whole Number
- `ClashHeatmap[X]`, `[Y]`, `[Z]` → Decimal Number
- `ClashSummary[Count]` → Whole Number
- All other columns → Text (default is fine)

Click **Close & Apply**.

---

## Step 2 — DAX Measures

In the **Model** view, create a new table called `_Measures` (blank table) to
keep all measures organised. Add these measures:

```dax
Active Clashes =
COUNTROWS(FILTER(ClashHeatmap, ClashHeatmap[Status] <> "resolved"))

Avg Health Score =
AVERAGE(ModelHealth[TotalScore])

Models Below 100 =
COUNTROWS(FILTER(ModelHealth, ModelHealth[TotalScore] < 100))

Clash Resolution Rate =
DIVIDE(
    CALCULATE(SUM(ClashSummary[Count]), ClashSummary[Status] = "Resolved"),
    SUM(ClashSummary[Count]),
    0
)

Latest Score Per Model =
CALCULATE(
    MAX(ModelHealth[TotalScore]),
    LASTDATE(ModelHealth[RunDate])
)
```

**To add a measure:** Click the `_Measures` table → **New Measure** in the ribbon → paste DAX.

---

## Step 3 — Dashboard 1: Project Health

**Create a new report page.** Rename it **"Project Health"**.

### KPI Cards (top row — 4 cards)

Add 4 **Card** visuals. Field assignments:

| Card | Field |
|---|---|
| Total Models | `DISTINCTCOUNT(ModelHealth[ModelName])` — add as a new measure |
| Avg Health Score | `[Avg Health Score]` measure |
| Active Clashes | `[Active Clashes]` measure |
| Models Below 100 | `[Models Below 100]` measure |

### Model Health Table

Add a **Table** visual. Columns:
- `ModelHealth[ModelName]`
- `ModelHealth[TotalScore]`
- `ModelHealth[Status]`
- `ModelHealth[RunDate]`

**Conditional formatting on Status column:**
- Visualizations pane → Format → Cell elements → Background color → **Field value**
- Rules:
  - "Elite" → `#107C41` (dark green)
  - "Excellent" → `#0070C0` (blue)
  - "Healthy" → `#00B050` (green)
  - "Needs Cleanup" → `#FFC000` (amber)
  - "Critical" → `#FF0000` (red)

### Score by Model Bar Chart

Add a **Clustered bar chart**:
- Y axis: `ModelHealth[ModelName]`
- X axis: `ModelHealth[TotalScore]`
- Sort: by TotalScore descending

**Add reference line at 100:**
Analytics pane → Constant Line → Value: 100 → Color: red, label: "Min for Coordination"

---

## Step 4 — Dashboard 2: Clash Heat Map

**Add a new page.** Rename it **"Clash Heat Map"**.

### Heat Map Matrix

Add a **Matrix** visual:
- Rows: `ClashHeatmap[Level]`
- Columns: `ClashHeatmap[GridZone]`
- Values: `COUNTROWS(ClashHeatmap)` — add as a measure called `Clash Count`

**Sort rows by level elevation:**
- Add a column `LevelOrder` to ClashHeatmap in Power Query using a merge with the
  `level_elevations.csv` table (join on Level = LevelName, bring in Elevation).
- Sort `ClashHeatmap[Level]` by `ClashHeatmap[LevelOrder]` in the column tools.

**Conditional formatting on Values:**
- Format → Cell elements → Background color → Rules:
  - 0 → White (`#FFFFFF`)
  - 1–10 → Light green (`#E2EFDA`)
  - 11–25 → Amber (`#FFE699`)
  - 26+ → Red (`#FF0000`)

### Slicers

Add two **Slicer** visuals:
- Slicer 1: `ClashHeatmap[DisciplineA]` — title: "Discipline A"
- Slicer 2: `ClashHeatmap[Status]` — title: "Clash Status"

### Clash by Discipline Pair Bar Chart

Add a new column in Power Query on ClashHeatmap:
```
DisciplinePair = [DisciplineA] & " vs " & [DisciplineB]
```

Add a **Clustered bar chart**:
- Y axis: `ClashHeatmap[DisciplinePair]`
- X axis: `Clash Count` measure
- Sort: by Clash Count descending
- Top N filter: show top 10

---

## Step 5 — Dashboard 3: Coordination Performance

**Add a new page.** Rename it **"Coordination Performance"**.

### Clashes by Discipline (Bar Chart)

Add a **Clustered bar chart**:
- Y axis: `ClashHeatmap[DisciplineA]`
- X axis: `Clash Count` measure
- Sort: descending

### Clash Status Breakdown (Stacked Bar)

Add a **Stacked bar chart**:
- Y axis: `ClashSummary[Status]`
- X axis: `SUM(ClashSummary[Count])`
- Legend: `ClashSummary[Status]`

Colors: Open=red, In Progress=amber, Resolved=green.

### Clash Trend Over Time (Line Chart)

Add a **Line chart**:
- X axis: `ClashHeatmap[RunDate]` — group by Week (right-click → Date hierarchy → Week)
  *(If RunDate column not in ClashHeatmap, use `CoordReport[RunDate]` and `CoordReport[CADImportCount]`
  as a proxy, or add RunDate to clash_heatmap_data.csv by updating clash_parser.py to stamp today's date)*
- Y axis: `Clash Count` measure
- Title: "Clash Count Trend"

---

## Step 6 — Dashboard 4: Model Health Trends

**Add a new page.** Rename it **"Model Health Trends"**.

### Score Over Time (Line Chart)

Add a **Line chart**:
- X axis: `ModelHealth[RunDate]`
- Y axis: `ModelHealth[TotalScore]`
- Legend: `ModelHealth[ModelName]`

**Reference lines (Analytics pane → Constant Line):**
- 130 → label "Elite", color green
- 100 → label "Min for Coordination", color orange
- 85 → label "Critical", color red

### Model Slicer

Add a **Slicer**:
- Field: `ModelHealth[ModelName]`
- Style: Dropdown (Format → Slicer settings → Style: Dropdown)

---

## Step 7 — Refresh Schedule

**Manual refresh (no gateway):**
After the Wednesday pipeline run, open Power BI Desktop and click **Refresh** in the Home ribbon.

**Scheduled refresh (requires Power BI Pro + on-premises data gateway):**
1. Publish the report to Power BI Service (Home → Publish)
2. In Power BI Service → Dataset settings → Scheduled refresh
3. Set: every Wednesday at 8:00 AM
4. Install on-premises data gateway on the machine running the pipeline

---

## Weekly Workflow Integration

| Day | Action |
|---|---|
| Monday | Run HealthScore button on all models (model_health_scores.csv updated) |
| Tuesday | Run clash tests in Navisworks; export XML to `C:\BIM_Automation\data\input\clash_report.xml` |
| Wednesday 6AM | Pipeline runs automatically (Task Scheduler); clash_heatmap_data.csv produced |
| Wednesday AM | Open Power BI Desktop → Refresh |
| Friday | Coordination meeting using all 4 dashboards |

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `clash_heatmap_data.csv` missing | XML not in input folder | Export XML from Navisworks Clash Detective → Results → Export → XML Report |
| GridZone shows "No Grid Data" | ExportGrids button not run | Run ExportGrids from Utilities panel in Revit |
| Level shows "Below Grade" | Z coordinate below all levels | Check level elevations — model may use a non-zero datum |
| Matrix has too many GridZone columns | Grid lines exported from wrong model | Run ExportGrids on the coordination model (the one with all grids) |
| RunDate column not parsed as date | Power Query loaded it as text | In Power Query: select column → Change Type → Date |
```

**Step 2: Verify**

Read `docs/powerbi/command-center-setup.md` — confirm all 4 dashboards covered, DAX measures present, conditional formatting colour codes included, weekly workflow table present, troubleshooting section present.

---

## Verification Checklist

After all tasks:

- [ ] `BIMTools.extension/Utilities.panel/ExportGrids.pushbutton/script.py` exists
- [ ] `BIM_Automation/clash_processing/clash_parser.py` exists
- [ ] `main.py` imports `clash_parser` and calls it as Stage 0 in its own try/except
- [ ] `docs/powerbi/command-center-setup.md` exists with all 4 dashboards documented
- [ ] `clash_parser.run()` accepts optional `input_dir`, `output_dir` arguments
- [ ] Stage 0 in main.py is non-blocking (failure does not stop the pipeline)
- [ ] ExportGrids script handles Revit 2022 UnitUtils API change via try/except ImportError
