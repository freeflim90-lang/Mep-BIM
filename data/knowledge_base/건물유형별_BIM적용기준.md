# 건물 유형별 BIM 적용 기준 지식 베이스

## 2026-06-05 건물 유형별 BIM 특화 기준 AI 즉시 답변 패턴 보강
- Source: 국토교통부 BIM 기본지침, 한국 건설업계 BIM 현황(2025), 오피스·물류·학교 BIM 특화 기준
- Tags: building-type,office,logistics,school,sports,lod,mep,bim-special,2026

**AI 즉시 답변 패턴 — "오피스 건물과 물류센터의 BIM 차이가 뭔가요?"**
```
건물 유형별 BIM 핵심 차이:

오피스 (업무시설):
- 특징: 층별 반복 평면, 개방형 오피스 레이아웃 변경 잦음
- MEP 포인트: VAV 존별 공조, 랜덤 인테리어 대응 유연한 배관 경로
- BIM 활용: 인테리어 변경에 따른 MEP 수정 시뮬레이션

물류센터 (창고시설):
- 특징: 대공간·대형 랙 시스템, 차량 도입 출입
- MEP 포인트: 스프링클러 배치(높이 제한), 대용량 환기 (화물 오염 방지)
- BIM 활용: 랙 배치와 스프링클러 헤드 살수반경 시뮬레이션

학교 (교육시설):
- 특징: 교실 단위 반복, 방과후 에너지 절약 운전
- MEP 포인트: 교실별 환기 (CO₂ 기준), 냉난방 스케줄 제어
- BIM 활용: 교실 유형별 표준 MEP 패턴 Dynamo 자동 배치
```

**건물 유형별 BIM LOD 요건 비교:**
| 건물 유형 | 기본설계 LOD | 실시설계 LOD | MEP 특화 항목 |
|---------|-----------|-----------|------------|
| 오피스 | 300 | 350 | VAV·FCU 구역 설정 |
| 공동주택 | 300 | 350 | 세대 PS·난방배관 |
| 병원 | 300 | 400 | 의료가스·음압·차폐 |
| 데이터센터 | 350 | 400 | DLC·UPS·PDU |
| 물류센터 | 200 | 300 | 스프링클러·대공간 환기 |
| 학교 | 200 | 300 | 교실 환기·스케줄 제어 |
| 스포츠시설 | 200 | 300 | 관중석 공조·소방 |
| 공항 | 300 | 400 | BHS·탑승교·HVAC |

**LUA BIM LABS Add-in 건물 유형 자동 감지 로직 (개발 방향):**
```csharp
// Revit 프로젝트 정보에서 건물 용도 코드 읽기
string buildingType = doc.ProjectInformation
    .LookupParameter("BuildingType")?.AsString() ?? "Unknown";

// 건물 유형별 MEP 체크 규칙 자동 로드
var rules = BuildingTypeRuleFactory.GetRules(buildingType);
// → 병원: 의료가스 체크 추가 / 데이터센터: DLC 구역 체크 추가
```

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: building-type,bim,lod,parameter,residential,office,hospital,education,industrial,infrastructure
- 업데이트: 2026-06-05

건물 용도·형태에 따라 요구되는 BIM LOD 수준, 필수 파라미터, IFC Entity 매핑, 납품 체크리스트가 달라진다.
LUA BIM LABS Add-in은 건물 유형을 감지해 자동으로 적절한 검수 규칙·파라미터 템플릿을 불러오는 구조로 발전해야 한다.

---

## 건물유형별 BIM적용기준 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: building-type-bim,lod-matrix,ifc-mapping,parameter-template,fire-compartment,mep-density

---

### 1. 건물 유형 분류 체계

#### 1-1. 한국 건축법 용도 분류 (BIM 연계)

