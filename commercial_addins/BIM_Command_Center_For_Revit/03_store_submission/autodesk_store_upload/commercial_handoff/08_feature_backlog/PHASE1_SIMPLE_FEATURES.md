# Phase 1 Simple Features

Status: ready for Revit API implementation
Owner boundary: Codex prepares specs/configs; owner validates and builds on the Revit machine.

## Screenshot-Based Priority

The user-provided BIMlize ribbon screenshot changes the first implementation order. Keep the earlier Store-public feature specs for market reference, but start with the small commands that map directly to the screenshot and fit BIM Command Center.

## 1. Settings Profile Manager

Goal: create a common settings backbone for future commands.

Minimum behavior:

- Save/load command presets as JSON.
- Validate profile version.
- Keep office default and project profile separate.
- Reject broken profiles with a clear message.

First release default:

- Non-Revit core only.
- No model changes.

## 2. View Template Copier

Goal: copy selected view templates with a safe collision policy.

Minimum behavior:

- List source templates.
- Preview target copy result.
- Skip, rename, or replace same-name templates.
- Export copy report.

First release default:

- Collision policy is skip.
- Replace requires explicit confirmation.

## 3. Type Batch Definer

Goal: create or update standard types from a controlled mapping table.

Minimum behavior:

- Load type definitions from JSON/CSV.
- Preview missing/existing types.
- Create missing types from selected base types.
- Skip read-only parameters.

First release default:

- Dry-run mandatory.
- Existing types skipped by default.

## 4. Tag/Text Aligner

Goal: provide a small drafting cleanup tool that is easy to test and easy to sell visually.

Minimum behavior:

- Align selected tags/text.
- Distribute selected tags/text.
- Skip pinned annotations.
- Preserve leaders by default.

First release default:

- Current selection only.
- Preview before move.

## 5. Project Cleanup Lite

Goal: clean or report project clutter while protecting production models.

Minimum behavior:

- Audit unused views, imported CAD, warnings count, unplaced rooms/spaces, and unused view templates where possible.
- Report first.
- Add cleanup actions one by one only after QA.

First release default:

- Audit/report only.

## 6. Schedule Excel Export

Goal: export schedules for review and office workflows before adding risky import behavior.

Minimum behavior:

- Export active schedule to CSV/XLSX.
- Preserve field names and visible order.
- Record read-only/import restrictions in the report.

First release default:

- Export only.
- Import is Phase 2.

## Market-Benchmark Features Kept For Later

### Line Cleanup Lite

Goal: clean CAD-import residue and drafting clutter before it hurts model performance or documentation quality.

Minimum behavior:

- Find duplicate or near-duplicate detail/model lines in the active view.
- Find lines shorter than a configured threshold.
- Preview count before deletion.
- Delete only after explicit user confirmation.
- Export cleanup summary to CSV or JSON.

First release default:

- Active view only.
- Detail lines first.
- Model lines are report-only until tested on real project models.

### Smart Selector Lite

Goal: quickly create a reliable element selection set by category, type, parameter, workset, and current view scope.

Minimum behavior:

- Select from active view or whole project.
- Filter by category, family/type name, parameter name, operator, and value.
- Reuse saved selection rules from JSON.
- Preview count and sample elements before applying selection.

First release default:

- Read-only preview first.
- Apply selection only after preview.
- Exclude groups by default unless user enables grouped elements.

### Workset Inspector Lite

Goal: make workset QA visible without leaving BIM Command Center.

Minimum behavior:

- List worksets with element counts.
- Select or isolate elements from a chosen workset.
- Flag elements on unexpected worksets based on configurable rules.
- Export workset QA summary.

First release default:

- Use existing Workset Dashboard as the natural integration target.
- Add rule-driven checks before adding complex UI.

## Done Criteria

- Each feature has a command entry proposal.
- Each feature has config defaults.
- Each feature can generate a dry-run report.
- Revit transaction changes are limited to confirmed user actions.
- QA evidence includes at least one small sample model and one real project model.
