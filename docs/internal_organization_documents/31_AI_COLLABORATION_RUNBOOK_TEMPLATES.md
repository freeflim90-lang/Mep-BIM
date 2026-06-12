# AI 협업 실행 런북 및 템플릿

문서번호: LBL-ORG-031
문서상태: 내부 실행 양식
작성일: 2026-06-05
작성주체: LUA BIM LAB
적용범위: AI 간 협업 세션 실행, 회의록, 합의 기록, 테스트 리허설, 내재화 추적

## 1. 사용 원칙

이 문서는 `30_AI_TO_AI_COLLABORATION_SOP.md`를 실제 업무에 적용하기 위한 실행 양식이다.
협업 세션을 시작할 때 아래 템플릿 중 하나를 선택해 기록하고, 종료 시 결정 로그 또는 지식베이스로 연결한다.

| 상황 | 사용할 템플릿 |
|---|---|
| 일반 협업 시작 | T01 협업 세션 카드 |
| AI 의견 수집 | T02 Evidence Pass |
| 반론/검토 | T03 Challenge Pass |
| 합의 확정 | T04 Consensus Record |
| 실행 인계 | T05 Execution Handoff |
| 회고/내재화 | T06 Retrospective |
| 월간 리허설 | T07 Scenario Test Record |

## 1.1 AI 협업 세션 등록부

반복 운영 시 아래 등록부를 월 단위로 복사해 사용한다.

| 세션 ID | 일시 | 요청자 | 모드 | 주관 AI | 참여 AI | 상태 | 합의 상태 | 리스크 게이트 | 결정 로그 | 충돌/테스트 케이스 | Reuse Closure | 다음 검토일 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AICOL-YYYYMMDD-NNN | YYYY-MM-DD HH:MM | [이름/채널] | [모드] | [AI명] | [AI명] | OPEN / IN_REVIEW / SETTLED / ESCALATED / CLOSED / DEFERRED | CONSENSUS / CONSENSUS_WITH_GUARDRAILS / SPLIT_DECISION / ESCALATE | NOT_NEEDED / LOCAL_ONLY / REDACTED_REVIEW / APPROVED / APPROVED_WITH_HOLD / BLOCKED | [링크] | [링크] | Created / Updated / Explicitly Deferred / Missing | [YYYY-MM-DD] |

## 1.2 ESCALATED SLA 추적부

`ESCALATED` 상태가 생기면 아래 표를 별도 월간 추적부에 복사한다.

| 케이스 | 세션 | Owner | Due by | 리스크 상태 | 필요한 산출물 | 현재 SLA 상태 | 근거 |
|---|---|---|---|---|---|---|---|
| AITEST-YYYYMMDD-NNN | AICOL-YYYYMMDD-NNN | [AI명] | YYYY-MM-DD | NOT_NEEDED / LOCAL_ONLY / REDACTED_REVIEW / APPROVED / APPROVED_WITH_HOLD / BLOCKED | Decision Log / KB / QA / Backlog / source of truth | ON_TRACK / AT_RISK / BREACHED / CLOSED | [한 줄 근거] |

SLA 상태 판정:

| 상태값 | 의미 |
|---|---|
| ON_TRACK | 기한 전이며 Owner, Due by, 임시 원칙, 실패 시 조치가 있음 |
| AT_RISK | 기한 전이나 Owner, 산출물, 승인자, 검증 방법 중 하나가 비어 있음 |
| BREACHED | 기한이 지났고 닫힘 증거가 없음 |
| CLOSED | 결정 또는 명시적 보류 증거가 있음 |

## T01 협업 세션 카드

