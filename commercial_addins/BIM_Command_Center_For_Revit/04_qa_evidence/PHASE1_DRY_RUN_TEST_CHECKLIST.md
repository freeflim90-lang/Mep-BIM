# Phase 1 Dry-Run Test Checklist

Status: ready for owner build/test on Revit machine
Last updated: 2026-05-19

## Build Target

Source:

External add-in development source root:

`$BCC_ADDIN_DEV_SOURCE_ROOT/01_Revit_Addins/Addin Dashboard`

Expected new dashboard group:

`Commercial Phase 1`

Expected new commands:

- 설정 프로필 관리
- 뷰 템플릿 복사 검토
- 유형 일괄정의 검토
- 태그/문자열 정렬 검토
- 프로젝트 정리 감사
- 일람표 엑셀저장 검토

## Build Notes

- Build must be run on a Windows machine with Revit API DLLs available.
- Local Mac validation completed only for JSON/XML structure.
- These commands are dry-run only and should not modify the Revit model.

## Smoke Test

1. Build `BIMCommandCenter.csproj`.
2. Confirm output contains:
   - `commands.json`
   - `license-settings.json`
   - `CommercialFeatures/Configs/settings_profile_sample.json`
   - `CommercialFeatures/Configs/view_template_copy_rules.json`
   - `CommercialFeatures/Configs/type_batch_definitions.json`
   - `CommercialFeatures/Configs/tag_text_aligner_rules.json`
   - `CommercialFeatures/Configs/project_cleanup_rules.json`
   - `CommercialFeatures/Configs/schedule_excel_export_rules.json`
3. Open Revit and load BIM Command Center.
4. Confirm `Commercial Phase 1` appears in the dashboard.
5. Run `설정 프로필 관리`.
   - Expected: profile path and feature list appear.
   - Expected: `%AppData%/LUA BIM LABS/BIM Command Center/Profiles/office_default_profile.json` is created.
6. Open any Revit model and run `뷰 템플릿 복사 검토`.
   - Expected: view template count appears.
   - Expected: no templates are copied.
7. Run `유형 일괄정의 검토`.
   - Expected: type definition rows appear.
   - Expected: no types are created or modified.
8. Select text notes or tags and run `태그/문자열 정렬 검토`.
   - Expected: selection count and supported annotation count appear.
   - Expected: no annotations move.
9. Run `프로젝트 정리 감사`.
   - Expected: warning/import/view/template/schedule counts appear.
   - Expected: no cleanup action runs.
10. Open a schedule view and run `일람표 엑셀저장 검토`.
   - Expected: schedule name, field count, body rows and body columns appear.
   - Expected: no CSV/XLSX file is written.

## Pass Criteria

- No command crashes Revit.
- All six commands show TaskDialog output.
- No Revit model element is created, deleted, moved, or modified.
- The generated profile JSON can be opened and edited manually.
