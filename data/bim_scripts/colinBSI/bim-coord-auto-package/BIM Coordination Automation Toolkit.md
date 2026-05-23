# BIM Coordination Automation Toolkit

This toolkit automates the most time-consuming BIM coordination tasks, reducing coordination admin work by 50–70%.

It connects:

- Navisworks Manage
- Autodesk Construction Cloud (ACC)
- Revit
- Python
- Power BI

---

## System Architecture

```
Revit Models
     ↓
Navisworks Clash Tests
     ↓
Clash Automation Engine (Python)
     ↓
ACC Issue Creation
     ↓
Weekly Coordination Reports
     ↓
Power BI Command Center
```

---

## The Four Tools

### Tool 1 — Automatic Clash Grouping
**Script:** `BIM_Automation/clash_processing/clash_grouper.py`

Large projects produce thousands of clashes. Reviewing them one-by-one is inefficient. This tool automatically groups them by level, discipline pair, and grid location.

**Key functions:**
- `load_clash_csvs(input_dir)` — loads all CSV exports from the input folder, skips malformed files
- `add_group_key(df)` — adds a `GroupKey` column: `Level3_Mechanical_vs_Structure`
- `summarize_groups(df)` — returns one row per group with clash count, sorted descending
- `run(input_dir)` — main entry point, returns `(detail_df, summary_df)`

**Before grouping:**
```
Clash 1, Clash 2, Clash 3 ... (hundreds of individual rows)
```

**After grouping:**
```
Level3_Mechanical_vs_Structure    42 clashes
Level2_Plumbing_vs_Structure      18 clashes
Level1_Electrical_vs_HVAC          9 clashes
```

---

### Tool 2 — Automatic ACC Issue Creation
**Script:** `BIM_Automation/acc_integration/issue_stub.py`

*Phase 2 stub — simulates issue creation now; live ACC API in Phase 2.*

This automation converts Critical and High priority clashes into ACC coordination issues automatically. Each simulated issue includes:

| Field | Example |
|---|---|
| Title | Mechanical vs Structure Clash — Level 3 Grid C5 |
| Description | 12" duct intersects beam B204 |
| Status | open |
| Priority | critical |
| Assigned To | Mechanical Contractor |
| Due Date | 7 days from run date |

**Phase 2 upgrade path:**
To activate live issue creation, see the TODO checklist in `issue_stub.py` and set `ACC_CLIENT_ID`, `ACC_CLIENT_SECRET`, and `ACC_PROJECT_ID` in `config.py`.

---

### Tool 3 — Weekly Coordination Report Generator
**Script:** `BIM_Automation/reports/report_generator.py`

Every coordination meeting should start with automatically generated reports. This tool produces three files from the enriched clash data:

| Output | Contents |
|---|---|
| `weekly_coordination_report.csv` | Full enriched clash list with GroupKey and Priority |
| `weekly_coordination_report.xlsx` | 3 tabs: Summary, Discipline Breakdown, High Risk Areas |
| `weekly_coordination_report.pdf` | 1-page styled summary for the Friday meeting |

**Excel tab: Summary**

| Metric | Value |
|---|---|
| Total Clashes | 1,240 |
| Critical | 420 |
| High | 210 |
| Medium | 515 |
| Low | 95 |
| Unique Groups | 18 |

**Excel tab: Discipline Breakdown** — clash counts by discipline pair, sorted descending

**Excel tab: High Risk Areas** — groups with 20+ clashes

---

### Tool 4 — Clash Prioritization Engine
**Script:** `BIM_Automation/clash_processing/clash_prioritizer.py`

Not all clashes matter equally. This tool automatically ranks clashes based on construction risk.

**Priority rules (evaluated in order):**

| Priority | Rule |
|---|---|
| Low | Cosmetic pairs: Lighting/Ceiling, Lighting/Furniture, Ceiling/Furniture |
| Critical | Either discipline is Structure or Structural |
| High | Either discipline is Mechanical or Plumbing |
| Medium | All other combinations |