```markdown
# AI 협업 세션 카드

- 세션 ID: AICOL-YYYYMMDD-NNN
- 요청 요약:
- 세션 일시:
- 요청자:
- 업무 유형: 기술 / 고객응대 / 견적 / 법무 / 보안 / 제품화 / 교육 / 전략 / 운영
- 긴급도: 즉시 / 24시간 / 주간 / 보류
- 우선순위 근거:
- 주관 AI:
- 검토 AI:
- 반론 AI:
- 결정권자:
- 산출물:
- 저장 위치:
- 연결 문서:

## Risk/Data/External AI Gate

| 항목 | 내용 |
|---|---|
| 데이터 등급 | Public / Client-Shareable / Internal / Confidential |
| 민감 신호 | 개인정보 / 고객명 / 프로젝트명 / 도면 / 계약 / 가격 / 내부 경로 / 계정·토큰 / 없음 |
| 외부 AI 모드 | Local-only / Redacted external review candidate / External allowed |
| 외부 AI 금지 또는 허용 사유 | |
| 익명화 증거 | 제거 필드, 샘플 링크, 감사자 |
| 고객 동의/계약 근거 | |
| 승인자 | 보안관 / 법무 / CFO / COO / CEO |
| 리스크 게이트 상태 | NOT_NEEDED / LOCAL_ONLY / REDACTED_REVIEW / APPROVED / APPROVED_WITH_HOLD / BLOCKED |

## 성공 조건

- [ ] 최종 결론이 합의 상태 4종 중 하나로 종료됨
- [ ] 담당자, 기한, 검증 방법이 있음
- [ ] Reuse Closure 상태가 Created, Updated, 또는 Explicitly Deferred임
- [ ] 해당 시 Risk/Data/External AI Gate가 작성됨
```

## T02 Evidence Pass

```markdown
## Evidence Pass

### [AI명]

- 판단:
- 근거:
- KST 등급: KST01 / KST03 / KST04 / KST06
- 출처 또는 내부 선례:
- 적용 조건:
- 불확실성:
- 다른 AI에게 확인할 질문:
- 결론 신뢰도: High / Medium / Low
```

## T03 Challenge Pass

```markdown
## Challenge Pass

### [검토/반론 AI명]

- 검토 대상 판단:
- 누락된 근거:
- 역할 경계 문제:
- 실행 리스크:
- 법무/보안/비용/고객 신뢰 리스크:
- 현장 예외 조건:
- 반대 또는 조건부 동의:
- 수정 제안:
```

## T04 Consensus Record

```markdown
## Consensus Record

- 합의 상태: CONSENSUS / CONSENSUS_WITH_GUARDRAILS / SPLIT_DECISION / ESCALATE
- conflict_resolution 상태: OPEN / PENDING / MEDIATED / ESCALATED / SETTLED / PRECEDENT / N/A
- 최종 결정:
- 채택한 근거:
- 기각한 대안:
- 조건 및 제한:
- 결정권자:
- 확정일:
- 다음 검토일:

## Customer/Commercial Release Gate

| 항목 | 내용 |
|---|---|
| 최종 고객 문구 링크 | |
| 배포 등급 | Internal / Client-Shareable / Public |
| 법무 승인 | 필요 없음 / 승인자 / 보류 |
| 보안 승인 | 필요 없음 / 승인자 / 보류 |
| CFO 가격 승인 | 필요 없음 / 승인자 / 보류 |
| 출시 상태 출처 | 판매 가능 / Coming Soon / 내부 검토 / 보류 |
| 예외 조건 | 무상 지원 / 할인 / 환불 / 납기 약속 / 없음 |
```

## T05 Execution Handoff

```markdown
## Execution Handoff

| 항목 | 내용 |
|---|---|
| 실행 담당 | |
| 협업 담당 | |
| 기한 | |
| 입력 데이터 | |
| 완료 산출물 | |
| 검증 방법 | |
| 실패 시 조치 | |
| 보류 조건 | |
| 지식화 위치 | |
```

## Reuse Closure

| 목적지 | 정확한 파일/경로 | 담당 | 기한 | 생성/수정 링크 | 검증자 | 상태 |
|---|---|---|---|---|---|---|
| Decision Log | | | | | | Created / Updated / Explicitly Deferred / Missing |
| KB | | | | | | Created / Updated / Explicitly Deferred / Missing |
| QA/Checklist | | | | | | Created / Updated / Explicitly Deferred / Missing |
| Training | | | | | | Created / Updated / Explicitly Deferred / Missing |
| Backlog | | | | | | Created / Updated / Explicitly Deferred / Missing |
| Conflict Precedent | | | | | | Created / Updated / Explicitly Deferred / Missing |

## T06 Retrospective

```markdown
## Retrospective

- 빨랐던 판단 경로:
- 막힌 지점:
- 다시 사용할 선례:
- SOP 보완 필요:
- KB 업데이트 필요:
- 교육자료 필요:
- 자동화 후보:
- 다음 리허설 시나리오:
```

