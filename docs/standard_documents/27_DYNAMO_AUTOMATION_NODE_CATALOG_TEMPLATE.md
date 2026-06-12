# LUA BIM LAB
# Dynamo 자동화 노드 카탈로그 템플릿

━━━━━━━━━━━━━━━━━━━━

문서번호: LBL-STD-027  
문서상태: 기준 초안  
작성일: 2026-05-21  
배포등급: Internal  
적용범위: Dynamo, Revit 자동화, MEP BIM 생산성 개선, Add-in 기능 후보, 교육 실습

## 1. 목적

본 문서는 Dynamo 그래프, Python 노드, 반복 자동화 스크립트를 조직 지식 자산으로 등록하고, 재사용 가능성 및 Add-in 전환 가능성을 평가하기 위한 LUA BIM LAB 표준 템플릿이다.

## 2. 문서 정보

| 항목 | 내용 |
|---|---|
| 카탈로그명 | Dynamo 자동화 노드 카탈로그 |
| 작성일 |  |
| 관리 담당 |  |
| 검토자 |  |
| 적용 버전 | Revit / Dynamo / Package 버전 |
| Revision | Rev.00 |

## 3. 등록 기준

| 항목 | 기준 |
|---|---|
| 목적 | 해결하는 업무 문제를 한 문장으로 정의 |
| 입력값 | 사용자 입력, 선택 요소, 파일, 파라미터를 명확히 표기 |
| 출력값 | 모델 변경, 엑셀 출력, 리포트 생성 등 결과 명시 |
| 위험도 | 모델을 직접 수정하는 기능은 백업 및 테스트 기준 필요 |
| 재사용성 | 프로젝트 의존 로직과 공통 로직을 구분 |
| Add-in 전환성 | 반복 사용, UI 필요, 오류 방지 필요 여부를 평가 |

## 4. 노드/그래프 카탈로그

| No. | Automation ID | 명칭 | 목적 | 공종 | 입력 | 출력 | 위험도 | 재사용성 | Add-in 후보 | 상태 |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 |  |  |  | MEP / 공통 | 요소 선택 / Excel / Parameter / View | 모델 수정 / 리포트 / CSV / 뷰 생성 | Low / Medium / High | Project / Common | Yes / No / Later | Draft / Tested / Approved / Deprecated |

## 5. 상세 카드

### 5.1 Automation ID

| 항목 | 내용 |
|---|---|
| 명칭 |  |
| 업무 문제 |  |
| 사용 대상 | 모델러 / BIM 코디네이터 / QA / PM |
| 사용 시점 | 착수 / 모델링 / 검토 / 납품 / 종료 |
| 필요 패키지 |  |
| 테스트 Revit 버전 |  |

#### 입력 조건

-

#### 실행 절차

1. 
2. 
3. 

#### 출력 결과

-

#### 오류 및 예외

| 오류 상황 | 원인 | 대응 | 오답노트 연결 |
|---|---|---|---|
|  |  |  |  |

#### Add-in 전환 판단

| 판단 항목 | 결과 |
|---|---|
| 반복 사용 빈도 | 높음 / 중간 / 낮음 |
| 사용자 UI 필요성 | 높음 / 중간 / 낮음 |
| 모델 변경 위험도 | 높음 / 중간 / 낮음 |
| 상용화 가능성 | 높음 / 중간 / 낮음 |
| 우선순위 | P1 / P2 / P3 / 보류 |

## 6. 운영 원칙

- 모델 변경 자동화는 샘플 모델에서 먼저 테스트한다.
- 프로젝트 전용 경로, 고객명, 내부 서버 경로는 카탈로그에 남기지 않는다.
- 패키지 의존성이 있는 경우 버전을 반드시 기록한다.
- 반복 오류는 Obsidian 오류 오답노트에 연결한다.
- Add-in 전환 후보는 Model Quality Auditor 또는 Add-in Dashboard 로드맵에 연결한다.

## 7. 관련 문서

- `23_MEP_BIM_AI_CAREER_MASTER_PLAN.md`
- `docs/revenue_products/model_quality_audit/00_PRODUCT_PACKAGE_INDEX.md`
- `docs/revenue_products/model_quality_audit/14_OBSIDIAN_KNOWLEDGE_SYSTEM.md`
- `docs/internal_organization_documents/21_KNOWLEDGE_CURATION_INTELLIGENCE_CELL.md`
