# ESCALATION SLA Tracker - 2026-06

> 기준 템플릿: `docs/internal_organization_documents/31_AI_COLLABORATION_RUNBOOK_TEMPLATES.md`
> 목적: `ESCALATED` 상태의 AI 협업 세션이 기한 전 방치되지 않고 결정 로그, 정책 source of truth, KB/QA, 백로그 중 하나로 닫히는지 추적한다.

## 1. SLA 상태값

| 상태값 | 의미 | 판정 기준 |
|---|---|---|
| ON_TRACK | 기한 전이며 담당/산출물/실패 시 조치가 있음 | Due by 이전, Owner와 완료 산출물이 명확함 |
| AT_RISK | 기한 전이나 산출물, 승인자, 검증 방법 중 하나가 비어 있음 | Due by 이전, 추적 필드 일부 Missing |
| BREACHED | 기한이 지났고 닫힘 증거가 없음 | Due by 이후, Decision/KB/Backlog/Policy 중 어느 것도 Updated 아님 |
| CLOSED | 에스컬레이션이 결정 또는 명시적 보류로 닫힘 | Decision Log, source of truth, KB/QA, Backlog, Explicitly Deferred 중 증거 있음 |

## 2. 2026-06-05 사전 점검

| 케이스 | 세션 | Owner | Due by | 리스크 상태 | 필요한 산출물 | 현재 SLA 상태 | 근거 |
|---|---|---|---|---|---|---|---|
| `AITEST_20260605_006` | `AICOL-20260605-006` | 법무조항검토 | 2026-06-12 | BLOCKED | 외부 AI disclosure rule 결정 로그, privacy/legal/AI routing 문구 정합화, Local-only 예외 조건 | ON_TRACK | source of truth 초안 Created, CEO/법무/보안관 승인 전 |
| `AITEST_20260605_007` | `AICOL-20260605-007` | CFO | 2026-06-12 | APPROVED_WITH_HOLD | 상품별 Launch Status 표, CFO 승인 가격표, 고객 안내 문구 | ON_TRACK | Launch Status 초안 Created, CEO/CFO 승인 전 |
| `AITEST_20260606_030` | `AICOL-20260606-030` | 지식큐레이터 | 2026-06-13 | REDACTED_REVIEW | KST04 공식 출처, QA 고객 문구, 법무 검토, KST 승격 판단 | ON_TRACK | Decision Log Draft Created, 고객 확정 응답 전 |

## 3. 기한 전 확인 질문

| 질문 | 적용 케이스 | 통과 기준 |
|---|---|---|
| Owner가 단일한가 | 006, 007, 030 | `CONFLICT_LOG`와 세션 등록부의 Owner가 일치 |
| 임시 보호 원칙이 있는가 | 006, 007, 030 | 006은 `LOCAL_ONLY/BLOCKED`, 007은 `APPROVED_WITH_HOLD`, 030은 `REDACTED_REVIEW` 유지 |
| 실패 시 기본 행동이 있는가 | 006, 007, 030 | 006은 외부 AI 사용 보류, 007은 Starter 외 Coming Soon 유지, 030은 KST04 고객 확정 응답 금지 |
| 닫힘 증거의 목적지가 정해졌는가 | 006, 007, 030 | Decision Log, KB, QA, Backlog 중 필요한 목적지가 명시 |
| 다음 검토일이 있는가 | 006, 007, 030 | 006/007은 2026-06-12, 030은 2026-06-13 |

## 4. 2026-06-12 판정 규칙

| 조건 | 조치 |
|---|---|
| 결정 로그 또는 source of truth가 생성됨 | 해당 Reuse Closure를 Updated로 바꾸고 SLA 상태를 CLOSED로 변경 |
| 결정은 못 했지만 보류 사유와 다음 결정권자가 명확함 | Explicitly Deferred로 닫고 다음 Due by를 새로 설정 |
| Owner/산출물/검증 방법이 비어 있음 | AT_RISK로 강등하고 조율차장이 당일 재배정 |
| Due by 이후에도 닫힘 증거가 없음 | BREACHED로 기록하고 CEO/COO에게 에스컬레이션 |

## 4.1 2026-06-12 분기 판정 매트릭스

