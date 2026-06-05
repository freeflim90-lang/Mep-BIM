# 학교·교육시설 BIM 적용 기준 지식 베이스

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #학교BIM #교육시설 #교실모듈 #피난 #채광 #실내공기질 #급식실 #체육관 #특수교실
- 업데이트: 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

학교·교육시설은 학생 안전, 피난, 채광·환기, 실별 정원, 유지관리성이 핵심인 반복 모듈형 공공 시설이다. 일반 건물보다 교실 단위 면적·수용인원·교육과정별 특수실 요구사항이 BIM 검수 로직에 직접 들어간다.

| 구분 | 일반 건물 | 학교·교육시설 |
|---|---|---|
| 공간 기준 | 임대·업무 효율 | 학급 수, 학생 수, 교실 모듈 |
| 안전 | 일반 피난 | 저연령 사용자 피난, 방화문 상시 개방 관리 |
| 환경 | 일반 공조 | 채광, CO2, 소음, 온열환경, 미세먼지 |
| 특수 공간 | 회의실 중심 | 과학실, 컴퓨터실, 음악실, 급식실, 체육관 |
| 운영 | 일반 FM | 학사 일정·방과후·지역 개방 시설 관리 |

---

## 2. BIM 필수 파라미터 목록

### 2.1 공간·학급 파라미터

```
Pset_EducationSpace
  - School_Level: Kindergarten / Elementary / Middle / High / University / Special
  - Classroom_Type: General / Science / Computer / Music / Art / Library / Gym / Cafeteria
  - Grade_Group: 학년 또는 과정
  - Class_ID: 학급 식별 번호
  - Student_Capacity: 설계 학생 정원
  - Teacher_Capacity: 교직원 정원
  - Net_Classroom_Area: 순 교실 면적 (m2)
  - Area_Per_Student: 학생 1인당 면적 (m2/person)
  - Furniture_Layout_Type: 일반 / 모둠 / 강의식 / 실험대형
  - Flexible_Classroom: 가변형 교실 여부
```

### 2.2 안전·환경 파라미터

| 파라미터명 | 데이터 타입 | 단위 | 설명 |
|---|---|---|---|
| Occupant_Load_Student | IfcCountMeasure | 명 | 학생 피난 산정 인원 |
| Evacuation_Route_ID | IfcLabel | - | 피난 동선 ID |
| Stair_Travel_Distance | IfcLengthMeasure | m | 직통계단까지 보행거리 |
| Daylight_Factor | IfcRatioMeasure | % | 채광 성능 |
| Window_To_Floor_Ratio | IfcRatioMeasure | % | 창면적/바닥면적 |
| CO2_Design_Level | IfcPositiveRatioMeasure | ppm | 실내 CO2 설계 기준 |
| Acoustic_NC_Level | IfcLabel | NC | 교실·음악실 소음 기준 |
| Playground_Area | IfcAreaMeasure | m2 | 운동장 또는 외부활동 면적 |
| BarrierFree_Route | IfcBoolean | - | 무장애 이동 동선 여부 |

### 2.3 급식실·과학실 특수 파라미터

```
Pset_SchoolSpecialRoom
  - Lab_Gas_Type: LPG / LNG / None
  - FumeHood_Required: 흄후드 필요 여부
  - Chemical_Storage_Class: 산/염기/인화성/일반
  - Cafeteria_Capacity: 급식 동시 수용 인원
  - Kitchen_Hood_ID: 주방 후드 ID
  - Grease_Duct_Route: 기름덕트 경로 ID
  - Food_Waste_Room: 음식물 처리실 연계 여부
  - SlipResistant_Floor: 미끄럼 방지 바닥 여부
```

---

## 3. LOD 단계별 요구사항

| LOD | 학교·교육시설 적용 내용 |
|---|---|
| LOD 100 | 학생 수, 학급 수, 교사동·체육관·급식동 매스 |
| LOD 200 | 교실 모듈, 코어, 피난계단, 운동장·차량 동선 개략 |
| LOD 300 | 교실·특별실 공간 확정, 방화구획, 급식실 MEP, 장애인 동선 |
| LOD 350 | 과학실 가스·배기, 주방 후드·기름덕트, 체육관 장스팬 간섭 검토 |
| LOD 400 | 교실 가구·실험대·주방 장비·체육관 장비 상세 |
| LOD 500 | As-Built + 교육시설 유지관리, 실별 자산·점검 속성 |

