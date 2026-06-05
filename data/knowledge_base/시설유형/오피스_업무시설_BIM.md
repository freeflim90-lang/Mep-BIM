# 오피스_업무시설 BIM 적용 기준 지식 베이스

## 2026-06-05 오피스 BIM AI 즉시 답변 패턴 보강
- Source: 업무시설 설계 기준, 에너지절약계획서 기준, BAS·스마트오피스 실무
- Tags: office,commercial,bim,lod,mep,energy,smart-office,2026

**AI 즉시 답변 패턴 — "오피스 건물 BIM에서 MEP 포인트가 뭔가요?"**
```
오피스 업무시설 BIM MEP 핵심 포인트:
1. VAV(가변풍량) 존 설계: 임대 공간 레이아웃 변경 대응
   - VAV 박스 위치·존 경계 BIM에서 파악
2. 이중마루(Access Floor): 배선·소형 배관 경로
   - 이중마루 높이(H=150~500mm) BIM 확인
3. 공조기(AHU) 위치: 층별 또는 기계실 집중
   - AHU 배연동선·유지보수 공간 BIM 확인
4. 에너지 성능: 외피 열관류율·에너지절약계획서
   - BEMS 포인트 위치 BIM 표시
5. 코어 효율: 계단실·EV·화장실 코어 위치
   - MEP 수직 샤프트 위치 확정 후 배관 설계
```

**오피스 BIM LOD 요건:**
| LOD | 핵심 항목 | 특이사항 |
|-----|---------|---------|
| 300 | VAV 존·AHU·수배전반 위치 | 임차 영역 구분 |
| 350 | 이중마루 배선·VAV 상세 | 에너지 분석 연동 |
| 400 | 소규모 분기·고정구 | 시공 도면 수준 |

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #오피스 #업무시설 #BOMA2017 #커튼월 #BAS #이중바닥 #에너지기준 #코어효율
- 업데이트: 2026-06-05

## 오피스_업무시설 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

### 시설 정의
- 건축법상 업무시설: 공공업무시설 + 일반업무시설 (오피스텔 제외)
- 주요 규모: 소형(~5,000m²), 중형(5,000~30,000m²), 대형(30,000m² 이상)
- BIM 의무: 연면적 50,000m² 이상 또는 국가 발주 공공청사는 BIM 필수

### 오피스 BIM의 핵심 과제
| 구분 | 주요 이슈 | BIM 대응 |
|------|---------|---------|
| 임대 면적 산정 | BOMA·한국·일본 기준 혼재 | Area Scheme 다중 운영 |
| 커튼월 시스템 | 비정형·유닛화 커튼월 IFC 매핑 복잡 | Curtain Wall Family + IfcCurtainWall |
| BAS 연동 | 조닝·센서 위치 BIM 반영 | COBie 데이터 + IFC FM 파라미터 |
| 이중바닥(AF) | Access Floor 시스템 CH 파라미터 | IfcCovering + 높이 파라미터 |
| 코어 배치 | 코어 효율(Core Ratio) 임대 면적 최적화 | Dynamo 자동 계산 |

---

## 2. BIM 필수 파라미터 목록 (IFC Property Set 기준)

### Pset_SpaceCommon (공간 공통)
```
NetFloorArea            : 전용면적 (m²) — BOMA 기준 Usable Area
GrossFloorArea          : 계약면적 (m²) — Rentable Area
CommonAreaFactor        : 공용면적 부하율 (Load Factor) — 일반적 1.10~1.20
OccupancyType           : "Office" / "CommonArea" / "Lobby" / "Mechanical"
IsExternal              : 외부 공간 여부
LightingControlZone     : 조명 제어 존 ID
HVACZone                : HVAC 존 ID (BAS 연동)
```

