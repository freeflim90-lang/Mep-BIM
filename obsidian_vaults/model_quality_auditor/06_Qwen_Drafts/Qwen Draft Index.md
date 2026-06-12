---
type: index
project: Model Quality Auditor
status: active
tags:
  - mqa
  - qwen
  - drafts
created: 2026-05-20
---

# Qwen Draft Index

Qwen이 생성한 초안, 순수 로직 설계, 테스트 가능한 구조를 모은다.

## 기록 대상

- 도메인 모델 초안
- 규칙 JSON 스키마
- 점수 계산 로직
- 리포트 생성 로직
- 단위 테스트 계획
- Revit API 어댑터 인터페이스 초안
- Add-in Dashboard 병합 백엔드 계약 초안

## 순차 초안 큐

현재 활성 조직 선정 아이템은 `BIM Command Center for Revit - BIMlize 기능 범위 내재화`이며, Qwen 담당자는 `config/qwen_product_draft_queue.json`의 작업 순서에 따라 백엔드 초안을 작성한다. 이전 `Model Quality Auditor` 큐는 `config/qwen_mqa_product_draft_queue.json`에 보관한다.

| 항목 | 기준 |
|---|---|
| 실행 스크립트 | `scripts/qwen_product_draft_runner.py` |
| 큐 설정 | `config/qwen_product_draft_queue.json` |
| 상태 파일 | `06_Qwen_Drafts/qwen_product_draft_queue_state.json` |
| 중간보고 | Telegram `sendMessage` |
| 백엔드 API | `/api/qwen-product-drafts/status`, `/api/qwen-product-drafts/next` |

완료된 초안은 아래 `생성된 초안` 섹션에 자동으로 연결한다.

## 연결

- [[Qwen Development Boundary]]
- [[Development Logging SOP]]
- [[Error Fix Index]]

