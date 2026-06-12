---
type: daily-knowledge-update
date: 2026-06-04
status: needs-review
source_grade: official-and-guidance
tags:
  - iso19650
  - cde
  - information-management
  - eir
  - bep
  - delivery-quality
---

# 2026-06-04 LUA BIM LABS ISO 19650 CDE Information Management Update

ISO 공식 페이지와 UK BIM Framework/IMI guidance 기준으로 LUA BIM LABS 계약, BEP/EIR 심사, CDE 운영, 납품검수에 필요한 정보관리 신호를 정리한다. 이 문서는 확정 계약 조항이 아니라 `needs-review` 기반 지식 업데이트이며, 프로젝트 적용 전 계약서, 발주처 EIR, 국내 발주 지침과 함께 검토한다.

## 공식·준공식 출처 기반 핵심 신호

| 출처 | 확인 신호 | LUA BIM LABS 운영 판정 |
|---|---|---|
| ISO 19650-1:2018 공식 페이지 | BIM을 활용한 정보관리의 개념·원칙을 다루며, 정보의 교환, 기록, 버전 관리, 조직화를 위한 프레임워크를 제공한다. 2024년에 확인되어 현행판으로 유지된다. | `PRI03 기준 병목`, 프로젝트 정보관리 기준으로 반영 |
| UK BIM Framework/IMI Framework | ISO 19650 series 기반 정보관리 구현 접근을 제공하며, 정보 요구사항, 표준, 방법, 절차, 기한, 프로토콜을 명확히 정의해야 한다고 설명한다. | `WKP03 기준 고정`, BEP/EIR 심사 체크리스트 보강 |
| UK BIM Framework Guidance Part 1 | 정보 요구사항과 납품, 기술·법무·계약 요구사항을 실무적으로 설명하고 CDE 내 정보 컨테이너 명명 기준을 다룬다. | `PRI02 납품 영향`, 파일명·상태·승인 기준 보강 |
| UK BIM Framework Guidance Part 2/4 | CDE 솔루션의 메타데이터 관리, Shared/Published 정보의 revision control, status allocation, status codes를 다룬다. | `PRI03 기준 병목`, CDE 상태 코드와 승인 워크플로우 정리 |
| buildingSMART IDS 1.0 | IDS는 ISO 19650 의도에 맞는 정보 요구사항 명세와 검토를 지원하는 경량 표준 접근이다. | `PRI07 승격 후보`, EIR 요구사항 자동 검증 후보 |

## LUA BIM LABS 반영 판단

### 1. ISO 19650은 모델링 기준보다 정보관리 프레임워크

ISO 19650-1은 BIM 모델 작성법 자체보다 정보의 교환, 기록, 버전 관리, 조직화를 위한 프레임워크다. LUA BIM LABS는 고객에게 "BIM 수행"을 제안할 때 Revit 모델링 범위뿐 아니라 정보 요구사항, CDE 상태, 승인·발행 절차, 납품 증빙을 함께 정의해야 한다.

판정:
- `FIX07 기준 분리`
- `PRI03 기준 병목`
- `WKP03 기준 고정`

다음 액션:
- 제안서와 SOW에 `정보관리 범위`를 모델링 범위와 분리해 기재
- BEP 템플릿에 정보 컨테이너, 상태 코드, 승인 책임자, 납품 증빙 필드 추가
- 다음 확인일: 2026-06-11

### 2. EIR은 Estimate가 아니라 Exchange Information Requirements로 정리

기존 자동 수집 문서 일부에서 EIR을 `Estimate Information Requirement`, `Estimate in Rough`, `Electronic Information Requirement`로 오기한 흔적이 있다. ISO 19650 맥락에서 LUA BIM LABS 운영 문서에는 `Exchange Information Requirements`로 정리하고, 과거 PAS/UK BIM Level 2 맥락의 Employer's Information Requirements와 혼용될 때는 기준일과 문맥을 남긴다.

판정:
- `FIX04 구조 재작성`
- `PRI05 링크 회복`
- `WKP06 중복 감소`

다음 액션:
- `BEP_수행계획서`, `EIRBEP_심사원`, `BIM_시방서`의 EIR 용어를 다음 감사 때 보정 후보로 등록
- 신규 문서에는 `Exchange Information Requirements`를 기본 용어로 사용
- 다음 확인일: 2026-06-11

### 3. CDE 운영은 폴더 구조보다 메타데이터·상태·승인 흐름

CDE는 단순 클라우드 폴더가 아니라 정보 컨테이너의 상태, revision, approval, metadata를 관리하는 운영 체계다. ACC/BIM360을 사용할 때도 WIP/Shared/Published/Archived 폴더명만 만드는 것으로는 부족하며, 어떤 상태가 고객 제출본인지, 어떤 revision이 계약 증빙인지, 누가 승인하는지를 BEP에 명시해야 한다.

판정:
- `FIX07 기준 분리`
- `PRI02 납품 영향`
- `WKP02 납품 연결`

다음 액션:
- `ACC_BIM360`에 CDE 상태·revision·승인 기준 추가
- 납품검수 결과표에 `CDE 상태`, `Revision`, `승인자`, `Published 일시` 필드 추가
- 다음 확인일: 2026-06-11

### 4. 정보 요구사항은 IDS/납품검수 자동화와 연결

정보 요구사항이 명확해야 IDS, ifctester, Model Quality Auditor 같은 자동 검증이 의미를 가진다. EIR/BEP가 모호하면 자동 검수 도구는 "없는 기준을 자동화"하게 된다.

판정:
- `FIX06 승격 이동`
- `PRI07 승격 후보`
- `WKP07 승격 실험`

다음 액션:
- 반복 파라미터 요구사항은 IDS 후보로 분리
- geometry/간섭/시공성은 자동 검증과 별도 수동 QA 기준으로 분리
- 다음 확인일: 2026-06-11

## Obsidian 연결

- [[EIR BEP_심사원 지식 베이스]]
- [[BEP 수행계획서 템플릿]]
- [[ACC BIM360 CDE 지식 베이스]]
- [[BIM 납품검수 지식 베이스]]
- [[IFC OpenBIM 지식 베이스]]
- [[지식업데이트]]
- [[지식큐레이터]]
- [[2026-06-04 Knowledge Update Queue]]
- [[2026-W23 Knowledge Curation Weekly Review]]

## 출처 URL

- ISO 19650-1:2018 official page: https://www.iso.org/standard/68078.html
- UK BIM Framework/IMI Framework about page: https://www.ukbimframework.org/about/
- Global BIM Network, ISO 19650 Guidance Part 1: https://globalbim.org/info-collection/information-management-according-to-bs-en-iso-19650-guidance-part-1-concepts/
- Global BIM Network, ISO 19650 Guidance Part 2: https://globalbim.org/info-collection/information-management-according-to-bs-en-iso-19650-guidance-part-2-processes-for-project-delivery/
- buildingSMART IDS 1.0 final standard: https://www.buildingsmart.org/information-delivery-specification-ids-v1-0-is-approved-as-a-final-standard/
