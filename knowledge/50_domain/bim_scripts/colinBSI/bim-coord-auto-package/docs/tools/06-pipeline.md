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
