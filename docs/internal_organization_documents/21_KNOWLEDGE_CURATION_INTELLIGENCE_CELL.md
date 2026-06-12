# LUA BIM LAB
# 지식 큐레이션·인텔리전스 셀 운영 기준

━━━━━━━━━━━━━━━━━━━━

문서번호: LBL-ORG-021  
문서상태: 내부 기준 초안  
작성일: 2026-05-21  
배포등급: Internal Only  
적용범위: 지식 DB, Obsidian, 교육자료, 상품자료, 개발 오답노트, 외부 공개 준비

## 1. 목적

본 문서는 매일 업데이트되는 지식 DB에서 LUA BIM LAB의 목적성에 맞는 정보를 선별, 구조화, 연결, 승격하기 위한 `지식 큐레이션·인텔리전스 셀`의 역할과 운영 기준을 정의한다.

## 2. 설치 필요성

지식 DB가 매일 업데이트되면 문서량은 빠르게 늘어나지만, 회사 목적성과 직접 연결되지 않은 정보가 섞이면 검색성과 의사결정 품질이 떨어진다. 따라서 단순 수집 담당과 별도로 다음 판단을 수행하는 조직 기능이 필요하다.

- 어떤 정보가 LUA BIM LAB의 성장 방향과 연결되는가
- 어떤 오류가 제품 품질 기준으로 승격되어야 하는가
- 어떤 문서가 교육자료, 상품자료, 제안자료로 재사용 가능한가
- 어떤 정보가 외부 공개 전에 숨겨져야 하는가
- 어떤 지식이 Autodesk Add-in Store, MEP BIM 품질진단, 교육 커리큘럼과 연결되는가

## 3. 조직 위치

| 항목 | 기준 |
|---|---|
| 조직 축 | 교육/지식 |
| 협업 축 | 경영/전략, BIM 수행, 고객/운영, 보안/관리 |
| 최종 책임 | 교육컨설팅 또는 최고전략 CSO |
| 실행 담당 | 지식큐레이터, 지식업데이트, 테크니컬 라이터, QA |
| 주요 산출물 | 큐레이션 리포트, 승격 후보, 공개 차단 목록, Obsidian 연결 개선 |

## 4. 핵심 역할

| 역할 | 책임 |
|---|---|
| 목적성 필터링 | 회사 방향과 관련 낮은 정보를 보관/아카이브로 분리 |
| 지식 승격 | 오류, 프로젝트 교훈, 고객 피드백을 표준/교육/상품 문서 후보로 승격 |
| 연결성 개선 | 고립 문서를 MOC, 제품, 교육, 조직 기준 문서와 연결 |
| 공개 준비 | Public, Client-Shareable, Internal, Confidential 분류 점검 |
| 전략 신호 감지 | 수익화, Add-in, 교육상품, 컨설팅 전환 가능 정보 식별 |
| DB 품질관리 | 중복, 오래된 문서, 미검증 문구, 보안 리스크 점검 |

## 4.1 전담 AI 직원

| 담당자 | 책임 |
|---|---|
| 지식큐레이터 | 매일 생성되는 큐레이션 검수 리포트를 확인하고, 수집 지식을 `보안검토`, `보강필요`, `승격후보`, `유지`, `보류`로 분류한다. 반복 질문과 개발 오류는 표준문서, 교육자료, FAQ, QA 체크리스트 후보로 연결한다. |
| 지식업데이트 | 질문, 브리핑, 자동 수집 결과, 보강 요청을 지식베이스와 Obsidian에 반영한다. |

## 5. 회사 목적성 기준

정보를 정리할 때 다음 우선순위를 적용한다.

1. MEP BIM 실무 품질 향상에 직접 기여하는가
2. Model Quality Auditor 또는 Autodesk Add-in Store 상품화와 연결되는가
3. 신규/연차별 BIM 교육 커리큘럼에 재사용 가능한가
4. 설계, 시공, 납품, 품질검토의 반복 업무를 줄이는가
5. AI와 자동화를 통해 생산성을 높이는 데 쓰이는가
6. 고객에게 설명 가능한 공식 문서 또는 리포트로 전환 가능한가
7. 내부 보안, 계약, 운영 리스크를 낮추는가

## 6. 일일 큐레이션 흐름

| 단계 | 작업 | 산출물 |
|---|---|---|
| 1 | 일일 업데이트 리포트 확인 | 신규/변경 문서 목록 |
| 2 | 자동 큐레이션 검수 실행 | 보안검토, 보강필요, 승격후보, 유지, 보류 |
| 3 | 목적성 기준으로 분류 확인 | 유지, 승격, 보류, 아카이브 |
| 4 | 공개 등급 확인 | Public, Client-Shareable, Internal, Confidential |
| 5 | 연결성 점검 | MOC, 제품문서, 교육자료, 오류노트 링크 |
| 6 | 승격 후보 작성 | 표준문서, 교육자료, 상품자료, 체크리스트 후보 |
| 7 | Obsidian 맵 재생성 | 전역 그래프 및 Canvas 갱신 |

