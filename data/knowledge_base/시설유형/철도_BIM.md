# 철도 BIM 적용 기준 지식 베이스

## 2026-06-05 국내 철도 BIM 지침 2025~2026 최신 업데이트
- Source: 국가철도공단 BIM 적용지침(2023.11), 서울형 설계 BIM 적용지침(철도설계편, 2025.06), 철도공단 BIM 대가 기준 수립 용역
- Tags: railway,bim,ifc43,alignment,national-railroad,2026

**AI 즉시 답변 패턴 — "철도 BIM 납품 기준이 어떻게 되나요?"**
```
국가철도공단 BIM 적용지침(2023.11) 기준:
- 기본설계: 교량·터널·역사 LOD 300
- 실시설계: 교량·터널·역사 LOD 350
- 철도 특화 IFC: IFC 4.3 (IfcAlignment·IfcBridge 활용)
- 4D 공정: 철도 공종별 TimeLiner 연동
- BIM 대가: 철도공단 대가 기준 수립 용역 진행 중(2025)

서울형 철도설계 BIM 지침(2025.06):
- 서울시 철도 사업(도시철도·경전철)에 적용
- 서울시 디지털트윈 연계 고려
```

**철도 BIM 공종별 특수 요건:**
| 공종 | 핵심 BIM 항목 | LOD |
|------|-------------|-----|
| 선로·토공 | IFC 4.3 Alignment, 성토·절토 | 300 |
| 교량 | IfcBridge, 거더·기초·신축이음 | 350 |
| 터널 | 라이닝·인버트·방수 | 300 |
| 역사 | 건축+MEP (지하철역 기준) | 350 |
| 전철 설비 | 가공선·전기 계통 | 300 |

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #철도 #IFC4.3 #Alignment #IfcAlignment #선형모델링 #철도BIM #토목BIM #4D시뮬레이션
- 업데이트: 2026-06-05

## 철도 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

### 1.1 일반 건물과의 핵심 차이점

철도 시설 BIM은 선형 인프라(Linear Infrastructure)가 핵심이다. 수km~수백km의 노선이 기준이 되며, 이를 중심으로 교량·터널·토공·역사가 배치된다. IFC 4.3부터 공식 도입된 `IfcAlignment`이 철도 BIM의 핵심 엔티티다.

| 구분 | 일반 건물 | 철도 시설 |
|------|-----------|-----------|
| 기준 좌표 | 로컬 기준점 | GIS 국가 좌표 + 철도 킬로포스트(KP) |
| 설계 기준선 | 없음 | 선형(Alignment) — 모든 요소의 배치 기준 |
| 시설 범위 | 단일 부지 | 수십~수백 km 선형 구조물 연속 |
| 구조물 형식 | 일반 건축 | 교량/터널/토공/고가/지하 복합 |
| 시공 순서 | 비교적 자유 | 선형 기준 구간별 순서 엄격 (4D 필수) |
| 유지관리 | 건물 FM | 선로 유지보수 시스템(PMS) 연동 필요 |

### 1.2 철도 BIM 구성 요소

```
철도 BIM 전체 구성:
  1. 선형 BIM (IfcAlignment): 평면/종단/횡단/캔트
  2. 토공 BIM: 성토·절토·흙막이
  3. 교량 BIM: 상부구조(거더)/하부구조(교각·교대)/기초
  4. 터널 BIM: 라이닝/갱문/환기/방수
  5. 궤도 BIM: 레일/침목/도상(자갈/콘크리트)
  6. 전차선 BIM: 전차선로/전주/변전소
  7. 신호 BIM: 신호기/ATC/ATP/연동장치
  8. 역사 BIM: 플랫폼/대합실/역무시설
  9. 통신 BIM: 무선/유선/CCTV
```

---

## 2. BIM 필수 파라미터 목록

### 2.1 IFC 4.3 Alignment 핵심 파라미터

