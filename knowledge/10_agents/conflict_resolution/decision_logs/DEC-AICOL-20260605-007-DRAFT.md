# DEC-AICOL-20260605-007-DRAFT: Product Launch Status 재판정 로그 초안

문서상태: Draft Created  
작성일: 2026-06-06  
재판정 예정일: 2026-06-12

## 1. 결정 개요

| 항목 | 내용 |
|---|---|
| Decision ID | DEC-AICOL-20260605-007-DRAFT |
| 제목 | 상품별 공개 판매 가능 상태와 고객 안내 문구 |
| 결정일 | 2026-06-12 예정 |
| 요청자 | 조율차장 |
| 승인자 | CEO, CFO, 법무조항검토 |
| 관련 프로젝트 | Product Launch Status |
| AI 협업 세션 ID | AICOL-20260605-007 |
| 관련 케이스 | AITEST_20260605_007 |
| 합의 상태 | ESCALATE |

## 2. 배경

Starter-only 출시 기준과 Project Mentor 가격/약관/결제 링크 문서가 충돌했다.
현재 임시 원칙은 `APPROVED_WITH_HOLD / Starter-only`이며, Starter 외 상품은 Coming Soon 또는 Consultation-only로 유지한다.

## 3. 재판정 선택지

| 선택지 | 적용 조건 | 리스크 | 후속 조치 |
|---|---|---|---|
| A. Starter-only 승인 | Starter 가격표, 결제 링크, 약관/환불 문구, CS 문구가 승인됨 | Starter 외 문의 혼선 | CS QA와 가격 문서 업데이트 |
| B. Starter 외 일부 승인 | CEO/CFO/법무/운영 리소스 증거가 상품별로 있음 | 운영 과부하, 환불 분쟁 | 상품별 Launch Status를 SALE_READY/CONSULTATION_ONLY로 갱신 |
| C. 명시적 보류 | 승인 필수 증거가 부족하지만 보류 사유와 다음 Due by가 명확함 | 출시 지연 | Explicitly Deferred, Starter-only 유지 |
| D. 위반 | Due by 이후에도 결정/보류/보완 근거가 없음 | 고객 안내/결제 혼선 | BREACHED, CEO/COO 에스컬레이션 |

## 4. 현재 초안 판정

| 항목 | 내용 |
|---|---|
| 선택안 | A 또는 C 후보 |
| 결정 사유 | 2026-06-06 기준 Starter 외 상품은 CEO/CFO/법무/운영 리소스 증거가 Missing |
| 적용 시점 | 2026-06-12 재판정 후 |
| 후속 조치 | Missing Evidence Matrix의 007 P0/P1 큐를 보완하고, 보완 전까지 Starter-only 유지 |

## 5. AI 협업 근거 및 반론

| 항목 | 내용 |
|---|---|
| 주관 AI | CFO |
| 검토 AI | CEO, 법무조항검토, 고객지원CS, COO |
| 반론 AI | 전략기획 |
| 채택한 근거 | `PRODUCT_LAUNCH_STATUS_SOURCE_OF_TRUTH_DRAFT_20260605.md`, `ESCALATED_MISSING_EVIDENCE_MATRIX_20260606.md` |
| 기각한 대안 | Project Mentor 가격/결제 링크를 승인 전 공개 |
| 주요 반론 | 시장 검증을 빠르게 하고 싶은 필요는 있으나 약관/환불/운영 증거 없이 결제 링크를 공개하면 고객 혼선 위험이 큼 |
| 보류 조건 | CEO/CFO 승인, 법무 검토, 운영 리소스, Starter 외 상품 승인 Missing |
| 지식화 위치 | CFO KB, 고객지원CS QA, 가격/결제 운영 문서 |

## 6. 재판정 체크

| 체크 | 상태 | 필요 조치 |
|---|---|---|
| Starter 가격표 CFO 승인 | Missing | CFO 승인 또는 보류 사유 기록 |
| CEO 출시 승인 | Missing | CEO 승인 또는 보류 사유 기록 |
| 약관/환불 문구 법무 검토 | Missing | 법무조항검토 보완 |
| CS 고객 문구 확정 | Draft | 고객지원CS와 CFO 확인 |
| 운영 리소스 확인 | Missing | COO 보완 |
| Starter 외 상품 승인 | Missing | CEO/CFO 승인 전 Coming Soon 또는 Consultation-only 유지 |

## 7. 변경 이력

| 일자 | 변경 내용 | 변경자 |
|---|---|---|
| 2026-06-06 | 재판정 로그 초안 생성 | 조율차장 |
