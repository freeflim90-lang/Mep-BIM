# IFC/OpenBIM 지식 베이스

## 2026-06-05 buildingSMART Korea 및 IFC 5.0 최신 동향 보강
- Source: buildingSMART International, buildingSMART Korea, BibLus
- Tags: ifc5,openbim,buildingsmart-korea,certification,iot,digitaltwin,2026

**IFC 5.0 주요 방향 (Draft 단계, 2026 기준):**
- IoT·센서 데이터 연동: `IfcSensor`, `IfcDistributionSensorElement` 확장 → 실시간 BAS 데이터와 IFC 모델 연결
- 디지털트윈 지원: 운영 단계 동적 데이터(에너지·환경·구조 모니터링) IFC 레이어로 표현
- 도시 스케일: IFC와 CityGML/LandXML 연계 → 도시 단위 디지털트윈
- AI/ML 통합: 모델 기반 예측 유지보수 데이터 링크 표준화
- 운영 주의: IFC 5.0은 2026년 현재 Draft 수준. 실무 납품은 IFC 4 Coordination View 2.0 또는 IFC 4.3(토목) 사용 권고

**buildingSMART 소프트웨어 인증 프로그램:**
- 인증 등급: Bronze(기본 IFC R/W) → Silver(상세 MVD 지원) → Gold(완전 구현)
- 인증 확인: technical.buildingsmart.org/certification 에서 소프트웨어별 IFC 버전·등급 확인
- 국내 주요 인증 소프트웨어: Revit, ArchiCAD, Solibri, Navisworks, BricsCAD, Tekla Structures
- buildingSMART Korea: www.buildingsmart.or.kr — 국내 공공 BIM 지침·인증 교육 제공

**국내 OpenBIM 의무화 연계 현황:**
- 국토부 BIM 시행지침: IFC 기반 납품 권고 (IFC 2x3 TC1 또는 IFC 4)
- 조달청: BIM 성과품에 IFC 파일 필수 포함
- buildingSMART Korea의 IFC 검증 서비스 활용 권고 (납품 전 품질 확인)
- LH공사, SH공사 등 공공발주처: 자체 BIM 지침에서 IFC 납품 버전 명시

**IFC Export 버전 선택 가이드 (2026 실무 기준):**
| 프로젝트 유형 | 권장 IFC 버전 | 근거 |
|--------------|--------------|------|
| 건축·MEP 일반 | IFC 4 Coordination View 2.0 | 수신 소프트웨어 지원 안정 |
| 토목·도로·철도 | IFC 4.3 | IfcAlignment·IfcBridge 지원 |
| COBie FM 연동 | IFC 4 Design Transfer View | COBie 파라미터 Export 최적화 |
| 레거시 발주처 요구 | IFC 2x3 TC1 | 구형 소프트웨어 호환성 |

**openBIM Hackathon Porto 2026:**
- buildingSMART International 주관 — IFC/IDS 기반 개방형 협업 도구 개발 대회
- 한국 BIM 스타트업의 글로벌 OpenBIM 생태계 진입 기회

관련: [[BIM 납품검수 지식 베이스]] · [[ACC BIM360 CDE 지식 베이스]] · [[FM 시설관리 자산관리 BIM 지식 베이스]]

## IFC 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: ifc,openbim,buildingsmart,iso16739,data-exchange,cde

IFC(Industry Foundation Classes)는 buildingSMART International이 관리하는 개방형 BIM 데이터 교환 표준.
ISO 16739 국제 표준, KS X ISO 16739 국내 채택. 중립 포맷으로 소프트웨어 의존성 제거.

**IFC 버전 이력:**
- IFC 2×3: 현재 가장 널리 사용 (Revit 기본값), 대부분 BIM 소프트웨어 지원
- IFC 4: 건축/구조/MEP 개선, 선형 인프라 일부 지원
- IFC 4.3: 교량·도로·철도·항만 인프라 공식 지원, 2023 ISO 16739-1:2024 등록
- IFC 5.0 Draft: 센서·IoT·디지털트윈 연동 준비 중

## IFC/OpenBIM Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: ifc,ifc4.3,ids,mvd,openbim,buildingsmart,revit-export,python-ifcopenshell

**IFC 4.3 주요 변경사항 (국토부 CIM 연계):**
- IfcAlignment: 도로·철도 수평/수직 선형 표현 (Civil 3D Corridor → IFC 변환 가능)
- IfcGeotechnicalElement: 지반 조사 데이터 (시추공·지층 경계)
- IfcBridge: 교량 전용 객체 분류
- MEP: IfcDistributionSystem 세분화 (HVAC/Electrical/Plumbing/FireProtection 독립 분류)

