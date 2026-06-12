# AI 협업 프로세스 테스트 계획

> 기준일: 2026-06-05
> 적용 문서: `docs/internal_organization_documents/30_AI_TO_AI_COLLABORATION_SOP.md`
> 목적: AI 간 의사소통, 추론, 반론, 합의, 실행 인계 프로세스가 다양한 상황에서 작동하는지 검증한다.

## 1. 테스트 운영 방식

| 항목 | 기준 |
|---|---|
| 주기 | 월 1회 정기 리허설, 주요 조직 변경 시 수시 리허설 |
| 주관 | 조율차장 |
| 기록 위치 | `knowledge/10_agents/conflict_resolution/CONFLICT_LOG.md` 또는 별도 케이스 파일 |
| 통과 기준 | 6개 평가 항목 중 5개 이상 PASS |
| 실패 처리 | 실패 항목을 SOP, KB, 체크리스트, 자동화 후보 중 하나로 개선 등록 |
| 실행 템플릿 | `docs/internal_organization_documents/31_AI_COLLABORATION_RUNBOOK_TEMPLATES.md` |

## 2. 공통 평가표

| 평가 항목 | PASS 기준 | 결과 |
|---|---|---|
| 역할 라우팅 | 주관 AI와 검토 AI가 올바르게 배정됨 | TBD |
| 근거 품질 | 판단마다 KST 등급, 출처, 적용 조건이 있음 | TBD |
| 반론 품질 | 실행 리스크와 예외 조건이 최소 1개 이상 제기됨 | TBD |
| 합의 도출 | 4개 합의 상태 중 하나로 종료됨 | TBD |
| 실행 인계 | 담당, 기한, 검증 방법이 명시됨 | TBD |
| 지식화 | 결과 저장 위치가 정해짐 | TBD |

## 3. 테스트 시나리오

### S01 기술 구현 협업

- 상황: Revit Add-in 신규 기능 요구가 들어왔고 구현 범위가 불명확하다.
- 주관: 요구사항분석
- 참여: 프로그램개발, Revit_Addin, QA_테스터, 빌드검증, 제품패키징
- 반론: 라이선스_보안관
- 기대 결과: 구현 범위, 제외 범위, 테스트 항목, 배포 리스크가 결정된다.
- 합의 상태 목표: CONSENSUS_WITH_GUARDRAILS

### S02 고객 응대 협업

- 상황: 고객이 납품 지연과 추가 기능을 동시에 문의했다.
- 주관: 고객지원CS
- 참여: 조율차장, 프로젝트분석, 법무조항검토
- 반론: CFO, COO
- 기대 결과: 고객 발송 문구, 내부 액션, 변경 요청 필요 여부가 분리된다.
- 합의 상태 목표: CONSENSUS_WITH_GUARDRAILS

### S03 견적/계약 협업

- 상황: 고객이 기존 계약 범위를 넘어서는 추가 BIM 모델링을 요구한다.
- 주관: 견적심사원
- 참여: BIM_프로젝트_견적산정, 법무조항검토, CFO
- 반론: 고객지원CS
- 기대 결과: 무상 대응 가능 범위, 유상 변경 견적, 고객 설명 문구가 확정된다.
- 합의 상태 목표: SPLIT_DECISION 또는 CONSENSUS_WITH_GUARDRAILS

### S04 보안/개인정보 협업

- 상황: AI 학습을 위해 고객 프로젝트 모델과 로그를 외부 API로 전송할 수 있는지 검토한다.
- 주관: 라이선스_보안관
- 참여: 법무조항검토, 프로그램개발, 인프라_DevOpsObsidian
- 반론: 성장전략그룹
- 기대 결과: 전송 가능 데이터, 금지 데이터, 익명화 조건, 승인 절차가 확정된다.
- 합의 상태 목표: ESCALATE 또는 CONSENSUS_WITH_GUARDRAILS

### S05 전략/제품화 협업

- 상황: 내부 자동화 도구를 Autodesk App Store 제품으로 전환할지 판단한다.
- 주관: 전략기획
- 참여: CSO, 제품패키징, 스토어심사, 프로그램개발, QA_테스터
- 반론: CFO, 라이선스_보안관
- 기대 결과: 제품화 우선순위, MVP 범위, 심사 리스크, 다음 실험이 정해진다.
- 합의 상태 목표: CONSENSUS_WITH_GUARDRAILS