```
IfcAlignmentHorizontal (평면 선형 세그먼트)
  - DesignParameters.StartPoint: 시작점 (Easting, Northing)
  - DesignParameters.StartDirection: 시작 방위각 (라디안)
  - DesignParameters.SegmentLength: 세그먼트 길이 (m)
  - DesignParameters.RadiusStart: 시작 반경 (m, 직선=∞)
  - DesignParameters.RadiusEnd: 종단 반경 (m)
  - PredefinedType: LINE / CIRCULARARC / CLOTHOID / CUBIC

IfcAlignmentVertical (종단 선형)
  - StartDistAlong: 시작 거리 (m, KP 기준)
  - HorizontalLength: 수평 거리 (m)
  - StartGradient: 시작 구배 (소수점, 예: 0.02 = 2%)
  - EndGradient: 종단 구배 (m)
  - RadiusOfCurvature: 종단 곡선 반경 (m)
  - PredefinedType: CONSTANTGRADIENT / CIRCULARARC / PARABOLICARC

IfcAlignmentCant (캔트 — 곡선부 편기울기)
  - StartDistAlong: 시작 거리
  - HorizontalLength: 적용 구간 길이
  - StartCantLeft, StartCantRight: 좌우 캔트 시작값 (m)
  - EndCantLeft, EndCantRight: 좌우 캔트 종료값 (m)
```

### 2.2 철도 시설 특화 파라미터

| 파라미터명 | 데이터 타입 | 단위 | 설명 |
|-----------|------------|------|------|
| KilometerPost | IfcLengthMeasure | m | 킬로포스트 (노선 거리) |
| TrackGauge | IfcLengthMeasure | mm | 궤간 (표준: 1435mm) |
| DesignSpeed | IfcLinearVelocityMeasure | km/h | 설계 속도 |
| MaxOperatingSpeed | IfcLinearVelocityMeasure | km/h | 최고 운행 속도 |
| Cant_Design | IfcLengthMeasure | mm | 설계 캔트값 |
| Cant_Max | IfcLengthMeasure | mm | 최대 캔트 허용값 |
| MinCurveRadius | IfcLengthMeasure | m | 최소 곡선 반경 |
| GradientValue | IfcRatioMeasure | % | 구배값 |
| Structure_Type | IfcLabel | - | 토공/교량/터널/지하 구분 |
| Rail_Type | IfcLabel | - | 50N/60Kg/UIC54 등 |
| Sleeper_Type | IfcLabel | - | PC/목침목/합성침목 |
| Track_Structure | IfcLabel | - | 자갈도상/콘크리트도상 |
| Catenary_Voltage | IfcElectricVoltageMeasure | kV | 전차선 전압 (25kV/1.5kV/3kV) |
| Signal_System | IfcLabel | - | ATC/ATP/ATO/ATCS |
| BridgeLength | IfcLengthMeasure | m | 교량 연장 |
| TunnelLength | IfcLengthMeasure | m | 터널 연장 |
| TunnelMethod | IfcLabel | - | NATM/쉴드/개착 |

### 2.3 교량 BIM 특화 파라미터

```
Pset_BridgeCommon
  - BridgeType: 교량 형식 (PSC Box / RC Box / Steel Box / I-Girder / Arch)
  - SpanCount: 경간 수
  - MaxSpanLength: 최대 경간 길이 (m)
  - SuperstructureType: 상부구조 형식
  - SubstructureType: 하부구조 형식 (원형교각/사각교각/교대)
  - FoundationType: 기초 형식 (직접기초/말뚝기초/케이슨)
  - SeismicCategory: 내진 등급 (1등급/2등급)
  - DesignLoad: 설계 하중 (HL-93 / KS 기준)
  - MaintenanceCategory: 유지관리 등급
```

---

## 3. LOD 단계별 요구사항

