# Autodesk Store Form Field Values

- Product: BIM Command Center for Revit
- Publisher: LUA BIM LABS
- Payment type: Subscription
- Trial: 30 days

## Product Name

BIM Command Center for Revit

## Short Description

A Revit productivity dashboard for BIM coordinators and MEP teams, combining model health, workset review, auto-save support, MEP tools and clash coordination utilities.

## Long Description

BIM Command Center for Revit brings frequently used BIM coordination and productivity tools into one unified Revit add-in. It is designed for BIM managers, VDC coordinators and Revit MEP teams that need quick access to model review, workset control, routine automation and clash follow-up workflows.

The add-in provides a dockable dashboard and ribbon commands inside Revit. Users can launch supported tools from one command center instead of switching between separate add-ins. The first commercial release focuses on local Revit productivity workflows and does not include external AI services.

## Key Features

- Unified dockable dashboard and Revit ribbon launcher
- Model health data refresh and dashboard access
- Workset visibility dashboard
- Auto Save / Auto Sync settings access
- MEP Splitter commands for split, break, unsplit and coupling alignment workflows
- Clash marker, section box and clash view utilities
- Clash report image capture and dashboard commands
- Unit conversion commands, after final validation
- Local BIM to-do workflow, after final validation

## Benefits

- Reduces time spent searching for repeated BIM coordination commands
- Gives BIM coordinators one place to access daily model review tools
- Supports practical Revit MEP production and coordination workflows
- Helps standardize common add-in access across a team
- Keeps the first release focused on local Revit workflows for simpler deployment and support

## Target Audience

- BIM managers
- VDC coordinators
- Revit MEP modelers
- Design coordination teams
- Contractors and engineering firms using Revit for production coordination

## Categories

Suggested categories:

- Productivity
- MEP
- Model Review
- Coordination

## Compatibility

Claim only versions tested on Windows:

- Autodesk Revit 2024
- Autodesk Revit 2025
- Autodesk Revit 2026

Do not claim Revit 2027 until the clean QA matrix is complete.

## System Requirements

- Windows 10 or Windows 11
- Autodesk Revit 2024, 2025 or 2026
- .NET Framework 4.8 for Revit 2024
- .NET 8 Desktop Runtime for Revit 2025 and newer if not already available
- Microsoft Edge WebView2 Runtime if dashboard web panel features are enabled
- Internet access for Autodesk App Store entitlement verification

## Pricing

- Individual Monthly: USD 14/month
- Individual Annual: USD 140/year (saves ~17% vs monthly)
- Team 5-Pack Annual: USD 490/year (~USD 8.17/seat/month, saves ~30% vs individual annual)
- Enterprise: custom pricing by direct contact

Note: Autodesk App Store listing uses the same USD 14/month · USD 140/year price points.
Direct sales via the LUA BIM LABS website use the same rates to avoid channel confusion.

## Autodesk Store Payment Field Notes

- Price type: Subscription
- Monthly price: 14 (USD)
- Annual price: 140 (USD)
- Currency: USD
- Confirm payment type before submission. Autodesk documentation says payment type cannot be changed once Subscription is selected.
- Enable 30-day trial only with Entitlement API integration.
- First release should use Entitlement API rather than a custom IPN backend.
- Team 5-Pack is handled via direct sales email (freeflim90@gmail.com); Autodesk Store lists individual pricing only.

## Support Information

Support email: `support@your-domain.example`

Recommended public text:

For installation, licensing and workflow support, contact LUA BIM LABS support by email. Please include your Revit version, Windows version, BIM Command Center version, a screenshot of the issue and the steps needed to reproduce it.

## Installation Text

Install the add-in using the provided installer. Restart Autodesk Revit after installation. BIM Command Center will appear in the Revit ribbon and can open a dockable dashboard panel.

## Uninstallation Text

Uninstall BIM Command Center from Windows Apps & Features or Control Panel > Programs and Features. Restart Revit after uninstalling.

## Privacy Summary

The first commercial release uses Autodesk App Store entitlement verification. The add-in checks the Autodesk login user identifier provided by Revit and the Store App ID to confirm subscription access. Core BIM commands run locally inside Revit. External AI features are not included in the first commercial release.

## Exclusions

The first commercial release excludes:

- `RevitAddin.MepBim`
- MEP·BIM Coordination Console browser dashboard
- External AI/chat workflows
- Navisworks tools
