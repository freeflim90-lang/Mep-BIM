# EIR/BEP_심사원 지식 베이스

## 2026-06-18 문서 체계 기반 EIR/BEP 심사 기준
- Source: `knowledge/30_intake/external_sources/2026-06-18_contract_proposal_bep_document_work_intake.md`
- Tags: eir,bep,proposal,sow,contract,document-review,scope-risk

EIR/BEP 심사는 기술 내용만 보지 않고 제안서, SOW, 계약서, BEP, 납품검수표가 같은 약속을 말하는지 확인한다. 특히 계약 전 BEP와 계약 후 BEP의 목적 차이를 구분해야 한다.

심사 순서:
1. 발주자 EIR/과업지시서가 무엇을 요구하는지 확인한다.
2. 제안서가 그 요구를 어떻게 해석했는지 확인한다.
3. SOW/계약서가 실제 포함 범위와 제외 범위를 어떻게 확정했는지 확인한다.
4. BEP가 수행 방법, 책임, CDE, LOD/LOI, 납품 기준을 운영 절차로 바꿨는지 확인한다.
5. 납품검수표가 SOW/BEP 기준과 일치하는지 확인한다.

위험 신호:
- EIR에는 없는데 BEP에 과도한 산출물이 추가됨
- 제안서에는 포함, 계약서에는 누락
- SOW 제외 업무를 고객이 납품물로 기대함
- LOD/LOI가 문서마다 다름
- 검토 횟수, 보완 횟수, 납품 형식이 확정되지 않음

## 2026-06-18 ISO 19650 프로토콜 기반 심사 보강
- Source: `knowledge/30_intake/external_sources/2026-06-18_iso19650_protocol_eir_bep_air_intake.md`
- Tags: iso19650,information-protocol,eir,bep,air,handover,review

심사 시 BEP만 보지 않고 정보관리 프로토콜 또는 계약 첨부 문서가 있는지 확인한다. 정보관리 프로토콜은 정보 생산, 정보 사용, 보안, CDE, 승인, 납품 기준을 계약문서와 연결하는 역할을 한다.

추가 심사 항목:
- EIR이 입찰/제안 문서에 포함되어 있는가
- pre-appointment BEP와 계약 후 BEP가 구분되어 있는가
- Information Exchange Requirements가 BIM Uses와 납품 마일스톤별로 정의되어 있는가
- AIR 또는 handover 요구가 COBie/FM/O&M 산출물과 연결되어 있는가
- 정보관리 프로토콜이 계약서/SOW/BEP의 문서 우선순위와 충돌하지 않는가
- 법률 판단이 필요한 프로토콜 조항은 내부 체크가 아니라 전문가 검토 대상으로 표시되어 있는가

## 2026-06-05 EIR·BEP 심사 AI 즉시 답변 패턴 보강
- Source: ISO 19650, 국토부 BIM 시행지침, 발주처 BIM 심사 실무
- Tags: eir,bep,review,compliance,iso19650,2026

**AI 즉시 답변 패턴 — "EIR과 BEP를 심사할 때 무엇을 봐야 하나요?"**
```
EIR(발주자 정보 요구사항) 심사 포인트:
- LOD 수준이 단계별로 명확히 정의되어 있는가?
- 납품 파일 형식(IFC 버전 포함)이 명시되어 있는가?
- CDE 플랫폼 요건이 구체적인가?
- 검토·승인 절차와 기간이 정의되어 있는가?

BEP(BIM 실행계획서) 심사 포인트:
- EIR 요건을 모두 충족하는 수행 계획이 있는가?
- BIM 담당자·책임자가 명확히 지정되어 있는가?
- 소프트웨어·CDE 환경이 EIR과 일치하는가?
- 납품 일정이 현실적이고 마일스톤이 있는가?
- 품질 관리(간섭검토·IFC 검증) 계획이 있는가?
```

**EIR/BEP 심사 체크리스트 (국내 공공 기준):**
| 항목 | EIR 확인 | BEP 확인 |
|------|---------|---------|
| LOD 계획 | 단계별 LOD 명시 | 공종별 LOD 매트릭스 |
| 납품물 목록 | IFC·RVT·PDF 형식 | 납품 일정·검토 절차 |
| CDE 환경 | 플랫폼·권한 요건 | 폴더 구조·워크플로우 |
| 품질 관리 | 검수 기준 | 간섭검토 계획·횟수 |
| 인력 구성 | BIM 책임자 요건 | 담당자·역할 명시 |

## 프로젝트별 문서 템플릿 참조 (2026-05-23)
- Source: LUA BIM LABS document template index
- Tags: eir,bep,proposal,template,external

