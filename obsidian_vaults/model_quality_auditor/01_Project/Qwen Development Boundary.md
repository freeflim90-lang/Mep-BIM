---
type: boundary
project: Model Quality Auditor
owner: Qwen_Coder_8B
status: active
node_type: procedure
tags:
  - qwen
  - mqa
  - development-boundary
created: 2026-05-20
---

# Qwen Development Boundary

Qwen은 `Model Quality Auditor` 개발에서 로컬 1차 구현 초안과 테스트 가능한 순수 로직을 담당한다.

## Qwen이 담당하는 범위

- Revit API 비의존 도메인 모델
- 진단 규칙 JSON 스키마
- 점수 계산 로직
- CSV/Markdown 리포트 생성
- 샘플 입력 데이터와 단위 테스트
- Store 문서, QA 체크리스트, 개발 로그 초안
- 조직에서 선정한 수익형 아이템 기준 백엔드 개발 초안 큐 수행
- 초안 완료 후 Telegram 중간보고 및 다음 초안 업무 연결

## Qwen이 확정하지 않는 범위

- Revit API 호출
- `Document`, `Element`, `FilteredElementCollector` 접근
- Transaction이 필요한 모델 변경
- 실제 Revit 버전 호환성
- Autodesk App Store 최종 제출 가능 여부

## Revit API 게이트

Revit API 접근이 필요한 작업은 [[Revit API Test Gate Index]]에 등록하고, 실제 Revit 사용 가능 환경에서 빌드/테스트 후 확정한다.

## 선정 아이템 기반 순차 초안 프로세스

Qwen 담당자는 `config/qwen_product_draft_queue.json`에 등록된 `Model Quality Auditor` 백엔드 초안 큐를 기준으로 작업한다.

| 단계 | 작업 | 산출물 |
|---|---|---|
| 1 | 다음 미완료 Task 확인 | `qwen_product_draft_state.json` |
| 2 | 상품 패키지 문서와 개발 경계 읽기 | 개발 초안 프롬프트 |
| 3 | Qwen 로컬 초안 작성 | `06_Qwen_Drafts/MQA-QWEN-*.md` |
| 4 | Telegram 중간보고 | 완료 작업, 기록 위치, 다음 작업 |
| 5 | 다음 Task 대기 또는 연속 실행 | 다음 초안 업무 |

수동 실행:

```bash
source .dev-venv/bin/activate && LOCAL_CODER_ENABLED=true python scripts/qwen_product_draft_runner.py
```

Telegram 없이 검증:

```bash
source .dev-venv/bin/activate && LOCAL_CODER_ENABLED=true python scripts/qwen_product_draft_runner.py --no-telegram
```

백엔드 API:

- `GET /api/qwen-product-drafts/status`
- `POST /api/qwen-product-drafts/next`

## 연결

- [[Development Logging SOP]]
- [[Error Fix Index]]
- [[Build Test Index]]
- [[Revit API Test Gate Index]]
- [[Qwen Draft Index]]
