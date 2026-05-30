# 병원·의료시설 BIM 적용 기준 지식 베이스

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #병원BIM #의료시설 #감염구획 #의료가스 #방사선차폐 #MRI실 #음압격리 #FGI #의료법
- 업데이트: 2026-05-28

## 병원·의료시설 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

### 1.1 일반 건물과의 핵심 차이점

병원은 환자 안전이 최우선인 특수 시설이다. 감염 제어, 의료 가스 공급, 방사선 차폐, 극도의 신뢰성 있는 전원 공급이 BIM에 직접 반영된다.

| 구분 | 일반 건물 | 병원·의료시설 |
|------|-----------|--------------|
| 공간 분류 | 건축 용도 | 감염 구획(오염/준오염/청결/준청결) |
| 배관 시스템 | 위생·급수배관 | 의료 가스 시스템 (O₂·N₂O·진공·공기·마취가스) |
| 전기 시스템 | 일반 상용 전원 | 비상 전원 의무 (UPS + 비상 발전기), IT 접지 계통 |
| 차폐 설계 | 없음 | 방사선 차폐 (납 동등 두께, Pb 당량) |
| 내부 환경 | 일반 공조 | 무균 수술실 층류 기류, 음압격리병실, 양압격리 |
| 법규 | 건축법 | 의료법·의료기관 인증 기준·FGI 가이드라인 |
| 기기 연동 | 없음 | 의료 영상 장비(MRI·CT·선형가속기) BIM 협의 |

### 1.2 의료 시설 유형별 BIM 특성

**종합병원 (500병상 이상)**
- 수술실 클린룸 BIM (Class ISO 5~7, 층류 기류 BIM)
- 대형 영상 장비(MRI·CT·PET-CT) 실 BIM — 차폐 설계 필수
- 중앙 공급 재료실(CSSD) BIM — 오염/세척/멸균/청결 구역 분리

**중소형 의원·클리닉**
- 치과: 파노라마·CT 방사선 차폐 BIM
- 정형외과: C-Arm 방사선 차폐 BIM
- 피부과: 레이저 안전 구역 BIM

**특수 시설**
- 암 센터: 선형가속기(LINAC) 미로형 차폐 BIM
- 방사선 치료 시설: 콘크리트 벽 1.5~2.5m 두께 BIM
- 핵의학 시설: 방사성 동위원소 사용 구역 차폐 BIM

---

## 2. BIM 필수 파라미터 목록

### 2.1 감염 구획 파라미터

```
Pset_InfectionControlZone (감염 관리 구역 속성)
  - Infection_Zone: Contaminated / Semi-Contaminated / Clean / Semi-Clean
  - Pressure_Differential: 공간 압력 차 (Pa)
      음압격리: -8 Pa 이상 (인접 실 대비)
      양압수술실: +8 Pa 이상
      무균 수술실: +15 Pa 이상
  - Air_Change_Rate: 환기 횟수 (회/시간)
      일반 병실: 2~6회
      격리병실: 12회 이상
      수술실: 15~25회 이상 (청정 공조)
  - Air_Direction: Positive / Negative / Neutral
  - HEPA_Filter_Required: HEPA 필터 의무 여부 (Boolean)
  - HEPA_Filter_Efficiency: HEPA 효율 (% — 0.3μm 기준, 99.97% 이상)
  - Anteroom_Required: 전실(前室) 필요 여부 (Boolean)
  - Surface_Material: 무봉합 바닥재·항균 도료 등
```

### 2.2 의료 가스 파라미터 (ISO 7396)

