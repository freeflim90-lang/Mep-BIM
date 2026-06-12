# BIMIZE Public Feature Internalization Plan

Status: draft
Last updated: 2026-05-19

## Purpose

This backlog turns publicly visible BIMIZE product categories into original BIM Command Center features. It is not a request to copy BIMIZE code, UI, icons, naming, files, help text, or implementation details.

## Source Review

Public Autodesk App Store listings reviewed on 2026-05-19:

- BIMIZE LineCleaner: duplicate/short line cleanup and model-line conversion.
- BIMIZE QuickSelect: category/parameter based element selection and saved selections.
- BIMIZE WorksetFinder: workset based element selection.
- BIMIZE LinkReloader: batch reload for linked references.
- BIMIZE QuickPrint: batch print for views, sheets, and schedules.
- BIMIZE SmartViews: sheet/view duplication and sheet-view management.
- BIMIZE AutoExcel: schedule export/import through Excel.

User-provided BIMlize for Revit ribbon screenshot reviewed on 2026-05-19:

- Project creation, type batch definition, view template copy, settings management.
- Parameter, project cleanup, family export/import, model comparison, utility commands.
- Schedule Excel save, schedule item processing, Excel export/import.
- Model processing, MEP utilities, 3D view creation/export, tag/text alignment, tag family type definition, multi material tag, license information.

See `BIMLIZE_RIBBON_FEATURE_MATRIX.md` for the screenshot-based matrix.

## Product Principle

- Use original product names in BIM Command Center.
- Keep Korean BIM production workflows in mind: imported CAD cleanup, workset QA, shop drawing issue support, schedule editing, and batch deliverable production.
- Prefer small, testable commands that fit the existing dashboard instead of another separate tab-heavy product.
- Build a non-Revit core first where possible: rule JSON, preview result DTOs, validation, export formats, and user guide behavior.

## Internal Feature Map

| Public category | Internal feature name | Priority | First implementation path |
| --- | --- | --- | --- |
| LineCleaner | Line Cleanup Lite | P1 | Rule config, preview report, Revit command later |
| QuickSelect | Smart Selector Lite | P1 | Rule config, category/parameter filter model |
| WorksetFinder | Workset Inspector Lite | P1 | Extend existing Workset Dashboard concept |
| LinkReloader | Link Health & Reload | P2 | Link status report first, reload command later |
| QuickPrint | Batch Print Assistant | P2 | Print set model and QA checklist |
| SmartViews | Sheet/View Duplicator | P2 | Scope after drawing automation review |
| AutoExcel | Schedule Excel Sync | P2 | CSV/XLSX mapping and read-only field policy |

## Phase Strategy

Phase 1 keeps the scope intentionally small and now favors the user-provided ribbon screenshot:

1. Settings Profile Manager
2. View Template Copier
3. Type Batch Definer
4. Tag/Text Aligner
5. Project Cleanup Lite audit mode
6. Schedule Excel Export

The earlier public Store features remain useful as a later market benchmark, but the screenshot matrix is the better target for this user's commercial add-in direction.

Phase 2 adds link, print, sheet/view, and schedule automation after the first commercial release package is stable.

## Legal And Store Safety

- Do not use BIMIZE names in shipped UI.
- Do not copy screenshots, command text, icons, or exact help wording.
- Keep this document internal.
- Store listing should describe customer outcomes, not competitor parity.
