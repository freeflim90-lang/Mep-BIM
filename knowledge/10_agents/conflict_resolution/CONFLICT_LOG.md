# AI 간 판단 충돌 로그

> 최종 갱신: 2026-06-06
> 운영 기준: [[conflict_resolution/README]] | 프로토콜: [[조율차장]]

---

## 현황 요약

| 상태 | 건수 |
|------|------|
| OPEN | 0 |
| PENDING | 0 |
| MEDIATED | 0 |
| ESCALATED | 3 |
| SETTLED | 1 |
| PRECEDENT | 1 |
| 누계 | 5 |

---

## 케이스 색인

| ID | 날짜 | 유형 | 당사자 AI | 주제 | 상태 | Opened | Due by | Owner | 결정 근거 |
|----|------|------|----------|------|------|------|------|------|----------|
| AITEST_20260605_004 | 2026-06-05 | T3 우선순위 충돌 | 견적심사원 vs 고객지원CS vs CFO | 범위 외 추가 모델링 무상/유상 판단 | PRECEDENT | 2026-06-05 | 2026-06-08 | 조율차장 | KST02 견적/CFO 판단 우선, 고객관계는 조건부 반영 |
| AITEST_20260605_006 | 2026-06-05 | T4 정책 충돌 | 라이선스_보안관 vs 법무조항검토 vs 성장전략그룹 | 개인정보/외부 AI 정책 문서 정합성 | ESCALATED | 2026-06-05 | 2026-06-12 | 법무조항검토 | Local-only 임시 적용, CEO+법무+보안관 정책 확정 필요 |
| AITEST_20260605_007 | 2026-06-05 | T3 우선순위 충돌 / T4 정책 충돌 | CFO vs 고객지원CS vs 전략기획 | 상업/가격 source of truth 정합성 | ESCALATED | 2026-06-05 | 2026-06-12 | CFO | Starter만 확정 판매, 기타 상품은 CEO/CFO 승인 전 공개 판매 금지 |
| AITEST_20260606_030 | 2026-06-06 | T2 지식 승격 / T4 품질 정책 충돌 | 지식큐레이터 vs 고객지원CS vs 성장전략그룹 | KST04 자동수집 지식 고객 응답 승격 | ESCALATED | 2026-06-06 | 2026-06-13 | 지식큐레이터 | 고객 확정 응답 전 공식 출처, QA 문구, 법무 검토 필요 |
| AITEST_20260605_008 | 2026-06-05 | T3 우선순위 충돌 | 견적심사원 vs 고객지원CS vs CFO | clash report 추가 리뷰 무상/유상 판단 | SETTLED | 2026-06-05 | 2026-06-06 | 고객지원CS | AITEST_20260605_004 PRECEDENT 적용 |

---

## 선례(PRECEDENT) 빠른 참조

> 합의 결과가 PRECEDENT로 승격되면 아래에 요약 추가

| ID | 선례 요약 | 즉시 적용 조건 | 주의 |
|----|----------|----------------|------|
| AITEST_20260605_004 | 범위 외 추가 작업은 유상 견적 원칙. 고객 신뢰 회복 목적의 무상 지원은 CFO 승인 공수 상한 내 1회성 예외만 가능 | T3 우선순위 충돌 + 견적심사원/고객지원CS/CFO 조합 + 범위 외 무상/유상 쟁점 | 계약/SOW와 예상 공수 확인 전 고객에게 무상 수락 표현 금지 |

## 협업 리허설 기록

