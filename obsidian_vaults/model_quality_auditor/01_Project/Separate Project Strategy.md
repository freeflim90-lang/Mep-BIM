---
type: decision-context
project: Model Quality Auditor
status: active
node_type: claim
tags:
  - mqa
  - architecture
  - separate-project
created: 2026-05-20
---

# Separate Project Strategy

## 결정

`Model Quality Auditor`는 초기 개발을 별도 프로젝트로 진행한다.

## 이유

- 기존 `Addin Dashboard` 상용 패키지 안정성을 유지한다.
- Revit API 가능한 자리에서 빌드/테스트하기 전까지 위험한 의존성을 분리한다.
- Qwen은 순수 로직, 문서, 테스트 가능한 구조 초안에 집중한다.
- 검증 후 Addin Dashboard에 합치는 편이 Store 제출 리스크를 낮춘다.

## 연결

- [[Qwen Development Boundary]]
- [[Revit API Test Gate Index]]
- [[Addin Dashboard Merge Plan]]
- [[DEC-2026-05-20-001 Separate Project First]]
