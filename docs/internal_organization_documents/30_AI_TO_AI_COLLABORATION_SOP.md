# AI 간 협업 의사소통 및 합의 운영 기준

문서번호: LBL-ORG-030
문서상태: 내부 운영 기준 초안
작성일: 2026-06-05
작성주체: LUA BIM LAB
적용범위: AI 담당자 간 협업, 추론 검증, 의견 충돌, 합의 도출, 실행 인계, 조직 내재화

## 1. 목적

이 문서는 LUA BIM LAB의 AI 담당자들이 같은 문제를 함께 다룰 때 의사소통, 추론, 반론, 합의, 실행 인계가 흔들리지 않도록 하는 표준 운영 기준이다.

목표는 세 가지다.

1. AI끼리의 의견이 병렬 나열로 끝나지 않고 실행 가능한 결론으로 수렴한다.
2. 판단 근거, 불확실성, 반대 의견, 결정권자를 기록해 같은 논쟁을 반복하지 않는다.
3. 반복 협업 결과를 지식베이스, 체크리스트, 교육자료, 자동화 백로그로 승격한다.

## 2. 기본 원칙

| 원칙 | 운영 기준 |
|---|---|
| 역할 우선 | 모든 AI는 자기 소유 역할 안에서 1차 판단한다. 경계 밖 판단은 소유 AI에게 넘긴다. |
| 근거 우선 | 결론보다 근거, KST 등급, 출처, 적용 조건을 먼저 남긴다. |
| 반론 의무 | 중요한 결정은 최소 1개 이상의 반대 관점 또는 실패 조건을 포함한다. |
| 합의 형식 고정 | 최종 결론은 결정, 근거, 실행 담당, 기한, 보류 조건을 포함한다. |
| 침묵은 보류 | 실무 첨언 또는 소유 AI 의견이 없으면 확정이 아니라 가설 상태로 둔다. |
| 선례 재사용 | 반복되는 충돌과 합의는 `conflict_resolution` 선례로 승격해 다음 판단에 재사용한다. |

## 3. 협업 참여 역할

| 역할 | 책임 |
|---|---|
| 요청 수신 AI | 사용자 요청을 업무 유형, 긴급도, 필요한 담당 AI로 분해한다. |
| 주관 AI | 결론 소유자다. 최종 산출물 품질과 실행 인계를 책임진다. |
| 검토 AI | 주관 AI의 판단을 근거, 리스크, 누락 항목 중심으로 검토한다. |
| 반론 AI | 의도적으로 실패 가능성, 예외 조건, 비용, 보안, 법무 리스크를 제기한다. |
| 조율차장 | 역할 충돌, 우선순위 충돌, 결론 교착을 중재한다. |
| 결정권자 AI | CEO, COO, CSO, CFO 등 상위 판단이 필요한 사안을 확정한다. |
| 지식큐레이터 | 합의 결과를 지식베이스, QA, 체크리스트, 선례로 승격한다. |

## 4. 표준 협업 프로세스

### 4.1 Intake

요청 수신 AI는 다음 6개 필드를 먼저 정리한다.

| 필드 | 기록 기준 |
|---|---|
| 요청 요약 | 사용자가 원하는 최종 상태를 한 줄로 정리 |
| 업무 유형 | 기술, 고객응대, 견적, 법무, 보안, 제품화, 교육, 전략, 운영 중 선택 |
| 긴급도 | 즉시, 24시간, 주간, 보류 |
| 주관 AI | 최종 결론 소유자 |
| 참여 AI | 필요한 검토자와 반론자 |
| 산출물 | 답변, 문서, 코드, 체크리스트, 로그, 백로그 중 선택 |

### 4.1.1 Risk/Data/External AI Gate

고객, 프로젝트, 계약, 가격, 개인정보, 법무, 보안, 외부 배포가 포함되면 Intake 직후 아래 게이트를 먼저 기록한다.

| 항목 | 기록 기준 |
|---|---|
| 데이터 등급 | Public / Client-Shareable / Internal / Confidential |
| 민감 신호 | 개인정보, 고객명, 프로젝트명, 도면, 계약, 가격, 내부 경로, 계정/토큰 |
| 외부 AI 모드 | Local-only / Redacted external review candidate / External allowed |
| 외부 AI 금지 사유 | 금지 또는 보류 시 이유 |
| 익명화 증거 | 제거한 필드, 샘플 감사자, 감사일 |
| 고객 동의/계약 근거 | 동의서, 계약 조항, 처리위탁/제3자 제공 여부 |
| 승인자 | 보안관, 법무, CFO, COO, CEO 중 해당자 |