| 파라미터명 | 데이터 타입 | 단위 | 설명 |
|-----------|------------|------|------|
| MedGas_Type | IfcLabel | - | O₂/N₂O/Vacuum/Air/CO₂/N₂/AGSS |
| MedGas_PipeColor | IfcLabel | - | O₂=백색/N₂O=청색/진공=황색/공기=흑색 |
| Supply_Pressure | IfcPressureMeasure | kPa | 공급 압력 (O₂: 400±40kPa) |
| Pipe_Material | IfcLabel | - | Medical_Grade_Copper / SS316L |
| Zone_Valve_ID | IfcLabel | - | 구역 밸브 ID |
| Outlet_Type | IfcLabel | - | Schrader / DISS / Christmas_Tree |
| Outlet_Count | IfcCountMeasure | - | 아웃렛 수량 |
| ISO_7396_Compliant | IfcBoolean | - | ISO 7396-1 준수 여부 |
| Pipeline_ID | IfcLabel | - | 의료 가스 배관 식별 번호 |
| Zone_Valve_Location | IfcLabel | - | 구역 밸브 위치 (BIM 객체 ID 연계) |

### 2.3 방사선 차폐 파라미터

```
Pset_RadiationShielding (방사선 차폐 속성)
  - Radiation_Source: X-Ray / MRI / CT / PET / LINAC / Nuclear_Medicine
  - Shielding_Material: Lead / Concrete / Baryte_Concrete / Steel / Polyethylene
  - Pb_Equivalent: 납 동등 두께 (mm Pb)
      일반 X-Ray: 1.5~2.0 mm Pb
      CT: 2.5~4.0 mm Pb
      선형가속기(LINAC): 콘크리트 1.5~2.5m
  - Concrete_Density: 콘크리트 밀도 (kg/m³)
      일반 콘크리트: 2,400 kg/m³
      바라이트 콘크리트: 3,200~3,500 kg/m³
  - Wall_Thickness: 벽체 두께 (mm)
  - Primary_Barrier: 1차 방벽 여부 (방사선 직접 조사 방향)
  - Secondary_Barrier: 2차 방벽 여부 (산란 방사선)
  - Workload: 주당 사용 부하 (mA·min/week)
  - Occupancy_Factor: 인접 구역 재실 인수 (T, 0~1)
  - Use_Factor: 방향 사용 인수 (U, 0~1)
  - Radiation_Survey_Required: 차폐 성능 측정 의무 여부
```

### 2.4 MRI실 파라미터

```
Pset_MRIRoom
  - MRI_FieldStrength: 자장 세기 (T, 예: 1.5T / 3.0T / 7.0T)
  - GaussLine_5: 5 Gauss 경계선 반경 (m)
      — 심박 조율기 등 금속 이식물 환자 금지선
  - GaussLine_50: 50 Gauss 경계선 반경 (m)
  - RF_Shielding: RF 차폐 (Faraday Cage) 여부 (Boolean)
  - RF_Shielding_Effectiveness: RF 차폐 효과 (dB, 최소 80~100dB)
  - Magnetic_Fringe_Field: 자기장 분포 BIM 연계 여부
  - Vibration_Isolation: 진동 절연 시스템 형식
  - Quench_Pipe_Route: 퀀치 파이프(He 가스 배기) 경로 BIM 표현
  - Cryogen_Fill_Point: 냉매 충전 위치
  - MRI_Manufacturer: 제조사 (Siemens/GE/Philips 등)
  - MRI_Model: 모델명
  - RF_Penetration_Panel: RF 관통 패널 위치
  - Acoustic_Noise_Level: 소음 수준 (dB — 인접 실 영향)
```

---

## 3. LOD 단계별 요구사항

| LOD | 병원 시설 적용 내용 |
|-----|---------------------|
| LOD 100 | 병상 수·진료 과목·건물 매스 |
| LOD 200 | 감염 구획 경계, 방사선 시설 위치, 의료 가스 계통 개략 |
| LOD 300 | 전체 건축·구조·MEP BIM + 의료 가스 배관 BIM + 방사선 차폐 BIM |
| LOD 350 | MRI 5 Gauss 경계 BIM + 수술실 층류 기류 BIM + 의료 가스 간섭 검토 |
| LOD 400 | 수술실 클린룸 장비 BIM + 의료 가스 아웃렛 상세 + 방사선 차폐 공사 상세 |
| LOD 500 | As-Built + 병원 FM 연동 + CMMS(설비 유지보수 시스템) 속성 완비 |