| ID | 날짜 | 범위 | 결과 | 상세 |
|----|------|------|------|------|
| AITEST_20260605_001 | 2026-06-05 | 기술 구현, 고객 응대, 견적/계약, 보안, 전략/제품화, AI 판단 충돌 | CONDITIONAL PASS | `cases/AITEST_20260605_001.md` |
| AITEST_20260605_002 | 2026-06-05 | 고객 납품 지연 + 추가 요구 | CONDITIONAL PASS | `cases/AITEST_20260605_002.md` |
| AITEST_20260605_003 | 2026-06-05 | 고객 모델 로그 외부 AI 전송 | PASS | `cases/AITEST_20260605_003.md` |
| AITEST_20260605_004 | 2026-06-05 | 견적 판단 충돌 | PRECEDENT | `cases/AITEST_20260605_004.md` |
| AITEST_20260605_005 | 2026-06-05 | 자동수집 지식 고객 응답 승격 | CONDITIONAL PASS | `cases/AITEST_20260605_005.md` |
| AITEST_20260605_006 | 2026-06-05 | 개인정보/외부 AI 정책 문서 충돌 | ESCALATED | `cases/AITEST_20260605_006.md` |
| AITEST_20260605_007 | 2026-06-05 | 상업/가격 source of truth 충돌 | ESCALATED | `cases/AITEST_20260605_007.md` |
| AITEST_20260605_008 | 2026-06-05 | PRECEDENT 승격 및 재사용 | PASS | `cases/AITEST_20260605_008.md` |
| AITEST_20260605_009 | 2026-06-05 | 리스크 게이트 상태값 표준화 | PASS | `cases/AITEST_20260605_009.md` |
| AITEST_20260605_010 | 2026-06-05 | ESCALATED 후속 SLA 사전 추적 | PASS | `cases/AITEST_20260605_010.md` |
| AITEST_20260605_011 | 2026-06-05 | 신규 AI 역할 온보딩 및 내재화 | CONDITIONAL PASS | `cases/AITEST_20260605_011.md` |
| AITEST_20260605_012 | 2026-06-05 | 신규 AI 온보딩 카드 2회 반복 적용 | PASS | `cases/AITEST_20260605_012.md` |
| AITEST_20260605_013 | 2026-06-05 | ESCALATED source of truth 초안 생성 | CONDITIONAL PASS | `cases/AITEST_20260605_013.md` |
| AITEST_20260606_014 | 2026-06-06 | 날짜 롤오버 및 일일 인계 검증 | PASS | `cases/AITEST_20260606_014.md` |
| AITEST_20260606_015 | 2026-06-06 | 2026-06-12 에스컬레이션 재판정 분기 리허설 | PASS | `cases/AITEST_20260606_015.md` |
| AITEST_20260606_016 | 2026-06-06 | 협업 등록부 자동 감사 후보 | PASS | `cases/AITEST_20260606_016.md` |
| AITEST_20260606_017 | 2026-06-06 | 자동 감사 운영 배치 의사결정 | PASS | `cases/AITEST_20260606_017.md` |
| AITEST_20260606_018 | 2026-06-06 | 자동 감사 스크립트화 검증 | PASS | `cases/AITEST_20260606_018.md` |
| AITEST_20260606_019 | 2026-06-06 | 자동 감사 네거티브 컨트롤 | PASS | `cases/AITEST_20260606_019.md` |
| AITEST_20260606_020 | 2026-06-06 | 자동 감사 네거티브 컨트롤 확장 | PASS | `cases/AITEST_20260606_020.md` |
| AITEST_20260606_021 | 2026-06-06 | 자동 감사 실패 메시지 가독성 | PASS | `cases/AITEST_20260606_021.md` |
| AITEST_20260606_022 | 2026-06-06 | 자동 감사 강제 적용 리허설 | PASS | `cases/AITEST_20260606_022.md` |
| AITEST_20260606_023 | 2026-06-06 | ESCALATED 재판정 준비성 감사 | CONDITIONAL PASS | `cases/AITEST_20260606_023.md` |
| AITEST_20260606_024 | 2026-06-06 | ESCALATED Missing 증거 보완 리허설 | CONDITIONAL PASS | `cases/AITEST_20260606_024.md` |
| AITEST_20260606_025 | 2026-06-06 | ESCALATED 결정 로그 패키지 리허설 | CONDITIONAL PASS | `cases/AITEST_20260606_025.md` |
| AITEST_20260606_026 | 2026-06-06 | ESCALATED Decision Log 자동 감사 확장 | PASS | `cases/AITEST_20260606_026.md` |
| AITEST_20260606_027 | 2026-06-06 | Decision Log Draft 필드 정합성 자동 감사 | PASS | `cases/AITEST_20260606_027.md` |
| AITEST_20260606_028 | 2026-06-06 | ESCALATED 재판정 결과 적용 리허설 | PASS | `cases/AITEST_20260606_028.md` |
| AITEST_20260606_029 | 2026-06-06 | 재판정 4분기 상태 전환 시뮬레이션 | PASS | `cases/AITEST_20260606_029.md` |
| AITEST_20260606_030 | 2026-06-06 | KST04 고객 응답 승격 충돌 | ESCALATED | `cases/AITEST_20260606_030.md` |
| AITEST_20260606_031 | 2026-06-06 | KST04 승격 source of truth 및 Missing 증거 큐 | PASS | `cases/AITEST_20260606_031.md` |
| AITEST_20260606_032 | 2026-06-06 | KST04 후속 큐 자동 감사 확장 | PASS | `cases/AITEST_20260606_032.md` |
| AITEST_20260606_033 | 2026-06-06 | Conflict Log 요약/색인 정합성 자동 감사 | PASS | `cases/AITEST_20260606_033.md` |
| AITEST_20260606_034 | 2026-06-06 | ESCALATED 상태 전환 드리프트 자동 감사 | PASS | `cases/AITEST_20260606_034.md` |
| AITEST_20260606_035 | 2026-06-06 | ESCALATED 닫힘 전환 원자성 자동 감사 | PASS | `cases/AITEST_20260606_035.md` |
| AITEST_20260606_036 | 2026-06-06 | Decision Log 최종화 자동 감사 | PASS | `cases/AITEST_20260606_036.md` |

