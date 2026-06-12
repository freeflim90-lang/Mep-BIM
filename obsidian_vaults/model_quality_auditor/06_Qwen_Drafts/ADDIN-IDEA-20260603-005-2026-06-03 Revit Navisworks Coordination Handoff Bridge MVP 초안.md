---
type: qwen-product-draft
project: Model Quality Auditor
task_id: ADDIN-IDEA-20260603-005
status: generated
external_code_only: true
created: 2026-06-03
tags:
  - qwen
  - mqa
  - backend-draft
  - product-development
---

# ADDIN-IDEA-20260603-005 Revit/Navisworks Coordination Handoff Bridge MVP 초안

선정 아이템: Qwen Coder daily 5-item Revit/Navisworks add-in development pipeline

## 작업 정보

| 항목 | 내용 |
|---|---|
| 산출물 | Revit 모델 QA 결과와 Navisworks 간섭 결과를 하나의 회의 액션 보드로 병합하는 DTO, 상태 전이, 리포트 계약 |
| 범위 | 양쪽 Add-in의 실제 API 어댑터는 경계만 정의하고, JSON/CSV 샘플을 입력받아 통합 액션 목록을 만드는 백엔드 초안을 작성한다. |
| 예상 출력 위치 | `backend/product_candidates/coordination_handoff_bridge.py` |
| Qwen 실행 | 성공 |
| 모델 | qwen2.5-coder:7b |
| 사유 | - |

## Qwen 초안

외부 개발 모드(`CODE_DEV_EXTERNAL_ONLY=true`)에 따라 코드 개발 본문은 Mac mini에 저장하지 않는다.

초안 본문은 Gmail 발송 대상으로만 처리하며, Gmail 설정이 없으면 본문을 폐기하고 재실행해야 한다.

## 연결

- [[Qwen Draft Index]]
- [[Qwen Development Boundary]]
- [[Revit API Test Gate Index]]
- [[Build Test Index]]