| 대분류 | 세분류 | BIM 핵심 이슈 | LUA Add-in 적용 포인트 |
|---|---|---|---|
| **공동주택** | 아파트·연립·다세대 | 세대 구획·방화·피난 | 세대별 면적 자동 산출, 발코니 연장 여부 |
| **제1·2종 근린생활시설** | 소매·음식점·사무소 | 용도별 점유 부하 | 스프링클러 헤드 자동 배치 |
| **업무시설** | 오피스·관공서 | 코어 효율·BAS 연동 | 면적 자동 분류 (임대/공용/기계) |
| **숙박시설** | 호텔·리조트·모텔 | 객실 단위 반복 패턴 | 패밀리 반복 배치 자동화 |
| **의료시설** | 종합병원·의원 | 감염 구획·의료 가스 | 의료 가스 ISO 7396 파라미터 |
| **교육연구시설** | 학교·학원·연구소 | 학생 밀도·피난 | 교실 면적·재실밀도 자동 체크 |
| **문화집회시설** | 공연장·전시장·경기장 | 장스팬 구조·피난 동선 | 비정형 지붕 LOD 300 처리 |
| **판매시설** | 백화점·대형마트 | 방화 셔터·비상구 | 방화구획 IFC 자동 생성 |
| **산업시설** | 공장·창고·물류센터 | 크레인 하중·환기 | 크레인 레일 BIM 가족 |
| **특수 구조물** | 초고층·지하·비정형 | 복합 구조 해석 | 층별 데이터 자동 집계 |

#### 1-2. 시설유형 독립 KB 확장 목록 (2026-05-28)

| 시설유형 | 독립 KB | Add-in 감지 키워드 | 핵심 자동 검수 |
|---|---|---|---|
| 학교·교육시설 | [[학교_교육시설_BIM]] | 학교, 교실, 체육관, 급식실, 과학실 | 학생 정원, 교실 면적, 피난거리, 채광·환기 |
| 공장·제조시설 | [[공장_제조시설_BIM]] | 공장, 생산라인, 크레인, 장비기초, 방폭 | 장비 하중, 유틸리티 접속점, 방폭 구역 |
| 물류센터·창고시설 | [[물류센터_창고시설_BIM]] | 물류센터, 창고, 랙, 도크, 컨베이어, WMS | 랙-스프링클러 간섭, 도크 치수, 저장 용량 |
| 스포츠시설·경기장 | [[스포츠시설_경기장_BIM]] | 경기장, 관람석, 좌석, 보미토리, 전광판 | 시야각, 관람객 피난, 방송·조명 위치 |
| 연구소·실험시설 | [[연구소_실험시설_BIM]] | 연구소, 실험실, 클린룸, 흄후드, 특수가스 | 압력 차, 배기량, 특수가스, 안전 설비 |
| 주차장·모빌리티시설 | [[주차장_모빌리티시설_BIM]] | 주차장, 램프, EV충전, 제트팬, LPR | 주차면, 차량 궤적, 유효 높이, 충전 용량 |

---

### 2. 건물 유형별 BIM 상세 기준

#### 2-1. 공동주택 (Apartment / Residential)

**BIM 필수 파라미터:**
```
세대 레벨:
- 세대 번호 (HouseholdNo): 동·층·호 (예: "101동 5층 501호")
- 전용면적 (ExclusiveArea_m2): 소수점 2자리
- 발코니 면적 (BalconyArea_m2): 연장 여부 구분
- 공급면적 (SupplyArea_m2): 전용 + 공용 지분
- 세대 유형 (UnitType): A형/B형 등

방화구획 레벨:
- 구획 번호 (FireCompartmentID)
- 구획 면적 (FireCompartmentArea_m2): 1,000m² 이하 체크
- 방화문 등급 (FireDoorRating): 60분/90분
```

**LOD 기준 (국내 공동주택):**
| LOD | 요구 사항 | 납품 단계 |
|---|---|---|
| LOD 200 | 세대 유형·층 구성, 공용 코어 형태 | 계획 설계 |
| LOD 300 | 세대 면적 확정, 구조 부재 단면, 방화구획 경계 | 기본 설계 |
| LOD 350 | MEP 주요 배관·덕트 경로, 세대 내 설비 위치 | 실시 설계 |
| LOD 400 | 공장 제작 정보 포함 (커튼월, PC 부재) | 시공 BIM |
| LOD 500 | As-Built 반영, FM 파라미터 완결 | 준공 납품 |

**IFC 매핑:**
- 세대 → `IfcSpace` (PredefinedType=SPACE, Name="세대번호")
- 방화문 → `IfcDoor` + `Pset_DoorCommon.FireRating`
- 방화구획 경계벽 → `IfcWall` + `Pset_WallCommon.FireRating`
- 발코니 → `IfcSlab` (PredefinedType=NOTDEFINED, IsExternal=True)

