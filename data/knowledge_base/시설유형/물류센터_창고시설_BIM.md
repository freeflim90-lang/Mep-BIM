# 물류센터·창고시설 BIM 적용 기준 지식 베이스

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #물류센터BIM #창고시설 #랙시스템 #도크 #AGV #AMR #자동창고 #스프링클러 #냉동창고
- 업데이트: 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

물류센터는 저장 밀도, 피킹 효율, 도크 회전율, 자동화 설비, 화재 안전이 성능을 좌우한다. BIM은 건축 모델에 랙·컨베이어·소방·차량 동선을 결합해 운영 시뮬레이션까지 연결해야 한다.

| 구분 | 일반 창고 | 현대 물류센터 |
|---|---|---|
| 저장 방식 | 평치·단순 랙 | 고단 랙, AS/RS, 셔틀, AMR |
| 핵심 치수 | 면적 | clear height, rack bay, dock pitch |
| 소방 | 일반 스프링클러 | 랙 인랙 스프링클러, ESFR, 방화구획 |
| 운영 | 지게차 | WMS, 자동분류기, 컨베이어 |
| 온도 | 상온 | 냉장·냉동·저온 복합 |

---

## 2. BIM 필수 파라미터 목록

### 2.1 랙·저장 파라미터

```
Pset_LogisticsStorage
  - Storage_Type: PalletRack / ASRS / Shelving / ColdStorage / HazardStorage
  - Rack_ID: 랙 식별 번호
  - Rack_Bay_Count: 베이 수
  - Rack_Level_Count: 단 수
  - Pallet_Position_Count: 팔레트 포지션 수
  - Rack_Load_Capacity: 랙 허용 하중 (kg/level)
  - Aisle_Width: 통로 폭 (mm)
  - Clear_Height: 유효 천장고 (mm)
  - Forklift_Turning_Radius: 지게차 회전 반경 (mm)
  - InRack_Sprinkler: 인랙 스프링클러 여부
```

### 2.2 도크·자동화 파라미터

| 파라미터명 | 데이터 타입 | 단위 | 설명 |
|---|---|---|---|
| Dock_ID | IfcLabel | - | 도크 번호 |
| Dock_Type | IfcLabel | - | Leveler / Pit / CrossDock / Van |
| Dock_Door_Clearance | IfcLengthMeasure | mm | 도크 문 유효 치수 |
| Trailer_Bay_Length | IfcLengthMeasure | m | 트럭 대기 구획 길이 |
| Conveyor_ID | IfcLabel | - | 컨베이어 식별 |
| Conveyor_Speed | IfcLinearVelocityMeasure | m/s | 컨베이어 속도 |
| AMR_Route_ID | IfcLabel | - | AMR/AGV 주행 경로 |
| Temperature_Zone | IfcLabel | - | Ambient / Chilled / Frozen |
| WMS_Location_Code | IfcLabel | - | WMS 로케이션 코드 |

---

## 3. LOD 단계별 요구사항

| LOD | 물류센터·창고시설 적용 내용 |
|---|---|
| LOD 100 | 물동량, 저장 용량, 상온·저온 구역 매스 |
| LOD 200 | 랙 존, 도크 수, 차량 동선, 자동화 설비 존 |
| LOD 300 | 랙 배치, 도크 상세, 스프링클러·배연·전기 간선 모델 |
| LOD 350 | 랙-스프링클러-조명-덕트 간섭, AMR/지게차 동선 clearance 검토 |
| LOD 400 | 랙 앵커, 도크 레벨러, 컨베이어, 냉동 패널 상세 |
| LOD 500 | As-Built + WMS/CMMS 연동, 위치 코드·자산 코드 완비 |

---

## 4. IFC Entity 매핑

| 요소 | IFC Entity | 비고 |
|---|---|---|
| 창고 공간 | IfcSpace | 온도·저장 등급 |
| 팔레트 랙 | IfcFurnishingElement 또는 IfcBuildingElementProxy | 하중·단수 |
| 자동창고 | IfcTransportElement 또는 IfcSystem | AS/RS 속성 |
| 컨베이어 | IfcTransportElement | 속도·라인 ID |
| 도크 도어 | IfcDoor | Dock_ID |
| 도크 레벨러 | IfcBuildingElementProxy | pit depth |
| 스프링클러 | IfcFireSuppressionTerminal | ESFR/InRack |
| 냉동 패널 | IfcWall 또는 IfcCovering | 단열 성능 |
| AMR 경로 | IfcAnnotation 또는 IfcSpace 경로 속성 | 운영 시뮬레이션 |

---

## 5. 국가별 기준 차이

| 국가 | BIM 기준 설계 포인트 |
|---|---|
| 한국 | 건축법 창고시설, 물류시설법, 소방시설 기준, 냉동창고 화재 리스크를 랙·방화구획·스프링클러 속성으로 관리 |
| 일본 | 建築基準法, 消防法, 지진 시 랙 전도 방지 기준 중요. 물류 자동화 설비와 피난 동선 분리 검토 |
| 싱가포르 | BCA, SCDF Fire Code, 고밀도 창고와 메자닌 승인 리스크 관리. 도크·방화구획·랙 하중 검증 강화 |
| 미국 | OSHA Warehousing, IBC Storage Occupancy, NFPA 13/30. 랙 저장 높이와 스프링클러 설계 조건 매핑 중요 |
| EU | Eurocodes, EN 랙 구조 기준, EPBD. 물류 자동화·에너지·냉매 규제를 시설 속성으로 관리 |

---

## 6. 실패 사례 Top 5

1. 랙 높이 변경 후 스프링클러 설계 기준이 갱신되지 않아 소방 재협의.
2. 지게차 회전 반경과 기둥 보호대 위치를 모델링하지 않아 운영 충돌 발생.
3. 냉동창고 방습·열교 디테일이 LOD 300에 누락되어 결로 하자.
4. WMS 로케이션 코드와 BIM 공간·랙 ID가 불일치해 준공 후 자산 등록 재작업.
5. 메자닌·컨베이어 하중이 구조 BIM에 반영되지 않아 보강 공사 발생.

## 관련 링크
- [[건물유형별_BIM적용기준]]
- [[국가별_건설법규_기준비교]]
- [[FM_자산관리]]
