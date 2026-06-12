# Autodesk Store Launch Plan

- Date: 2026-05-19
- Source product family: `$BCC_ADDIN_DEV_SOURCE_ROOT`
- Primary recommendation: launch one integrated Revit suite first, then split high-performing tools into separate listings later.

## 1. Product Strategy

### First store product

**BIM Command Center for Revit**

This should be the first Autodesk Store submission because the `Addin Dashboard` project already acts as a unified shell for many existing tools and includes an installer flow. A suite product is easier to explain, support and sell than 15 separate add-ins with different readiness levels.

### Initial included modules

Include only modules that are useful, explainable and close to Store-ready:

- Dashboard launcher and ribbon panel
- Model Health Dashboard
- Workset Dashboard
- Revit Auto Save / Auto Sync
- MEP Splitter
- Clash Point / section box / view automation tools, after smoke testing
- Unit conversion tools, after hardcoded path cleanup
- To Do List, if it remains local-only and stable

### Hold for later releases

Do not include these in the first paid Store listing until compliance and support risk is lower:

- Revit LOA Chat and external AI functions: requires clear privacy policy, network disclosure, terms, cost control and data handling rules.
- RevitAddin.MepBim / MEP·BIM Coordination Console: excluded from the first commercial package by product decision.
- Navisworks tools: submit later as a separate Navisworks product after packaging and version validation.
- Experimental Korean-only workflows such as load calculation and auto drawing: commercialize after documentation and test cases are prepared.
- Any tool with hardcoded local developer paths in `.addin`, `.csproj` or installer logic.

## 2. Store Readiness Gates

The product should not be submitted until all gates are complete:

- Product name, logo, icon, short description and screenshots are final.
- Clean install and uninstall work on a Windows machine without developer folders.
- Supported Revit versions are tested. Claim only versions that were actually tested.
- No hardcoded secrets, activation passwords, local user paths or developer machine paths remain in release builds.
- Any license check uses a server-side or official entitlement flow, not secrets embedded in DLLs.
- If the add-in collects user name, phone, email, machine ID, model data or sends network requests, disclose it in privacy policy and product page.
- Installer includes all dependencies or clearly handles prerequisites such as WebView2 runtime.
- A smoke test checklist is completed for each supported Revit version.
- Support email, user guide, EULA and privacy policy URL are available.

## 3. Launch Phases

### Phase 0 - Publisher Setup

- Create or confirm Autodesk App Store publisher account.
- Decide publisher name: recommended `LUA BIM LABS`.
- Prepare support email, website/product page, privacy policy URL and EULA URL.
- Decide pricing model: recommended subscription app with a 30-day trial.
- First price recommendation: USD 19/month or USD 190/year for individual users.
- Decide supported versions for first release. Recommended initial target: Revit 2024, 2025, 2026 only.

### Phase 1 - Product Hardening

- Remove hardcoded license secrets from the dashboard project.
- Replace local license file logic with a safer activation design.
- Remove local developer paths from manifests and project files.
- Ensure the installer installs to `ProgramData/Autodesk/Revit/Addins` and supports uninstall.
- Disable or hide modules that are not included in the first commercial package.
- Add release configuration that does not copy debug artifacts or source files.
- Add a smoke test document and keep screenshots of test results.

### Phase 2 - Listing Package

- Prepare 5-8 screenshots showing actual Revit workflows.
- Record a 60-120 second demo video.
- Write English Store listing first; Korean can be added later on the product website.
- Prepare user guide PDF or web page.
- Prepare privacy policy, EULA and support runbook.

### Phase 3 - Submission

- Upload app package and listing materials.
- Respond to Autodesk review feedback.
- Track required changes in `docs/autodesk_store/store_tasks.csv`.
- After approval, monitor first-user issues closely and ship a quick patch if needed.

## 4. Knowledge Feedback To AI Dashboard

For monthly AI knowledge updates, add these Store-specific knowledge domains:

- Autodesk App Store compliance and packaging
- Revit API release compatibility
- Navisworks API release compatibility
- BIM/VDC workflow validation
- MEP coordination and clash review
- License, trial, privacy and customer support operations

Each monthly update should refresh official Autodesk references first, then append lessons learned from support tickets, customer feedback and rejected Store review notes.

## 5. Official References

- Autodesk App Store Product Guidelines: https://apps.autodesk.com/en/Publisher/ProductGuidelines
- Autodesk App Store Getting Started Guide: https://aps.autodesk.com/marketplace/marketplace-getting-started
- Autodesk App Store FAQ: https://apps.autodesk.com/EN/Public/FAQ
- Revit add-in registration: https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Introduction/Add_In_Integration/Revit_API_Revit_API_Developers_Guide_Introduction_Add_In_Integration_Add_in_Registration_html.html
- Navisworks API overview: https://aps.autodesk.com/developer/overview/navisworks-api

## 6. Pricing Reference

Detailed subscription pricing is maintained in `docs/autodesk_store/SUBSCRIPTION_PRICING.md`.

## 7. Submission Package

The current working package index is maintained in `docs/autodesk_store/STORE_SUBMISSION_PACKAGE_INDEX.md`.
