# Schedule Excel Export

Priority: P1

## Commercial Value

Schedule export supports BIM QA, quantity review, and office data workflows without immediately taking on the risk of import-driven model changes.

## Minimum Scope

- Detect active schedule view.
- Report schedule field count and row count where possible.
- Confirm export settings.
- Keep first implementation dry-run only.

## Default Safeguards

- Export only after dry-run QA.
- Import is out of scope for Phase 1.
- Preserve visible schedule field order.

## Revit API Work Later

- Use schedule table data for CSV export.
- Add XLSX only if dependency policy is approved.
- Add import in a later phase with read-only and type safety checks.

## QA Cases

- Active schedule view.
- Non-schedule active view.
- Schedule with hidden fields.
- Schedule with no body rows.
