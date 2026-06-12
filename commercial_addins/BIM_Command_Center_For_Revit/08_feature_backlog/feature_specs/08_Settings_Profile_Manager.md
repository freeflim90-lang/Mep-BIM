# Settings Profile Manager

Priority: P0

## Commercial Value

Users need predictable presets for BIM Command Center commands, especially when the same office standard is reused across projects.

## Minimum Scope

- Save command settings as JSON profiles.
- Load a selected profile.
- Validate profile version before applying it.
- Keep profiles outside Revit model files.
- Support office default and project-specific profiles.

## Non-Revit Work Now

- JSON schema and sample profile.
- Profile validation script.
- UI labels and error messages.

## Revit API Work Later

- Apply profile settings to command dialogs.
- Avoid writing to the model unless the command itself requires it.

## QA Cases

- Load valid profile.
- Reject unsupported version.
- Reject missing required feature key.
- Preserve unknown future keys without crashing.
