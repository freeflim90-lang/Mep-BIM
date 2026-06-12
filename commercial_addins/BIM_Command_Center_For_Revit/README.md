# BIM Command Center For Revit

Commercial product workspace for Autodesk Store submission and subscription sales.

## Source Of Truth

Development source:

`$BCC_ADDIN_DEV_SOURCE_ROOT/01_Revit_Addins/Addin Dashboard`

Store documentation:

`../../docs/autodesk_store`

Work boundary:

`00_product/WORK_BOUNDARY.md`

## Product Decision

- Product name: BIM Command Center for Revit
- Payment type: Subscription
- Trial: 30 days
- First release products:
  - Individual: USD 19/month or USD 190/year
  - Team 5-Pack: USD 79/month or USD 790/year, if supported by the sales workflow
  - Enterprise: custom pricing
- Licensing method: Autodesk App Store Entitlement API
- First release excludes:
  - `RevitAddin.MepBim`
  - MEP·BIM Coordination Console browser dashboard
  - External AI/chat workflows
  - Navisworks tools

## Folder Structure

- `00_product`: product decision records and release scope
- `01_release_inputs`: files received from the Revit build machine
- `02_build_artifacts`: final installers/packages
- `03_store_submission`: generated upload bundles and Store form assets
- `04_qa_evidence`: screenshots and QA results
- `05_customer_support`: support materials and templates
- `06_legal`: public EULA/privacy drafts or final files
- `07_archive`: frozen submitted packages
- `08_feature_backlog`: future commercial feature specs and non-Revit API configs

## Next Owner Inputs

- Final installer `.exe`
- Product icon
- Screenshots
- Demo video or video URL
- Final support email
- Product website URL
- Public privacy policy URL
- Public EULA URL
- Autodesk Store App ID
- QA evidence for Revit 2024/2025/2026
