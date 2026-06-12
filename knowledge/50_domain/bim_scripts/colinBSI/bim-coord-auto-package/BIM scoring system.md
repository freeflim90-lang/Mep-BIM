Below is a production-grade 150-Point Revit Model Health Scoring System designed for BIM Coordinators and VDC teams.


The goal is to convert model quality into a measurable score (0–150) so teams can instantly see whether a model is:

  

- Excellent (120–150)
- Healthy (100–119)
- Needs Cleanup (80–99)
- Critical (<80)

  

  

This system works extremely well when paired with pyRevit automation and Power BI dashboards.

  

  

  

  

150-Point Revit Model Health Scoring System

  

  

  

Category Overview

  

|   |   |
|---|---|
|Category|Points|
|Model Warnings|25|
|Model Size & Performance|20|
|CAD & External Content|20|
|Families & Modeling Practices|25|
|Views & Documentation|15|
|Worksets & Links|15|
|Clash & Coordination Readiness|15|
|Automation & Data Standards|15|

Total Possible Score:

150 points

  

  

  

  

1 Model Warnings (25 Points)

  

  

Warnings significantly slow models and indicate modeling problems.

|   |   |
|---|---|
|Warning Count|Score|
|0–100|25|
|100–500|20|
|500–1000|15|
|1000–2000|10|
|2000–5000|5|

5000 | 0 |

  

Additional penalty:

−5 points if critical warnings exist

Examples:

  

- duplicate instances
- room separation issues
- overlapping elements

  

  

  

  

  

2 Model Size & Performance (20 Points)

  

  

Large models degrade coordination performance.

|   |   |
|---|---|
|File Size|Score|
|<300 MB|20|
|300–500 MB|15|
|500–800 MB|10|
|800 MB–1 GB|5|

1 GB | 0 |

  

Additional checks:

|   |   |
|---|---|
|Metric|Points|
|Purgeable elements low|+3|
|Compact central model|+2|

  

  

  

  

3 CAD & External Content (20 Points)

  

  

Imported CAD is one of the biggest model performance killers.

|   |   |
|---|---|
|Condition|Score|
|No imported CAD|10|
|1–3 CAD imports|7|
|4–10 CAD imports|3|

10 imports | 0 |

  

CAD links instead of imports:

+5 points

Correct origin placement:

+5 points

  

  

  

  

4 Families & Modeling Practices (25 Points)

  

  

Bad family practices destroy model performance.

|   |   |
|---|---|
|Metric|Score|
|No in-place families|10|
|1–3 in-place families|5|

3 in-place families | 0 |

  

Nested family optimization:

+5 points

Proper family categories:

+5 points

Unused families purged:

+5 points

  

  

  

  

5 Views & Documentation (15 Points)

  

  

Excessive views create file bloat.

|   |   |
|---|---|
|View Count|Score|
|<300 views|10|
|300–600 views|7|
|600–900 views|4|

900 views | 0 |

  

View templates applied:

+5 points

  

  

  

  

6 Worksets & Links (15 Points)

  

  

Proper worksharing is essential.

|   |   |
|---|---|
|Condition|Score|
|Logical worksets|5|
|Linked models properly attached|5|
|Unused worksets removed|5|

Bad practice penalty:

−5 if >25 worksets

  

  

  

  

7 Clash & Coordination Readiness (15 Points)

  

  

The model must be coordination-ready.

|   |   |
|---|---|
|Check|Points|
|Correct project base point|5|
|Shared coordinates established|5|
|Levels correctly named|5|

  

  

  

  

8 Automation & Data Standards (15 Points)

  

  

High-performing BIM teams enforce standards.

|   |   |
|---|---|
|Condition|Points|
|Naming standards followed|5|
|Parameter standards enforced|5|
|Model health automation enabled|5|

  

  

  

  

Model Health Score Interpretation

  

|   |   |
|---|---|
|Score|Status|
|130–150|Elite Model|
|115–129|Excellent|
|100–114|Healthy|
|85–99|Needs Cleanup|
|<85|Critical Model|

  

  

  

  

Example Model Score

  

  

Mechanical model example:

|   |   |
|---|---|
|Category|Score|
|Warnings|15|
|Model Size|10|
|CAD Imports|5|
|Families|18|
|Views|10|
|Worksets|12|
|Coordination Readiness|10|
|Standards|12|

Total:

92 / 150

Status:

Needs Cleanup

  

  

  

  

Automated Scoring Workflow

  

  

This system becomes powerful when automated.

  

  

Step 1 — Run Model Health Script

  

  

pyRevit script collects:

warnings

view count

imported CAD

family counts

file size

worksets

  

  

  

  

Step 2 — Calculate Score

  

  

Python or Dynamo script calculates:

Model Health Score

  

  

  

  

Step 3 — Export Data

  

  

Export results to:

CSV

ACC folder

SharePoint

  

  

  

  

Step 4 — Power BI Dashboard

  

  

Dashboard displays:

Model health scores

Health trends

Problem models

  

  

  

  

Command Center Example

  

|   |   |   |
|---|---|---|
|Model|Health Score|Status|
|Architecture|132|Elite|
|Structure|125|Excellent|
|Mechanical|92|Cleanup Needed|
|Electrical|105|Healthy|

  

  

  

  

Weekly BIM Coordinator Workflow

  

  

Monday

Run automated model health scan

Tuesday

Notify teams below 100 score

Wednesday

Teams fix issues

Thursday

Run clash coordination

Friday

Update command center dashboard

  

  

  

  

What Top BIM Teams Do

  

  

Elite VDC teams enforce minimum model health scores.

  

Typical requirement:

No model below 100 allowed in coordination

This prevents:

  

- bloated models
- broken coordinates
- poor modeling practices

  

  

before they affect construction.

  

  

  

If you’d like, I can also create the full automation package for this system, including:

  

1. A pyRevit 150-Point Model Health Auto-Scoring Script
2. A Dynamo version that works across multiple models
3. A Power BI template that automatically scores every model

  

  

Those three tools will turn this scoring system into a fully automated BIM quality control engine.