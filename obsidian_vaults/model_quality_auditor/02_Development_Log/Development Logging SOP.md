---
type: sop
project: Model Quality Auditor
status: active
node_type: procedure
tags:
  - mqa
  - development-log
  - sop
created: 2026-05-20
---

# Development Logging SOP

개발 중 남길 기록은 네 종류로 나눈다.

| 기록 | 위치 | 템플릿 |
|---|---|---|
| 일일 개발 로그 | `02_Development_Log/` | `TEMPLATE_Dev_Log.md` |
| 오류/수정 기록 | `03_Errors_Fixes/` | `TEMPLATE_Error_Fix.md` |
| 의사결정 기록 | `04_Decisions/` | `TEMPLATE_Decision.md` |
| Revit API 테스트 | `05_Revit_API_Gates/` | `TEMPLATE_Revit_API_Test.md` |
| Qwen 상품 초안 | `06_Qwen_Drafts/` | `scripts/qwen_product_draft_runner.py` |

## 기록 원칙

1. 오류는 증상, 원인, 수정, 재발방지, 연결 노드를 반드시 남긴다.
2. 수정은 단순 해결만 쓰지 않고 “다음에 재사용할 판단 기준”까지 적는다.
3. Revit API가 필요한 내용은 추정으로 확정하지 않는다.
4. Qwen이 만든 초안은 검증 상태를 표시한다.
5. Addin Dashboard 병합 가능성에 영향을 주는 항목은 [[Addin Dashboard Merge Plan]]과 연결한다.

## 연결

- [[Error Fix Index]]
- [[Decision Log Index]]
- [[Revit API Test Gate Index]]
- [[Qwen Development Boundary]]
- [[Qwen Draft Index]]
