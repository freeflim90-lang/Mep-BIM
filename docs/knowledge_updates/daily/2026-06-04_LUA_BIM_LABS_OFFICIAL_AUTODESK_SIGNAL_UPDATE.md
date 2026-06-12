---
type: daily-knowledge-update
date: 2026-06-04
status: needs-review
source_grade: official
tags:
  - autodesk
  - revit
  - aps
  - addin
  - knowledge-update
---

# 2026-06-04 LUA BIM LABS Official Autodesk Signal Update

Autodesk 공식 문서와 APS 공식 블로그 기준으로 LUA BIM LABS에 필요한 기술 신호를 정리한다. 이 문서는 확정 개발 지시가 아니라 `needs-review` 기반 지식 업데이트이며, 제품·교육·자동화 로드맵 반영 전 QA와 출처 재검증을 요구한다.

## 수집 출처

| 출처 | 확인 신호 | 운영 판정 |
|---|---|---|
| Autodesk Help, What's New in Revit 2026 | Revit 2026 기능·릴리스 변화, MEP/플랫폼/성능/문서화 항목 | `PRI04 재검증 예약`, Add-in QA 매트릭스 후보 |
| APS Blog, Building for Agentic AI | AEC Data Model API, granular Revit data, Data Exchanges, APS agentic AI 방향 | `PRI07 승격 후보`, 클라우드 데이터 연동 후보 |
| APS Blog, Secure Service Accounts GA | 3LO 자동화 계정의 보안·운영 개선 | `PRI01 즉시 차단`/보안 기준 후보 |
| APS Blog, APS business model evolution | API 접근·과금 모델 전환, 사용량 계획 필요 | `PRI04 재검증 예약`, 비용·라이선스 검토 후보 |
| APS Blog, AI Era Demands a Platform Revolution | 플랫폼 통합, AI·데이터 기반 설계/제조 흐름 강화 | `PRI08 백로그 유지`, 전략 관찰 후보 |

## LUA BIM LABS 반영 판단

### 1. Revit 2026 Add-in QA 매트릭스 보강

Autodesk Help의 Revit 2026 What's New는 Revit 2026 기능과 업데이트가 플랫폼, MEP, 성능, 문서화, Dynamo 등 여러 축에서 변하고 있음을 보여준다. LUA BIM LABS Add-in은 `Revit 2024/2025/2026 지원`을 주장하기 전에 Revit 2026.4 계열 스모크 테스트와 릴리스 노트 기준 호환성 점검을 분리해야 한다.

판정:
- `FIX03 출처 재검증`
- `PRI04 재검증 예약`
- `WKP04 재검증 예약`

다음 액션:
- `docs/autodesk_store/QA_SMOKE_TEST_PLAN.md`와 Revit 2026 테스트 항목 연결
- Revit 2026 전용 실패 로그와 Store 문구 검토
- 다음 확인일: 2026-06-11

### 2. APS AEC Data Model API와 클라우드 데이터 연동 후보

APS 공식 블로그는 AEC Data Model API가 Revit 데이터의 geometry, properties, relationships를 구조화된 클라우드 데이터로 다루는 방향을 강조한다. LUA BIM LABS의 Model Quality Auditor, BIM Command Center, 납품 검수 자동화는 단독 Add-in 버튼보다 ACC/APS 데이터 연동과 리포팅 구조를 고려해야 한다.

판정:
- `FIX06 승격 이동`
- `PRI07 승격 후보`
- `WKP07 승격 실험`

다음 액션:
- Model Quality Auditor 백로그에 APS 데이터 연동 PoC 후보 추가
- ACC/BIM360 지식과 Revit_Addin 지식 상호 링크
- 파일럿 조건: 샘플 모델 1개, 읽기 전용 데이터 추출, 보안검토 통과

### 3. Secure Service Accounts 보안 기준 반영

APS Secure Service Accounts GA 신호는 ACC/BIM360의 3LO 중심 API 자동화에서 토큰·계정 운영 위험을 줄이는 방향과 맞닿아 있다. LUA BIM LABS는 refresh token 장기 보관, 공유 계정, 원문 credential 기록을 보안 위험으로 보고 차단 기준에 넣어야 한다.

판정:
- `FIX05 보안 정리`
- `PRI01 즉시 차단`
- `WKP01 보안 먼저`

다음 액션:
- `라이선스_보안관`, `ACC_BIM360`, `인프라_DevOpsObsidian`에 SSA/토큰 보안 검토 링크 연결
- `.env`, 토큰, 고객 계정 정보가 Obsidian 원문에 들어가지 않도록 차단
- 다음 확인일: 2026-06-11

### 4. APS 과금·비즈니스 모델 변화 Watch

APS 비즈니스 모델 전환은 API 실험, 사용량 한도, 유료 API 확장 계획에 영향을 준다. LUA BIM LABS는 APS 기능을 상품 기능으로 확정하기 전에 비용 구조와 고객 과금 방식이 맞는지 확인해야 한다.

판정:
- `FIX03 출처 재검증`
- `PRI04 재검증 예약`
- `WKP08 보류 사유`

다음 액션:
- APS 사용량 기반 기능은 MVP에서 읽기 전용/수동 실행 우선
- 비용·라이선스 영향은 `라이선스결제`, `CFO`, `제품패키징`으로 연결
- 다음 확인일: 2026-06-11

## Obsidian 연결

- [[Revit_Addin]]
- [[ACC BIM360 CDE 지식 베이스]]
- [[라이선스_보안관]]
- [[지식업데이트]]
- [[지식큐레이터]]
- [[2026-06-04 Knowledge Update Queue]]
- [[2026-W23 Knowledge Curation Weekly Review]]

## 공식 출처 URL

- Autodesk Help, What's New in Revit 2026: https://help.autodesk.com/cloudhelp/2026/KOR/Revit-WhatsNew/files/GUID-C81929D7-02CB-4BF7-A637-9B98EC9EB38B.htm
- APS Blog, Building for Agentic AI: https://aps.autodesk.com/blog/building-agentic-ai-whats-new-autodesk-platform-services
- APS Blog, Secure Service Accounts GA: https://aps.autodesk.com/node/3765
- APS Blog, APS Business Model Evolution: https://aps.autodesk.com/blog/aps-business-model-evolution
- APS Blog, The AI Era Demands a Platform Revolution: https://aps.autodesk.com/blog/ai-era-demands-platform-revolution
