# 주차장·모빌리티시설 BIM 적용 기준 지식 베이스

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #주차장BIM #모빌리티시설 #램프 #전기차충전 #환기 #배연 #차량동선 #자주식주차 #기계식주차
- 업데이트: 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

주차장·모빌리티시설은 차량 동선, 램프 경사, 주차 구획, 환기·배연, 전기차 충전, 보행자 안전이 핵심이다. BIM은 자동차 궤적과 구조·설비 간섭을 동시에 확인해야 하며, 운영 단계에서는 주차 관제·EV 충전 자산과 연결된다.

| 구분 | 일반 건물 부속주차 | 독립 모빌리티 시설 |
|---|---|---|
| 목적 | 법정 주차 대수 충족 | 교통 허브, 환승, 충전, 정비 |
| 동선 | 단순 입출차 | 차량·보행자·자전거·배송 동선 분리 |
| 설비 | 기본 조명·환기 | CO 감지, 배연, EV 충전, 관제 |
| 구조 | 일반 슬래브 | 램프, 장스팬, 차량 하중, 진동 |
| 운영 | 수동 관리 | LPR, 주차유도, 충전 과금 |

---

## 2. BIM 필수 파라미터 목록

### 2.1 주차·램프 파라미터

```
Pset_ParkingMobility
  - Parking_Stall_ID: 주차면 번호
  - Stall_Type: Standard / Compact / Accessible / EV / Loading / Bicycle
  - Stall_Width: 주차면 폭 (mm)
  - Stall_Length: 주차면 길이 (mm)
  - Drive_Aisle_Width: 차로 폭 (mm)
  - Ramp_Slope: 램프 경사 (%)
  - Ramp_Turning_Radius: 램프 회전 반경 (mm)
  - Clear_Height: 유효 높이 (mm)
  - Vehicle_SweptPath_OK: 차량 궤적 검토 통과 여부
  - Pedestrian_Route_ID: 보행자 동선 ID
```

### 2.2 환기·EV 충전 파라미터

| 파라미터명 | 데이터 타입 | 단위 | 설명 |
|---|---|---|---|
| CO_Sensor_ID | IfcLabel | - | CO 감지기 ID |
| Ventilation_Mode | IfcLabel | - | Natural / Mechanical / JetFan |
| JetFan_ID | IfcLabel | - | 제트팬 ID |
| Smoke_Control_Zone | IfcLabel | - | 배연 구역 |
| EV_Charger_ID | IfcLabel | - | 충전기 ID |
| EV_Charger_Capacity | IfcPowerMeasure | kW | 충전 용량 |
| Charger_Type | IfcLabel | - | AC / DC Fast / UltraFast |
| LPR_Camera_ID | IfcLabel | - | 번호판 인식 카메라 |
| Parking_Guidance_Node | IfcLabel | - | 주차 유도 센서·표지 |

---

## 3. LOD 단계별 요구사항

| LOD | 주차장·모빌리티시설 적용 내용 |
|---|---|
| LOD 100 | 주차 대수, 층수, 진출입 위치, 램프 방식 |
| LOD 200 | 주차면 모듈, 차량 동선, 보행 동선, 환기 방식 |
| LOD 300 | 구조·램프·주차면·제트팬·EV 충전·관제 설비 모델 |
| LOD 350 | 차량 swept path, 유효 높이, 배연·스프링클러·조명 간섭 검토 |
| LOD 400 | 충전기 기초·케이블트레이·센서·차량 방호 시설 상세 |
| LOD 500 | As-Built + 주차관제·충전 과금·FM 자산 연동 |

---

## 4. IFC Entity 매핑

| 요소 | IFC Entity | 비고 |
|---|---|---|
| 주차 공간 | IfcSpace | Stall_ID |
| 램프 | IfcRamp | 경사·회전반경 |
| 주차 차로 | IfcSpace 또는 IfcAnnotation | 차량 동선 |
| 제트팬 | IfcFan | 환기·배연 속성 |
| CO 감지기 | IfcSensor | CO_Sensor_ID |
| EV 충전기 | IfcElectricAppliance 또는 IfcBuildingElementProxy | 용량·회로 |
| 케이블트레이 | IfcCableCarrierSegment | 충전 간선 |
| 주차 관제 카메라 | IfcSensor | LPR_Camera_ID |
| 차량 방호벽 | IfcWall 또는 IfcRailing | 충돌 안전 |

---

## 5. 국가별 기준 차이

| 국가 | BIM 기준 설계 포인트 |
|---|---|
| 한국 | 주차장법, 건축법, 소방·기계설비 기준, 전기차 충전 인프라 의무 비율. 램프·주차면·EV 충전 회로 속성 관리 |
| 일본 | 駐車場法, 建築基準法, 消防法. 소형 대지의 기계식 주차와 지진 시 설비 안전 검토 중요 |
| 싱가포르 | BCA, LTA, SCDF 기준. 도심 고밀도 주차, EV 충전, 접근성·화재 안전 검토 강화 |
| 미국 | IBC Parking Garage, NFPA, ADA, NEC EV charging. 접근성 주차·환기·충전 회로 검증 |
| EU | Eurocodes, EPBD, 각국 EV 인프라 지침. 충전 설비와 에너지 관리·화재 안전 속성 연계 |

---

## 6. 실패 사례 Top 5

1. 주차 대수는 맞지만 차량 궤적 검토가 없어 램프 회전부 이용 불가.
2. 유효 높이에 덕트·스프링클러·표지판이 포함되지 않아 대형 차량 충돌.
3. EV 충전기 위치만 표시하고 전력 간선·분전반 용량이 누락됨.
4. 보행자 동선과 차량 동선이 출입구에서 교차해 안전 리스크 발생.
5. 자연환기 가정 후 지하층 CO·배연 검토가 부족해 기계 환기 추가 공사.

## 관련 링크
- [[일반건물_빌딩_BIM]]
- [[데이터센터_BIM]]
- [[FM_자산관리]]
