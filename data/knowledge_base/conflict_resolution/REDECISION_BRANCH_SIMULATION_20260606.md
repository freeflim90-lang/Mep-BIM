# Redecision Branch Simulation - 2026-06-06

> 목적: `ESCALATED_REDECISION_EXECUTION_PLAYBOOK_20260606.md`가 2026-06-12 실제 결과 적용 전에 네 가지 결과 분기에서 일관된 상태값을 산출하는지 검증한다.

## 1. 시뮬레이션 전제

| 항목 | 값 |
|---|---|
| 대상 | `AICOL-20260605-006`, `AICOL-20260605-007` |
| 현재 원상태 | ESCALATED / ON_TRACK |
| 현재 보호 행동 | 006은 BLOCKED/Local-only, 007은 APPROVED_WITH_HOLD/Starter-only |
| 원본 변경 여부 | 없음 |
| 목적 | 결과별 기대 상태와 추가 필요 갱신을 고정 |

## 2. Branch A: 승인

| 대상 | Register 상태 | SLA 상태 | Risk Gate | Decision Log | Reuse Closure | 자동 감사 통과 조건 |
|---|---|---|---|---|---|---|
| 006 | CLOSED 가능 | CLOSED | APPROVED 또는 REDACTED_REVIEW | 선택안 A, 승인 범위/금지 데이터 갱신 | Updated | CLOSED로 전환하면 Register consensus도 `CONSENSUS_WITH_GUARDRAILS`, Reuse Closure `Updated` 필요 |
| 007 | CLOSED 가능 | CLOSED | APPROVED 또는 APPROVED_WITH_HOLD | Starter-only 또는 상품별 SALE_READY 범위 갱신 | Updated | CLOSED로 전환하면 SLA 본표에서 해당 원건 상태와 Register 상태가 충돌하지 않아야 함 |

승인 분기는 원건을 닫을 수 있지만, 자동 감사는 `CLOSED` 세션의 `ESCALATE` consensus를 허용하지 않는다.
따라서 Register 상태를 `CLOSED`로 바꾸면 consensus도 반드시 `CONSENSUS_WITH_GUARDRAILS`로 바꾼다.

## 3. Branch B: 명시적 보류

| 대상 | Register 상태 | SLA 상태 | Risk Gate | Decision Log | Reuse Closure | 자동 감사 통과 조건 |
|---|---|---|---|---|---|---|
| 006 | ESCALATED 유지 | ON_TRACK 또는 CLOSED | BLOCKED | 선택안 B, 보류 사유/다음 Owner/Due by | Created 또는 Updated | ESCALATED 유지 시 consensus `ESCALATE`, SLA risk `BLOCKED` 유지 |
| 007 | ESCALATED 유지 | ON_TRACK 또는 CLOSED | APPROVED_WITH_HOLD | 선택안 C, 보류 상품/다음 Owner/Due by | Created 또는 Updated | ESCALATED 유지 시 Decision Log Draft 경로와 필드 정합성 유지 |

명시적 보류는 승인 실패가 아니라 통제된 보류다.
보류 사유와 다음 Due by가 명확하면 `BREACHED`가 아니라 `ON_TRACK` 또는 닫힘 근거가 있는 `CLOSED`로 관리할 수 있다.

## 4. Branch C: 조건부 보완

| 대상 | Register 상태 | SLA 상태 | Risk Gate | Decision Log | Reuse Closure | 자동 감사 통과 조건 |
|---|---|---|---|---|---|---|
| 006 | ESCALATED 유지 | AT_RISK | BLOCKED | 선택안 C, 보완 항목/Owner/Due by | Created 또는 Updated | SLA status가 `AT_RISK`로 바뀌어도 risk는 Register와 동일해야 함 |
| 007 | ESCALATED 유지 | AT_RISK | APPROVED_WITH_HOLD | 조건부 보완 선택안, 상품별 보완 항목/Owner/Due by | Created 또는 Updated | 다음 검토일을 새 Due by로 바꾸면 Register/SLA/Decision Log가 같은 날짜를 가리켜야 함 |

조건부 보완은 Missing 항목이 남았다는 뜻이므로 원건은 닫지 않는다.
다만 Owner와 Due by가 명확해야 `BREACHED`가 아니라 `AT_RISK`로 관리된다.

## 5. Branch D: 위반

| 대상 | Register 상태 | SLA 상태 | Risk Gate | Decision Log | Reuse Closure | 자동 감사 통과 조건 |
|---|---|---|---|---|---|---|
| 006 | ESCALATED 유지 | BREACHED | BLOCKED | 선택안 D, BREACHED 사유/CEO-COO 에스컬레이션 | Created 또는 Updated | SLA status `BREACHED` 허용, Decision Log Draft는 실제 위반 사유로 갱신 필요 |
| 007 | ESCALATED 유지 | BREACHED | APPROVED_WITH_HOLD | 선택안 D, BREACHED 사유/CEO-COO 에스컬레이션 | Created 또는 Updated | 기본 행동 Starter-only 유지 |

위반 분기에서도 Register의 risk gate는 임시 보호 행동을 유지한다.
006은 외부 AI 전송 금지, 007은 Starter-only가 기본값이다.

## 6. Cross-Branch Invariants

| 불변조건 | 이유 |
|---|---|
| ESCALATED 유지 시 consensus는 `ESCALATE` | 자동 감사 INV-06 |
| CLOSED 전환 시 consensus는 `CONSENSUS_WITH_GUARDRAILS` | 자동 감사 INV-07 |
| CLOSED 전환 시 Reuse Closure는 `Updated` | 자동 감사 INV-10 |
| ESCALATED 원건은 Decision Log Draft가 실제 파일로 존재 | 자동 감사 INV-12 |
| Decision Log Draft 내부 필드는 원건과 일치 | 자동 감사 INV-13 |
| SLA risk는 Register risk와 일치 | 자동 감사 스크립트 risk 비교 |
| 006 승인 전 기본 행동은 Local-only | 보안/법무 보호 |
| 007 승인 전 기본 행동은 Starter-only | 상업/CS 보호 |

## 7. Reuse Closure

| 목적지 | 정확한 파일/경로 | 담당 | 기한 | 생성/수정 링크 | 검증자 | 상태 |
|---|---|---|---|---|---|---|
| 029 Case | `data/knowledge_base/conflict_resolution/cases/AITEST_20260606_029.md` | 조율차장 | 2026-06-06 | Branch Simulation | QA_테스터 | Created |
| Execution Playbook | `data/knowledge_base/conflict_resolution/ESCALATED_REDECISION_EXECUTION_PLAYBOOK_20260606.md` | 조율차장 | 2026-06-06 | Branch invariants 반영 | QA_테스터 | Updated |
| Session Register | `data/knowledge_base/conflict_resolution/SESSION_REGISTER_202606.md` | 조율차장 | 2026-06-06 | AICOL-20260606-029 | 조율차장 | Updated |

## 8. 결론

네 가지 분기 모두 적용 가능하지만 자동 감사 통과 조건이 다르다.
특히 승인 분기에서 원건을 `CLOSED`로 바꾸면 consensus와 Reuse Closure를 함께 바꿔야 하고, ESCALATED 유지 분기에서는 Decision Log Draft와 SLA risk 정합성이 계속 유지되어야 한다.
