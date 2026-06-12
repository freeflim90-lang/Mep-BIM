# 공연장_문화집회시설 BIM 적용 기준 지식 베이스

## 2026-06-05 공연장 BIM AI 즉시 답변 패턴 보강
- Source: 공연시설법, NFPA 기준, 공연장 음향·MEP 설계 실무
- Tags: concert-hall,theater,bim,acoustics,mep,evacuation,2026

**AI 즉시 답변 패턴 — "공연장 BIM에서 MEP 특이사항이 뭔가요?"**
```
공연장·문화집회시설 BIM 핵심 MEP 특이사항:
1. 음향 공조: 무소음 공조 (NC-15~20 이하)
   - 일반 공조 덕트 소음 → 공연 방해 → 저속 대용량 덕트 필요
2. 무대 조명 발열: 대용량 조명 냉각
   - LED 전환으로 감소했지만 여전히 별도 냉각 고려
3. 대공간 소화: 스프링클러 대신 드렌처·포소화 일부 구간
   - NFPA 13 또는 국내 소방법 특수 대공간 기준 적용
4. 피난 시뮬레이션: 다수 관중 동시 피난
   - BIM 기반 피난 경로·시간 시뮬레이션
5. 무대 기계: 플라이 타워·무대 리프트
   - 기계 하중·전기 BIM 표시 필수
```

**공연장 BIM LOD 특수 요건:**
| 항목 | BIM 표현 |
|------|---------|
| 무대 공간 | 플라이 타워 높이, 분리 가능 무대 |
| 음향 처리 | 반사판·흡음재·좌석 재료 파라미터 |
| 객석 시야선 | 전석 무대 시야선 BIM 분석 |
| 피난 경로 | 출구 위치·폭·방향 |

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #공연장 #극장 #콘서트홀 #전시장 #장스팬트러스 #음향설계 #RT60 #비정형천장 #대피시뮬레이션 #NFPA13
- 업데이트: 2026-06-05

## 공연장_문화집회시설 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

### 시설 유형 분류
| 유형 | 규모 기준 | 대표 사례 |
|------|---------|---------|
| 대형 오페라하우스 | 객석 1,500석 이상 | 예술의전당, 국립극장 해오름 |
| 콘서트홀 | 객석 1,000~2,500석 | 롯데콘서트홀, 서울아트센터 |
| 다목적 공연장 | 300~1,500석 | 세종문화회관 대극장 |
| 소극장 | 100~300석 | 블랙박스 극장 |
| 전시장·컨벤션 | 2,000~100,000m² | COEX, KINTEX |
| 문화복합시설 | 공연+전시+교육 복합 | 국립아시아문화전당 |

### BIM 적용의 핵심 과제
| 구분 | 주요 이슈 | BIM 대응 전략 |
|------|---------|-------------|
| 장스팬 구조 | 50~120m 트러스·아치 | 구조 해석 → BIM 연동 (Grasshopper + Karamba3D) |
| 비정형 천장 | 음향 반사판, 오케스트라 셸 | Adaptive Component + NURBS 형상 |
| 음향 파라미터 | RT60, Clarity(C80), Strength(G) | 음향 파라미터 BIM IFC Pset화 |
| 대규모 피난 | 3,000~10,000명 동시 피난 | Pathfinder + BIM IFC 연동 시뮬레이션 |
| 무대 기계 | 플라이 타워, 오케스트라 피트, 무대 리프트 | 별도 Stage Machinery BIM 모델 |
| 대규모 스프링클러 | NFPA 13 집회시설 고밀도 기준 | MEP BIM + 음향 천장 간섭 검토 |

---

## 2. BIM 필수 파라미터 목록 (IFC Property Set 기준)

### Pset_SpaceCommon + 공연장 확장
```
NetFloorArea            : 유효 면적 (m²)
OccupancyType           : "Auditorium" / "Stage" / "Backstage" / "FOH" / "Lobby" / "Exhibition"
OccupancyLoad           : 재실 인원 (명) — 피난 계산 기준
EvacuationRoute         : 피난 경로 ID
AcousticZoneType        : "PerformanceHall" / "RehearsalRoom" / "Foyer" / "ControlRoom"
```

