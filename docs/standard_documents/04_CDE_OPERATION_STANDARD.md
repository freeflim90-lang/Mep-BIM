# CDE 운영 기준

━━━━━━━━━━━━━━━━━━━━

문서번호: LBL-STD-004  
작성일: 2026-05-20  
적용범위: BIM 모델, 도면, 보고서, 회의록, 이슈, 납품자료 관리

## 목 차

1. CDE 운영 목적
2. 정보 상태 체계
3. 폴더 구조
4. 파일 명명 규칙
5. 권한 기준
6. 버전 및 승인 흐름
7. 이슈 관리
8. 보안 및 백업

## 1. CDE 운영 목적

CDE(Common Data Environment)는 프로젝트의 공식 정보 저장소다. 모든 참여자는 최신 승인본과 검토 중인 자료를 구분하여 사용해야 하며, 구두 전달이나 개인 저장소 기반의 자료 배포를 공식 정보로 간주하지 않는다.

## 2. 정보 상태 체계

| 상태 | 의미 | 사용 예 |
|---|---|---|
| WIP | 작성 중 자료 | 공종별 모델 작업본, 내부 검토본 |
| Shared | 참여자 검토용 공유 | 간섭 검토 모델, 회의자료 |
| Published | 승인 후 공식 배포 | 시공 배포 모델, 승인 도면 |
| Archived | 완료/보관 | 납품본, 종료 회차 보고서 |

## 3. 폴더 구조

```text
00_Admin
01_EIR_Contract
02_BEP_Standards
03_WIP
04_Shared
05_Published
06_Clash_QA
07_Quantity_Change
08_Meetings
09_Deliverables
99_Archive
```

## 4. 파일 명명 규칙

기본 형식:

```text
[Project]-[Discipline]-[Zone]-[DocumentType]-[Revision]-[YYYYMMDD]
```

예시:

```text
ICN-T1-MEP-L01-RVT-R02-20260520.rvt
ICN-T1-BIM-ALL-ClashReport-R05-20260520.pdf
ICN-T1-BIM-ALL-BEP-R01-20260520.docx
```

| 구성 | 설명 |
|---|---|
| Project | 프로젝트 약어 |
| Discipline | ARC/STR/MEP/MEC/ELE/FPS/COM/BIM 등 |
| Zone | 구역, 층, 공구 |
| DocumentType | RVT, IFC, NWD, Report, BEP 등 |
| Revision | R00, R01, R02 |
| Date | YYYYMMDD |

## 5. 권한 기준

| 역할 | WIP | Shared | Published | Archived |
|---|---|---|---|---|
| BIM PM | 전체 | 전체 | 승인/배포 | 전체 |
| BIM Modeler | 해당 공종 | 조회/업로드 | 조회 | 조회 |
| 시공사 | 조회 제한 | 조회/검토 | 조회/다운로드 | 조회 |
| 설계사 | 해당 자료 | 조회/검토 | 조회 | 조회 |
| 감리/CM | 조회 제한 | 조회/검토 | 조회/다운로드 | 조회 |
| 발주처 | 제한 | 필요 시 조회 | 조회/다운로드 | 조회 |

## 6. 버전 및 승인 흐름

| 단계 | 설명 | 결과 |
|---|---|---|
| 작성 | WIP에서 공종별 작업 | 내부 버전 |
| 내부 검토 | BIM PM/Coordinator 검토 | Shared 이동 |
| 외부 검토 | 시공사/설계사/CM 의견 수렴 | 이슈 등록 |
| 승인 | 승인권자 확인 | Published 이동 |
| 보관 | 회차 종료 또는 납품 완료 | Archived 이동 |

## 7. 이슈 관리

이슈는 다음 필드를 기준으로 관리한다.

| 필드 | 설명 |
|---|---|
| Issue ID | 고유 번호 |
| 제목 | 간단한 문제 설명 |
| 공종 | 관련 공종 |
| 위치 | 층/구역/좌표 |
| 우선순위 | High/Medium/Low |
| 책임자 | 조치 주체 |
| 조치기한 | YYYY-MM-DD |
| 상태 | Open/In Progress/Resolved/Closed |
| 근거 파일 | 모델, 도면, 보고서 링크 |

## 8. 보안 및 백업

- Published 및 Archived 자료는 삭제하지 않고 버전으로 보관한다.
- 보안 구역 모델, 장비 정보, 연락처 등 민감 정보는 접근 권한을 제한한다.
- 외부 공유 링크는 만료일과 다운로드 권한을 설정한다.
- 월 1회 이상 납품 예정 자료의 백업 상태를 점검한다.