### Pset_BOMA_Office (BOMA 2017 커스텀 Pset)
```
BOMA_UsableArea         : Usable Area (m²) — 임차인 전용
BOMA_RentableArea       : Rentable Area (m²) — 임차인 계약 면적
BOMA_BuildingCommonArea : Building Common Area (m²)
BOMA_FloorCommonArea    : Floor Common Area (m²)
BOMA_LoadFactor         : Load Factor (%) — Rentable/Usable
BOMA_OfficeClass        : "Class A" / "Class B" / "Class C"
LeaseableFloor          : 임대 가능 층 여부 (Boolean)
TenantName              : 임차인 명 (운영 단계)
```

### Pset_AccessFloor (이중바닥)
```
AccessFloorType         : "Stringerless" / "Stringer" / "Structural"
AccessFloorHeight       : AF 높이 (mm) — 일반 150~300mm
PedestalSpacing         : 페데스탈 간격 (mm) — 표준 600×600
FloorLoadCapacity       : 하중 용량 (kN/m²)
ClearHeight             : AF 하부 설비 공간 높이 (mm)
CableManagement         : 케이블 트레이 유무 (Boolean)
```

### Pset_CurtainWallCommon (커튼월)
```
CurtainWallType         : "UnitizedSystem" / "StickSystem" / "StructuralGlazing"
GlazingType             : 유리 타입 (예: "Triple Low-E", "BIPV")
UValue                  : U-value (W/m²K) — 에너지 성능
SHGC                    : Solar Heat Gain Coefficient
MullionDepth            : 멀리언 깊이 (mm)
TransomSpacing          : 트랜섬 간격 (mm)
AcousticPerformance     : 차음 성능 (dB)
FireRating              : 방화 성능 (해당 시)
```

### Pset_BASZone (BAS 빌딩 자동화)
```
BASZoneID               : BAS 존 코드 (예: "F10-HVAC-01")
BASZoneType             : "HVAC" / "Lighting" / "Security" / "Access"
SensorType              : 센서 타입 (CO2/온도/습도/재실)
ControllerID            : BAS 컨트롤러 ID
SetpointTemperature     : 설정 온도 (°C)
OccupancySensor         : 재실 감지 센서 유무 (Boolean)
```

---

## 3. LOD 단계별 요구사항 (LOD 200~500)

### LOD 200 — 기본설계
- 건축: 주동 외형, 코어 위치, 층별 임대 구획 개략
- 구조: 구조 시스템 타입 (철골/RC/SRC), 기둥 그리드 (선)
- MEP: 기계실·전기실 위치, 옥탑 층 설비 면적
- 산출물: 코어 효율 개략 계산서, 층별 임대 가능 면적 (개략)

### LOD 300 — 실시설계 (민간 오피스 납품 기준)
- 건축: 전 층 평면 (임대 구획 경계, 화장실, EV홀, 커튼월 그리드)
  - BOMA 면적표 파라미터 100% 입력
  - 이중바닥 높이 파라미터 층별 입력
- 구조: 철골 부재 단면 크기, 슬래브 두께, 기초 타입
- MEP: HVAC 조닝 평면, 스프링클러 메인 배관, 전기 간선 루트
- 커튼월: 유닛 크기·패턴, 멀리언 위치 (중심선 기준)

### LOD 350 — 조정설계 (간섭 검토 완료)
- MEP 종합 간섭 검토 완료 (Hard Clash 0건)
- 이중바닥-MEP 간격 확인 (배선 공간 확보)
- 커튼월 앵커 위치와 구조 슬래브 Edge 간섭 확인
- BAS 센서·컨트롤러 위치 BIM 반영

### LOD 400 — 제작·시공
- 커튼월: 유닛별 제작 번호, 앵커 상세, 실란트 타입
- 철골: 접합부 상세 (볼트 패턴, 용접 크기), 시공 시퀀스
- 이중바닥: 페데스탈 위치 Shop Drawing
- MEP: 모든 배관 사이즈, 행거 위치, VAV Box 위치

### LOD 500 — 준공(As-Built) + FM
- As-Built 반영 후 COBie 2.4 데이터 출력
- FM 시스템(CAFM) 연동: 공간 ID, 장비 정보, 유지보수 일정
- BAS 연동: BIM Object ↔ BAS Point 매핑 완료

---