### Pset_AcousticPerformance (음향 성능)
```
RT60_125Hz              : 잔향시간 125Hz (초)
RT60_250Hz              : 잔향시간 250Hz (초)
RT60_500Hz              : 잔향시간 500Hz (초) — 핵심 주파수
RT60_1000Hz             : 잔향시간 1kHz (초)
RT60_2000Hz             : 잔향시간 2kHz (초)
RT60_4000Hz             : 잔향시간 4kHz (초)
Clarity_C80             : 명료도 C80 (dB) — 음악 공연 기준
Strength_G              : 음의 세기 G (dB)
Intimacy_ITDG           : 초기시간간격 ITDG (ms) — 80ms 이하 친밀감
EarlyDecayTime_EDT      : 초기잔향감 EDT (초)
SoundIsolationRating    : 차음 등급 (STC)
BackgroundNoise_NR      : 배경 소음 NR 등급 (NR 15~25 목표)
AcousticFinishMaterial  : 흡음 마감 재료
AbsorptionCoefficient   : 흡음 계수 (주파수별 복합값)
```

### Pset_StageSystem (무대 시스템)
```
StageType               : "Proscenium" / "Thrust" / "BlackBox" / "Arena" / "Flexible"
StageWidth              : 무대 폭 (m)
StageDepth              : 무대 깊이 (m)
FlyTowerHeight          : 플라이 타워 높이 (m) — 무대 높이 × 2.5배 이상
OrchestraPitArea        : 오케스트라 피트 면적 (m²)
OrchestraPitDepth       : 오케스트라 피트 깊이 (m) — 일반 2.5~3.5m
SeatingCapacity         : 총 객석 수 (석)
SightlineAngle          : 시선각 (°) — C값: 60~80mm 기준
LiftSystemType          : 무대 리프트 타입 ("Hydraulic" / "Electric")
RiggingSystemType       : 리깅 시스템 ("CounterWeight" / "Motorized")
```

### Pset_FireSuppression_Assembly (집회시설 소방)
```
SprinklerSystemType     : "Wet" / "Dry" / "PreAction" — NFPA 13 기준
HazardClassification    : "LightHazard" / "OrdinaryHazard1" / "ExtraHazard"
DesignDensity           : 설계 살수 밀도 (mm/min) — 집회 0.10 이상
DesignArea              : 설계 면적 (m²)
SprinklerTemperatureRating: 표시 온도 (°C) — 일반 68°C, 고온부 93°C
HeadSpacing             : 헤드 간격 (m) — NFPA 13: 최대 4.6m×4.6m
```

---

## 3. LOD 단계별 요구사항 (LOD 200~500)

### LOD 200 — 기본설계
- 건축: 주요 공간 배치 (객석·무대·로비·백스테이지), 관람석 경사 개략
- 구조: 장스팬 구조 시스템 결정 (트러스·아치·돔), 스팬·하중 개략
- 음향: 홀 볼륨 + RT60 목표값 설정 (음향 컨설턴트 협의)
- MEP: 기계실 위치, 공조 방식 (변위 환기/공조), 소방 시스템 결정

### LOD 300 — 실시설계
- 건축: 객석 배치 (좌석 수·배열), 무대 평면·단면 확정, 비정형 천장 형상 확정
  - 시선각(Sightline) 분석 완료 — C값 60mm 이상
  - 비상구 위치·피난 경로 확정
- 구조: 트러스 부재 단면, 접합부 상세, 시공 시퀀스 (양중 계획)
- 음향: Odeon/EASE 음향 시뮬레이션 → RT60 충족 여부 검증
- MEP: 스프링클러 헤드 위치 (음향 천장 간섭 검토), HVAC 소음 레벨 계산

### LOD 350 — 조정설계
- 장스팬 구조-MEP 간섭 검토 완료 (트러스 내부 배관 루트)
- 음향 반사판 형상 최종 확정 (Adaptive Component)
- 피난 시뮬레이션 완료 (Pathfinder IFC 연동)
- 무대 기계 BIM 통합 (플라이 타워·리프트·오케스트라 피트)

### LOD 400 — 제작·시공
- 트러스: 부재별 제작 번호, 볼트 패턴, 피스 마킹 도면
- 음향 패널: 패널별 두께·흡음 계수·고정 방법 상세
- 좌석: 좌석 번호·등급·방향 파라미터 전수 입력
- MEP 천장 관통: 스프링클러·조명·스피커 좌표 확정

