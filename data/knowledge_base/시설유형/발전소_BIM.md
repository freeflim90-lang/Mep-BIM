# 발전소 BIM 적용 기준 지식 베이스

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #발전소 #방폭BIM #ASME #원자력BIM #내진설계 #신재생에너지 #공정안전 #SIL #IEC61511
- 업데이트: 2026-05-28

## 발전소 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

### 1.1 일반 건물과의 핵심 차이점

발전소는 에너지 생산을 위한 초고위험 산업 시설이다. 폭발·화재·방사선·고압·고온이 복합되며, 일반 건축 BIM과는 근본적으로 다른 전문성이 요구된다.

| 구분 | 일반 건물 | 발전소 |
|------|-----------|--------|
| 안전 기준 | 건축법 안전 | 공정 안전(PSM), IEC 61511(SIL), ASME 기준 |
| 구조 하중 | 건물 자중·설하중·풍하중 | 터빈 진동 하중, 파이프 반력, 폭발 하중 추가 |
| 배관 시스템 | 일반 위생·설비 배관 | 고압·고온 공정 배관 (ASME B31.1/B31.3) |
| 내진 설계 | 건축법 내진 기준 | 원전: 내진 Category I/II/III 별도 분류 |
| 방폭 구역 | 없음 | Zone 0/1/2 (가연성 가스), Zone 20/21/22 (분진) |
| 방재 | 일반 스프링클러 | CO₂·포소화·불활성가스·VESDA 복합 |
| 전기 시스템 | 일반 상용 전원 | UPS·비상발전기·버스 이중화·비상 전원 분리 |

### 1.2 발전소 유형별 BIM 특성

**화력 발전소 (석탄/LNG/오일)**
- 보일러·터빈·발전기 3대 대형 기계 BIM이 중심
- 연료 공급 시스템(석탄 야드/LNG 저장 탱크) BIM 포함
- 냉각수 취수·방수 설비 BIM

**원자력 발전소**
- 내진 Category I 구조물의 극단적 상세 BIM
- 방사선 차폐 콘크리트(밀도 2.4t/m³ 이상) 두께 BIM
- 格納容器(격납 건물) 특수 BIM — 사전 허가용 BIM 별도 관리
- 비상 노심 냉각 계통(ECCS) BIM

**신재생 에너지**
- 태양광: 패널 배열·구조 BIM + GIS 연동 일사량 시뮬레이션
- 풍력: 타워·블레이드 BIM + 시뮬레이션 영역(Shadow Flicker, Sound)

---

## 2. BIM 필수 파라미터 목록

### 2.1 방폭 구역 (Hazardous Area) 파라미터

```
Pset_HazardousArea (방폭 구역 속성 — 커스텀 Property Set)
  - Zone_Classification: Zone 0 / Zone 1 / Zone 2
                         Zone 20 / Zone 21 / Zone 22 (분진)
  - Gas_Group: IIA / IIB / IIC (가스 그룹)
  - Temperature_Class: T1 / T2 / T3 / T4 / T5 / T6 (발화온도 등급)
  - ATEX_Category: 1G / 2G / 3G (장비 사용 카테고리)
  - Ventilation_Type: Natural / Artificial / Unknown
  - Release_Source: Continuous / Primary / Secondary
  - Standard_Reference: IEC 60079-10-1 / NFPA 497 / NEC 500

Zone 0: 항시 폭발성 가스 분위기 존재 (탱크 내부 등)
Zone 1: 정상 운전 시 폭발성 가스 가능성 있음
Zone 2: 이상 시에만 폭발성 가스 가능성 있음
```

### 2.2 고압 배관 파라미터 (ASME B31.1/B31.3)

| 파라미터명 | 데이터 타입 | 단위 | 설명 |
|-----------|------------|------|------|
| Pipe_Class | IfcLabel | - | 배관 등급 (예: A1B, A2C, ASME B31.1 Class 1) |
| Design_Pressure | IfcPressureMeasure | MPa | 설계 압력 |
| Design_Temperature | IfcThermodynamicTemperatureMeasure | °C | 설계 온도 |
| Operating_Pressure | IfcPressureMeasure | MPa | 운전 압력 |
| Operating_Temperature | IfcThermodynamicTemperatureMeasure | °C | 운전 온도 |
| Material_Grade | IfcLabel | - | 배관 재료 (예: SA-335 P11, SA-106 Gr.B) |
| Insulation_Type | IfcLabel | - | 단열 형식 (Hot/Cold/Personal Protection) |
| Insulation_Thickness | IfcLengthMeasure | mm | 단열재 두께 |
| Fluid_Service | IfcLabel | - | 유체 서비스 (Normal/Severe/High-Pressure) |
| NDE_Requirement | IfcLabel | - | 비파괴검사 요건 (100%RT/US/PT) |
| Stress_Analysis_ID | IfcLabel | - | 응력 해석 번호 연계 |

