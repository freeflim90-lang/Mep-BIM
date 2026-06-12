# Power BI Command Center

The Power BI Command Center connects to the pipeline output CSVs and provides four dashboards for coordination tracking.

For the complete build guide (DAX measures, conditional formatting, step-by-step setup), see:

**[docs/powerbi/command-center-setup.md](../powerbi/command-center-setup.md)**

---

## Four Dashboards

| Dashboard | What It Shows |
|---|---|
| **Project Health** | Model health score by discipline, warning counts, file sizes |
| **Clash Heat Map** | Spatial clash density by grid zone and level |
| **Coordination Performance** | Open vs. resolved clashes over time; discipline pair breakdown |
| **Model Health Trends** | Health score history per model over time |

---

## Data Sources

All dashboards read from `C:\BIM_Automation\data\output\`:

| File | Used By |
|---|---|
| `weekly_coordination_report.csv` | Coordination Performance |
| `clash_heatmap_data.csv` | Clash Heat Map |
| `model_health_scores.csv` | Project Health, Model Health Trends |
| `warnings_report.csv` | Project Health |

---

## Refresh Schedule

Power BI does not refresh automatically in the current setup. After the Wednesday pipeline run:

1. Open Power BI Desktop
2. Click **Home → Refresh**
3. Verify all four dashboards update

> Phase 2 will add automatic dataset push from the Python pipeline — see [Pipeline docs](06-pipeline.md#phase-2-planned).

---

## Quick Start

1. Open Power BI Desktop
2. **Get Data → Text/CSV** → connect to each file in `C:\BIM_Automation\data\output\`
3. Follow the full setup guide: [command-center-setup.md](../powerbi/command-center-setup.md)
