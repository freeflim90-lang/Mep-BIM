# Release Notes - Version 1.0

## BIM Command Center for Revit 1.0

Initial commercial release for Autodesk Revit.

## Supported Versions

Final support list must match QA evidence:

- Autodesk Revit 2024
- Autodesk Revit 2025
- Autodesk Revit 2026

## Included

- Unified BIM Command Center dashboard
- Revit ribbon launcher
- Model Health dashboard access
- Workset Dashboard access
- Auto Save / Auto Sync settings access
- MEP Splitter command access
- Clash marker and section box utility access
- Clash report capture/dashboard command access
- Unit conversion command access, after final validation
- Local To Do command access, after final validation
- Autodesk App Store entitlement check

## Excluded

- `RevitAddin.MepBim`
- MEP·BIM Coordination Console browser dashboard
- External AI/chat workflows
- Navisworks tools

## Known Limitations

- Internet access is required for Autodesk App Store entitlement verification.
- WebView2 Runtime may be required for dashboard panel features.
- Some commands require suitable Revit model categories, views or worksharing state.
- First release compatibility is limited to Revit versions verified in QA evidence.

## Upgrade Notes

Close Revit before installing or upgrading. After installation, restart Revit and sign in with the Autodesk account associated with the app subscription or trial.