**공동주택 특유 함정:**
- 발코니 연장 서비스 면적은 전용면적 미포함 → 면적 산출 로직에 반드시 구분
- PIT 층·기계실 층은 `IfcBuildingStorey.Elevation` 오기입 빈번 → 층별 높이 자동 검증 필요
- 세대 Mirror(반전) 배치 시 문 개폐 방향·소방 감지기 위치 좌우 반전 확인

---

#### 2-2. 업무시설 / 오피스 (Office)

**BIM 필수 파라미터:**
```
공간 분류:
- 임대 면적 (RentableArea_m2): BOMA 2017 기준
- 공용 면적 (CommonArea_m2): 코어·로비·복도
- 부하율 (LoadFactor): 전용/임대 비율
- 층 효율 (FloorEfficiency): 임대/전체 비율 → 70% 이상 목표

BAS/에너지:
- 존 코드 (ZoneCode): HVAC 제어 존
- 조명 회로 (LightingCircuit)
- 에너지 소비 밀도 (EUI_kWh/m2/yr): 설계 목표값
```

**오피스 BIM 특화 이슈:**
- 커튼월(Curtain Wall): Revit 커튼월 시스템 → IFC Export 시 `IfcCurtainWall` 매핑 필수 확인
- 이중 바닥(Access Floor): 실 높이(CH) vs 구조 슬래브 높이 구분 파라미터
- 천장 공간(Plenum): 설비 배관·덕트 경로 확보 여부 — 최소 400mm 확보 기준
- 코어 배치: 내부/외부 코어에 따른 방화구획 경계 자동 판단

---

#### 2-3. 의료시설 (Hospital / Healthcare)

**BIM이 가장 복잡한 건물 유형** — 감염 제어, 의료 가스, 특수 전기, HVAC 압력 구분이 모두 BIM에 반영되어야 한다.

**필수 파라미터:**
```
공간 분류:
- 감염 구획 (InfectionZone): 일반/준오염/오염/청결 구역
- 청정도 등급 (CleanroomClass): ISO 5~8 (수술실 ISO 5)
- 기압 차 (PressureDifferential_Pa): 양압/음압 구분 (+8Pa / -8Pa)

의료 가스 (ISO 7396 기반):
- 산소 배관 (O2_Outlet): 콘센트 수량·위치
- 음압 흡인 (VAC_Outlet): 위치·유량(L/min)
- 의료 압축공기 (MedAir_Outlet): 4bar 기준
- 마취 가스 배기 (AGSS_Outlet): 수술실 전용

구조:
- 방사선 차폐 (RadiationShielding_mm): Pb 당량 두께 → 벽체 파라미터
- MRI실 자기장 차폐 (MRI_GaussLine): 5 Gauss 경계선 BIM 표시
```

**의료시설 BIM 설계 시 반드시 지켜야 할 순서:**
1. 기능 구획 (오염/청결 동선 분리) 확정 → 공간 경계 BIM 입력
2. 감염 제어 구획 승인 (병원 감염관리팀) → 이후 MEP 설계 진행
3. 의료 가스 배관 루팅 → 의료 가스 전문 시공사와 BIM 협업
4. 방사선실 차폐 → 방사선 전문가 계산서 BIM 파라미터 반영
5. MRI실 자기장 선 → Gausslin BIM 시각화 후 주변 설비 배치

---

#### 2-4. 교육시설 (Educational)

**필수 파라미터:**
```
- 교실 유형 (ClassroomType): 일반/실험/컴퓨터/체육
- 학생 정원 (Occupancy): 학생 수 → 피난 설계 근거
- 채광률 (DaylightFactor): 창면적/바닥면적 1/5 이상 (학교보건법)
- 소음 레벨 (NC Level): NC-30 기준 (교실)
```

**학교 BIM 특화 체크:**
- 장애인 접근: 경사로 기울기 1/18 이하, 점자블록 위치 BIM 확인
- 피난: 직통계단까지 보행 거리 30m 이하 자동 체크
- 채광: 교실 창 위치→일조 시뮬레이션 (학교보건법 기준)

---

#### 2-5. 초고층 건물 (High-rise / Super tall)

기준: 높이 200m 이상 (한국 건축법 기준 50층 이상 또는 200m 이상)