| 분기 | 조건 | conflict_resolution 상태 | SLA 상태 | 필수 조치 |
|---|---|---|---|---|
| 승인 | CEO/법무/보안/CFO가 초안을 승인하고 적용 범위가 명확함 | SETTLED 또는 PRECEDENT | CLOSED | 결정 로그 생성, KB/QA Updated, 등록부 Reuse Closure Updated |
| 명시적 보류 | 승인 불가 사유와 다음 결정권자/기한이 명확함 | ESCALATED 유지 또는 DEFERRED | CLOSED 또는 ON_TRACK | Explicitly Deferred 기록, 새 Due by 지정, 임시 원칙 유지 |
| 조건부 보완 | 일부 승인 조건이 비어 있으나 Owner와 보완 항목이 명확함 | ESCALATED | AT_RISK | 보완 항목/Owner/Due by 지정, 다음 일일 인계 포함 |
| 위반 | Due by 이후에도 결정/보류/보완 근거가 없음 | ESCALATED | BREACHED | CEO/COO 에스컬레이션, 원칙상 BLOCKED/HOLD 유지 |

케이스별 기본값:

| 케이스 | 승인 전 기본값 | 승인 실패 시 기본 행동 |
|---|---|---|
| `AITEST_20260605_006` | BLOCKED / Local-only | 외부 AI 사용 금지 유지 |
| `AITEST_20260605_007` | APPROVED_WITH_HOLD / Starter-only | Starter 외 Coming Soon 또는 Consultation-only 유지 |
| `AITEST_20260606_030` | REDACTED_REVIEW / KST04-only | 고객 확정 응답 금지, 내부 검토 초안 유지 |

## 5. 2026-06-06 일일 인계 점검

| 케이스 | 전일 상태 | 2026-06-06 상태 | 변경 | 다음 액션 |
|---|---|---|---|---|
| `AITEST_20260605_006` | ON_TRACK / BLOCKED / Draft Created | ON_TRACK / BLOCKED / Draft Created | 변경 없음 | 2026-06-12 승인성 재판정 |
| `AITEST_20260605_007` | ON_TRACK / APPROVED_WITH_HOLD / Draft Created | ON_TRACK / APPROVED_WITH_HOLD / Draft Created | 변경 없음 | 2026-06-12 승인성 재판정 |
| `AITEST_20260606_030` | 신규 등록 없음 | ON_TRACK / REDACTED_REVIEW / Draft Created | 신규 ESCALATED 등록 | 2026-06-13 KST 승격 재판정 |

판정: 2026-06-06 기준 006/007/030 모두 기한 전이며, Owner, Due by, 임시 원칙, Decision Log Draft가 있으므로 `ON_TRACK`을 유지한다.

## 6. 결론

2026-06-05 기준 `AITEST_20260605_006`, `AITEST_20260605_007`은 아직 기한 전이므로 닫힘을 요구하지 않는다.
2026-06-06 기준 `AITEST_20260606_030`도 신규 ESCALATED 원건으로 추가됐지만 2026-06-13 기한 전이므로 `ON_TRACK`으로 유지한다.
source of truth 초안 또는 Decision Log Draft는 생성됐지만 최종 승인 전이므로 고객 확정 응답과 외부 공개는 금지한다.

## 7. 2026-06-06 재판정 준비성 감사

| 케이스 | 준비성 | 통과 근거 | 남은 Missing | 2026-06-12 예상 분기 |
|---|---|---|---|---|
| `AITEST_20260605_006` | CONDITIONAL PASS | Owner, Due by, Local-only/BLOCKED, source of truth 초안 있음 | 제공자 약관, 보관/삭제, 학습 사용, 국외 이전, 고객 동의/처리위탁, CEO/법무/보안 승인 | 명시적 보류 또는 조건부 보완 가능성 높음 |
| `AITEST_20260605_007` | CONDITIONAL PASS | Owner, Due by, Starter-only/HOLD, Launch Status 초안 있음 | CEO/CFO 승인, 약관/환불 법무 검토, 운영 리소스, Starter 외 상품 승인 | 명시적 보류 또는 조건부 보완 가능성 높음 |

판정: `AITEST_20260606_023` 기준 006/007은 아직 기한 전이므로 `ON_TRACK`을 유지한다. 다만 Missing 항목이 그대로 남으면 2026-06-12에는 승인보다 명시적 보류 또는 조건부 보완으로 분기해야 한다.

## 8. 2026-06-06 Missing 증거 보완 큐

| 우선순위 | 케이스 | 보완 묶음 | Owner | Due by | 완료 기준 | 상태 |
|---|---|---|---|---|---|---|
| P0 | `AITEST_20260605_006` | 제공자 약관/보관/학습/국외이전 1차 법무 검토 | 법무조항검토 | 2026-06-12 | 승인 또는 보류 사유가 문서에 남음 | QUEUED |
| P0 | `AITEST_20260605_006` | 고객 동의/처리위탁/제3자 제공 라벨 결정 | 법무조항검토 | 2026-06-12 | 고객 고지 필요 여부가 명시됨 | QUEUED |
| P0 | `AITEST_20260605_007` | Starter-only 공개 범위와 금지 문구 확정 | CFO | 2026-06-12 | 고객지원CS가 사용할 문구가 확정됨 | QUEUED |
| P1 | `AITEST_20260605_007` | Starter 외 상품 운영 리소스 확인 | COO | 2026-06-12 | 판매 가능/불가 사유와 다음 Due by가 있음 | QUEUED |
| P1 | `AITEST_20260605_006/007` | 승인 로그 또는 명시적 보류 로그 생성 | 조율차장 | 2026-06-12 | SLA Tracker가 CLOSED, ON_TRACK, AT_RISK 중 하나로 갱신됨 | QUEUED |

