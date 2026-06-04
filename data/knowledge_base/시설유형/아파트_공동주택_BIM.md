# 아파트_공동주택 BIM 적용 기준 지식 베이스

## 2026-06-05 한국 공동주택 BIM AI 즉시 답변 패턴 보강
- Source: LH공사 BIM 적용지침(2024), SH공사 서울형 BIM 지침, 건설산업 BIM 기본지침
- Tags: apartment,public-housing,lh,sh,mep,bim-lod,korea,2026

**AI 즉시 답변 패턴 — "아파트 공동주택 BIM에서 MEP LOD 기준이 어떻게 되나요?"**
```
LH공사 공동주택 BIM 설계도면 작성가이드(2024) 기준:
- 기본설계 (LOD 300): 층별 MEP 주 배관·덕트 경로, 기계실 장비 위치
- 실시설계 (LOD 350): 세대 내 분기배관·위생기구 위치, 간섭검토 완료
- 시공 BIM (LOD 400): 배관 지지철물·보온재 포함 전체 상세

세대 MEP 특수 기준:
- 세대 내 급수·급탕: 아파트 전용 PS(파이프 샤프트) 통한 수직 공급
- 난방: 바닥복사 난방(온돌) 배관 LOD 300에서 구역 구분 필수
- 환기: 세대 환기시스템(ERV/HRV) 급기/배기 덕트 위치 명시
```

**공동주택 BIM 특수 고려 사항:**
| 항목 | 내용 | BIM 모델링 포인트 |
|------|------|----------------|
| 방화구획 | 3,000㎡마다 또는 층별 | 방화구획 경계벽·댐퍼·방화문 표시 |
| 세대 분리 | 각 세대 독립 Revit 파일 또는 Workset | 세대 유형별 표준 패밀리 |
| PS(파이프 샤프트) | 세대별 급수·급탕·난방·환기 수직 통로 | PS 위치·치수·각 층 연결 |
| 피난 계단 | 비상구·피난 경로 명확히 | 계단 규격·방화문·경보 연동 |
| 지하주차장 | 대형 공간·소방·환기 복잡 | MEP 간섭검토 최우선 구간 |

**LH vs SH 공동주택 BIM 차이점:**
| 항목 | LH공사 | SH공사(서울시) |
|------|--------|-------------|
| 지침 기준 | LH BIM 설계 가이드(2024) | 서울시 BIM 가이드라인 |
| CDE 플랫폼 | ACC/자체 시스템 | 서울시 디지털트윈 연계 |
| 패밀리 표준 | LH 표준 패밀리 사용 의무 | 서울시 표준 준용 |
| 재건축·재개발 | LH 정비사업 BIM 지침 | 서울 주거환경 정비 BIM |

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #아파트 #공동주택 #한국BIM #LH #SH #세대면적 #방화구획 #MEP
- 업데이트: 2026-06-05

## 아파트_공동주택 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

### 시설 정의
- 한국 주택법상 공동주택: 아파트(5층 이상), 연립주택(4층 이하 660m² 초과), 다세대주택(4층 이하 660m² 이하)
- BIM 의무 적용 대상: LH·SH 발주 500세대 이상 공동주택(BIM 납품 필수), 민간 1,000세대 이상 권고

### BIM 적용의 핵심 과제
| 구분 | 특성 | BIM 대응 전략 |
|------|------|--------------|
| 반복 세대 | 동일 세대 수백~수천 개 반복 | Revit Family 세대 Unit 화 + Array |
| 면적 산출 | 전용/공용/발코니 면적 법적 정의 엄격 | Area Plan 별도 관리, 방화벽 경계 기준 |
| 층별 변형 | 1층 필로티·옥탑층 등 예외층 처리 | Design Option 또는 별도 Type |
| 인허가 연동 | 서울시 BIM 인허가 시스템 제출 | IFC 2x3 / IFC 4 이중 납품 체계 |

