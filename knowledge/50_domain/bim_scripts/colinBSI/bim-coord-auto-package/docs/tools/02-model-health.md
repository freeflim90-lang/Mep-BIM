# Model Health Panel

The Model Health panel provides read-only diagnostic tools. Use these tools to audit a Revit model before coordination, after model receipt, or as part of a weekly health check.

> All Model Health tools are **read-only** — they never modify the model.

---

## Tools

### Warning Manager

**Purpose:** Exports all Revit warnings to a CSV, classified by severity.

**When to use:**
- Weekly health checks
- Before issuing a model health score
- After receiving a model from a subcontractor

**How to use:**
1. Open the Revit model
2. Click **Warning Manager**
3. Report is saved to `C:\BIM_Automation\data\output\warnings_report.csv`

**Output columns:** Warning message, element IDs, severity classification

**Severity classification:**

| Severity | Keywords |
|---|---|
| Critical | corrupt, overlap |
| High | duplicate, joins |
| Medium | all other warnings |

**Targets:**
- Ideal: fewer than 300 warnings
- Acceptable: fewer than 1,000 warnings

---

### Find CAD Imports

**Purpose:** Lists all CAD files that have been imported (not linked) into the model.

**When to use:** When auditing a model received from a subcontractor, or as part of setup QC.

**How to use:**
1. Click **Find CAD Imports**
2. Results appear in the pyRevit console

**Why it matters:** Imported CAD files increase file size and can cause performance issues. They should be linked instead.

**Action:** For each CAD import found, delete it and re-insert as a linked file (Insert → Link CAD).

---

### Find Large Families

**Purpose:** Identifies Revit families larger than 5 MB.

**When to use:**
- When model file size exceeds targets
- During model audits

**How to use:**
1. Click **Find Large Families**
2. Results appear in the pyRevit console with family name and size

**File size targets:**
- Ideal: under 300 MB total model size
- Acceptable: under 500 MB

**Action:** Replace oversized families with leaner versions, or purge unused types from within the family.

---

### Group Inspector

**Purpose:** Reports on all groups in the model — count, types, and nested groups.

**When to use:** When investigating model warnings related to groups, or during cleanup.

**How to use:**
1. Click **Group Inspector**
2. Results appear in the pyRevit console

**What to look for:** Large numbers of nested groups or ungrouped instances can cause warnings and slow performance.

---

### Unplaced Views

**Purpose:** Lists all views that exist in the model but are not placed on any sheet.

**When to use:** Before issuing a model for coordination or at project closeout.

**How to use:**
1. Click **Unplaced Views**
2. Results appear in the pyRevit console

**Action:** Delete views that are no longer needed, or place them on sheets if they are required for documentation.

---

### Unused Families

**Purpose:** Exports a list of families loaded into the model with zero placed instances.

**When to use:** Before model health scoring or when reducing file size.

**How to use:**
1. Click **Unused Families**
2. Report saved to `C:\BIM_Automation\data\output\unused_families_report.csv`

> This tool only **reports** — it does not purge. Use Revit's native Purge Unused (Manage tab) to remove families after reviewing the report.

---

## Model Health Score

The **HealthScore** button (BIM panel) runs all health checks automatically and generates a 150-point score. See the root [README](../../README.md#model-health-score) for score thresholds.

---

## Tips

- Run all Model Health tools when you first receive a model from a new subcontractor
- The Warning Manager and Unused Families reports feed into the Power BI Model Health Trends dashboard
- A model must score 100 or higher before entering active coordination