### 3.1 의료 시설 BIM 특수 검토 단계

- **의료 가스 설계 검토**: ISO 7396 준수 여부 → 설비 전문가 검토 필수
- **방사선 차폐 계산서**: 의학물리사(Medical Physicist) 차폐 계산 → BIM 반영
- **MRI 자기장 시뮬레이션**: 제조사 제공 Gauss 등고선 → BIM에 3D 경계 표현
- **감염관리 BIM 검토**: 감염관리 전문 간호사(ICP) + BIM 팀 공동 검토

---

## 4. IFC Entity 매핑

### 4.1 병원 특화 IFC 엔티티

| 요소 | IFC Entity | 비고 |
|------|------------|------|
| 병실 공간 | IfcSpace (PredefinedType: BEDROOM) | 감염 구획 속성 |
| 수술실 | IfcSpace (PredefinedType: OPERATING_SUITE) | 압력 차·환기 속성 |
| 음압격리병실 | IfcSpace + Pset_InfectionControlZone | -8Pa 파라미터 |
| MRI실 | IfcSpace + Pset_MRIRoom | 5 Gauss 경계 BIM |
| 방사선 차폐벽 | IfcWall + Pset_RadiationShielding | Pb 동등 두께 |
| 의료 가스 배관 | IfcPipeSegment + MedGas Property Set | 색상 코딩 |
| 의료 가스 아웃렛 | IfcValve 또는 IfcBuildingElementProxy | 타입·위치 |
| 의료 가스 구역 밸브 | IfcValve (ZoneType: Medical) | |
| 수술 조명 | IfcLightFixture (PredefinedType: OPERATING) | |
| 전동 침대 공간 | IfcSpace (최소 3.6m×3.6m 이상) | 이동 공간 포함 |
| HEPA 필터 유닛 | IfcFilter + HEPA 속성 | |
| 층류 기류 천장 | IfcSlab (LaminarFlow) 또는 IfcCovering | 수술실 클린 유닛 |
| 방사선 차폐 도어 | IfcDoor + 차폐 파라미터 | Pb 함량 |

### 4.2 병원 공간 분류 체계

```
병원 공간 감염 구획 분류:
  Zone 1 (오염 구역, Contaminated)
    - 격리병실 내부 (음압)
    - 오염 폐기물 처리 구역
    - 부검실
  Zone 2 (준오염 구역, Semi-Contaminated)
    - 일반 병실
    - 처치실
    - 화장실/욕실
  Zone 3 (준청결 구역, Semi-Clean)
    - 복도
    - 대기실
    - 간호 스테이션
  Zone 4 (청결 구역, Clean)
    - 수술실 (양압)
    - 무균 준비실
    - 중앙 공급 재료실(멸균 완료 구역)
```

---

## 5. 국가별 기준 차이

### 5.1 한국 (의료법·의료기관 인증)

- **의료법 시행규칙 [별표 4]**: 의료기관 시설 기준 — 병실 면적(1인실 10m² 이상), 수술실 크기
- **의료기관 인증 기준**: 의료기관평가인증원 — 감염 관리·안전 시설 체크리스트
  - JCI(국제의료기관인증)와 유사 구조
- **의료 가스**: KS C IEC 60601 + 의료기기 기준 규격 — ISO 7396 준용
- **방사선 차폐**: 원자력안전법·의료법 — 의학물리사 차폐 계산 의무
- **내진 설계**: 병원은 용도 분류 1군(중요도 계수 1.5) 적용

### 5.2 일본 (병원 BIM 납품 요건)