### 국내 공동주택 BIM 발주 현황 (2026 기준)
- LH(한국토지주택공사): BIM 성과품 작성 기준 v3.0 적용, LOD 300 이상 요구
- SH(서울주택도시공사): BIM 납품 지침 2024 적용, IFC 4.x 권장
- GH(경기주택도시공사): LH 기준 준용, 공사비 3,000억 이상 필수
- 민간(현대·삼성·GS 등): 자체 BIM 표준 보유, 납품 시 협의 필요

---

## 2. BIM 필수 파라미터 목록 (IFC Property Set 기준)

### Pset_SpaceCommon (공간 공통)
```
NetFloorArea          : 전용면적 (m²) — 주택법 기준, 발코니 제외
GrossFloorArea        : 공급면적 (m²) — 전용 + 주거공용
BalconyArea           : 발코니 면적 (m²) — 법정 서비스면적
NetVolume             : 세대 체적 (m³)
IsExternal            : 외부 공간 여부
OccupancyType         : "Residential" / "Common" / "Parking"
```

### Pset_KR_ApartmentUnit (한국 공동주택 커스텀 Pset)
```
UnitType              : 세대 타입 (예: 59A, 84B, 114C)
HouseHoldNumber       : 세대 번호 (예: 1101)
Floor                 : 층 (Integer)
LineNumber            : 라인 번호 (예: 1호라인)
DongNumber            : 동 번호 (예: 101동)
SupplyArea            : 공급면적 (m²)
ExclusiveArea         : 전용면적 (m²)
ServiceArea           : 서비스면적 m²) — 발코니·다용도실
BedroomCount          : 침실 수
BathroomCount         : 욕실 수
MirrorType            : "Normal" / "Mirror" — 미러세대 여부
BalconyExtended       : 발코니 확장 여부 (Boolean)
FireCompartmentID     : 방화구획 ID
```

### Pset_WallCommon (벽체 공통)
```
FireRating            : 방화 등급 (예: "1시간", "2시간")
IsExternal            : 외벽 여부
LoadBearing           : 내력벽 여부
AcousticRating        : 차음 등급 (dB) — 공동주택 소음기준 적용
ThermalTransmittance  : 열관류율 (W/m²K) — 에너지 절약설계기준
```

### Pset_DoorCommon (문 공통)
```
FireRating            : 방화문 등급 ("갑종", "을종")
HandingType           : 손잡이 방향 ("Left", "Right")
IsExternal            : 세대 현관문 여부
AcousticRating        : 차음 성능
```

---

## 3. LOD 단계별 요구사항 (LOD 200~500)

### LOD 200 — 기본설계 단계
- **건축**: 세대 평면 윤곽, 코어(계단·EV) 위치, 주동 형태(판상/타워)
- **구조**: 기둥·보 위치 및 개략 크기, 전이층 여부
- **MEP**: 기계실·전기실·수조 위치, 주배관 루트 (선 표현)
- **납품 파일**: Revit .rvt + IFC 2x3 (건축, 구조 각 1개)

### LOD 300 — 실시설계 단계 (LH 납품 최소 기준)
- **건축**: 세대 내 모든 벽체, 창호 번호·크기, 세대 현관문, 방화구획 경계선
  - 면적표: 전용/공급/발코니 파라미터 100% 입력
  - 세대 Type 별 Family 완성 (Normal + Mirror 구분)
- **구조**: 슬래브 두께, 기둥 단면, 보 높이, 철근 커버 (설계치)
- **MEP**: 급배수 Main 배관, 전기 간선, HVAC 덕트 메인
  - 스프링클러 헤드 위치 (개략)
  - 각 세대 분기점 표현
- **납품 파일**: Revit .rvt + IFC 4 + 2D PDF 도면 일치 확인