**BIM 고급 요구사항:**
```
구조:
- 풍하중 해석: CFD 시뮬레이션 결과 → BIM 부재 응력 파라미터 연동
- 전이층 (Transfer Floor): 코어-외벽 하중 전이 구조 BIM 정밀 모델링
- 피난안전구역 (Refuge Floor): 매 30층마다 피난안전구역 면적 자동 체크

MEP:
- 조닝(Zoning): 고층부/저층부 압력 분리 (Zone Valve, PRV 위치)
- 비상발전 용량: 전체 부하의 15% 이상 → BIM 파라미터 자동 집계
- 피난 경보 시스템: 초고층 전용 음성 경보 체계 (각 층 스피커 위치)

피난:
- 피난 동선 분석: 피난 시뮬레이션 소프트웨어(Pathfinder) 연동
- 특별 피난 계단: 부속실 가압 급기 설비 BIM 연동
```

**초고층 BIM 실무 함정:**
- 층고 누적 오차: 100층에서 1mm/층 오차 → 100mm 오프셋 발생 → 층별 실측 높이 파라미터 입력 필수
- 코어 시공 오차: 철골 커튼월과 코어 RC 공기 차이 → BIM 시공 단계별 모델 분리 관리
- 피난안전구역 면적 부족: 설계 초기에 BIM으로 자동 검증하지 않으면 실시 설계 후반에 발견 → 전면 재설계

---

#### 2-6. 물류센터 / 산업시설 (Logistics / Industrial)

**BIM 필수 파라미터:**
```
- 크레인 하중 (CraneTonnage_t): 레일 거더 BIM 파라미터
- 바닥 하중 (FloorLoad_kN/m2): 랙 하중·지게차 하중
- 천장 높이 (ClearHeight_m): 랙 최대 높이 결정
- 하역 도크 (LoadingDock): 위치·수량·유형(Leveler/Seal)
- 스프링클러 등급 (SprinklerHazard): OH1/OH2/EH1/EH2 (NFPA 13)
```

**물류센터 BIM 특화:**
- ASRS(자동창고 시스템): 랙 구조물 BIM → 실 하중 기반 슬래브 두께 자동 산정
- 온도 구역: 냉동/냉장/상온 구역 BIM 공간 분류 → 단열 두께 파라미터 자동 적용
- 지게차 동선: 교행 가능 폭 3.5m 이상 자동 체크

---

#### 2-7. 데이터센터 (Data Center)

급성장하는 건물 유형 — 전력·냉각·내진·보안이 BIM의 핵심 대상

**BIM 필수 파라미터:**
```
- 전력 밀도 (PowerDensity_kW/rack): 랙당 전력 → 냉각 용량 자동 산정
- PUE (Power Usage Effectiveness): 설계 목표 PUE → BIM 에너지 모델
- Tier 등급 (TierLevel): Tier I~IV (Uptime Institute) → 이중화 수준
- 내진 등급 (SeismicZone): 내진 특등급 (서버 장비 보호)
- 방수 구역 (FloodZone): 전기실·UPS실 지상층 배치 원칙
- 냉각 방식 (CoolingType): Air-cooled / Liquid-cooled / Immersion
```

---

### 3. 비정형 건물 (Non-orthogonal / Complex Geometry)

#### 3-1. BIM 모델링 전략

| 형태 유형 | Revit 접근법 | IFC Export 주의사항 |
|---|---|---|
| 자유 곡면 지붕 | Mass → Adaptive Component 또는 DirectShape API | IfcShellBasedSurfaceModel — 검수 도구 인식률 낮음 |
| 경사 커튼월 | Curtain Wall System + 사면체 패널 | IfcCurtainWall 매핑 수동 확인 필수 |
| 원형·타원형 평면 | Revit 원형 벽 제한 → RevitAPI Arc-based Wall | IfcWall 분절 가능성 |
| 파라메트릭 패사드 | Dynamo → Adaptive Component 생성 | 요소 수 폭발(10만+) → Navisworks 성능 저하 |

#### 3-2. 비정형 BIM 실무 전략
- Grasshopper/Rhino → Revit 변환: Speckle 또는 Rhino.Inside.Revit 활용
- LOD 설정 현실적 타협: 비정형 패사드는 LOD 300까지 (LOD 400은 제작 BIM 별도)
- IFC 품질 검증: 비정형 벽 단면 `IfcExtrudedAreaSolid` 대신 `IfcFacetedBrep` 생성 → Solibri 검증 규칙 예외 처리 필요

---

### 4. 건물 유형별 BIM 파라미터 자동 감지 전략 (Add-in 개발 방향)