## 6.1 자동 큐레이션 분류 기준

매일 지식 업데이트 루틴은 최근 변경된 Markdown 문서를 자동으로 검토하여 `knowledge/40_curation/updates/curation`에 일일 큐레이션 검수 리포트를 생성한다.

| 자동 권고 | 의미 | 후속 조치 |
|---|---|---|
| 보안검토 | 개인정보, 계정, 토큰, 내부 경로, 고객/프로젝트 실명 가능성 감지 | 공개 전 제거/마스킹 및 보안/법무 확인 |
| 보강필요 | 팀원 답변 부족, 지식 공백, 검토 필요 상태 감지 | 담당 지식베이스 보강 후 재답변 |
| 승격후보 | 표준문서, 교육자료, 상품자료, QA 체크리스트, FAQ로 전환 가능 | 큐레이션 담당이 승격 대상 확정 |
| 유지 | 회사 목적성과 연결되며 현재 위치에 보관 가능 | Obsidian 연결성 유지 |
| 보류 | 목적성 연결이 낮거나 중복/미검증 가능성 있음 | 아카이브 또는 삭제 후보 검토 |

자동 분류는 최종 승인 판단이 아니라 1차 triage이다. 최종 공개, 교육 배포, 표준문서 승격은 담당자의 검토를 거친다.

## 6.2 AI 사용 배치

지식 큐레이션은 기본적으로 로컬 규칙 기반과 지식큐레이터 판단으로 수행한다. DeepSeek API는 일일 분류에는 사용하지 않는다.

| 작업 | AI 배치 |
|---|---|
| 일일 큐레이션 검수 | 로컬 규칙 기반 |
| 팀원 Q&A 분류 | 로컬/Obsidian |
| `더 찾아줘` 수집 결과 분류 | 로컬 + needs-review |
| 승격/보류/보안검토 1차 판단 | 지식큐레이터 |
| 분류 기준 자체 개선 또는 경영 전략 판단 | 민감정보 제거 후 DeepSeek 제한 허용 |

세부 기준은 `26_AI_EXECUTION_PLACEMENT_POLICY.md`를 따른다.

## 7. 승격 기준

| 정보 유형 | 승격 대상 |
|---|---|
| 반복 오류 | 오류 오답노트, QA 체크리스트, 개발 테스트 항목 |
| 고객 반복 질문 | FAQ, 고객지원 템플릿, 제안서 문구 |
| 프로젝트 교훈 | 표준문서 개정, 교육 실습, 납품 체크리스트 |
| 생산성 개선 아이디어 | Add-in 후보, 자동화 기능, 내부 툴 |
| BIM 품질 이슈 | Model Quality Auditor 진단 항목 |
| 교육 공백 | 연차별 커리큘럼, 실습 자료, 평가 기준 |
| AI 협업 결과 | KB, QA, 교육자료, 표준문서, 자동화 백로그, conflict_resolution 선례 |

## 7.1 AI 협업 산출물 승격 기준

AI 협업 세션에서 나온 결과는 다음 기준으로 승격한다.

| 산출물 | 승격 위치 | 담당 |
|---|---|---|
| 반복 판단 기준 | `knowledge/10_agents/90_확장에이전트/*.md` | 지식큐레이터 |
| 의견 충돌 선례 | `knowledge/10_agents/conflict_resolution/CONFLICT_LOG.md` | 조율차장 |
| 업무 실행 양식 | `docs/internal_organization_documents/31_AI_COLLABORATION_RUNBOOK_TEMPLATES.md` | 테크니컬 라이터 |
| 교육 필요 항목 | `knowledge/60_public/training_curriculum/` 또는 `19_TRAINING_RECORD_COMPETENCY_MATRIX.md` | 교육컨설팅 |
| 자동화 후보 | `docs/internal_growth/AX_INTERNAL_GROWTH_BACKLOG.md` | 내부성장루프 |
| 고객 응대 문구 | `docs/lua_bim_lab_official_documents/27_CS_RESPONSE_SCRIPT.md` | 고객지원CS |

승격 전 확인:
- Evidence Pass에 KST 등급 또는 내부 선례가 있는가
- Challenge Pass에서 실패 조건 또는 예외 조건이 기록되었는가
- Consensus Record에 합의 상태가 명시되었는가
- Execution Handoff에 담당, 기한, 검증 방법이 있는가

## 8. 템플릿 내재화 운영

개인/업무 자료, 프로젝트 산출물, 외부 공개 자료에서 반복 사용 가치가 높은 문서 형식이 발견되면 `지식 큐레이션·인텔리전스 셀`은 해당 자료를 다음 원칙으로 내재화한다.