### LOD 500 — 준공 + 운영
- 음향 측정값(실제 RT60) BIM 파라미터 업데이트 (설계치 vs 준공치 비교)
- 무대 기계 As-Built + 유지보수 정보
- 스피커·조명 As-Built 위치 (사운드 엔지니어 운영 도면 연동)

---

## 4. IFC Entity 매핑 (주요 요소별)

| BIM 요소 | IFC Entity | 비고 |
|---------|-----------|------|
| 객석 공간 | `IfcSpace` | OccupancyType = "Auditorium" |
| 무대 공간 | `IfcSpace` | OccupancyType = "Stage" |
| 장스팬 트러스 | `IfcBeam` | PredefinedType = "LATTICEGIRDER" |
| 아치 구조 | `IfcBeam` | PredefinedType = "ARCH" |
| 비정형 천장 | `IfcCovering` | PredefinedType = "CEILING" + 음향 파라미터 |
| 음향 반사판 | `IfcPlate` | AcousticFinishMaterial 파라미터 |
| 좌석 | `IfcFurnishingElement` | SeatingCapacity, SightlineAngle |
| 오케스트라 피트 | `IfcSlab` | PredefinedType = "LOWEREDSLAB" |
| 무대 리프트 | `IfcTransportElement` | LiftSystemType 파라미터 |
| 방화 셔터 | `IfcDoor` | PredefinedType = "ROLLINGDOOR", FireRating 필수 |
| 스프링클러 헤드 | `IfcFireSuppressionTerminal` | PredefinedType = "SPRINKLER" |
| 연기 감지기 | `IfcSensor` | PredefinedType = "SMOKESENSOR" |
| 비상구 표시등 | `IfcLightFixture` | EmergencyLight = TRUE |
| 무대 스포트라이트 | `IfcLightFixture` | PredefinedType = "SPOTLIGHT" |
| 앰프·스피커 | `IfcAudioVisualAppliance` | |
| 전시 파티션 | `IfcWall` | Movable = TRUE |

---

## 5. 국가별 기준 차이 (한국/미국/일본)

### 한국
| 항목 | 기준 | 세부 내용 |
|------|------|---------|
| 공연법 | 공연법 제11조 | 1,000석 이상 공연장 소방·구조 안전점검 의무 |
| 관람석 기준 | 건축법 시행령 | 객석 열 간격 최소 850mm, 통로 폭 1,200mm |
| 비상구 | 건축법 제49조 | 공연장 비상구 2개 이상, 객석에서 30m 이내 |
| 소방 | 소방시설법 | 300석 이상 자동 스프링클러 의무 |
| 음향 기준 | 건설기술진흥법 | 공연장 소음 환경기준: NR-25 이하 |
| 무대 기계 | 한국산업표준 KS B 6980 | 무대 기계 안전 기준 |

### 미국
| 항목 | 기준 | 세부 내용 |
|------|------|---------|
| 소방 | NFPA 13 (2022) | 집회시설 Light Hazard: 0.10 gpm/ft² |
| 건축 | IBC 2021 Section 303 | Assembly Group A — 객석 면적 0.65m²/인 |
| 접근성 | ADA | 휠체어석 비율: 총 객석의 1% + 4석 (최소) |
| 피난 | NFPA 101 (Life Safety Code) | 피난 경로 설계 기준 |
| 음향 | ANSI/ASA S12.60 | 교육 시설 음향 기준 (공연장 참고) |

### 일본
| 항목 | 기준 | 세부 내용 |
|------|------|---------|
| 건축기준법 | 第35条 | 집회장 피난 계단 기준 |
| 소방법 | 令別表第一(1)項 | 映画館·劇場 스프링클러 500m² 이상 |
| 음향 | 劇場・音楽堂等の活性化に関する法律 | 지역 공연 시설 지원 법안 |
| 내진 | 建築基準法 新耐震基準 | 大ホール 면진 구조 권장 |

---

## 6. 자주 발생하는 BIM 실패 사례 Top 5

