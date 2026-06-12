# Workset Inspector Lite

## Commercial Value

Workset mistakes are common in multi-user BIM production. This feature makes ownership and placement errors easier to detect and fix.

## User Flow

1. Open Workset Inspector Lite from BIM Command Center.
2. Review workset element counts.
3. Select a workset.
4. Preview elements and unexpected category placements.
5. Isolate, select, or export a QA report.

## Rule Examples

- Linked model instances must be on link worksets.
- Levels and grids must be on shared datum workset.
- MEP pipes must not be on architectural worksets.
- Imported CAD must be on CAD/import worksets.

## Default Safeguards

- Report first, selection second.
- No automatic workset reassignment in v1.
- Export rule violations before any model change is introduced.

## Revit API Work Later

- Read `ELEM_PARTITION_PARAM`.
- Count elements by workset and category.
- Use isolate/select commands for quick investigation.
- Add reassignment only after strong QA confidence.

## QA Cases

- Revit links on wrong workset.
- CAD imports on generic workset.
- MEP category on architectural workset.
- Empty workset appears with zero count.
- Exported summary matches visible count.