## 생성된 초안
- [[MQA-QWEN-001-2026-05-21 도메인 모델 및 데이터 계약 초안]] — `MQA-QWEN-001-2026-05-21 도메인 모델 및 데이터 계약 초안.md`
- [[MQA-QWEN-002-2026-05-21 품질진단 룰 JSON 스키마 초안]] — `MQA-QWEN-002-2026-05-21 품질진단 룰 JSON 스키마 초안.md`
- [[BIMLIZE-QWEN-001-2026-05-21 BIMlize 기능 내재화 백엔드 원칙 및 기능 레지스트리 초안]] — `BIMLIZE-QWEN-001-2026-05-21 BIMlize 기능 내재화 백엔드 원칙 및 기능 레지스트리 초안.md`
- [[BIMLIZE-QWEN-002-2026-05-21 Settings Profile Manager 백엔드 초안]] — `BIMLIZE-QWEN-002-2026-05-21 Settings Profile Manager 백엔드 초안.md`
- [[BIMLIZE-QWEN-003-2026-05-24 View Template Copier dry-run 계약 초안]] — `BIMLIZE-QWEN-003-2026-05-24 View Template Copier dry-run 계약 초안.md`
- [[BIMLIZE-QWEN-004-2026-05-24 Type Batch Definer mapping 계약 초안]] — `BIMLIZE-QWEN-004-2026-05-24 Type Batch Definer mapping 계약 초안.md`
- [[BIMLIZE-QWEN-005-2026-05-24 Tag Text Aligner geometry preview 초안]] — `BIMLIZE-QWEN-005-2026-05-24 Tag Text Aligner geometry preview 초안.md`
- [[BIMLIZE-QWEN-006-2026-05-24 Project Cleanup Lite audit report 초안]] — `BIMLIZE-QWEN-006-2026-05-24 Project Cleanup Lite audit report 초안.md`
- [[BIMLIZE-QWEN-007-2026-05-24 Schedule Excel Export 계약 초안]] — `BIMLIZE-QWEN-007-2026-05-24 Schedule Excel Export 계약 초안.md`
- [[NAV-001-2026-05-28 제품 문제 정의 및 MVP Pro 범위 초안]] — `NAV-001-2026-05-28 제품 문제 정의 및 MVP Pro 범위 초안.md`
- [[NAV-002-2026-05-29 도메인 모델 및 설정 스키마 초안]] — `NAV-002-2026-05-29 도메인 모델 및 설정 스키마 초안.md`
- [[NAV-003-2026-05-30 Dry-run 및 리포트 계약 초안]] — `NAV-003-2026-05-30 Dry-run 및 리포트 계약 초안.md`
- [[NAV-004-2026-05-31 테스트 케이스 및 실패 오답노트 템플릿 초안]] — `NAV-004-2026-05-31 테스트 케이스 및 실패 오답노트 템플릿 초안.md`
- [[NAV-005-2026-06-01 Revit API 게이트 및 Store 패키징 계약 초안]] — `NAV-005-2026-06-01 Revit API 게이트 및 Store 패키징 계약 초안.md`
- [[ADDIN-IDEA-20260603-001-2026-06-03 Revit MEP Access Clearance Auditor MVP 초안]] — `ADDIN-IDEA-20260603-001-2026-06-03 Revit MEP Access Clearance Auditor MVP 초안.md`
- [[ADDIN-IDEA-20260603-002-2026-06-03 Revit Sheet Issue Packager MVP 초안]] — `ADDIN-IDEA-20260603-002-2026-06-03 Revit Sheet Issue Packager MVP 초안.md`
- [[ADDIN-IDEA-20260603-003-2026-06-03 Navisworks Clash Cause Classifier MVP 초안]] — `ADDIN-IDEA-20260603-003-2026-06-03 Navisworks Clash Cause Classifier MVP 초안.md`
- [[ADDIN-IDEA-20260603-004-2026-06-03 Navisworks Search Set QA Reporter MVP 초안]] — `ADDIN-IDEA-20260603-004-2026-06-03 Navisworks Search Set QA Reporter MVP 초안.md`
- [[ADDIN-IDEA-20260603-005-2026-06-03 Revit Navisworks Coordination Handoff Bridge MVP 초안]] — `ADDIN-IDEA-20260603-005-2026-06-03 Revit Navisworks Coordination Handoff Bridge MVP 초안.md`
- [[ADDIN-IDEA-20260604-001-2026-06-04 Revit Workset Hygiene Auditor MVP 초안]] — `ADDIN-IDEA-20260604-001-2026-06-04 Revit Workset Hygiene Auditor MVP 초안.md`
- [[ADDIN-IDEA-20260604-002-2026-06-04 Revit Family Connector QA MVP 초안]] — `ADDIN-IDEA-20260604-002-2026-06-04 Revit Family Connector QA MVP 초안.md`
- [[ADDIN-IDEA-20260604-003-2026-06-04 Navisworks Weekly Clash Delta Reporter MVP 초안]] — `ADDIN-IDEA-20260604-003-2026-06-04 Navisworks Weekly Clash Delta Reporter MVP 초안.md`
- [[ADDIN-IDEA-20260604-004-2026-06-04 Navisworks Viewpoint Meeting Pack Builder MVP 초안]] — `ADDIN-IDEA-20260604-004-2026-06-04 Navisworks Viewpoint Meeting Pack Builder MVP 초안.md`
- [[ADDIN-IDEA-20260604-005-2026-06-04 Revit Navisworks Issue Status Sync Contract MVP 초안]] — `ADDIN-IDEA-20260604-005-2026-06-04 Revit Navisworks Issue Status Sync Contract MVP 초안.md`
- [[ADDIN-IDEA-20260606-001-2026-06-06 Revit Workset Hygiene Auditor MVP 초안]] — `ADDIN-IDEA-20260606-001-2026-06-06 Revit Workset Hygiene Auditor MVP 초안.md`
- [[ADDIN-IDEA-20260606-002-2026-06-06 Revit Family Connector QA MVP 초안]] — `ADDIN-IDEA-20260606-002-2026-06-06 Revit Family Connector QA MVP 초안.md`
- [[ADDIN-IDEA-20260606-003-2026-06-06 Navisworks Weekly Clash Delta Reporter MVP 초안]] — `ADDIN-IDEA-20260606-003-2026-06-06 Navisworks Weekly Clash Delta Reporter MVP 초안.md`
- [[ADDIN-IDEA-20260606-004-2026-06-06 Navisworks Viewpoint Meeting Pack Builder MVP 초안]] — `ADDIN-IDEA-20260606-004-2026-06-06 Navisworks Viewpoint Meeting Pack Builder MVP 초안.md`
- [[ADDIN-IDEA-20260606-005-2026-06-06 Revit Navisworks Issue Status Sync Contract MVP 초안]] — `ADDIN-IDEA-20260606-005-2026-06-06 Revit Navisworks Issue Status Sync Contract MVP 초안.md`
- [[ADDIN-IDEA-20260609-001-2026-06-09 Revit MEP Access Clearance Auditor MVP 초안]] — `ADDIN-IDEA-20260609-001-2026-06-09 Revit MEP Access Clearance Auditor MVP 초안.md`
- [[ADDIN-IDEA-20260609-002-2026-06-09 Revit Sheet Issue Packager MVP 초안]] — `ADDIN-IDEA-20260609-002-2026-06-09 Revit Sheet Issue Packager MVP 초안.md`
- [[ADDIN-IDEA-20260609-003-2026-06-09 Navisworks Clash Cause Classifier MVP 초안]] — `ADDIN-IDEA-20260609-003-2026-06-09 Navisworks Clash Cause Classifier MVP 초안.md`
- [[ADDIN-IDEA-20260609-004-2026-06-09 Navisworks Search Set QA Reporter MVP 초안]] — `ADDIN-IDEA-20260609-004-2026-06-09 Navisworks Search Set QA Reporter MVP 초안.md`
- [[ADDIN-IDEA-20260609-005-2026-06-09 Revit Navisworks Coordination Handoff Bridge MVP 초안]] — `ADDIN-IDEA-20260609-005-2026-06-09 Revit Navisworks Coordination Handoff Bridge MVP 초안.md`
- [[ADDIN-IDEA-20260610-001-2026-06-10 Revit Workset Hygiene Auditor MVP 초안]] — `ADDIN-IDEA-20260610-001-2026-06-10 Revit Workset Hygiene Auditor MVP 초안.md`
- [[ADDIN-IDEA-20260610-002-2026-06-10 Revit Family Connector QA MVP 초안]] — `ADDIN-IDEA-20260610-002-2026-06-10 Revit Family Connector QA MVP 초안.md`
- [[ADDIN-IDEA-20260610-003-2026-06-10 Navisworks Weekly Clash Delta Reporter MVP 초안]] — `ADDIN-IDEA-20260610-003-2026-06-10 Navisworks Weekly Clash Delta Reporter MVP 초안.md`
- [[ADDIN-IDEA-20260610-004-2026-06-10 Navisworks Viewpoint Meeting Pack Builder MVP 초안]] — `ADDIN-IDEA-20260610-004-2026-06-10 Navisworks Viewpoint Meeting Pack Builder MVP 초안.md`
- [[ADDIN-IDEA-20260610-005-2026-06-10 Revit Navisworks Issue Status Sync Contract MVP 초안]] — `ADDIN-IDEA-20260610-005-2026-06-10 Revit Navisworks Issue Status Sync Contract MVP 초안.md`
- [[ADDIN-IDEA-20260611-001-2026-06-11 Revit MEP Access Clearance Auditor MVP 초안]] — `ADDIN-IDEA-20260611-001-2026-06-11 Revit MEP Access Clearance Auditor MVP 초안.md`
- [[ADDIN-IDEA-20260611-002-2026-06-11 Revit Sheet Issue Packager MVP 초안]] — `ADDIN-IDEA-20260611-002-2026-06-11 Revit Sheet Issue Packager MVP 초안.md`
- [[ADDIN-IDEA-20260611-003-2026-06-11 Navisworks Clash Cause Classifier MVP 초안]] — `ADDIN-IDEA-20260611-003-2026-06-11 Navisworks Clash Cause Classifier MVP 초안.md`
- [[ADDIN-IDEA-20260611-004-2026-06-11 Navisworks Search Set QA Reporter MVP 초안]] — `ADDIN-IDEA-20260611-004-2026-06-11 Navisworks Search Set QA Reporter MVP 초안.md`
- [[ADDIN-IDEA-20260611-005-2026-06-11 Revit Navisworks Coordination Handoff Bridge MVP 초안]] — `ADDIN-IDEA-20260611-005-2026-06-11 Revit Navisworks Coordination Handoff Bridge MVP 초안.md`
- [[ADDIN-IDEA-20260612-001-2026-06-12 Revit Workset Hygiene Auditor MVP 초안]] — `ADDIN-IDEA-20260612-001-2026-06-12 Revit Workset Hygiene Auditor MVP 초안.md`
- [[ADDIN-IDEA-20260612-002-2026-06-12 Revit Family Connector QA MVP 초안]] — `ADDIN-IDEA-20260612-002-2026-06-12 Revit Family Connector QA MVP 초안.md`
- [[ADDIN-IDEA-20260612-003-2026-06-12 Navisworks Weekly Clash Delta Reporter MVP 초안]] — `ADDIN-IDEA-20260612-003-2026-06-12 Navisworks Weekly Clash Delta Reporter MVP 초안.md`
- [[ADDIN-IDEA-20260612-004-2026-06-12 Navisworks Viewpoint Meeting Pack Builder MVP 초안]] — `ADDIN-IDEA-20260612-004-2026-06-12 Navisworks Viewpoint Meeting Pack Builder MVP 초안.md`
- [[ADDIN-IDEA-20260612-005-2026-06-12 Revit Navisworks Issue Status Sync Contract MVP 초안]] — `ADDIN-IDEA-20260612-005-2026-06-12 Revit Navisworks Issue Status Sync Contract MVP 초안.md`
