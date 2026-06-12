# Tag/Text Aligner

Priority: P1

## Commercial Value

Drawing cleanup consumes a lot of time near issue deadlines. Aligning tags and text is small, understandable, and easy to demonstrate in Store screenshots.

## Minimum Scope

- Align selected tags/text horizontally.
- Align selected tags/text vertically.
- Distribute selected tags/text by spacing.
- Keep leaders optional and unchanged by default.

## Default Safeguards

- Works on current selection only.
- Preview movement vector before applying.
- Do not move pinned annotations.

## Revit API Work Later

- Resolve supported annotation elements.
- Move elements using Revit transaction after confirmation.
- Validate leader behavior per tag category.

## QA Cases

- Align three room tags.
- Align text notes.
- Skip pinned annotation.
- Preserve leaders in default mode.