### 2.3 원전 내진 분류 파라미터

```
Pset_NuclearSeismicCategory
  - Seismic_Category: Category_I / Category_II / Category_III / Non-Seismic
  - SSE_Level: Safe Shutdown Earthquake (g 단위)
  - OBE_Level: Operating Basis Earthquake (g 단위)
  - Safety_Class: SC-1 / SC-2 / SC-3 / Non-Safety
  - Quality_Group: A / B / C / D (ASME Nuclear Code)
  - Environmental_Qualification: 10CFR50 Appendix B 준수 여부
  - Documentation_Ref: UFSAR 참조 섹션

Category I: 안전 기능 관련 — 지진 후 기능 유지 필수
Category II: Category I 붕괴 방지 관련
Category III: 안전 관련 없음
```

### 2.4 신재생 BIM 특화 파라미터

```
Pset_SolarPanel
  - Panel_Manufacturer: 제조사
  - Panel_Model: 모델명
  - Peak_Power: 최대 출력 (Wp)
  - Panel_Efficiency: 효율 (%)
  - Tilt_Angle: 경사각 (°)
  - Azimuth_Angle: 방위각 (°)
  - Array_ID: 어레이 번호
  - StringCount: 직렬 수
  - InverterID: 연계 인버터 ID

Pset_WindTurbine
  - Turbine_Manufacturer: 제조사
  - Hub_Height: 허브 높이 (m)
  - Rotor_Diameter: 로터 직경 (m)
  - Rated_Power: 정격 출력 (kW)
  - Cut_In_Speed: 기동 풍속 (m/s)
  - Rated_Wind_Speed: 정격 풍속 (m/s)
  - Cut_Out_Speed: 정지 풍속 (m/s)
  - IEC_Class: IEC 61400 등급 (IA/IB/IIA/IIB/IIIA)
```

---

## 3. LOD 단계별 요구사항

| LOD | 발전소 적용 내용 |
|-----|-----------------|
| LOD 100 | 발전 방식·용량·부지 위치 매스 |
| LOD 200 | 주요 건물 배치, 터빈 홀·보일러 홀 형태, 방폭 구역 개략 |
| LOD 300 | 전체 건축·구조·공정 배관 BIM, 방폭 구역 3D 경계, 대형 기계 배치 |
| LOD 350 | 공정 배관 간섭 검토, 기계 접근 통로, 유지보수 공간 확보 BIM |
| LOD 400 | 배관 스풀 BIM, 철골 제작 BIM, 콘크리트 철근 BIM |
| LOD 500 | As-Built 준공 BIM, P&ID 연계, 운영 CMMS 연동 |

### 3.1 원전 BIM 특수 요구사항

원전은 설계 수명이 60~80년이며 규제기관(NRC/NSSC) 검토용 BIM이 별도 요구된다.

- **규제 제출용 BIM**: 인허가 도서 대체 BIM — 정확도 최우선
- **BIM 검증 프로세스**: 제3자 BIM 검증 (Peer Review) 의무
- **변경 관리**: 10CFR50 App. B 기반 BIM 변경 관리 절차 수립
- **원전 방화 BIM**: NRC 규제 10CFR50 App. R — 방화 구획 BIM

---

## 4. IFC Entity 매핑

### 4.1 발전소 특화 IFC 엔티티

| 요소 | IFC Entity | 비고 |
|------|------------|------|
| 터빈 건물 | IfcBuilding | |
| 보일러 | IfcBuildingElementProxy (Boiler) | 기계 BIM 별도 |
| 터빈 | IfcBuildingElementProxy (Turbine) | 기계 BIM 별도 |
| 발전기 | IfcElectricGenerator | |
| 냉각탑 | IfcCoolingTower | |
| 고압 배관 | IfcPipeSegment + IfcPipeFitting | ASME 등급 파라미터 필수 |
| 방폭 구역 경계 | IfcZone + IfcSpace | Zone 0/1/2 속성 |
| 압력용기 | IfcBuildingElementProxy (Vessel) | |
| 히트 익스체인저 | IfcHeatExchanger | |
| 펌프 | IfcPump | |
| 압축기 | IfcCompressor | |
| 원자로 격납 건물 | IfcBuilding (Containment) | 별도 BIM 파일 |
| 태양광 패널 | IfcPlate 또는 IfcBuildingElementProxy | |
| 풍력 타워 | IfcColumn (Tower) | |

