# BIM Command Center for Revit - User Guide Draft

## Overview

BIM Command Center for Revit is a unified Revit dashboard for frequently used BIM coordination and MEP productivity tools. It provides a Revit ribbon entry and a dockable command dashboard.

## Installation

1. Close Revit.
2. Run the BIM Command Center installer.
3. Select the Revit versions to install.
4. Complete installation.
5. Restart Revit.
6. Sign in to Revit with the Autodesk account that owns the Store subscription or trial entitlement.

## Subscription Check

When Revit starts, BIM Command Center checks Autodesk App Store entitlement.

If subscription access is valid, the add-in loads normally.

If access is not valid:

- Confirm that Revit is signed in to Autodesk.
- Confirm that the same Autodesk account downloaded or purchased the app.
- Confirm that the trial or subscription is still active.
- Contact support with the error screenshot if the issue continues.

## Opening The Dashboard

1. Open Revit.
2. Go to the BIM Command Center ribbon tab.
3. Click the BIM Command Center button.
4. The dashboard opens as a dockable panel.

## Main Workflows

### Model Health

Use Model Health commands to refresh and open model health dashboard information. This helps BIM managers review model status and identify routine model quality issues.

### Workset Dashboard

Use Workset Dashboard to review workset visibility and coordination state. This is useful for workshared models and coordination reviews.

### Auto Save / Auto Sync

Use Auto Sync settings to configure supported save or sync assistance options. Validate settings on a sample model before using them on production workshared models.

### MEP Splitter

Use MEP Splitter commands for supported MEP element split, break, unsplit and coupling alignment workflows. Test each command on copied model elements before applying it broadly.

### Clash Coordination Utilities

Use clash point, section box and clash view commands to support clash review and follow-up. Use reporting commands to capture before/after views where supported.

### Unit Conversion

Use unit conversion commands only after confirming the project standard. For family batch workflows, test on a copied folder first.

### To Do List

Use the local To Do command to manage BIM task notes connected to Revit context where supported.

## First Release Exclusions

The first commercial release does not include:

- `RevitAddin.MepBim`
- MEP·BIM Coordination Console browser dashboard
- External AI/chat workflows
- Navisworks tools

## Troubleshooting

### Add-In Does Not Appear

- Restart Revit.
- Confirm the selected Revit version was checked during installation.
- Confirm the add-in appears in the Revit add-ins folder.
- Reinstall as administrator if required by company policy.

### Subscription Check Fails

- Confirm Autodesk login inside Revit.
- Confirm purchase or trial entitlement in Autodesk App Store.
- Confirm internet access to Autodesk App Store services.
- Contact support with Revit version, Windows version and a screenshot.

### Dashboard Is Blank

- Confirm WebView2 Runtime is installed.
- Restart Revit.
- Check company firewall or antivirus policies.
- Contact support if the issue continues.

## Support

Support email: `support@your-domain.example`

Include:

- Revit version
- Windows version
- BIM Command Center version
- Screenshot
- Steps to reproduce
- Whether the model is local, central or cloud workshared
