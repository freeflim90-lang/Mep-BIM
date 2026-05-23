# Reporting Panel

The Reporting panel generates coordination reports directly from Revit. For the full weekly pipeline report (from Navisworks exports), see the [Pipeline](06-pipeline.md) documentation.

---

## Tools

### Coordination Report

**Purpose:** Generates a coordination status report combining model health metrics, clash data, warnings, and open issues.

**When to use:** On demand — before coordination meetings or when a status summary is needed.

**How to use:**
1. Click **Coord Report**
2. Report is saved to `C:\BIM_Automation\data\output\`

**Output:** CSV/Excel report with:
- Model health summary
- Clash metrics (open, in progress, resolved)
- Warning counts
- Open issues

---

### Clash Summary

**Purpose:** Generates a summary of open and resolved clashes grouped by discipline pair.

**When to use:**
- Friday coordination meetings
- Weekly status updates

**How to use:**
1. Click **Clash Summary**
2. Report is saved to `C:\BIM_Automation\data\output\`

**Output columns:** Discipline pair, total clashes, open, in progress, resolved

---

## Tips

- The Python pipeline (run automatically each Wednesday) generates a more complete report including prioritization and PDF output — see [Pipeline documentation](06-pipeline.md)
- Reporting panel tools pull live data from the open Revit model; the pipeline pulls from Navisworks CSV exports
- All outputs go to `C:\BIM_Automation\data\output\` — this is the same folder Power BI reads from
