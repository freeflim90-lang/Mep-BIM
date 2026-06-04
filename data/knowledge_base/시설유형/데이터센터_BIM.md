# 데이터센터 BIM 적용 기준 지식 베이스

## 2026-06-05 AI 데이터센터 냉각·전기 BIM AI 즉시 답변 패턴 보강
- Source: HVAC KOREA 2026 데이터센터 컨퍼런스, 한국데이터경제신문, 슈나이더일렉트릭
- Tags: datacenter,ai-datacenter,cooling,dlc,pue,bim-lod,hvac,2026

**AI 즉시 답변 패턴 — "AI 데이터센터 냉각 설계가 일반 데이터센터와 다른가요?"**
```
AI 데이터센터 냉각 (2025~2026 핵심 변화):
- 랙 전력 밀도: 일반 IDC 5~15kW/rack → AI GPU 서버 40~132kW/rack (Nvidia GB200 NVL72: 132kW)
- 냉각 방식 전환:
  - 에어쿨링(공조): 15kW 이하 랙에 적용 (기존 방식)
  - DLC(직접액체냉각): 15~60kW 랙 (냉각수 코일 서버 직접 접촉)
  - 침지냉각(Immersion): 60kW 이상 (서버를 냉각액에 담금)
  - 마이크로유체: 2030년 이후 상용화 예정
- PUE(Power Usage Effectiveness): 일반 1.5~2.0 → AI 데이터센터 목표 1.2~1.3
```

**데이터센터 BIM LOD 요건 (AI 데이터센터 기준):**
| 공종 | LOD 300 | LOD 350 | 핵심 |
|------|--------|--------|------|
| 냉각 (CRAC/CRAH) | 위치·용량·외형 | 급배기 경로·DLC 배관 | 콜드/핫 아일 구분 |
| UPS/발전기 | 기계실 위치·용량 | 배선 경로·버스덕트 | 이중화(N+1/2N) |
| 전기 (PDU/배전) | 랙 레이아웃·PDU | 분기배선·접지 | 이중 전원 공급 |
| 서버 랙 | 행/열 배치 | 열 구분(냉각 방식별) | 전력밀도 표기 |
| 소화 설비 | 가스계 소화 위치 | 감지기·방출 구역 | 비전도성 소화 |

**2026년 한국 데이터센터 BIM 설계 트렌드:**
- HVAC KOREA 2026 데이터센터 컨퍼런스: AI 서버 냉각기술 집중 논의
- DLC 비율 확대: 신규 AI IDC의 50% 이상 DLC 적용 설계
- BIM 협업: 서버 레이아웃(IT팀) + MEP 냉각·전기(설비팀) BIM 통합 조율 필수
- 냉각 시뮬레이션: CFD(전산유체역학) + BIM 모델 연동 → 핫스팟 사전 예측

**데이터센터 BIM 간섭검토 특수 우선순위:**
1. 콜드/핫 아일 구분 격벽과 CRAC 위치 (냉각 효율 결정)
2. UPS·발전기 하중 — 구조 슬래브 특별 보강 필요
3. 가스계 소화(CO₂/FM-200/청정소화) 방출 구역 밀폐 확인
4. 이중 전원 경로 (A/B 계통) 분리 거리 유지

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #데이터센터BIM #TIA942 #TierI-IV #PUE #ColdAisle #HotAisle #액체냉각 #내진특등급 #UPS
- 업데이트: 2026-06-05

## 데이터센터 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

### 1.1 일반 건물과의 핵심 차이점

데이터센터는 IT 인프라를 수용하는 고밀도 전기·냉방 집약 시설이다. 일반 건물 대비 전기 용량이 수십~수백 배, 냉방 부하가 극단적으로 높으며, 서버 가용성(Uptime) 확보가 최우선 목표다.

| 구분 | 일반 건물 | 데이터센터 |
|------|-----------|------------|
| 전기 밀도 | 40~60 W/m² | 500~5,000+ W/m² (랙당 5~50+ kW) |
| 냉방 부하 | 실내 발열 제거 | IT 장비 발열 제거 (PUE 목표 1.2~1.5) |
| 이중화 | 일반 예비 | N+1 ~ 2N+1 완전 이중화 (Tier 기준) |
| 내진 설계 | 건축법 기준 | 내진 특등급 (서버 장비 낙하 방지) |
| 전원 공급 | 단일 상용 | UPS + 비상발전기 + 이중 급전 경로 |
| 바닥 | 일반 슬래브 | 이중 바닥(Raised Floor) 또는 오버헤드 케이블링 |
| 운영 | 일반 FM | DCIM(Data Center Infrastructure Management) 연동 |