LUA BIM LABS Add-in은 프로젝트 파일 열기 시 건물 유형을 자동 감지해 적절한 파라미터 템플릿을 제안해야 한다.

```python
# 건물 유형 감지 로직 (Dynamo Python 예시)
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, ProjectInfo

doc = IN[0]
proj_info = doc.ProjectInformation
building_type = proj_info.BuildingType  # Revit 내장 유형

# IFC Property Set 기반 매핑
type_to_template = {
    "Residential": "template_residential_ko.json",
    "Office": "template_office_ko.json",
    "Healthcare": "template_healthcare_ko.json",
    "Education": "template_education_ko.json",
    "Industrial": "template_industrial_ko.json",
}
OUT = type_to_template.get(str(building_type), "template_default_ko.json")
```

**국가별 템플릿 분기:**
```
template_{building_type}_{country_code}.json
예: template_residential_ko.json  → 한국 공동주택
    template_residential_jp.json  → 일본 공동주택 (建築基準法)
    template_residential_sg.json  → 싱가포르 주거 (BCA)
    template_office_us.json       → 미국 오피스 (IBC + BOMA)
```

---

### 5. 건물 유형별 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: building-type-failures,hospital-bim,highrise-bim,logistics-bim

**실패 1 — 의료시설 감염구획 BIM 미반영**: 설계 BIM에서 공간 오염도 구분 없이 MEP 루팅을 진행하면 감염관리실 리뷰 단계에서 덕트 경로 전면 재설계 지시를 받는다. 공조 덕트가 오염 구역 → 청결 구역을 관통하면 감염 경로가 된다. 해결: 설계 초기 공간 감염 등급(Zone: Clean/Contaminated/Semi)을 BIM Space 파라미터로 입력하고 MEP 루팅 시 Zone 경계 관통 자동 경고 규칙 적용.

**실패 2 — 초고층 피난안전구역 면적 부족**: 30층마다 피난안전구역을 배치해야 하는데 코어 효율 극대화 설계로 면적을 줄이다가 법정 면적(재실 인원 × 0.5m²) 미달 판정. 해결: BIM Space 파라미터에서 피난안전구역 면적과 해당 층 최대 재실 인원을 연계해 자동 산출·경고.

**실패 3 — 물류센터 스프링클러 등급 오류**: 창고 내 랙 높이 4m를 초과하는 ASRS 설치 후 스프링클러 등급 재산정이 필요한데 BIM 상 원래 설정(OH2)을 그대로 유지해 소방 준공 검사 반려. NFPA 13 기준 랙 높이 3.66m(12ft) 초과 시 in-rack sprinkler 추가 설치 요구. 해결: 창고 BIM Space에 랙 최대 높이 파라미터 입력 → 스프링클러 등급 자동 재산정 로직.

**실패 4 — 데이터센터 PUE 계산 BIM-실측 괴리**: BIM 에너지 모델에서 목표 PUE 1.4를 달성하도록 설계했으나 실제 운영 시 PUE 1.8 측정. 원인: 냉각탑 주변 기류 간섭(short-circuit) 미고려, IT 부하 실제 밀도(kW/rack)가 설계 가정보다 50% 높음. 해결: BIM 에너지 모델에 cold aisle/hot aisle 분리 실제 air flow 패턴 반영 + 랙 전력 밀도 10% 여유 설계 원칙.

**실패 5 — 비정형 지붕 IFC 납품 거절**: Revit DirectShape 기반 자유 곡면 지붕이 IFC Export 후 `IfcBuildingElementProxy`로 분류되어 납품 검수 소프트웨어(Solibri)에서 '지붕 없음' 판정. 해결: 비정형 지붕은 IFC Export 설정에서 DirectShape → `IfcRoof` 수동 매핑 설정 또는 API로 IfcRoof Entity 강제 지정. 납품 전 ifcopenshell로 `ifc.by_type("IfcRoof")` 건수 확인 필수.

### 6. 정형 건물 vs 비정형 건물 BIM 적용 고려사항 (2026-05-29)
- Source: claude-code-enhanced 2026-05-29
- Tags: 정형건물, 비정형건물, freeform, BIM적용기준, 공수가산

#### 정형 건물 (Orthogonal / Regular Form)

직교 좌표계 기반, 반복 층 구조가 지배적인 건물:
- 공동주택, 업무용 오피스, 학교, 공공청사, 물류창고 (일반형)

