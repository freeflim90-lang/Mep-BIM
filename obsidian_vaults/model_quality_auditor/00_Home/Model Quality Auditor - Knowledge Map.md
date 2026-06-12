---
type: moc
project: Model Quality Auditor
status: active
node_type: concept
tags:
  - mqa
  - knowledge-map
  - obsidian
created: 2026-05-20
---

# Model Quality Auditor - Knowledge Map

이 문서는 `Model Quality Auditor` 개발 지식의 중심 노드다. 모든 오류, 수정, 의사결정, Revit API 테스트, Qwen 초안은 이 문서 또는 하위 인덱스와 연결한다.

## 핵심 노드

- [[Organizational Knowledge Hierarchy]]
- [[Semantic Node Edge Taxonomy]]
- [[Semantic Knowledge Index]]
- [[Project Overview]]
- [[Separate Project Strategy]]
- [[Qwen Development Boundary]]
- [[Development Logging SOP]]
- [[Error Fix Index]]
- [[Decision Log Index]]
- [[Revit API Test Gate Index]]
- [[Build Test Index]]
- [[Addin Dashboard Merge Plan]]
- [[Store Package Link]]

## 개발 흐름

1. [[Organizational Knowledge Hierarchy]]에서 현재 지식이 어느 업무 분류 아래에 있는지 먼저 확인한다.
2. 오래 살아남을 노트는 [[Semantic Node Edge Taxonomy]] 기준으로 `concept`, `procedure`, `event`, `claim`, `actor` 중 하나로 분류한다.
3. [[Qwen Development Boundary]] 기준으로 Revit API 비의존 코어와 문서를 먼저 만든다.
4. 개발 중 이슈는 [[Error Fix Index]]에 연결하고 `Templates/TEMPLATE_Error_Fix.md`를 사용한다.
5. 아키텍처 결정은 [[Decision Log Index]]에 연결하고 `Templates/TEMPLATE_Decision.md`를 사용한다.
6. Revit API 접근이 필요한 순간에는 [[Revit API Test Gate Index]]로 넘긴다.
7. 실제 Revit 자리에서 빌드/테스트한 결과는 [[Build Test Index]]에 기록한다.
8. 안정화 후 [[Addin Dashboard Merge Plan]]에 따라 패키징 후보로 편입한다.

## 관련 외부 문서

- `docs/revenue_products/model_quality_audit/00_PRODUCT_PACKAGE_INDEX.md`
- `docs/revenue_products/model_quality_audit/11_ADDIN_MVP_FEATURE_SPEC.md`
- `docs/revenue_products/model_quality_audit/12_STORE_SUBMISSION_CHECKLIST.md`
- `docs/revenue_products/model_quality_audit/13_PRODUCT_ROADMAP.md`