### S06 AI 판단 충돌 협업

- 상황: 두 AI가 동일 기준에 대해 서로 다른 판단을 낸다.
- 주관: 조율차장
- 참여: 충돌 당사자 AI, 지식큐레이터, 지식업데이트
- 반론: KST 신뢰도 검토자
- 기대 결과: KST 비교, 역할 경계 확인, 최종 판단, 선례 등록 여부가 기록된다.
- 합의 상태 목표: SETTLED 또는 PRECEDENT

## 4. 2026-06-05 드라이런 결과

| 시나리오 | 결과 | 관찰 |
|---|---|---|
| S01 | PASS | 기술 구현은 요구사항분석 주관, 프로그램개발/QA/빌드검증 검토 구조가 적합하다. |
| S02 | PASS | 고객 발송 문구는 고객지원CS가 소유하고 법무/조율차장이 조건을 붙이는 구조가 안정적이다. |
| S03 | PASS | 견적 판단과 고객 관계 판단을 분리해야 하며, 최종 가격은 CFO 검토가 필요하다. |
| S04 | CONDITIONAL | 보안 사안은 AI 단독 확정보다 보안관 주관 후 CEO/법무 에스컬레이션 조건이 필요하다. |
| S05 | PASS | 제품화는 전략기획 주관, CSO 승인, 스토어심사/제품패키징 검토 구조가 적합하다. |
| S06 | PASS | 기존 `conflict_resolution` 체계와 연결하면 충돌 로그가 선례화될 수 있다. |

상세 기록: `cases/AITEST_20260605_001.md`

## 4.1 2026-06-05 추가 방향성 테스트

