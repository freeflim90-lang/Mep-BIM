# Autodesk Store Submission Checklist

## Publisher

- [ ] Autodesk App Store publisher account created
- [ ] Publisher name selected
- [ ] Support email ready
- [ ] Product website or landing page ready
- [ ] Privacy policy URL ready
- [ ] EULA URL ready
- [ ] Payment/tax setup complete if selling as paid product
- [ ] PayPal or BlueSnap selected for first launch
- [ ] Payment processor settings configured in Publisher Corner

## Product Scope

- [ ] Final product name selected
- [ ] First release module list frozen
- [x] Experimental modules hidden or disabled in listing scope
- [x] Supported Revit versions selected for QA target
- [ ] Supported Windows versions selected
- [x] Subscription price selected
- [x] Trial and license behavior defined
- [x] Autodesk Entitlement API source integration scaffolded for 30-day trial/subscription unlock
- [ ] Final Autodesk Store App ID inserted into `license-settings.json`
- [ ] Payment type confirmed before selecting `Subscription`

## Code And Packaging

- [ ] Release build created
- [ ] Owner completed Revit/Navisworks API dependent build on Autodesk-installed machine
- [ ] Debug-only code removed from release
- [x] No hardcoded activation passwords or signing secrets in source
- [ ] Release binaries rebuilt after license cleanup
- [ ] No hardcoded local developer paths in manifests, project files or installer
- [ ] `.addin` manifests use installed assembly paths
- [ ] Installer tested on clean Windows machine
- [ ] Uninstaller tested
- [ ] WebView2/runtime prerequisites handled
- [ ] External DLL dependencies included
- [ ] Add-in loads without exceptions
- [ ] Revit shutdown does not leave orphan processes

## Privacy And Security

- [x] Collected personal data documented in draft privacy policy
- [x] Commercial license flow avoids phone/email/machine ID collection in source
- [x] Network calls documented in draft privacy policy
- [x] AI/cloud features documented as excluded for first release
- [x] Customer model data handling documented in draft privacy policy
- [ ] Privacy policy matches real behavior
- [ ] User can contact support for data/license issues

## QA

- [ ] Owner completed final validation on Autodesk-installed machine
- [ ] Smoke test on Revit 2024
- [ ] Smoke test on Revit 2025
- [ ] Smoke test on Revit 2026
- [ ] Install/uninstall test on clean Windows account
- [ ] Test with sample architectural model
- [ ] Test with sample MEP model
- [ ] Test with workshared model
- [ ] Test with Korean and English Windows/Revit names where possible
- [ ] Capture screenshots of successful tests

## Listing Materials

- [ ] Product icon
- [ ] Store banner if required
- [x] Short description
- [x] Long description
- [x] Feature list
- [ ] Screenshots
- [ ] Demo video
- [x] User guide draft
- [x] Support/runbook document
- [x] Pricing page or pricing copy
- [x] Version number and release notes draft

## Submission

- [ ] Upload package
- [ ] Local upload handoff ZIP prepared
- [ ] Upload listing content
- [ ] Preview Store page
- [ ] Test purchase/download flow if available
- [ ] Submit for Autodesk review
- [ ] Track review feedback
- [ ] Patch and resubmit if needed