기본값은 `Local-only`이다. 외부 AI 사용은 허용이 아니라 예외로 취급한다.

리스크 게이트 상태값은 아래 중 하나만 사용한다. 리스크 영역이 여러 개면 가장 제한적인 상태를 세션 등록부에 기록하고, 세부 영역은 게이트 표에 남긴다.

| 상태값 | 의미 | 사용 조건 |
|---|---|---|
| NOT_NEEDED | 별도 리스크 게이트 불필요 | 공개 정보, 내부 운영 메모 등 민감 신호 없음 |
| LOCAL_ONLY | 외부 AI 또는 외부 공유 금지 | 고객/프로젝트/개인정보/계약/가격 등 민감 신호 포함 |
| REDACTED_REVIEW | 익명화된 제한 검토 후보 | 보안관 또는 법무가 제거 필드와 감사 증거를 확인 |
| APPROVED | 필요한 승인 완료 | 보안/법무/가격/배포 승인자가 확인 |
| APPROVED_WITH_HOLD | 내부 검토는 가능하나 고객 발송, 공개 판매, 외부 전송은 보류 | 출시 상태, 가격표, 법무 문구, 고객 동의 중 하나가 미확정 |
| BLOCKED | 리스크 때문에 실행 중단 | 금지 데이터, 미승인 외부 전송, 확정 불가 정책 충돌 |

### 4.2 Role Framing

주관 AI는 협업 시작 전에 각 AI의 발언 범위를 지정한다.

```text
주관: 요구사항분석
검토: 프로그램개발, QA_테스터, 빌드검증
반론: 라이선스_보안관, 법무조항검토
결정권자: COO
```

### 4.3 Evidence Pass

각 AI는 자기 의견을 다음 형식으로 제출한다.

```text
[AI명]
판단:
근거:
KST 등급:
적용 조건:
불확실성:
다른 AI에게 확인할 질문:
```

KST 등급이 낮은 의견은 확정 결론이 아니라 가설로 취급한다.

### 4.4 Challenge Pass

검토 AI와 반론 AI는 다음 항목을 확인한다.

| 항목 | 질문 |
|---|---|
| 근거 | 공식 출처 또는 내부 선례가 있는가 |
| 역할 | 결론 소유자가 맞는가 |
| 실행성 | 담당자, 기한, 입력 데이터가 있는가 |
| 리스크 | 법무, 보안, 비용, 고객 신뢰 리스크가 누락되지 않았는가 |
| 예외 | 현장 조건에 따라 달라지는 부분이 명시되었는가 |

### 4.5 Consensus Pass

합의는 다음 4단계 중 하나로만 기록한다.

| 합의 상태 | 의미 | 다음 행동 |
|---|---|---|
| CONSENSUS | 참여 AI가 같은 결론에 동의 | 실행 인계 |
| CONSENSUS_WITH_GUARDRAILS | 결론은 동의하나 조건과 제한이 있음 | 조건부 실행 |
| SPLIT_DECISION | 의견이 갈렸으나 소유 AI 또는 결정권자가 선택 | 결정 로그 기록 |
| ESCALATE | AI 수준에서 확정 불가 | 조율차장 또는 상위 결정권자에게 인계 |

충돌 로그에는 실행 상태를 별도로 기록한다. 합의 상태 `ESCALATE`는 conflict_resolution 상태 `ESCALATED`로 매핑한다.

| 합의 상태 | conflict_resolution 상태 |
|---|---|
| CONSENSUS | SETTLED |
| CONSENSUS_WITH_GUARDRAILS | SETTLED |
| SPLIT_DECISION | SETTLED 또는 ESCALATED |
| ESCALATE | ESCALATED |

`ESCALATED` 상태는 실패가 아니라 상위 결정 대기 상태다. 단, 다음 필드가 없으면 운영 방치로 간주한다.

| 필드 | 필수 기준 |
|---|---|
| Owner | 최종 후속 산출물을 닫을 단일 책임자 |
| Due by | 다음 검토일 또는 결정 기한 |
| Temporary rule | 결정 전까지 적용할 임시 보호 원칙 |
| Failure action | 기한 초과 또는 결정 실패 시 기본 행동 |
| Closure destination | Decision Log, KB, QA, Backlog, source of truth 중 닫힘 증거 위치 |

기한 전 `ESCALATED` 케이스는 `ON_TRACK` 또는 `AT_RISK`로 추적하고, 기한 이후에는 `CLOSED`, `Explicitly Deferred`, `BREACHED` 중 하나로 재판정한다.

