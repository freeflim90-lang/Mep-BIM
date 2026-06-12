# Autodesk Store Upload Automation Policy

- Date checked: 2026-05-19
- Product: BIM Command Center for Revit

## Can Upload Be Fully Automated?

Not safely for first release.

As of the checked Autodesk Publisher Center and submission documentation, Autodesk provides:

- Publisher Center / Publisher Corner web workflow
- App submission form
- File upload through the web form
- Payment processor setup through Publisher Corner
- Entitlement API for runtime subscription verification
- BlueSnap API credential setup for Autodesk payment integration

What was not found:

- Public Autodesk App Store submission API for creating/updating product listings
- Public CLI for uploading app packages
- Public CI/CD endpoint for submitting apps for review

## Recommended Approach

Use a semi-automated workflow:

1. Automate package preparation locally.
2. Automate validation checklist generation.
3. Automate metadata/document bundle generation.
4. Manually upload through Autodesk Publisher Center.
5. Manually preview and submit.

This avoids brittle browser automation, accidental wrong-price submission and possible account/security issues.

## What We Can Automate Safely

- Build output collection after owner builds on Revit machine
- Store metadata bundle creation
- Screenshot/video asset checklist
- Release notes inclusion
- Privacy/EULA/User Guide inclusion
- Package manifest generation
- Pre-upload validation
- Source scan for excluded features such as `RevitAddin.MepBim`
- Source scan for old local license secrets
- ZIP creation for the upload handoff folder

## What Should Stay Manual

- Publisher login
- Payment processor setup
- Choosing `Subscription`
- Final price input
- File upload
- Store preview review
- Final Submit button
- Responding to Autodesk review comments

## Why Browser Automation Is Not Recommended

Browser automation could technically click through Publisher Center, but it is risky because:

- Login, MFA and session controls may change.
- Payment type selection is high impact.
- Autodesk documentation says Subscription payment type may not be changeable after selection.
- Upload forms and validation can change without notice.
- A mistaken automated click could submit incomplete pricing or compatibility data.

Use browser automation only for read-only checks or screenshots, not final submission.

## First Release Policy

For BIM Command Center v1.0:

- Do not automate final Store submission.
- Prepare a complete local upload bundle.
- Owner manually uploads the bundle in Publisher Center.
- Owner manually confirms payment type, price and preview page.
- Owner manually clicks Submit.

## References

- Autodesk Publisher Center: https://aps.autodesk.com/app-store/publisher-center
- Autodesk desktop app submission guide: https://www.autodesk.com/content/dam/autodesk/www/adn/pdf/desktop-app-submission-process-overview.pdf
- Autodesk desktop subscription guide: https://damassets.autodesk.net/content/dam/autodesk/www/adn/pdf/selling-desktop-app-on-monthly-subscription.pdf