**Example output:**

| Clash | DisciplineA | DisciplineB | Priority |
|---|---|---|---|
| CLH-001 | Structure | Mechanical | Critical |
| CLH-002 | Plumbing | Electrical | High |
| CLH-003 | HVAC | Electrical | Medium |
| CLH-004 | Lighting | Ceiling | Low |

---

## Pipeline — How It All Connects

**Script:** `BIM_Automation/main.py`

The master runner chains all four tools in sequence:

```
data/input/*.csv
     ↓
clash_grouper.run()       — groups clashes, adds GroupKey
     ↓
clash_prioritizer.run()   — adds Priority column
     ↓
report_generator.run()    — writes CSV, Excel, PDF to data/output/
     ↓
issue_stub.run()          — simulates ACC issue creation (Phase 2: live API)
     ↓
archive_inputs()          — moves processed CSVs to data/archive/
```

---

## Weekly Workflow

| Day | Activity |
|---|---|
| Monday | Teams upload models to ACC |
| Tuesday | Clash tests run in Navisworks; CSV exports dropped in `data/input/` |
| Wednesday | Pipeline runs automatically at 6:00 AM via Task Scheduler |
| Thursday | Coordinator reviews reports in `data/output/` |
| Friday | Coordination meeting using PDF summary and Power BI dashboard |

---

## Folder Structure

```
BIM_Automation/
├── main.py                        Master runner
├── config.py                      All paths and settings
├── clash_processing/
│   ├── clash_grouper.py           Tool 1
│   └── clash_prioritizer.py      Tool 4
├── reports/
│   └── report_generator.py       Tool 3
├── acc_integration/
│   └── issue_stub.py             Tool 2 (Phase 2 stub)
├── logs/
│   └── pipeline.log              Rotating log, ~6 weeks history
└── data/
    ├── input/                    Drop Navisworks CSVs here
    ├── output/                   Reports written here
    └── archive/                  Processed CSVs moved here after each run
```

---

## Setup and Deployment

### Dependencies

```
pip install pandas openpyxl reportlab
```

### Input CSV Format

Navisworks clash exports must include these columns:

| Column | Example |
|---|---|
| ClashID | CLH-0042 |
| Level | Level 3 |
| Grid | C5 |
| DisciplineA | Mechanical |
| DisciplineB | Structure |
| ClashType | Hard |
| Description | 12" duct intersects beam B204 |
| Distance | -0.5 |

### Windows Task Scheduler Setup

1. Open Task Scheduler → Create Basic Task
2. Name: `BIM Coordination Pipeline`
3. Trigger: Weekly, Wednesday, 6:00 AM
4. Action: Start a Program
   - Program: `python`
   - Arguments: `C:\BIM_Automation\main.py`
   - Start in: `C:\BIM_Automation\`
5. Check: Run whether user is logged on or not

---

## Roadmap — Phase 2 Upgrades

All Phase 2 items are marked with `# TODO (Phase 2):` comments in the relevant scripts.

| Upgrade | Script | Notes |
|---|---|---|
| Live ACC issue creation | `issue_stub.py` | OAuth 2.0 + ACC Issues API v1 |
| Replace CSV drop with ACC API pull | `clash_grouper.py` | Fully automated, no manual export |
| Email alert on pipeline failure | `main.py` | SMTP or SendGrid |
| Per-record error skipping | `main.py` | Continue past bad rows |
| Power BI direct dataset push | `report_generator.py` | REST API |

---

## Phase 5 Upgrade Path

This toolkit automates clash grouping, ACC issue creation, and weekly reports using flat CSV outputs — this is the **Phase 3–4 automation** layer.

For portfolio-scale coordination intelligence, see `BIM compliance dashboard Requirements.md` (Phase 5), which introduces:
- Structured fact tables replacing ad-hoc CSVs
- Link placement tracking and coordinate drift detection
- Sheet and view governance with predictive velocity metrics
