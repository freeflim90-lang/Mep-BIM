# 지하철역사 BIM 적용 기준 지식 베이스

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #지하철 #역사BIM #도시철도 #토공BIM #IFC4.3 #Alignment #방재시뮬레이션 #환기제연
- 업데이트: 2026-05-28

## 지하철역사 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

### 1.1 일반 건물과의 핵심 차이점

지하철역사는 단순 건축물이 아니라 **토목+건축+설비+전기+신호+운영 시스템**이 복합된 인프라 시설이다. BIM 적용 시 다음 특성을 반드시 이해해야 한다.

| 구분 | 일반 건물 | 지하철역사 |
|------|-----------|------------|
| 기준 좌표계 | 로컬 프로젝트 기준점 | GIS 국가 좌표계(TM/WGS84) 필수 |
| 구조 시스템 | 독립 구조물 | 인접 구조물·선로 연계 하중 고려 |
| 화재·방재 | 건축법 피난 기준 | 도시철도법 제연 구역 분리 + NFPA 130 |
| 공간 분류 | 건축 용도 기준 | 대합실/승강장/기계실/전기실/선로구역 분리 |
| 지하 굴착 | 일반 터파기 | 흙막이 BIM(CFA, H-Pile, SCW) + 계측 연동 |
| 운영 시스템 | 독립 FM | ATP/ATO/SCADA·스크린도어 시스템과 연동 |

### 1.2 프로젝트 유형별 BIM 적용 범위

- **신규 노선 건설**: 설계 단계부터 IFC 4.3 Alignment로 선형 확정 → 역사 설계 연계
- **기존 역사 리모델링**: 레이저 스캔(점군) → Revit/Recap 역모델링 → 간섭 검토
- **연장·분기 공사**: 기존 선로와 새 선형의 IFC Alignment 조인트 관리가 핵심
- **스마트역사 전환**: FM 시스템 연동을 위한 COBie 데이터 정리

---

## 2. BIM 필수 파라미터 목록

### 2.1 IFC Property Set 기준 파라미터

```
Pset_SpaceCommon (공간 공통)
  - GrossFloorArea: 바닥면적 (m²)
  - NetFloorArea: 순 사용면적 (m²)
  - IsExternal: 외부공간 여부

Pset_BuildingElementProxyCommon (특수 요소)
  - Reference: 요소 코드 (예: PLT-B1-01)
  - Status: 시공 상태 (Design/Approved/Installed)
```

### 2.2 지하철역사 특화 파라미터

| 파라미터명 | 데이터 타입 | 단위 | 설명 |
|-----------|------------|------|------|
| Station_Code | IfcLabel | - | 역 코드 (예: 2-235) |
| Platform_Type | IfcLabel | - | 섬식/상대식/복합식 |
| Platform_Length | IfcLengthMeasure | m | 승강장 유효 길이 |
| Platform_Level | IfcLengthMeasure | m | 레일면 기준 승강장 높이 |
| Concourse_Zone | IfcLabel | - | 대합실 구역 분류 (유개/유료) |
| FireZone_ID | IfcLabel | - | 방재구획 번호 |
| SmokeControl_Zone | IfcLabel | - | 제연구역 번호 |
| ExitCapacity | IfcCountMeasure | 인/분 | 출구 피난 용량 |
| Track_Gauge | IfcLengthMeasure | mm | 궤간 (표준: 1435mm) |
| TunnelType | IfcLabel | - | 개착/NATM/쉴드 구분 |
| SoilRetention_Method | IfcLabel | - | 흙막이 공법 (CFA/H-Pile/SCW/Top-Down) |
| GroundwaterLevel | IfcLengthMeasure | m | 설계 지하수위 |
| SeismicZone | IfcLabel | - | 내진 구역 (1등급/2등급) |
| PSD_Type | IfcLabel | - | 스크린도어 형식 (전폐형/반높이형) |
| VentilationSystem | IfcLabel | - | 환기 방식 (종류식/횡류식/반횡류식) |

### 2.3 흙막이·토공 BIM 특화 파라미터

