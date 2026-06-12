# Autodesk Store Readiness Audit

- Generated: 2026-05-19 10:00:31
- Source: `$BCC_ADDIN_DEV_SOURCE_ROOT`
- Products scanned: 23

## Recommended Launch Order

1. **Model Health Dashboard** (Revit) - score 85/100
   - Blockers: Suspicious ProjectReference path
   - Next: Add smoke/regression test checklist; Prepare privacy policy/network disclosure
2. **Addin Dashboard** (Revit) - score 80/100
   - Next: Write README/user guide; Add smoke/regression test checklist; Prepare privacy policy/network disclosure
3. **MEP Splitter** (Revit) - score 80/100
   - Blockers: Suspicious ProjectReference path
   - Next: Write README/user guide; Verify latest supported Autodesk version
4. **Revit Auto Save** (Revit) - score 80/100
   - Next: Write README/user guide; Add smoke/regression test checklist
5. **Auto Tagging Dimensioning** (Revit) - score 75/100
   - Next: Create customer-friendly installer/uninstaller; Add smoke/regression test checklist
6. **Filter Utility Summary** (Revit) - score 75/100
   - Blockers: Suspicious ProjectReference path
   - Next: Write README/user guide; Add smoke/regression test checklist
7. **REVIT CRASH POINT** (Revit) - score 75/100
   - Blockers: Suspicious ProjectReference path
   - Next: Write README/user guide; Add smoke/regression test checklist
8. **To Do List** (Revit) - score 75/100
   - Blockers: Suspicious ProjectReference path
   - Next: Write README/user guide; Add smoke/regression test checklist
9. **Workset Dashboard** (Revit) - score 75/100
   - Blockers: Suspicious ProjectReference path
   - Next: Write README/user guide; Add smoke/regression test checklist; Prepare privacy policy/network disclosure
10. **Crash Point Photo** (Revit) - score 70/100
   - Blockers: Suspicious ProjectReference path
   - Next: Write README/user guide; Add smoke/regression test checklist; Verify latest supported Autodesk version; Prepare privacy policy/network disclosure

## Product Inventory

| Platform | Product | Score | Versions | Installer | README | License | Blockers |
|---|---:|---:|---|---:|---:|---:|---|
| Revit | Model Health Dashboard | 85 | 2019, 2024, 2026 | 3 | 1 | Y | Suspicious ProjectReference path |
| Revit | Addin Dashboard | 80 | 2019, 2024, 2025, 2026 | 3 | 0 | Y | - |
| Revit | MEP Splitter | 80 | 2021, 2024 | 6 | 0 | Y | Suspicious ProjectReference path |
| Revit | Revit Auto Save | 80 | 2019, 2024, 2025, 2026 | 1 | 0 | Y | - |
| Revit | Auto Tagging Dimensioning | 75 | 2024, 2025 | 0 | 1 | Y | - |
| Revit | Filter Utility Summary | 75 | 2023, 2024, 2025 | 4 | 0 | Y | Suspicious ProjectReference path |
| Revit | REVIT CRASH POINT | 75 | 2022, 2023, 2024, 2025, 2026 | 5 | 0 | Y | Suspicious ProjectReference path |
| Revit | To Do List | 75 | 2019, 2024, 2025, 2026 | 2 | 0 | Y | Suspicious ProjectReference path |
| Revit | Workset Dashboard | 75 | 2026 | 2 | 0 | Y | Suspicious ProjectReference path |
| Revit | Crash Point Photo | 70 | 2024 | 6 | 0 | Y | Suspicious ProjectReference path |
| Navisworks | Navisworks Auto SearchSet | 70 | 2023 | 2 | 0 | Y | Suspicious ProjectReference path |
| Revit | Family Plan Batch | 60 | 2024 | 7 | 0 | Y | Hardcoded local/user paths in manifests or projects; Suspicious ProjectReference path |
| Revit | Multi File Upgrade | 60 | 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 | 6 | 0 | Y | Suspicious ProjectReference path |
| Revit | PlumbingFlexPipe | 60 | 2024 | 0 | 1 | N | - |
| Revit | RevitLOAChat | 60 | 2019, 2023, 2024, 2025, 2026 | 3 | 0 | N | Hardcoded local/user paths in manifests or projects |
| Revit | RevitAddin.MepBim | 55 | 2019, 2022, 2023, 2024, 2025, 2026 | 0 | 0 | N | - |
| Revit | Project Unit Conversion | 50 | 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 | 6 | 0 | Y | Hardcoded local/user paths in manifests or projects; Suspicious ProjectReference path |
| Revit | 부하계산 | 50 | 2024 | 0 | 0 | N | - |
| Revit | 자동 도면화 | 40 | 2019, 2021, 2024 | 0 | 0 | N | Hardcoded local/user paths in manifests or projects |
| Navisworks | Naviswork Data Heatmap | 30 | 2023 | 0 | 0 | N | Hardcoded local/user paths in manifests or projects; Suspicious ProjectReference path |
| Revit | Crash Point 3D Section Box | 20 | - | 0 | 0 | N | No csproj found |
| Revit | docs | 20 | - | 0 | 0 | N | No csproj found |
| Revit | mep final VER1.1 | 20 | - | 0 | 0 | N | No csproj found |

## Store Submission Gate

A product is not ready to submit until all of these are complete:

- One clear product name and value proposition.
- Installer and uninstaller tested on a clean Windows machine.
- Revit/Navisworks latest supported version verified.
- No hardcoded developer/local paths in manifests or project files.
- No undocumented Autodesk API usage.
- Privacy policy prepared if network, cloud, telemetry or customer model data is used.
- Support email and user guide prepared.
- Smoke-test evidence captured for each supported Autodesk version.
- Listing screenshots and short demo video prepared.