### 사례 1: 음향 천장 – 스프링클러 간섭
- **원인**: 콘서트홀 비정형 음향 천장(반사판)이 스프링클러 헤드 배치를 막아, NFPA 13·소방법 기준 헤드 간격 미충족
- **해결**: 스프링클러 헤드를 음향 반사판 개구부 또는 측벽 위치로 재설계. BIM에서 Navisworks 간섭 검토 후 헤드 위치 조정
  ```python
  # Dynamo — 스프링클러 헤드 간격 자동 체크 (NFPA 13 기준 4.6m)
  import math
  
  sprinkler_points = IN[0]  # XYZ 리스트
  max_spacing = 4.6  # m
  
  violations = []
  for i, p1 in enumerate(sprinkler_points):
      nearest_dist = min([math.dist([p1.X, p1.Y], [p2.X, p2.Y]) 
                          for j, p2 in enumerate(sprinkler_points) if i != j])
      if nearest_dist > max_spacing * 1000:  # mm 변환
          violations.append(f"헤드 {i}: 인접 헤드 거리 {nearest_dist/1000:.1f}m > 4.6m 초과")
  
  OUT = violations if violations else ["PASS: 모든 헤드 간격 기준 충족"]
  ```
- **예방**: LOD 300에서 음향 천장 확정 후 즉시 MEP 스프링클러 배치 검토 (MEP 선행 후 음향 조정)

### 사례 2: 장스팬 트러스 처짐으로 무대 가시선 변경
- **원인**: 60m 이상 장스팬 트러스가 자중·활하중에 의해 20~40mm 처짐 발생 → 무대 상부 리깅 시스템 위치 변경 → 3D BIM과 실제 불일치
- **해결**: 구조 해석 소프트웨어(Midas Civil)와 BIM 연동, 처짐값을 BIM 모델에 반영 (1차 형상 + 변형 후 형상 모두 모델링)
- **예방**: 기본설계 단계에서 트러스 처짐 L/360 이하 확보 여부 BIM 파라미터로 관리

### 사례 3: 피난 시뮬레이션 BIM 형상 불일치
- **원인**: Pathfinder 피난 시뮬레이션에 IFC 파일을 임포트할 때, 비정형 천장·계단 곡면이 제대로 변환되지 않아 피난 경로가 실제와 다르게 시뮬레이션됨
- **해결**:
  ```
  Pathfinder IFC 임포트 체크리스트:
  1. IFC 내보내기 전 계단 IfcStair 분류 확인
  2. 바닥면 IfcSlab 연속성 확인 (비정형 면 분할 없이)
  3. 문 IfcDoor 스윙 방향 확인 (피난 방향 기준)
  4. 피난 경로 IfcSpace 경계 연속성 확인
  5. Pathfinder에서 IFC 임포트 후 형상 검증 뷰 확인
  ```
- **예방**: 전용 Pathfinder IFC 내보내기 뷰(Evacuation_View) 별도 생성, 단순화된 형상 사용

### 사례 4: 관람석 시선각(Sightline) BIM 미검토로 인허가 반려
- **원인**: BIM에서 관람석 경사 설계 시 C값(시선각) 계산을 수작업으로만 하고 BIM 파라미터로 관리하지 않음 → 실제 시공 후 일부 좌석에서 무대 가시성 불량
- **해결**:
  ```python
  # Dynamo — 관람석 C값 자동 계산 (C = 시선 여유 높이)
  # C 최소 60mm, 권장 80~100mm
  
  def calculate_c_value(stage_z, eye_z_current, eye_z_prev, dist_current, dist_prev):
      # C = (무대 높이 기준) × 좌석간격 / 앞좌석까지 거리 + 앞좌석 눈높이
      # 표준 C값 공식
      c = ((stage_z - eye_z_prev) * (dist_current - dist_prev) / dist_prev) - (eye_z_current - eye_z_prev)
      return c
  
  seats = IN[0]  # 좌석 XYZ 리스트 (앞열부터 순서)
  stage_height = IN[1]  # 무대 중심 Z (mm)
  
  c_values = []
  for i in range(1, len(seats)):
      c = calculate_c_value(
          stage_height,
          seats[i].Z + 1200,    # 착석 시 눈높이 +1200mm
          seats[i-1].Z + 1200,
          seats[i].Y,
          seats[i-1].Y
      )
      c_values.append({"seat": i, "c_value": c, "pass": c >= 60})
  
  OUT = c_values
  ```
- **예방**: LOD 200 단계에서 Dynamo 시선각 분석 필수 실행, C값 60mm 미달 좌석 즉시 수정