### 4.2 방폭 구역 3D 표현

```
방폭 구역 BIM 모델링 접근법:
  1. 각 방폭 구역을 IfcSpace로 표현
  2. 방폭 구역 경계는 3D 볼륨으로 정의
  3. Zone 속성을 IfcSpace의 커스텀 Property Set에 입력
  4. 해당 Zone 내 모든 전기·계장 장비에 ATEX 등급 파라미터 연계
  5. Zone별 색상 구분: Zone 0=Red, Zone 1=Orange, Zone 2=Yellow

Dynamo 활용:
  - 방폭 Release Source(위험 물질 방출 지점) 좌표 입력
  - 가스 그룹·환기 조건 기반 Zone 반경 자동 산출
  - Zone 볼륨 자동 생성 + 내부 장비 자동 색상 분류
```

---

## 5. 국가별 기준 차이

### 5.1 한국 (전기사업법·산업안전보건법)

- **전기사업법**: 발전사업 허가 및 공사계획 인가 — BIM이 인허가 도서 역할 준용 추진
- **산업안전보건법 (PSM)**: 공정 안전 관리 — 발전소는 PSM 12개 요소 이행
  - P&ID, 공정위험성 평가(HAZOP), 비상 조치 계획
  - BIM-P&ID 연계가 핵심 과제
- **원자력안전법**: 원자력안전위원회(NSSC) 허가 — 미국 NRC 기준과 유사
- **내진 설계**: 건축구조기준(KBC) + 원자력 시설물의 내진 설계 기준 (KNS-N601)
- **방폭 기준**: KS C IEC 60079 (국제 기준 부합화), KOSHA 방폭 지침

### 5.2 미국 (ASME·NFPA·NRC 기준)

- **ASME Boiler & Pressure Vessel Code (BPVC)**: 압력용기 설계·제작 기준
  - Section I: 발전 보일러, Section VIII: 압력용기, Section III: 원전 기기
- **ASME B31.1**: 발전 배관 (Power Piping), B31.3: 공정 배관
- **NFPA 850**: 화력 발전소 화재 방호 기준
- **10CFR50**: 원전 허가 기준 (Appendix A: GDC, Appendix B: QA, Appendix R: 화재)
- **NEC Article 500**: 방폭 전기 설비 기준 (Zone 방식 또는 Division 방식)

### 5.3 유럽 (ATEX 지침)

- **ATEX 지침 (2014/34/EU + 1999/92/EC)**: 방폭 장비·설치 의무 기준
- **IEC 60079 시리즈**: 국제 방폭 기준 (한국 KS IEC도 동일 체계)
- **EN 13463**: 비전기적 방폭 장비 기준
- **유럽원자력공동체 (Euratom)**: 원전 규제 기준 — 각국 별도 적용

---

## 6. 자주 발생하는 BIM 실패 사례 Top 5

### 실패 사례 1: 공정 배관 BIM과 P&ID 불일치
**원인**: P&ID(프로세스 설계)와 배관 BIM(3D 설계)이 별도 팀에서 독립적으로 작성. 설계 변경 시 P&ID는 수정됐으나 BIM 미반영.

**결과**: 시공 단계 배관 루프 검사(Piping Loop Check) 시 P&ID와 BIM 불일치 대거 발견. 재설계 비용 20억 원.

**해결책**:
1. P&ID 소프트웨어(AVEVA/SmartPlant P&ID)와 BIM 연동 체계 구축
2. 설계 변경 시 P&ID-BIM 동시 업데이트 의무화
3. ISOGEN(배관 ISO 자동 생성) BIM 연계로 P&ID-BIM-배관도 삼각 검증

---

### 실패 사례 2: 방폭 구역 내 非방폭 장비 설치
**원인**: 방폭 구역(Zone 1)이 BIM에 정의됐으나, 전기 BIM 팀이 방폭 구역 속성 미확인. 일반 모터·스위치 BIM으로 배치.

**결과**: 시공 완료 후 ATEX 검사에서 Zone 1 내 일반 전기 장비 대량 적발. 전면 교체 비용 30억 원.