| LOD | 명칭 | 철도 시설 적용 내용 |
|-----|------|---------------------|
| LOD 100 | 개념 선형 | 개략 선형 (직선+원곡선), 노선 길이, 역사 위치 |
| LOD 200 | 기본 설계 선형 | 완성된 평면/종단/횡단 선형, 구조물 형식 결정 |
| LOD 300 | 실시 설계 | 전체 토목/건축/궤도/전기/신호 실시 BIM |
| LOD 350 | 시공 조정 | 4D 시공 시뮬레이션, 교량 가설 공법 BIM |
| LOD 400 | 제작 BIM | PC 거더 제작 BIM, 전주 기초 상세 BIM |
| LOD 500 | As-Built | 준공 선형+구조물 BIM, 궤도 검측 데이터 연동 |

### 3.1 철도 BIM 4D 시뮬레이션 특화

철도는 선형을 따라 구간별로 시공이 진행되므로, 4D 시뮬레이션이 일반 건물보다 훨씬 중요하다.

```
4D 시뮬레이션 단계별 표현:
  Phase 1: 용지 보상·가이설·가도로 공사
  Phase 2: 토공(절토·성토) 공사
  Phase 3: 교량 하부구조(교각·교대) 공사
  Phase 4: 교량 상부구조(거더 가설) 공사
  Phase 5: 터널 굴착 (막장별 진행률)
  Phase 6: 궤도 부설 (KP별 진행률)
  Phase 7: 전차선 설치
  Phase 8: 신호·통신 설치
  Phase 9: 시험 운행·개통
```

---

## 4. IFC Entity 매핑

### 4.1 IFC 4.3 철도 특화 엔티티

```
IfcRailway (최상위 철도 시설 컨테이너)
  └─ IfcRailwayPart
      ├─ PredefinedType: TRACKSTRUCTURE (궤도 구조)
      ├─ PredefinedType: TRACKSTRUCTUREPART
      ├─ PredefinedType: LINESIDESTRUCTURE (선로 변 시설)
      └─ PredefinedType: DILATATIONSUPERSTRUCTURE

IfcTrackElement
  ├─ PredefinedType: RAIL (레일)
  ├─ PredefinedType: SLEEPER (침목)
  ├─ PredefinedType: RAILPAD (레일 패드)
  ├─ PredefinedType: BASEPLATE (체결 장치)
  ├─ PredefinedType: AUDIENCETERRACE (철도 요소 포함)
  └─ PredefinedType: DERAILER (탈선 방지)

IfcLinearPlacement → 선형(Alignment) 기준 모든 요소 배치
IfcOffsetCurveByDistances → KP 기반 배치 기준선

IfcBridge
  ├─ IfcBridgePart (상부구조/하부구조/기초 구분)
  └─ IfcBearing (교량 받침)

IfcTunnel
  └─ IfcTunnelPart (라이닝/갱문/환기/방수 구분)

IfcAlignment (선형 정의)
  ├─ IfcAlignmentHorizontal
  ├─ IfcAlignmentVertical
  └─ IfcAlignmentCant
```

### 4.2 신호·전기 IFC 매핑

| 요소 | IFC Entity | 비고 |
|------|------------|------|
| 신호기 | IfcSignal (IFC 4.3) | 색등신호기/입환신호기 |
| 전주 | IfcElectricDistributionBoard (커스텀) | 전차선 전주 |
| 변전소 | IfcBuilding (별도) | 급전 구분소 포함 |
| ATC/ATP 지상자 | IfcBuildingElementProxy | 선형 기준 위치 |
| 건널목 | IfcCrossing (IFC 4.3) | 도로-철도 교차 |

---

## 5. 국가별 기준 차이

### 5.1 한국 (철도건설규칙·국가철도공단)

- **철도건설규칙**: 선형 기준 (최소 곡선 반경, 최급 구배, 캔트 기준)
  - 고속철도: 최소 R=7,000m, 최급 구배 35‰
  - 일반철도: 최소 R=400m, 최급 구배 25‰
- **국가철도공단(KR) BIM 지침**: 철도 설계 BIM 납품 기준 (2022 개정)
  - IFC 4.0 기반 (IFC 4.3 전환 추진 중)
  - 선형 BIM 필수, 구조물별 LOD 300 이상
- **한국철도표준(KRS)**: 궤도 구조, 전차선, 신호 설계 기준