```
Pset_EarthRetainingWall (흙막이벽 속성)
  - RetainingMethod: CFA_Pile / H_Pile_Lagging / SCW / Diaphragm_Wall
  - EmbeddedDepth: 근입 깊이 (m)
  - WallThickness: 벽체 두께 (mm)
  - AnchoryType: 앵커 형식 (Earth_Anchor / Strut / Raker)
  - AnchorSpacing_H: 수평 간격 (m)
  - AnchorSpacing_V: 수직 간격 (m)
  - MonitoringPoint_ID: 계측 포인트 연계 ID
```

---

## 3. LOD 단계별 요구사항

| LOD | 명칭 | 지하철역사 적용 내용 |
|-----|------|---------------------|
| LOD 100 | 개념 설계 | 역사 위치·승강장 형식·출구 개수 매스 표현 |
| LOD 200 | 기본 설계 | 대합실/승강장 공간 분리, 구조 형식 확정, 흙막이 위치 |
| LOD 300 | 실시 설계 | 전체 구조·건축·MEP 실시 BIM, 간섭 검토 완료 |
| LOD 350 | 시공 조정 | 철근 상세, 흙막이 단계별 시공 BIM, 4D 시뮬레이션 |
| LOD 400 | 제작·시공 | PC 프리캐스트 부재 제작 BIM, 스크린도어 상세 |
| LOD 500 | 준공 As-Built | 점군+BIM 통합 준공 모델, FM 연동 COBie 완성 |

### 3.1 단계별 핵심 납품물

**LOD 300 필수:**
- 구조 BIM (기둥·보·슬래브·지하벽체)
- MEP BIM (환기·소방·전기 주요 간선)
- 공간 BIM (방재 구획 포함)
- IFC 4.3 Alignment (선로 선형)
- 흙막이 BIM (CIP/H-Pile 위치, 앵커 배치)

**LOD 500 필수:**
- COBie 스프레드시트 (공간-설비 연계)
- 점군 등록 완료 모델
- FM 시스템 연동 속성 완비

---

## 4. IFC Entity 매핑

### 4.1 주요 IFC 엔티티

| 건축 요소 | IFC Entity | 비고 |
|-----------|------------|------|
| 대합실 공간 | IfcSpace (PredefinedType: INTERNAL) | 유개/유료구역 분리 |
| 승강장 | IfcSpace (PredefinedType: EXTERNAL) | 선로 접촉면 별도 처리 |
| 역사 건물 | IfcBuilding | 지하/지상 복합 스토리 |
| 지하층 | IfcBuildingStorey | B1, B2, B3... 레일면 기준 |
| 구조 기둥 | IfcColumn | 지하 구조 기둥 |
| 지하 벽체 | IfcWall (PredefinedType: SHEAR) | 지하 연속벽 포함 |
| 흙막이벽 | IfcCivilElement (커스텀) 또는 IfcBuildingElementProxy | 공법별 세분화 |
| 앵커 | IfcFastener 또는 IfcBuildingElementProxy | |
| 스크린도어 | IfcDoor (PredefinedType: SLIDING) | PSD 파라미터 추가 |
| 에스컬레이터 | IfcTransportElement (PredefinedType: ESCALATOR) | |
| 엘리베이터 | IfcTransportElement (PredefinedType: LIFTCAR) | |

### 4.2 IFC 4.3 인프라 특화 엔티티

```
IfcAlignment
  └─ IfcAlignmentHorizontal (평면 선형)
  └─ IfcAlignmentVertical (종단 선형)
  └─ IfcAlignmentCant (캔트: 곡선부 편기울기)

IfcLinearPlacement → 선로 위 요소 배치 (선형 기준 좌표)
IfcRailway → 철도/도시철도 시설 최상위 컨테이너
IfcRailwayPart → 역사/터널/교량 구역 구분
IfcTrackElement (PredefinedType: RAIL/SLEEPER/RAILPAD)
```

### 4.3 공간 분류 체계 (UniClass/OmniClass)

```
역사 공간 분류 코드 예시:
  Z1001: 대합실 (유개구역)
  Z1002: 대합실 (유료구역)
  Z1003: 승강장
  Z1004: 선로 구역
  Z2001: 기계실 (환기)
  Z2002: 전기실
  Z2003: 변전실
  Z3001: 역무실
  Z3002: 관리 사무실
  Z4001: 화장실
  Z9001: 비상 대피 통로
```

---

## 5. 국가별 기준 차이

### 5.1 한국 (도시철도법·철도건설규칙)