## T07 Scenario Test Record

```markdown
# AI 협업 시나리오 테스트 기록

- 테스트 ID: AITEST-YYYYMMDD-NNN
- 시나리오: S01 기술 구현 / S02 고객 응대 / S03 견적 계약 / S04 보안 개인정보 / S05 전략 제품화 / S06 AI 판단 충돌
- 테스트일:
- 주관:
- 참여 AI:
- 결과: PASS / CONDITIONAL / FAIL

## 평가

| 평가 항목 | PASS/CONDITIONAL/FAIL | 근거 |
|---|---|---|
| 역할 라우팅 | | |
| 근거 품질 | | |
| 반론 품질 | | |
| 합의 도출 | | |
| 실행 인계 | | |
| 지식화 | | |
| 리스크/외부AI 게이트 | | |

## 개선 액션

| 액션 | 담당 | 기한 | 저장 위치 |
|---|---|---|---|
| | | | |
```

## 2. 운영 게이트

협업 세션은 아래 게이트를 통과해야 완료로 본다.

| 게이트 | 통과 기준 | 미통과 시 조치 |
|---|---|---|
| G1 역할 게이트 | 주관 AI와 검토/반론 AI가 분리됨 | 조율차장이 재배정 |
| G2 근거 게이트 | 핵심 판단에 KST 또는 선례가 있음 | 지식큐레이터에게 보강 요청 |
| G3 반론 게이트 | 최소 1개 실패 조건이 기록됨 | Challenge Pass 재수행 |
| G4 결정 게이트 | 합의 상태 4종 중 하나로 종료됨 | 결정권자 에스컬레이션 |
| G5 실행 게이트 | 담당, 기한, 검증 방법이 있음 | Execution Handoff 보완 |
| G6 내재화 게이트 | Reuse Closure 상태가 Created, Updated, 또는 Explicitly Deferred임 | Reuse Closure 보완 |
| G7 리스크/배포 게이트 | 데이터/외부AI/고객/가격 리스크가 해당 시 기록됨 | Risk/Data 또는 Release Gate 재수행 |

## 3. 협업 안티패턴

| 안티패턴 | 위험 | 교정 방법 |
|---|---|---|
| 의견 병렬 나열 | 결론 없이 회의가 끝남 | Consensus Record 작성 의무화 |
| 근거 없는 확신 | 잘못된 자동화/고객 응대 발생 | KST 등급 없으면 가설로 표시 |
| 반론 생략 | 법무/보안/비용 리스크 누락 | 반론 AI 지정 |
| 침묵을 승인으로 간주 | 실무 검증 없이 규칙 승격 | 침묵은 보류 원칙 적용 |
| 모든 사안을 조율차장에게 집중 | 병목 발생 | 주관 AI 1차 결론 의무화 |
| 실행 인계 누락 | 합의 후 실제 작업 미진행 | 담당/기한/검증 방법 없으면 미완료 |

## 4. 월간 운영 리듬

| 시점 | 활동 | 산출물 |
|---|---|---|
| 매주 월요일 | 지난주 AI 협업 세션 3건 샘플 점검 | 미흡 항목 메모 |
| 매주 금요일 | 반복 충돌과 결정 로그 확인 | 선례 후보 |
| 매월 첫째 주 | 6개 시나리오 리허설 | Scenario Test Record |
| 매월 마지막 주 | KPI와 성숙도 리뷰 | SOP 개정 후보 |

## 5. 성숙도 모델

| 단계 | 상태 | 판단 기준 |
|---|---|---|
| L1 임시 협업 | AI별 의견은 있으나 형식이 다름 | 세션 카드 없음 |
| L2 표준 협업 | Intake와 Evidence Pass가 사용됨 | 주관 AI 지정률 80% 이상 |
| L3 검증 협업 | Challenge Pass와 Consensus Record가 정착됨 | 결정 로그 완성률 90% 이상 |
| L4 학습 협업 | 회고가 KB, QA, 교육, 자동화 후보로 연결됨 | 월 5건 이상 지식화 |
| L5 자동 개선 협업 | 라우팅, 선례 참조, KPI 점검이 자동화됨 | 월간 리허설과 선례 재사용 안정화 |