### 5.2 일본 (鉄道設計要領)

- **鉄道·運輸機構(JRTT) BIM/CIM 가이드라인**: 2022년 전면 개정
  - IFC 4.3 Alignment 채택 확정
  - 터널·교량 LOD 400 수준 상세 요구
- **新幹線 설계 기준**: JR 각 사별 고유 기준 (JR東日本, JR西日本 등)
  - 신칸센 최소 R=4,000m, 최급 구배 15‰
- **鉄道構造物等設計標準**: 교량·터널·토공 상세 설계 기준

### 5.3 유럽 (HS2 BIM 요건)

- **HS2 (High Speed 2, 영국)**: 세계 최고 수준 철도 BIM 요건
  - ISO 19650 완전 준수
  - IFC 4.3 Alignment 전면 채택
  - 단계별 BIM 실행계획(BEP) + 정보 제공 요건(EIR) 체계 완비
  - CDE (Common Data Environment) 의무 사용
- **Crossrail (Elizabeth Line)**: 런던 지하철 확장 — 복잡한 도심 지하 선형 BIM 모범 사례
- **ETCS (European Train Control System)**: 유럽 통합 신호 시스템 BIM 표현 기준

### 5.4 미국 (AREMA·FRA 기준)

- **AREMA (American Railway Engineering and Maintenance)**: 철도 설계 표준
- **FRA (Federal Railroad Administration)**: 철도 안전 기준
- **BIM 요구**: MAP-21/FAST Act 연방 예산 — BIM 요건 점진 강화
- **AASHTO**: 교량 설계 기준 (HL-93 하중 모델)

---

## 6. 자주 발생하는 BIM 실패 사례 Top 5

### 실패 사례 1: 선형(Alignment) 미확정 상태에서 구조물 BIM 선행
**원인**: 선형 설계 완료 전 교량·터널 구조물 BIM 작성 착수. 선형 변경 시 구조물 BIM 전면 재작성 필요.

**결과**: 선형 2회 수정으로 교량 BIM 3회 재작성. 설계 기간 2개월 추가 소요.

**해결책**:
1. 선형 확정(동결) 이후 구조물 BIM 착수 원칙 수립
2. IFC 4.3 IfcLinearPlacement 기반 모델링 — 선형 변경 시 구조물 자동 이동
3. 선형 변경 영향 구조물 자동 추출 Add-in 활용

---

### 실패 사례 2: 교량-터널 접속부 BIM 공백 구간 발생
**원인**: 교량 BIM(토목 팀 A)과 터널 BIM(토목 팀 B)이 접속부를 서로 상대방 범위로 인식. 교대-갱문 접속 구간 BIM 누락.

**결과**: 실시 설계 납품 시 접속부 배수·방수 설계 누락 확인. 현장 타설 후 누수 발생.

**해결책**:
1. BEP에 구조물 간 접속부(Interface) 담당 팀 명시
2. 접속부 BIM은 두 팀 중 한 팀이 전담 (중복 작성 + 통합)
3. 접속부 검토 게이트 도입 (LOD 200 단계에서 접속부 확인)

---

### 실패 사례 3: 4D 시뮬레이션 없이 교량 가설 공법 결정
**원인**: 도심 구간 교량 가설 공법(ILM, FCM, MSS 등)을 BIM 시뮬레이션 없이 도면으로만 검토. 인접 도로·건물과의 간섭 미확인.

**결과**: MSS(이동식 비계) 설치 시 인접 건물과 간섭. 공법 변경으로 공사비 15억 원 추가 발생.

**해결책**:
1. 교량 가설 단계별 4D BIM 시뮬레이션 필수화
2. Navisworks TimeLiner + 가설 공법 BIM 패밀리 라이브러리 구축
3. 도심 구간 교량 가설 사전 주민 설명 시 4D 영상 활용

---

### 실패 사례 4: 전차선 BIM과 건축 한계 간섭 미검토
**원인**: 전차선 BIM(전기 팀)과 구조 BIM(토목 팀)의 통합 검토 미실시. 전차선 가동 브래킷이 차량 건축 한계를 침범.

