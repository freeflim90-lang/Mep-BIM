# Utilities Panel

The Utilities panel contains infrastructure tools that support the broader automation pipeline.

---

## Tools

### Export Grids

**Purpose:** Exports grid line positions and level elevations from the active Revit model to CSV files used by the Python clash pipeline.

**When to use:** Every Wednesday before the automation pipeline runs — or any time grids or levels change.

**How to use:**
1. Open the Revit coordination model (the model containing grids and levels)
2. Click **Export Grids**
3. Two files are written to `C:\BIM_Automation\data\output\`

**Output files:**

| File | Contents |
|---|---|
| `grid_lines.csv` | Grid name, orientation (H/V), position in feet |
| `level_elevations.csv` | Level name, elevation in feet |

**Why it matters:** The Python pipeline uses these files to map each clash's XYZ coordinates to a grid zone and level name. Without up-to-date grid/level data, the clash heat map will be inaccurate.

> Compatible with Revit 2021 and 2022+ (handles the UnitUtils API change automatically).

---

### Sync and Close

**Purpose:** Saves and syncs the model to central, then closes it.

**When to use:**
- At the end of a work session
- Before handing a model off to another team member

**How to use:**
1. Click **Sync and Close**
2. Confirm the dialog prompt
3. The model syncs to central and closes automatically

> Requires confirmation before running. Do not use if you have unsaved work you want to discard — sync will commit all local changes.

---

## Tips

- Add **Export Grids** to your Wednesday morning checklist, before the 6 AM pipeline run
- If grid lines or levels were modified since the last export, re-run Export Grids and verify that `grid_lines.csv` and `level_elevations.csv` in the output folder have today's date
