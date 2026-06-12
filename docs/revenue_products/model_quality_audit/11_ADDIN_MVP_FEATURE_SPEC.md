# LUA BIM LAB
# Model Quality Auditor Add-in MVP 기능 명세

문서번호: LBL-REV-MQA-011  
문서상태: MVP 명세 초안  
작성일: 2026-05-20  
배포등급: Internal Only

---

## 1. MVP 목표

v1.0의 목표는 고객이 Autodesk App Store에서 설치 후 바로 이해할 수 있는 모델 품질진단 Add-in을 제공하는 것이다.

핵심은 “모델 품질을 자동으로 완벽히 판단”하는 것이 아니라, 반복적인 품질 점검 항목을 빠르게 수집하고 보고서화하는 것이다.

---

## 2. v1.0 포함 기능

| 기능 | 설명 | 출력 |
|---|---|---|
| Model Health Summary | 모델 기본 상태 요약 | 점수/등급/요약 |
| Warning Review | Revit warnings 분류 | 경고 목록 |
| Link Status Review | 링크 모델 상태 확인 | 링크 상태표 |
| Workset Review | workshared 모델의 workset 상태 확인 | Workset 요약 |
| Parameter Completeness | 필수 파라미터 누락률 확인 | 누락 항목표 |
| View/Template Review | 뷰/템플릿 정합성 기본 점검 | 검토 목록 |
| Export Report | CSV/XLSX/PDF 중 최소 1개 출력 | 리포트 파일 |
| Entitlement Gate | Store 구독/체험 상태 확인 | 잠금/사용 가능 UX |

---

## 3. v1.0 제외 기능

| 제외 기능 | 제외 이유 |
|---|---|
| 모델 자동 수정 | 고객 모델 변경 리스크 |
| 외부 AI 분석 | 개인정보/모델 데이터 전송 심사 리스크 |
| 법규 적합성 판정 | 책임 범위 과다 |
| 구조/소방 최종 판단 | 전문가 검토 필요 |
| Navisworks 간섭 엔진 | 별도 제품 또는 v2 이후 |
| 클라우드 동기화 | 개인정보/보안 정책 추가 필요 |

---

## 4. 진단 점수 구조

| 영역 | 배점 |
|---|---:|
| 파일/모델 기본 상태 | 20 |
| 링크/좌표/Workset | 20 |
| Warnings/오류 | 20 |
| 파라미터 완성도 | 20 |
| 뷰/템플릿/납품 준비 | 20 |

점수는 절대적인 설계 품질 인증이 아니라 모델 관리 상태를 나타내는 참고 지표로 표시한다.

---

## 5. 리포트 필드

| 필드 | 설명 |
|---|---|
| Audit Date | 검토일 |
| Product Version | Add-in 버전 |
| Revit Version | 실행 Revit 버전 |
| Model Name | 모델명 |
| Overall Score | 종합 점수 |
| Risk Level | Low / Medium / High |
| Issue Category | 파일, 링크, 경고, 파라미터, 뷰 |
| Issue Description | 이슈 설명 |
| Recommended Action | 권장 조치 |

---

## 6. Store 제출 전 성공 기준

| 기준 | 통과 조건 |
|---|---|
| 설치 | 지원 Revit 버전에서 설치/제거 성공 |
| 로딩 | Revit 시작 시 Add-in 로드 및 리본 표시 |
| 실행 | 샘플 모델에서 모든 v1.0 명령 실행 |
| 안정성 | 명령 실행 중 Revit 크래시 없음 |
| 리포트 | 결과 파일 생성 및 열람 가능 |
| 권한 | 구독/체험 상태에 따른 잠금 UX 동작 |
| 문서 | User Guide, Privacy, EULA, Release Notes 준비 |

---

## 7. 개발 우선순위

1. 기존 Model Health Dashboard 기능 검토
2. Store용 제품명/리본/아이콘 분리
3. 로컬 리포트 출력 안정화
4. Entitlement API 연결
5. Revit 2024/2025/2026 smoke test
6. Store listing, screenshots, user guide 정리

