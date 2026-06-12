---
type: daily-knowledge-update
date: 2026-06-04
status: needs-review
source_grade: official
tags:
  - openbim
  - ifc
  - ids
  - bcf
  - delivery-quality
---

# 2026-06-04 LUA BIM LABS OpenBIM IDS BCF Update

buildingSMART 공식 문서 기준으로 LUA BIM LABS 납품검수, Model Quality Auditor, OpenBIM 교육에 필요한 IFC/IDS/BCF 신호를 정리한다. 이 문서는 확정 제품 사양이 아니라 `needs-review` 기반 지식 업데이트이며, 프로젝트 적용 전 발주처 EIR/BEP 기준과 사용 소프트웨어 지원 여부를 확인한다.

## 공식 출처 기반 핵심 신호

| 출처 | 공식 신호 | LUA BIM LABS 운영 판정 |
|---|---|---|
| buildingSMART IDS 공식 페이지 | IDS는 컴퓨터가 해석 가능한 정보 요구사항 정의 표준이며, IFC 모델의 자동 적합성 검토에 쓰인다. IDS 1.0 이전 버전은 공식 표준이 아니다. | `PRI02 납품 영향`, IDS 1.0 기준으로 검수 룰 후보 관리 |
| buildingSMART IDS 1.0 final standard 발표 | IDS 1.0은 2024-06-01 승인되어 공식 buildingSMART 표준이 됐다. | `PRI03 기준 병목`, EIR/BEP 요구사항을 IDS로 전환하는 기준 노트 필요 |
| buildingSMART BCF 공식 페이지 | BCF는 IFC 기반 모델 이슈와 토픽을 파일 기반 `.bcfzip` 또는 RESTful 서비스 방식으로 교환한다. | `PRI02 납품 영향`, 검수 이슈 추적·재검수 루프 후보 |
| buildingSMART IFC 4.3 ISO 승인 | IFC 4.3은 ISO 16739 표준 최신 축으로 인프라 영역 확장을 포함한다. | `PRI04 재검증 예약`, 건축/MEP 실무 적용은 수신 소프트웨어 지원 확인 필요 |
| buildingSMART IFC 표준 페이지 | 최신 공식 IFC 버전과 스키마 문서를 기준으로 버전·지원 범위를 확인한다. | `PRI04 재검증 예약`, 프로젝트별 IFC 버전 선택 기준 관리 |

## LUA BIM LABS 반영 판단

### 1. IDS는 납품 요구사항 자동 검증의 기준 후보

IDS는 발주처가 요구하는 객체, 분류, 재료, 속성, 값 요구사항을 IFC 모델에서 자동 검토할 수 있게 만드는 표준이다. LUA BIM LABS는 EIR/BEP의 파라미터 요구사항을 Excel이나 PDF 체크리스트로만 관리하지 말고, 반복 검수 항목은 IDS 1.0 파일 후보로 분리한다.

판정:
- `FIX07 기준 분리`
- `PRI03 기준 병목`
- `WKP03 기준 고정`

주의:
- IDS는 정보 요구사항 검증에 적합하지만 geometry 검토 전체를 대체하지 않는다.
- 형상, 간섭, 시공성, MEP 연결성은 Navisworks/Revit QA/수동 샘플링 검토와 함께 운영한다.

다음 액션:
- `BIM_납품검수`의 필수 파라미터 검수 항목을 IDS 후보와 수동 검토 항목으로 분리
- `Model Quality Auditor` 백로그에 IDS 1.0 샘플 검증 PoC 추가
- 다음 확인일: 2026-06-11

### 2. BCF는 검수 이슈의 추적 언어

BCF는 모델 기반 이슈를 다른 BIM 애플리케이션 사이에서 주고받기 위한 openBIM 표준이다. LUA BIM LABS 납품검수에서는 검수 실패 항목을 구두/이메일로만 처리하지 않고, BCF 이슈 또는 BCF 호환 이슈 구조로 남기는 것이 재검수와 고객 커뮤니케이션에 유리하다.

판정:
- `FIX06 승격 이동`
- `PRI02 납품 영향`
- `WKP02 납품 연결`

다음 액션:
- 납품검수 결과표에 `BCF 이슈 ID`, `상태`, `담당`, `재검수일` 필드 추가
- Navisworks/ACC 이슈와 BCF 파일 기반 교환 가능성 분리
- 다음 확인일: 2026-06-11

### 3. IFC 4.3은 최신 표준이지만 무조건 적용 대상은 아님

buildingSMART는 IFC 4.3을 ISO 16739 최신 축으로 제시하지만, LUA BIM LABS의 건축/MEP 납품에서는 발주처와 수신 소프트웨어 지원 여부가 먼저다. IFC 4.3은 도로·철도·교량 등 인프라 프로젝트에서는 후보가 될 수 있으나, 일반 건축/MEP 프로젝트에서는 IFC 2x3 또는 IFC 4 요구가 여전히 우세할 수 있다.

판정:
- `FIX03 출처 재검증`
- `PRI04 재검증 예약`
- `WKP04 재검증 예약`

다음 액션:
- 프로젝트 착수 체크리스트에 `요구 IFC 버전`, `수신 소프트웨어`, `검증 도구`, `좌표 기준`을 필수 필드로 추가
- 다음 확인일: 2026-06-11

## Obsidian 연결

- [[IFC OpenBIM 지식 베이스]]
- [[BIM 납품검수 지식 베이스]]
- [[QA_테스터]]
- [[ACC BIM360 CDE 지식 베이스]]
- [[지식업데이트]]
- [[지식큐레이터]]
- [[2026-06-04 Knowledge Update Queue]]
- [[2026-W23 Knowledge Curation Weekly Review]]

## 공식 출처 URL

- buildingSMART IDS: https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/
- buildingSMART IDS 1.0 final standard: https://www.buildingsmart.org/information-delivery-specification-ids-v1-0-is-approved-as-a-final-standard/
- buildingSMART BCF: https://technical.buildingsmart.org/standards/bcf/
- buildingSMART IFC 4.3 ISO approval: https://www.buildingsmart.org/ifc-4-3-formally-approved-and-published-as-an-iso-standard/
- buildingSMART IFC schema specifications: https://technical.buildingsmart.org/standards/ifc/ifc-schema-specifications/