| ID | 방향 | 결과 | 핵심 검증 |
|---|---|---|---|
| AITEST_20260605_002 | 고객 납품 지연 + 추가 요구 | CONDITIONAL PASS | 고객 발송, 법무 조건, 비용 반론, PM 복구 계획 분리 |
| AITEST_20260605_003 | 고객 모델 로그 외부 AI 전송 | PASS | 외부 API 금지 조건과 익명화 요약본 제한 허용 게이트 작동 |
| AITEST_20260605_004 | 견적 판단 충돌 | PRECEDENT | KST02 견적/CFO 판단과 KST05 고객관계 가설의 우선순위 정리 후 선례 승격 |
| AITEST_20260605_005 | 자동수집 지식 고객 응답 승격 | CONDITIONAL PASS | KST04 확정 사용 금지, 공식 출처 확인 후 승격 절차 작동 |
| AITEST_20260605_006 | 개인정보/외부 AI 정책 문서 충돌 | ESCALATED | privacy/legal/AI routing 표현 충돌을 발견하고 Local-only 임시 적용 |
| AITEST_20260605_007 | 상업/가격 source of truth 충돌 | ESCALATED | Starter-only launch와 Project Mentor 가격 약관의 공개 가능 상태 충돌 발견 |
| AITEST_20260605_008 | PRECEDENT 승격 및 재사용 | PASS | AITEST_20260605_004 선례를 유사한 무상/유상 범위 충돌에 재적용하고 KB/QA 내재화 완료 |
| AITEST_20260605_009 | 리스크 게이트 상태값 표준화 | PASS | SOP/런북/세션 등록부의 리스크 상태값을 6개 표준값으로 정리 |
| AITEST_20260605_010 | ESCALATED 후속 SLA 사전 추적 | PASS | 006/007을 닫지 않고 ON_TRACK/AT_RISK/BREACHED/CLOSED 판정 체계로 추적 |
| AITEST_20260605_011 | 신규 AI 역할 온보딩 및 내재화 | CONDITIONAL PASS | 15분 온보딩 카드와 역량 매트릭스 연결, 012에서 샘플 2회 적용 통과 |
| AITEST_20260605_012 | 신규 AI 온보딩 카드 2회 반복 적용 | PASS | 역량 매트릭스에 2회 적용 기록과 개선 과제 누적 |
| AITEST_20260605_013 | ESCALATED source of truth 초안 생성 | CONDITIONAL PASS | 006/007 후속 판단용 초안 2개 생성, 최종 승인 전 |
| AITEST_20260606_014 | 날짜 롤오버 및 일일 인계 검증 | PASS | 2026-06-06에도 006/007 ON_TRACK 유지, 일일 인계 생성 |
| AITEST_20260606_015 | 2026-06-12 에스컬레이션 재판정 분기 리허설 | PASS | 승인/명시적 보류/조건부 보완/위반 분기 처리 기준 생성 |
| AITEST_20260606_016 | 협업 등록부 자동 감사 후보 | PASS | 표준값, 케이스 파일 존재, ESCALATED SLA, Reuse Closure 점검식 통과 |
| AITEST_20260606_017 | 자동 감사 운영 배치 의사결정 | PASS | 월간 리허설/내부성장 백로그 채택, pre-commit/CI 보류 |
| AITEST_20260606_018 | 자동 감사 스크립트화 검증 | PASS | Python 스크립트 생성, 세션 ID/SLA 열 수 오탐 수정, 14건 기준 통과 |
| AITEST_20260606_019 | 자동 감사 네거티브 컨트롤 | PASS | 임시 깨진 등록부의 비표준 리스크 상태값을 실패로 감지 |
| AITEST_20260606_020 | 자동 감사 네거티브 컨트롤 확장 | PASS | 케이스 파일 누락, CLOSED Reuse Closure 약화, ESCALATED SLA 누락 감지 |
| AITEST_20260606_021 | 자동 감사 실패 메시지 가독성 | PASS | 실패 메시지에 `fix:` 힌트를 추가해 수정 경로 안내 |
| AITEST_20260606_022 | 자동 감사 강제 적용 리허설 | PASS | pre-commit/CI 후보 래퍼 생성, 정상 exit 0/실패 exit 1 확인 |
| AITEST_20260606_023 | ESCALATED 재판정 준비성 감사 | CONDITIONAL PASS | 006/007은 ON_TRACK 유지, Missing 항목 때문에 승인보다 보류/보완 분기 가능 |
| AITEST_20260606_024 | ESCALATED Missing 증거 보완 리허설 | CONDITIONAL PASS | Missing Evidence Matrix로 006/007의 Owner, 검증자, 금지 행동, 목표 상태 분해 |
| AITEST_20260606_025 | ESCALATED 결정 로그 패키지 리허설 | CONDITIONAL PASS | 006/007 Decision Log Draft 생성, 원건 Reuse Closure의 TBD를 실제 경로로 전환 |
| AITEST_20260606_026 | ESCALATED Decision Log 자동 감사 확장 | PASS | 감사 스크립트가 Decision Log Draft 경로/파일 존재를 검증하고 TBD 퇴행을 실패로 감지 |
| AITEST_20260606_027 | Decision Log Draft 필드 정합성 자동 감사 | PASS | Decision ID/세션/케이스/합의 상태/선택지/초안 판정을 자동 검증 |
| AITEST_20260606_028 | ESCALATED 재판정 결과 적용 리허설 | PASS | 승인/보류/조건부 보완/위반 결과별 Decision Log, SLA, Register, KB/QA 갱신 순서 고정 |
| AITEST_20260606_029 | 재판정 4분기 상태 전환 시뮬레이션 | PASS | 승인/CLOSED, 보류/ESCALATED, 보완/AT_RISK, 위반/BREACHED별 자동 감사 기대 상태 고정 |
| AITEST_20260606_030 | KST04 고객 응답 승격 충돌 | ESCALATED | 신규 ESCALATED 원건에서도 SLA, Decision Log Draft, 자동 감사 반복 적용 통과 |
| AITEST_20260606_031 | KST04 승격 source of truth 및 Missing 증거 큐 | PASS | 030 재판정용 고객 응답 금지선, 승격 조건, P0/P1 증거 큐 생성 |
| AITEST_20260606_032 | KST04 후속 큐 자동 감사 확장 | PASS | source draft/Matrix/SLA readiness/P0 금지선 누락을 자동 감사로 감지 |
| AITEST_20260606_033 | Conflict Log 요약/색인 정합성 자동 감사 | PASS | 요약 숫자, 색인, 등록부 ESCALATED 원건 누락을 자동 감사로 감지 |
| AITEST_20260606_034 | ESCALATED 상태 전환 드리프트 자동 감사 | PASS | Register만 CLOSED가 되고 Conflict Log가 ESCALATED로 남는 부분 전환을 실패로 감지 |
| AITEST_20260606_035 | ESCALATED 닫힘 전환 원자성 자동 감사 | PASS | Register/Conflict Log/SLA 중 하나만 닫히는 부분 전환을 실패로 감지 |
| AITEST_20260606_036 | Decision Log 최종화 자동 감사 | PASS | 닫힌 원건 Decision Log에 Draft/예정/후보/Missing 문구가 남으면 실패로 감지 |

