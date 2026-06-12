# AI Collaboration Automated Audit - 2026-06

> 목적: AI 협업 세션 등록부, 케이스 파일, ESCALATED SLA 추적표가 수동 기억이 아니라 반복 실행 가능한 기준으로 유지되는지 점검한다.

## 1. 감사 범위

| 대상 | 파일 |
|---|---|
| 세션 등록부 | `data/knowledge_base/conflict_resolution/SESSION_REGISTER_202606.md` |
| SLA 추적표 | `data/knowledge_base/conflict_resolution/ESCALATION_SLA_TRACKER_202606.md` |
| 케이스 파일 | `data/knowledge_base/conflict_resolution/cases/` |
| 테스트 계획 | `data/knowledge_base/conflict_resolution/COLLABORATION_TEST_PLAN.md` |

## 2. 불변조건

| ID | 불변조건 | 실패 시 조치 |
|---|---|---|
| INV-01 | 세션 상태는 `CLOSED` 또는 `ESCALATED`만 사용한다. | 등록부 상태값을 SOP 표준값으로 수정한다. |
| INV-02 | 합의 상태는 `CONSENSUS_WITH_GUARDRAILS` 또는 `ESCALATE`로 제한한다. | 케이스 파일의 합의 근거를 확인하고 상태 매핑을 수정한다. |
| INV-03 | 리스크 게이트는 `NOT_NEEDED`, `LOCAL_ONLY`, `REDACTED_REVIEW`, `APPROVED`, `APPROVED_WITH_HOLD`, `BLOCKED` 중 하나만 사용한다. | Risk/Data/External AI Gate 또는 Customer/Commercial Release Gate에 세부 사유를 분리한다. |
| INV-04 | 결정 로그 상태는 `Explicitly Deferred` 또는 `Draft Created`로 기록한다. | 실제 운영 세션이면 Decision Log ID를 생성하고 테스트 세션이면 defer 사유를 남긴다. |
| INV-05 | Reuse Closure는 `Created`, `Updated`, `Explicitly Deferred`, `Missing` 중 하나만 사용한다. | 닫힌 세션은 KB/QA/교육/백로그 중 하나로 내재화하거나 defer 사유를 기록한다. |
| INV-06 | `ESCALATED` 세션은 합의 상태가 반드시 `ESCALATE`여야 한다. | 상태 매핑 또는 케이스 결론을 재검토한다. |
| INV-07 | `CLOSED` 세션은 합의 상태가 `ESCALATE`이면 안 된다. | 닫힘 근거가 없으면 ESCALATED로 되돌린다. |
| INV-08 | 등록부의 모든 케이스 파일 링크는 실제 파일로 존재해야 한다. | 누락 케이스 파일을 생성하거나 등록부 링크를 정정한다. |
| INV-09 | ESCALATED SLA 항목은 Owner, Due by, 리스크 상태, SLA 상태, 근거를 갖는다. | SLA Tracker를 보강하고 일일 인계에 포함한다. |
| INV-10 | CLOSED 세션의 Reuse Closure는 `Updated`여야 한다. | CLOSED 유지가 어렵다면 `ESCALATED` 또는 `CONDITIONAL` 케이스로 재분류한다. |
| INV-11 | 다음 검토일은 `YYYY-MM-DD` 형식이어야 한다. | 특정 날짜 고정보다 세션별 후속 기한을 명시하고, ESCALATED 기한은 SLA Tracker에서 별도 검증한다. |
| INV-12 | ESCALATED 원건의 Decision Log Draft 경로는 실제 파일로 존재해야 한다. | 케이스 Reuse Closure의 Decision Log 경로를 만들고 `decision_logs/` 아래 초안을 생성한다. |
| INV-13 | Decision Log Draft의 ID, 세션, 케이스, 합의 상태, 선택지, 초안 판정은 원건과 맞아야 한다. | Decision Log Draft의 핵심 필드를 원건 등록부/케이스 파일과 맞추고 A/B/C/D 선택지를 유지한다. |
| INV-14 | KST04 ESCALATED 원건은 source draft, Missing Matrix, SLA readiness 참조, P0 고객 확정 응답 금지선을 갖는다. | KST04 후속 산출물을 만들고 P0 기본 행동에 고객 확정 응답 금지를 명시한다. |
| INV-15 | Conflict Log 요약 숫자와 케이스 색인은 서로 일치하고, 등록부의 ESCALATED 원건을 포함해야 한다. | `CONFLICT_LOG.md` 요약/색인/Owner/Due by를 등록부 기준으로 갱신한다. |
| INV-16 | Conflict Log가 ESCALATED로 표시한 케이스는 등록부에서도 ESCALATED여야 한다. | Register를 닫을 때 Conflict Log 상태/요약/결정 근거를 같은 패스에서 갱신한다. |
| INV-17 | Conflict Log가 SETTLED/PRECEDENT로 닫힌 케이스는 Register도 CLOSED여야 하며, 닫힌 Register의 SLA 행은 CLOSED여야 한다. | 닫힘 전환 시 Register, Conflict Log, SLA Tracker를 같은 패스에서 갱신한다. |
| INV-18 | 닫힌 전환 대상의 Decision Log는 Draft/예정/후보/Missing 같은 초안 흔적을 남기면 안 된다. | 실제 선택안, 결정일, 결정 사유, 후속 조치로 Decision Log를 최종화한다. |