**IDS(Information Delivery Specification) 1.0:**
- XML 기반 납품 요구사항 정의 파일 — 발주처가 "어떤 파라미터가 필수인지" 기계 검증 가능
- 예: `<Entity name="IfcFlowTerminal"><Property name="Manufacturer" minOccurs="1"/></Entity>`
- buildingSMART IDS 검증기: 오픈소스 Python 라이브러리 `ifctester`
- 국토부 BIM 업무지침: IDS 기반 납품 검수 도입 예고 (2026~)

**Revit IFC Export 설정 (최적화):**
- IFC Version: IFC 4 (Coordination View 2.0) 또는 IFC 4 Design Transfer View
- Export Base Quantities: ✅ (면적·체적 COBie 연동)
- Split Walls and Columns by Level: ✅ (층별 독립 객체)
- IFC Property Sets: 공유 파라미터 → IfcPropertySet 자동 매핑
- 주의: Curtain Wall → IfcCurtainWall 매핑 확인 (기본값 IfcWall로 잘못 내보내는 경우 있음)

**ifcopenshell Python 활용:**
```python
import ifcopenshell
ifc = ifcopenshell.open("project.ifc")
# MEP 기기 전체 조회
for product in ifc.by_type("IfcFlowTerminal"):
    psets = ifcopenshell.util.element.get_psets(product)
    manufacturer = psets.get("Pset_ManufacturerTypeInformation", {}).get("Manufacturer")
    print(product.Name, manufacturer)
```
- 관련: [[BIM_지침서]] · [[BIM_납품검수]] · [[ACC_BIM360]] · [[엔지니어링계산서]]

## IFC 실전 활용 심화: 공종별 매핑과 트러블슈팅 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: ifc,entity-mapping,troubleshooting,revit-export,ifcopenshell,quality

**공종별 IFC Entity 매핑 기준표:**
| Revit 카테고리 | IFC Entity | 비고 |
|---|---|---|
| 벽 (Walls) | IfcWall / IfcWallStandardCase | 커튼월은 IfcCurtainWall |
| 바닥 (Floors) | IfcSlab (FLOOR) | 지붕은 IfcRoof |
| 기둥 (Columns) | IfcColumn | 구조기둥 IfcStructuralCurve |
| 보 (Beams) | IfcBeam | IfcMember (경량 구조) |
| 덕트 (Ducts) | IfcDuctSegment | 피팅: IfcDuctFitting |
| 배관 (Pipes) | IfcPipeSegment | 피팅: IfcPipeFitting |
| 공조기기 | IfcFlowTerminal | AHU: IfcAirTerminalBox |
| 전기기기 | IfcElectricDistributionBoard | 분전반·MCC |
| 스프링클러 | IfcFireSuppressionTerminal | 헤드·밸브류 |
| 공간 | IfcSpace | Revit Room → IfcSpace |

**IFC Export 품질 검증 체크포인트:**
- [ ] `IfcProject` 1개만 존재 (중복 시 병합 오류 발생)
- [ ] `IfcSite`·`IfcBuilding`·`IfcBuildingStorey` 계층 완전 (누락 시 FM 연동 불가)
- [ ] 모든 IfcProduct에 `GlobalId` (GUID) 고유값 (재익스포트 시 GUID 변경 여부 확인)
- [ ] PSet_Revit* 자동 생성 PSet 外 사용자 정의 PSet 존재 여부
- [ ] 좌표: `IfcLocalPlacement` vs `IfcGeometricRepresentationContext` 일치

**ifcopenshell로 IFC 품질 검증 자동화:**
```python
import ifcopenshell, collections

ifc = ifcopenshell.open("project.ifc")
# 1. 고아 IfcSpace 탐지 (BuildingStorey 미배정)
spaces = ifc.by_type("IfcSpace")
orphan = [s for s in spaces if not ifcopenshell.util.element.get_container(s)]
print(f"고아 IfcSpace: {len(orphan)}개")

# 2. PSet 입력률 체크
required = ["Manufacturer","ModelNumber"]
missing = [e.Name for e in ifc.by_type("IfcFlowTerminal")
           if not all(ifcopenshell.util.element.get_psets(e)
           .get("Pset_ManufacturerTypeInformation",{}).get(p) for p in required)]
print(f"필수 파라미터 누락 기기: {len(missing)}개")
```
- 관련: [[OpenBIM_프로그램연동]] · [[BIM_납품검수]] · [[ACC_BIM360]] · [[Revit_Addin]]


