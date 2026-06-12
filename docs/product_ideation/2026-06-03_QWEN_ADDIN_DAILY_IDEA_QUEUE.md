# Qwen Add-in Daily Idea Queue - 2026-06-03

## Purpose

매일 Qwen Coder가 Revit Add-in 및 Navisworks Add-in 상품 후보를 5개씩 개발 초안으로 전환한다. Qwen은 먼저 API 비의존 도메인 모델, 설정 스키마, dry-run 리포트, 테스트 케이스를 만든다.

## Daily Items

| ID | Platform | Item | First Qwen Output |
|---|---|---|---|
| ADDIN-IDEA-20260603-001 | Revit | MEP Access Clearance Auditor | 유지관리 공간 진단 룰과 dry-run 리포트 |
| ADDIN-IDEA-20260603-002 | Revit | Sheet Issue Packager | 시트/뷰 기준 이슈 패키징 계약 |
| ADDIN-IDEA-20260603-003 | Navisworks | Clash Cause Classifier | 간섭 원인/책임/우선순위 분류 엔진 |
| ADDIN-IDEA-20260603-004 | Navisworks | Search Set QA Reporter | Search Set 명명/누락/중복 QA 리포트 |
| ADDIN-IDEA-20260603-005 | Revit + Navisworks | Coordination Handoff Bridge | Revit QA와 Navisworks 간섭 결과 통합 액션 보드 |

## Operating Rule

- Daily runner: `scripts/qwen_product_draft_daily.sh`
- Daily seeder: `scripts/seed_qwen_addin_idea_queue.py`
- Daily quantity: 5 tasks
- Queue: `config/qwen_product_draft_queue.json`
- Draft output: `obsidian_vaults/model_quality_auditor/06_Qwen_Drafts/`
- Revit/Navisworks API implementation is held until the API gate and Windows test environment are ready.