---

## 케이스 기록 방법

새 충돌 발생 시:
1. 위 색인 표에 행 추가 (ID: `CASE_YYYYMMDD_001` 형식)
2. `cases/CASE_YYYYMMDD_001.md` 파일 생성 (아래 템플릿 사용)
3. 해소 완료 후 상태를 `SETTLED`로 갱신
4. 재발 가능성 높으면 상태를 `PRECEDENT`로 승격, 빠른 참조 섹션에 요약 추가

---

## 케이스 파일 템플릿

```markdown
# CASE_YYYYMMDD_NNN: [충돌 주제 한 줄 요약]

- 날짜: YYYY-MM-DD
- 유형: T1 지식 충돌 / T2 역할 충돌 / T3 우선순위 충돌 / T4 정책 충돌
- 당사자: [AI명 1] vs [AI명 2]
- 상태: OPEN
- Opened:
- Due by:
- Owner:
- Escalation owner:
- Blocker:

## 충돌 내용

[어떤 질문/상황에서 어떤 다른 판단이 나왔는지 서술]

## 당사자 의견

**[AI명 1] 입장:**
- 판단 내용:
- 근거 (KST + 출처):

**[AI명 2] 입장:**
- 판단 내용:
- 근거 (KST + 출처):

## 조율 과정

| 단계 | 날짜 | 내용 |
|------|------|------|
| 1단계 KST 비교 | | |
| 2단계 역할 경계 | | |
| 3단계 직접 조율 | | |
| 4단계 중재 | | |
| 5단계 에스컬레이션 | | |

## 최종 결정

- 결정 내용:
- 결정 근거:
- 결정 주체:
- 확정일:

## 선례 등록 여부

- [ ] PRECEDENT 승격 (재발 가능성 높음)
- 승격 이유:

## Downstream Internalization

| 항목 | 링크/ID | 담당 | 기한 | 검증일 | 상태 |
|---|---|---|---|---|---|
| Decision Log ID | | | | | Created / Updated / Explicitly Deferred / Missing |
| KB update | | | | | Created / Updated / Explicitly Deferred / Missing |
| QA/checklist update | | | | | Created / Updated / Explicitly Deferred / Missing |
| Training update | | | | | Created / Updated / Explicitly Deferred / Missing |
| Backlog item | | | | | Created / Updated / Explicitly Deferred / Missing |
| Precedent summary | | | | | Created / Updated / Explicitly Deferred / Missing |
```

관련: [[조율차장]] · [[지식큐레이터]] · [[COO]] · [[CEO]] · [[최고전략CSO]]