## 3. 2026-06-06 실행 명령

### 3.1 세션 등록부 상태 점검

```bash
awk -F'|' '/^\| AICOL-202606(05|06)-[0-9]+ \| 2026-06-(05|06)/{total++; id=$2; status=$8; consensus=$9; risk=$10; decision=$11; casefile=$12; reuse=$13; review=$14; gsub(/^ +| +$/, "", id); gsub(/^ +| +$/, "", status); gsub(/^ +| +$/, "", consensus); gsub(/^ +| +$/, "", risk); gsub(/^ +| +$/, "", decision); gsub(/^ +| +$/, "", casefile); gsub(/^ +| +$/, "", reuse); gsub(/^ +| +$/, "", review); if (status !~ /^(CLOSED|ESCALATED)$/) {print "INVALID STATUS " id " -> " status; bad=1}; if (consensus !~ /^(CONSENSUS_WITH_GUARDRAILS|ESCALATE)$/) {print "INVALID CONSENSUS " id " -> " consensus; bad=1}; if (risk !~ /^(NOT_NEEDED|LOCAL_ONLY|REDACTED_REVIEW|APPROVED|APPROVED_WITH_HOLD|BLOCKED)$/) {print "INVALID RISK " id " -> " risk; bad=1}; if (decision !~ /^(Explicitly Deferred|Draft Created)$/) {print "INVALID DECISION " id " -> " decision; bad=1}; if (reuse !~ /^(Created|Updated|Explicitly Deferred|Missing)$/) {print "INVALID REUSE " id " -> " reuse; bad=1}; if (review !~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/) {print "INVALID REVIEW " id " -> " review; bad=1}; if (status=="ESCALATED" && consensus!="ESCALATE") {print "ESCALATED WITHOUT ESCALATE " id; bad=1}; if (status=="CLOSED" && consensus=="ESCALATE") {print "CLOSED WITH ESCALATE " id; bad=1}; print "OK SESSION " id} END{print "TOTAL " total; exit bad}' data/knowledge_base/conflict_resolution/SESSION_REGISTER_202606.md
```

2026-06-06 결과: PASS, 총 14건.

### 3.2 케이스 파일 존재 점검

