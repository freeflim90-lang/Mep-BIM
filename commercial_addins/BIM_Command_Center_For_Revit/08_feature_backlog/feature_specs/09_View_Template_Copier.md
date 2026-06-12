# View Template Copier

Priority: P1

## Commercial Value

Project teams frequently need to copy view template standards between projects or apply a consistent template set to multiple views.

## Minimum Scope

- List source view templates.
- List target project view templates.
- Copy selected templates.
- Detect name collisions.
- Offer rename, skip, or replace behavior.

## Default Safeguards

- Default collision policy is `skip`.
- Preview before copy.
- No automatic overwrite without confirmation.

## Revit API Work Later

- Read `View` elements where `IsTemplate` is true.
- Duplicate/copy template elements through safe Revit API mechanisms.
- Validate copied template parameter behavior in Revit 2024/2025/2026.

## QA Cases

- Copy one template to an empty project.
- Skip same-name template.
- Rename same-name template with suffix.
- Confirm overwrite only after explicit user action.