- **医療法施行規則**: 의료 시설 기준 — 병실 6.4m²/1병상 이상
- **국토交通省 BIM 가이드라인**: 병원 BIM 권고 (2023 강화)
- **感染対策**: COVID-19 이후 음압 격리 병실 BIM 기준 명확화
- **医療ガス設備**: JIS T 7101 — 의료 가스 설비 기준 (ISO 7396과 유사)
- **免震構造**: 대형 병원 면진 구조 적용 → Revit에서 면진 층 BIM 표현 필요

### 5.3 미국 (FGI 가이드라인)

- **FGI Guidelines for Design and Construction of Hospitals**: 미국 병원 설계 핵심 기준
  - 2022 Edition: 음압 격리 병실 -2.5 Pa 이상, 12 ACH 이상
  - 수술실 양압 +8 Pa, 15 ACH 이상, HEPA 99.97%
  - MRI실 5 Gauss 경계 표시 의무
- **NFPA 99**: 의료 가스 및 진공 시스템 기준 (미국 표준)
- **NFPA 101**: 생명 안전 코드 — 병원 피난 기준
- **Joint Commission**: 미국 병원 인증 — 시설 기준 포함

### 5.4 싱가포르 (MOH 기준)

- **Ministry of Health (MOH) Guidelines**: 병원 설계 기준
- **HDB/BCA 기준 준용**: 일반 건축 기준 위에 의료 특화 기준 추가
- **CORENET X**: 병원 건축 허가 BIM 제출 의무
- **CRISSP**: 싱가포르 병원 감염 관리 기준 — BIM 공간 분류 연계

---

## 6. 자주 발생하는 BIM 실패 사례 Top 5

### 실패 사례 1: 의료 가스 배관과 일반 배관 BIM 색상 혼용
**원인**: 설비 BIM 팀이 의료 가스 배관을 일반 배관과 동일한 색상으로 모델링. ISO 7396 색상 기준 미적용.

**결과**: 시공 현장에서 산소(백색)와 진공(황색) 배관 연결 혼동. 환자 안전 사고 위험. 전체 배관 재라벨링 작업.

**해결책**:
1. BIM 의료 가스 배관 객체에 ISO 7396 색상 코딩 Property Set 의무 입력
2. 색상 코딩 필터 뷰 생성 — 시공 도면에 의료 가스별 색상 자동 반영
3. 의료 가스 배관 BIM 납품 전 ISO 7396 준수 자동 체크리스트

---

### 실패 사례 2: MRI 5 Gauss 경계 BIM 미표현 → 심박 조율기 환자 위험
**원인**: MRI실 BIM 설계 시 자기장 분포 고려 없이 병실 배치. 인접 복도에 심박 조율기 착용 환자 통행.

**결과**: 운영 개시 후 5 Gauss 경계 내 심박 조율기 환자 진입 사고 위험. MRI실 출입 통제 구역 대폭 확대 변경.

**해결책**:
1. MRI 제조사 제공 Gauss 등고선 데이터를 BIM 3D 경계 볼륨으로 표현
2. 5 Gauss 경계 내 공간(IfcSpace) 에 경고 속성 자동 부여
3. 출입 통제 구역 BIM 경계 = 5 Gauss 경계 + 안전 여유 설정

---

### 실패 사례 3: 방사선 차폐 두께 BIM과 차폐 계산서 불일치
**원인**: 의학물리사 차폐 계산서(PDF)와 건축 BIM 벽체 두께가 서로 달랐음. BIM 팀이 계산서 검토 없이 임의로 두께 조정.

**결과**: 건설 완료 후 방사선 방호 측정에서 차폐 불충분 구간 발견. 추가 납 판넬 설치로 공사비 5억 원 추가.

**해결책**:
1. 차폐 계산서 결과값을 BIM 벽체 Pset_RadiationShielding에 직접 입력
2. BIM 벽체 두께와 차폐 계산서 Pb 동등값 자동 비교 스크립트
3. 방사선 구역 BIM 변경 시 의학물리사 재검토 게이트 의무화

