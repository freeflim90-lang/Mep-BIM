# 공항 BIM 적용 기준 지식 베이스

## 2026-06-05 공항 BIM 인천공항 MEP·수하물처리 AI 즉시 답변 패턴 보강
- Source: 인천국제공항공사, 현대건설 인천공항 BIM 사례, 공항시설법
- Tags: airport,terminal,bhs,mep,hvac,bim-lod,incheon,2026

**AI 즉시 답변 패턴 — "공항 BIM에서 가장 복잡한 MEP 공종이 뭔가요?"**
```
공항 터미널 MEP 복잡도 순위:
1. 공조(HVAC): 초대형 오픈 공간 + 탑승동 간 온도 조절
   - 인천공항 T1: 열교환기·AHU 규모 일반 건물의 10배 이상
2. 수하물처리시스템(BHS): MEP와 독립 설비이나 공간 간섭 심각
   - 인천공항 T1: 88km 컨베이어, 시간당 5.8만 개 처리
3. 소방: 대형 오픈 공간 → 스프링클러 대신 드렌처·포소화 적용 구간
4. 전기: 탑승교(PBB) 전원·항행 조명(OLS)·관제 시스템
5. 의료(공항 의무실): 응급 의료가스·산소 공급 시스템
```

**공항 BIM LOD 요건 (인천공항 2016 BIM 어워드 수준 기준):**
| 공종 | LOD 300 | LOD 350 | 특수 항목 |
|------|--------|--------|---------|
| 터미널 구조 | 대형 스팬 구조 형상 | 루버·커튼월 패널 분할 | 곡선 천장 BIM |
| HVAC | AHU·덕트 주 경로 | 탑승동 급배기 경로 | 외기 도입량 |
| BHS | 컨베이어 경로 레이아웃 | 분류기·카트 보관 | 별도 BIM 계통 |
| 소방 | 스프링클러·드렌처 구역 | 방화구획 댐퍼 | 대공간 방화 |
| 탑승교(PBB) | 탑승교 도킹 위치 | 전원·공조 연결 | 이동형 설비 |

**인천공항 BIM 사례 (2026 기준):**
- 인천공항 현대건설 T2 공사: 곡선 루버 천장 BIM으로 공장 제작·현장 조립 성공
- BIM 어워드 2016 건축 부문 대상 수상 → 공항 BIM 참조 사례
- 인천공항공사 BIM 설계 내재화: 건축·협력설계·운영관리까지 BIM 활용

**공항 BIM 납품 특수 요건:**
- OLS(항행 장애등) 좌표: 국토교통부 항공 장애물 관리 시스템 연동
- 소방 대공간: KDS 기준 + 드렌처·포소화 구역 별도 표시
- 탑승교(PBB): 이동형 설비 → 도킹 위치별 MEP 연결 인터페이스 BIM 표시

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #공항 #터미널BIM #BHS #탑승교 #OLS #IATA #방화구획 #공항시설법
- 업데이트: 2026-06-05

## 공항 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

### 1.1 일반 건물과의 핵심 차이점

공항 터미널은 초대형 복합 인프라 시설로, BIM 적용 범위가 건축 단독을 훨씬 초과한다. 항공기 운영 시스템, 보안 요구사항, 국제 항공 기준(ICAO/IATA)이 설계에 직접 반영된다.

| 구분 | 일반 건물 | 공항 터미널 |
|------|-----------|------------|
| 공간 통제 | 일반 접근 통제 | 보안 구역(Security Zone) 철저 분리 |
| 하중 기준 | 일반 활하중 | 수하물 컨베이어·BHS 장비 하중 별도 |
| 방화 | 건축법 방화구획 | 항공기 연료·Jet-A 누설 고려 특수 방화구획 |
| 공간 분류 | 건축 용도 | IATA 기준 공간 프로그램 (출국/입국/환승/상업/운영) |
| 외부 연계 | 인접 대지 | 비행안전구역(OLS) 내 건축 높이 규제 |
| 규모 | 수천~수만 m² | 수십만 m² (인천공항 T1: 496,000m²) |

