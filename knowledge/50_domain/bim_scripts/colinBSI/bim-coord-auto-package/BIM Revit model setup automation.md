Automating Revit model setup is one of the highest-ROI automations a BIM team can implement. The goal is that a coordinator clicks one button and a fully configured project is created in 2–3 minutes with:

  

- Correct worksets
- Linked models
- Project coordinates
- View templates
- Sheets
- Filters
- Shared parameters
- Browser organization
- Standard views
- Model health settings

  

  

Below is a complete enterprise workflow used by top BIM teams.

  

  

  

  

Automated Revit Model Setup Framework

  

  

  

Overview of the Automation Stack

  

  

A high-performing BIM team typically uses:

|   |   |
|---|---|
|Tool|Role|
|Revit Template (.RTE)|Base project configuration|
|pyRevit scripts|Model setup automation|
|Dynamo scripts|Parameter and bulk configuration|
|ACC templates|Folder + permission structure|
|Navisworks template (.NWF)|Preconfigured clash environment|

Goal:

New Project

     ↓

Coordinator clicks "Initialize Project"

     ↓

Automation scripts run

     ↓

Model ready for production in <5 minutes

  

  

  

  

Step 1 — Build a Strong Revit Template (Foundation)

  

  

Your .RTE template must contain 70–80% of the setup already.

  

Include:

  

  

Worksets

  

  

Example worksets:

Shared Levels and Grids

Arch

Structure

Mechanical

Electrical

Plumbing

Civil

Links

Coordination

Scan



Standard Views

  

  

Create:

3D - Coordination

3D - Navisworks

3D - Clash Detection

3D - Worksets

3D - Linked Models

  

View Templates

  

  

Examples:

Coordination

Navisworks Export

Clash Review

Issue Tracking

Presentation

  

Filters

  

  

Examples:

Unplaced Elements

Oversized Elements

Interference Check

Clash Status

Coordination Review

  

Shared Parameters

  

  

Add:

BIM_Status

Clash_Status

Issue_ID

Issue_Status

Discipline

Zone

Level_Code

> **Parameter naming note:** The parameters listed above (`BIM_Status`, `Clash_Status`, `Issue_ID`, `Issue_Status`, `Coordination_Zone`, `Model_Author`) are the **Phase 1–4 standard**.
>
> In Phase 5 (see `BIM compliance dashboard Requirements.md`), these are superseded by the `Portfolio_` parameter convention (`Portfolio_ProjectID`, `Portfolio_Discipline`, `Sheet_Status`, `View_Status`, `QA_Modelled`, etc.). Plan a migration when implementing Phase 5.









Step 2 — Create a “Project Initialization Script”

  

  

Using pyRevit, build a button called:

Initialize Project

The script should automatically:

1 Create worksets

2 Load shared parameters

3 Load view templates

4 Create coordination views

5 Set project coordinates

6 Link models

7 Create sheets

8 Apply browser organization

9 Configure worksharing

10 Set export settings

  

  

  

  

Step 3 — Automated Workset Creation

  

  

Example pyRevit / Revit API workflow:

DB.Workset.Create(doc, "Arch")

DB.Workset.Create(doc, "Structure")

DB.Workset.Create(doc, "Mechanical")

DB.Workset.Create(doc, "Electrical")

DB.Workset.Create(doc, "Plumbing")

DB.Workset.Create(doc, "Civil")

DB.Workset.Create(doc, "Links")

DB.Workset.Create(doc, "Coordination")

The script should:

  

1 Check if worksets exist

2 Create missing worksets

  

  

  

  

Step 4 — Automatic Model Linking

  

  

The script can automatically link:

Architectural model

Structural model

Civil model

Plant model

CAD backgrounds

LiDAR point cloud scans (RCP/RCS) — place on Scan workset, visual reference only

Example workflow:

Collect files from ACC folder

Link models automatically

Assign to Links workset

Set positioning to Shared Coordinates

Pin links

  

  

  

  

Step 5 — Automatic View Creation

  

  

Your script should generate standard views.

  

Examples:

3D - Coordination

3D - Navisworks

3D - Clash

3D - Worksets

3D - Scan Reference

Typical automation steps:

Create 3D View

Apply view template

Rename view

Set discipline

Apply section box

  

  

  

  

Step 6 — Automated Navisworks Export View

  

  

Create a dedicated view:

3D - Navisworks

Settings:

Detail Level: Medium

Parts Visibility: Show Parts

Worksets: Visible

Linked Files: Visible

Filters: Coordination filters

Automation ensures:

Everyone exports the same view

Consistent clash results

  

  

  

  

Step 7 — Automated Sheet Creation

  

  

Your script should create baseline sheets:

  

Example:

G000 Cover Sheet

G001 General Notes

