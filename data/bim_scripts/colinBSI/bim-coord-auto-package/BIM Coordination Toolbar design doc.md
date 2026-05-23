
## Production Status

All 21 scripts built and deployed under `BIMTools.extension/`. See implementation plan:
`docs/plans/2026-03-07-pyrevit-toolbar.md`

| Panel | Scripts | Status |
|---|---|---|
| Project_Setup.panel | 6 tools | Built |
| Model_Health.panel | 6 tools | Built |
| Coordination.panel | 6 tools | Built |
| Reporting.panel | 2 tools | Built |
| Utilities.panel | 1 tool | Built |
| lib/ | bim_utils.py | Built |

---

Below is a complete design for a BIM Coordinator pyRevit Toolbar with 40 high-value tools. This structure is designed specifically for teams using:

  

- Revit
- Navisworks Manage
- AutoCAD / Plant 3D / CADWorx
- Civil 3D
- Autodesk Construction Cloud (ACC)

  

  

The goal is that 95% of coordination work can be executed from a single toolbar.

  

  

  

  

BIM Coordinator pyRevit Toolbar (40 Tools)

  

  

  

Toolbar Structure

  

BIM_COORDINATION

  

1_Project_Setup

2_Model_Health

3_Coordination

4_Model_Fixing

5_Sheets_and_Views

6_Links_and_Imports

7_Navisworks

8_Reporting

9_Utilities

  

  

  

  

1. Project Setup (6 Tools)

  

  

These tools automatically configure a project.

  

  

1. Initialize Project

  

  

Creates:

  

- worksets
- coordination views
- templates
- browser organization
- parameters

  

  

Purpose: full model setup in 2 minutes

  

  

  

  

2. Create Worksets

  

  

Creates standard worksets:

Shared Levels and Grids

Arch

Structure

Mechanical

Electrical

Plumbing

Civil

Plant

Links

Coordination

Scan









3. Load Shared Parameters

  

  

Loads your company shared parameter file and adds:

Clash_Status

Issue_ID

Issue_Status

Coordination_Zone

Discipline

Model_Author

> **Parameter naming note:** The parameters listed above (`BIM_Status`, `Clash_Status`, `Issue_ID`, `Issue_Status`, `Coordination_Zone`, `Model_Author`) are the **Phase 1–4 standard**.
>
> In Phase 5 (see `BIM compliance dashboard Requirements.md`), these are superseded by the `Portfolio_` parameter convention (`Portfolio_ProjectID`, `Portfolio_Discipline`, `Sheet_Status`, `View_Status`, `QA_Modelled`, etc.). Plan a migration when implementing Phase 5.









4. Setup Coordination Views

  

  

Automatically creates views:

3D - Coordination

3D - Navisworks

3D - Clash Review

3D - Worksets

3D - Linked Models

3D - QAQC

  

  

  

  

5. Create Standard Sheets

  

  

Creates baseline sheets:

G000 Cover

G001 General Notes

G100 Level Plans

G200 Sections

G300 Coordination

  

  

  

  

6. Setup Browser Organization

  

  

Automatically applies company browser organization rules.

  

  

  

  

2. Model Health (7 Tools)

  

  

These tools detect performance and coordination problems.

  

  

7. Model Health Check

  

  

Reports:

  

- warnings
- CAD imports
- groups
- model size
- family count

  

  

  

  

  

8. Warning Manager

  

  

Lists warnings by category:

duplicate marks

room separation issues

overlapping walls

  

  

  

  

9. Find Imported CAD

  

  

Highlights:

ImportInstance

Shows all CAD imports.

  

  

  

  

10. Find Large Families

  

  

Detects families larger than:

5 MB

  

  

  

  

11. Group Inspector

  

  

Shows:

Group count

Group types

Nested groups

  

  

  

  

12. Unplaced Views Finder

  

  

Lists views not placed on sheets.

  

  

  

  

13. Unused Families Cleaner

  

  

Finds unused families and types.

  

  

  

  

3. Coordination (6 Tools)

  

  

These tools support clash resolution workflows.

  

  

14. Create Clash Views

  

  

Automatically creates clash review views.

  

  

  

  

15. Color by Workset

  

  

Helps detect ownership conflicts.

  

  

  

  

16. Color by Discipline

  

  

Quick visual discipline identification.

  

  

  

  

17. Clash Status Manager

  

  

Allows coordinators to mark elements:

Open

In Progress

Resolved

  

  

  

  

18. Zone Checker

  

  

Verifies coordination zones.

  

  

  

  

19. Interference Check Launcher

  

  

