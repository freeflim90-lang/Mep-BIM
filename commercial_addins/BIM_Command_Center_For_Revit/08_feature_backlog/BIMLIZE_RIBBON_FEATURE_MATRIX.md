# BIMlize Ribbon Feature Matrix

Status: draft from user-provided screenshot
Last updated: 2026-05-19

## Purpose

This matrix captures the BIMlize for Revit ribbon features shown in the user-provided screenshot. It is an internal benchmark list for original BIM Command Center feature planning.

Do not copy BIMlize names, icons, ribbon layout, command text, help text, or implementation. Use this as a scope map only.

## Screenshot Feature Inventory

| Ribbon group | Screenshot command | Internal BIM Command Center direction | Priority | Notes |
| --- | --- | --- | --- | --- |
| Project | 프로젝트 생성 | Project Starter | P2 | Needs template/project standard policy before implementation |
| 구성 | 유형 일괄정의 | Type Batch Definer | P1 | Good simple start if limited to dry-run and type mapping |
| 구성 | 뷰 템플릿 복사 | View Template Copier | P1 | Low-risk productivity feature with clear QA cases |
| 설정관리 | 설정관리 | Settings Profile Manager | P0 | Non-Revit core can start now with JSON presets |
| 매개변수 | 매개변수 | Parameter Toolkit | P2 | Broad scope; split into audit/export/import later |
| 유틸 | 프로젝트 정리 | Project Cleanup Lite | P1 | Start with audit/report only |
| 유틸 | 패밀리 Export/Import | Family Package Transfer | P2 | Existing dashboard has Family Batch; merge carefully |
| 유틸 | 모델 비교 | Model Compare Report | P2 | Begin with exported metadata comparison |
| 유틸 | 유틸리티 | Utility Hub | P3 | Avoid vague catch-all in commercial UI |
| 일람표 | 일람표 엑셀저장 | Schedule Excel Export | P1 | Can start with CSV/XLSX export spec |
| 일람표 | 일람표 항목처리 | Schedule Item Processor | P2 | Define allowed edit operations first |
| 일람표 | Excel Export/Import | Data Table Sync | P2 | Higher risk because import changes model data |
| 모델 | 모델 처리 | Model Processor | P3 | Too broad; split by real workflow |
| 모델링 | MEP유틸 | MEP Modeling Tools | Excluded v1 | First commercial package excludes MEPBIM-style module |
| 모델링 | MEP유틸2 | MEP Modeling Tools 2 | Excluded v1 | Keep for later separate product if needed |
| 도면화 | 3D 뷰생성 내보내기 | 3D View Export Assistant | P2 | Existing clash/view tooling may cover part of this |
| 도면화 | 태그/문자열 정렬 | Tag/Text Aligner | P1 | Small, visible drafting productivity feature |
| 도면화 | 태그 패밀리 유형정의 | Tag Family Type Mapper | P2 | Useful but needs company standard mapping |
| 태그 | 다중 재료태그 | Multi Material Tagger | P2 | Needs sample project QA |
| 제품인증 | 사용인증(정보) | License Status Panel | P0 | Already aligned with entitlement API direction |
| BIMlize | BIMlize | About/Product Launcher | P3 | Use BIM Command Center branding only |

## Recommended Simple-First Order

1. Settings Profile Manager
2. View Template Copier
3. Type Batch Definer
4. Tag/Text Aligner
5. Project Cleanup Lite audit mode
6. Schedule Excel Export

These are more aligned with the screenshot than the earlier public Store list and can be added to BIM Command Center without changing the commercial licensing direction.

## Existing Dashboard Overlap

- Family Export/Import overlaps with current Family Batch work.
- 3D view creation/export overlaps with clash point and section box workflows.
- Project Cleanup overlaps with Model Health Dashboard.
- License Status Panel overlaps with Autodesk Entitlement API scaffold.
- MEP utility features should stay out of the first commercial package because `RevitAddin.MepBim` is excluded.
