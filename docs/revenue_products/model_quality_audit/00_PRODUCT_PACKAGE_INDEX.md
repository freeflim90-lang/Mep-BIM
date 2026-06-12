# LUA BIM LAB
# MEP BIM 모델 품질진단 상품 패키지

문서번호: LBL-REV-MQA-000  
문서상태: 상품화 초안  
작성일: 2026-05-20  
관리부서: BIM PMO / 품질검증 / 영업기획  
배포등급: Internal / External With Approval

---

## 1. 패키지 목적

본 패키지는 LUA BIM LAB의 첫 번째 수익형 서비스 후보인 `MEP BIM 모델 품질진단`을 실제 영업, 견적, 수행, 납품, 재판매가 가능한 상품으로 운영하기 위한 기준 문서 묶음이다.

이 상품은 고객이 보유한 BIM 모델의 품질, 간섭, 납품 가능성, 데이터 완성도를 짧은 기간 안에 진단하고, 수정 우선순위와 실행 가능한 보고서를 제공하는 서비스다.

---

## 2. 문서 구성

| No. | 문서명 | 파일명 | 용도 |
|---:|---|---|---|
| 1 | 상품 정의서 | `01_PRODUCT_BRIEF.md` | 상품 개요, 타깃, 가치 제안 |
| 2 | 서비스 메뉴 및 가격 구조 | `02_SERVICE_MENU_PRICING.md` | Lite/Standard/Premium 구성 |
| 3 | 고객 접수 정보서 | `03_CLIENT_INTAKE_FORM.md` | 견적 전 자료 요청 |
| 4 | 품질진단 체크리스트 | `04_AUDIT_CHECKLIST.md` | 모델 검토 항목 |
| 5 | 보고서 템플릿 | `05_AUDIT_REPORT_TEMPLATE.md` | 고객 납품 보고서 |
| 6 | 내부 수행 SOP | `06_DELIVERY_WORKFLOW_SOP.md` | 수행 절차와 역할 |
| 7 | 영업 제안 문구 | `07_SALES_MESSAGE_PLAYBOOK.md` | 제안 메일, 통화, 미팅 문구 |
| 8 | 견적 및 SOW 템플릿 | `08_QUOTATION_SOW_TEMPLATE.md` | 범위/제외/납품/변경 기준 |
| 9 | Autodesk App Store 제품화 전략 | `09_AUTODESK_STORE_PRODUCT_STRATEGY.md` | Store 판매 구조 |
| 10 | Store Listing 초안 | `10_STORE_LISTING_DRAFT.md` | 제품 페이지 문안 |
| 11 | Add-in MVP 기능 명세 | `11_ADDIN_MVP_FEATURE_SPEC.md` | v1.0 구현 범위 |
| 12 | Store 제출 체크리스트 | `12_STORE_SUBMISSION_CHECKLIST.md` | 제출 전 검수 |
| 13 | 제품 로드맵 | `13_PRODUCT_ROADMAP.md` | 버전별 확장 계획 |
| 14 | Obsidian 지식관리 기준 | `14_OBSIDIAN_KNOWLEDGE_SYSTEM.md` | 개발 오류/수정/결정 지식 그래프 |

---

## 3. 상품 포지션

| 항목 | 기준 |
|---|---|
| 상품명 | Model Quality Auditor |
| Store 표시 | Model Quality Auditor - Works with Autodesk Revit® |
| 핵심 고객 | 시공사, 설계사, CM, BIM 외주 수행사, 발주처 기술팀, BIM Manager |
| 핵심 문제 | 모델은 있으나 품질, 간섭, 납품 가능성, 수정 우선순위가 불명확 |
| 핵심 산출물 | Add-in 기반 모델 품질 리포트, 이슈 목록, 수정 우선순위, 납품 적합성 판단 보조 |
| 초기 판매 방식 | Autodesk App Store 구독형 Add-in |
| 확장 판매 | 리포트 리뷰 컨설팅, 고객사 교육, BEP/CDE 컨설팅, 물량/변경관리 |

---

## 4. 관련 기준 문서

| 문서 | 활용 |
|---|---|
| `docs/standard_documents/05_MODELING_DELIVERY_STANDARD.md` | 모델링/납품 기준 |
| `docs/standard_documents/06_CLASH_QA_STANDARD.md` | 간섭 및 품질 검증 기준 |
| `docs/standard_documents/12_QUOTATION_SOW_STANDARD.md` | 견적/SOW 기준 |
| `docs/standard_documents/14_SECURITY_NDA_STANDARD.md` | 보안/NDA 기준 |
| `docs/lua_bim_lab_official_documents/07_BIM_QUALITY_ASSURANCE_STATEMENT.md` | 외부 품질보증 설명 |
| `docs/lua_bim_lab_official_documents/16_SCOPE_CONFIRMATION_SOW_TEMPLATE.md` | 외부 범위 확인서 |

---

## 5. 운영 원칙

1. 품질진단은 모델을 대신 수정하는 서비스가 아니라, 상태를 객관적으로 진단하고 수정 우선순위를 제시하는 서비스다.
2. 고객 자료 수령 전 보안 조건과 사용 범위를 확인한다.
3. 모든 진단 결과는 모델명, 버전, 검토일, 기준 문서를 명시한다.
4. 추정이나 의견은 사실 기반 검토 결과와 구분하여 작성한다.
5. 추가 모델링, 도면 수정, 물량 산출, 반복 재검토는 별도 범위로 관리한다.
6. Autodesk App Store 판매 제품은 고객 모델 데이터를 외부 서버로 전송하지 않는 로컬 진단 기능을 기본 원칙으로 한다.
7. 제품명에는 Autodesk 또는 Revit을 소유권처럼 포함하지 않고, 호환 설명에서만 Autodesk Revit®을 표기한다.