## 4. IFC Entity 매핑 (주요 요소별)

| BIM 요소 | IFC Entity | 비고 |
|---------|-----------|------|
| 임대 공간 | `IfcSpace` | BOMA 파라미터 포함 |
| 공용 공간 | `IfcSpace` | OccupancyType = "CommonArea" |
| 외벽 (커튼월) | `IfcCurtainWall` | 유닛화 시스템 전체 |
| 커튼월 패널 | `IfcPlate` | 글레이징 패널 |
| 커튼월 멀리언 | `IfcMember` | PredefinedType = "MULLION" |
| 커튼월 트랜섬 | `IfcMember` | PredefinedType = "TRANSOM" |
| 이중바닥 | `IfcCovering` | PredefinedType = "FLOORING" |
| 이중바닥 페데스탈 | `IfcFastener` | |
| 이중바닥 패널 | `IfcPlate` | |
| 철골 기둥 | `IfcColumn` | PredefinedType = "COLUMN" |
| 철골 보 | `IfcBeam` | PredefinedType = "BEAM" |
| VAV Box | `IfcAirTerminalBox` | BAS Zone ID 파라미터 |
| FCU | `IfcUnitaryEquipment` | PredefinedType = "FANCOILUNIT" |
| BAS 센서 | `IfcSensor` | SensorType 파라미터 |
| 조명 컨트롤 패널 | `IfcElectricDistributionBoard` | |
| 배연창 | `IfcWindow` | SmokeVent = TRUE |

---

## 5. 국가별 기준 차이 (한국/일본/미국/싱가포르)

### 한국
| 항목 | 기준 | 비고 |
|------|------|------|
| 면적 산정 | 건축법 시행령 — 바닥 면적 (벽 중심선 기준) | BOMA와 다름 |
| 에너지 성능 | 에너지절약설계기준: 업무시설 냉방부하 30W/m² 이하 | |
| 화재 안전 | 건축법 제49조: 업무시설 방화구획 1,000m² | |
| 승강기 기준 | 6층 이상 또는 연면적 2,000m² 이상 설치 의무 | |
| 장애인 기준 | 장애인·노인·임산부 편의증진법 — 오피스 적용 |  |

### 일본
| 항목 | 기준 | 비고 |
|------|------|------|
| 면적 산정 | 建築基準法: 壁芯基準 | 한국 유사하나 공용 배분 방식 상이 |
| 에너지 | ZEB(Zero Energy Building) 인증 — 省エネ法 | |
| 내진 | 新耐震基準 (1981년 이후): 震度6強 대응 | BIM 구조 파라미터에 내진 등급 입력 |
| BIM 납품 | 国交省 BIM ガイドライン 2023 | IFC 4.x 권장 |

### 미국
| 항목 | 기준 | 비고 |
|------|------|------|
| 면적 산정 | BOMA 2017 Office Standard | Usable / Rentable / Gross |
| 에너지 | ASHRAE 90.1-2022 | BIM 에너지 분석 연동 |
| 화재 | NFPA 13 / IBC 2021 | 스프링클러 설계 파라미터 |
| 접근성 | ADA (Americans with Disabilities Act) | |
| BIM 납품 | GSA BIM Guide Series | 공공청사 필수 |

### 싱가포르
| 항목 | 기준 | 비고 |
|------|------|------|
| 면적 산정 | SISV (Singapore Institute of Surveyors) 기준 | |
| 에너지 | BCA Green Mark for New Buildings 2021 | Platinum/Gold 등급 |
| BIM 납품 | CORENET X e-Submission | IFC 4.x 필수, 2025년부터 5층 이상 의무 |
| 지속 가능성 | BCA Green Mark BIM Guide | 에너지 파라미터 BIM 내 필수 |

---

## 6. 자주 발생하는 BIM 실패 사례 Top 5

