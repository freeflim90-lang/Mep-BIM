
If your goal is to build one of the most advanced BIM coordination teams in the United States, the right approach is to implement a complete BIM Coordination System, not just scripts. Below is the full package organized into deployable components your team can roll out.

  

This will give you:

  

- Automated Revit project setup
- Automated model QA/QC
- Automated clash detection and grouping
- Automated issue tracking in ACC
- Performance dashboards
- A BIM coordinator automation toolbar
- Standardized workflows across all projects

  

  

  

  

  

Enterprise BIM Coordination System

  

  

  

System Architecture

  

Revit Models

      ↓

Automated Model Health Checks

      ↓

Navisworks Coordination Model

      ↓

Automated Clash Detection

      ↓

Automated Clash Grouping

      ↓

Automated Issue Creation (ACC)

      ↓

Performance Dashboards

Tools used:

  

- Revit
- Navisworks Manage
- Autodesk Construction Cloud
- Dynamo
- pyRevit
- Power BI or ACC Insight
- Autodesk ReCap (LiDAR Point Clouds — RCP/RCS/RCMR)

  

  

  

  

  

Part 1 — Revit Project Auto Setup System

  

  

Goal: Create a fully configured project in under 3 minutes

  

  

pyRevit Tool: Initialize Project

  

  

The script should automatically:

  

  

1. Create Worksets

  

  

Example standard:

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



2. Load Shared Parameters

  

  

Example:

BIM_Status

Clash_Status

Issue_ID

Issue_Status

Coordination_Zone

Discipline

Model_Author

> **Parameter naming note:** The parameters listed above (`BIM_Status`, `Clash_Status`, `Issue_ID`, `Issue_Status`, `Coordination_Zone`, `Model_Author`) are the **Phase 1–4 standard**.
>
> In Phase 5 (see `BIM compliance dashboard Requirements.md`), these are superseded by the `Portfolio_` parameter convention (`Portfolio_ProjectID`, `Portfolio_Discipline`, `Sheet_Status`, `View_Status`, `QA_Modelled`, etc.). Plan a migration when implementing Phase 5.



3. Create Standard Views

  

3D - Coordination

3D - Navisworks Export

3D - Clash Review

3D - Worksets

3D - Linked Models

3D - QAQC

  

4. Apply View Templates

  

  

Examples:

Coordination

Clash Review

Navisworks Export

QAQC

Presentation

  

5. Setup Browser Organization

  

  

Organize by:

Discipline

View Type

Coordination

  

6. Link Models Automatically

  

  

Script scans the ACC Shared folder and links:

Architectural model

Structural model

Civil model

Plant model

CAD references

All placed on:

Links Workset

  

  

  

  

Part 2 — Automated Model Health Checks

  

  

Run automatically before coordination meetings.

  

  

Model Health Checks

  

  

  

Warning Count

  

  

Threshold:

Target < 300 warnings

  

Imported CAD

  

  

Find:

ImportInstance

Flag models with:

>5 CAD imports

  

Large Families

  

  

Flag families larger than:

5 MB

  

Groups

  

  

Flag models with:

>50 groups

  

Unplaced Views

  

  

Clean unused views.

  

  

  

  

Part 3 — Automated Clash Detection

  

  

Navisworks template (.NWF) should include:

  

  

Clash Tests

  

Arch vs Structure

Structure vs Mechanical

Structure vs Electrical

Mechanical vs Electrical

Mechanical vs Plumbing

Plant vs Structure

Civil vs Structure

Tolerance:

0.25 inches

  

  

  

  

Part 4 — Automated Clash Grouping

  

  

Goal: Reduce thousands of clashes into actionable issues.

  

Example grouping rules:

  

  

Group by Grid + Level

  

Grid A–B

Level 2

  

Group by System

  

  

Example:

Duct vs Beam

Pipe vs Column

Cable Tray vs Wall

  

Result

  

2,500 raw clashes

↓

120 grouped issues

  

  

  

  

Part 5 — Automated Issue Creation (ACC)

  

  

When clashes are grouped, automatically create issues.

  

Fields:

Title

Description

Location

Discipline

Assigned company

Due date

Screenshot

Example issue:

Mechanical duct clashes with structural beam at Grid B3 Level 4

Assigned to:

Mechanical contractor

  

  

  

  

Part 6 — Automated Coordination Reports

  

  

Automatically generate weekly reports.

  

Example report sections:

  

  

Model Health

  

Model size

Warnings

CAD imports

Groups

  

Clash Summary

  

Total clashes

Grouped clashes

Open issues

Resolved issues

  

Discipline Status

  

Architecture

Structure

Mechanical

Electrical

Plumbing

Civil

Plant

  

  

  

  

Part 7 — BIM Performance Dashboard

  

  

Your leadership should see metrics like:

  

  

Model Health

  

Warnings

Model size

Load time

Family count

  

Coordination Progress

  

Clashes resolved per week

Open issues

Average resolution time

  

Discipline Performance

  

Issues by discipline

Issues resolved

Coordination compliance

  

  

  

  

Part 8 — BIM Coordinator Automation Toolbar

  

  

Using pyRevit.

  

Example layout:

BIM Coordination Toolbar

  

Project Setup

Initialize Project

Create Worksets

Setup Views

Load Shared Parameters

  

Model Health

Run Model Health Check

Find CAD Imports

Find Groups

Warning Report

  

Coordination

Export Navisworks

Create Clash Views

Sync Audit

  

Reporting

Generate Coordination Report

Publish Clash Report

Open Issue Dashboard

  

  

  

  

Part 9 — Automated Navisworks Export

  

  

One-button export.

  

Script ensures:

Correct export view

Correct coordinates

Correct file naming

Correct folder location

Example naming:

PROJECT_DISCIPLINE_DATE.nwc

Example:

Plant_AreaA_MEP_2026-03-07.nwc

  

  

  

  

Part 10 — ACC Coordination Workflow

  

  

Standard workflow:

Model Upload

↓

Automated Model Check

↓

Navisworks Clash Run

↓

Clash Grouping

↓

Issue Creation

↓

Issue Assignment

↓

Resolution

↓

Verification

  

  

  

  

Part 11 — Weekly Coordination Meeting Structure

  

  

Top BIM teams follow a strict format.

  

  

Meeting Agenda

  

  

1. Model health review
2. New clash review
3. Issue resolution updates
4. Critical coordination areas
5. Schedule impact

  

  

  

  

  

Part 12 — BIM Standards Manual

  

  

Your team should maintain a manual covering:

  

  

Modeling Standards

  

Levels

Coordinates

Families

Worksets

Naming

  

Coordination Standards

  

Clash tolerance

Issue workflow

Meeting schedule

LOD expectations

  

  

  

  

Part 13 — Training System for Your Team

  

  

Create two tracks:

  

  

BIM Coordinator 101

  

  

Topics:

Revit coordination views

Navisworks basics

ACC issues

Clash detection

Model QAQC

  

Advanced BIM Coordinator

  

  

Topics:

Clash automation

Model debugging

Revit performance optimization

Advanced Navisworks workflows

API automation

  

  

  

  

Part 14 — Ideal BIM Team Structure

  

  

For large projects:

BIM Manager

Senior BIM Coordinator

Discipline Coordinators

Model Health Specialist

Automation Developer

  

  

  

  

Part 15 — Automation Roadmap

  

  

Phase implementation.

  

  

Phase 1

  

Standard templates

Navisworks template

Coordination workflow

  

Phase 2

  

pyRevit automation

Model health checks

Navisworks export automation

  

Phase 3

  

Clash grouping automation

ACC issue automation

  

Phase 4

  

Performance dashboards

AI model analytics

Predictive coordination

  

  

  

  

If you’d like, I can also build for you next:

  

  

1. A complete pyRevit BIM Coordinator toolbar (30–40 tools)
2. A Revit Auto Project Setup Script
3. A Navisworks Clash Automation Script
4. An ACC Issue Automation System
5. A BIM Command Center Dashboard
6. A BIM Coordinator Certification Program for your company

  

  

Those combined are what firms like large ENR contractors and major EPC firms build internally to dominate BIM coordination.

  

If you’d like, I can also design a “BIM Command Center” system that would realistically put your team in the top 1% of BIM teams in the U.S.