### 1.2 Tier 이중화 수준별 BIM 특성

Uptime Institute Tier 기준은 데이터센터 이중화의 국제 표준이다. BIM에 Tier 수준이 직접 반영된다.

| Tier | 이중화 수준 | 연간 가용시간 | BIM 특성 |
|------|------------|--------------|----------|
| Tier I | 기본 (N) | 99.671% (28.8hr 다운) | 단일 경로, 단일 UPS |
| Tier II | 예비 (N+1) | 99.741% (22.0hr) | 예비 컴포넌트, 단일 경로 |
| Tier III | 동시 유지 보수 가능 | 99.982% (1.6hr) | 이중 경로, 능동 예비 |
| Tier IV | 내결함성 | 99.995% (0.4hr) | 2N 이중화, 완전 독립 경로 |

```
Tier별 BIM 요구 사항:
  Tier I-II: 단일 UPS룸, 단일 냉동기실, 단일 배전 경로
  Tier III: 이중 UPS 경로 BIM, 이중 냉각 경로, 유지보수 우회 경로
  Tier IV: 완전 독립 A/B 계통 BIM, 이중 UPS룸, 이중 발전기실, 
            이중 냉동기실, 이중 냉각탑, 완전 분리 경로
```

---

## 2. BIM 필수 파라미터 목록

### 2.1 IT 랙 및 전력 밀도 파라미터

```
Pset_ITRack (IT 랙 속성)
  - Rack_ID: 랙 식별 번호 (예: A01-R01)
  - Rack_Type: 2-Post / 4-Post / Enclosed_Cabinet
  - Rack_Height: 랙 높이 (U, 예: 42U / 48U)
  - Rack_Depth: 깊이 (mm)
  - Rack_Width: 폭 (mm, 600mm 또는 800mm)
  - Design_Power_kW: 설계 전력 밀도 (kW/rack)
      저밀도: 3~5 kW/rack
      중밀도: 5~15 kW/rack
      고밀도: 15~30 kW/rack
      초고밀도 AI: 30~100+ kW/rack
  - Installed_Power_kW: 설치 전력 (kW) — DCIM 연동
  - Max_Power_kW: 최대 허용 전력 (kW)
  - Cooling_Type: Air / Rear_Door_Heat_Exchanger / Direct_Liquid / Immersion
  - Weight_Capacity: 최대 탑재 중량 (kg)
  - Aisle_Type: Cold_Aisle / Hot_Aisle
  - Row_ID: 랙 열 ID
  - PDU_ID: 연결 PDU(전력 분배 장치) ID
```

### 2.2 데이터센터 전력·냉방 핵심 파라미터

| 파라미터명 | 데이터 타입 | 단위 | 설명 |
|-----------|------------|------|------|
| PUE_Design | IfcRatioMeasure | - | 설계 목표 PUE (1.2~1.5 일반) |
| PUE_Actual | IfcRatioMeasure | - | 실측 PUE (DCIM 연동) |
| Total_IT_Load | IfcPowerMeasure | kW | 총 IT 부하 |
| Total_Facility_Load | IfcPowerMeasure | kW | 총 시설 전력 |
| Cooling_Capacity | IfcPowerMeasure | kW | 냉방 용량 |
| UPS_Capacity | IfcPowerMeasure | kVA | UPS 용량 |
| UPS_Redundancy | IfcLabel | - | N+1 / 2N / 2N+1 |
| Generator_Capacity | IfcPowerMeasure | kVA | 비상 발전기 용량 |
| Generator_Runtime | IfcTimeMeasure | hr | 연료 탱크 기준 운전 시간 |
| Battery_Backup_Time | IfcTimeMeasure | min | UPS 배터리 백업 시간 |
| Tier_Level | IfcLabel | - | Tier I / II / III / IV |
| RaisedFloor_Height | IfcLengthMeasure | mm | 이중 바닥 높이 (450~900mm) |
| Ceiling_Height_Net | IfcLengthMeasure | mm | 랙 상단~구조체 순 높이 |
| DCIM_Asset_ID | IfcLabel | - | DCIM 시스템 연계 자산 ID |

