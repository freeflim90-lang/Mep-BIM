# ESCALATED Missing Evidence Matrix - 2026-06-06

> 목적: `AITEST_20260605_006`, `AITEST_20260605_007`의 2026-06-12 재판정 전에 Missing 항목을 실행 가능한 증거 단위로 분해한다.

## 1. 판정 원칙

| 증거 상태 | 의미 | 2026-06-12 분기 |
|---|---|---|
| APPROVAL_READY | 승인자, 근거 파일, 적용 범위, 고객/내부 문구가 모두 있음 | 승인 후보 |
| DEFERRAL_READY | 승인 불가 사유, 임시 원칙, 다음 Owner/Due by가 명확함 | 명시적 보류 후보 |
| REMEDIATION_READY | Missing 항목이 남았지만 보완 Owner/Due by와 금지 행동이 명확함 | 조건부 보완 후보 |
| INSUFFICIENT | 누가 무엇을 보완할지 불명확함 | AT_RISK 또는 BREACHED 후보 |

## 2. AITEST_20260605_006 외부 AI Disclosure Rule

| Missing 증거 | 최소 보완 산출물 | Owner | 검증자 | 보완 전 기본 행동 | 목표 상태 |
|---|---|---|---|---|---|
| 외부 AI 제공자명과 서비스 약관 확인 | 제공자명, 서비스명, 약관 URL/문서, 데이터 처리 조항 요약 | 법무조항검토 | 라이선스_보안관 | 외부 AI 전송 금지 | REMEDIATION_READY |
| 보관 기간과 삭제 가능 여부 | 보관 기간, 삭제 요청 가능 여부, 삭제 SLA, 고객 요청 대응 문구 | 라이선스_보안관 | 법무조항검토 | 외부 AI 전송 금지 | REMEDIATION_READY |
| 학습 사용 여부 | 입력 데이터의 모델 학습 사용 여부와 opt-out 가능 여부 | 법무조항검토 | 라이선스_보안관 | 외부 AI 전송 금지 | REMEDIATION_READY |
| 국외 이전 여부 | 처리 지역, 이전 국가, 법적 근거, 고객 고지 필요성 판단 | 법무조항검토 | CEO | 외부 AI 전송 금지 | REMEDIATION_READY |
| 고객 동의/처리위탁/제3자 제공 판단 | 고객 고지/동의/처리위탁/제3자 제공 중 필요한 법적 라벨 | 법무조항검토 | 고객지원CS | 외부 AI 전송 금지 | DEFERRAL_READY |
| CEO/법무/보안관 승인 | 승인 로그, 적용 범위, 금지 데이터 목록, 예외 승인 절차 | CEO, 법무조항검토, 라이선스_보안관 | 조율차장 | Local-only 유지 | APPROVAL_READY |

### 2.1 006 재판정 최소 결론

2026-06-12까지 모든 항목이 `APPROVAL_READY`가 아니면 외부 AI 사용은 승인하지 않는다.
다만 각 Missing 항목에 Owner, Due by, 금지 행동이 지정되면 `BREACHED`가 아니라 명시적 보류 또는 조건부 보완으로 닫을 수 있다.

## 3. AITEST_20260605_007 Product Launch Status

| Missing 증거 | 최소 보완 산출물 | Owner | 검증자 | 보완 전 기본 행동 | 목표 상태 |
|---|---|---|---|---|---|
| Starter 가격표 CFO 승인 | 승인 가격표, 통화, 결제 링크, 할인/환불 금지 조건 | CFO | CEO | Starter 외 공개 판매 금지 | APPROVAL_READY |
| CEO 출시 승인 | 판매 가능 상품 목록, 출시 범위, 보류 상품 목록 | CEO | CFO | Starter-only 유지 | APPROVAL_READY |
| 약관/환불 문구 법무 검토 | 고객 발송 약관, 환불 조건, 책임 제한, 금지 문구 | 법무조항검토 | 고객지원CS | 확정 환불 약속 금지 | REMEDIATION_READY |
| CS 고객 문구 확정 | Starter, Coming Soon, Consultation-only별 고객 응대 문구 | 고객지원CS | CFO | Draft 문구만 내부 사용 | REMEDIATION_READY |
| 운영 리소스 확인 | 운영 가능 시간, 담당자, 납품 범위, 수용 가능 고객 수 | COO | CFO | Standard/Intensive 판매 보류 | DEFERRAL_READY |
| Starter 외 상품 승인 | 상품별 Launch Status와 결제 링크 허용/금지 표 | CEO, CFO | 조율차장 | Coming Soon 또는 Consultation-only 유지 | APPROVAL_READY |

### 3.1 007 재판정 최소 결론

2026-06-12까지 Starter 외 상품은 CEO/CFO/법무/운영 리소스 증거가 모두 있어야 공개 판매할 수 있다.
증거가 부족하면 Starter-only는 유지하고, 나머지는 Coming Soon 또는 Consultation-only로 명시적 보류한다.

## 4. 재판정 전 보완 큐

| 우선순위 | 케이스 | 보완 묶음 | 담당 | Due by | 완료 기준 |
|---|---|---|---|---|---|
| P0 | 006 | 제공자 약관/보관/학습/국외이전 1차 법무 검토 | 법무조항검토 | 2026-06-12 | 승인 또는 보류 사유가 문서에 남음 |
| P0 | 006 | 고객 동의/처리위탁/제3자 제공 라벨 결정 | 법무조항검토 | 2026-06-12 | 고객 고지 필요 여부가 명시됨 |
| P0 | 007 | Starter-only 공개 범위와 금지 문구 확정 | CFO | 2026-06-12 | 고객지원CS가 사용할 문구가 확정됨 |
| P1 | 007 | Starter 외 상품 운영 리소스 확인 | COO | 2026-06-12 | 판매 가능/불가 사유와 다음 Due by가 있음 |
| P1 | 006/007 | 승인 로그 또는 명시적 보류 로그 생성 | 조율차장 | 2026-06-12 | SLA Tracker가 CLOSED, ON_TRACK, AT_RISK 중 하나로 갱신됨 |

## 5. Reuse Closure

| 목적지 | 정확한 파일/경로 | 담당 | 기한 | 생성/수정 링크 | 검증자 | 상태 |
|---|---|---|---|---|---|---|
| 024 Case | `data/knowledge_base/conflict_resolution/cases/AITEST_20260606_024.md` | 조율차장 | 2026-06-06 | Missing Evidence Matrix | QA_테스터 | Created |
| SLA Tracker | `data/knowledge_base/conflict_resolution/ESCALATION_SLA_TRACKER_202606.md` | 조율차장 | 2026-06-06 | 재판정 전 보완 큐 | QA_테스터 | Updated |
| Session Register | `data/knowledge_base/conflict_resolution/SESSION_REGISTER_202606.md` | 조율차장 | 2026-06-06 | AICOL-20260606-024 | 조율차장 | Updated |

## 6. 결론

006/007은 아직 승인 상태가 아니지만, Missing 항목을 증거 단위로 분해하면 2026-06-12에 `BREACHED` 없이 승인, 명시적 보류, 조건부 보완 중 하나로 재판정할 수 있다.
