# BIM Coordination Auto Package

A complete BIM coordination system for Revit and Navisworks projects. Includes a pyRevit toolbar (27 scripts), a Python automation pipeline, and Power BI dashboard guides.

---

## What It Does

| Component | Description |
|---|---|
| **BIMTools pyRevit Toolbar** | 27 buttons across 7 panels — project setup, model health checks, clash coordination, coordinate management, reporting, utilities, and health scoring |
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
├── BIMTools.extension/          pyRevit toolbar (27 scripts)
│   ├── lib/
│   │   ├── bim_utils.py         Shared utilities
│   │   └── coord_utils.py       Coordinate math + Extensible Storage I/O
│   ├── BIM.panel/               1 button: HealthScore (150-pt model scorer)
│   ├── Project_Setup.panel/     6 setup buttons
│   ├── Model_Health.panel/      6 health check buttons
│   ├── Coordination.panel/      7 clash workflow buttons
│   ├── Coordinates.panel/       4 coordinate management buttons
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
| [Coordinates](docs/tools/08-coordinates.md) | Coordinate setup, validation, grid finder, CAD export |

---

## Model Health Score

The **HealthScore** button (BIM panel) generates a 150-point score across 8 categories. Scores are logged to `model_health_scores.csv` for trend tracking in Power BI.

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