### 2.3 냉각 시스템 파라미터

```
Pset_CoolingSystem_DC
  - Cooling_Architecture: Air_Economizer / DX / Chilled_Water / 
                          Rear_Door_HX / In_Row_Cooling / Direct_Liquid / 
                          Immersion_Single_Phase / Immersion_Two_Phase
  - CRAC_CRAH_Type: CRAC(자체 압축기) / CRAH(냉수 코일)
  - Supply_Air_Temp: 공급 공기 온도 (°C) — ASHRAE A1: 15~27°C
  - Return_Air_Temp: 환기 온도 (°C)
  - Chilled_Water_Supply_Temp: 냉수 공급 온도 (°C) — 일반: 7~12°C
  - Chilled_Water_Return_Temp: 냉수 환수 온도 (°C)
  - Cooling_Water_Supply_Temp: 냉각수 공급 온도 (냉각탑)
  - FreeCoooling_Hours: 연간 자연 냉각 가능 시간 (hr/year)
  - WUE_Design: 물 사용 효율 목표값 (Water Usage Effectiveness)
  
Pset_DirectLiquidCooling (DLC 직접 액체 냉각)
  - DLC_Type: Cold_Plate / Rear_Door_HX / Immersion_Single / Immersion_Two_Phase
  - Coolant_Type: Water / Dielectric_Fluid / Glycol_Mix
  - Coolant_Inlet_Temp: 냉각수 입구 온도 (°C)
  - Coolant_Outlet_Temp: 냉각수 출구 온도 (°C)
  - Flow_Rate: 유량 (L/min/rack)
  - Manifold_ID: 냉각수 분배 매니폴드 ID
```

### 2.4 내진 특등급 파라미터

```
Pset_SeismicProtection_DC
  - Seismic_Category: 특등급 / 1등급 / 2등급
  - Design_Spectral_Acceleration: 설계 스펙트럼 가속도 (g)
  - Equipment_Anchorage_Type: Floor_Bolt / Seismic_Pad / Rail_System
  - Rack_Seismic_Rating: 랙 내진 성능 등급 (예: Zone 4 / GR-63-CORE)
  - Floor_Anchorage_Spacing: 바닥 앵커 간격 (mm)
  - Raised_Floor_Seismic: 이중 바닥 내진 지지대 사양
  - Cable_Routing_Seismic: 케이블 트레이 내진 행거 사양
```

---

## 3. LOD 단계별 요구사항

| LOD | 데이터센터 적용 내용 |
|-----|---------------------|
| LOD 100 | IT 용량(kW/MW), 티어 수준, 부지 면적 매스 |
| LOD 200 | 화이트 스페이스/그레이 스페이스 구획, 이중화 계통 개략, Cold/Hot Aisle 배열 |
| LOD 300 | 전체 건축·구조·전기·기계 BIM, Cold/Hot Aisle 격리 BIM, UPS·발전기실 배치 |
| LOD 350 | 랙 배열 BIM, 케이블 트레이·냉각 배관 간섭 검토, Tier 이중화 경로 검증 |
| LOD 400 | 랙 단위 전력·냉각 배관 상세 BIM, DLC 매니폴드 상세, 내진 앵커 상세 |
| LOD 500 | As-Built + DCIM 연동, 자산 관리 속성 완비, BMS 연동 |

### 3.1 데이터센터 BIM 고유 납품 요구사항

- **Capacity Planning BIM**: 랙 전력 밀도 분포 히트맵 → BIM 공간 색상 표현
- **Airflow BIM**: Cold Aisle/Hot Aisle 격리 경계 3D 표현 (지붕 격리 포함)
- **Tier Path BIM**: A/B 이중화 경로를 색상으로 구분 (Tier III/IV)
- **DCIM 연동 속성**: 모든 IT 장비·PDU·UPS에 DCIM Asset ID 매핑

---

## 4. IFC Entity 매핑

### 4.1 데이터센터 특화 IFC 엔티티