### 사례 5: 공연장 RT60 설계치 미달
- **원인**: BIM 음향 파라미터 (흡음 계수)를 설계 단계에서 올바르게 입력하지 않고, 시공 후 음향 측정에서 RT60이 목표치(클래식 1.8~2.1초)보다 0.3~0.5초 부족
- **해결**: 추가 흡음재 제거 (시트 하부, 벽면 마감 변경) + 음향 가변 장치(Variable Acoustic) 설치
- **예방**: ODEON 음향 시뮬레이션과 BIM 파라미터 연동 — 재료 변경 즉시 RT60 재계산

---

## 7. LUA BIM LABS Add-in 적용 방향

### 7.1 음향 파라미터 자동 집계 모듈
```csharp
// 공연장 RT60 파라미터 검증 Add-in
public class AcousticParameterChecker : IExternalCommand
{
    // RT60 목표값 (시설 유형별)
    private static readonly Dictionary<string, (double Min, double Max)> RT60Targets = new()
    {
        { "ConcertHall",      (1.8, 2.2) },  // 클래식 콘서트홀
        { "OperaHouse",       (1.4, 1.8) },  // 오페라하우스
        { "MultiPurpose",     (1.2, 1.6) },  // 다목적 공연장
        { "Drama",            (0.8, 1.2) },  // 연극 전용
        { "ConferenceHall",   (0.7, 1.0) },  // 회의장
        { "Exhibition",       (0.5, 0.8) }   // 전시장
    };
    
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        var doc = commandData.Application.ActiveUIDocument.Document;
        var spaces = new FilteredElementCollector(doc)
            .OfClass(typeof(SpatialElement))
            .Cast<SpatialElement>();
        
        var report = new List<string>();
        foreach (var space in spaces)
        {
            var hallType = space.LookupParameter("AcousticZoneType")?.AsString();
            if (hallType == null) continue;
            
            var rt60_500 = space.LookupParameter("RT60_500Hz")?.AsDouble() ?? 0;
            if (RT60Targets.ContainsKey(hallType))
            {
                var (min, max) = RT60Targets[hallType];
                bool pass = rt60_500 >= min && rt60_500 <= max;
                report.Add($"{space.Name}: RT60={rt60_500:F2}s [{(pass ? "PASS" : "FAIL")}]");
            }
        }
        
        ShowReport(report);
        return Result.Succeeded;
    }
}
```

### 7.2 Pathfinder 피난 시뮬레이션 연동 자동화
```python
# BIM → Pathfinder IFC 내보내기 최적화 스크립트
# 피난 관련 요소만 선별 내보내기

def export_for_pathfinder(doc):
    # 내보낼 카테고리 목록 (피난 관련)
    export_categories = [
        BuiltInCategory.OST_Floors,       # 바닥
        BuiltInCategory.OST_Stairs,       # 계단
        BuiltInCategory.OST_Doors,        # 문
        BuiltInCategory.OST_Walls,        # 벽
        BuiltInCategory.OST_Rooms,        # 공간
    ]
    
    # IFC 내보내기 설정
    ifc_options = IFCExportOptions()
    ifc_options.FileVersion = IFCVersion.IFC4
    ifc_options.WallAndColumnSplitting = True
    ifc_options.ExportBaseQuantities = False  # 간소화
    
    # 피난 공간 파라미터 우선 검증
    rooms = FilteredElementCollector(doc).OfClass(SpatialElement)
    for room in rooms:
        if not room.LookupParameter("EvacuationRoute"):
            print(f"경고: {room.Name} — EvacuationRoute 파라미터 미입력")
    
    doc.Export(r"C:\LUA_Output", "Pathfinder_Model.ifc", ifc_options)
```

### 7.3 시선각(Sightline) 자동 분석 리포트
- Dynamo 기반 시선각 C값 자동 계산 (전 좌석)
- C값 60mm 미만 좌석 자동 하이라이트 (색상 오버레이)
- PDF 리포트 자동 출력 (한국 공연법 인허가 제출용)

### 7.4 글로벌 공연장 BIM 납품 포인트
- **한국**: 공연법·소방법 자동 체크 → 인허가 보고서 출력
- **미국**: NFPA 13 헤드 간격 자동 검증, ADA 휠체어석 비율 체크
- **일본**: 耐震性能 파라미터 + 消防法 스프링클러 검증

