# 공장·제조시설 BIM 적용 기준 지식 베이스

## 2026-06-05 공장·제조시설 BIM AI 즉시 답변 패턴 보강
- Source: 산업안전보건법, 공장 MEP 설계 실무, 반도체·배터리 공장 BIM 사례
- Tags: factory,manufacturing,cleanroom,crane,utility,bim,mep,2026

**AI 즉시 답변 패턴 — "공장 BIM에서 MEP 특이사항이 뭔가요?"**
```
공장·제조시설 BIM 핵심 MEP 특이사항:
1. Utility 배관: 공업용수(IW)·순수(DW)·질소(N₂)·압축공기(CA)·진공(VAC) 계통
   → 각 계통별 독립 BIM 레이어로 관리
2. 크레인 이동 경로: 천장 MEP 배관은 크레인 이동 영역 피해야 함
   → 크레인 빔 하부 300mm 이상 여유 확보
3. 폭발 위험 구역(ATEX Zone): 수소·가스 누출 가능 구역
   → 방폭 전기 기기 사용, 환기 계획 특별 설계
4. 중장비 하중: 기계 기초(머신 패드)와 배관 관통 간섭
   → 구조 강화 슬래브와 MEP 배관 이격 확인
5. 생산 라인 레이아웃: 생산 흐름(Flow)에 맞는 MEP 배치
   → 제조사 장비 배치도와 BIM 정합 필수
```

**반도체·배터리 공장 BIM 특수 사항:**
| 공장 유형 | 특수 MEP | 핵심 기준 |
|---------|---------|---------|
| 반도체 | 초순수(UPW), 특수가스, 클린룸 | ISO 1~5 등급, 초진동 제어 |
| 배터리 | 드라이룸(습도 -50℃ dew point), 소방 | 리튬 화재 대응 특수 소화 |
| 식품 공장 | HACCP 급수·배수 위생, 냉장 | 식품위생법 기준 |
| 자동차 공장 | 도장 부스 환기, 폭발 방지 | ATEX Zone 2 적용 |

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #공장BIM #제조시설 #생산라인 #클린룸 #크레인 #산업안전 #유해물질 #설비기초 #Utility
- 업데이트: 2026-06-05

---

## 1. 시설 개요 및 BIM 적용 특성

공장·제조시설은 건축물이 생산 설비를 담는 그릇이 아니라 생산 공정의 일부가 되는 시설이다. BIM은 생산라인, 장비 반입, 크레인, 유틸리티, 안전 구역, 유지보수 접근성을 동시에 검토해야 한다.

| 구분 | 일반 건물 | 공장·제조시설 |
|---|---|---|
| 우선순위 | 공간 효율 | 생산 공정 연속성 |
| 구조 | 일반 하중 | 장비 하중, 진동, 크레인 하중 |
| MEP | 쾌적성 중심 | 전력·압축공기·공정수·스팀·배기 |
| 안전 | 피난 중심 | 산업안전, 위험물, 방폭, Lockout/Tagout |
| 운영 | 입주자 변경 | 생산라인 증설·설비 교체 |

---

## 2. BIM 필수 파라미터 목록

### 2.1 생산라인·장비 파라미터

```
Pset_ManufacturingEquipment
  - Process_Line_ID: 생산라인 ID
  - Equipment_ID: 장비 식별 번호
  - Equipment_Type: CNC / Press / Assembly / Paint / Packaging / CleanTool
  - Footprint_Area: 장비 점유 면적 (m2)
  - Operating_Clearance: 운전 여유 공간 (mm)
  - Maintenance_Clearance: 유지보수 여유 공간 (mm)
  - Installation_Weight: 설치 중량 (kg)
  - Operating_Weight: 운전 중량 (kg)
  - Vibration_Class: Low / Medium / High / Precision
  - Utility_Connection_ID: 유틸리티 연결 ID
  - Relocation_Priority: 이전 가능성 High / Medium / Low
```

### 2.2 구조·유틸리티 파라미터