| 요소 | IFC Entity | 비고 |
|------|------------|------|
| 데이터홀 (White Space) | IfcSpace (DataHall) | 랙 전력 밀도 파라미터 |
| IT 랙 | IfcFurnishingElement 또는 IfcBuildingElementProxy | 전력·냉각 속성 |
| 이중 바닥 | IfcSlab (PredefinedType: FLOOR) | 높이·하중 파라미터 |
| UPS | IfcElectricDistributionBoard (UPS) | 용량·이중화 수준 |
| 배터리실 | IfcSpace + 하중 파라미터 (450~750 kg/m²) | |
| 비상 발전기 | IfcElectricGenerator | 용량·연료·런타임 |
| 발전기 연료 탱크 | IfcTank (Fuel) | |
| 냉동기(Chiller) | IfcChiller | |
| 냉각탑 | IfcCoolingTower | |
| CRAC/CRAH | IfcUnitaryControlElement 또는 IfcAirHandlingUnit | 랙 열 위치 기반 |
| PDU (전력 분배) | IfcElectricDistributionBoard | 상위 UPS ID 연계 |
| 케이블 트레이 | IfcCableCarrierSegment | 전력/데이터/광케이블 구분 |
| DLC 매니폴드 | IfcPipeDistributionSystem | 냉각수 분배 |
| BMS/DCIM 서버실 | IfcSpace (NOC/DCIM) | |
| Cold Aisle 격리 캡 | IfcPlate 또는 IfcCovering | 천장 격리 |

### 4.2 Cold Aisle / Hot Aisle BIM 표현

```
Cold Aisle / Hot Aisle 격리 BIM 체계:
  1. 랙 열(Row) 방향 정의: 랙 전면이 마주보는 방향 = Cold Aisle
  2. Cold Aisle 격리:
     - 양쪽 랙 열 사이 통로를 IfcSpace(ColdAisle)로 정의
     - 격리 문(Aisle Containment Door): IfcDoor
     - 격리 천장(Overhead Containment): IfcPlate
  3. Hot Aisle 격리:
     - 랙 후면 배기 방향 통로 = IfcSpace(HotAisle)
     - 천장 봉인(Ceiling Blanking): IfcCovering
  4. 격리 효율 파라미터:
     - Containment_Type: Cold_Aisle / Hot_Aisle / None
     - Mixing_Index: 공기 혼합 지수 (목표: 0.0~0.2)
     - ΔT_Supply_Return: 공급-환기 온도 차 (목표: 15~20°C)
```

---

## 5. 국가별 기준 차이

### 5.1 한국 (데이터센터 설계 기준)

- **데이터센터 설계·운영 가이드라인 (과학기술정보통신부)**: PUE 1.5 이하 권고 (2022~)
- **클라우드컴퓨팅 발전 및 이용자 보호에 관한 법률**: 공공 클라우드 보안 기준
- **내진 설계**: 건축법 내진 설계 기준 + 서버 장비 내진 특등급(행정안전부 시설물 기준)
- **전기사업법**: 수전 용량·비상 발전기 연계 신청 (한전 협의)
- **소방법**: UPS실·배터리실 자동 소화 설비 (CO₂ 또는 청정 소화약제)
- **환경부**: 냉각탑 수질 관리·레지오넬라균 방지 규정

### 5.2 일본 (DC 입지 규제)

- **IDC (Internet Data Center) 입지**: 도쿄 집중 해소 정책 — 지방 분산 지원 (2021~)
- **省エネ法**: 데이터센터 에너지 절약 의무 — PUE 보고 의무 (특정 사업자)
- **建築基準法**: 정보통신시설 구조 기준 — 면진 구조 권고
- **免震構造**: AI/HPC 시설의 대형 서버 장비 보호 — 면진 설계 증가 추세
- **土地利用**: 북해도·九州 지방 재생에너지 연계 DC 입지 우대

### 5.3 싱가포르 (DC 입지 규제)

- **DC 모라토리엄 (2019~2022)**: 탄소 발자국 우려로 신규 DC 건설 일시 중단
- **Green DC 기준 (2022 재개)**: PUE 1.3 이하 + 재생에너지 비율 목표 의무
- **BCA Green Mark DC**: 싱가포르 DC 친환경 인증 — BIM 제출 요구
- **IMDA**: 정보통신 미디어 개발청 — DC 운영 기준 및 보안 요건
- **CORENET X**: DC 건축 허가 BIM 제출 의무

