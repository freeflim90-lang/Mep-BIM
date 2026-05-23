# BIM Portfolio Governance Exporter — Phase 5 (Advanced Tier)

> **Phase context:** This document describes the most advanced layer of the BIM Coordination Automation Package. It is intended for implementation **after** Phases 1–4 are operational (see `BIM Coordination Package - Index.md`).
>
> This system supersedes the simpler CSV export approach used in the Phase 1–4 tools. The data model defined here (append-only fact tables, DimModel, DimRun, Portfolio_ shared parameters) is the authoritative long-term standard for BIM portfolio intelligence.
>
> **Prerequisites before implementing this phase:**
> - pyRevit BIM Coordinator Toolbar deployed (Phase 2)
> - Model health scoring automated (Phase 3)
> - Clash automation and ACC issue creation operational (Phase 3–4)
> - Power BI Command Center dashboard live (Phase 4)

---

 # Master scope including:
 * Sheet completion
 * View placement tracking
 * FactViewMeta / FactViewPlacement tables
 * Updated shared parameter standard
 * Governance + Predictive alignment
 * Final exporter table list (complete and production-ready)

## COMPLETE DATA ARCHITECTURE (FINAL)
Append-Only CSV Fact Tables
 * FactModelHealth
 * FactModelCoordSignature
 * FactHostLinkPlacement
 * FactCADLinks
 * FactSheetMeta
 * FactSheetRevisions
 * FactViewMeta
 * FactViewPlacement (optional but recommended)
Each table includes:
 * RunId
 * RunDateTime
 * RevitVersion
 * ModelTitle
 * Portfolio_ProjectID
 * Portfolio_ProjectName
 * Portfolio_Discipline
JSON per run will mirror all of this plus detailed arrays.
1. FactModelHealth (unchanged)
## Model stability & performance risk indicators.
Key fields:
 * WarningsTotal
 * CADImportsCount
 * CADLinksCount
 * InPlaceCount
 * GroupsTotalInstances
 * GroupTypesSingleInstance
 * UnplacedViewsCount
 * ModelFileSizeMB (if retrievable)
 * LinkCount
 * DetailItemCount (optional)
 * DirectShapeCount (optional)
Used for:
 * Governance scoring
 * Performance risk
 * Growth velocity
2. FactModelCoordSignature
Per model per run:
 * Shared_EW / NS / Elev
 * Shared_Angle
 * PBP coords
 * Survey coords
 * Tolerance used
 * Coord_BaselineRole flag
Used for:
 * Cross-model coordinate mismatch
 * Drift tracking
 * Coordination risk
3. FactHostLinkPlacement
## Per host model x link instance:
 * LinkModelTitle
 * LinkInstanceId
 * OriginX/Y/Z
 * RotationAboutZ
 * Basis vectors
 * IsPinned
 * WorksetName (optional)
Used for:
 * Link movement detection
 * Rotation drift
 * Host coordination governance
4. FactCADLinks
## Per CAD link instance:
 * CADFileName
 * CADFilePath
 * CADFileSize_MB
 * CADLastModified
 * IsLinked
 * IsImported
 * HostView (optional)
 * WorksetName (optional)
## Governance rules:
 * Imported CAD = Fail
 * CAD > size threshold = Warn
 * Old CAD file = Warn
 * Missing path = Fail
5. FactSheetMeta (UPDATED)
One row per sheet per run.
## Core Metadata
 * SheetId
 * SheetNumber
 * SheetName
 * IsPlaceholder
## Governance
 * Sheet_Status
 * Sheet_TargetPackage
 * Sheet_RequiredOnIssue
## Completion Indicators
 * HasTitleBlock (Y/N)
 * PlacedViewportCount
 * PlacedScheduleCount
 * DistinctPlacedViewCount
 * HasAnyViewsPlaced (Y/N)
 * RevisionCount
 * SheetCompletionScore (optional computed field)
## Authoring Metadata
 * DrawnBy
 * DesignedBy
 * CheckedBy
 * ApprovedBy
## Governance checks:
 * Missing checker/approver
 * Issued without revisions
 * Sheet with zero placed views
 * Sheet with no title block
## Predictive:
 * Sheet placement velocity
 * Issuance velocity
 * Author compliance trend
6. FactSheetRevisions
## Per sheet x revision:
 * SheetNumber
 * RevisionId
 * RevisionNumberOnSheet
 * RevisionSequence
 * RevisionDate
 * RevisionDescription
 * RevisionIssued
 * RevisionIssuedBy
 * RevisionIssuedTo
