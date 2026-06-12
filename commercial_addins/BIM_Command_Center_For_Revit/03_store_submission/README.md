# Store Submission

Generated Autodesk Store upload handoff packages go here.

Use from repository root:

```bash
python3 scripts/prepare_autodesk_store_upload_package.py \
  --installer "commercial_addins/BIM_Command_Center_For_Revit/02_build_artifacts/BIMCommandCenter_Setup_v1.0.0.exe" \
  --icon "commercial_addins/BIM_Command_Center_For_Revit/01_release_inputs/icon.png" \
  --screenshots "commercial_addins/BIM_Command_Center_For_Revit/01_release_inputs/screenshots" \
  --video "commercial_addins/BIM_Command_Center_For_Revit/01_release_inputs/demo-url.txt" \
  --out "commercial_addins/BIM_Command_Center_For_Revit/03_store_submission/autodesk_store_upload_v1_0"
```

Final upload to Autodesk Publisher Center is manual.
