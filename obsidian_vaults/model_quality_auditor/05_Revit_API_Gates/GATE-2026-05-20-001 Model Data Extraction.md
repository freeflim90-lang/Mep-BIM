---
type: revit-api-gate
id: GATE-2026-05-20-001
project: Model Quality Auditor
status: pending
tags:
  - mqa
  - revit-api
  - data-extraction
created: 2026-05-20
---

# GATE-2026-05-20-001 Model Data Extraction

## 검증 목적

Revit 모델에서 품질진단에 필요한 기초 데이터를 안정적으로 추출할 수 있는지 확인한다.

## 검증 대상

- 모델명 및 문서 정보
- Warning 수와 분류
- 링크 모델 상태
- Workset 상태
- 필수 파라미터 누락률
- 뷰/템플릿 기본 상태

## 대기 사유

실제 Revit API 사용 가능 환경에서만 `Document`, `Element`, `FilteredElementCollector` 접근을 확정할 수 있다.

## 연결

- [[Revit API Test Gate Index]]
- [[ERR-2026-05-20-001 Revit API Boundary Risk]]
- [[Build Test Index]]