Governance:
 * Revision not marked issued
 * Issued sheets missing revisions
 * Revision growth spikes
Predictive:
 * Revision velocity
 * Late revision patterns
7. FactViewMeta (NEW – IMPORTANT)
One row per view per run.
## Identity
 * ViewId
 * ViewName
 * ViewType
 * ViewDiscipline (optional)
 * IsTemplate
Governance
 * IsPlacedOnSheet (Y/N)
 * SheetNumber (first sheet if placed)
 * View_Status (shared param)
 * View_RequiredOnIssue (Y/N)
Completion
 * IsPrintable (if evaluated)
 * IsDependentView
 * ViewTemplateApplied (Y/N)
Governance:
 * Unplaced printable views
 * Required views not placed
 * Views without template
 * View bloat growth
Predictive:
 * Unplaced view growth rate
 * View creation velocity vs placement velocity
8. FactViewPlacement (OPTIONAL BUT CLEAN)
One row per Viewport:
 * ViewportId
 * ViewId
 * SheetId
 * SheetNumber
 * DetailNumber
 * ViewScale
This allows:
 * Precise many-to-many analysis
 * Clean relationship modeling in Power BI
Recommended if your portfolio is large.
# SHARED PARAMETERS (UPDATED MASTER LIST)
## A) Project Information Parameters
| Name | Type | Category | Instance | Group |
|---|---|---|---|---|
| Portfolio_ProjectID | Text | Project Information | Instance | Identity Data |
| Portfolio_ProjectName | Text | Project Information | Instance | Identity Data |
| Portfolio_Discipline | Text | Project Information | Instance | Identity Data |
| Portfolio_ProjectPhase | Text | Project Information | Instance | Project Information |
| Portfolio_Milestone_NextName | Text | Project Information | Instance | Project Information |
| Portfolio_Milestone_NextDate | Date | Project Information | Instance | Project Information |
| Coord_BaselineRole | Yes/No | Project Information | Instance | Identity Data |
| ACC_ProjectId | Text | Project Information | Instance | Identity Data |
## B) Sheet Parameters
| Name | Type | Category | Instance | Group |
|---|---|---|---|---|
| Sheet_Status | Text | Sheets | Instance | Identity Data |
| Sheet_TargetPackage | Text | Sheets | Instance | Identity Data |
| Sheet_RequiredOnIssue | Yes/No | Sheets | Instance | Identity Data |
## C) QA Parameters (Bind to selected model categories only)
| Name | Type | Categories | Instance | Group |
|---|---|---|---|---|
| QA_Modelled | Yes/No | Doors, Rooms, Ducts, etc. | Instance | Identity Data |
| QA_Reviewed | Yes/No | Same as above | Instance | Identity Data |
| QA_ReadyForIssue | Yes/No | Same as above | Instance | Identity Data |
| QA_Notes | Text | Same as above | Instance | Text |
# GOVERNANCE ENGINE 
Governance checks now include:
## Model Health
 * Warnings threshold
 * CAD imports
 * In-place limit
 * Single-instance groups
 * Unplaced views
## Coordination
 * Coordinate mismatch
 * Link movement
 * Link unpinned
## Documentation
 * Missing Sheet_Status
 * Missing Checker/Approver
 * Issued sheet without revisions
 * Sheet without views
 * Required views not placed
## Delivery
 * Sheet issuance velocity
 * QA review velocity
# PREDICTIVE ENGINE 
Rolling windows:
 * 30 / 60 / 90 days
Milestone-based:
 * Required vs actual velocity
Drift detection:
 * Coordinate deltas over time
 * Link origin drift
 * View bloat acceleration
 * Revision acceleration
# IMPLEMENTATION PLAN
 * Phase 1 – Core exporter (health + coord + sheet + view)
 * Phase 2 – CAD + revision + placement deepening
 * Phase 3 – Governance scoring in Power BI
 * Phase 4 – Predictive measures
 * Phase 5 – Milestone forecasting
 
SYSTEM MATURITY LEVEL
This is no longer “dashboarding”. It is:
 * BIM governance enforcement
 * Coordination drift monitoring
 * Model performance management
 * Delivery risk forecasting
 * Portfolio technical intelligence

It must be a single monolithic pyRevit (CPython) exporter that writes:

- Append-only CSV facts (all tables we agreed on)
- One JSON per run (audit/debug package)
- Designed for Revit 2024 / 2025 and BIM Collaborate Pro (cloud-safe: avoids relying on doc.PathName)
  
## What this one button exports

Append-only CSVs (in your OUT_FOLDER)