### 1.2 BIM 적용 핵심 특수성

1. **BHS(수하물 처리 시스템)**: 터미널 지하층 전체를 가로지르는 컨베이어 시스템. 독립 BIM 모델로 관리하며 건축 BIM과 통합 간섭 검토 필수
2. **항공기 탑승교(Boarding Bridge)**: 가변 길이·높이 구조물. Revit에서 동적 패밀리로 구현 필요
3. **OLS(Obstacle Limitation Surface)**: 3D 비행안전구역 면을 BIM으로 시각화하여 주변 건물·크레인 높이 검토
4. **보안 구역 분리**: CIQ(세관·출입국·검역) 구역 경계를 BIM 공간으로 정확히 표현

---

## 2. BIM 필수 파라미터 목록

### 2.1 IFC Property Set 기준 파라미터

```
Pset_AirTerminalTypeCommon (공기 터미널 유형)
  - AirFlowRateRange: 풍량 범위
  - FaceVelocity: 면풍속

Pset_SpaceCommon
  - SecurityLevel: 보안 등급 (Public/Sterile/Restricted)
  - OccupancyType: 점유 유형
```

### 2.2 공항 특화 파라미터

| 파라미터명 | 데이터 타입 | 단위 | 설명 |
|-----------|------------|------|------|
| Terminal_Zone | IfcLabel | - | Departures / Arrivals / Transfer / Commercial / Operations |
| Security_Level | IfcLabel | - | Public / Sterile / Restricted / AOSide |
| Gate_Number | IfcLabel | - | 탑승구 번호 (예: A01, B12) |
| Aircraft_Category | IfcLabel | - | Code C/D/E/F (날개폭 기준) |
| BoardingBridge_Type | IfcLabel | - | Fixed / Apron_Drive |
| BHS_Zone_ID | IfcLabel | - | 수하물 처리 구역 ID |
| Baggage_Claim_ID | IfcLabel | - | 수하물 수취대 번호 |
| CheckIn_Counter_ID | IfcLabel | - | 체크인 카운터 번호 |
| Jetway_Reach_Min | IfcLengthMeasure | m | 탑승교 최소 도달 거리 |
| Jetway_Reach_Max | IfcLengthMeasure | m | 탑승교 최대 도달 거리 |
| OLS_Clearance | IfcLengthMeasure | m | OLS 여유 높이 |
| FuelPit_Location | IfcLabel | - | 항공기 연료 피트 위치 |
| FireSuppression_Type | IfcLabel | - | 소화 시스템 (Foam/Sprinkler/CO2) |
| IATA_LOS_Category | IfcLabel | - | 서비스 수준 (A/B/C/D/E) |
| paxCapacity_Peak | IfcCountMeasure | pax/hr | 피크시 처리 용량 |
| Customs_Lane_Count | IfcCountMeasure | - | 세관 통과 레인 수 |

### 2.3 BHS 특화 파라미터

```
Pset_BaggageHandlingSystem
  - BHS_LineID: 컨베이어 라인 ID
  - ConveyorSpeed: 컨베이어 속도 (m/s) — 표준 0.5~2.5 m/s
  - BagCapacity_perHour: 시간당 처리 수하물 수
  - HazardousDetection: 폭발물 탐지 장치 연계 여부 (Boolean)
  - BHSLevel: B0/B1/B2 (지하층 레벨)
  - MaintenanceAccess_Width: 유지보수 통로 폭 (mm) — 최소 600mm 이상
  - ConveyorLoad: 설계 하중 (kg/m) — 구조 하중 산정 기준
```

---

## 3. LOD 단계별 요구사항