### 5.4 미국 (ANSI/TIA-942)

- **ANSI/TIA-942-C (2017)**: 데이터센터 통신 인프라 기준 — Tier I~IV 설계 지침
  - 전원 공급: A/B 이중 급전, UPS, 비상 발전기
  - 냉각: N+1 이상 이중화
  - 접지: TIA-607-C 단일 접지 기준점
- **ASHRAE TC9.9**: 데이터센터 온습도 기준
  - Class A1: 15~32°C, 20~80% RH
  - Class A2: 10~35°C
- **NFPA 75**: IT 장비 화재 방호 기준
- **UL 9540**: 에너지 저장 시스템(ESS/배터리) 화재 안전 기준

### 5.5 EU (유럽 기준)

- **EU Green Deal / European Green Deal Data Centre Pact**: PUE 1.3 이하, 재생에너지 100% 목표
- **EN 50600**: 유럽 데이터센터 설계 기준 (TIA-942와 유사, Tier I~IV)
- **GDPR**: 데이터 주권 — 물리적 시설 보안 BIM (보안 구역 표현)
- **EED (Energy Efficiency Directive)**: 에너지 효율 보고 의무

---

## 6. 자주 발생하는 BIM 실패 사례 Top 5

### 실패 사례 1: Cold Aisle / Hot Aisle 격리 BIM 없이 설계 → 냉각 효율 저하
**원인**: 랙 배열 BIM 작성 시 Cold/Hot Aisle 격리 캡(Containment) 미표현. 건축 천장 높이와 격리 캡 간격 미검토.

**결과**: 준공 후 Cold Aisle 격리 캡 설치 불가(천장 배관 간섭). PUE 1.8 이상 — 목표 1.5 초과. 에너지 비용 연간 15억 원 추가.

**해결책**:
1. Cold/Hot Aisle 격리 구조를 LOD 300 단계부터 BIM에 포함
2. 격리 캡-천장 배관·케이블 트레이 간섭 검토 의무화
3. PUE 예측 시뮬레이션 기반 BIM 검토 — 격리 효율 사전 검증

---

### 실패 사례 2: UPS·발전기 이중화 경로 BIM 미검증 → Tier IV 불만족
**원인**: Tier IV 설계로 계약됐으나 BIM에서 A/B 전원 경로가 일부 공유 구간 존재. 이중화 분리 미완료.

**결과**: Uptime Institute Tier IV 인증 검사에서 공유 경로 지적. 전기 배선 재공사로 인증 3개월 지연, 추가 비용 8억 원.

**해결책**:
1. A 계통/B 계통 전원 경로를 BIM에 색상으로 구분 (A=Red, B=Blue)
2. 경로 공유 구간 자동 탐지 스크립트 — 동일 케이블 트레이 공유 여부 검토
3. Tier III/IV BIM 납품 전 이중화 경로 완전 분리 자동 검증

---

### 실패 사례 3: 배터리실 바닥 하중 BIM 미반영 → 슬래브 처짐
**원인**: 리튬이온 배터리 UPS 도입 시 배터리 단위 중량이 납축전지의 절반이라고 과신. 배터리실 밀도를 과다 배치. 구조 하중 재검토 없음.

**결과**: 배터리실 슬래브 과하중으로 처짐 발생. 배터리 절반 제거 + 구조 보강 공사.

**해결책**:
1. BIM 배터리실 슬래브에 설계 하중 파라미터 필수 입력 (kg/m²)
2. 배터리 BIM 객체에 단위 중량 파라미터 입력 → 자동 면적당 하중 산출
3. 배터리 배치 변경 시 구조 허용 하중 자동 비교 알림

---

### 실패 사례 4: 내진 앵커 BIM 미작성 → 지진 시 랙 전도
**원인**: 서버 랙 BIM에 내진 앵커 상세 미표현. 이중 바닥 앵커 방식, 간격, 사양 미정의.

**결과**: 지진 발생(규모 5.8) 시 고밀도 랙(40kW, 1,200kg) 전도. 서버 손상 및 3일간 서비스 중단.