---

## 4. IFC Entity 매핑

| 요소 | IFC Entity | 비고 |
|---|---|---|
| 일반 교실 | IfcSpace | Class_ID, Student_Capacity 필수 |
| 과학실 | IfcSpace + Pset_SchoolSpecialRoom | 가스·배기 속성 |
| 급식실 | IfcSpace | Cafeteria_Capacity |
| 주방 후드 | IfcFlowTerminal 또는 IfcBuildingElementProxy | 배기 계통 연계 |
| 체육관 | IfcSpace | 장스팬 구조·피난 인원 |
| 교실 가구 | IfcFurniture | 배치 유형 |
| 운동장 | IfcSite 또는 IfcSpace(External) | 외부활동 면적 |
| 방화문 | IfcDoor + Pset_DoorCommon.FireRating | 피난 경로 포함 |
| 무장애 경사로 | IfcRamp | BarrierFree_Route |

---

## 5. 국가별 기준 차이

| 국가 | BIM 기준 설계 포인트 |
|---|---|
| 한국 | 학교시설사업 촉진법, 교육시설 안전·유지관리 기준, 학교보건·소방·장애인 편의시설 기준을 교실·특별실·피난 파라미터로 분리 |
| 일본 | 建築基準法, 학교시설 정비 지침, 지진·피난·체육관 피난소 활용을 반영해 구조·설비 내진 속성 강화 |
| 싱가포르 | BCA Building Control, Green Mark, 접근성 코드 중심. 고온다습 기후로 교실 냉방·차양·실내공기질 검토 강화 |
| 미국 | IBC Educational Occupancy, NFPA Life Safety Code, ADA, ASHRAE 62.1 적용. 피난·접근성·환기량의 수치 검증 중요 |
| EU | Eurocodes, EPBD, 각국 학교 설계 지침. 에너지 성능·자연채광·실내환경 품질을 BIM 속성으로 관리 |

---

## 6. 실패 사례 Top 5

1. 학생 정원과 실 면적 파라미터 불일치로 교육청 심의에서 교실 수 재산정.
2. 과학실 배기·가스 배관이 일반 교실 MEP 템플릿으로 모델링되어 안전 검토 누락.
3. 급식실 기름덕트와 방화구획 관통부가 IFC 속성 없이 납품되어 소방 협의 지연.
4. 체육관 장스팬 구조와 조명·덕트 간섭을 LOD 300 이전에 검토하지 않아 재설계.
5. 장애인 동선이 평면 선으로만 표현되고 경사·문턱·승강기 속성이 누락됨.

## 관련 링크
- [[건물유형별_BIM적용기준]]
- [[국가별_건설법규_기준비교]]
- [[BIM_납품검수]]

## 2026-06-05 학교 BIM AI 즉시 답변 패턴 보강
- Source: 교육시설 설계 기준, 학교보건법, 학교시설 환경 관리 기준
- Tags: school,education,ventilation,co2,mep,bim,2026

**AI 즉시 답변 패턴 — "학교 교실 환기 기준이 어떻게 되나요?"**
```
학교 교실 환기 기준 (학교보건법 기준):
- CO₂ 농도: 1,000 ppm 이하 유지 (재실 기준)
- 환기 횟수: 시간당 3회 이상 (기계환기)
- 창문 자연환기: 바닥 면적의 1/20 이상 개구부
- Revit BIM: 교실별 ERV(전열교환기) 급기/배기 덕트 표현
- CO₂ 감지기: 교실 내 위치 BIM 확인
```

**학교 BIM MEP 특수 사항:**
- 에너지: 학교 에너지 절약 운전 (방과후·주말·방학 절전 스케줄)
- 수도: 학생 음용 급수 배관 위생 관리 (납 성분 규제 강화)
- 방음: 인접 교실 소음 차단 → 덕트 소음기 위치 BIM 확인
- 소방: 스프링클러 의무 설치 (연면적 5,000㎡ 이상)
