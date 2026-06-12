# LUA BIM LAB
# Autodesk App Store 제품화 전략

문서번호: LBL-REV-MQA-009  
문서상태: 제품화 전략 초안  
작성일: 2026-05-20  
배포등급: Internal Only

---

## 1. 전략 전환

기존 `MEP BIM 모델 품질진단`은 컨설팅형 서비스로 정의되었으나, 기본 판매처를 Autodesk App Store로 설정할 경우 1차 상품은 Add-in 제품이어야 한다.

따라서 본 상품은 다음 구조로 전환한다.

| 구분 | 기존 방향 | Store 중심 방향 |
|---|---|---|
| 판매물 | 품질진단 용역 | 품질진단 Add-in |
| 고객 접점 | 제안서/견적/미팅 | Autodesk App Store 검색/설치/체험 |
| 산출물 | 컨설턴트 작성 보고서 | Add-in 생성 리포트 |
| 수익 방식 | 프로젝트별 견적 | 월 구독/연 구독 |
| 후속 매출 | 재검토/교육 | Pro 기능, 팀 라이선스, 컨설팅 업셀 |

---

## 2. 권장 제품 포지션

| 항목 | 기준 |
|---|---|
| 제품명 | Model Quality Auditor |
| Store 설명명 | Model Quality Auditor - Works with Autodesk Revit® |
| 회사명 | LUA BIM LAB |
| 제품 유형 | Revit Add-in |
| 1차 고객 | BIM Manager, BIM Coordinator, MEP Modeler, Contractor |
| 핵심 약속 | 모델 품질 문제를 빠르게 찾아 보고서로 정리 |
| v1.0 원칙 | 로컬 실행, 외부 AI/클라우드 전송 없음, 설치/구독 검증 안정성 우선 |

---

## 3. 왜 Store 제품으로 적합한가

| 판단 기준 | 적합성 |
|---|---|
| 반복 사용성 | 모델 제출 전, 주간 검토, 외주 검수마다 반복 사용 |
| 구매 명확성 | 품질 확인, 납품 리스크 감소, 검토 시간 단축 |
| Store 검색성 | model health, quality check, BIM audit, Revit add-in 키워드와 연결 |
| 기술 난이도 | Model Health Dashboard 계열 기능과 연결 가능 |
| 구독 적합성 | 월별/프로젝트별 반복 검토 도구로 구독 가치 존재 |

---

## 4. 기존 자산과 연결

| 기존 자산 | 활용 방향 |
|---|---|
| `Model Health Dashboard` | v1.0 핵심 엔진 후보 |
| `BIM Command Center` | 통합 셸 또는 상위 제품으로 활용 가능 |
| `QA_SMOKE_TEST_PLAN.md` | Store 제출 전 테스트 기준 |
| `SUBSCRIPTION_PRICING.md` | 구독 가격 기준 |
| `ENTITLEMENT_API_IMPLEMENTATION.md` | 구독 권한 확인 기준 |
| 품질진단 보고서 템플릿 | Add-in 리포트 출력 양식으로 변환 |

---

## 5. 제품 구조 권장안

### 권장 1안: 단독 제품

`Model Quality Auditor`를 단독 Store 제품으로 출시한다.

| 장점 | 단점 |
|---|---|
| 메시지가 명확하고 검색성이 좋음 | 별도 설치/지원/문서 필요 |
| 품질진단 수익 아이템과 직접 연결 | 기존 BIM Command Center와 중복 가능 |
| 컨설팅 업셀 연결이 쉬움 | 초기 리뷰/평점 확보가 필요 |

### 권장 2안: BIM Command Center 내부 모듈

`BIM Command Center` 안에 `Model Quality Auditor` 모듈을 포함한다.

| 장점 | 단점 |
|---|---|
| 기존 Store 준비 문서와 연결 쉬움 | 제품 메시지가 넓어짐 |
| 여러 기능을 묶어 가격 정당화 가능 | 품질진단 상품성이 희석될 수 있음 |
| 향후 Pro 모듈 확장 용이 | Store 설명이 복잡해짐 |

---

## 6. 추천 결정

첫 Store 수익형 아이템은 **단독 제품에 가까운 포지션**으로 잡되, 기술 구현은 기존 `BIM Command Center` 셸과 `Model Health Dashboard` 자산을 재사용하는 것이 좋다.

권장 구조:

1. Store 노출명: `Model Quality Auditor`
2. 내부 코드/셸: 기존 Addin Dashboard 또는 BIM Command Center 재사용 가능
3. v1.0 기능: 모델 품질 스캔, 점수화, 이슈 목록, CSV/PDF 리포트
4. v1.1 기능: MEP 특화 규칙 추가
5. v2.0 기능: 팀 기준 템플릿, 비교 리포트, 컨설팅 연계

---

## 7. 수익 모델

| 플랜 | 권장 방향 |
|---|---|
| Free Trial | 30일 체험 |
| Individual | 월 구독 |
| Team | 5인 또는 10인 패키지 |
| Enterprise | 직접 계약, 교육/컨설팅 포함 |

초기 가격은 기존 `SUBSCRIPTION_PRICING.md`의 `USD 19/month` 기준을 검토하되, 단독 제품일 경우 `USD 9~19/month` 범위에서 시장 반응을 확인한다.

---

## 8. Store 리스크

| 리스크 | 대응 |
|---|---|
| 제품명에 Autodesk/Revit 오용 | 제품명은 독립명 사용, 설명에만 호환 제품 표기 |
| 개인정보/모델 데이터 전송 우려 | v1.0은 로컬 실행, 외부 전송 없음으로 설계 |
| 기능 과장 | 자동 설계검토/법규검토가 아니라 품질진단 보조로 표현 |
| 지원 버전 과다 표기 | 실제 테스트한 Revit 버전만 표기 |
| 구독 검증 실패 | Entitlement API 실패 시 유료 기능 잠금과 안내 UX 제공 |

