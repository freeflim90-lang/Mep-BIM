---
type: knowledge-map
project: Model Quality Auditor
status: active
node_type: concept
tags:
  - mqa
  - lesson-learned
  - error-fix
  - knowledge-map
created: 2026-05-21
---

# Lessons Learned Matrix

오류 기록을 개발 오답노트에서 조직 지식으로 전환하기 위한 매트릭스다. 개별 오류 노트는 해결 순간에 작성하고, 반복되는 패턴은 이 문서에 모아 기준화한다.

## 지식 전환 흐름

1. `03_Errors_Fixes`에 오류 노트를 작성한다.
2. 원인과 수정이 확정되면 `배운 점`과 `재발 방지 체크`를 채운다.
3. 같은 패턴이 2회 이상 반복되면 아래 매트릭스에 등록한다.
4. Revit API 검증이 필요하면 `05_Revit_API_Gates`에 연결한다.
5. 제품 정책 변경이 필요하면 `04_Decisions`에 연결한다.
6. 전역 지식망 반영이 필요하면 global Obsidian map을 재생성한다.

## 패턴 매트릭스

| 패턴 | 대표 증상 | 원인 분류 | 예방 기준 | 연결 |
|---|---|---|---|---|
| Revit API 환경 경계 | 로컬에서는 판단 불가한 모델 데이터 추출 오류 | `revit-api` | 실제 Revit 가능 환경 전까지 확정 문구 금지 | [[ERR-2026-05-20-001 Revit API Boundary Risk]], [[Revit API Test Gate Index]] |
| Store 기능 문구 불일치 | 판매 문구와 실제 구현 범위가 다름 | `store`, `product` | 기능 확정 전 Store 문구는 베타/제한 표현 사용 | [[Store Package Link]], [[Decision Log Index]] |
| Addin Dashboard 병합 충돌 | 별도 프로젝트 기능이 기존 대시보드 구조와 맞지 않음 | `architecture`, `merge` | 병합 전 인터페이스, 설정, 리포트 출력 경로 정의 | [[Addin Dashboard Merge Plan]] |
| 리포트 수치 신뢰성 문제 | 진단 점수와 실제 모델 품질 체감이 다름 | `qa`, `metric` | 점수 산식, 제외 조건, 경고 기준을 문서화 | [[Build Test Index]] |

## 오류 노트 품질 기준

| 등급 | 조건 | 조치 |
|---|---|---|
| A | 재현, 원인, 수정, 검증, 재발 방지가 모두 명확함 | 표준/체크리스트 후보로 승격 |
| B | 수정은 되었지만 검증 또는 재발 방지가 부족함 | 후속 검증 태스크 등록 |
| C | 증상만 있고 원인/수정이 불명확함 | 임시 기록으로 유지, 원인 확정 전 제품 반영 금지 |

## 연결

- [[Error Fix Index]]
- [[Knowledge Capture Rules]]
- [[Revit API Test Gate Index]]
- [[Decision Log Index]]
- [[Build Test Index]]
