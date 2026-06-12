# LUA BIM LAB
# Model Quality Auditor Store 제출 체크리스트

문서번호: LBL-REV-MQA-012  
문서상태: 제출 전 체크리스트 초안  
작성일: 2026-05-20  
배포등급: Internal Only

---

## 1. 제품 범위

| 항목 | 상태 | 비고 |
|---|---|---|
| 제품명 확정 | □ | Model Quality Auditor |
| Store 설명문 확정 | □ | 영어 우선 |
| v1.0 기능 목록 확정 | □ | 기능 과장 금지 |
| 제외 기능 명시 | □ | AI/클라우드/자동수정 제외 |
| 지원 Revit 버전 확정 | □ | 실제 테스트 후 표기 |

---

## 2. 빌드/설치

| 항목 | 상태 | 비고 |
|---|---|---|
| Release 빌드 생성 | □ | Debug DLL 제외 |
| `.addin` 매니페스트 확인 | □ | 설치 경로, Assembly 경로 |
| 설치 프로그램 생성 | □ | Revit 종료 안내 포함 |
| 제거 기능 확인 | □ | 잔여 파일 최소화 |
| 하드코딩 로컬 경로 제거 | □ | 개발자 PC 경로 금지 |

---

## 3. 기능 테스트

| 항목 | 상태 | 비고 |
|---|---|---|
| Revit 2024 설치/로드 테스트 | □ | 증빙 캡처 |
| Revit 2025 설치/로드 테스트 | □ | 증빙 캡처 |
| Revit 2026 설치/로드 테스트 | □ | 증빙 캡처 |
| 샘플 건축 모델 테스트 | □ | |
| 샘플 MEP 모델 테스트 | □ | |
| Workshared 모델 테스트 | □ | 가능 시 |
| 리포트 출력 테스트 | □ | CSV/XLSX/PDF |
| 오류/예외 메시지 확인 | □ | 사용자 친화 문구 |

---

## 4. 구독/라이선스

| 항목 | 상태 | 비고 |
|---|---|---|
| Autodesk App Store App ID 확인 | □ | |
| Entitlement API 동작 확인 | □ | |
| Trial 상태 UX 확인 | □ | |
| 구독 만료 UX 확인 | □ | |
| 네트워크 실패 UX 확인 | □ | |
| 비밀값 DLL 포함 여부 확인 | □ | 포함 금지 |

---

## 5. Store 문서

| 문서 | 상태 | 위치 |
|---|---|---|
| Store Listing | □ | `10_STORE_LISTING_DRAFT.md` |
| User Guide | □ | `docs/autodesk_store/USER_GUIDE_DRAFT.md` 기반 |
| EULA | □ | `docs/autodesk_store/EULA_DRAFT.md` 기반 |
| Privacy Policy | □ | `docs/autodesk_store/PRIVACY_POLICY_DRAFT.md` 기반 |
| Release Notes | □ | `docs/autodesk_store/RELEASE_NOTES_V1_0.md` 기반 |
| Support Runbook | □ | `docs/autodesk_store/SUPPORT_RUNBOOK.md` 기반 |
| Screenshots | □ | 실제 UI 캡처 |
| Demo Video | □ | 필요 시 |

---

## 6. 표현 검수

| 항목 | 상태 | 비고 |
|---|---|---|
| Autodesk 공식 제품처럼 보이는 표현 제거 | □ | |
| 제품명에 Autodesk/Revit 소유 표현 없음 | □ | |
| `Works with Autodesk Revit®` 표기 확인 | □ | |
| 법규/설계 적합성 보증 표현 제거 | □ | |
| 모델 데이터 외부 전송 여부 명확히 표기 | □ | |
| 지원 이메일 확인 | □ | |

---

## 7. 제출 결정

| 게이트 | 승인자 | 상태 |
|---|---|---|
| 제품 범위 승인 | CEO / Product | □ |
| QA 승인 | QA | □ |
| 법무/문구 승인 | 법무/문서 | □ |
| 가격 승인 | CEO / 재무 | □ |
| 최종 제출 승인 | 대표 | □ |