| LOD | 지하철역사 적용 내용 |
|-----|---------------------|
| LOD 100 | 터미널 매스, 게이트 수, 연간 여객 처리 용량 |
| LOD 200 | 보안 구역 경계, BHS 경로 개략, 탑승교 배치, OLS 3D 경계면 |
| LOD 300 | 전체 건축·구조·MEP BIM, BHS 시스템 배치, 탑승교 피트 상세 |
| LOD 350 | BHS 컨베이어 상세, 탑승교 동적 범위 BIM, 보안 장비 위치 |
| LOD 400 | 제작 BIM (탑승교, BHS, 체크인 카운터 시스템 가구) |
| LOD 500 | As-Built + FM 연동, 공항 운영 시스템(AODB·FIDS) 연계 속성 |

### 3.1 공항 BIM 특수 납품 요구사항

- **OLS BIM**: AIP(Aeronautical Information Publication) 기반 3D 제한 표면 모델
- **항공등화 BIM**: 활주로·유도로 항공등화 IFC 모델 (운항지원본부 검토용)
- **보안시설 BIM**: 별도 보안 등급 파일로 납품 (일반 BIM과 분리)
- **AVSEC 검토 BIM**: 항공보안 구역 분리 도면 대체 BIM

---

## 4. IFC Entity 매핑

### 4.1 공항 특화 IFC 엔티티

| 요소 | IFC Entity | 비고 |
|------|------------|------|
| 터미널 건물 | IfcBuilding | 터미널별 독립 건물 객체 |
| 보안 구역 공간 | IfcSpace (ZoneType: Security) | 구역별 SecurityLevel 파라미터 |
| 탑승구 게이트 | IfcSpace (PredefinedType: GATE) | |
| 탑승교 | IfcTransportElement (PredefinedType: BOARDING_BRIDGE) 또는 IfcBuildingElementProxy | 동적 길이 Dynamo 자동화 필요 |
| BHS 컨베이어 | IfcTransportElement (PredefinedType: CONVEYOR) | |
| 체크인 카운터 | IfcFurnishingElement | |
| 수하물 수취대 | IfcFurnishingElement (커스텀) | |
| 보안 검색대 | IfcBuildingElementProxy | 보안 BIM 별도 파일 |
| 항공등화 | IfcLightFixture | AOSide 구역 |
| 연료 피트 | IfcOpeningElement 또는 IfcBuildingElementProxy | |
| 주기장 (Apron) | IfcSlab (PredefinedType: FLOOR) + IfcPavement (IFC 4.3) | |
| OLS 경계면 | IfcGeographicElement 또는 IfcBuildingElementProxy | |

### 4.2 공항 시설 구역 체계

```
공항 구역 BIM 계층 구조:
  IfcSite (공항 전체 부지)
  ├─ IfcBuilding (터미널 1)
  │   ├─ IfcBuildingStorey (B2: BHS 층)
  │   ├─ IfcBuildingStorey (B1: 도착 층)
  │   ├─ IfcBuildingStorey (L1: 출발 층)
  │   └─ IfcBuildingStorey (L2: 환승 층)
  ├─ IfcBuilding (터미널 2)
  ├─ IfcBuilding (탑승동/Concourse A)
  └─ IfcExternalSpatialElement (에이프런/유도로)
```

---

## 5. 국가별 기준 차이

### 5.1 한국 (공항시설법·국토부 기준)

- **공항시설법 시행규칙**: 터미널 면적 산정 기준 (연간 1백만 여객당 약 5,000m²)
- **국토교통부 공항 BIM 지침**: 인천국제공항공사 자체 BIM 기준 (IIA-BIM-STD) — LOD 400 수준 요구
- **항공안전법**: OLS 기준 — 진입면·수평면·원추면 등 6개 제한 표면
- **화재안전기준**: 공항터미널 화재안전기준 (NFPC 501A 준용) — Jet-A 연료 누설 시 포소화 시스템

### 5.2 일본 (成田空港·나리타 BIM 기준)