**결과**: 현장 설치 후 전차선 재위치 조정 필요. 전주 12기 재시공.

**해결책**:
1. 차량 건축 한계(Kinematic Envelope)를 BIM에 3D 형상으로 표현
2. 전차선 BIM + 건축 한계 자동 간섭 검토 스크립트
3. 곡선부 건축 한계 확대(Overthrow/Lean) 자동 산출 파라미터 적용

---

### 실패 사례 5: GIS 좌표-BIM 좌표 변환 오류
**원인**: GIS 원점(TM 좌표)에서 BIM 내부 좌표로 변환 시 부동소수점 오류. 수치 범위 초과로 Revit 내부 좌표 정확도 저하.

**결과**: 10km 구간 BIM 모델 좌표가 수십 mm 오차 누적. 측량 검수 시 불합격.

**해결책**:
1. Revit 내부 좌표 원점은 실제 시공 위치 부근으로 이동 (GIS 원점에서 분리)
2. Survey Point(GIS 좌표)와 Project Base Point(BIM 내부 원점) 분리 관리
3. 구간별 BIM 파일 분할 — 단일 파일 내 좌표 범위 ±10km 이내 유지

---

## 7. LUA BIM LABS 사업 기회 및 Add-in 적용 방향

### 7.1 핵심 사업 기회

| 시장 | 기회 내용 | 규모 |
|------|-----------|------|
| 한국 | GTX·수도권 광역철도·동해선·서해선 등 신규 철도 BIM | 2025~2040 |
| 일본 | リニア(마그레브)·신칸센 연장 BIM/CIM | 대형 국가 프로젝트 |
| 싱가포르 | HSR(KL-Singapore) 재추진 시 BIM 컨설팅 | |
| 중동 | 사우디 네옴 철도·UAE 노선 BIM | Vision 2030 |
| 유럽 | HS2 하도급 BIM 컨설팅 | 영국 고속철도 |

### 7.2 Revit Add-in 적용 방향

**① 선형 기반 구조물 자동 배치 (Linear Structure Placer)**
- IFC 4.3 Alignment 파일 Import → Revit 선형 자동 생성
- KP(킬로포스트) 기반 교각·전주·신호기 자동 배치
- 선형 변경 시 배치 요소 자동 업데이트

**② 건축 한계 자동 검증기 (Kinematic Envelope Checker)**
- 차량 건축 한계 3D 표현 (설계 속도·곡선 반경 기반 자동 산출)
- 전차선·신호기·교량 하부 구조물 건축 한계 자동 간섭 검토
- 곡선부 Overthrow/Lean 자동 계산

**③ 철도 BIM 4D 시공 자동화 (Railway 4D Scheduler)**
- 구간별 시공 Phase 자동 할당 (KP 범위 입력)
- Navisworks 내보내기 + TimeLiner 일정 자동 연동
- 주공정 변경 시 4D 자동 재생성

**④ 궤도 파라미터 자동 산출기 (Track Parameter Calculator)**
- 선형 데이터 → 캔트·최소 곡선 반경·완화 곡선 자동 검증
- 설계 속도별 기준값 자동 비교 (철도건설규칙/JIS/EN 기준 선택)
- 기준 초과 구간 자동 강조 + 보고서 생성

### 7.3 컨설팅 패키지 제안

- **IFC 4.3 Alignment 전환 컨설팅**: 기존 2D 선형 설계 → IFC 4.3 BIM 전환
- **철도 BIM 품질 검수**: LOD 단계별 납품 BIM 자동 검수 (선형 일치, 파라미터 완비)
- **4D 시공 계획 서비스**: 교량 가설 공법 BIM 시뮬레이션 전문 서비스

---

- 관련: [[건물유형별_BIM적용기준]] · [[국가별_건설법규_기준비교]] · [[IFC_OpenBIM]] · [[OpenBIM_프로그램연동]] · [[BIM_납품검수]] · [[해외건설기업_동향분석]]