**해결책**:
1. 랙 BIM에 내진 앵커 상세(바닥 볼트·브래킷) LOD 350 수준 표현
2. 랙 중량·중심 높이 기반 내진 앵커 크기 자동 산출
3. 이중 바닥(Raised Floor) 내진 지지대 BIM 필수화

---

### 실패 사례 5: 고밀도 AI 랙 DLC 배관 BIM 없이 시공 → 누수 사고
**원인**: AI GPU 서버 도입으로 고밀도 랙(30kW+) 채택. DLC(직접 액체 냉각) 추가 설계 시 냉각수 매니폴드 배관 BIM 미작성.

**결과**: 냉각수 연결부 누수 발생 — AI 서버 침수 피해. 서버 복구 비용 30억 원. 서비스 중단 1주일.

**해결책**:
1. DLC 매니폴드 배관 BIM을 LOD 350 수준으로 상세 모델링
2. 냉각수 배관 연결부·밸브 위치 BIM 표현 — 누수 탐지 센서 위치 연계
3. DLC 배관 Pressure Test 계획을 BIM 단계별 체크리스트에 포함

---

## 7. LUA BIM LABS 사업 기회 및 Add-in 적용 방향

### 7.1 핵심 사업 기회

| 시장 | 기회 내용 | 규모 |
|------|-----------|------|
| 한국 | AI 인프라 투자 급증 — 초고밀도 DC BIM 수요 폭증 | 2024~2030 초고성장 |
| 일본 | 지방 분산 DC 신설 러시, 면진 구조 DC BIM | 연 10조 엔+ 투자 |
| 싱가포르 | Green DC 기준 충족 BIM 컨설팅 (PUE 1.3 이하) | 엄격한 규제 기회 |
| 북미 | AI/HPC Hyperscale DC BIM — Microsoft·Google·AWS | 최대 시장 |
| 중동 | 사우디·UAE DC 허브 구축 (NEOM 포함) | Vision 2030 |

### 7.2 Revit Add-in 적용 방향

**① DC 전력 밀도 히트맵 생성기 (DC Power Density Heatmap)**
- 랙 kW 파라미터 → 데이터홀 전력 밀도 히트맵 자동 생성
- 냉각 용량 대비 전력 초과 구간 자동 알림
- 공간 색상 뷰 자동 생성 → 냉각 계획 검토 지원

**② Tier 이중화 경로 검증기 (Tier Path Verifier)**
- A/B 계통 전원 경로 BIM 자동 추출
- 공유 경로(Single Point of Failure) 자동 탐지
- Tier 등급별 이중화 요건 충족 여부 자동 체크리스트

**③ Cold/Hot Aisle 자동 격리 BIM 생성기 (Aisle Containment Modeler)**
- 랙 열 배치 BIM 기반 격리 캡(천장·측면 도어) 자동 생성
- 격리 캡-천장 장애물 간섭 자동 검토
- PUE 예측값 자동 계산 (격리 효율 파라미터 기반)

**④ DC 내진 앵커 자동 설계기 (DC Seismic Anchor Designer)**
- 랙 중량·높이·지진 구역 → 내진 앵커 크기·간격 자동 산출
- 이중 바닥 내진 지지대 BIM 자동 생성
- 내진 특등급 준수 여부 자동 검증

**⑤ DCIM 자산 연동 속성 관리기 (DCIM Asset Linker)**
- BIM 객체 DCIM Asset ID 일괄 입력 자동화
- BIM↔DCIM 양방향 데이터 동기화
- 자산 현황 보고서 자동 출력 (랙 수·전력 용량·가용률)

### 7.3 컨설팅 패키지 제안

- **DC BIM 전략 수립**: Tier 수준별 BIM 설계 기준·납품 기준 수립
- **PUE 최적화 컨설팅**: Cold/Hot Aisle 격리 BIM 기반 냉각 효율 개선
- **Tier 인증 BIM 지원**: Uptime Institute Tier 인증을 위한 BIM 근거 자료 작성
- **AI DC 전환 BIM**: 기존 DC → 고밀도 AI 서버 전환 시 BIM 리모델링

---

- 관련: [[건물유형별_BIM적용기준]] · [[국가별_건설법규_기준비교]] · [[IFC_OpenBIM]] · [[OpenBIM_프로그램연동]] · [[BIM_납품검수]] · [[해외건설기업_동향분석]]