**BIM 특성:**
- 층 복사(Copy Level)·배열(Array) 활용 가능 → 공수 절감
- 표준 Revit 패밀리(벽/슬라브/창호)로 대부분 처리 가능
- Clash Detection: 코어 주변 MEP 집중 → 코어 구역 집중 검토

**주요 주의사항:**
- 반복 층이라도 설비 코어 클래시는 층마다 재확인 필요
- 지하층·옥상층은 비표준 → 별도 공수 산정

#### 비정형 건물 (Free-form / Complex Geometry)

곡면·경사·파라메트릭 형태가 구조·입면·지붕을 지배하는 건물:
- 공연장, 공항터미널, 랜드마크 오피스, 스타디움, 종교시설 (대형)

**BIM 특성:**
- Revit DirectShape, 개념 매스 기반 모델링 필요
- Grasshopper/Dynamo → Revit 임포트 워크플로우 필수
- IFC Export: 곡면 부재 → `IfcBuildingElementProxy` 강등 위험

**공수 가산 기준:**

| 비정형 수준 | 판단 기준 | 가산율 |
|-----------|---------|-------|
| 경미 (경사) | 단일 방향 경사 지붕·입면 | +10% |
| 중간 (복합경사) | 다방향 경사, 돔, 곡선 트러스 | +25% |
| 심화 (자유 곡면) | NURBS 기반 매스, 파라메트릭 패널 | +50% |
| 전면 비정형 | 전 부위 비정형, 파라메트릭 설계 전반 | +70% |

**비정형 건물 BIM 필수 체크리스트:**

```
□ 설계 소프트웨어 확인
  - [ ] Rhino/Grasshopper 파일 존재 여부
  - [ ] 파라메트릭 패널화 설계 포함 여부

□ 모델링 전략
  - [ ] DirectShape vs Native Revit 요소 사용 방침 결정
  - [ ] 패널 분할 기준 (개수, 허용 최대 크기) 명기

□ IFC 납품 기준
  - [ ] 버전: IFC 2x3 vs IFC 4 결정
  - [ ] 비정형 부재 Entity 매핑 목록 사전 협의
  - [ ] 납품 전 ifcopenshell 검증 스크립트 실행

□ 수량 산출 허용 오차
  - [ ] 곡면 면적 근사 계산 허용 오차율 ±X% 계약서 명기

□ 인력 역량
  - [ ] Dynamo 스크립트 작성 가능 인력 확인
  - [ ] Grasshopper 경험 보유 여부 확인
```

#### 건물 유형별 정형/비정형 분류표

| 건물 유형 | 구조 형태 | 입면 형태 | 분류 |
|---------|---------|---------|-----|
| 공동주택 | 정형 | 정형 | 정형 |
| 일반 오피스 | 정형 | 정형 | 정형 |
| 학교·공공청사 | 정형 | 정형~경미비정형 | 정형~경미 |
| 물류창고 | 정형 | 정형 | 정형 |
| 쇼핑몰 (일반형) | 정형 | 경미비정형 | 경미 |
| 스타디움 | 비정형 (트러스) | 비정형 | 심화 |
| 공연장 | 비정형 (음향 최적) | 비정형 | 심화~전면 |
| 공항터미널 | 비정형 | 비정형 | 심화~전면 |
| 랜드마크 타워 | 정형~비정형 | 비정형 커튼월 | 중간~심화 |
| 종교시설 (대형) | 비정형 (돔/아치) | 비정형 | 중간~심화 |

## 2026-06-06 건물유형별 BIM 적용기준 2026 법령·의무화 현황 업데이트
- Source: 국토부 BIM 시행지침 2022, 국가철도공단 BIM 로드맵, ZEB 의무화 고시(2024), 노후계획도시특별법 시행령(2026.4)
- Tags: BIM적용기준,ZEB,철도BIM,재건축BIM,공동주택,2025,2026