- **도시철도법 시행령**: 역사 규모 기준 (출구 수, 승강장 폭)
- **도시철도 정거장 및 환승·편의시설의 규모 산정 기준**: 승강장 길이·폭, 에스컬레이터 용량
- **소방청 고시**: 도시철도 화재안전기준 — 제연 구역 설정, 방연댐퍼 위치
- **BIM 납품 기준**: 국토교통부 BIM 기본지침서(2022) + 발주처 지침 병행
- **좌표 기준**: TM128 또는 GRS80 기반 Bessel 타원체

### 5.2 일본 (地下鉄 BIM 기준)

- **国土交通省 BIM/CIM 추진 로드맵**: 2023년부터 일정 규모 이상 지하철 공사 BIM 의무화 단계 추진
- **鉄道·運輸機構(JRTT)**: BIM/CIM 가이드라인 적용 — LOD 기준이 한국보다 상세한 편
- **設計要領**: 各鉄道会社別 고유 기준 존재 (도쿄메트로, 오사카지하철 등 별도 요구사항)
- **내진 기준**: 건축기준법 + 鉄道構造物等設計標準 (L1/L2 지진 2단계 설계)
- **소방·방재**: 消防法 + 地下鉄特有 피난 기준 (양방향 피난 500m 이내)

### 5.3 싱가포르 (MRT BIM 납품 요구)

- **LTA (Land Transport Authority) BIM 요구사항**: IFC 4.x 기반 납품 의무
- **CORENET X (BCA)**: 싱가포르 전국 BIM 제출 시스템 — MRT 역사도 동일 플랫폼 사용
- **BIM Essential Guide (LTA판)**: 지하철 특화 BIM 속성 목록 별도 배포
- **LOD 요구**: 설계 단계 LOD 300, 시공 완료 LOD 500 (As-Built) 의무
- **COBie 요구**: 영국식 COBie 변형 사용, FM 연동 필수

### 5.4 유럽 (영국 크로스레일 기준)

- **PAS 1192-2/BS EN ISO 19650**: 정보 관리 프레임워크
- **Crossrail BIM 요건**: 역사별 Independent BIM Execution Plan, 계약 BIM 조항 포함
- **IFC 4.3**: 유럽에서 철도 분야 IFC 4.3 Alignment 표준 선도

---

## 6. 자주 발생하는 BIM 실패 사례 Top 5

### 실패 사례 1: 선로 선형과 역사 BIM 좌표 불일치
**원인**: 토목팀(선형 설계)과 건축팀(역사 설계)이 서로 다른 기준점 사용. 토목팀은 GIS 국가 좌표, 건축팀은 프로젝트 내부 좌표 사용.

**결과**: BIM 통합 시 역사가 선로에서 수십 미터 이탈. IFC 병합 후 간섭 검토 불가.

**해결책**:
1. 착수 단계에서 BEP에 공통 기준점(Shared Coordinate) 명시
2. 토목 BIM에서 Survey Point + Project Base Point 모두 정의
3. 건축 BIM 시작 전 토목 기준 IFC 파일을 링크로 받아 좌표 정렬 확인

---

### 실패 사례 2: 흙막이 단계별 시공 BIM 미작성
**원인**: 흙막이는 "임시 가시설"로 인식, BIM 모델링 대상에서 제외.

**결과**: 지하 굴착 단계에서 앵커와 영구 구조물(기둥, 슬래브) 간섭 발생. 현장 변경으로 공기 3주 지연.

**해결책**:
1. 흙막이 BIM을 별도 모델로 작성 (IfcBuildingElementProxy + 단계 속성)
2. 굴착 단계별 4D 시뮬레이션 — 각 레벨 굴착 시 앵커 위치 간섭 검토
3. LOD 350 단계에서 영구 구조물과 흙막이 통합 간섭 체크 의무화

---

### 실패 사례 3: 제연 구역 BIM과 실제 방화 구획 불일치
**원인**: 건축 BIM(방화벽 위치)과 기계 BIM(제연 덕트·댐퍼 위치)이 독립적으로 작성. 통합 검토 없음.

**결과**: 제연 구획 경계와 방화 구획 경계가 불일치. 소방 사전 협의 단계에서 설계 변경 다수 발생.