Runs Revit interference checks.

  

  

  

  

4. Model Fixing Tools (6 Tools)

  

  

These tools repair common modeling mistakes.

  

  

20. Purge Unused

  

  

Runs purge operations.

  

  

  

  

21. Delete Imported CAD

  

  

Deletes all CAD imports.

  

  

  

  

22. Fix Line Styles

  

  

Standardizes line styles.

  

  

  

  

23. Convert CAD Layers to Revit Categories

  

  

Helps migrate CAD models.

  

  

  

  

24. Batch Pin Links

  

  

Pins all linked models.

  

  

  

  

25. Reset Element Overrides

  

  

Removes view overrides.

  

  

  

  

5. Sheets and Views (5 Tools)

  

  

Tools to manage documentation.

  

  

26. Duplicate Sheets

  

  

Batch duplicate sheets.

  

  

  

  

27. Copy Viewports to Sheets

  

  

Similar logic to the script you uploaded that copies viewports between sheets. 

  

  

  

  

28. View Template Manager

  

  

Apply templates to many views.

  

  

  

  

29. Sheet QAQC

  

  

Checks:

missing views

empty sheets

incorrect naming

  

  

  

  

30. Sheet Renumber

  

  

Renumbers sheets automatically.

  

  

  

  

6. Links and Imports (4 Tools)

  

  

Manage linked models.

  

  

31. Link Model

  

  

Automatically link models from ACC.
Also supports linking RCP point cloud files (placed on Scan workset as visual reference).









32. Reload All Links

  

  

Reloads all links in one click.

  

  

  

  

33. Find Unloaded Links

  

  

Detects broken links.

  

  

  

  

34. Move Links to Workset

  

  

Moves all links to:

Links Workset

  

  

  

  

7. Navisworks Tools (3 Tools)

  

  

Tools for exporting coordination models.

  

  

35. Export Navisworks

  

  

Exports using the correct coordination view.

  

File naming example:

PROJECT_DISCIPLINE_DATE.nwc

  

  

  

  

36. Batch Export NWC

  

  

Exports multiple models.

  

  

  

  

37. Create Navisworks View

  

  

Creates:

3D - Navisworks

with correct settings.

  

  

  

  

8. Reporting (2 Tools)

  

  

Tools for coordination reporting.

  

  

38. Generate Coordination Report

  

  

Creates report containing:

Model health

Clash metrics

Warnings

Issues

  

  

  

  

39. Clash Summary Report

  

  

Shows:

Open clashes

Resolved clashes

Clashes by discipline

  

  

  

  

9. Utilities (1 Tool)

  

  

  

10. Sync and Close

  

  

Automatically:

Synchronize

Relinquish

Save

Close

  

  

  

  

Recommended Toolbar Layout

  

BIM Coordination

  

Project Setup

Model Health

Coordination

Model Fixing

Sheets & Views

Links & Imports

Navisworks

Reporting

Utilities

  

  

  

  

Deployment Strategy

  

  

Deploy via company pyRevit extension.

  

Structure:

CompanyTools.extension

  

BIM_COORDINATION.tab

  

Project_Setup.panel

Model_Health.panel

Coordination.panel

Model_Fixing.panel

Sheets_Views.panel

Links.panel

Navisworks.panel

Reporting.panel

Utilities.panel

  

  

  

  

Estimated Impact on Your Team

  

  

Without automation:

Project setup = 3 hours

Model health review = 45 minutes

Clash prep = 30 minutes

With this toolbar:

Project setup = 3 minutes

Model health = 5 minutes

Clash prep = 5 minutes

  

  

  

  

Next Level (Highly Recommended)

  

  

To truly make your team elite, the next step is building:

  

  

1. Fully scripted 

Revit project initializer

  

  

Creates:

  

- views
- sheets
- parameters
- worksets
- links

  

  

automatically.

  

  

  

  

2. 

Navisworks clash automation

  

  

Automatically:

run clashes

group clashes

generate reports

  

  

  

  

3. 

ACC issue automation

  

  

Automatically convert clashes to ACC issues.

  

  

  

  

4. 

BIM Command Center dashboard

  

  

Shows:

Model health

Clash metrics

Issue tracking

Team performance

  

  

  

If you’d like, I can also build next:

  

1. Actual working pyRevit scripts for all 40 tools
2. A downloadable pyRevit extension folder structure
3. A Dynamo automation package for coordination
4. A Navisworks clash automation workflow
5. A BIM Command Center dashboard for executives

  

  

These combined are what top EPC firms and ENR contractors use internally to dominate BIM coordination.