- **国土交通省 航空局**: 공항 시설 BIM 도입 가이드라인 (2023)
- **成田国際空港(NAA) BIM 요건**: 터미널 리모델링 시 레이저 스캔 + BIM 역모델링 요구
- **건축기준법 적용**: 공항 터미널도 건축기준법 적용 (특수 건축물), 1관구 최대 1,500m²
- **내진 기준**: 건축기준법 + 공항 시설 내진성능 평가 기준 (레벨 2 지진 대응)

### 5.3 싱가포르 (창이공항 BIM 기준)

- **CAG (Changi Airport Group) BIM 요구사항**: ISO 19650 기반, LOD 500 As-Built 의무
- **BCA CORENET X**: 공항 터미널 건축 허가 BIM 제출
- **T5 신터미널 BIM**: 총 1.4M m² — 역대 최대 규모 공항 BIM 프로젝트 중 하나
- **디지털 트윈**: 창이공항은 실시간 운영 디지털 트윈 구현 — BIM이 기반 데이터

### 5.4 미국 (FAA 기준)

- **FAA Advisory Circular**: AC 150/5300-13B (공항 설계 기준)
- **OLS 기준**: FAR Part 77 — 항행안전시설 보호 구역
- **BIM 요구**: 연방 예산 사용 시 GSA BIM 가이드라인 준용
- **내진 기준**: IBC (International Building Code) + ASCE 7 위험도 기준
- **AVSEC**: TSA 보안 구역 기준 — BIM에 보안 등급 구역 반드시 표시

### 5.5 EU (유럽 기준)

- **EASA**: 유럽 항공안전청 — 공항 설계 기준 (ADR 규정)
- **Eurocode**: 건축 구조 설계 기준 (EN 1990~1999)
- **BIM 의무화**: EU 공공 발주 BIM 의무 (영국 PAS 1192 → ISO 19650)

---

## 6. 자주 발생하는 BIM 실패 사례 Top 5

### 실패 사례 1: BHS와 구조 BIM 간섭 — 컨베이어 피트 누락
**원인**: BHS는 전문 업체(Vanderlande, BEUMER 등) 별도 설계. 건축·구조 BIM과 통합 시점이 늦어짐. 구조 슬래브에 BHS 피트(구멍) 미반영.

**결과**: BHS 설치 직전 슬래브 코어링 대규모 발생. 추가 보강 철근 공사, 6주 공기 지연.

**해결책**:
1. BHS 업체 BIM 라이브러리 조기 확보 (기본 설계 단계)
2. BHS 피트·슬리브 요구 사항을 구조 BIM에 Placeholder로 먼저 반영
3. LOD 300 단계에서 BHS-구조 통합 간섭 검토 의무화

---

### 실패 사례 2: 탑승교 동적 범위 미검증
**원인**: Revit에서 탑승교를 고정 형상으로 모델링. 실제 탑승교는 최소~최대 길이, 높이 조절 범위가 있는 동적 구조물.

**결과**: 주기 항공기 기종 변경 시(B737 → A380) 탑승교 도달 범위 부족 확인. 게이트 레이아웃 전면 재설계.

**해결책**:
1. 탑승교 Revit 패밀리에 동적 파라미터 적용 (최소/최대 길이, 높이 범위)
2. 항공기 기종별 탑승구 위치(도어 센터) 데이터 반영
3. Dynamo로 탑승교 도달 범위 자동 검증 스크립트 작성

---

### 실패 사례 3: 보안 구역 BIM 공개 납품 → 보안 위반
**원인**: LOD 500 BIM 납품 시 보안 장비 위치(검색대·CCTV·폭발물 탐지기)가 일반 BIM 파일에 포함.

**결과**: BIM 파일이 컨설팅 협력사를 통해 유출 위험. 공항 당국 즉시 납품 중단 요청.

**해결책**:
1. BIM 파일 분리 전략: 일반 BIM / 보안 BIM 별도 파일 관리
2. 보안 BIM은 암호화 IFC + 접근 권한 관리 (BIM 360 권한 레벨 설정)
3. BEP에 보안 정보 취급 절차 명시