판정: `AITEST_20260606_024` 기준 006/007은 아직 승인 상태가 아니다. 다만 Missing 항목이 보완 큐로 분해되었으므로, 2026-06-12에 보완 결과가 없으면 `AT_RISK` 또는 `BREACHED` 후보로 재판정한다.

## 9. 2026-06-06 Decision Log Draft 패키지

| 케이스 | Decision Log Draft | 현재 상태 | 2026-06-12 갱신 조건 |
|---|---|---|---|
| `AITEST_20260605_006` | `decision_logs/DEC-AICOL-20260605-006-DRAFT.md` | Draft Created | 승인, 명시적 보류, 조건부 보완, 위반 중 실제 결과로 선택안/결정 사유 갱신 |
| `AITEST_20260605_007` | `decision_logs/DEC-AICOL-20260605-007-DRAFT.md` | Draft Created | Starter-only 승인, Starter 외 보류, 조건부 보완, 위반 중 실제 결과로 선택안/결정 사유 갱신 |

판정: `AITEST_20260606_025` 기준 결정 로그 목적지는 `TBD`가 아니라 Draft 파일로 연결됐다. 다만 Draft는 최종 결정이 아니므로, 2026-06-12에 승인자와 실제 선택안을 반드시 갱신해야 한다.

## 10. 2026-06-06 재판정 결과 적용 플레이북

| 항목 | 파일 | 적용 시점 | 목적 |
|---|---|---|---|
| Redecision Execution Playbook | `ESCALATED_REDECISION_EXECUTION_PLAYBOOK_20260606.md` | 2026-06-12 재판정 직후 | Decision Log, SLA Tracker, 원 케이스, Register, KB/QA, 자동 감사 순서 고정 |

판정: `AITEST_20260606_028` 기준 승인, 명시적 보류, 조건부 보완, 위반 결과별 문서 전환 순서가 준비됐다. 현재 006/007 상태는 변경하지 않고, 2026-06-12 실제 결과에 따라 적용한다.

## 11. 2026-06-06 Branch 상태 전환 시뮬레이션

| 항목 | 파일 | 적용 시점 | 목적 |
|---|---|---|---|
| Redecision Branch Simulation | `REDECISION_BRANCH_SIMULATION_20260606.md` | 2026-06-12 재판정 직후 | 승인/보류/조건부 보완/위반 분기별 Register/SLA/Decision Log/자동 감사 기대 상태 확인 |

판정: `AITEST_20260606_029` 기준 네 가지 분기 모두 적용 가능하다. 승인 분기는 CLOSED 전환 시 consensus와 Reuse Closure 동시 갱신이 필요하고, ESCALATED 유지 분기는 Decision Log Draft와 SLA risk 정합성을 유지해야 한다.

## 12. 2026-06-06 KST04 승격 Source of Truth 및 Missing 증거 큐

| 항목 | 파일 | 적용 시점 | 목적 |
|---|---|---|---|
| KST04 Source of Truth Draft | `KST04_CUSTOMER_RESPONSE_PROMOTION_SOURCE_OF_TRUTH_DRAFT_20260606.md` | 2026-06-13 재판정 전 | 고객 확정 응답 금지선, 승격 조건, 재판정 선택지 고정 |
| KST04 Missing Evidence Matrix | `KST04_PROMOTION_MISSING_EVIDENCE_MATRIX_20260606.md` | 2026-06-13 재판정 전 | 공식 출처, 고객 문구, 법무 검토, QA 반례를 Owner/검증자/Due by로 분해 |

| 케이스 | 준비성 | 남은 Missing | 예상 분기 |
|---|---|---|---|
| `AITEST_20260606_030` | CONDITIONAL PASS | 공식 출처, 고객 문구, 법무 책임/면책 검토, QA 반례, KST 승격 판단 | 명시적 보류 또는 조건부 보완 가능성 높음 |

판정: `AITEST_20260606_031` 기준 030은 아직 기한 전이므로 `ON_TRACK`을 유지한다. 다만 P0 증거가 보완되지 않으면 2026-06-13에는 승인보다 명시적 보류 또는 조건부 보완으로 분기해야 한다.