## 4.2 에이전트 감사 반영 현황

| 감사 관점 | 발견 사항 | 조치 |
|---|---|---|
| 운영성 | 세션 등록부, SLA, 상태 매핑 부족 | 런북에 세션 등록부 추가, CONFLICT_LOG에 Opened/Due/Owner 필드 추가 |
| 지식 내재화 | Reuse Closure 증거가 약함 | 런북과 AI 협업 KB에 Reuse Closure 기준 추가 |
| 보안/상업 리스크 | 외부 AI, 고객 문구, 가격 승인 필드 부족 | SOP/런북에 Risk/Data/External AI Gate 및 Customer/Commercial Release Gate 추가 |

라운드 요약: `TEST_ROUND_20260605_001_SUMMARY.md`

세션 등록부 샘플: `SESSION_REGISTER_202606.md`

## 4.4 2026-06-06 연속성 테스트

| ID | 방향 | 결과 | 핵심 검증 |
|---|---|---|---|
| AITEST_20260606_014 | 날짜 롤오버 및 일일 인계 | PASS | 전일 ESCALATED, source of truth 초안, Open 액션이 날짜 변경 후에도 유지됨 |
| AITEST_20260606_015 | 에스컬레이션 재판정 분기 | PASS | 2026-06-12 승인/보류/보완/위반 처리 경로 사전 정의 |
| AITEST_20260606_016 | 협업 등록부 자동 감사 후보 | PASS | 등록부 12건, 케이스 파일, SLA 2건, Reuse Closure 반복 점검 기준 생성 |
| AITEST_20260606_017 | 자동 감사 운영 배치 | PASS | 강제 훅 전 단계로 월간 리허설과 내부성장 백로그 후보에 배치 |
| AITEST_20260606_018 | 자동 감사 스크립트화 | PASS | `scripts/validate_ai_collaboration_audit.py` 생성 및 14건 기준 통과 |
| AITEST_20260606_019 | 자동 감사 실패 감지 | PASS | `/private/tmp` 깨진 등록부에서 `LOCAL-ISH`를 invalid risk로 감지 |
| AITEST_20260606_020 | 자동 감사 결함 유형 확장 | PASS | 케이스 파일 누락, Reuse Closure 오류, SLA 누락을 각각 실패로 감지 |
| AITEST_20260606_021 | 자동 감사 가독성 | PASS | 실패 메시지가 문제와 수정 경로를 함께 표시 |
| AITEST_20260606_022 | 자동 감사 강제 적용 리허설 | PASS | 실제 hook 설치 없이 래퍼 기반 차단 흐름 확인 |
| AITEST_20260606_023 | ESCALATED 재판정 준비성 감사 | CONDITIONAL PASS | ON_TRACK과 승인 준비성을 분리해 006/007의 Missing 항목 보완 필요 확인 |
| AITEST_20260606_024 | ESCALATED Missing 증거 보완 리허설 | CONDITIONAL PASS | 승인 전 Missing 항목을 증거 단위 보완 큐로 전환 |
| AITEST_20260606_025 | ESCALATED 결정 로그 패키지 리허설 | CONDITIONAL PASS | 재판정일 선택지/보류 조건/후속 조치를 Decision Log Draft에 사전 배치 |
| AITEST_20260606_026 | ESCALATED Decision Log 자동 감사 확장 | PASS | 원건 Decision Log Draft 누락을 자동 감사 불변조건으로 추가 |
| AITEST_20260606_027 | Decision Log Draft 필드 정합성 자동 감사 | PASS | Decision Log Draft 내부 필드가 원건과 맞는지 검증 |
| AITEST_20260606_028 | ESCALATED 재판정 결과 적용 리허설 | PASS | 2026-06-12 결과 적용 순서와 분기별 상태값을 사전 검증 |
| AITEST_20260606_029 | 재판정 4분기 상태 전환 시뮬레이션 | PASS | 분기별 Register/SLA/Decision Log/자동 감사 불변조건을 비교 |
| AITEST_20260606_030 | 신규 ESCALATED 반복 적용 | ESCALATED | KST04 지식 승격 충돌을 3번째 ESCALATED 원건으로 등록 |
| AITEST_20260606_031 | 신규 ESCALATED 후속 큐 내재화 | PASS | 030을 닫기 위한 source of truth 초안과 Missing 증거 Matrix를 생성 |
| AITEST_20260606_032 | KST04 후속 큐 자동 감사 | PASS | KST04 후속 산출물 누락과 P0 금지선 약화를 실패로 감지 |
| AITEST_20260606_033 | Conflict Log 정합성 자동 감사 | PASS | 사람이 보는 Conflict Log 요약/색인이 등록부와 어긋나면 실패로 감지 |
| AITEST_20260606_034 | ESCALATED 상태 전환 드리프트 | PASS | Conflict Log ESCALATED 상태가 Register CLOSED와 충돌하면 실패로 감지 |
| AITEST_20260606_035 | ESCALATED 닫힘 원자성 | PASS | Conflict SETTLED/PRECEDENT, Register CLOSED, SLA CLOSED 상태 조합을 자동 감사로 검증 |
| AITEST_20260606_036 | Decision Log 최종화 | PASS | 닫힘 전환에서 Decision Log 초안 흔적을 자동 감사로 검증 |

