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

## 3. 기한 전 확인 질문

| 질문 | 적용 케이스 | 통과 기준 |
|---|---|---|
| Owner가 단일한가 | 006, 007 | `CONFLICT_LOG`와 세션 등록부의 Owner가 일치 |
| 임시 보호 원칙이 있는가 | 006, 007 | 006은 `LOCAL_ONLY/BLOCKED`, 007은 `APPROVED_WITH_HOLD` 유지 |
| 실패 시 기본 행동이 있는가 | 006, 007 | 006은 외부 AI 사용 보류, 007은 Starter 외 Coming Soon 유지 |
| 닫힘 증거의 목적지가 정해졌는가 | 006, 007 | Decision Log, KB, QA, Backlog 중 필요한 목적지가 명시 |
| 다음 검토일이 있는가 | 006, 007 | 2026-06-12 |

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

## 5. 2026-06-06 일일 인계 점검

| 케이스 | 전일 상태 | 2026-06-06 상태 | 변경 | 다음 액션 |
|---|---|---|---|---|
| `AITEST_20260605_006` | ON_TRACK / BLOCKED / Draft Created | ON_TRACK / BLOCKED / Draft Created | 변경 없음 | 2026-06-12 승인성 재판정 |
| `AITEST_20260605_007` | ON_TRACK / APPROVED_WITH_HOLD / Draft Created | ON_TRACK / APPROVED_WITH_HOLD / Draft Created | 변경 없음 | 2026-06-12 승인성 재판정 |

판정: 2026-06-06 기준 둘 다 기한 전이며, Owner, Due by, 임시 원칙, source of truth 초안이 있으므로 `ON_TRACK`을 유지한다.

## 6. 결론

2026-06-05 기준 `AITEST_20260605_006`, `AITEST_20260605_007`은 아직 기한 전이므로 닫힘을 요구하지 않는다.
둘 다 source of truth 초안은 생성되었지만 최종 승인 전이므로 `ON_TRACK`으로 유지한다.