---

## 관련 파일
- 관련: [[건물유형별_BIM적용기준]] · [[국가별_건설법규_기준비교]] · [[IFC_OpenBIM]] · [[BIM_납품검수]]
- 참고: [[소방기계]] · [[건축]] · [[4D5D_BIM]] · [[Revit_Addin]] · [[Dynamo]]

## 2026-06-06 공연장 리모델링·몰입형 전시 BIM 보강
- Source: 인천 문화예술회관 리모델링 2025, 문화체육관광부 공연장 지원사업, 몰입형 전시 국내 확산 동향
- Tags: performance-hall,immersive-exhibition,acoustics,remodeling,bim,2025,2026

**한국 공연장 리모델링 BIM 수요 급증 (2025~2026):**
- 배경: 1980~90년대 건설된 지방 문화예술회관 노후화 → 리모델링 러시
- 사례: 인천 문화예술회관 대공연장 (2025) — 1,504석 → **1,310석** 리모델링 (좌석 배치·시야·음향 개선)
- 리모델링 BIM 핵심 사항:
  - 기존 구조 현황 BIM (포인트클라우드 → Revit) → 리모델링 설계 BIM
  - 좌석 배치 최적화: C-value(시야) 재검토 → 새 좌석 Row/Section BIM 재설계
  - 음향 성능 개선: 반사판·흡음재·측벽 마감 변경 → BIM LOD 400 상세

**몰입형 전시(Immersive Exhibition) 공간 BIM 설계 신규 분야:**
- 국내 확산: 팀랩, 클래식500, 빛의 벙커 계열 → 전국 주요 도시 몰입형 전시 공간 급증
- 기존 공연장·창고·산업 건물 → 몰입형 전시 공간으로 용도 전환 BIM 수요
- **설계 특수 요구사항:**
  | 항목 | 내용 | BIM 파라미터 |
  |------|------|------------|
  | LED 미디어 벽/천장 | 대형 LED 패널 설치 → 고중량 天板 하중 | `LED_Panel_Load_kN_m2`, `Structural_Reinforce` |
  | 고밀도 전력 | LED·프로젝터 전력 밀도 매우 높음 | `Power_Density_kW_m2` (일반의 10배+) |
  | 암실 성능 | 외부광 차단 → 창문 없애거나 차광 | `Blackout_Level: Full/Partial` |
  | 음향 몰입 | 다채널 사운드시스템 → 반사 제어 | `Acoustic_Mode: Immersive` |
  | 관람 동선 | 오픈 플로어 → 군중 밀도 제어 | `Crowd_Zone_Capacity` |

**공연장 음향 시뮬레이션 BIM 연동:**
- 설계 단계: Revit BIM (실내 형상·마감재) → ODEON / CATT-Acoustic 연동
- 주요 지표:
  - RT60(잔향시간): 오케스트라 1.8~2.2초, 오페라 1.4~1.8초, 뮤지컬 1.2~1.5초
  - C80(명료도): +/-5 dB 내 유지 목표
- BIM 파라미터: `Room_RT60_sec`, `Surface_Absorption_Coefficient`, `Diffuser_Placement`

**공연장 ZEB 의무화 적용 (2025~ 1,000m² 이상):**
- 대형 공연장·문화회관: 1,000m² 이상 대부분 해당 → ZEB 5등급(민간) / 4등급(공공) 의무
- 특수 고려사항: 공연 중 관중 발열(1인당 80W) + 대규모 조명 열부하 → 에너지 시뮬레이션 필수
- BIM 에너지 파라미터: `Peak_Occupancy_Load_W_m2`, `Stage_Lighting_kW`, `Curtain_U_value`

**LUA BIM LABS 공연장 BIM 수주 전략:**
- 지방 문예회관 리모델링: 현황 BIM + 좌석·음향 개선 설계 BIM 패키지
- 몰입형 전시 용도 전환: 기존 건물 구조 검토 BIM → 전력·냉방 재설계 MEP BIM
- 문화체육관광부 공연장 대관료 지원사업 연계 → 지방 공연장 발주처 접촉

관련: [[스포츠시설_경기장_BIM]] · [[건물유형별_BIM적용기준]] · [[소방기계]] · [[FM_자산관리]]
