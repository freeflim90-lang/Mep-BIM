---
type: merge-plan
project: Model Quality Auditor
status: draft
node_type: procedure
tags:
  - mqa
  - addin-dashboard
  - packaging
created: 2026-05-20
---

# Addin Dashboard Merge Plan

## 병합 조건

아래 조건을 모두 만족한 뒤 Addin Dashboard 패키지 편입을 검토한다.

- 별도 프로젝트에서 코어 진단 로직 단위 테스트 통과
- 실제 Revit 환경에서 모델 데이터 추출 테스트 통과
- Revit 2024/2025/2026 중 지원 표기 대상 버전 smoke test 완료
- 리포트 출력 파일 검증 완료
- 라이선스/구독 UX 정책 확정
- Store 문구와 실제 기능 일치 확인

## 병합 후보 경로

- Addin Dashboard 리본/대시보드 모듈로 편입
- 또는 독립 Store 제품으로 유지하고 추후 번들 구성

## 연결

- [[Separate Project Strategy]]
- [[Build Test Index]]
- [[Revit API Test Gate Index]]
- [[Store Package Link]]
