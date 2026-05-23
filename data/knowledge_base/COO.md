# COO 지식 베이스


## 운영 총괄 기준 (2026-05-19 09:16:50)
- Source: LUA BIM LABS curated baseline, Autodesk official docs checked 2026-05-19
- Tags: operations,delivery,process

COO는 개발 요청이 실제 납품 가능한 운영 흐름으로 이어지는지 본다. 범위, 일정, 리소스, 품질 기준, 고객지원 준비 상태를 확인하고 병목을 조율한다.


## 운영 KPI 및 릴리스 게이트 기준 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: operations,kpi,release-gate

릴리스 게이트 기준:
□ 빌드 검증: 지원 Revit 버전 전체 smoke test 통과
□ QA: P1/P2 버그 0건, P3 이하 알려진 이슈 문서화
□ 문서: 설치 가이드, 릴리스 노트, 스토어 설명 최신화
□ 법무: EULA, 개인정보 정책 검토 완료
□ 가격/결제: 구독 플랜 및 Entitlement 연동 테스트 완료
운영 KPI: 설치 성공률 95%↑, 지원 문의 응답 SLA 준수율 90%↑, 1개월 이내 환불률 5%↓.


## 개발-출시-지원 사이클 관리 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: operations,delivery,lifecycle

Sprint 주기: 2주. 스토어 제출 주기: 분기 1회 이상.
개발 완료 → 내부 QA(1주) → 빌드 검증(2~3일) → 스토어 제출(심사 1~2주) → 출시.
긴급 패치: P1 버그 발생 시 핫픽스 브랜치 → 긴급 빌드 검증 → 스토어 업데이트 제출(심사 단축 요청 가능).
고객 피드백 → 제품 백로그 → 분기 로드맵 업데이트 사이클 운영.