---

### 실패 사례 4: OLS 3D 경계 미적용으로 크레인 높이 초과
**원인**: 시공 단계 타워크레인 위치 계획 시 OLS 제한 높이 검토 미실시.

**결과**: 활주로 인근 크레인이 OLS 위반. 항공청 비행 제한 명령. 크레인 재배치로 공기 4주 지연.

**해결책**:
1. BIM 모델에 OLS 3D 면(IfcGeographicElement)을 착공 전 반영
2. 타워크레인 위치 계획 시 BIM으로 OLS 간섭 자동 체크
3. 시공 단계 장비 계획서 BIM 검토 의무화

---

### 실패 사례 5: IATA 공간 프로그램과 실제 BIM 면적 불일치
**원인**: IATA 공항개발 레퍼런스 매뉴얼(ADRM) 기준 면적 산정 후, 실제 설계 진행 중 공간 배치 변경. BIM 업데이트 미흡.

**결과**: 체크인 카운터 수·수하물 수취대 수가 IATA 서비스 수준(LOS C) 미달. 공항 운영사 설계 재검토 요구.

**해결책**:
1. IATA LOS 파라미터를 BIM 공간 객체에 직접 입력
2. Dynamo로 체크인 카운터 수·보안 레인 수 자동 산출 → IATA 기준 비교
3. 설계 변경 시 BIM 공간 면적 자동 업데이트 알림 체계 구축

---

## 7. LUA BIM LABS 사업 기회 및 Add-in 적용 방향

### 7.1 핵심 사업 기회

| 시장 | 기회 내용 | 규모 |
|------|-----------|------|
| 한국 | 인천공항 T3·청주·제주 확장 BIM | 2026~2035 |
| 일본 | 나리타·하네다 리모델링 BIM/CIM | 2025~2030 |
| 싱가포르 | 창이공항 T5 신터미널 BIM 컨설팅 | 초대형 프로젝트 |
| 중동 | 리야드 킹살만공항·두바이 확장 | 중동 항공 허브 성장 |

### 7.2 Revit Add-in 적용 방향

**① IATA LOS 자동 산출기 (Airport LOS Analyzer)**
- BIM 공간 면적 → IATA LOS(A~E) 자동 산출
- 체크인 카운터·보안 레인·게이트 수 자동 검증
- 피크 시간 여객 처리 용량 시뮬레이션 결과 출력

**② BHS 간섭 자동 검토기 (BHS Clash Detector)**
- BHS 컨베이어 경로 BIM Import → 구조 BIM 자동 간섭 검토
- BHS 피트·슬리브 위치 자동 표시 → 구조 설계팀 전달 자동화

**③ OLS 높이 검증기 (OLS Height Checker)**
- FAA/ICAO 기준 OLS 표면 자동 생성
- 시공 단계 장비(크레인) 높이 자동 OLS 간섭 검토
- 위반 항목 색상 강조 + 보고서 자동 생성

**④ 공항 공간 분류 자동화 (Airport Zone Classifier)**
- IATA 공간 프로그램 기준 구역 코드 자동 부여
- 보안 구역 경계 자동 생성 + 보안 BIM 분리 내보내기

### 7.3 컨설팅 패키지 제안

- **공항 BIM 전략 수립**: IATA ADRM 기반 BIM 공간 프로그램 수립 지원
- **BHS-구조 통합 검토 서비스**: 공항 수하물 처리 시스템 BIM 통합 전문 서비스
- **공항 디지털 트윈 전환**: FM 연동 COBie + 운영 데이터 연계 컨설팅

---

- 관련: [[건물유형별_BIM적용기준]] · [[국가별_건설법규_기준비교]] · [[IFC_OpenBIM]] · [[OpenBIM_프로그램연동]] · [[BIM_납품검수]] · [[해외건설기업_동향분석]]

