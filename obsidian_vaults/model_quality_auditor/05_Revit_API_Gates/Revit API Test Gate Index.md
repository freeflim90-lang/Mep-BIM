---
type: index
project: Model Quality Auditor
status: active
node_type: procedure
tags:
  - mqa
  - revit-api
  - test-gate
created: 2026-05-20
---

# Revit API Test Gate Index

Revit API 접근이 필요한 항목은 여기에서 대기시킨 뒤 실제 Revit 사용 가능 환경에서 검증한다.

## 테스트 대기 항목

- [[GATE-2026-05-20-001 Model Data Extraction]]

## 게이트 통과 기준

| 기준 | 설명 |
|---|---|
| 빌드 | 지원 Revit 버전 대상 빌드 성공 |
| 로딩 | `.addin` 로드 및 리본 표시 |
| 실행 | 샘플 모델에서 명령 실행 |
| 안정성 | Revit 크래시 없음 |
| 리포트 | 파일 생성 및 내용 확인 |
| 증빙 | 스크린샷, 로그, 버전 정보 기록 |

## 연결

- [[Qwen Development Boundary]]
- [[Build Test Index]]
- [[Addin Dashboard Merge Plan]]
