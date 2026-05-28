---
type: knowledge-strategy
date: 2026-05-28
status: active
tags:
  - ax
  - ai-transformation
  - construction
  - design
  - bim
  - smart-construction
  - knowledge-strategy
---

# AX 전환을 위한 건설 BIM AI 지식 축적 전략

## 목적

건설 관련 설계, 시공, BIM, AI 지식 수집의 최종 목적은 단순 자료 보관이 아니라 LUA BIM LAB의 AX(AI Transformation) 실행 역량을 만드는 것이다. 모든 지식은 아래 흐름으로 승격 가능해야 한다.

`정보 수집 -> 실무 기준화 -> 데이터 구조화 -> 자동화 워크플로우 -> AI 에이전트화 -> 상품/서비스화`

## 회사 성장 비전

LUA BIM LABS는 AX를 BIM 실무에 적용하여 BIM 업계에서 선도적인 기술 기업으로 성장한다.

이 비전은 회사의 지식 수집, 교육, 자동화, Add-in 개발, 품질검토 서비스, 고객 응대의 공통 기준이다. AX는 별도 유행어가 아니라 LUA BIM LABS가 BIM 전문성을 확장하는 운영 방식이다.

## AX 관점의 지식 분류 축

### 1. 정책/시장 신호

- 국토교통부, KAIA, KCSC, 소방청, 전기협회 등 공식 기준과 지원사업
- 스마트건설, AI 도시, 디지털 트윈국토, AX-SPRINT, AI 응용제품 상용화
- 대형 건설사/설계사/플랫폼사의 AI 전환 사례

승격 기준:
- 공공사업, 지원사업, 법규/기준 변경과 연결되면 `전략기획`, `CSO`, `제품패키징`으로 연결한다.

### 2. 설계 BIM 지능화

- Revit, Forma, IFC, IDS, openBIM, 설계 자동화, 생성형 설계
- 설계 오류 검출, BIM 모델 품질, 속성/분류체계, 납품 요구사항 자동 검증

승격 기준:
- 모델 품질 검토나 납품 검증으로 연결되면 `Model Quality Auditor` 룰 후보로 승격한다.

### 3. 시공 BIM/스마트건설

- 현장 디지털 트윈, 드론/로봇/IoT, 공정·안전·품질 모니터링
- Navisworks 간섭, 4D/5D, 현장 이슈-모델 연결, 준공 데이터

승격 기준:
- 현장 반복 업무를 줄이면 `시공_지침서`, `설비시공조율`, `Navisworks_Addin`으로 연결한다.

### 4. MEP 전문 지식

- 공조덕트, 공조배관, 위생, 소방기계, 소방전기, 전기, 통신
- KDS/KCS/KEC/NFTC 기준, 장비/패밀리/LOD/속성 체계

승격 기준:
- 수치/법규 기준은 출처와 기준일을 붙이고, 원문 확인 전까지 추정 답변으로 운영하지 않는다.

### 5. 데이터/지식 인프라

- Obsidian 지식맵, RAG, 질의응답 로그, QA 데이터셋, 지식 그래프
- 반복 질문 캐시, 출처 우선순위, 보안/개인정보 분류

승격 기준:
- 동일 질문이 반복되면 공식 답변 노트, FAQ, 교육자료, QA 체크리스트로 전환한다.

### 6. AI 에이전트/상품화

- Revit Add-in, Telegram/Revit Assistant, 자동 리포트, 견적/검토/조율 도구
- Autodesk Store, 내부 업무 자동화, 고객 서비스 패키지

승격 기준:
- 실무자가 반복 실행하는 판단/검토/문서화 작업은 에이전트 기능 후보로 기록한다.

## 수집 우선순위

1. 공식 기준/정책: 국토교통부, KAIA, KCSC, 법령, Autodesk, buildingSMART
2. 실무 플랫폼 변화: Revit, Autodesk Construction Cloud/Forma, IFC/IDS, Navisworks
3. 현장 적용 사례: 스마트건설, 안전 AI, 공정/품질 자동화, 대형 건설사 사례
4. 연구/오픈소스: Scan-to-BIM, BIM-to-digital-twin, BIM LLM, IFC 자동 검증
5. 내부 반복 질문: Telegram, Revit Assistant, 프로젝트 질의, 교육 피드백

