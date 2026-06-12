# BIM Automation Toolkit Expansion — Design Document
**Date:** 2026-03-07
**Status:** Approved

---

## Overview

Expand the 4 stub scripts in `BIM Coordination Automation Toolkit.md` into a production-ready, scheduled pipeline that runs on a Windows server via Task Scheduler.

---

## Architecture

**Pattern:** Modular scripts with a master runner (Option B)

```
BIM_Automation/
├── main.py                  # Master runner — scheduled via Task Scheduler
├── config.py                # Paths, thresholds, settings
├── clash_processing/
│   ├── clash_grouper.py     # Tool 1: groups clashes by level/discipline/grid
│   └── clash_prioritizer.py # Tool 4: scores each group by construction risk
├── reports/
│   └── report_generator.py  # Tool 3: CSV + Excel + PDF output
├── acc_integration/
│   └── issue_stub.py        # Tool 2: placeholder with TODO markers for ACC API
├── logs/
│   └── pipeline.log         # Rotating log file (30-day retention)
└── data/
    ├── input/               # Drop CSVs here
    ├── output/              # Reports written here
    └── archive/             # Processed CSVs moved here after each run
```

**Data flow:**
`main.py` triggers on schedule → reads CSVs from `data/input/` → grouper → prioritizer → report generator → moves input to archive → writes outputs to `data/output/` → logs result.

---

## Data Model

### Input CSV (Navisworks export)

| Column | Example |
|---|---|
| `ClashID` | CLH-0042 |
| `Level` | Level 3 |
| `Grid` | C5 |
| `DisciplineA` | Mechanical |
| `DisciplineB` | Structure |
| `ClashType` | Hard |
| `Description` | 12" duct intersects beam B204 |
| `Distance` | -0.5 |

### Pipeline enrichment

- Grouper adds: `GroupKey` (e.g. `Level3_Mechanical_vs_Structure`)
- Prioritizer adds: `Priority` (`Critical / High / Medium / Low`)

### Outputs

| File | Format | Contents |
|---|---|---|
| `weekly_report.csv` | CSV | Full enriched clash list |
| `weekly_report.xlsx` | Excel | 3 tabs: Summary, Discipline Breakdown, High Risk Areas |
| `weekly_report.pdf` | PDF | 1-page summary for Friday coordination meeting |

---

## Error Handling & Logging

- Python `logging` module with `RotatingFileHandler` — 30-day retention
- Per-stage log entries: start time, record count, output path, completion time
- Malformed or missing-column CSVs: skipped and flagged, pipeline continues
- Zero records processed: logged as `WARNING`, not a crash
- Log format: `2026-03-07 09:00:01 [INFO] clash_grouper: processed 1,240 clashes into 18 groups`

---

## Roadmap Stubs (Phase 2)

All stubs marked with `# TODO (Phase 2):` comments in code:

- Replace CSV drop with ACC API pull
- Email alert on pipeline failure
- Fault-tolerant bad-record skipping with per-record logging
- ACC issue creation via Autodesk API

---

## Deployment

- **Scheduler:** Windows Task Scheduler
- **Trigger:** Scheduled (Wednesday per weekly workflow)
- **Entry point:** `main.py`

---

## Out of Scope

- ACC API integration (Phase 2)
- Power BI direct push (Phase 2)
- Email alerts (Phase 2)
- Fault-tolerant per-record error handling (Phase 2)
