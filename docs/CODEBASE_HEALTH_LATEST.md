# LUA BIM LABS Codebase Health Report

## Summary

- tracked_text_files_scanned: 9083
- code_lines: 60829
- doc_lines: 609444
- first_party_code_lines: 57282
- backend_lines: 11283
- script_lines: 34175
- test_lines: 2603
- test_to_backend_ratio_percent: 23.07
- test_to_first_party_code_ratio_percent: 4.54

## Excluded Reference Paths

- `knowledge/50_domain/bim_scripts/`

## Largest Files

- `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/BIMobject/BIMobject - 위생 패밀리.md`: 10032 lines
- `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/BIMobject/BIMobject - 가구 패밀리.md`: 10022 lines
- `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/BIMobject/위생/수도꼭지 패밀리.md`: 10022 lines
- `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/BIMobject/BIMobject - 조명 패밀리.md`: 9113 lines
- `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/BIMobject/BIMobject - 배관 패밀리.md`: 8886 lines
- `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/BIMobject/BIMobject - 공조(HVAC) 패밀리.md`: 6999 lines
- `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/BIMobject/BIMobject - 건축자재 패밀리.md`: 6088 lines
- `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/BIMobject/위생/욕실소품 패밀리.md`: 5909 lines
- `website/index.html`: 5369 lines
- `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/BIMobject/위생/샤워실 패밀리.md`: 5308 lines

## Risks

- HIGH `large_modules`: 32 code files are 500+ lines. Action: Extract pure helpers and route/service modules, keeping tests green after each move.
- MEDIUM `repository_boundary`: Data/knowledge/vendor material is larger than backend source. Action: Keep runtime/vendor data ignored or moved behind explicit import/export workflows.
- MEDIUM `automation_surface`: Automation scripts are much larger than their tests. Action: Promote reusable script logic into small modules and test the scheduling-critical paths.

## Growth Opportunities

- `commercial_reliability`: Treat LUAChat/Revit Assistant as an operational product surface with health, auth, and feedback tests. Next: Review recurring LUAChat support backlog items weekly and convert approved items into customer-facing FAQ pages.
- `knowledge_productization`: Use the knowledge base as reusable product collateral instead of passive notes. Next: Generate service FAQ, sales snippets, and Revit add-in support answers from approved knowledge only.
- `automation_roi`: Standardize high-frequency scripts behind make targets and measurable outputs. Next: Add make targets for market briefing, knowledge curation, and add-in readiness audit with dry-run modes.
- `engineering_velocity`: Reducing `server_total.py` responsibility will make feature delivery less risky. Next: Continue extracting the next high-traffic API area from `server_total.py` into router/controller/service modules.