### 4.6 Decision Record

최종 결론은 반드시 다음 형식으로 남긴다.

```text
결정:
채택한 근거:
기각한 대안:
실행 담당:
기한:
검증 방법:
보류 조건:
지식화 위치:
```

### 4.7 Execution Handoff

실행 인계에는 다음 중 하나 이상이 포함되어야 한다.

| 산출물 | 위치 |
|---|---|
| 의사결정 로그 | `docs/internal_organization_documents/12_DECISION_LOG_TEMPLATE.md` |
| 리스크 등록 | `docs/internal_organization_documents/14_INTERNAL_RISK_ISSUE_REGISTER.md` |
| 충돌 로그 | `knowledge/10_agents/conflict_resolution/CONFLICT_LOG.md` |
| 지식베이스 업데이트 | `knowledge/10_agents/90_확장에이전트/*.md` |
| 교육자료 | `knowledge/60_public/training_curriculum/` |
| 자동화 백로그 | `docs/internal_growth/AX_INTERNAL_GROWTH_BACKLOG.md` |

### 4.7.1 Customer/Commercial Release Gate

고객 발송 또는 상업 판단이 포함된 세션은 실행 인계 전에 아래 항목을 기록한다.

| 항목 | 기록 기준 |
|---|---|
| 최종 고객 문구 | 발송 대상 문구 또는 저장 링크 |
| 배포 등급 | Internal / Client-Shareable / Public |
| 법무/보안 승인 | 승인자와 승인일 |
| 가격 기준 | CFO 승인 가격표 또는 견적 기준 링크 |
| 출시 상태 | 판매 가능 / Coming Soon / 내부 검토 / 보류 |
| 예외 조건 | 무상 지원, 할인, 환불, 납기 약속의 제한 조건 |

가격, 무상 지원, 환불, 납기 보상은 CFO 또는 CEO 승인 전 확정 문구로 발송하지 않는다.
상업/고객 배포 게이트에서 가격, 출시 상태, 법무 문구 중 하나라도 보류면 세션 리스크 상태는 `APPROVED_WITH_HOLD` 또는 `BLOCKED`로 기록한다.

### 4.8 Retrospective

중요 협업 종료 후 주관 AI는 5분 회고를 남긴다.

| 질문 | 기록 기준 |
|---|---|
| 무엇이 빨랐나 | 재사용 가능한 판단 경로 |
| 어디서 막혔나 | 역할 충돌, 근거 부족, 정보 부족 |
| 다음에는 무엇을 자동화할까 | 템플릿, 라우팅, 체크리스트 후보 |
| 지식화할 것인가 | KB, QA, 교육, 선례 중 선택 |

### 4.9 Completion Gate

협업 세션은 아래 6개 게이트를 통과해야 완료로 본다.

| 게이트 | 통과 기준 | 증거 |
|---|---|---|
| G1 역할 게이트 | 주관 AI와 검토/반론 AI가 분리됨 | 협업 세션 카드 |
| G2 근거 게이트 | 핵심 판단에 KST 등급 또는 내부 선례가 있음 | Evidence Pass |
| G3 반론 게이트 | 최소 1개 실패 조건 또는 예외 조건이 기록됨 | Challenge Pass |
| G4 결정 게이트 | 합의 상태 4종 중 하나로 종료됨 | Consensus Record |
| G5 실행 게이트 | 담당, 기한, 검증 방법이 있음 | Execution Handoff |
| G6 내재화 게이트 | Reuse Closure 상태가 Created, Updated, 또는 Explicitly Deferred임 | Retrospective + Reuse Closure |
| G7 리스크/배포 게이트 | 데이터/외부AI/고객/가격 리스크가 해당 시 기록됨 | Risk/Data Gate 또는 Release Gate |

## 5. 상황별 협업 모드