### 사례 1: BOMA 면적과 한국 법정 면적 혼용
- **원인**: 해외 투자자 요청으로 BOMA 면적 산출 + 인허가용 법정 면적 별도 산출 필요한데, BIM 모델에서 Area Scheme을 하나로만 운영 → 두 면적이 혼재
- **해결**:
  - Revit Area Scheme 2개 운영: "법정면적_KR" / "BOMA2017_EN"
  - 각 Scheme별 Area Boundary 별도 설정
  - Schedule 필터로 구분 집계
- **예방**: 프로젝트 킥오프 시 면적 기준 협의서 작성 (발주처 + 임차인 + 설계사)

### 사례 2: 커튼월 IFC 내보내기 누락
- **원인**: Revit 커튼월은 IfcCurtainWall로 올바르게 내보내지지 않고 IfcWall로 분류되거나, Mullion이 별도 요소로 분리되지 않음
- **해결**:
  ```python
  # IFC 내보내기 전 커튼월 분류 검증 스크립트
  import clr
  clr.AddReference("RevitAPI")
  from Autodesk.Revit.DB import *
  
  # 커튼월 Family 확인
  curtain_walls = FilteredElementCollector(doc)\
      .OfClass(Wall)\
      .Cast[Wall]()\
      .Where(lambda w: w.WallType.Kind == WallKind.Curtain)
  
  for cw in curtain_walls:
      # IFC 내보내기 파라미터 확인
      ifc_class = cw.LookupParameter("IFC Class")
      if ifc_class is None or ifc_class.AsString() != "IfcCurtainWall":
          print(f"수정 필요: ID {cw.Id} — IFC Class 미설정")
  ```
- **예방**: IFC Export Setting에서 "Export element as" 매핑 테이블 사전 정의

### 사례 3: 이중바닥 CH(층고) 파라미터 미반영 → MEP 공간 충돌
- **원인**: 이중바닥 높이 150~250mm를 BIM에 반영하지 않아, 슬래브 위 기준으로 설계된 MEP와 실제 AF 패널 사이 공간 충돌
- **해결**: IfcCovering (이중바닥) 높이 파라미터 실제치 입력, MEP 배관·배선 기준점을 AF 상면 기준으로 통일
- **예방**: BEP(BIM 실행 계획서)에 기준면 정의 명시 — "구조 슬래브 상면 / AF 상면 / 천장 마감면"

### 사례 4: BAS 존 경계와 BIM 공간 경계 불일치
- **원인**: 건축 BIM의 IfcSpace 경계와 BAS(건물 자동화) 시스템의 Control Zone이 다름 → FM 운영 단계에서 에너지 분석 데이터 연동 실패
- **해결**: BIM 공간 설정 시 BASZoneID 공유 파라미터 적용, BAS 설계 도면과 BIM Space 경계 일치 확인
- **예방**: MEP BIM과 건축 BIM 공간 ID 체계 사전 통일, COBie Space 시트 출력 후 BAS 팀과 검증

### 사례 5: 코어 효율 계산 오류로 임대 면적 손실
- **원인**: 코어(계단·EV·화장실) 면적 경계를 BIM에서 잘못 설정 → 실제보다 코어 비율이 크게 산출 → 임대 면적 손실 추정
- **해결**:
  ```python
  # Dynamo — 코어 효율(Core Ratio) 자동 계산
  # Core Ratio = Core Area / Gross Floor Area × 100%
  
  spaces = UnwrapElement(IN[0])
  floor_num = IN[1]
  
  office_area = sum([s.Area * 0.0929 for s in spaces 
                     if s.LookupParameter("OccupancyType").AsString() == "Office"
                     and s.Level.Name == f"{floor_num}F"])
  
  core_area = sum([s.Area * 0.0929 for s in spaces 
                   if s.LookupParameter("OccupancyType").AsString() in ["Core", "Stair", "EV"]
                   and s.Level.Name == f"{floor_num}F"])
  
  gross_area = office_area + core_area
  core_ratio = (core_area / gross_area * 100) if gross_area > 0 else 0
  
  OUT = [f"코어 효율: {core_ratio:.1f}%", f"임대 가능 면적: {office_area:.1f}m²"]
  # 일반 오피스 목표: Core Ratio 20~25% 이하
  ```