## AX 전환 성숙도

| 단계 | 상태 | 설명 | 산출물 |
|---|---|---|---|
| L0 | 수집 | 뉴스/문서/질문을 저장 | 일일 브리핑, QA 노트 |
| L1 | 정리 | 출처, 기준일, 태그 부여 | Obsidian 노트, MOC |
| L2 | 표준화 | 반복 기준/체크리스트화 | 표준문서, 교육자료 |
| L3 | 데이터화 | 규칙, 파라미터, 스키마로 변환 | JSON 룰, QA 데이터셋 |
| L4 | 자동화 | 사람이 반복하던 검토/작성 자동화 | Add-in, 스크립트, 리포트 |
| L5 | 에이전트화 | 맥락 기반 판단과 실행 지원 | Revit/Telegram/웹 에이전트 |
| L6 | 상품화 | 고객에게 판매 가능한 패키지 | 서비스 메뉴, Store 제품 |

## 운영 리듬

AX 지식 축적은 아래 시간 단위로 운영한다.

| 주기 | 목적 | 자동화 | 산출물 |
|---|---|---|---|
| 매시간 | 노이즈가 많은 최신 신호를 가볍게 감지 | `com.luabimlab.hourly-ax-signal-monitor` | `docs/industry_intelligence/hourly/`, `AX_시간별_신호모니터링` |
| 매일 07:00 | 신호를 큐레이션하고 지식베이스/Obsidian에 정식 반영 | `com.luabimlab.daily-knowledge-update` | 일일 브리핑, 일일 지식 업데이트, Obsidian 그래프 |
| 매주 월요일 07:30 | 반복 신호를 전략/제품/교육/자동화 후보로 승격 | `com.luabimlab.weekly-ax-strategy-review` | `docs/knowledge_updates/weekly/`, `AX_전략승격리뷰` |

매시간 수집은 판단을 확정하지 않는다. 매일은 정리하고, 매주는 승격한다. 이 구조를 통해 빠른 시장 감지와 과도한 지식 노이즈를 동시에 관리한다.

## 현재 우선 축적 과제

- Revit 2027 AI/MCP/Forma 변화와 Add-in 호환성
- IFC/IDS 기반 납품 요구사항 자동 검증
- KDS/KCS/KEC/NFTC 기준을 공종별 BIM 체크리스트로 구조화
- 시공 현장 AI/스마트건설 사례를 안전, 공정, 품질, 물량, 준공 데이터로 분해
- 반복 Q&A를 로컬 지식 우선 답변과 공식 출처 답변으로 분리
- Model Quality Auditor를 AX 상품화의 첫 번째 실행 제품으로 유지

## 공식/검증 출처

- 국토교통부 2026 업무계획: https://www.molit.go.kr/2026plan/sub2_economy.html
- 국토교통부 AI 응용제품 신속 상용화 지원사업(AX-SPRINT): https://hub.kaia.re.kr/organSupportHub.do/view?curPage=1&orgKind=ORG_KIND_1&suppId=194
- 국토교통부 스마트건설 강소기업·기술실증 공모: https://www.molit.go.kr/USR/NEWS/dtl.jsp?id=95091873&lcmspage=7
- Autodesk Forma/Revit cloud connection: https://adsknews.autodesk.com/en/news/autodesk-design-and-make-intelligence/
- Autodesk Construction Cloud to join Forma: https://adsknews.autodesk.com/en/news/autodesk-construction-cloud-to-join-forma/
- buildingSMART IDS: https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/
- 국가건설기준센터: https://kcsc.re.kr/

## 연결

- [[LUA BIM LABS AX BIM 선도기업 성장 비전]]
- [[Global Knowledge Map]]
- [[2026-05-28 BIM AI openBIM 기준 업데이트]]
- [[지식업데이트]]
- [[산업동향_데일리브리핑]]
- [[BIM_지침서]]
- [[시공_지침서]]
- [[설계_지침서]]
- [[Revit_Addin]]
- [[Navisworks_Addin]]
- [[Model Quality Auditor - Knowledge Map]]
