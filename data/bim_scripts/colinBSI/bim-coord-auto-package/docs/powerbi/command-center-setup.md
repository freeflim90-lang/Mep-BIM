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

## Step 0 — Auto-Refresh Setup

Do this once when you first open the `.pbix` file. It makes Power BI refresh all
connected CSVs automatically every time you open the file — no manual Refresh click needed.

1. **Options → Data Load:**
   Power BI Desktop → **File → Options and settings → Options → Data Load**
   - Check: **"Refresh data in the background when opening reports"**
   - Set **Query timeout (in seconds)** to **30**
2. Click **OK**.

> **Result:** Every time you open the `.pbix` on Wednesday morning after the pipeline
> has run, the data automatically reflects the latest CSVs from `C:\BIM_Automation\data\output\`.

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

## Step 7 — Pipeline Status Card

Add two status cards to each of the 4 dashboard pages so you always know when the
data was last updated and whether the pipeline succeeded.

### Load the metadata table

In **Power Query (Transform Data)**, load `pipeline_metadata.csv` from the output folder.
Rename the query: `PipelineStatus`.

**Data types to set:**
- `PipelineStatus[RunDate]` → Date
- `PipelineStatus[RunTimestamp]` → Datetime (use locale: en-US, format: `yyyy-MM-dd HH:mm:ss`)
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
    "ddd DD-MMM h:mm AM/PM"
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

## Step 8 — Refresh Schedule

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
| Wednesday AM | Open Power BI Desktop — auto-refreshes on open (Step 0) |
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