- FactModelHealth.csv
- FactModelCoordSignature.csv
- FactHostLinkPlacement.csv
- FactCADLinks.csv
- FactSheetMeta.csv
- FactSheetRevisions.csv
- FactViewMeta.csv
- FactViewPlacement.csv (recommended; included)
  

Per-run JSON


- {Portfolio_ProjectID}_{Discipline}_{RunId}_EXPORT.json
-
# BIM Portfolio Governance Exporter (One Button)

Revit 2024/2025 + pyRevit CPython

## Outputs:

- Append-only CSV facts:

    FactModelHealth

    FactModelCoordSignature

    FactHostLinkPlacement

    FactCADLinks

    FactSheetMeta

    FactSheetRevisions

    FactViewMeta

    FactViewPlacement

- JSON per run for audit/debug

## Notes:

- Cloud models: doc.PathName may be blank. We key by Portfolio_ProjectID + ModelTitle + RunId.

- Imported CAD often has no external path. Linked CAD is where size/path typically exists.

# Shared parameter names expected on Project Information

PARAM_PORTFOLIO_ID = "Portfolio_ProjectID"

PARAM_PORTFOLIO_NAME = "Portfolio_ProjectName"

PARAM_PORTFOLIO_DISC = "Portfolio_Discipline"

PARAM_COORD_BASELINE_ROLE = "Coord_BaselineRole"  # Yes/No (optional)

# Optional shared parameters used in docs/governance

PARAM_SHEET_STATUS = "Sheet_Status"

PARAM_SHEET_TARGET_PACKAGE = "Sheet_TargetPackage"

PARAM_SHEET_REQUIRED_ON_ISSUE = "Sheet_RequiredOnIssue"

PARAM_VIEW_STATUS = "View_Status"

PARAM_VIEW_REQUIRED_ON_ISSUE = "View_RequiredOnIssue"

## Updated shared parameters list (with the sheet/view placement additions)

### Project Information

|   |   |   |   |   |
|---|---|---|---|---|
|Parameter|Type|Bind to|Instance/Type|Group|
|Portfolio_ProjectID|Text|Project Information|Instance|Identity Data|
|Portfolio_ProjectName|Text|Project Information|Instance|Identity Data|
|Portfolio_Discipline|Text|Project Information|Instance|Identity Data|
|Portfolio_ProjectPhase|Text|Project Information|Instance|Project Information|
|Portfolio_Milestone_NextName|Text|Project Information|Instance|Project Information|
|Portfolio_Milestone_NextDate|Date|Project Information|Instance|Project Information|
|Coord_BaselineRole|Yes/No|Project Information|Instance|Identity Data|
|(Optional) ACC_ProjectId|Text|Project Information|Instance|Identity Data|

### Sheets

|   |   |   |   |   |
|---|---|---|---|---|
|Parameter|Type|Bind to|Instance/Type|Group|
|Sheet_Status|Text|Sheets|Instance|Identity Data|
|Sheet_TargetPackage|Text|Sheets|Instance|Identity Data|
|Sheet_RequiredOnIssue|Yes/No|Sheets|Instance|Identity Data|

Author/Checker/Approver do not need shared params (they are built-in sheet parameters). The exporter reads them directly.
## Views

|   |   |   |   |   |
|---|---|---|---|---|
|Parameter|Type|Bind to|Instance/Type|Group|
|View_Status|Text|Views|Instance|Identity Data|
|View_RequiredOnIssue|Yes/No|Views|Instance|Identity Data|

## QA parameters 
(bind only to your selected discipline categories)

|   |   |   |   |   |
|---|---|---|---|---|
|Parameter|Type|Bind to|Instance/Type|Group|
|QA_Modelled|Yes/No|Selected model categories|Instance|Identity Data|
|QA_Reviewed|Yes/No|Selected model categories|Instance|Identity Data|
|QA_ReadyForIssue|Yes/No|Selected model categories|Instance|Identity Data|
|QA_Notes|Text|Selected model categories|Instance|Text|

# Final scope recap

## Governance


- Sheet completion compliance (status, titleblock, views placed, revisions)
- View governance (required views not placed, views without templates, unplaced view bloat)
- CAD governance (imports, linked file size/age)
- Coordinate signature + link movement governance

## Predictive

- 30/60/90 rolling velocities: warnings, unplaced views, revisions, sheets gaining placed views
- Milestone forecasting using milestone dates + velocities
- Drift detection: coordinate deltas + link transform changes
  
If modify the exporter to also write a small DimModel.csv (ModelTitle + Discipline + ProjectID) and DimRun.csv (RunId, RunDateTime, user, machine) so Power BI setup is even cleaner.