| 문서 | 파일 | 용도 |
|---|---|---|
| BEP 수행계획서 | [[BEP_수행계획서]] | 프로젝트 착수 시 BIM 수행 계획 작성·발주처 제출 |
| BIM 제안서 | [[BIM_제안서]] | 수주 제안 또는 BIM 컨설팅 제안 시 사용 |

> 두 문서 모두 `[대괄호]` 항목을 프로젝트 값으로 교체하고, `<!-- 삭제 가능 -->` 섹션은 해당 없으면 제거해서 사용.


## EIR/BEP 요구사항 검토 기준 (2026-05-19 09:16:50)
- Source: LUA BIM LABS curated baseline, Autodesk official docs checked 2026-05-19
- Tags: eir,bep,bim-requirements

EIR/BEP 심사원은 고객 BIM 요구사항, 모델 명명 규칙, 좌표/레벨 기준, 속성 입력 기준, LOD/LOI, 보고서 제출 양식이 Add-in 기능과 맞는지 확인한다.


## EIR/BEP 핵심 요구사항 검토 기준 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: eir,bep,bim-requirements

EIR (Employer's Information Requirements) 검토 항목:
□ LOD(Level of Development) 단계별 요구사항 (설계 LOD200, 시공 LOD350, 준공 LOD400)
□ LOI(Level of Information) — 각 단계별 필수 파라미터 목록
□ 명명 규칙: 파일명, 레이어명, 패밀리명, 파라미터명 형식
□ 좌표계: 프로젝트 기준점, 측량 기준점, 공유 좌표 설정 방식
□ 납품 형식: RVT, IFC, NWD, PDF, Excel 지정 버전

BEP (BIM Execution Plan) 검토 항목:
□ 팀별 역할·책임(RACI) 명확화
□ 소프트웨어 버전 통일 (Revit 연도 버전 고정)
□ 협업 플랫폼: BIM 360/ACC 워크스페이스 설정
Add-in 기능이 EIR 파라미터 명명 규칙과 불일치하면 현장 적용 불가 → 공유 파라미터 매핑 기능 필요.


## EIR/BEP 납품 검토 보고서 양식 (2026-05-23)
- Source: LUA BIM LABS document template
- Tags: eir,bep,bim,report,template,external

```
프로젝트명:
발주처:
검토일:
검토자:
검토 대상 문서(버전):
```

### EIR 요구사항 충족 여부

| 항목 | 요구 기준 | 납품 현황 | 충족 여부 | 비고 |
|---|---|---|---|---|
| LOD 단계 | LOD___ | LOD___ | ✅/❌ |  |
| LOI 파라미터 목록 |  |  | ✅/❌ |  |
| 파일명 규칙 |  |  | ✅/❌ |  |
| 레이어·패밀리명 규칙 |  |  | ✅/❌ |  |
| 좌표계 설정 |  |  | ✅/❌ |  |
| 납품 형식(RVT/IFC/NWD/PDF) |  |  | ✅/❌ |  |
| 공유 파라미터 매핑 |  |  | ✅/❌ |  |

### BEP 이행 여부

| 항목 | 기준 | 이행 현황 | 충족 여부 | 비고 |
|---|---|---|---|---|
| 팀별 역할·책임(RACI) |  |  | ✅/❌ |  |
| 소프트웨어 버전 통일 |  |  | ✅/❌ |  |
| 협업 플랫폼 설정 |  |  | ✅/❌ |  |
| Add-in 파라미터 명명 일치 |  |  | ✅/❌ |  |

### 미충족 항목 및 조치

| 항목 | 미충족 사유 | 조치 방법 | 기한 | 담당 |
|---|---|---|---|---|
|  |  |  |  |  |

### 결론

- 납품 적합 여부: 적합 / 조건부 적합 / 부적합
- 재검토 필요 항목 수:
- 최종 납품 가능 예정일:


## EIRBEP 심사원 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: BIM,EIR,BEP,review,국토부,checklist,2025

- 2025년 국토부 BIM 심사 기준 업데이트: 국토교통부 「건설산업 BIM 기본지침 v2.0」(2023.12) 및 「공공건축물 BIM 적용 가이드라인 2025」에 따라 EIR/BEP 심사 체크리스트를 갱신한다. LOD(Level of Development) 기준이 LOI(Level of Information) 개념으로 전환됨에 따라 정보 요건 중심의 심사 항목을 추가한다.
- EIR 심사 핵심 체크리스트(2025): ① 사업 정보 요구 수준(LOI) 명세 여부, ② IFC 2x3 또는 IFC 4 납품 형식 지정, ③ 소프트웨어 상호운용성 요건(IDS 파일 첨부), ④ 정보 납품 시점(PDT: Plain Data Transfer) 일정표, ⑤ BIM 품질 검토 기준(Clash Detection, Model Checker 활용 여부).
- BEP 적합성 자동 검증: Python 3.12로 BEP 문서(PDF → 텍스트 추출)에서 국토부 필수 항목 50개를 키워드 매칭 + Claude API 의미론적 분석으로 검증하는 자동화 도구를 개발한다. 미충족 항목은 항목명·기준 조항·개선 제안을 포함한 리포트로 자동 생성한다.
- Revit Add-in 기반 모델 품질 검사: LUA BIM LABS Model Quality Auditor Add-in을 활용하여 EIR 요건(파라미터 완성도, 네이밍 규칙, 레벨 정합성)을 Revit 2025 내에서 직접 검증한다. 검사 결과는 Excel 리포트로 출력하여 BEP 준수 증빙 자료로 활용한다.
- 심사 피드백 데이터 축적: 심사 완료 프로젝트별 미비 사항 유형을 태그로 분류하여 Obsidian KB에 축적한다. 누적 데이터 분석으로 반복 미비 사항 Top 10을 도출하고, 다음 심사 시즌 전 사전 교육 자료로 활용한다.
- 관련: [[BEP_수행계획서]] · [[BIM_시방서]] · [[BIM_지침서]]

## EIRBEP_심사원 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: EIRBEP,심사,EIR품질,BEP허위기재,LOD협상,범위통제

EIR 작성 품질 낮은 발주처 설득 전략: EIR에 "BIM 모델 제출"만 기재되고 LOD·LOI·납품 형식이 명시되지 않은 경우, 착수 전에 "BIM 정보 요구사항 확인 회의"를 공식 요청한다. 회의에서 국토부 BIM 기본지침 v2.0의 표준 EIR 체크리스트를 기준 문서로 제시하고, 발주처가 선택할 수 있는 3가지 수준(기본/표준/심화)의 EIR 템플릿을 사전 준비하여 제공한다. 발주처가 EIR 개선을 거부하면, 계약서에 "EIR 미비로 인한 범위 분쟁 시 발주처 귀책" 조항을 삽입하도록 법무조항검토 담당에게 요청한다.

BEP 허위 기재 적발 시 계약 처리: 협력사가 BEP에 "Revit 2024 사용"으로 기재했으나 실제로는 2022 버전을 사용하는 경우, 이는 계약서 위반이다. 적발 즉시 서면 시정 요구를 발송하고, 7일 이내 미이행 시 계약서 상 하자 통보 절차를 개시한다. 소프트웨어 버전 차이가 모델 품질에 영향을 미치지 않음을 협력사가 기술적으로 증명한 경우에는 BEP 공식 개정(버전 변경 내역 기록)으로 처리한다.

중소 설계사 BIM 역량 부족 시 현실적 LOD 하향 협상: 발주처가 LOD 350을 요구하지만 협력사 역량이 LOD 200 수준인 경우, "LOD 300 제출 + 미달 항목 별도 도면으로 보완" 방식의 조건부 적합 협상안을 발주처에 제안한다. 이때 LOD 하향으로 절감되는 공수를 견적에서 삭감하고 계약 단가를 조정하여 발주처에게 비용 절감 혜택을 제시하면 수용 가능성이 높아진다. 협상 결과는 반드시 BEP 개정본에 반영하고 발주처 서명을 받아야 한다.

심사 중 추가 요구 사항 범위 통제: 심사 과정에서 발주처가 BEP에 없는 추가 산출물(예: 공정-BIM 연동 보고서)을 요청하는 경우, 조율차장과 협의하여 "변경 요청서 양식"으로 공식 접수 후 추가 견적을 제출한다. 구두 요청에 바로 착수하면 무상 작업 선례가 되므로, 심사 회의 직후 이메일로 "오늘 논의된 추가 요구 사항은 별도 계약 사항으로 확인 요청드립니다"를 명시적으로 발송한다.

- 관련: [[조율차장]] · [[법무조항검토]] · [[프로젝트분석]] · [[BEP_수행계획서]]


## 2026-06-04 ISO 19650 정보관리 기반 EIR/BEP 심사 보강
- Source: `knowledge/40_curation/updates/daily/2026-06-04_LUA_BIM_LABS_ISO19650_CDE_INFORMATION_MANAGEMENT_UPDATE.md`
- Tags: EIR,BEP,ISO19650,CDE,information-management,official-source

ISO 19650-1 공식 페이지와 UK BIM Framework/IMI guidance 기준으로 EIR/BEP 심사는 모델 품질만이 아니라 정보 요구사항, 교환, 기록, 버전, 승인, CDE 상태 관리를 함께 확인해야 한다. ISO 19650은 모델링 기술서가 아니라 정보관리 프레임워크로 본다.

심사 기준:
- EIR은 신규 운영 문서에서 `Exchange Information Requirements`로 정리한다. 과거 `Employer's Information Requirements` 표현을 인용할 때는 문맥과 기준일을 남긴다.
- BEP에는 정보 컨테이너 명명 규칙, CDE 상태, revision, 승인자, Published 기준, 보안 권한을 포함한다.
- CDE는 폴더 구조만으로 충분하지 않으며 metadata, status, revision, approval 흐름이 있어야 한다.
- 정보 요구사항이 명확해야 IDS, ifctester, Model Quality Auditor 자동 검증이 의미를 가진다.

다음 액션:
- EIR/BEP 심사 체크리스트에 `정보관리 범위`, `CDE 상태 코드`, `승인·발행 기준`, `정보 요구사항 자동검증 가능성`을 추가한다.
- 다음 확인일: 2026-06-11

관련: [[BEP 수행계획서 템플릿]] · [[ACC BIM360 CDE 지식 베이스]] · [[BIM 납품검수 지식 베이스]] · [[2026-06-04 LUA BIM LABS ISO 19650 CDE Information Management Update]]


## 2026-06-04 국내 공공 BIM 지침 기반 EIR/BEP 심사 보강
- Source: `knowledge/40_curation/updates/daily/2026-06-04_LUA_BIM_LABS_KOREA_PUBLIC_BIM_GUIDELINE_UPDATE.md`
- Tags: EIR,BEP,molit,pps,public-procurement

EIR/BEP 심사 시 국내 공공 BIM 기준은 국토부 기본지침, 국토부 시행지침, 조달청 BIM 적용지침, 발주처별 적용지침, 실제 과업지시서·입찰안내서 순서로 확인한다. 동일한 `BIM 적용` 문구라도 어떤 지침 계층이 적용되는지에 따라 성과품, 검수, CDE, 책임 범위가 달라진다.

심사 추가 항목:
- 적용 지침 계층 확인
- 발주처 적용지침(Level 2-1) 제공 여부
- 실무요령(Level 2-2) 제공 여부
- BIM 요구사항정의서, 과업지시서, 수행계획서 세부 서식 제공 여부
- 조달청 시설사업 BIM 적용지침서 v2.1 적용 여부

운영 기준:
- 발주처가 EIR을 제공하지 않으면 기준 보정 회의를 요청한다.
- 지침 계층이 불명확하면 BEP에 임의 기준을 확정하지 않고 `needs-confirmation`으로 둔다.
- 조달청 적용 사업은 설계공모 지침, 설계용역 과업지침서, 입찰안내서의 BIM 요구사항을 우선 기준으로 본다.

관련: [[BIM 지침서 지식 베이스]] · [[견적심사원 지식 베이스]] · [[법규변경모니터링]]

## EIR·BEP 심사 최신 기준 업데이트 (2026-06-26)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-26
- KST04 자동수집: 공식 출처/담당자 검증 전 고객 확정 답변, 납품 기준, 견적 기준으로 사용 금지.
- Tags: EIR,BEP,review,update

- EIR·BEP 심사원들은 국토부 BIM 지침을 기반으로 2023년부터 적용되는 새로운 심사 기준을 숙지해야 합니다. 이는 정보요구사항(EIR)에 따라 제출된 BIM 데이터의 적합성을 판단하는 방법론을 제공합니다.
- 디지털 데이터 전환과 관련하여, EIR·BEP 심사원들은 BIM 데이터의 정확성, 일관성, 그리고 접근성 등을 철저히 검토해야 합니다. 이는 2023년 국토부 지침에서 명시된 기준을 따르도록 요구됩니다.
- 자주 발생하는 미비 사항으로는 BIM 모델링의 차질, 데이터 통합 문제, 그리고 정보 누락 등이 있습니다. 이러한 문제를 방지하기 위해 EIR·BEP 심사원들은 프로젝트 초기부터 BIM 관리 계획을 철저히 검토해야 합니다.
- 또한, 최근의 BIM 관련 연구와 개발 동향을 파악하여, 최신 기술과 방법론을 반영한 심사가 이루어질 수 있도록 노력해야 합니다. 이는 BIM 클러스터 운영 전략 로드맵 및 BIM 데이터의 디지털 전환에 대한 이해를 높이는 데 도움이 됩니다.
- 관련: [[BIM_시방서]] · [[BEP_수행계획서]] · [[스토어심사]]

