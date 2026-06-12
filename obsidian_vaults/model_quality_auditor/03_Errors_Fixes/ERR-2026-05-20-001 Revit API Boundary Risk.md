---
type: error-fix
id: ERR-2026-05-20-001
project: Model Quality Auditor
severity: major
status: open
node_type: event
tags:
  - mqa
  - error/revit-api
  - qwen
created: 2026-05-20
---

# ERR-2026-05-20-001 Revit API Boundary Risk

## 증상

별도 프로젝트 개발 초기에 Revit API가 필요한 기능과 Qwen이 로컬에서 작성 가능한 순수 로직 범위가 섞일 위험이 있다.

## 원인

`Model Quality Auditor`는 Revit 모델 데이터를 다루는 제품이지만, 현재 개발 환경에서는 실제 Revit API 실행 검증을 확정할 수 없다.

## 수정 방향

- Qwen은 도메인 모델, 규칙 스키마, 점수 계산, 리포트 생성까지만 작성한다.
- Revit API 호출부는 인터페이스 또는 어댑터 경계로 분리한다.
- 실제 `Document`, `Element`, `FilteredElementCollector` 사용은 [[Revit API Test Gate Index]]에 등록한다.

## 재발 방지

새 기능 명세를 작성할 때 `Revit API 필요 여부` 필드를 필수로 둔다.

## 연결

- [[Qwen Development Boundary]]
- [[Revit API Test Gate Index]]
- [[Separate Project Strategy]]
