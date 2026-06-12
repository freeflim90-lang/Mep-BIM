---
type: qwen-product-draft
project: Model Quality Auditor
task_id: ADDIN-IDEA-20260603-003
status: generated
external_code_only: true
created: 2026-06-03
tags:
  - qwen
  - mqa
  - backend-draft
  - product-development
---

# ADDIN-IDEA-20260603-003 Navisworks Clash Cause Classifier MVP 초안

선정 아이템: Qwen Coder daily 5-item Revit/Navisworks add-in development pipeline

## 작업 정보

| 항목 | 내용 |
|---|---|
| 산출물 | 간섭 결과를 원인 유형, 책임 공종, 반복 패턴, 회의 우선순위로 분류하는 설정 스키마와 테스트 케이스 |
| 범위 | Navisworks API 호출 없이 Clash Detective export CSV/XML을 가정한 파서 계약과 분류 엔진만 작성한다. |
| 예상 출력 위치 | `backend/product_candidates/clash_cause_classifier.py` |
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
