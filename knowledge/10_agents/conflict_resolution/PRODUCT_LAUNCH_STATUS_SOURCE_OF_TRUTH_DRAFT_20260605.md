# Product Launch Status Source of Truth Draft - 2026-06-05

문서상태: CEO/CFO 승인 전 초안  
관련 케이스: `cases/AITEST_20260605_007.md`  
목적: 고객에게 공개 가능한 상품, 가격, 결제 링크, Coming Soon 문구의 단일 기준을 정리한다.

## 1. 임시 결론

CEO/CFO가 최종 승인하기 전까지 공개 판매 가능한 상품은 Starter만으로 본다.
Project Mentor Standard/Intensive 및 상위 멘토링 상품은 준비 문서 또는 별도 상담 후보로만 취급한다.

## 2. Launch Status 표

| 상품 | Launch Status | 고객 공개 가격 | 결제 링크 | 고객 안내 가능 문구 | 금지 문구 |
|---|---|---|---|---|---|
| Starter Plan | SALE_READY | 공개 가능 | Starter 승인 링크만 가능 | "Starter Plan은 현재 신청 가능합니다." | 승인되지 않은 할인/환불 약속 |
| Personal Tutor | COMING_SOON | 확정 금지 | 금지 | "준비 중이며 관심 등록 또는 상담으로 안내드릴 수 있습니다." | "지금 결제 가능합니다." |
| Coordinator Mentor | COMING_SOON | 확정 금지 | 금지 | "준비 중이며 운영 일정 확정 후 안내드리겠습니다." | "월 가격이 확정되었습니다." |
| Project Mentor Standard | CONSULTATION_ONLY | 내부 검토 | CEO/CFO 승인 전 금지 | "프로젝트 범위 확인 후 별도 상담으로 검토합니다." | "USD 490로 바로 결제 가능합니다." |
| Project Mentor Intensive | CONSULTATION_ONLY | 내부 검토 | CEO/CFO 승인 전 금지 | "운영 리소스와 범위 확인 후 별도 상담으로 검토합니다." | "USD 790로 바로 결제 가능합니다." |

## 3. 상태값 정의

| 상태값 | 의미 | 고객 발송 |
|---|---|---|
| SALE_READY | 가격, 약관, 결제 링크, 운영 리소스, CS 문구가 승인됨 | 가능 |
| COMING_SOON | 상품 아이디어 또는 준비 문서는 있으나 판매 승인 전 | 관심 등록/준비 중 안내만 가능 |
| CONSULTATION_ONLY | 가격표 확정 전, 범위 확인과 수동 상담만 가능 | 결제 링크 없이 상담 안내 가능 |
| INTERNAL_DRAFT | 내부 기획/약관/가격 초안 | 고객 발송 금지 |
| HOLD | 법무/환불/운영 리스크로 보류 | 고객 발송 금지 |

## 4. 고객 응대 문구 초안

Starter 문의:

> Starter Plan은 현재 신청 가능한 상품입니다. 신청 전 커리큘럼, 제공 범위, 환불 및 지원 조건을 확인해 주세요.

Project Mentor 문의:

> Project Mentor는 현재 공개 결제 상품이 아니라 별도 상담 후보입니다. 프로젝트 범위, 필요한 지원 강도, 운영 가능 일정을 확인한 뒤 가능 여부를 검토하겠습니다. CEO/CFO 승인 전에는 확정 가격이나 결제 링크를 안내드리지 않습니다.

상위 상품 가격 문의:

> 상위 멘토링 상품은 아직 공개 판매 가격이 확정되지 않았습니다. 현재 안내 가능한 확정 상품과 준비 중인 상품을 구분해 안내드리겠습니다.

## 5. 승인 체크리스트

| 항목 | Starter | Personal Tutor | Coordinator Mentor | Project Mentor |
|---|---|---|---|---|
| 가격표 CFO 승인 | 필요 | Missing | Missing | Missing |
| CEO 출시 승인 | 필요 | Missing | Missing | Missing |
| 약관/환불 문구 법무 검토 | 필요 | Missing | Missing | Missing |
| CS 고객 문구 | 필요 | Draft | Draft | Draft |
| 결제 링크 | 승인된 링크만 | 금지 | 금지 | 금지 |
| 운영 리소스 확인 | 필요 | Missing | Missing | Missing |

## 6. 문서 정합성 수정 후보

| 문서 | 현재 위험 | 수정 방향 |
|---|---|---|
| `docs/personal_mep_bim_tutor_pricing_payment.md` | Starter-only와 다중 플랜 출시 문구 혼재 | 상품별 Launch Status 필드 추가 |
| `docs/project_mentor_terms_and_disclaimers.md` | 가격/환불 조건이 공개 판매 약관처럼 읽힐 수 있음 | 배포 등급과 `CONSULTATION_ONLY` 상태 표시 |
| `docs/external_service_setup_guide.md` | Project Mentor 결제 링크 생성 작업이 공개 준비로 오해될 수 있음 | CEO/CFO 승인 전 링크 생성/발송 금지 표시 |
| `data/knowledge_base/CFO.md` | App Store 구독 가격과 교육 상품 가격 기준이 혼재 | 상품군별 source of truth 분리 |
| `data/knowledge_base/고객지원CS.md` | 가격 문의 응대 시 상위 상품 확정 안내 위험 | Coming Soon/상담 후보 문구 추가 |

## 7. 판정

이 문서는 최종 가격표가 아니라 `AITEST_20260605_007`의 후속 결정을 위한 source of truth 초안이다.
승인 전 운영 상태는 `APPROVED_WITH_HOLD`이며, 실패 시 Starter 외 상품은 Coming Soon 또는 Consultation-only로 유지한다.

## 8. 후속 보완 입력물

2026-06-12 재판정 전 Missing 항목은 `ESCALATED_MISSING_EVIDENCE_MATRIX_20260606.md`의 007 보완 큐를 기준으로 보완한다.
CEO/CFO 승인, 약관/환불 법무 검토, CS 문구, 운영 리소스, Starter 외 상품 승인 중 하나라도 비어 있으면 Starter-only 원칙을 유지한다.