## 2026-06-06 KAC-BIM 스마트공항·인천공항 스마트패스 BIM 보강
- Source: 한국공항공사 KAC-BIM 발표, 인천국제공항공사 스마트패스, 인천공항 T3 나무위키
- Tags: kac-bim,smart-airport,digital-twin,smartpass,egate,incheon-t3,bim,2025,2026

**KAC-BIM — 한국공항공사 오픈BIM 디지털트윈 (2020~2026 국가 프로젝트):**
- 사업명: **KAC-BIM** (오픈BIM 기반 시설정보 통합관리기술)
- 기간: 2020~2026년 7년 장기 프로젝트
- 목표: 공항시설 3D BIM 디지털트윈 → 설계·건설·유지관리 정보 단일 통합 플랫폼
- 주관: 한국공항공사 (KAC), 세계 최초 오픈BIM 기반 공항 시설정보 통합시스템 개발
- 핵심 기술:
  - 공항 시설 3D BIM 모델 → 지능형 제어·자동화 연동
  - 건설 단계 BIM 데이터 → 운영 FM 데이터 자동 전환 (COBie 확장)
  - OpenBIM 표준(IFC) 기반 → 발주처·설계·시공·운영 전 단계 데이터 공유

**인천공항 스마트패스 (eGate 자동화) — BIM 연동 포인트:**
- 서비스: 얼굴 인식 1회 등록 → 체크인·보안검색·출국심사·탑승까지 자동 통과
- 스마트패스 백드랍: 자동 수하물 위탁 기기 → 줄 없이 직접 위탁
- BIM 설계 연동 사항:
  | 설비 | BIM 파라미터 | 설계 포인트 |
  |------|------------|-----------|
  | 자동 출입국 e-Gate | `AutoGate_ID`, `Biometric_Type: Face` | 게이트 전·후 대기 공간 확보 |
  | 스마트패스 백드랍 | `BagDrop_ID`, `SmartPass_Enable: true` | 카운터 동선 최적화 |
  | 스마트 보안검색장 | `SecurityLane_ID`, `SmartScan_Type` | CT스캐너 설치 공간·전원 |
  | 얼굴인식 카메라 | `FRT_Camera_ID`, `FOV_deg` | 조명·각도 BIM LOD 350 |

**인천공항 T3 신터미널 동향 (2026 기준):**
- 인천공항 3단계 확장: 제3여객터미널(T3) 추가 건설 계획 진행 중
- 현재 T1·T2 운영 중, T3는 중장기 수요 대비 확장 계획
- 공항 용량 목표: 여객 처리 능력 확대 (현재 T1 5,400만 + T2 2,000만 → T3 추가)
- BIM 수요: T3 설계 착수 시 KAC-BIM 표준 적용 → 공항 전문 BIM 컨설팅 수요

**스마트공항 BIM 디지털트윈 운영 사례 (2025~2026):**
- **예측 유지보수**: 공항 시설물 센서 → BIM 자산 ID 연동 → 장애 예측 알람
  - IfcSensor → `FM_Asset_ID` → CMMS(유지보수관리시스템) 자동 작업 지시
- **에너지 최적화**: 공항 BEMS → 환절기·비성수기 에너지 절감 스케줄 BIM 연동
- **군중 흐름 모니터링**: 실시간 여객 밀도 → 게이트·카운터 배치 시뮬레이션
- **탄소발자국 모니터링**: 공항 운영 탄소 → EC3 연동 탄소 추적 BIM

**LUA BIM LABS 공항 BIM 추가 기회 (KAC-BIM 연계):**
- KAC-BIM 협력사 등록 → 지방 공항(김포·김해·제주·광주·청주) BIM 유지관리 용역
- 스마트공항 설비 BIM 납품: 자동 게이트·보안검색장 MEP 설계 BIM
- 공항 디지털트윈 FM 컨설팅: KAC-BIM 표준 기반 COBie 확장 납품 패키지

관련: [[지하철역사_BIM]] · [[FM_자산관리]] · [[IFC_OpenBIM]] · [[BIM_납품검수]]