**해결책**:
1. 건축 BIM에 방화구획·제연구획 공간(IfcSpace)을 먼저 정의
2. 기계 BIM 팀은 건축 BIM의 구획 경계를 기준으로 댐퍼 위치 결정
3. 설계 단계 소방 BIM 검토 — 방재 시뮬레이션 전 구획 일치 확인 필수

---

### 실패 사례 4: 스크린도어(PSD) BIM 상세 미반영
**원인**: 스크린도어는 시공사 조달 품목으로 인식, 설계 BIM에 매스 수준만 표현.

**결과**: 설치 공사 시 케이블 트레이, 환기 덕트, 방수턱과 간섭. 스크린도어 하부 배선 공간 부족.

**해결책**:
1. PSD 제조사 BIM 라이브러리 조기 확보 (Panasonic, Nabtesco 등)
2. 승강장 BIM에 PSD 프레임·하부 피트·케이블 공간 포함
3. 전기 BIM과 PSD BIM 통합 간섭 검토 LOD 350 단계 의무화

---

### 실패 사례 5: 점군-BIM 준공 모델 불일치 (LOD 500 품질 미달)
**원인**: 준공 시 점군 스캔은 수행했으나, 시공 중 변경된 내용이 BIM에 미반영. 점군과 BIM이 100mm 이상 편차.

**결과**: FM 시스템 연동 시 공간 면적 오류, 설비 위치 오류로 유지보수 혼란.

**해결책**:
1. 시공 단계 변경관리(Change Management) BIM 업데이트 프로세스 수립
2. 주요 구조물 타설 후 부분 스캔 → BIM 즉시 반영 (중간 체크포인트)
3. 준공 전 점군-BIM 편차 허용 기준 설정 (주요 구조: ±25mm 이내)

---

## 7. LUA BIM LABS 사업 기회 및 Add-in 적용 방향

### 7.1 핵심 사업 기회

| 시장 | 기회 내용 | 규모 |
|------|-----------|------|
| 한국 | GTX·수도권 광역급행철도 신규 노선 BIM | 2025~2035 대규모 발주 |
| 일본 | 노후 지하철 리모델링 BIM/CIM 전환 지원 | 도쿄·오사카·나고야 |
| 싱가포르 | LTA MRT 신규 노선 BIM 컨설팅 | CRL, TEL 연장 |
| 중동 | 리야드·두바이 메트로 확장 | Saudi Vision 2030 |

### 7.2 Revit Add-in 적용 방향

**① 지하철 공간 자동 분류기 (Metro Space Classifier)**
- 선택한 IfcSpace에 도시철도 공간 코드 자동 부여
- 유개/유료 구역 경계 자동 산출 (게이트 위치 기반)
- 방재 구획 면적 자동 집계 → 소방 면적 보고서 출력

**② 흙막이 BIM 자동화 도구 (Earth Retention Modeler)**
- 지반 조사 데이터(CSV) → Revit 흙막이 BIM 자동 생성
- 앵커 간격/근입깊이 파라미터 일괄 적용
- 굴착 단계별 시공 Phase 자동 설정

**③ 선형-역사 좌표 정합 도구 (Alignment Connector)**
- IFC 4.3 Alignment 파일 import → Revit 기준점 자동 정렬
- 선로 중심선 기준 승강장 간격 자동 검증
- 좌표 불일치 알림 시스템

**④ 제연 구획 검증 도구 (Smoke Control Verifier)**
- 방화구획 BIM과 제연구획 BIM 자동 비교
- 불일치 구간 색상 강조 + 보고서 자동 생성
- 도시철도 화재안전기준 준수 여부 체크리스트

### 7.3 컨설팅 패키지 제안

- **BEP 수립 패키지**: 지하철역사 특화 BIM Execution Plan 템플릿 제공
- **품질 검증 서비스**: LOD 단계별 납품 BIM 자동 검수 (LUA QA 체계 적용)
- **교육 프로그램**: 지하철 BIM 담당자 교육 (IFC 4.3 Alignment + 좌표 관리)

---

- 관련: [[건물유형별_BIM적용기준]] · [[국가별_건설법규_기준비교]] · [[IFC_OpenBIM]] · [[OpenBIM_프로그램연동]] · [[BIM_납품검수]] · [[해외건설기업_동향분석]]