| 원칙 | 기준 |
|---|---|
| 원문 비복사 | 원본 문구, 고객명, 프로젝트명을 복사하지 않고 구조와 운영 논리만 추출 |
| LUA BIM LAB 테마 적용 | 문서번호, 배포등급, 목적, 적용범위, 표 중심 구성, 승인 흐름을 부여 |
| 업무 흐름 연결 | 보고서, 등록부, 체크리스트, 교육자료, 제품문서 중 어디에 쓰일지 명시 |
| 보안 등급 부여 | Public, Client-Shareable, Internal, Confidential 중 하나로 분류 |
| Obsidian 연결 | 원천 후보, 표준문서, 교육자료, 제품 기능 후보, 오류 오답노트와 링크 |

우선 내재화 대상은 `오류검토/RFI`, `품질 이슈 등록부`, `BIM 라이브러리 등록부`, `Dynamo 자동화 카탈로그`, `프로젝트 인수인계서`로 한다.

## 9. 공개 차단 기준

다음 정보는 외부 공개 문서로 자동 승격하지 않는다.

- 고객명, 프로젝트명, 계약 조건, 비용 구조
- 계정, 토큰, 내부 경로, 보안 설정
- Revit API 환경에서 검증되지 않은 기능
- Qwen 또는 AI 초안 중 검수되지 않은 내용
- 내부 의사결정, 실패 기록, 전략 가설
- 법무/보안 검토가 필요한 문구

## 10. RACI

| 업무 | CSO | 교육컨설팅 | 지식큐레이터 | 지식업데이트 | QA | 테크니컬 라이터 | 보안/법무 |
|---|---|---|---|---|---|---|---|
| 목적성 기준 수립 | A | R | R | C | C | C | C |
| 일일 큐레이션 | C | A | R | R | C | C | I |
| 오류 지식 승격 | I | C | R | C | A/R | C | I |
| 교육자료 반영 | C | A/R | R | C | C | R | I |
| 상품문서 반영 | A | C | R | C | R | R | C |
| 공개 등급 점검 | I | C | R | C | C | C | A/R |
| Obsidian 연결 개선 | I | A | R | R | C | R | I |

## 11. 관련 문서

- `15_KNOWLEDGE_DOCUMENT_REPOSITORY_POLICY.md`
- `20_PUBLIC_DISCLOSURE_DB_READINESS_CHECKLIST.md`
- `22_EXTERNAL_PERSONAL_ARCHIVE_KNOWLEDGE_INTAKE_STANDARD.md`
- `29_ORGANIZATIONAL_KNOWLEDGE_LEARNING_AND_EVIDENCE_RESPONSE_STANDARD.md`
- `30_AI_TO_AI_COLLABORATION_SOP.md`
- `31_AI_COLLABORATION_RUNBOOK_TEMPLATES.md`
- `32_AI_COLLABORATION_UTILIZATION_AUDIT.md`
- `docs/standard_documents/24_BIM_ISSUE_REVIEW_REPORT_TEMPLATE.md`
- `docs/standard_documents/25_PROJECT_QUALITY_ISSUE_REGISTER_TEMPLATE.md`
- `docs/standard_documents/26_BIM_LIBRARY_FAMILY_REGISTER_TEMPLATE.md`
- `docs/standard_documents/27_DYNAMO_AUTOMATION_NODE_CATALOG_TEMPLATE.md`
- `docs/standard_documents/28_PROJECT_HANDOVER_KNOWLEDGE_TRANSFER_TEMPLATE.md`
- `docs/revenue_products/model_quality_audit/14_OBSIDIAN_KNOWLEDGE_SYSTEM.md`
- `knowledge/10_agents/09_지식팀/지식업데이트.md`
- `knowledge/10_agents/09_지식팀/지식큐레이터.md`
- `knowledge/10_agents/90_확장에이전트/최고전략CSO.md`
- `obsidian_vaults/lua_bim_lab_global_map/00_Home/Global Knowledge Map.md`

## 12. 조직 학습 연계

지식 큐레이션·인텔리전스 셀은 수집 지식을 보관하는 데서 끝내지 않고, 역할별 학습 과제로 전환한다.

운영 기준:
- 신규 공식 기준 업데이트는 `KST01 공식확인` 또는 `KST03 적용주의`로 상태 코드를 부여한다.
- 자동 수집 지식은 기본적으로 `KST04 자동수집`으로 두고, 공식 확인 전 확정 기준으로 승격하지 않는다.
- 교육컨설팅과 HR은 주 1회 역할별 학습 레인에 맞춰 3개 이하의 학습 과제를 배정한다.
- CS, PM, QA, BIM 수행팀은 고객/내부 중요 응답에 결론, 근거, 적용 범위, 주의, 다음 액션을 포함한다.
- 반복 질문은 FAQ, 교육자료, QA 체크리스트, 표준문서 후보로 등록한다.

관련: [[LUA BIM LABS Organizational Knowledge Learning Evidence Response Standard]] · [[교육컨설팅 지식 베이스]] · [[HR_인재분석관 지식 베이스]]