| 파라미터명 | 데이터 타입 | 단위 | 설명 |
|---|---|---|---|
| Floor_Load_Capacity | IfcPressureMeasure | kN/m2 | 바닥 허용 하중 |
| Point_Load | IfcForceMeasure | kN | 장비 집중 하중 |
| Crane_SWL | IfcForceMeasure | ton | 크레인 안전 작업 하중 |
| Hook_Height | IfcLengthMeasure | m | 크레인 훅 높이 |
| CompressedAir_Pressure | IfcPressureMeasure | bar | 압축공기 공급 압력 |
| ProcessWater_Flow | IfcVolumetricFlowRateMeasure | L/min | 공정수 유량 |
| Exhaust_Airflow | IfcVolumetricFlowRateMeasure | m3/h | 국소 배기량 |
| Hazardous_Material_Class | IfcLabel | - | 위험물·화학물질 등급 |
| ATEX_or_ClassDiv | IfcLabel | - | 방폭 구역 등급 |

---

## 3. LOD 단계별 요구사항

| LOD | 공장·제조시설 적용 내용 |
|---|---|
| LOD 100 | 생산 용량, 공정 흐름, 대형 장비 존 매스 |
| LOD 200 | 라인 배치, 물류 흐름, 장비 반입구, 크레인 범위 |
| LOD 300 | 건축·구조·MEP + 주요 생산장비 footprint와 유틸리티 접속점 |
| LOD 350 | 장비 유지보수 공간, 배관·덕트·케이블트레이 간섭, 방폭 구역 경계 |
| LOD 400 | 설비기초, 앵커볼트, 크레인 레일, 공정배관 상세 |
| LOD 500 | As-Built + CMMS/EAM 연동, 장비 이력·예비품 속성 |

---

## 4. IFC Entity 매핑

| 요소 | IFC Entity | 비고 |
|---|---|---|
| 생산라인 | IfcSystem 또는 IfcProcess | 공정 흐름 연계 |
| 제조 장비 | IfcBuildingElementProxy 또는 IfcTransportElement | 장비 속성 확장 |
| 설비기초 | IfcFooting 또는 IfcSlab | 하중·앵커 속성 |
| 크레인 | IfcTransportElement | SWL, Hook_Height |
| 크레인 레일 | IfcRail 또는 IfcMember | 레일 레벨 관리 |
| 압축공기 배관 | IfcPipeSegment | 압력·유량 |
| 국소배기 덕트 | IfcDuctSegment | 오염물질 속성 |
| 방폭 구역 | IfcSpace | ATEX/ClassDiv 속성 |
| 위험물 저장소 | IfcSpace + IfcTank | 물질 등급 |

---

## 5. 국가별 기준 차이

| 국가 | BIM 기준 설계 포인트 |
|---|---|
| 한국 | 산업안전보건법, 위험물안전관리법, 건축법 공장 용도, 기계설비·소방 기준을 생산라인별 안전 구역으로 속성화 |
| 일본 | 建築基準法, 消防法, 労働安全衛生法 중심. 지진 시 장비 전도·배관 유연 이음·방재 구획 검토 강화 |
| 싱가포르 | BCA Building Control, SCDF Fire Code, MOM 산업안전 요구. 고밀도 산업단지에서 방화·위험물 보관·배기 검토 중요 |
| 미국 | OSHA, IBC Factory/Industrial, NFPA 30/70/654, ASME 계열 기준. 방폭·분진·전기 안전 속성 관리 중요 |
| EU | Eurocodes, Machinery Regulation, ATEX, EPBD. CE·방폭 구역·에너지 성능을 장비 및 공간 속성으로 연결 |

---

## 6. 실패 사례 Top 5

1. 장비 하중을 균등하중으로만 처리해 실제 집중하중 검토가 누락됨.
2. 장비 반입 경로와 개구부 크기를 BIM에 반영하지 않아 준공 후 벽체 해체.
3. 생산라인 변경 가능성을 고려하지 않고 유틸리티 접속점을 고정 배치.
4. 방폭 구역을 도면 해치로만 표현하고 공간 객체 속성에 반영하지 않음.
5. 크레인 훅 높이와 덕트·조명 간섭을 늦게 발견해 천장 설비 재배치.

## 관련 링크
- [[건물유형별_BIM적용기준]]
- [[국가별_건설법규_기준비교]]
- [[설비시공조율]]
