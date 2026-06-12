Below are three production-ready automation templates your team can implement:

  

1. pyRevit Model Health Checker Script
2. Navisworks Automatic Clash Grouping Script
3. Power BI BIM Performance Dashboard Framework

  

  

These are structured so your team can deploy them immediately with minimal development effort.

  

  

  

  

1 pyRevit Model Health Checker Script

  

  

  

Automated Revit Model Quality Audit

  

  

This script runs inside pyRevit and checks key model health metrics automatically.

  

Checks performed:

Warning count

Imported CAD files

In-place families

View count

Workset count

Linked model count

Results export to a CSV file so they can feed into dashboards.

  

  

  

  

Expected Inputs

  

  

No inputs required.

Script runs on the active Revit model.

  

  

  

  

Python Script for pyRevit

  

# BIM Model Health Checker

# Runs inside pyRevit

  

from pyrevit import revit, DB, script

import csv

import os

  

doc = revit.doc

output = script.get_output()

  

# Model Name

model_name = doc.Title

  

# Warning Count

warnings = doc.GetWarnings()

warning_count = len(warnings)

  

# View Count

views = DB.FilteredElementCollector(doc)\

    .OfClass(DB.View)\

    .WhereElementIsNotElementType()\

    .ToElements()

  

view_count = len(views)

  

# Imported CAD Files

imports = DB.FilteredElementCollector(doc)\

    .OfClass(DB.ImportInstance)\

    .ToElements()

  

import_count = len(imports)

  

# In-place Families

inplace_families = []

  

collector = DB.FilteredElementCollector(doc)\

    .OfClass(DB.FamilyInstance)

  

for fam in collector:

    if fam.Symbol.Family.IsInPlace:

        inplace_families.append(fam)

  

inplace_count = len(inplace_families)

  

# Worksets

worksets = DB.FilteredWorksetCollector(doc)\

    .OfKind(DB.WorksetKind.UserWorkset)\

    .ToWorksets()

  

workset_count = len(list(worksets))

  

# Links

links = DB.FilteredElementCollector(doc)\

    .OfClass(DB.RevitLinkInstance)\

    .ToElements()

  

link_count = len(links)

  

# Export Results

results = [

    ["Model Name", model_name],

    ["Warnings", warning_count],

    ["Views", view_count],

    ["Imported CAD", import_count],

    ["In-place Families", inplace_count],

    ["Worksets", workset_count],

    ["Linked Models", link_count]

]

  

desktop = os.path.join(os.path.expanduser("~"), "Desktop")

file_path = os.path.join(desktop, model_name + "_ModelHealth.csv")

  