상세 기록: `DAILY_HANDOFF_20260606.md`

## 4.3 다음 검증 초점

| 우선순위 | 검증 초점 | 판단 기준 |
|---|---|---|
| P1 | ESCALATED 후속 SLA | `AITEST_20260605_006`, `AITEST_20260605_007`이 2026-06-12까지 결정 로그, 정책/가격 source of truth, Reuse Closure 중 하나로 닫히는지 확인 |
| P1 | ESCALATED Missing 항목 보완 | 006은 제공자 약관/보관삭제/학습사용/국외이전/고객동의/승인, 007은 CEO/CFO 승인/약관환불/리소스 증거를 보완했는지 확인 |
| P1 | Missing Evidence Matrix 실행성 | `ESCALATED_MISSING_EVIDENCE_MATRIX_20260606.md`의 P0/P1 큐가 실제 결정 로그 또는 명시적 보류 로그로 전환되는지 확인 |
| P1 | Decision Log Draft 재판정 전환 | `DEC-AICOL-20260605-006-DRAFT.md`, `DEC-AICOL-20260605-007-DRAFT.md`가 2026-06-12에 승인/보류/보완 결과로 갱신되는지 확인 |
| P1 | Decision Log 자동 감사 반복성 | ESCALATED 원건이 추가될 때 Decision Log Draft 존재 검사가 오탐 없이 작동하는지 확인 |
| P1 | Decision Log 필드 정합성 반복성 | 새 Decision Log Draft가 추가될 때 ID/세션/케이스/합의 상태 불일치를 잡는지 확인 |
| P1 | 재판정 결과 적용 실행성 | 2026-06-12 실제 결과가 `ESCALATED_REDECISION_EXECUTION_PLAYBOOK_20260606.md` 순서대로 반영되는지 확인 |
| P1 | 재판정 분기 상태 조합 실행성 | 실제 결과 분기가 `REDECISION_BRANCH_SIMULATION_20260606.md`의 기대 상태와 일치하는지 확인 |
| P1 | 신규 ESCALATED 반복 적용성 | `AICOL-20260606-030`이 2026-06-13까지 SLA/Decision Log/KB/QA 경로로 관리되는지 확인 |
| P1 | KST04 Missing 증거 큐 실행성 | `KST04_PROMOTION_MISSING_EVIDENCE_MATRIX_20260606.md`의 P0 항목이 2026-06-13까지 실제 증거 또는 명시적 보류 로그로 전환되는지 확인 |
| P1 | KST04 후속 큐 자동 감사 지속성 | KST04 source draft, Matrix, SLA readiness, P0 고객 확정 응답 금지선이 다음 갱신 후에도 유지되는지 확인 |
| P1 | Conflict Log 정합성 지속성 | 신규 ESCALATED 또는 CLOSED 전환이 생길 때 Conflict Log 요약/색인/등록부 상태가 함께 갱신되는지 확인 |
| P1 | ESCALATED 상태 전환 양방향 정합성 | Register, Conflict Log, SLA, Decision Log가 닫힘/보류/위반 분기에서 서로 다른 상태로 남지 않는지 확인 |
| P1 | ESCALATED 닫힘 원자성 | 닫힘 분기에서 Register CLOSED, Conflict SETTLED/PRECEDENT, SLA CLOSED가 같은 패스에서 반영되는지 확인 |
| P1 | Decision Log 최종화 | 닫힘 분기에서 Decision Log가 실제 선택안/결정일/사유/후속 조치로 바뀌는지 확인 |
| P1 | 리스크 게이트 상태값 적용성 검증 | 표준 상태값 6개가 다음 실제 세션에서도 자유 문구 없이 유지되는지 확인 |
| P2 | PRECEDENT 반복 사용 | `AITEST_20260605_004/008` 선례가 새 고객 응대와 견적 판단에서 다시 사용되고 CS/견적 문구가 흔들리지 않는지 확인 |
| P2 | 에스컬레이션 SLA 재판정 | `ESCALATION_SLA_TRACKER_202606.md`의 ON_TRACK 항목이 2026-06-12에 CLOSED/Explicitly Deferred/AT_RISK/BREACHED 중 하나로 갱신되는지 확인 |
| P2 | 신규 AI 역할 온보딩 월간 누적 | 온보딩 카드가 실제 운영 세션에서 월 2회 이상 Pass/Conditional/Fail과 개선 과제를 남기는지 확인 |
| P2 | source of truth 초안 승인성 검증 | 006/007 초안이 CEO/CFO/법무/보안 승인 또는 명시적 보류로 전환되는지 확인 |
| P2 | 일일 인계 반복성 검증 | 2026-06-07 이후에도 Open/Due/Done 상태가 유지되는지 확인 |
| P2 | 재판정 분기 실행 검증 | 2026-06-12 실제 결과가 분기 매트릭스대로 등록부/SLA/KB에 반영되는지 확인 |
| P2 | 자동 감사 월간 실행 검증 | `AUTOMATED_COLLABORATION_AUDIT_202606.md` 점검식이 다음 등록부 증가 후에도 오탐 없이 통과하는지 확인 |
| P2 | 자동 감사 스크립트 반복 실행 검증 | `scripts/validate_ai_collaboration_audit.py`가 다음 실제 세션 증가 후에도 통과하는지 확인 |
| P2 | 자동 감사 실제 hook 후보 검토 | 독립 래퍼를 실제 pre-commit 또는 CI 중 어디에 둘지 판단 |