G100 Level Plans

G200 Sections

G300 3D Coordination

Workflow:

Load titleblock

Create sheets

Assign parameters

Apply sheet organization

  

  

  

  

Step 8 — Browser Organization Automation

  

  

Automate view sorting:

Discipline

  ├ Architecture

  ├ Structure

  ├ Mechanical

  ├ Electrical

  └ Plumbing

  

Coordination

  ├ Clash Views

  ├ Navisworks

  ├ QAQC

Using parameter:

View_Subcategory

Automation sets values automatically.

  

  

  

  

Step 9 — Automatic Model Health Setup

  

  

Add model check views:

3D - Warnings

3D - Groups

3D - Imported CAD

3D - Oversized Elements

This lets coordinators detect problems instantly.

  

  

  

  

Step 10 — Automatic Shared Coordinates Setup

  

  

Script workflow:

Link survey model

Acquire coordinates

Publish coordinates to other links

Pin survey point

Pin base point

This prevents 95% of coordination alignment issues.

  

  

  

  

Step 11 — Automatic Parameter Setup

  

  

Your automation should load:

Shared parameters file

Project parameters

Global parameters

Common ones:

Issue_ID

Issue_Status

Clash_Status

Coordination_Zone

BIM_Phase

> **Parameter naming note:** The parameters listed above (`BIM_Status`, `Clash_Status`, `Issue_ID`, `Issue_Status`, `Coordination_Zone`, `Model_Author`) are the **Phase 1–4 standard**.
>
> In Phase 5 (see `BIM compliance dashboard Requirements.md`), these are superseded by the `Portfolio_` parameter convention (`Portfolio_ProjectID`, `Portfolio_Discipline`, `Sheet_Status`, `View_Status`, `QA_Modelled`, etc.). Plan a migration when implementing Phase 5.









Step 12 — Automatic Model Health Dashboard

  

  

Create schedules:

Warnings

Imported CAD files

Unplaced views

Large families

Groups

These power model health metrics.

  

  

  

  

Step 13 — ACC Integration Automation

  

  

Automate folder setup:

/01_WIP

/02_Shared

/03_Published

/04_Archive

/05_Coordination

Also automate:

Permissions

Naming standards

Issue workflows

  

  

  

  

Step 14 — One Button Workflow

  

  

Your coordinator runs:

pyRevit → Initialize Project

Script executes:

Create worksets

Load parameters

Create views

Create sheets

Link models

Set coordinates

Apply templates

Generate dashboards

Time saved:

Manual setup: 3–4 hours

Automated setup: 3 minutes

  

  

  

  

Step 15 — Add a “QAQC Model Check” Button

  

  

Second button:

Run Model Health Check

Runs checks for:

Warnings

Unpinned links

CAD imports

Large families

Groups

Duplicate types

  

  

  

  

Example BIM Coordinator Toolbar

  

  

Your pyRevit toolbar could look like:

BIM Coordination

  

Project Setup

 ├ Initialize Project

 ├ Create Worksets

 ├ Load Parameters

 ├ Setup Views

  

Model Health

 ├ Model Health Check

 ├ Find Imported CAD

 ├ Find Groups

 ├ Warning Report

  

Coordination

 ├ Export Navisworks

 ├ Create Clash Views

 ├ Publish Models

  

  

  

  

Recommended Automation Tools

  

  

For the strongest BIM automation stack:

  

  

pyRevit

  

  

Best for:

UI buttons

Project automation

Batch tools

  

Dynamo

  

  

Best for:

Parameter management

Bulk edits

Data analysis

  

Navisworks API

  

  

Best for:

Clash automation

Grouping clashes

Reporting

  

ACC API

  

  

Best for:

Issue creation

Model tracking

Automation

  

  

  

  

What Elite BIM Teams Automate

  

  

Top BIM teams automate:

Project setup

Revit QAQC

Clash grouping

Clash reporting

Issue creation

Model health dashboards

Sheet creation

Navisworks export

  

  

  

  

If you’d like, I can also build these for you:

  

  

  

1. A 

full pyRevit BIM Coordinator Toolbar

  

  

30+ automation tools.

  

  

2. A 

Revit Auto Setup Script

  

  

Creates entire project environment automatically.

  

  

3. A 

Navisworks Clash Automation System

  

  

Automatically:

Run clashes

Group clashes

Assign issues

Publish reports

  

4. A 

BIM Command Center Dashboard

  

  

Your team sees:

Model health

Clash counts

Open issues

Performance metrics

  

5. A 

complete BIM Coordinator Automation Package

  

  

(What top ENR firms use internally)

  

If you’d like, I can build a complete “BIM Coordinator Automation Playbook” that could realistically make your team one of the most advanced BIM teams in the US.