## 2026-06-04 buildingSMART 공식 OpenBIM 표준 업데이트
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_OPENBIM_IDS_BCF_UPDATE.md`
- Tags: ifc,openbim,ids,bcf,buildingsmart,official-source

buildingSMART 공식 문서 기준으로 IDS 1.0은 공식 표준이며, IFC 모델의 정보 요구사항을 컴퓨터가 해석 가능한 방식으로 정의하고 자동 적합성 검토에 활용한다. IDS 1.0 이전 버전은 공식 표준으로 보지 않는다.

운영 판단:
- EIR/BEP의 반복 파라미터 요구사항은 IDS 1.0 후보로 분리한다.
- IDS는 속성, 값, 분류, 재료 등 정보 요구사항 검증에 적합하지만 geometry, 간섭, 시공성, MEP 연결성 검토 전체를 대체하지 않는다.
- BCF는 검수 이슈를 `.bcfzip` 또는 RESTful 서비스 방식으로 추적하는 openBIM 이슈 언어로 본다.
- IFC 4.3은 최신 ISO 축이지만 건축/MEP 납품에서는 발주처 요구 버전과 수신 소프트웨어 지원 여부를 먼저 확인한다.

다음 액션:
- `BIM_납품검수`의 자동 검수 항목을 IDS 후보, BCF 이슈, 수동 샘플링 검토로 분리한다.
- `QA_테스터`에 IDS 통과 후에도 실무 부적합을 찾는 보완 검토 항목을 연결한다.
- 다음 확인일: 2026-06-11

관련: [[BIM 납품검수 지식 베이스]] · [[QA_테스터]] · [[ACC BIM360 CDE 지식 베이스]] · [[2026-06-04 LUA BIM LABS OpenBIM IDS BCF Update]]

## IFC/OpenBIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: IFC4.3소프트웨어미지원, IDS검증실패, GUID재익스포트, FM연동, 2026현황

**IFC 4.3 실제 사용 시 소프트웨어 미지원 문제(2026 현황)**: IFC 4.3은 2023년 ISO 16739-1:2024로 공식 등록되었으나, 2026년 현재 대부분의 BIM 소프트웨어는 IFC 4.3을 아직 부분 지원 또는 미지원 상태다. Revit 2025는 IFC 4.3 내보내기를 실험적으로 지원하지만 IfcAlignment(도로·철도 선형) 및 IfcBridge(교량) 객체 내보내기는 Civil 3D와의 연동에서만 정상 작동. Navisworks 2025는 IFC 4.3 읽기를 지원하나 IfcGeotechnicalElement 시각화가 미완성. Solibri 9.13 이상에서 IFC 4.3 규칙 검증 지원. 실무 권고: 건축·MEP 프로젝트는 IFC 4 Coordination View 2.0을 유지하고, 토목 인프라 프로젝트에서만 IFC 4.3을 사용하되 수신 소프트웨어의 지원 여부를 착수 전에 반드시 확인.

**IDS 1.0 검증에서 자주 실패하는 패턴**: IDS(Information Delivery Specification) 검증을 `ifctester` 라이브러리로 실행할 때 실무에서 반복되는 실패 패턴 3가지. ① 엔티티 조건 vs 파라미터 조건 불일치 — IDS에서 `IfcFlowTerminal`에 `Manufacturer` 필수 조건을 걸었는데, 실제 IFC에서 해당 기기가 `IfcMechanicalFastener`로 잘못 매핑된 경우 조건이 적용되지 않아 누락 기기가 검증에서 통과된 것처럼 보임. ② PSet 조건의 대소문자 민감도 — IDS에서 `Pset_ManufacturerTypeInformation`으로 정의했는데 IFC 파일에 `PSET_ManufacturerTypeInformation`으로 저장된 경우 실패. ③ 옵셔널 파라미터의 존재 조건 — `minOccurs="0"` 조건의 파라미터가 IDS 파일에서 누락 선언되면 ifctester가 해당 파라미터를 선택사항으로 처리하지 않고 필수로 처리하는 버그(ifctester v0.5 이하에서 확인됨).

**IFC GUID가 재익스포트마다 바뀌는 문제(FM 연동 중단) 해결법**: Revit에서 IFC를 재익스포트할 때 `IfcProduct`의 `GlobalId`(GUID)가 변경되면 FM 시스템(Autodesk Tandem, Archibus 등)에서 해당 자산의 이력 데이터와 연결이 끊긴다. 원인: Revit의 IFC GUID는 기본적으로 Revit ElementId에서 결정론적으로 생성되지만, 요소가 삭제 후 재생성된 경우(예: 패밀리 교체), 링크 모델 요소, 또는 IFC Export 플러그인 버전 차이로 인해 GUID가 변경될 수 있다. 해결법: ① `IFC GUID` 공유 파라미터를 Revit 요소에 명시적으로 저장하는 Add-in을 활용 — 최초 익스포트 시 GUID를 파라미터에 기록하고 이후 익스포트에서 저장된 GUID를 강제 사용. ② ifcopenshell로 두 버전의 IFC를 비교하여 GUID 변경된 요소 목록 자동 추출 후 FM 시스템에 매핑 업데이트 적용. ③ FM 연동이 중요한 장비(공조기, 펌프, 발전기)는 `IfcProduct.Name` + 제조사 시리얼번호 조합으로 보조 식별자를 IDS에 필수 조건으로 추가하여 GUID 변경 시에도 자산 매칭 가능하도록 설계.

## 2026-06-06 Revit 2027 IFC 개선·IDS+BCF 3.0 실무 워크플로우·IFC 5.0 Draft 보강
- Source: Autodesk Revit 2027 릴리즈 노트, buildingSMART BCF 3.0 API 문서, buildingSMART IFC 5.0 로드맵
- Tags: revit2027,ifc-export,ids,bcf3.0,ifc5.0,2026,practical-workflow

**Revit 2027 IFC 개선 사항 (2026-04-07 출시):**
- IFC 4.3 내보내기 안정성 개선: IfcAlignment(선형) 내보내기 오류 수정
- Autodesk Forma Connected Client → IFC 파일 Forma 클라우드 직접 업로드 가능 (Revit 2027~)
- IFC Open 개선: IFC 4.3 파일 열기 시 MEP 객체 자동 범주 매핑 정확도 향상
- Carbon Parameters (EC3 연동): IFC 내보내기 시 `Pset_EnvironmentalImpact` 자동 포함 옵션 추가
- 주의: Revit 2027 IFC 내보내기 플러그인(IFC for Revit)과 기본 내장 내보내기 통합 — 별도 플러그인 설치 불필요

**IDS + BCF 3.0 실무 워크플로우 (2026 권장 프로세스):**
```
[발주처] IDS 파일 작성 (.ids XML)
    → BIM 요건 정의: 어떤 객체에 어떤 파라미터가 필수인지 명시
    ↓