### LOD 350 — 시공상세 단계 (간섭 검토 완료)
- **MEP 간섭 검토**: Navisworks Clash Detective 완료 (Hard Clash 0건 기준)
- **구조-건축 정합**: 슬래브 개구부 위치, 인서트 위치 확정
- **배관 슬리브**: 벽체·슬래브 관통 슬리브 Revit Family 삽입

### LOD 400 — 제작·설치 단계
- **PC 공법** 적용 시: PC 부재별 번호·중량·제작정보 파라미터
- **커튼월**: 멀리언·트랜섬 단면, 앵커 위치, 글레이징 타입
- **MEP**: 배관 사이즈, 피팅 타입, 행거 위치, 전선관 직경

### LOD 500 — 준공(As-Built) 단계
- **시공 변경사항 100% 반영**: RFI·변경도면 → BIM 업데이트
- **FM 파라미터 입력**: 장비 제조사·모델·보증기간·유지보수 일정
- **IFC 최종 납품**: 발주처(LH/SH) 검수 시스템 통과 필수

---

## 4. IFC Entity 매핑 (주요 요소별)

| BIM 요소 | IFC Entity | 비고 |
|---------|-----------|------|
| 세대 공간 | `IfcSpace` | OccupancyType = "Residential" |
| 공용 복도 | `IfcSpace` | OccupancyType = "CommonArea" |
| 외벽 | `IfcWall` | IsExternal = TRUE |
| 세대 간 벽 | `IfcWall` | AcousticRating 필수 |
| 방화벽 | `IfcFireSuppressionTerminal` or `IfcWall` + FireRating |
| 슬래브 | `IfcSlab` | PredefinedType = "FLOOR" / "ROOF" |
| 기둥 | `IfcColumn` | StructuralRole 입력 |
| 보 | `IfcBeam` | 전이보 별도 Type 설정 |
| 계단 | `IfcStair` | 비상계단 FireExit = TRUE |
| 엘리베이터 | `IfcTransportElement` | PredefinedType = "ELEVATOR" |
| 현관문 | `IfcDoor` | IsExternal = TRUE, FireRating = "갑종" |
| 창호 | `IfcWindow` | ThermalTransmittance 입력 |
| 발코니 | `IfcSlab` or `IfcSpace` | BalconyArea 파라미터 |
| 스프링클러 헤드 | `IfcFireSuppressionTerminal` | |
| 소화전 | `IfcFireSuppressionTerminal` | PredefinedType = "SPRINKLER" |
| 급수 배관 | `IfcPipeSegment` | |
| 전기 패널 | `IfcElectricDistributionBoard` | |

---

## 5. 국가별 기준 차이

### 한국 (주요 법령 기준)
- **주택법 시행령**: 세대 면적 산정 기준 — 전용면적 = 내벽 기준 (내측 마감 치수)
- **건축법 제49조**: 방화구획 — 바닥면적 1,000m² 마다 구획 (스프링클러 설치 시 3,000m²)
- **건축물의 에너지절약 설계기준**: 중부1지역 외벽 열관류율 0.150 W/m²K 이하
- **주택건설기준 등에 관한 규정**: 세대 간 경계벽 차음 성능 (STC 45 이상)
- **BIM 납품 기준**: 국토교통부 BIM 적용 가이드라인 v3.0 (2023)

### 일본 참고
- **面積算定**: 壁芯基準 (벽 중심선 기준) — 한국 내법과 다름 주의
- 일본 납품 시 IfcSpace 면적값 재산출 필요

### 싱가포르 참고
- **CORENET e-Submission**: IFC 파일 직접 제출, BCA BIM e-Submission Guide 준수
- Strata Area 기준 — 공용면적 배분 방식 한국과 상이

---

## 6. 자주 발생하는 BIM 실패 사례 Top 5