```bash
awk -F'|' '/^\| AICOL-202606(05|06)-[0-9]+ \| 2026-06-(05|06)/{casefile=$12; gsub(/^ +| +$/, "", casefile); gsub(/`/, "", casefile); path="data/knowledge_base/conflict_resolution/" casefile; if (system("test -f \"" path "\"") != 0) {print "MISSING CASE " path; bad=1} else {print "OK CASE " path}} END{exit bad}' data/knowledge_base/conflict_resolution/SESSION_REGISTER_202606.md
```

2026-06-06 결과: PASS, 등록부 14건 모두 케이스 파일 존재.

### 3.3 ESCALATED SLA 점검

```bash
awk -F'|' '/^\| `AITEST_20260605_00[67]` \| `AICOL-20260605-00[67]`/{caseid=$2; session=$3; owner=$4; due=$5; risk=$6; sla=$8; evidence=$9; gsub(/^[ `]+|[ `]+$/, "", caseid); gsub(/^[ `]+|[ `]+$/, "", session); gsub(/^ +| +$/, "", owner); gsub(/^ +| +$/, "", due); gsub(/^ +| +$/, "", risk); gsub(/^ +| +$/, "", sla); gsub(/^ +| +$/, "", evidence); if (owner=="" || due!="2026-06-12" || risk !~ /^(BLOCKED|APPROVED_WITH_HOLD)$/ || sla !~ /^(ON_TRACK|AT_RISK|BREACHED|CLOSED)$/ || evidence=="") {print "INVALID SLA " caseid; bad=1} else {print "OK SLA " caseid " -> " sla; total++}} END{print "TOTAL " total; exit bad}' data/knowledge_base/conflict_resolution/ESCALATION_SLA_TRACKER_202606.md
```

2026-06-06 결과: PASS, ESCALATED 2건 모두 `ON_TRACK`.

### 3.4 Reuse Closure 강도 점검

```bash
awk -F'|' '/^\| AICOL-202606(05|06)-[0-9]+ \| 2026-06-(05|06)/{total++; status=$8; reuse=$13; gsub(/^ +| +$/, "", status); gsub(/^ +| +$/, "", reuse); if (status=="CLOSED" && reuse!="Updated") {print "CLOSED REUSE NOT UPDATED " $2 " -> " reuse; bad=1}; if (status=="ESCALATED" && reuse !~ /^(Created|Updated)$/) {print "ESCALATED REUSE WEAK " $2 " -> " reuse; bad=1}} END{print "TOTAL " total; exit bad}' data/knowledge_base/conflict_resolution/SESSION_REGISTER_202606.md
```

2026-06-06 결과: PASS, 총 14건.

## 4. 발견한 자동화 위험

| 위험 | 관찰 | 보완 |
|---|---|---|
| Markdown 표 열 번호 오류 | 참여 AI 열에 여러 이름이 들어가도 `|` 기준 열 위치는 유지되지만, 점검식 작성자가 열 번호를 한 칸 밀리게 잡을 수 있음 | 등록부 열 번호를 문서화하고 점검식에 `id/status/consensus/risk` 변수를 명시 |
| 같은 케이스 ID 반복 검출 | SLA 추적표의 일일 인계 표에도 같은 케이스 ID가 반복됨 | SLA 본표는 `AITEST + AICOL` 조합으로만 매칭 |
| 검색식 과신 | 단순 `rg`는 참조 존재를 보여주지만 표준값/상태 매핑을 증명하지 못함 | 표 구조 기반 `awk` 점검을 병행 |

## 5. 결론

2026-06-06 기준 협업 프로세스는 수동 문서화 단계를 넘어 반복 가능한 감사 후보 기준을 갖췄다.
`AITEST_20260606_017`에서 운영 배치는 월간 협업 리허설과 내부성장 백로그 후보로 정했다.
다만 아직 완전한 자동화 스크립트는 아니므로, 다음 등록부 증가 후에도 오탐 없이 통과하면 pre-commit 또는 CI 후보로 재검토한다.

## 6. 운영 배치

| 배치 위치 | 상태 | 근거 | 다음 조건 |
|---|---|---|---|
| 월간 협업 리허설 | 채택 | SOP의 월간 6개 시나리오 리허설과 맞음 | 매월 등록부 증가 후 4개 점검식 실행 |
| 내부성장 백로그 | 채택 | 자동화 후보로 추적 필요 | 2026-06-30까지 스크립트화 여부 검토 |
| pre-commit | 보류 | 표 구조 변경 시 오탐 가능 | 다음 세션 추가 후 재검증 |
| CI | 보류 | 저장소 CI 운영 범위 미확정 | 전용 파서 또는 스크립트 작성 후 재검토 |

## 7. 스크립트 실행 후보

| 항목 | 값 |
|---|---|
| 스크립트 | `scripts/validate_ai_collaboration_audit.py` |
| 실행 명령 | `python3 scripts/validate_ai_collaboration_audit.py` |
| 1차 결과 | `PASS sessions=13 closed=11 escalated=2 sla_rows=2` |
| 018 등록 후 재검증 결과 | `PASS sessions=14 closed=12 escalated=2 sla_rows=2` |
| 019 등록 후 재검증 결과 | `PASS sessions=15 closed=13 escalated=2 sla_rows=2` |
| 020 등록 후 재검증 결과 | `PASS sessions=16 closed=14 escalated=2 sla_rows=2` |
| 021 등록 후 재검증 결과 | `PASS sessions=17 closed=15 escalated=2 sla_rows=2` |
| 022 등록 후 재검증 결과 | `PASS sessions=18 closed=16 escalated=2 sla_rows=2` |
| 023 등록 후 재검증 결과 | `PASS sessions=19 closed=17 escalated=2 sla_rows=2` |
| 024 등록 후 재검증 결과 | `PASS sessions=20 closed=18 escalated=2 sla_rows=2` |
| 025 등록 후 재검증 결과 | `PASS sessions=21 closed=19 escalated=2 sla_rows=2` |
| 026 등록 후 재검증 결과 | `PASS sessions=22 closed=20 escalated=2 sla_rows=2` |
| 027 등록 후 재검증 결과 | `PASS sessions=23 closed=21 escalated=2 sla_rows=2` |
| 028 등록 후 재검증 결과 | `PASS sessions=24 closed=22 escalated=2 sla_rows=2` |
| 029 등록 후 재검증 결과 | `PASS sessions=25 closed=23 escalated=2 sla_rows=2` |
| 030 신규 ESCALATED 등록 후 재검증 결과 | `PASS sessions=26 closed=23 escalated=3 sla_rows=3` |
| 031 KST04 후속 큐 등록 후 재검증 결과 | `PASS sessions=27 closed=24 escalated=3 sla_rows=3` |
| 032 KST04 후속 큐 자동 감사 확장 후 재검증 결과 | `PASS sessions=28 closed=25 escalated=3 sla_rows=3` |
| 033 Conflict Log 정합성 자동 감사 확장 후 재검증 결과 | `PASS sessions=29 closed=26 escalated=3 sla_rows=3 conflicts=5` |
| 034 ESCALATED 상태 전환 드리프트 자동 감사 후 재검증 결과 | `PASS sessions=30 closed=27 escalated=3 sla_rows=3 conflicts=5` |
| 035 ESCALATED 닫힘 전환 원자성 자동 감사 후 재검증 결과 | `PASS sessions=31 closed=28 escalated=3 sla_rows=3 conflicts=5` |
| 036 Decision Log 최종화 자동 감사 후 재검증 결과 | `PASS sessions=32 closed=29 escalated=3 sla_rows=3 conflicts=5` |

스크립트화 과정에서 다음 액션 표의 `AICOL-...` 문구를 세션 행으로 오인한 문제와 SLA 본표 열 수를 잘못 잡은 문제가 발견되어 수정했다.
018번 등록 후 14건 기준으로 재실행했을 때도 통과했다.

## 8. 네거티브 컨트롤

| 테스트 | 주입 결함 | 기대 | 결과 |
|---|---|---|---|
| AITEST_20260606_019 | `AICOL-20260606-018` 리스크 상태 `LOCAL_ONLY`를 임시 파일에서 `LOCAL-ISH`로 변경 | FAIL | `FAIL AICOL-20260606-018: invalid risk LOCAL-ISH` |
| AITEST_20260606_020-A | 케이스 파일 링크를 존재하지 않는 `AITEST_20260606_999.md`로 변경 | FAIL | `FAIL AICOL-20260606-019: missing case file ...` |
| AITEST_20260606_020-B | CLOSED 세션 Reuse Closure를 `Missing`으로 변경 | FAIL | `FAIL AICOL-20260606-019: CLOSED session reuse closure must be Updated` |
| AITEST_20260606_020-C | `AICOL-20260605-006` SLA 본표 행 삭제 | FAIL | `FAIL AICOL-20260605-006: missing SLA tracker row` |
| AITEST_20260606_026 | ESCALATED 원건 Decision Log 경로를 `TBD`로 변경 | FAIL | `FAIL AICOL-20260605-006: missing decision log draft path in case Reuse Closure ...` |
| AITEST_20260606_027 | Decision Log `Decision ID`와 파일명 불일치 | FAIL | `FAIL AICOL-20260605-006: decision log ID ... != file stem ...` |
| AITEST_20260606_032-A | KST04 P0 기본 행동에서 고객 확정 응답 금지선 누락 | FAIL | `FAIL AICOL-20260606-030: KST04 P0 row default action does not preserve customer-confirmed-response hold` |
| AITEST_20260606_032-B | `/private/tmp` SLA 복사본에서 KST04 Matrix 참조 제거 | FAIL | `FAIL AICOL-20260606-030: SLA tracker does not reference KST04 follow-up artifacts` |
| AITEST_20260606_033-A | `/private/tmp` Conflict Log 복사본에서 ESCALATED 요약을 2로 변경 | FAIL | `FAIL CONFLICT_LOG: summary ESCALATED=2 but index has 3` |
| AITEST_20260606_033-B | `/private/tmp` Conflict Log 복사본에서 030 색인 제거 | FAIL | `FAIL AICOL-20260606-030: ESCALATED case AITEST_20260606_030 missing from CONFLICT_LOG index` |
| AITEST_20260606_034 | `/private/tmp` 등록부 복사본에서 030만 CLOSED로 변경 | FAIL | `FAIL AICOL-20260606-030: CONFLICT_LOG still ESCALATED but register status is CLOSED` |
| AITEST_20260606_035-A | `/private/tmp`에서 030 Register/Conflict는 닫고 SLA만 ON_TRACK 유지 | FAIL | `FAIL AICOL-20260606-030: register is CLOSED but SLA status is ON_TRACK` |
| AITEST_20260606_035-B | `/private/tmp` Conflict Log만 030 SETTLED로 변경 | FAIL | `FAIL AICOL-20260606-030: CONFLICT_LOG is SETTLED but register status is ESCALATED` |
| AITEST_20260606_036 | `/private/tmp`에서 030 Register/Conflict/SLA는 닫고 Decision Log만 Draft 유지 | FAIL | `FAIL AICOL-20260606-030: closed case decision log still contains draft or missing-evidence markers` |

원본 등록부는 수정하지 않고 `/private/tmp` 복사본만 사용했다.

## 9. 실패 메시지 가독성

`AITEST_20260606_021`에서 실패 메시지에 `fix:` 힌트를 추가했다.

| 결함 | 개선된 출력 예 |
|---|---|
| 케이스 파일 누락 | `FAIL AICOL-20260606-019: missing case file ... | fix: create the case file under conflict_resolution/cases or fix the register link` |
| CLOSED Reuse Closure 약화 | `FAIL AICOL-20260606-019: CLOSED session reuse closure must be Updated | fix: update KB/QA/backlog evidence or reopen the session before marking it CLOSED` |
| ESCALATED SLA 누락 | `FAIL AICOL-20260605-006: missing SLA tracker row | fix: add this ESCALATED session to ESCALATION_SLA_TRACKER_202606.md` |
| ESCALATED Decision Log Draft 누락 | `FAIL AICOL-20260605-006: missing decision log draft path in case Reuse Closure | fix: replace the Decision Log TBD with a real draft path under conflict_resolution/decision_logs` |
| Decision Log Draft ID 불일치 | `FAIL AICOL-20260605-006: decision log ID ... != file stem ... | fix: make the Decision ID field match the decision log filename` |
| KST04 후속 산출물 SLA 참조 누락 | `FAIL AICOL-20260606-030: SLA tracker does not reference KST04 follow-up artifacts | fix: add the KST04 source draft and missing evidence matrix to the SLA tracker readiness section` |
| Conflict Log 요약 불일치 | `FAIL CONFLICT_LOG: summary ESCALATED=2 but index has 3 | fix: update the CONFLICT_LOG status summary to match the case index` |
| ESCALATED 상태 전환 드리프트 | `FAIL AICOL-20260606-030: CONFLICT_LOG still ESCALATED but register status is CLOSED | fix: when closing a register session, update CONFLICT_LOG status/summary and supporting decision evidence in the same pass` |
| ESCALATED 닫힘 SLA stale | `FAIL AICOL-20260606-030: register is CLOSED but SLA status is ON_TRACK | fix: when closing an escalated register row, set the matching SLA row to CLOSED or remove/reclassify the stale SLA tracking row` |
| Decision Log 최종화 누락 | `FAIL AICOL-20260606-030: closed case decision log still contains draft or missing-evidence markers | fix: replace Draft/예정/후보/Missing language with the actual final choice, date, reason, and follow-up actions before closing` |

## 10. 강제 적용 후보

| 항목 | 값 |
|---|---|
| 래퍼 | `scripts/precommit_ai_collaboration_audit.sh` |
| 정상 리허설 | `PASS sessions=32 closed=29 escalated=3 sla_rows=3 conflicts=5`, exit 0 |
| 실패 리허설 | missing case file + `fix:` 힌트, exit 1 |
| 실제 hook 설치 | 보류 |

현재는 실제 `.git/hooks/pre-commit`을 설치하지 않고, hook/CI에서 호출 가능한 독립 래퍼만 둔다.