[설계사] Revit에서 IFC 내보내기
    → ifctester (Python) 또는 Solibri 9.13+로 IDS 자동 검증
    → 실패 요소: BCF 3.0 이슈 파일(.bcfzip) 자동 생성
    ↓
[BIM 관리자] BCF 3.0 이슈 검토
    → BCF REST API (buildingSMART BCF 3.0 API)로 Jira/Asana 자동 연동
    → 이슈 상태 추적: Open → In Progress → Resolved
    ↓
[검수] 재검증 IDS 통과 → 납품 승인
```
- BCF 3.0 주요 변경: REST API 표준화, 비디오 클립 첨부 지원, 뷰포인트에 단면 클리핑 정보 포함
- 무료 IDS 도구: `ifctester` (Python, buildingSMART 공식), `IDS Audit` (Solibri 플러그인)
- BCF 3.0 호환 소프트웨어 (2026 기준): Solibri, Revit (내장), Navisworks 2026+, BIMcollab

**IFC 5.0 Draft 현황 (2025~2026):**
- IFC 5.0 표준: buildingSMART International 개발 중 (2026년 현재 Draft 단계)
- 주요 변경 예상:
  | 항목 | IFC 4.x | IFC 5.0 Draft |
  |------|---------|-------------|
  | 기하 표현 | BREP/CSG/SweptSolid | Tessellation 표준화 + STEP AP242 통합 |
  | 프로젝트 구조 | IfcProject > IfcSite | 다중 사이트 지원 확장 |
  | 인프라 | IFC 4.3 일부 | IfcFacility 계층 완전 통합 |
  | 디지털트윈 | 미지원 | IoT 센서 시계열 데이터 참조 스펙 포함 |
- 실무 영향: 2026~2028년은 IFC 4.x 과도기 → IFC 5.0 채택은 2029년 이후 예상

- 관련: [[OpenBIM_프로그램연동]] · [[BIM_납품검수]] · [[ACC_BIM360]] · [[Revit_Addin]] · [[FM_자산관리]]
