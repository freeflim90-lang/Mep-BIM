# Smart Selector Lite

## Commercial Value

Large Revit projects need fast, repeatable selection rules for cleanup, QA, parameter editing, and coordination.

## User Flow

1. Open Smart Selector Lite.
2. Choose scope: active view, current selection, or entire project.
3. Add one or more filters.
4. Preview matching elements.
5. Apply selection or save rule.

## Filter Model

- Category
- Family name
- Type name
- Workset
- Parameter name
- Operator: equals, contains, starts with, ends with, exists, missing
- Value

## Default Safeguards

- Exclude grouped elements by default.
- Exclude pinned elements by default when selection is intended for editing.
- Show count before applying selection.
- Save rule files separately from project data.

## Revit API Work Later

- Use `FilteredElementCollector`.
- Resolve built-in and shared parameters by display name and internal id where possible.
- Apply selection through `UIDocument.Selection.SetElementIds`.
- Save selection sets only if the Revit version and API surface support the intended behavior safely.

## QA Cases

- Select pipes by system abbreviation.
- Select doors with missing fire rating.
- Select elements in active view only.
- Exclude grouped elements from editable selection.
- Save and reload a JSON selection rule.