### 사례 1: Mirror 세대 문 방향 오류
- **원인**: Revit에서 세대 Family를 Mirror 배치 시, 문 Family의 Handing 파라미터가 자동 반전되지 않음. 특히 현관문·화장실 문이 반대로 열리는 문제 발생
- **해결**:
  ```python
  # Dynamo: Mirror 세대 문 방향 자동 보정
  import clr
  clr.AddReference('RevitAPI')
  from Autodesk.Revit.DB import *

  doors = FilteredElementCollector(doc).OfClass(FamilyInstance).ToElements()
  for door in doors:
      param = door.LookupParameter("MirrorType")
      if param and param.AsString() == "Mirror":
          handing = door.LookupParameter("HandingType")
          if handing:
              current = handing.AsString()
              handing.Set("Right" if current == "Left" else "Left")
  ```
- **예방**: 세대 Family 내부에 MirrorType 공유 파라미터 설정, 납품 전 자동 체크 스크립트 실행

### 사례 2: 발코니 면적 이중 계산
- **원인**: IfcSpace 경계를 발코니 외벽 기준으로 설정하면 전용면적에 발코니가 포함됨. LH 검수 시 면적 불일치로 반려
- **해결**: 발코니 공간을 별도 IfcSpace로 분리, OccupancyType = "Balcony" 설정, 면적 집계 Schedule에서 발코니 행 분리
- **예방**: Revit Area Scheme을 "전용면적용"과 "발코니면적용" 두 가지로 운영

### 사례 3: 층고 차이로 인한 MEP 공간 부족
- **원인**: 판상형 아파트 일반층 층고 2,800mm, 1층 필로티 층고 3,200mm 혼재 시, MEP 팀이 일반층 기준으로 덕트 설계 → 필로티 천장 간섭 발생
- **해결**: Revit 레벨별 층고 파라미터를 MEP 모델에 공유 파라미터로 연동, BIM 협업 킥오프 시 층별 층고 표 배포
- **예방**: 층별 단면 뷰 + Section Box로 MEP 공간 확보 여부 시각 확인

### 사례 4: 방화구획 누락으로 인허가 반려
- **원인**: 복도형 아파트 지하주차장 면적이 1,000m²를 초과함에도 BIM 모델에 방화문·방화셔터 미삽입. 2D 도면에는 표기되었으나 BIM에는 없음
- **해결**: 방화구획 체크 Dynamo 스크립트 구축 — 각 구획 면적 자동 산출, 1,000m² 초과 시 알림
  ```python
  # 방화구획 면적 체크
  spaces = FilteredElementCollector(doc).OfClass(SpatialElement)
  for space in spaces:
      area = space.Area  # ft² → m² 변환
      area_m2 = area * 0.0929
      if area_m2 > 1000:
          print(f"경고: {space.Name} — {area_m2:.1f}m² 방화구획 검토 필요")
  ```
- **예방**: BIM 체크리스트에 방화구획 항목 필수 포함, LOD 300 완료 전 자동 검증

### 사례 5: PC(프리캐스트) 부재 번호 불일치
- **원인**: PC 공법 적용 아파트에서 구조 BIM 모델 부재 번호와 공장 제작 도면 번호가 불일치. 현장 설치 시 혼선 → 공기 2주 지연
- **해결**: Revit 구조 부재에 PCElementNumber 공유 파라미터 설정, 공장 제작 번호 체계와 BIM 번호 체계 사전 협의 문서화
- **예방**: LOD 350 단계에서 PC 제작사와 BIM 모델 협업 킥오프, IFC 파일로 번호 체계 공유

---

## 7. LUA BIM LABS Add-in 적용 방향