**해결책**:
1. BIM 방폭 구역 내 장비 배치 시 ATEX 등급 파라미터 자동 체크
2. 방폭 구역과 장비 ATEX 등급 불일치 시 Revit 경고 알림 Add-in
3. 전기 BIM 납품 전 방폭 구역 준수 자동 검증 보고서 의무화

---

### 실패 사례 3: 터빈 유지보수 공간 미확보
**원인**: 터빈 BIM 모델링 시 운전 정지 상태(Static)만 표현. 정비 시 블레이드 인출, 크레인 접근 공간 미검토.

**결과**: 현장 설치 후 터빈 분해 검사(Overhaul) 시 기존 배관·강구조물과 충돌. 정비 공간 확보를 위해 배관 재배치.

**해결책**:
1. 터빈 BIM에 유지보수 동적 범위(Maintenance Envelope) 포함
2. EOT 크레인 이동 범위 BIM 시뮬레이션 — 간섭 구간 사전 제거
3. OEM 제조사 유지보수 요건 BIM 패밀리에 반영 (크레인 반경, 작업 공간)

---

### 실패 사례 4: 원전 내진 Category I 구조물 BIM 정확도 미달
**원인**: 원전 격납 건물 BIM을 일반 콘크리트 구조물과 동일한 LOD 300 수준으로 작성. 철근 상세, 앵커 플레이트 위치 미표현.

**결과**: NRC/NSSC 규제 검토 시 BIM 정확도 부족으로 인허가 지연 6개월.

**해결책**:
1. Category I 구조물은 LOD 400 수준 BIM 의무화
2. 철근 3D 모델링(Revit Structure/Tekla) + 앵커 플레이트 상세 포함
3. 원전 BIM 전담 팀 구성 — 일반 BIM 팀과 분리 관리

---

### 실패 사례 5: 태양광 BIM 지붕 하중 검토 누락
**원인**: 태양광 패널 BIM을 외관 설계 단계에서 추가. 기존 구조 BIM 하중 재검토 없이 패널 배치.

**결과**: 지붕 구조물 처짐 한계 초과. 철골 보강 공사 추가 발생.

**해결책**:
1. 태양광 패널 BIM에 단위 면적당 하중 파라미터 필수 입력
2. 패널 배치 변경 시 구조 BIM 자동 연계 하중 재산출
3. Dynamo로 패널 면적-하중-구조 허용하중 자동 비교 스크립트

---

## 7. LUA BIM LABS 사업 기회 및 Add-in 적용 방향

### 7.1 핵심 사업 기회

| 시장 | 기회 내용 | 규모 |
|------|-----------|------|
| 한국 | 신재생 에너지 BIM 의무화 확산, 원전 계속 운전 BIM | 급성장 |
| 일본 | 원전 재가동 BIM 지원, 재생에너지 목표 50% (2030) | 대형 수요 |
| 중동 | UAE Barakah 원전 운영 BIM, 태양광 NEOM | 중동 에너지 전환 |
| 북미 | SMR(소형모듈원전) BIM 컨설팅 | 차세대 원전 급증 |

### 7.2 Revit Add-in 적용 방향

**① 방폭 구역 자동 생성기 (Hazardous Zone Generator)**
- 위험 물질 방출 지점(Release Source) 입력 → Zone 0/1/2 자동 생성
- IEC 60079-10-1 기반 거리·환기 조건 자동 산출
- Zone 내 장비 ATEX 등급 자동 검증 + 부적합 알림

**② P&ID-BIM 자동 정합 도구 (P&ID Reconciler)**
- AVEVA/SmartPlant P&ID XML → Revit BIM 자동 대조
- 불일치 항목(Line Number, Valve, Equipment) 자동 추출
- 불일치 보고서 자동 생성

**③ 유지보수 공간 자동 확보 검증기 (Maintenance Clearance Checker)**
- 회전 기계(터빈/펌프/압축기) 유지보수 엔벨로프 자동 생성
- 크레인 이동 범위 자동 BIM + 간섭 검토
- 접근 통로(600mm 이상) 자동 검증

**④ 신재생 BIM 하중 검토기 (PV Load Analyzer)**
- 태양광 패널 배치 BIM → 지붕 하중 자동 산출
- 경사각·방위각 최적화 시뮬레이션
- 구조 허용하중 초과 구간 자동 알림

---

- 관련: [[건물유형별_BIM적용기준]] · [[국가별_건설법규_기준비교]] · [[IFC_OpenBIM]] · [[OpenBIM_프로그램연동]] · [[BIM_납품검수]] · [[해외건설기업_동향분석]]
