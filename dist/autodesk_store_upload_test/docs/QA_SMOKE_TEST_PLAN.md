# QA Smoke Test Plan

- Product: BIM Command Center for Revit
- Release: 1.0
- Tester:
- Date:

## Test Matrix

| Environment | Status | Tester | Notes |
|---|---|---|---|
| Windows 10 + Revit 2024 | Not started |  |  |
| Windows 11 + Revit 2024 | Not started |  |  |
| Windows 10 + Revit 2025 | Not started |  |  |
| Windows 11 + Revit 2025 | Not started |  |  |
| Windows 10 + Revit 2026 | Not started |  |  |
| Windows 11 + Revit 2026 | Not started |  |  |

## Install / Uninstall

| Check | Expected | Status | Evidence |
|---|---|---|---|
| Installer starts | Installer opens without crash | Not started |  |
| Revit version detection | Installed Revit versions are selectable | Not started |  |
| Install completes | No error dialog | Not started |  |
| Add-in files installed | Files exist in expected Autodesk add-in folders | Not started |  |
| Revit starts after install | Revit starts without add-in load error | Not started |  |
| Uninstall completes | Product removed from Windows app list | Not started |  |
| Revit starts after uninstall | No missing add-in warning | Not started |  |

## Entitlement

| Check | Expected | Status | Evidence |
|---|---|---|---|
| App ID configured | `license-settings.json` contains final Store App ID | Not started |  |
| Autodesk signed-in user | Valid Store user passes entitlement check | Not started |  |
| User not signed in | Clear login message shown | Not started |  |
| User without entitlement | Clear subscription message shown | Not started |  |
| Trial user | Trial entitlement passes | Not started |  |

## Revit Load

| Check | Expected | Status | Evidence |
|---|---|---|---|
| Ribbon tab visible | BIM Command Center tab appears | Not started |  |
| Dashboard opens | Dockable dashboard opens | Not started |  |
| Dashboard can dock/undock | Panel behaves normally | Not started |  |
| Revit closes cleanly | No orphan process or shutdown error | Not started |  |

## Command Smoke Tests

| Command Group | Minimum Test | Status | Evidence |
|---|---|---|---|
| Model Health | Refresh/open dashboard on sample model | Not started |  |
| Workset Dashboard | Open on workshared test model | Not started |  |
| Auto Save / Auto Sync | Open settings only | Not started |  |
| MEP Splitter | Split/break/unsplit on copied MEP elements | Not started |  |
| Clash Utilities | Create marker or section box on sample clash setup | Not started |  |
| Clash Report | Capture before/after sample view | Not started |  |
| Unit Conversion | Run on copied sample model/family only | Not started |  |
| To Do | Create and reopen sample task | Not started |  |

## Store Evidence Folder

Save evidence under:

`docs/autodesk_store/evidence/v1.0/YYYY-MM-DD/`

Suggested files:

- installer-start.png
- install-complete.png
- revit-ribbon.png
- dashboard-open.png
- entitlement-valid.png
- entitlement-invalid.png
- model-health.png
- workset-dashboard.png
- mep-splitter.png
- clash-utility.png
- uninstall-complete.png
