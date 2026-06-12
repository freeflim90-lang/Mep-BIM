# LUA BIM LAB
# BIM 라이브러리 및 패밀리 등록부 템플릿

━━━━━━━━━━━━━━━━━━━━

문서번호: LBL-STD-026  
문서상태: 기준 초안  
작성일: 2026-05-21  
배포등급: Internal / Client-Shareable  
적용범위: Revit Family, MEP BIM 라이브러리, 공통 파라미터, 납품 자산, 교육 실습 자산

## 1. 목적

본 문서는 LUA BIM LAB에서 사용하는 BIM 라이브러리, Revit Family, 공통 파라미터, 유형별 표준 자산을 체계적으로 등록하고 재사용하기 위한 표준 템플릿이다.

라이브러리 등록부는 프로젝트 산출물, 교육자료, Model Quality Auditor 룰, Add-in 기능 후보와 연결되는 조직 지식 자산으로 관리한다.

## 2. 문서 정보

| 항목 | 내용 |
|---|---|
| 라이브러리 그룹 | 공조 / 배관 / 소방 / 전기 / 통신 / 위생 / 공통 |
| 작성일 |  |
| 관리 담당 |  |
| 검토자 |  |
| 적용 프로젝트 | 공통 / 프로젝트명 |
| Revision | Rev.00 |

## 3. 등록 기준

| 항목 | 기준 |
|---|---|
| 명명 규칙 | 공종_분류_장비명_규격_Rev |
| 파라미터 | 회사 표준 파라미터와 프로젝트 요구 파라미터를 구분 |
| LOD | 단계별 요구 수준을 명확히 표기 |
| 원점/커넥터 | 삽입 기준점, Connector 방향, Flow 기준 검토 |
| 물량 연계 | 산출 대상 파라미터와 산식 연결 여부 확인 |
| 공개 등급 | 내부용, 고객 납품 가능, 교육용, 검토 필요로 구분 |

## 4. 라이브러리 등록부

| No. | Family ID | 공종 | 분류 | Family명 | Type | LOD | 파라미터 상태 | 검수상태 | 공개등급 | 위치/경로 | 비고 |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 |  | HVAC / Piping / Fire / Electrical / Telecom / Plumbing | 장비 / 배관부속 / 덕트부속 / 전기기기 |  |  | 200 / 300 / 350 / 400 | 완료 / 보완 / 미검토 | Draft / QA / Approved / Deprecated | Internal / Client-Shareable / Training |  |  |

## 5. 검수 체크리스트

| 검수 항목 | 기준 | 결과 | 비고 |
|---|---|---|---|
| 명명 규칙 준수 | 표준 명명 규칙 적용 | Pass / Fail / N.A. |  |
| Type 구성 | 불필요한 중복 Type 없음 | Pass / Fail / N.A. |  |
| Connector 설정 | 방향, 시스템, 크기, 연결성 검토 | Pass / Fail / N.A. |  |
| 파라미터 | 필수 파라미터 누락 없음 | Pass / Fail / N.A. |  |
| 물량 산출 | 수량/길이/면적/중량 산출 가능 | Pass / Fail / N.A. |  |
| 시각 표현 | 평면/단면/3D 표현 적정 | Pass / Fail / N.A. |  |
| 파일 용량 | 과도한 형상/불필요 요소 없음 | Pass / Fail / N.A. |  |
| 버전 호환 | 사용 Revit 버전 확인 | Pass / Fail / N.A. |  |

## 6. 변경 이력

| Revision | 변경일 | 변경 내용 | 변경 사유 | 작성/검토 |
|---|---|---|---|---|
| Rev.00 |  | 최초 등록 |  |  |

## 7. 교육 및 제품 연결

| 연결 대상 | 활용 방식 |
|---|---|
| 연차별 교육자료 | Family 제작, 파라미터, 물량 연계 실습 |
| Model Quality Auditor | 패밀리 명명, 파라미터 누락, Connector 오류 진단 룰 |
| Add-in 기능 후보 | 등록부 자동 생성, Family 품질 스캔, 표준 파라미터 주입 |
| 납품 체크리스트 | 고객 제출 가능 여부와 검수 상태 확인 |

## 8. 관련 문서

- `05_MODELING_DELIVERY_STANDARD.md`
- `06_CLASH_QA_STANDARD.md`
- `17_DELIVERY_ACCEPTANCE_STANDARD.md`
- `23_MEP_BIM_AI_CAREER_MASTER_PLAN.md`