| 상황 | 모드 | 필수 참여 AI | 종료 조건 |
|---|---|---|---|
| 단순 Q&A | FAST_ANSWER | 주관 AI | KST01 또는 내부 선례로 즉시 답변 |
| 기술 구현 | BUILD_REVIEW | 프로그램개발, QA_테스터, 빌드검증 | 테스트 또는 검증 방법 확정 |
| 고객 응대 | CLIENT_SAFE_RESPONSE | 고객지원CS, 법무조항검토, 라이선스_보안관 | 외부 발송 문구 확정 |
| 견적/계약 | COMMERCIAL_REVIEW | 견적심사원, CFO, 법무조항검토 | 가격, 범위, 예외 조건 확정 |
| 보안/개인정보 | SECURITY_GATE | 라이선스_보안관, 법무조항검토 | 공개 가능 범위 확정 |
| 전략/제품화 | STRATEGY_COUNCIL | 전략기획, CSO, 제품패키징, 프로그램개발 | 우선순위와 다음 실험 확정 |
| AI 간 충돌 | CONFLICT_RESOLUTION | 조율차장, 충돌 당사자 | `CONFLICT_LOG`에 SETTLED 또는 ESCALATED |
| 지식 승격 | KNOWLEDGE_PROMOTION | 지식큐레이터, 지식업데이트, 주관 AI | KST 등급과 저장 위치 확정 |

## 6. 테스트 및 내재화 기준

AI 협업 프로세스는 매월 최소 6개 시나리오로 리허설한다.

| 테스트 축 | 통과 기준 |
|---|---|
| 역할 라우팅 | 주관 AI와 검토 AI가 올바르게 배정됨 |
| 근거 품질 | 결론마다 KST 등급 또는 선례가 붙음 |
| 반론 품질 | 최소 1개 이상의 실행 리스크가 제기됨 |
| 합의 도출 | 합의 상태 4종 중 하나로 종료됨 |
| 실행 인계 | 담당, 기한, 검증 방법이 기록됨 |
| 지식화 | 반복 가능 항목이 KB, QA, 체크리스트, 백로그로 분류됨 |

리허설 기록은 `knowledge/10_agents/conflict_resolution/COLLABORATION_TEST_PLAN.md` 또는 케이스 파일에 남긴다.
실행 양식은 `31_AI_COLLABORATION_RUNBOOK_TEMPLATES.md`를 사용한다.

## 6.1 조직 내재화 절차

| 단계 | 주기 | 담당 | 산출물 |
|---|---|---|---|
| 협업 세션 샘플 점검 | 매주 | 조율차장 | 미흡 항목 메모 |
| 결정 로그 감사 | 매주 | 지식큐레이터 | 선례 후보 목록 |
| 6개 시나리오 리허설 | 매월 | 조율차장 | 테스트 기록 |
| SOP/KBI 개정 후보 정리 | 매월 | 내부성장루프 | 자동화/교육 후보 |
| 온보딩 반영 | 분기 | 경영지원, 지식큐레이터 | 교육자료 개정 |

## 6.2 성숙도 모델

| 단계 | 상태 | 다음 목표 |
|---|---|---|
| L1 임시 협업 | AI별 의견은 있으나 형식이 다름 | 세션 카드 도입 |
| L2 표준 협업 | Intake와 Evidence Pass가 사용됨 | 반론/검토 의무화 |
| L3 검증 협업 | Challenge Pass와 결정 로그가 정착됨 | 실행 인계 누락 제거 |
| L4 학습 협업 | 회고가 KB, QA, 교육, 자동화 후보로 연결됨 | 선례 재사용률 향상 |
| L5 자동 개선 협업 | 라우팅, 선례 참조, KPI 점검이 자동화됨 | 월간 자동 감사 |

## 7. 운영 KPI

| KPI | 목표 |
|---|---|
| 협업 건별 주관 AI 지정률 | 95% 이상 |
| 결정 로그 완성률 | 90% 이상 |
| 충돌 72시간 내 해소율 | 90% 이상 |
| 선례 재사용률 | 월 3건 이상 |
| KST04에서 KST01/03 승격 건수 | 월 5건 이상 |
| 회고에서 자동화 후보 도출률 | 월 2건 이상 |
| Reuse Closure 완료율 | 월간 협업 세션의 80% 이상 |
| 외부 AI Local-only 판정 준수율 | 민감 세션 100% |

## 8. 관련 문서

- `02_ROLE_RESPONSIBILITY_RACI.md`
- `03_DECISION_AUTHORITY_MATRIX.md`
- `11_INTERNAL_MEETING_CADENCE.md`
- `12_DECISION_LOG_TEMPLATE.md`
- `14_INTERNAL_RISK_ISSUE_REGISTER.md`
- `21_KNOWLEDGE_CURATION_INTELLIGENCE_CELL.md`
- `29_ORGANIZATIONAL_KNOWLEDGE_LEARNING_AND_EVIDENCE_RESPONSE_STANDARD.md`
- `31_AI_COLLABORATION_RUNBOOK_TEMPLATES.md`
- `knowledge/10_agents/01_경영진/조율차장.md`
- `knowledge/10_agents/conflict_resolution/README.md`
