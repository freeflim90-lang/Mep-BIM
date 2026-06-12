# 물류센터·창고시설 BIM 적용 기준 지식 베이스

## 2026-06-05 물류센터 BIM AI 즉시 답변 패턴 보강
- Source: 건설산업 BIM 기본지침, 물류센터 특화 MEP 설계 실무, 소방청 기준
- Tags: logistics,warehouse,bim,sprinkler,agv,cold-storage,mep,2026

**AI 즉시 답변 패턴 — "물류센터 BIM에서 가장 중요한 MEP 사항이 뭔가요?"**
```
물류센터 BIM 핵심 MEP 사항:
1. 스프링클러: 랙 높이에 따라 헤드 배치가 달라짐
   - 랙 높이 3.7m 이하: 천장 헤드만으로 커버
   - 랙 높이 3.7m 초과: 랙 내부 중간 헤드 추가 필요 (NFTC 기준)
2. 대공간 환기: 지게차·AGV 배기가스 처리 (자연환기 또는 기계환기)
3. 냉동창고: 단열+냉동기계실 위치가 MEP 간섭의 핵심
4. 전기 수전: 냉동기·AGV 충전·컨베이어 전력 대용량 분전반
5. 바닥 배수: 청소·소화수 배수 위한 바닥 구배 확보
```

**물류센터 BIM 특수 고려 사항:**
| 항목 | 내용 | BIM 포인트 |
|------|------|-----------|
| 랙 시스템 | 고층 랙(5~40m) 자동창고 | 랙 위치·높이→스프링클러 배치 |
| AGV/AMR | 자율주행 물류 로봇 이동 경로 | 바닥 레이아웃 BIM 확정 필요 |
| 도크(Dock) | 화물 입출입 플랫폼 | 외기 침투→공조 설계 영향 |
| 냉동창고 | -18℃~-25℃ 유지 | 단열재 두께·냉동기 용량 BIM |
| 드라이브인 | 차량 진입 구조 | 처마 높이·진입 경로 BIM |

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #물류센터BIM #창고시설 #랙시스템 #도크 #AGV #AMR #자동창고 #스프링클러 #냉동창고
- 업데이트: 2026-06-05

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

## 2026-06-06 창고시설 화재안전기준 강화(NFPC 609)·AMR 자동화 BIM 보강
- Source: 창고시설의 화재안전성능기준(NFPC 609) 제정 2024, 소방청, 이천 물류센터 화재 2025, 씨메스/로지스올 AMR
- Tags: warehouse-fire,nfpc609,amr,cold-chain,bim,logistics,2024,2025,2026

**창고시설 화재안전성능기준(NFPC 609) 제정 — BIM 설계 필수 반영:**
- 배경: 2021년 쿠팡 이천 물류창고 화재(사망 1, 대규모 소실) → 창고시설 전용 화재안전기준 신설
- 고시: **창고시설의 화재안전성능기준(NFPC 609)** 제정 (2024)
- 2025년 이천 물류센터 재화재 → 리튬이온 배터리 화재 대응 추가 기준 강화 논의 중

**NFPC 609 핵심 강화 내용 (BIM 반영 필수 체크리스트):**
| 항목 | 강화 내용 | BIM 파라미터 |
|------|---------|------------|
| 스프링클러 방식 | **습식 스프링클러 의무화** (건식→습식 전환) | `Sprinkler_Type: Wet` |
| 배전반·분전반 | **소공간용 소화용구 의무 설치** (배전반 내부 또는 전면) | `Panel_FireExtinguisher: Required` |
| 방화구획 | 창고 특성 반영 방화구획 강화 (1,000m² 이상) | `FireCompartment_Area_m2` |
| 옥내소화전 수원 | 수원 기준 상향 (일반 기준 → 창고 기준) | `Hydrant_Water_Volume_m3` |
| 인랙 스프링클러 | 랙 높이 3.7m 초과: **인랙 중간 헤드 추가** 의무 | `InRack_Sprinkler_Required: true` |
| 리튬이온 배터리 | EV 배터리·물류 로봇 충전 구역 특수 대응 (기준 강화 예고) | `Li_Battery_Zone: true` |

**BIM 체크리스트 (NFPC 609 준수):**
```
[ ] 모든 스프링클러 → 습식 타입 속성 확인
[ ] 분전반별 소공간용 소화용구 위치 BIM 표시
[ ] 랙 높이 별도 파라미터 → 3.7m 초과 시 인랙 헤드 자동 플래그
[ ] 물류 로봇(AMR) 충전 스테이션 → 리튬 배터리 위험구역 지정
[ ] 방화구획 면적 BIM 속성 확인 (창고 기준 검수)
```

**AMR/자동창고 BIM 설계 최신 동향 (2025~2026):**
- 글로벌 물류 자동화 시장: **2032년 987억 달러** 규모 전망 (AMR이 주도)
- AMR(Autonomous Mobile Robot): AGV 대비 진화 → SLAM 내비게이션, 실시간 경로 재계산
- 물류센터 BIM에 AMR 경로 통합 설계 확산:
  - AMR 이동 영역 바닥 마킹 → BIM `IfcAnnotation` 경로 속성 추가
  - 충전 스테이션 위치 BIM → 전기 회로·분전반 용량 연동
  - AGV/AMR 이동 중 MEP 배관 이격거리(최소 600mm) 확인 자동화

**AI 콜드체인 물류센터 BIM 특화 요구사항 (2026):**
- **다온도 구역 복합**: 상온(Ambient) + 냉장(Chilled 2~8℃) + 냉동(Frozen -18~-25℃) 구역 단일 동
  - BIM 파라미터: `Temperature_Zone` → 구역별 색상 코드 의무화
- **단열 연속성 검토**: 냉동↔냉장↔상온 경계면 열교 방지 디테일 BIM (LOD 350)
- **냉동창고 결로 방지**: 방습층 위치 + 선형 열관류율(PSI) BIM 속성 추가
- **냉매 누출 감지기 위치**: `Refrigerant_Detector_ID` BIM 속성 (HCFC→HFO 냉매 전환 추세)
- **정전 시 비상 유틸리티**: 냉동창고 전원 이중화 UPS/발전기 → BIM 전원 계통도 연동

관련: [[FM_자산관리]] · [[소방기계]] · [[전기]] · [[BIM_납품검수]]