**2026 건물유형별 BIM 의무화 현황 및 적용 우선순위:**
| 건물 유형 | BIM 의무 근거 | 2026 현황 | MEP BIM 난이도 |
|---------|------------|---------|-------------|
| **공공청사·정부시설** | 국토부 500억+ 의무 | 전면 의무 시행 | 중간 (표준 계통) |
| **철도역사·철도시설** | 국가철도공단 500억+ | **2026 의무 신규 추가** | 높음 (HVAC·소방 복합) |
| **공동주택** (1기 신도시) | 노후계획도시특별법 2026.4 | 재건축 BIM 5단계 적용 | 중간~높음 |
| **ZEB 인증 건물** | 에너지절약설계기준 고시 | 공공 4등급·민간 5등급 의무 | 높음 (에너지 해석 연동) |
| **물류센터·창고** | NFPC 609(2024): 습식 스프링클러 | 화재안전성능기준 필수 반영 | 중간 (AMR 동선 추가) |
| 일반 민간 건물 | 권고 (2025 현재) | 의무 아님 (단, 발주처 요구 增) | 낮음~중간 |

**ZEB(제로에너지건물) 의무화 적용 건물유형별 BIM 파라미터 요건 (2026):**
- 공공 4등급 의무 (2025.1.1~): 에너지자립률 20% 이상
- 민간 5등급 의무 (2025.12.31~): 에너지자립률 10% 이상
- ZEB BIM 필수 파라미터:
  ```
  Pset_ZEBCompliance:
    - ZEB_Grade: 1~5 (등급)
    - Energy_Independence_Rate: % (에너지자립률)
    - BEMS_System: Yes/No (빌딩에너지관리시스템)
    - Renewable_Energy_Type: Solar/Geothermal/Wind/Combined
    - EUI_Target: kWh/㎡·년 (목표 에너지사용량 원단위)
    - EPI_Score: 에너지성능지표 점수
  ```
- 건물유형별 ZEB 달성 난이도: 공장·물류 (쉬움) → 주거 (중간) → 병원·데이터센터 (어려움)

**철도 BIM 2026 의무화 — 건물유형 특수 요건:**
- 국가철도공단: 2026년부터 500억원+ 신규 철도 프로젝트 BIM 필수
- 철도역사 MEP BIM 특수 파라미터:
  ```
  Pset_RailwayStation_MEP:
    - Platform_HVAC_Zone: 승강장/대합실/기계실 구분
    - Emergency_Ventilation_Mode: 화재시 연기 배출 모드
    - Station_Depth: 지하 심도 (m) — 심부역사 기준 적용 여부
    - GTX_Line: A/B/C (GTX 노선별 사양 차이 반영)
    - HITTS_Smart_Safety: Yes/No (터널 스마트 안전 시스템 연동)
  ```

**1기 신도시 재건축 BIM (노후계획도시특별법 2026.4 시행):**
- 대상: 분당·일산·평촌·산본·중동 (5개 신도시) 재건축 단지
- BIM 적용 단계: 기획설계(LOD 100) → 계획설계(LOD 200) → 실시설계(LOD 300) → 시공(LOD 350/400) → 준공(LOD 400+)
- MEP 특수 사항:
  - 기존 인프라(열병합·지역난방·단지 배전) 역설계 BIM 필요
  - 수직스택 배관(30층 이상): 슬리브 위치·압력 존 BIM 파라미터 필수
  - 단지 통합 BIM: 동별 모델 → 단지 Federated Model → ACC/CDE 통합

**건물유형별 MEP BIM 복잡도 분류표 (2026 업데이트):**
| 복잡도 | 건물 유형 | 특수 MEP 요소 | BIM 추가 작업 시간 추정 |
|------|---------|------------|-------------------|
| **최고** | 반도체 팹·AI팩토리 | 드라이룸·초고압 전원·UPS | 설계 인력의 +150% |
| **최고** | 바이오/GMP 시설 | 클린룸 압력 캐스케이드·HVAC 이중화 | +120% |
| **높음** | 데이터센터 | 60~80kW/rack 냉각·N+1 이중화 | +80% |
| **높음** | 병원·의료시설 | 음압병실·RTLS·로봇 동선 | +70% |
| **높음** | 철도역사 | 비상환기·심부 압력·GTX 특수사양 | +60% |
| **중간** | 오피스·공동주택 | ZEB 파라미터·지역난방 | +30~40% |
| **낮음** | 물류·공장(일반) | 습식 스프링클러·AMR 동선 | +20% |

- 관련: [[국가별_건설법규_기준비교]] · [[IFC_OpenBIM]] · [[OpenBIM_프로그램연동]] · [[BIM_납품검수]] · [[BIM_지침서]] · [[BIM_등급별_투입일_기준표]] · [[건물유형_공사구분_산정로직]] · [[해외건설기업_동향분석]]
