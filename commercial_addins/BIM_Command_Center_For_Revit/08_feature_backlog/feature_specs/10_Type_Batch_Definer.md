# Type Batch Definer

Priority: P1

## Commercial Value

Office standards often require repeated type naming, type parameter defaults, and tag/type alignment. A controlled batch definer reduces manual setup time.

## Minimum Scope

- Load a type mapping table from JSON or CSV.
- Preview target categories and type names.
- Create missing types by duplicating a selected base type.
- Set allowed type parameters only.
- Export result report.

## Default Safeguards

- Dry-run is mandatory.
- Instance parameters are out of scope.
- Read-only parameters are skipped.
- Existing types are skipped unless user enables update mode.

## Revit API Work Later

- Use category-specific collectors for element types.
- Duplicate base symbols/types where supported.
- Set type parameters only inside confirmed transactions.

## QA Cases

- Create new door type from base type.
- Skip existing type.
- Skip read-only parameter.
- Reject row with missing category.
