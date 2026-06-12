# Autodesk Entitlement API Implementation

- Date: 2026-05-19
- Product: BIM Command Center for Revit

## Implemented

- Removed the hardcoded activation password from source.
- Removed the hardcoded HMAC signing secret from source.
- Removed CPU/MAC based machine binding from source.
- Replaced local password activation with Autodesk App Store entitlement checking.
- Added `license-settings.json` so the final Store App ID can be inserted after the Store app record exists.
- Added installer embedding for `license-settings.json`.

## Runtime Flow

1. Revit starts `BIMCommandCenter.App`.
2. `LicenseManager` reads the current Autodesk login user ID from the Revit application object.
3. `LicenseManager` reads the Store App ID from `license-settings.json` or `BIM_COMMAND_CENTER_APP_ID`.
4. The add-in calls `https://apps.autodesk.com/webservices/checkentitlement`.
5. If `IsValid` is true, the add-in continues loading.
6. If entitlement is invalid, the add-in blocks startup and shows the subscription check dialog.

## Required Before Release

- Create the Autodesk Store app record.
- Replace `REPLACE_WITH_AUTODESK_APP_STORE_APP_ID` in `license-settings.json`.
- Rebuild the add-in DLLs and installer on Windows.
- Recommended build helper: `scripts/build_bim_command_center_release.ps1 -AutodeskAppId <STORE_APP_ID>`.
- Confirm entitlement behavior with an Autodesk test account.
- Confirm 30-day trial behavior in the Store submission workflow.

## Important

Old binaries may still contain previous local-license code until a clean Windows release build is produced. Do not ship existing `bin/Release` binaries without rebuilding.

## Official References

- Autodesk Entitlement API for desktop apps: https://www.autodesk.com/content/dam/autodesk/www/adn/pdf/entitlement-api-for-desktop-apps.pdf
- Autodesk desktop app submission process: https://www.autodesk.com/content/dam/autodesk/www/adn/pdf/desktop-app-submission-process-overview.pdf
- Revit `LoginUserId` reference: https://www.revitapidocs.com/2025/8d3b257a-7b99-a6ee-b146-f635c35f425c.htm