## 5. 개선 액션

| 액션 | 담당 | 기한 | 저장 위치 |
|---|---|---|---|
| AI 협업 SOP를 내부 조직 문서 인덱스에 추가 | 조율차장 | 2026-06-05 | `00_INTERNAL_ORG_DOCUMENT_INDEX.md` |
| AI 협업운영체계 KB 생성 | 지식큐레이터 | 2026-06-05 | `knowledge/10_agents/90_확장에이전트/AI_협업운영체계.md` |
| 충돌 해소 README에 협업 테스트 계획 링크 추가 | 조율차장 | 2026-06-05 | `conflict_resolution/README.md` |
| 월간 리허설 결과를 CONFLICT_LOG 또는 케이스 파일에 누적 | 조율차장 | 매월 | `conflict_resolution/` |
| ESCALATED 후속 SLA를 다음 라운드의 최우선 검증으로 지정 | 조율차장 | 2026-06-12 | `AITEST_20260605_006`, `AITEST_20260605_007` |
| PRECEDENT 선례의 KB/QA 반영 여부를 CLOSED 세션 필수 게이트로 적용 | 지식큐레이터 | 2026-06-12 | `SESSION_REGISTER_202606.md` |
| ESCALATION SLA Tracker 생성 및 2026-06-12 재판정 예약 | 조율차장 | 2026-06-05 | `ESCALATION_SLA_TRACKER_202606.md` |
| 신규 AI 협업 온보딩 카드 생성 및 역량 매트릭스 연결 | 교육컨설팅 | 2026-06-05 | `2026-06-05_AI_COLLABORATION_ONBOARDING_CARD_SAMPLE.md` |
| 신규 AI 협업 온보딩 카드 샘플 2회 적용 기록 | 교육컨설팅 | 2026-06-05 | `19_TRAINING_RECORD_COMPETENCY_MATRIX.md` |
| 006/007 source of truth 초안 생성 | 조율차장 | 2026-06-05 | `EXTERNAL_AI_DISCLOSURE_RULE_DRAFT_20260605.md`, `PRODUCT_LAUNCH_STATUS_SOURCE_OF_TRUTH_DRAFT_20260605.md` |
| 2026-06-06 일일 인계 감사 생성 | 조율차장 | 2026-06-06 | `DAILY_HANDOFF_20260606.md` |
| 2026-06-12 재판정 분기 매트릭스 생성 | 조율차장 | 2026-06-06 | `AITEST_20260606_015.md` |
| 협업 등록부 자동 감사 후보 생성 | 조율차장 | 2026-06-06 | `AUTOMATED_COLLABORATION_AUDIT_202606.md` |
| 협업 등록부 자동 감사 운영 배치 결정 | 조율차장 | 2026-06-06 | `AITEST_20260606_017.md`, `AX_INTERNAL_GROWTH_BACKLOG.md` |
| 협업 등록부 자동 감사 스크립트 생성 | 내부성장루프 | 2026-06-06 | `scripts/validate_ai_collaboration_audit.py` |
| 협업 등록부 자동 감사 네거티브 컨트롤 실행 | QA_테스터 | 2026-06-06 | `AITEST_20260606_019.md` |
| 협업 등록부 자동 감사 네거티브 컨트롤 확장 | QA_테스터 | 2026-06-06 | `AITEST_20260606_020.md` |
| 협업 등록부 자동 감사 실패 메시지 가독성 개선 | QA_테스터 | 2026-06-06 | `AITEST_20260606_021.md` |
| 협업 등록부 자동 감사 강제 적용 래퍼 생성 | 내부성장루프 | 2026-06-06 | `scripts/precommit_ai_collaboration_audit.sh` |
| 006/007 재판정 준비성 Missing 항목 보완 | 법무조항검토, 라이선스_보안관, CFO | 2026-06-12 | `AITEST_20260606_023.md` |
| 006/007 Missing Evidence Matrix 생성 | 조율차장 | 2026-06-06 | `ESCALATED_MISSING_EVIDENCE_MATRIX_20260606.md` |
| 006/007 Decision Log Draft 생성 | 조율차장 | 2026-06-06 | `decision_logs/DEC-AICOL-20260605-006-DRAFT.md`, `decision_logs/DEC-AICOL-20260605-007-DRAFT.md` |
| ESCALATED Decision Log Draft 자동 감사 추가 | QA_테스터 | 2026-06-06 | `scripts/validate_ai_collaboration_audit.py` |
| Decision Log Draft 필드 정합성 자동 감사 추가 | QA_테스터 | 2026-06-06 | `scripts/validate_ai_collaboration_audit.py` |
| 2026-06-12 재판정 결과 적용 플레이북 생성 | 조율차장 | 2026-06-06 | `ESCALATED_REDECISION_EXECUTION_PLAYBOOK_20260606.md` |
| 재판정 4분기 상태 전환 시뮬레이션 생성 | QA_테스터 | 2026-06-06 | `REDECISION_BRANCH_SIMULATION_20260606.md` |
| 신규 ESCALATED KST04 승격 충돌 등록 | 지식큐레이터 | 2026-06-13 | `AITEST_20260606_030.md` |

## 6. 조직 내재화 체크리스트

- [ ] 신규 AI 역할 추가 시 SOP의 상황별 라우팅 표에 반영한다.
- [ ] 월간 협업 리허설 6개 시나리오를 실행한다.
- [ ] 실제 충돌은 `CONFLICT_LOG`에 기록한다.
- [ ] 반복 충돌은 PRECEDENT로 승격한다.
- [ ] SOP 위반 사례는 내부성장루프의 개선 후보로 등록한다.
- [ ] 교육/온보딩 문서에 AI 협업 메시지 형식을 포함한다.

## 7. 성숙도 목표

| 기간 | 목표 단계 | 판단 기준 |
|---|---|---|
| 2026-06 | L3 검증 협업 | 협업 세션 3건 이상에서 Evidence/Challenge/Consensus 기록 |
| 2026-07 | L4 학습 협업 | 회고 결과 월 5건 이상 KB, QA, 교육, 자동화 후보로 승격 |
| 2026-Q3 | L5 자동 개선 협업 후보 | 라우팅, 선례 참조, KPI 점검 자동화 후보 정의 |
