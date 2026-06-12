# Project Cleanup Lite

Priority: P1

## Commercial Value

Project cleanup is a high-frequency BIM manager task. A safe audit-first command helps users understand model clutter before any destructive cleanup is allowed.

## Minimum Scope

- Count project warnings.
- Count imported CAD/link-like import instances.
- Count views and view templates.
- Count schedules.
- Report cleanup candidates.

## Default Safeguards

- Audit only.
- No delete operations in first implementation.
- Cleanup actions require owner QA on real Revit projects.

## Revit API Work Later

- Add targeted cleanup actions one by one after dry-run results are reliable.
- Use explicit user confirmation for every destructive operation.

## QA Cases

- Model with warnings.
- Model with imported CAD.
- Model with multiple view templates.
- Empty/small model with no cleanup candidates.