- **예방**: 기본설계 단계에서 코어 효율 목표치 설정 (Class A: 18~22%), Dynamo 자동 계산으로 매 설계 변경 시 확인

---

## 7. LUA BIM LABS Add-in 적용 방향

### 7.1 BOMA 면적 자동 산출 및 변환 모듈
```csharp
// C# — BOMA 2017 면적 자동 산출 및 한국 법정 면적 비교
public class OfficeAreaCalculator : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        var doc = commandData.Application.ActiveUIDocument.Document;
        var results = new List<FloorAreaResult>();
        
        // 층별 면적 집계
        var levels = new FilteredElementCollector(doc)
            .OfClass(typeof(Level))
            .Cast<Level>()
            .OrderBy(l => l.Elevation);
        
        foreach (var level in levels)
        {
            var spaces = new FilteredElementCollector(doc)
                .OfClass(typeof(SpatialElement))
                .Cast<SpatialElement>()
                .Where(s => s.LevelId == level.Id && s.Area > 0);
            
            var result = new FloorAreaResult
            {
                FloorName = level.Name,
                UsableArea = spaces.Where(s => IsOfficeSpace(s)).Sum(s => s.Area * 0.0929),
                CommonArea = spaces.Where(s => IsCommonArea(s)).Sum(s => s.Area * 0.0929),
                CoreArea = spaces.Where(s => IsCoreArea(s)).Sum(s => s.Area * 0.0929)
            };
            result.RentableArea = result.UsableArea * (1 + result.LoadFactor);
            results.Add(result);
        }
        
        // BOMA Excel 리포트 + 한국 법정면적 비교 시트 출력
        GenerateBomaReport(results);
        return Result.Succeeded;
    }
}
```

### 7.2 에너지 성능 파라미터 자동 체크 (한국/미국/일본 기준 선택)
| 체크 항목 | 한국 기준 | ASHRAE 90.1 | 일본 ZEB |
|---------|---------|-------------|---------|
| 외벽 열관류율 | 0.260 W/m²K 이하 | 0.124 W/m²K | PAL* 적용 |
| 창호 U-value | 1.5 W/m²K 이하 | 1.99 W/m²K | 4.65 W/m²K |
| SHGC | 0.4 이하 | 0.25 이하 | - |
| 조명 밀도 | 10 W/m² 이하 | 9.68 W/m² | 12 W/m² |

### 7.3 BAS 존 자동 할당 (Dynamo)
```python
# Dynamo — BIM Space에서 BAS Zone ID 자동 생성 및 할당
spaces = UnwrapElement(IN[0])

TransactionManager.Instance.EnsureInTransaction(doc)
for space in spaces:
    level_name = space.Level.Name.replace("F", "").zfill(2)
    space_num = space.Number.zfill(3)
    hvac_zone_id = f"F{level_name}-HVAC-{space_num}"
    light_zone_id = f"F{level_name}-LT-{space_num}"
    
    hvac_param = space.LookupParameter("HVACZone")
    if hvac_param: hvac_param.Set(hvac_zone_id)
    
    light_param = space.LookupParameter("LightingControlZone")
    if light_param: light_param.Set(light_zone_id)

TransactionManager.Instance.TransactionTaskDone()
OUT = [s.LookupParameter("HVACZone").AsString() for s in spaces]
```

### 7.4 글로벌 오피스 BIM 납품 자동화 패키지
- **한국**: IFC 4.x + 면적 집계표 자동 출력
- **일본**: 国交省 BIM ガイドライン 체크리스트 자동 검증
- **싱가포르**: CORENET X IFC 검증 + Green Mark 파라미터 체크
- **미국**: GSA BIM Guide COBie 자동 출력

---

## 관련 파일
- 관련: [[건물유형별_BIM적용기준]] · [[국가별_건설법규_기준비교]] · [[IFC_OpenBIM]] · [[BIM_납품검수]]
- 참고: [[BIM_지침서]] · [[BIM_제안서]] · [[Revit_Addin]] · [[Dynamo]] · [[FM_자산관리]]
