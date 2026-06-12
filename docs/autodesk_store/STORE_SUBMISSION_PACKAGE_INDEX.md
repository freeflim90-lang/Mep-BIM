# Store Submission Package Index

Use this file as the working index before uploading to Autodesk Store.

Commercial release workspace:

`commercial_addins/BIM_Command_Center_For_Revit`

## Ready Drafts

- `STORE_FORM_FIELD_VALUES.md`
- `BIM_COMMAND_CENTER_STORE_LISTING_DRAFT.md`
- `SUBSCRIPTION_PRICING.md`
- `PRIVACY_POLICY_DRAFT.md`
- `EULA_DRAFT.md`
- `USER_GUIDE_DRAFT.md`
- `SUPPORT_RUNBOOK.md`
- `SUPPORT_EMAIL_TEMPLATES.md`
- `RELEASE_NOTES_V1_0.md`
- `QA_SMOKE_TEST_PLAN.md`
- `SCREENSHOT_VIDEO_SHOTLIST.md`
- `ENTITLEMENT_API_IMPLEMENTATION.md`
- `SUBSCRIPTION_ACCOUNT_PAYMENT_RISK.md`
- `AUTODESK_STORE_ACTUAL_WORKFLOW.md`
- `UPLOAD_AUTOMATION_POLICY.md`

## Missing Inputs From Owner

- Final support email
- Product website URL
- Privacy policy public URL
- EULA public URL
- Autodesk Store App ID
- Final Revit version QA evidence
- Final installer package
- Product icon
- Screenshots
- Demo video
- Payment/tax setup confirmation
- PayPal Business/Premier account or BlueSnap setup confirmation
- Decision: PayPal or BlueSnap for first launch

## Do Not Upload Until

- Windows release build is complete.
- Owner completes Revit/Navisworks API dependent validation on Autodesk-installed machine.
- `license-settings.json` contains the final Autodesk Store App ID.
- Installer and uninstaller are tested on clean Windows/Revit environments.
- Screenshots do not show confidential project data or excluded tools.
- Store listing does not mention `RevitAddin.MepBim`, external AI/chat workflows or Navisworks tools as included features.
- Payment type is final before selecting `Subscription`, because Autodesk documentation says it cannot be changed after selecting Subscription.

## Local Package Automation

Use `scripts/prepare_autodesk_store_upload_package.py` to create a local handoff ZIP after the final installer, icon and screenshots are available.

Example:

```bash
python3 scripts/prepare_autodesk_store_upload_package.py \
  --installer "commercial_addins/BIM_Command_Center_For_Revit/02_build_artifacts/BIMCommandCenter_Setup_v1.0.0.exe" \
  --icon "commercial_addins/BIM_Command_Center_For_Revit/01_release_inputs/icon.png" \
  --screenshots "commercial_addins/BIM_Command_Center_For_Revit/01_release_inputs/screenshots" \
  --video "commercial_addins/BIM_Command_Center_For_Revit/01_release_inputs/demo-url.txt" \
  --out "commercial_addins/BIM_Command_Center_For_Revit/03_store_submission/autodesk_store_upload_v1_0"
```

The script prepares files for manual Publisher Center upload. It does not submit to Autodesk automatically.
