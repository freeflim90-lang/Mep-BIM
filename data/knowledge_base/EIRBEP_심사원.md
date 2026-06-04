# EIR/BEP_심사원 지식 베이스


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


## EIR·BEP 심사 최신 기준 업데이트 (2026-05-28)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-28
- Tags: EIR,BEP,review,update

- 2025년 BIM EIR·BEP 심사 기준은 CEN/TR 17654:2021을 중심으로 진행되며, 정보 교환과 모델의 일치성을 강조하고 있습니다.
- 국토부 BDC 지침에 따르면, 정보요구사항(EIR)에 따라 제출되는 BIM 데이터의 적합성 판단 방법론이 필요합니다. 특히 디지털 데이터 전환에 따른 문제점을 주의해야 합니다.
- 자주 발생하는 미비 사항으로는 BIM 모델의 구체적인 항목별 정보 누락이나 오류, 그리고 EIR 요구사항과 일치하지 않는 데이터 제출 등이 있습니다. 이를 피하기 위해 EIR 요구사항을 철저히 준수하며, 모델링 시점부터 정확한 정보를 입력해야 합니다.
- BIM 설계 의무화와 관련하여, 건축사들은 BIM 설계가 잘 정착하지 못하는 이유 중 하나로 BIM 기술의 익숙하지 않은 점을 지적하고 있습니다. 따라서 BIM 교육과 함께 실질적인 적용 사례를 통해 이해도를 높이는 것이 중요합니다.
- 성과물 품질, 납품 등 프로젝트 종료 시 적용되는 기준은 반드시 준수해야 하며, 이를 위해 정기적인 심사와 모니터링이 필요합니다.

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


## EIR·BEP 심사 최신 기준 업데이트 (2026-05-29)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-29
- Tags: EIR,BEP,review,update

- 2025년 한국 EIR·BEP 심사 기준은 EN ISO 19650와 CEN/TR 17654에 근거하고 있으며, 주요 변화는 BIM 실행 계획(BEP)과 정보 교환 요구사항(EIR)의 디지털 데이터 전환을 강조하고 있다.
- 국토부 BIM 지침은 BIM 클러스터 운영 전략 로드맵 수립 및 연구기획에 대한 방법론을 제시하며, EIR에 따라 제출되는 BIM 데이터의 적합성을 판단할 수 있도록 하는 것이 중요하다.
- 자주 발생하는 미비 사항으로는 BIM 데이터의 정확성과 일관성, BEP와 EIR 간의 일치성, 그리고 정보의 실시간 업데이트가 포함된다.
- 관련: [[BIM_시방서]] · [[BEP_수행계획서]] · [[스토어심사]]


## 2026-06-04 ISO 19650 정보관리 기반 EIR/BEP 심사 보강
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_ISO19650_CDE_INFORMATION_MANAGEMENT_UPDATE.md`
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
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_KOREA_PUBLIC_BIM_GUIDELINE_UPDATE.md`
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


## EIR·BEP 심사 최신 기준 업데이트 (2026-05-30)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-30
- Tags: EIR,BEP,review,update

