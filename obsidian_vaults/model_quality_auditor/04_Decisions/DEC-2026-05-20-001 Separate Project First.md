---
type: decision
id: DEC-2026-05-20-001
project: Model Quality Auditor
status: accepted
node_type: claim
tags:
  - mqa
  - decision
  - separate-project
created: 2026-05-20
---

# DEC-2026-05-20-001 Separate Project First

## 결정

`Model Quality Auditor`는 별도 프로젝트로 개발하고, 실제 Revit API 사용 가능 환경에서 빌드/테스트한 뒤 Addin Dashboard에 합쳐서 패키징한다.

## 배경

기존 Addin Dashboard는 Store 제출 후보이므로 검증되지 않은 기능을 즉시 병합하면 패키징 안정성과 심사 리스크가 커진다.

## 결과

- Qwen 개발은 별도 프로젝트 초안과 순수 로직 중심으로 진행한다.
- Revit API 검증은 별도 게이트로 남긴다.
- 병합 여부는 테스트 증빙 이후 결정한다.

## 연결

- [[Separate Project Strategy]]
- [[Qwen Development Boundary]]
- [[Addin Dashboard Merge Plan]]