### 7.1 세대 면적 자동 산출 (Revit Add-in)
```csharp
// C# — 전용/공용/발코니 면적 자동 집계 및 LH 양식 Excel 출력
public class ApartmentAreaExporter : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        Document doc = commandData.Application.ActiveUIDocument.Document;
        
        // Area Scheme에서 전용면적 수집
        var areaSchemes = new FilteredElementCollector(doc)
            .OfClass(typeof(AreaScheme))
            .Cast<AreaScheme>();
        
        var unitAreas = new Dictionary<string, ApartmentAreaData>();
        
        var areas = new FilteredElementCollector(doc)
            .OfClass(typeof(Area))
            .Cast<Area>()
            .Where(a => a.Area > 0);
        
        foreach (var area in areas)
        {
            string unitType = area.LookupParameter("UnitType")?.AsString() ?? "Unknown";
            string mirrorType = area.LookupParameter("MirrorType")?.AsString() ?? "Normal";
            
            if (!unitAreas.ContainsKey(unitType))
                unitAreas[unitType] = new ApartmentAreaData();
            
            // 발코니 구분
            if (area.LookupParameter("OccupancyType")?.AsString() == "Balcony")
                unitAreas[unitType].BalconyArea += area.Area * 0.0929;  // ft² → m²
            else
                unitAreas[unitType].ExclusiveArea += area.Area * 0.0929;
        }
        
        // LH Excel 양식 출력 (ClosedXML 사용)
        ExportToLHFormat(unitAreas, @"C:\LUA_Output\ApartmentAreaReport.xlsx");
        
        return Result.Succeeded;
    }
}
```

### 7.2 Mirror 세대 자동 생성 (Dynamo)
```python
# Dynamo Python — 기준 세대에서 Mirror 세대 자동 파라미터 반전
import clr
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument

# 입력: 기준 세대 Family Instance 리스트
base_units = IN[0]  # Dynamo 입력 노드에서

TransactionManager.Instance.EnsureInTransaction(doc)

mirrored = []
for unit in base_units:
    # Mirror 파라미터 설정
    mirror_param = unit.LookupParameter("MirrorType")
    if mirror_param:
        mirror_param.Set("Mirror")
    
    # 문 방향 자동 반전
    for sub_elem in doc.GetElement(unit.Id).GetSubComponentIds():
        elem = doc.GetElement(sub_elem)
        if elem.Category.Name == "Doors":
            handing = elem.LookupParameter("HandingType")
            if handing:
                handing.Set("Right" if handing.AsString() == "Left" else "Left")
    
    mirrored.append(unit.Id.IntegerValue)

TransactionManager.Instance.TransactionTaskDone()
OUT = mirrored
```

### 7.3 LH 납품 BIM 자동 검수 체크리스트 (Add-in 기능)
| 검수 항목 | 자동 체크 여부 | 판정 기준 |
|---------|-------------|---------|
| 세대 파라미터 완성도 | ✅ 자동 | UnitType·ExclusiveArea·SupplyArea 전 세대 입력 |
| 방화구획 면적 | ✅ 자동 | 구획당 1,000m² 이하 |
| 면적 오차 | ✅ 자동 | BIM ↔ 2D 도면 오차 ±0.5m² 이내 |
| IFC 필수 파라미터 | ✅ 자동 | Pset_SpaceCommon 100% 입력 |
| Mirror 세대 문 방향 | ✅ 자동 | MirrorType = Mirror 세대 Handing 검증 |
| 슬리브 위치 확인 | ⚠️ 반자동 | 구조-MEP 간섭 0건 확인 후 승인 |

### 7.4 글로벌 시장 확장 포인트
- **일본**: 면적 산정 방식(벽심) 전환 모듈 추가 — KR ↔ JP 면적 전환 버튼
- **싱가포르**: CORENET IFC 자동 검증 기능 연동
- **중동(UAE/사우디)**: 이슬람 문화 고려 성별 분리 공간(남성/여성) 파라미터 추가

---

## 관련 파일
- 관련: [[건물유형별_BIM적용기준]] · [[국가별_건설법규_기준비교]] · [[IFC_OpenBIM]] · [[BIM_납품검수]]
- 참고: [[BIM_등급별_투입일_기준표]] · [[BIM_제안서]] · [[Revit_Addin]] · [[Dynamo]]