---

### 실패 사례 4: 수술실 층류 기류 천장과 조명·의료 가스 간섭
**원인**: 수술실 천장에 층류 기류 유닛(Clean Air Unit), 수술 조명(무영등), 의료 가스 아웃렛, 마취 가스 배기 덕트가 집중. 각 팀 독립 설계로 상호 간섭.

**결과**: 현장 설치 시 층류 유닛 위치를 조명과 의료 가스로 인해 이동 불가. 수술실 전면 천장 재공사.

**해결책**:
1. 수술실 천장 BIM을 단일 통합 모델로 작성 (건축+기계+전기+의료가스 동시)
2. 층류 유닛 위치 확정 후 주변 설비 배치 → 선후 관계 명확화
3. 수술실 전용 BIM 통합 검토 세션 — LOD 300 단계 의무화

---

### 실패 사례 5: 음압격리병실 전실 없이 BIM 설계 → 인증 탈락
**원인**: 음압 격리 병실 BIM 설계 시 전실(Anteroom) 면적 확보 없이 병실 수 극대화. FGI·국내 기준 전실 의무 요건 미인식.

**결과**: 의료기관 인증 심사에서 음압 격리 병실 전실 미비로 감염 관리 기준 부적합. 리모델링으로 병실 수 감소.

**해결책**:
1. 음압 격리 병실 BIM 템플릿에 전실 공간 필수 포함
2. BIM 객체 수준에서 FGI 기준 자동 검증 — 전실 면적·압력 차 자동 체크
3. 병원 BIM 착수 전 감염관리 전문가와 공간 프로그램 사전 협의

---

## 7. LUA BIM LABS 사업 기회 및 Add-in 적용 방향

### 7.1 핵심 사업 기회

| 시장 | 기회 내용 | 규모 |
|------|-----------|------|
| 한국 | 공공 병원 BIM 의무화 (국립·지방의료원), 민간 대형병원 BIM 컨설팅 | 전국 수백 개 |
| 일본 | 의료 시설 BIM 수요 급증, 고령화로 병원 신축·리모델링 지속 | 대형 수요 |
| 싱가포르 | MOH BIM 요건 강화, 신규 종합병원 프로젝트 | |
| 중동 | 사우디·UAE 의료 인프라 확충 (Vision 2030) | 고부가 수주 |

### 7.2 Revit Add-in 적용 방향

**① 의료 가스 배관 검증기 (Medical Gas Verifier)**
- BIM 의료 가스 배관 색상·압력·재질 ISO 7396 자동 준수 검토
- 의료 가스 구역 밸브 위치 자동 검증 (병동 입구 등)
- 아웃렛 수량·타입 일람표 자동 출력

**② 방사선 차폐 BIM 자동화 (Radiation Shield Modeler)**
- 차폐 계산서(CSV) → BIM 벽체 두께 자동 반영
- Pb 동등 두께 → 콘크리트 두께 자동 환산
- 1차/2차 방벽 색상 구분 뷰 자동 생성

**③ MRI 자기장 경계 시각화기 (MRI Gauss Line Visualizer)**
- MRI 제조사 Gauss 데이터 → 3D 경계 볼륨 자동 생성
- 5 Gauss·50 Gauss 경계 BIM 표현 자동화
- 경계 내 공간 출입 통제 속성 자동 부여

**④ 감염 구획 자동 분류기 (Infection Zone Classifier)**
- 공간 유형 기반 감염 구획(오염/준오염/청결) 자동 분류
- 압력 차·환기 횟수·HEPA 요건 자동 적용
- FGI/한국 기준 준수 여부 자동 체크리스트 출력

---

- 관련: [[건물유형별_BIM적용기준]] · [[국가별_건설법규_기준비교]] · [[IFC_OpenBIM]] · [[OpenBIM_프로그램연동]] · [[BIM_납품검수]] · [[해외건설기업_동향분석]]
