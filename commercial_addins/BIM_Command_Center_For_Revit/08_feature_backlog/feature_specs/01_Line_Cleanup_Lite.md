# Line Cleanup Lite

## Commercial Value

Imported and exploded CAD details often leave duplicate, tiny, or wrong-kind lines. This feature reduces view clutter and model maintenance time.

## User Flow

1. Open a drafting, detail, plan, or section view.
2. Run Line Cleanup Lite.
3. Choose cleanup checks.
4. Preview affected lines.
5. Confirm deletion or conversion.
6. Save cleanup report.

## Supported Checks

- Duplicate lines: same or near-same endpoints and line style.
- Short lines: length below configured threshold.
- Model-line report: list model lines in views where detail lines are preferred.

## Default Safeguards

- Active view only.
- Delete action requires confirmation.
- Model line conversion is disabled for first implementation.
- Ignore pinned elements unless explicitly enabled.
- Ignore grouped elements unless explicitly enabled.

## Revit API Work Later

- Collect `CurveElement` instances from the active view.
- Normalize line endpoints with geometric tolerance.
- Use a `Transaction` only after preview confirmation.
- Capture deleted element ids in the report.

## QA Cases

- Two identical detail lines overlap.
- Short imported CAD fragments below 10 mm.
- Pinned line is found but skipped.
- Grouped detail line is found but skipped.
- Model line appears in report without conversion.