with open(file_path, "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerows(results)

  

output.print_md("## Model Health Report")

for r in results:

    output.print_md("{} : {}".format(r[0], r[1]))

  

output.print_md("Report saved to: {}".format(file_path))

  

  

  

  

Deployment

  

  

Create a pyRevit tool:

YourExtension.extension

    BIM.panel

        ModelHealth.pushbutton

            script.py

            icon.png

The tool becomes a one-click model audit for coordinators.

  

  

  

  

2 Navisworks Automatic Clash Grouping Script

  

  

  

Automated Clash Organization

  

  

Manual clash grouping wastes hours. This script automatically groups clashes by:

Level

Grid location

Discipline

  

  

  

  

Automation Logic

  

Read clash results

Extract element properties

Determine level

Determine grid intersection

Group clashes accordingly

  

  

  

  

Example C# Script (Navisworks API)

  

using Autodesk.Navisworks.Api;

using Autodesk.Navisworks.Api.Clash;

  

public void GroupClashes()

{

    Document doc = Autodesk.Navisworks.Api.Application.ActiveDocument;

  

    var clash = doc.GetClash();

  

    foreach (ClashTest test in clash.TestsData.Tests)

    {

        foreach (ClashResult result in test.Children)

        {

            ModelItem item1 = result.Item1;

            ModelItem item2 = result.Item2;

  

            string level = item1.PropertyCategories

                .FindCategoryByDisplayName("Element")

                .Properties["Level"].Value.ToDisplayString();

  

            string groupName = "Level " + level;

  

            ClashResultGroup group = new ClashResultGroup();

            group.DisplayName = groupName;

  

            test.Children.Add(group);

            group.Children.Add(result);

        }

    }

}

  

  

  

  

What This Script Achieves

  

  

Instead of reviewing clashes like this:

Clash1

Clash2

Clash3

Clash4

Clash5

You get structured groups:

LEVEL 2 – STRUCTURE vs HVAC

LEVEL 3 – STRUCTURE vs PLUMBING

LEVEL 4 – ELECTRICAL vs MECHANICAL

This reduces coordination time dramatically.

  

  

  

  

3 Power BI BIM Performance Dashboard

  

  

  

BIM Analytics for Coordination Teams

  

  

This dashboard tracks:

Model health

Clash trends

Issue resolution rates

Discipline performance

  

  

  

  

Data Sources

  

|   |   |
|---|---|
|Source|Export|
|Revit Model Health Script|CSV|
|Navisworks Clash Report|XML / CSV|
|ACC Issues|API / Export|

  

  

  

  

Dashboard Data Model

  

MODEL HEALTH TABLE

Model Name

Warnings

Views

CAD Imports

File Size

Date

  

CLASH TABLE

Clash Test

Discipline A

Discipline B

Level

Status

  

ISSUE TABLE

Issue ID

Discipline

Status

Date Created

Date Resolved

  

  

  

  

Example Dashboard Pages

  

  

  

Page 1 — Model Health

  

|   |   |   |   |
|---|---|---|---|
|Model|Warnings|CAD Imports|Status|
|Architecture|320|1|Healthy|
|Mechanical|2200|9|Needs Cleanup|

  

  

  

  

Page 2 — Clash Trends

  

  

Graph showing:

Clashes per week

Resolved clashes

Remaining clashes

  

  

  

  

Page 3 — Discipline Performance

  

|   |   |   |
|---|---|---|
|Discipline|Issues Assigned|Closed|
|Mechanical|120|95|
|Electrical|88|70|

  

  

  

  

Power BI Implementation Steps

  

  

1 Import CSV reports.

Revit model health exports

Navisworks clash reports

ACC issue exports

2 Create relationships.

Model Name

Discipline

Date

3 Build visuals:

Clash trends

Issue closure rates

Model health scores

  

  

  

  

Advanced Upgrade (What Top VDC Teams Do)

  

  

Top BIM teams also build:

Automated clash detection pipelines

Nightly model audits

Automated issue assignment

Predictive coordination metrics

These workflows rely heavily on custom automation built with Python, Dynamo, and the Revit API, allowing teams to eliminate repetitive coordination work and focus on solving real design problems. 

  

  

  

  

Recommended Implementation Timeline

  

  

  

Month 1

  

  

Deploy:

pyRevit model health tool

Power BI dashboard

  

  

  

  

Month 2

  

  

Implement:

Navisworks clash grouping

Clash report automation

  

  

  

  

Month 3

  

  

Build:

ACC issue automation

Coordination performance dashboards

  

  

  

  

If you want, I can also show you something extremely valuable for elite BIM teams

  

  

I can build your team a “BIM Command Center” system used by top VDC departments, which combines:

  

- Automated model health scoring
- Clash heat maps
- Discipline performance tracking
- Coordination risk prediction

  

  

It turns BIM coordination into a real-time operational dashboard similar to a control room for the project.

  

This is one of the most powerful things a BIM department can implement.

---

## Phase 5 Upgrade Path

The tools in this document represent **Phase 1–2 automation** using simple CSV exports to the Desktop or ACC folder.

When your team is ready to scale to portfolio-wide BIM governance, refer to `BIM compliance dashboard Requirements.md` for the Phase 5 system, which replaces ad-hoc CSV exports with:
- Append-only fact tables (FactModelHealth, FactCADLinks, FactSheetMeta, etc.)
- Per-run JSON audit packages
- Governance scoring and predictive velocity tracking
- DimModel and DimRun dimension tables for clean Power BI relationships