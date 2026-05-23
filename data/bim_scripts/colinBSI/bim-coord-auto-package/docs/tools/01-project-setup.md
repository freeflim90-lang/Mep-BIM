# Project Setup Panel

The Project Setup panel initializes a new Revit model with standard worksets, shared parameters, views, and sheets. Run these tools once at project start on each Revit model.

> All setup tools are **idempotent** — running them a second time skips items that already exist.

---

## Tools

### Initialize Project

**Purpose:** Master setup runner. Runs all other Project Setup tools in sequence.

**When to use:** Once at the start of a new project, on each discipline model.

**How to use:**
1. Open the Revit model (must be a workshared model)
2. Click **Initialize Project**
3. Confirm the dialog prompt
4. Wait for completion — check the pyRevit console for a summary

**What it does:**
1. Creates standard worksets
2. Loads coordination shared parameters
3. Creates standard 3D views
4. Creates standard sheets
5. Applies browser organization

> Requires confirmation before running. Takes 10–30 seconds depending on model size.

---

### Create Worksets

**Purpose:** Creates 11 standard worksets for discipline ownership and link management.

**When to use:** On any new workshared model before linking files.

**How to use:**
1. Click **Create Worksets**
2. Check pyRevit console for skipped (already exist) vs. created worksets

**Worksets created:**

| Workset | Purpose |
|---|---|
| Shared Levels & Grids | Levels and grids (all disciplines) |
| Arch | Architectural elements |
| Structure | Structural elements |
| Mechanical | HVAC elements |
| Electrical | Electrical elements |
| Plumbing | Plumbing elements |
| Civil | Civil/site elements |
| Plant | Equipment |
| Links | All linked Revit files |
| Coordination | Clash review elements |
| Scan | Point cloud files (RCP/RCS) |

---

### Load Shared Parameters

**Purpose:** Loads 6 coordination shared parameters into the model, bound to the Project Information category.

**When to use:** After worksets are created, before coordination begins.

**How to use:**
1. Click **Load Shared Parameters**
2. Check pyRevit console for confirmation

**Parameters loaded:**

| Parameter | Use |
|---|---|
| Clash_Status | Track clash resolution: Open / In Progress / Resolved |
| Issue_ID | ACC issue reference number |
| Issue_Status | ACC issue status |
| Coordination_Zone | Zone designation for clash grouping |
| Discipline | Discipline classification |
| Model_Author | Who owns this model |

---

### Setup Views

**Purpose:** Creates 7 standard 3D views for coordination and quality control.

**When to use:** After worksets are created.

**How to use:**
1. Click **Setup Views**
2. Views appear in the Project Browser under 3D Views

**Views created:**

| View Name | Purpose |
|---|---|
| 3D-Coordination | General coordination review |
| 3D-Navisworks | Export to Navisworks (NWC) |
| 3D-Clash Review | Active clash review sessions |
| 3D-Worksets | Color by workset visibility checks |
| 3D-Linked Models | All links visible |
| 3D-QAQC | Quality control review |
| 3D-Scan Reference | Point cloud overlay |

---

### Create Sheets

**Purpose:** Creates 5 baseline coordination sheets.

**When to use:** At project start for documentation structure.

**How to use:**
1. Click **Create Sheets**
2. Sheets appear in the Project Browser

**Sheets created:**

| Number | Name |
|---|---|
| G000 | Cover |
| G001 | General Notes |
| G100 | Level Plans |
| G200 | Sections |
| G300 | Coordination |

---

### Browser Organization

**Purpose:** Applies standard browser organization rules based on Discipline or Type parameters.

**When to use:** After views and sheets are created; or when browser organization looks disorganized.

**How to use:**
1. Click **Browser Org**
2. If a matching organization scheme is found (discipline- or type-based), it is applied automatically

---

## Tips

- Run **Initialize Project** instead of each tool individually when setting up a new model from scratch
- If a workset or view already exists with the correct name, the tool skips it — no duplicates are created
- Check the pyRevit console (pyRevit tab → Console) for a detailed log of what was created vs. skipped