- 2025년부터 국토부 BIM 지침에 따라 EIR·BEP 심사원들이 수행해야 하는 심사 기준이 변경되었습니다.
- BIM 데이터의 적합성을 판단하기 위한 방법론 제시가 필요합니다 (출처: https://www.codil.or.kr/filebank/original/RK/OTKCRK220270/OTKCRK220270.pdf).
- BIM 모델과 BEP에 명시된 BIM 요구사항을 연결하여 검증해야 합니다 (출처: https://www.codil.or.kr/filebank/original/RK/OTKCRK220270/OTKCRK220270.pdf).
- 자주 발생하는 미비 사항으로는 BIM 모델과 BEP 요구사항 간의 일치성 확인이 어렵다는 점입니다.
- 관련: [[BIM_시방서]] · [[BEP_수행계획서]] · [[스토어심사]]


## EIR·BEP 심사 최신 기준 업데이트 (2026-05-31)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-31
- Tags: EIR,BEP,review,update

- 2025년 국토부 BIM EIR·BEP 심사 기준에 따르면, 정보요구사항(EIR)과 BIM 실행 계획(BEP)의 준수 여부가 중요한 검토 항목이다.
- EIR은 프로젝트 참여자 간의 정보 교환을 위한 요구 사항을 명시해야 하며, BEP는 BIM 도입을 위한 구체적인 계획이 포함되어야 한다. 이 두 기준은 BIM 데이터의 적합성과 디지털 전환에 대한 준수 여부를 판단하는 데 필수적이다.
- 자주 발생하는 미비 사항으로는 EIR에서 요구사항의 명확성이 부족하거나 BEP가 구체적이지 않아 프로젝트 진행에 차질을 빚는 경우가 있다. 따라서 심사원은 이 두 항목이 상세하고 체계적임을 확인해야 한다.
- BIM 클러스터 운영 전략 로드맵 및 연구기획 문서를 참고하면, EIR과 BEP의 적합성을 판단하는 방법론을 이해할 수 있다. 이를 통해 심사 과정에서 필요한 정보와 절차가 명확해질 것이다.
- 관련: [[BIM_시방서]] · [[BEP_수행계획서]] · [[스토어심사]]


## EIR·BEP 심사 최신 기준 업데이트 (2026-06-01)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-01
- Tags: EIR,BEP,review,update

- 2025 국토부 BIM EIR·BEP 심사 기준에 따르면, 정보요구사항(EIR)과 BIM 실행 계획(BEP)의 준수 여부가 중요한 체크포인트이다.
- EIR 심사는 고용주/교환 정보 요구 사항을 분석하고, BEP는 BIM 모델과 연결하여 BIM 요구사항을 검증해야 한다. 이 과정에서 디지털 데이터 전환의 적합성을 판단한다.
- 자주 발생하는 미비 사항으로는 EIR에 명시된 정보가 부족하거나 정확하지 않은 경우, BEP와 BIM 모델 간의 일치성이 확보되지 않은 경우 등이 있다.
- 관련: [[BIM_시방서]] · [[BEP_수행계획서]] · [[스토어심사]]


## EIR·BEP 심사 최신 기준 업데이트 (2026-06-02)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-02
- Tags: EIR,BEP,review,update

- 2025년 국토부 BIM EIR·BEP 심사 기준에 따르면, 정보요구사항(EIR)과 BIM 실행계획(BEP)의 적합성을 평가해야 한다.
- EIR심사는 정보전달매뉴얼의 내용을 체크하고, BEP심사는 BIM 활용 및 협업 전략을 포함한 deliverables와 roles를 확인한다.
- 특히 디지털 데이터 전환에 따른 BIM 데이터 적합성 평가 방법론이 중요하며, 자주 발생하는 미비 사항으로는 정보의 일관성과 정확성이 있다.
- 관련: [[BIM_시방서]] · [[BEP_수행계획서]] · [[스토어심사]]


## EIR·BEP 심사 최신 기준 업데이트 (2026-06-03)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-03
- Tags: EIR,BEP,review,update

- 2025년 국토부 EIR·BEP 심사 기준에 따르면, BIM(Building Information Modeling) 구현이 중점 사항으로 지정되어 있으며, 정보 교환 및 실행 계획의 명확성은 프로젝트 성공을 위한 핵심 요소로 인식된다.
- EIR 심사에서 BIM 데이터의 적합성을 평가하기 위해 방법론을 제시하고 있어, 디지털 데이터 전환에 따른 BIM 데이터의 적합성 판단 기준이 중요해졌다. 이는 2025년 국토부 BIM 지침 기반으로 수립된 EIR·BEP 심사 항목에서 확인할 수 있다.
- 자주 발생하는 미비 사항으로, 프로젝트 초기 단계부터 BIM 데이터 전환 과정에서의 협업과 정보 공유가 부족한 경우가 많다. 이를 해결하기 위해 EIR 및 BEP 심사 시 철저한 계획 수립과 실행이 요구된다.
- 특히, BIM 데이터의 정확성과 일관성을 확보하기 위해서는 프로젝트 시작부터 끝까지의 전 과정에서 BIM 기반 정보 관리가 필수적이다. 이는 2025년 국토부 EIR·BEP 심사 기준에 명시되어 있다.
- 연구개발과제 유형 및 실용화 여부를 고려한 BIM 구현 계획이 필요하며, 이를 통해 항만시설 등 다양한 분야에서의 BIM 적용이 체계적으로 이루어질 수 있어, 2025년 국토부 EIR·BEP 심사 기준에 따라 철저히 준비해야 한다.
- 관련: [[BIM_시방서]] · [[BEP_수행계획서]] · [[스토어심사]]


## EIR·BEP 심사 최신 기준 업데이트 (2026-06-03)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-03
- Tags: EIR,BEP,review,update

- 2025년 국토부 EIR·BEP 심사에서는 BIM(Building Information Modeling)의 실현 가능성을 강조하고 있으며, EN ISO 19650과 같은 국제 지침에 맞춰 정보 교환 및 프로젝트 성공을 위한 실행 계획이 명확해야 합니다.
- EIR 심사에서 제출되는 BIM 데이터의 적합성 판단 방법론은 디지털 데이터 전환에 따른 BIM 클러스터 운영 전략 로드맵 수립과 연구기획을 통해 개발되어야 합니다.
- 자주 발생하는 미비 사항으로는 EIR·BEP 심사에서 요구되는 정보의 명확성 부족, 프로젝트 협업 강화를 위한 실행 계획 미비 등이 있습니다.
- 관련: [[BIM_시방서]] · [[BEP_수행계획서]] · [[스토어심사]]


## EIR·BEP 심사 최신 기준 업데이트 (2026-06-04)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-04
- Tags: EIR,BEP,review,update

- 2025 국토부 BIM EIR·BEP 심사 기준은 EN ISO 19650에 근거하고 있으며, 프로젝트별 실행 계획과 정보 관리에 중점을 둡니다.
- 디지털 데이터 전환에 따른 BIM 데이터 적합성 판단 방법론을 마련해야 합니다.
- 자주 발생하는 미비 사항으로는 EIR과 BEP 간 일관성이 부족한 경우가 있습니다. 이를 위해 두 문서의 내용을 철저히 검토하고 조정이 필요합니다.
- 정보요구사항(EIR)은 프로젝트 특성에 맞게 정확하게 작성되어야 하며, BIM 데이터의 적합성을 판단할 수 있어야 합니다.
- BEP는 BIM 실행 계획을 명확하게 제시해야 하며, 프로젝트 관리와 정보 전달 과정에서의 일관성을 보장합니다.
- 관련: [[BIM_시방서]] · [[BEP_수행계획서]] · [[스토어심사]]
