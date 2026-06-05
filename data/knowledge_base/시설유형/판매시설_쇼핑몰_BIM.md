# 판매시설_쇼핑몰 BIM 적용 기준 지식 베이스

## 2026-06-05 쇼핑몰 BIM AI 즉시 답변 패턴 보강
- Source: 판매시설 설계 기준, 소방청 기준, 쇼핑몰 MEP 설계 실무
- Tags: shopping-mall,retail,tenant,mep,sprinkler,fire-shutter,bim,2026

**AI 즉시 답변 패턴 — "쇼핑몰 BIM에서 MEP 특이사항이 뭔가요?"**
```
쇼핑몰·판매시설 BIM 핵심 MEP 특이사항:
1. 테넌트(입주 매장) 분리:
   - 공용 MEP(베이스 빌딩) vs 테넌트 MEP 구분 필수
   - 테넌트별 계량기 설치 → 별도 청구
2. 방화셔터 계획: 매장별 방화구획 → 방화셔터 위치 BIM 표시
3. 스프링클러 Extended Coverage(EH):
   - 대공간(아트리움·푸드코트)은 EH 헤드 적용
4. 에스컬레이터 설비:
   - 에스컬레이터 전력·환기 BIM 표시
   - 에스컬레이터 하부 기계실 공간 확보
5. 환기량: 쇼핑몰 재실 인원 밀도 높음 → 대용량 환기
   - 1인당 10~20 CMH 신선 외기 공급
```

**쇼핑몰 BIM 테넌트 조율 체계:**
| 레벨 | 내용 | BIM 담당 |
|------|------|---------|
| 베이스 빌딩 | 공용 기계·전기·소방 | 건물주 |
| 쉘 앤 코어 | 테넌트 공간 인입 배관 | 건물주 |
| 테넌트 공사 | 각 매장 내부 MEP | 테넌트 |

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #판매시설 #쇼핑몰 #백화점 #대형마트 #복합상업 #방화셔터 #테넌트BIM #에스컬레이터 #스프링클러EH #창고형할인점 #싱가포르몰 #일본몰
- 업데이트: 2026-06-05

## 판매시설_쇼핑몰 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

### 시설 유형 분류
| 유형 | 연면적 기준 | 특성 |
|------|-----------|------|
| 백화점 | 30,000~200,000m² | 고급 마감, 층별 테넌트 고정 |
| 복합쇼핑몰 | 50,000~500,000m² | 앵커 테넌트 + 인라인 테넌트 혼합 |
| 대형마트 (할인점) | 10,000~30,000m² | 창고형 높은 천장, 주차 직결 |
| 아울렛 | 20,000~100,000m² | 저층 분산형, 야외 통로 |
| 스트리트 몰 | 5,000~30,000m² | 지상층 분산, 야외 동선 |
| 창고형 할인점 | 10,000~20,000m² | 천장고 9~12m, 랙 시스템 |

### 판매시설 BIM의 핵심 과제
| 구분 | 주요 이슈 | BIM 대응 전략 |
|------|---------|-------------|
| 방화 셔터 | 판매시설 특화 방화 구획 + 셔터 위치 | 자동 배치 알고리즘 (Dynamo) |
| 테넌트 공간 | 테넌트별 임대 면적·공용면적 분류 | IfcSpace + 테넌트 파라미터 |
| 수직 동선 | 에스컬레이터·무빙워크·엘리베이터 위치 최적화 | 보행 시뮬레이션 연동 |
| 높은 천장 | 창고형 9~12m 천장 → MEP 설계 복잡 | 층 구분 없는 단층 대공간 BIM |
| 스프링클러 | Extra Hazard 기준 판매·창고 구역 | NFPA 13 EH 설계 파라미터 |
| 테넌트 변경 | 테넌트 입점/철수 빈번 → BIM 업데이트 | BIM 공간 DB 연동 (CAFM) |

---

## 2. BIM 필수 파라미터 목록 (IFC Property Set 기준)

### Pset_SpaceCommon + 판매시설 확장
```
NetFloorArea            : 임대 전용 면적 (m²) — 테넌트 경계 내부
GrossFloorArea          : 임대 계약 면적 (m²)
OccupancyType           : "Retail" / "Anchor" / "FoodCourt" / "CommonMall" / "Warehouse" / "ServiceArea"
OccupancyLoad           : 재실 밀도 (명/m²) — 판매: 1인/3m², 대형매장: 1인/5m²
FireCompartmentID       : 방화 구획 ID
```

### Pset_RetailTenant (테넌트 관리)
```
TenantID                : 테넌트 고유 ID (예: "T-B1-001")
TenantName              : 테넌트 명 (예: "나이키", "스타벅스")
TenantCategory          : "Fashion" / "F&B" / "Electronics" / "Anchor" / "Entertainment" / "Beauty"
LeaseArea               : 임대 면적 (m²) — 테넌트 내부 순면적
CommonAreaCharge        : 공용면적 부과 면적 (m²)
LeaseStartDate          : 임대 시작일
LeaseEndDate            : 임대 종료일
RentGrade               : 임대 등급 (A/B/C — 위치·면적·매출 기준)
FitoutCategory          : 인테리어 공사 범주 ("ShellAndCore" / "CatA" / "CatB")
LoadingDockAccess       : 반입구 접근 여부 (Boolean)
MallMallage             : 몰 관리비 코드
```

### Pset_FireShutter (방화 셔터)
```
ShutterID               : 셔터 고유 ID (예: "FS-B1-001")
FireRating              : 방화 등급 ("1시간" / "2시간")
ShutterWidth            : 셔터 폭 (mm)
ShutterHeight           : 셔터 높이 (mm)
OperationType           : "Automatic" / "Manual" / "AutoManual"
ActivationSystem        : "SmokeDetector" / "HeatDetector" / "Manual"
FireCompartmentID       : 연결 방화 구획 ID
ShutterType             : "Rolling" / "Side-Folding" / "Horizontal"
MaintenanceCycle        : 점검 주기 (월)
LastInspectionDate      : 최종 점검일
```

### Pset_SprinklerSystem_Retail (판매시설 스프링클러)
```
HazardClassification    : "LightHazard" / "OrdinaryHazard1" / "OrdinaryHazard2" / "ExtraHazard1" / "ExtraHazard2"
DesignDensity           : 설계 살수 밀도 (mm/min)
DesignArea              : 설계 면적 (m²)
HeadType                : "Pendant" / "Upright" / "SideWall" / "ESFR"  
SprinklerModel          : 제조사 모델
TemperatureRating       : 표시 온도 (°C)
K_Factor                : K-Factor (유출 계수)
MaxHeadSpacing          : 최대 헤드 간격 (m) — OHG2: 3.7m×3.7m
HeightAboveFloor        : 헤드 설치 높이 (m) — 창고: 최상부 랙 위 30cm
ESFRApplicable          : ESFR(Early Suppression Fast Response) 적용 여부
```

### Pset_EscalatorConveyor (에스컬레이터·무빙워크)
```
EscalatorType           : "Escalator" / "MovingWalk" / "AutoWalk"
RiseHeight              : 층간 높이차 (mm)
StepWidth               : 스텝 폭 (mm) — 표준 600/800/1000mm
InclineAngle            : 경사각 (°) — 에스컬레이터: 30°/35°
SpeedMPS                : 운행 속도 (m/s) — 표준 0.5m/s
Capacity                : 수송 용량 (명/시간)
BrandModel              : 제조사·모델 (예: "Otis 506NCE")
MaintenanceContractor   : 유지보수 업체
SafetyGrade             : 안전 등급 (KS C IEC 기준)
```

---

## 3. LOD 단계별 요구사항 (LOD 200~500)

### LOD 200 — 기본설계
- 건축: 동선 계획 (주출입구·부출입구·하역구), 앵커 테넌트 위치, 에스컬레이터 코어 위치
- 구조: 대형 스팬 구조 시스템, 기둥 그리드 (테넌트 모듈 기준: 8m×10m 또는 10m×12m)
- MEP: 대형 기계실 위치, 하역구 근처 스프링클러 시스템 구분
- 방화: 방화 구획 구분 계획 (판매/창고/주차 구역 분리)

### LOD 300 — 실시설계
- 건축: 테넌트별 공간 경계 확정 (IfcSpace 전수 입력)
  - 방화 셔터 위치 확정 (구획 경계 × 통로 교차점)
  - 에스컬레이터·엘리베이터 피트 확정
  - 창고형 높은 천장 구역 별도 레벨 설정
- 구조: 에스컬레이터 피트 개구부, 대형 기둥 단면
- MEP: 스프링클러 구역 구분 (LH/OH1/OH2/EH1/EH2), 덕트 메인 루트

### LOD 350 — 조정설계
- 방화 셔터-MEP 간섭 검토 (셔터 레일 내 배관·배선 금지 구역 확인)
- 에스컬레이터 층간 개구부와 스프링클러 편향판(Deflector) 간섭 검토
- 높은 천장 창고 구역 ESFR 헤드 위치 확정
- 테넌트 임대 면적 최종 확정 (관리사무소·임차인 서명용)

### LOD 400 — 제작·시공
- 에스컬레이터: 제조사 Shop Drawing BIM 반영 (피트·치수·앵커)
- 방화 셔터: 셔터 박스·가이드레일·하강 공간 Shop Drawing
- 창고형 랙 시스템: 랙 위치·높이·하중 BIM 반영

### LOD 500 — 준공 + CAFM 연동
- 테넌트 입점 현황 As-Built (임대 면적 최종 확정)
- CAFM 연동: 테넌트 DB ↔ BIM Space ID 매핑
- 방화 셔터 점검 이력 BIM 파라미터 연동

---

## 4. IFC Entity 매핑 (주요 요소별)

| BIM 요소 | IFC Entity | 비고 |
|---------|-----------|------|
| 테넌트 공간 | `IfcSpace` | TenantID, TenantCategory 파라미터 |
| 공용 몰 통로 | `IfcSpace` | OccupancyType = "CommonMall" |
| 창고 구역 | `IfcSpace` | OccupancyType = "Warehouse", ESFR 적용 |
| 방화 셔터 | `IfcDoor` | PredefinedType = "ROLLINGDOOR", FireRating 필수 |
| 방화문 | `IfcDoor` | FireRating = "갑종" |
| 에스컬레이터 | `IfcTransportElement` | PredefinedType = "ESCALATOR" |
| 무빙워크 | `IfcTransportElement` | PredefinedType = "MOVINGWALKWAY" |
| 엘리베이터 | `IfcTransportElement` | PredefinedType = "ELEVATOR" |
| 화물 엘리베이터 | `IfcTransportElement` | ServiceElevator = TRUE |
| ESFR 스프링클러 | `IfcFireSuppressionTerminal` | ESFRApplicable = TRUE |
| 일반 스프링클러 | `IfcFireSuppressionTerminal` | PredefinedType = "SPRINKLER" |
| 방화 댐퍼 | `IfcDamper` | PredefinedType = "FIREDAMPER" |
| 셔터 레일 | `IfcMember` | 셔터 가이드레일 구조 |
| 대형 보 | `IfcBeam` | 판매시설 대스팬 보 |
| 랙 시스템 | `IfcFurnishingElement` | 창고형 선반 |
| 카트 보관 구역 | `IfcSpace` | OccupancyType = "CartStorage" |

---

## 5. 국가별 기준 차이 (한국/일본/싱가포르/미국)

### 한국
| 항목 | 기준 | 세부 내용 |
|------|------|---------|
| 방화 구획 | 건축법 제49조 | 판매시설: 바닥면적 1,000m² (스프링클러 3,000m²) |
| 방화 셔터 | 건축법 시행령 제46조 | 개구부 방화 셔터 설치 기준 |
| 대규모 점포 | 유통산업발전법 | 3,000m² 이상 대규모 점포 등록 의무 |
| 소방 | 소방시설법 | 판매시설 스프링클러: 연면적 5,000m² 이상 또는 지하층 |
| 에스컬레이터 | 승강기 안전관리법 | 형식 승인 + 완성 검사 의무 |
| 창고형 할인점 | 화재예방법 | 천장고 10m 이상 랙 창고 ESFR 적용 권고 |

### 일본
| 항목 | 기준 | 세부 내용 |
|------|------|---------|
| 백화점 건축기준 | 建築基準法 第24条 | 百貨店·マーケット 방화 기준 별도 |
| 소방 | 消防法 令別表第一(4)項 | 물품販売店 — 스프링클러 3,000m² 이상 |
| 에스컬레이터 | 建築基準法 第34条 | 形式適合認定 필요 |
| 大型商業施設 | 大規模小売店舗立地法 | 1,000m² 이상 届出 의무 |
| BIM 납품 | 国交省 BIM ガイドライン | 대형 상업시설 IFC 납품 권장 |

### 싱가포르
| 항목 | 기준 | 세부 내용 |
|------|------|---------|
| 몰 설계 기준 | URA Master Plan | 복합 개발 비율, GFA 산정 |
| 소방 | SCDF Fire Code 2018 | 쇼핑몰 스프링클러 의무화 |
| BIM 납품 | CORENET X (2025~) | IFC 4.x, 5층 이상 신축 의무 |
| 친환경 | BCA Green Mark | 대형 쇼핑몰 Green Mark Gold 이상 권장 |
| 접근성 | BCA Accessibility Code | 쇼핑몰 전층 배리어프리 의무 |

### 미국
| 항목 | 기준 | 세부 내용 |
|------|------|---------|
| 소방 | NFPA 13 (2022) | Extra Hazard Group 1: 0.30 gpm/ft² |
| 창고형 | NFPA 13 Chapter 12~17 | Rack Storage 별도 챕터, ESFR 규정 |
| 건축 | IBC 2021 Group M (Mercantile) | 판매시설 피난 거리·비상구 기준 |
| 접근성 | ADA | 쇼핑몰 전 매장 접근성 |

---

## 6. 자주 발생하는 BIM 실패 사례 Top 5

### 사례 1: 방화 셔터 위치 자동 배치 오류
- **원인**: 방화 구획 경계와 통로 교차점에 셔터를 수작업으로 배치하다 누락 발생. 10,000m² 이상 대형 쇼핑몰에서 방화 구획 경계가 수십 개이므로 수작업 오류율 높음
- **해결**:
  ```python
  # Dynamo — 방화 구획 경계 × 통로 교차점 자동 셔터 위치 제안
  import clr
  clr.AddReference("RevitAPI")
  from Autodesk.Revit.DB import *
  from RevitServices.Persistence import DocumentManager
  from RevitServices.Transactions import TransactionManager
  
  doc = DocumentManager.Instance.CurrentDBDocument
  
  # 방화 구획 경계 벽 수집 (FireRating 파라미터 보유)
  fire_walls = [w for w in FilteredElementCollector(doc).OfClass(Wall)
                if w.LookupParameter("FireRating") is not None 
                and w.LookupParameter("FireRating").AsString() != ""]
  
  # 복도/통로 공간 수집
  corridors = [s for s in FilteredElementCollector(doc).OfClass(SpatialElement)
               if s.LookupParameter("OccupancyType") is not None
               and s.LookupParameter("OccupancyType").AsString() in ["CommonMall", "Corridor"]]
  
  shutter_positions = []
  
  for wall in fire_walls:
      wall_curve = (wall.Location as LocationCurve).Curve
      for corridor in corridors:
          boundary = corridor.GetBoundarySegments(SpatialElementBoundaryOptions())[0]
          for seg in boundary:
              intersect = wall_curve.Intersect(seg.GetCurve())
              if intersect == SetComparisonResult.Overlap:
                  # 교차점 = 셔터 위치 후보
                  shutter_positions.append({
                      "wall_id": wall.Id.IntegerValue,
                      "position": intersect,
                      "fire_rating": wall.LookupParameter("FireRating").AsString()
                  })
  
  OUT = [f"셔터 위치 후보: {len(shutter_positions)}개", shutter_positions]
  ```
- **예방**: Dynamo 스크립트를 LOD 300 방화 구획 확정 직후 실행, 셔터 위치 전수 검증

### 사례 2: 테넌트 면적 집계 오류로 임대차 분쟁
- **원인**: BIM의 IfcSpace 경계가 실제 임대차 계약서 경계(벽 중심선·내벽·그로스 등)와 불일치 → 계약 면적 vs BIM 면적 차이 발생 → 법적 분쟁
- **해결**: 임대차 계약 면적 기준을 BEP에 명시 (예: "임대 면적 = 내벽 기준"), Revit Area Scheme을 "임대면적" 전용으로 생성
  ```python
  # 임대 면적 검증 스크립트
  # BIM 면적 vs 계약서 면적 비교
  
  tenant_data = IN[0]  # [{"id": "T-001", "contract_area": 150.5}, ...]
  spaces = UnwrapElement(IN[1])  # BIM Space 리스트
  
  discrepancies = []
  for td in tenant_data:
      bim_space = next((s for s in spaces 
                        if s.LookupParameter("TenantID").AsString() == td["id"]), None)
      if bim_space:
          bim_area = bim_space.Area * 0.0929  # ft² → m²
          diff = abs(bim_area - td["contract_area"])
          if diff > 0.5:  # 0.5m² 이상 차이
              discrepancies.append(f"테넌트 {td['id']}: BIM {bim_area:.2f}m² / 계약 {td['contract_area']:.2f}m² (차이 {diff:.2f}m²)")
  
  OUT = discrepancies if discrepancies else ["PASS: 모든 테넌트 면적 일치"]
  ```
- **예방**: 테넌트 임대 계약 전 BIM 면적 기준서 발행, 양측 서명 보관

### 사례 3: 에스컬레이터 개구부 스프링클러 방호 미흡
- **원인**: 에스컬레이터 층간 개구부(Void)에 스프링클러 편향판(Draft Curtain) 설치 누락 → 소방 검사 불합격. 특히 4층 이상 연속 오픈 개구부에서 발생
- **해결**: NFPA 13·소방법 기준 에스컬레이터 개구부 방호 방식 결정 — ① 편향판(4면) + 헤드 배치 또는 ② 드렌처 시스템
  ```
  에스컬레이터 개구부 스프링클러 방호 체크리스트:
  □ 개구부 둘레 편향판 설치 (높이 450mm 이상) — KS 기준
  □ 편향판 내부 스프링클러 헤드 설치 (2.4m 이내)
  □ 인접 헤드와 동일 방호 구역 포함 여부
  □ 드렌처 시스템 적용 시: 작동 밸브·제어반 위치 BIM 반영
  ```
- **예방**: LOD 300에서 에스컬레이터 개구부별 방호 방식 BIM 파라미터 입력

### 사례 4: 창고형 할인점 ESFR 헤드 높이 오류
- **원인**: 천장고 9m 창고에서 ESFR 헤드를 천장면 기준으로만 배치 → 랙 시스템 설치 후 최상위 랙 위 300mm 이내에 헤드가 없어 NFPA 13 Chapter 17 위반
- **해결**: BIM에 랙 시스템 Family 삽입 후, 랙 최상단 높이 + 300mm 위치에 ESFR 헤드 배치 Dynamo 스크립트 작성
  ```python
  # ESFR 헤드 위치 자동 계산 (NFPA 13 Ch.17)
  # 헤드 위치 = 랙 최상단 + 최소 150mm, 최대 460mm
  
  racks = UnwrapElement(IN[0])  # 랙 Family Instance 리스트
  esfr_offset = 300  # mm — 랙 상단에서 300mm 위
  
  esfr_positions = []
  for rack in racks:
      rack_top_z = rack.LookupParameter("RackHeight").AsDouble() * 304.8  # ft → mm
      esfr_z = rack_top_z + esfr_offset
      
      if esfr_z > 9000:  # 천장고 9m 초과 시 경고
          print(f"경고: 랙 {rack.Id} — ESFR 헤드 높이 {esfr_z}mm > 천장고")
      
      esfr_positions.append({
          "rack_id": rack.Id.IntegerValue,
          "esfr_height_mm": esfr_z,
          "x": (rack.Location as LocationPoint).Point.X * 304.8,
          "y": (rack.Location as LocationPoint).Point.Y * 304.8
      })
  
  OUT = esfr_positions
  ```
- **예방**: 창고 구역 BIM 설계 시 랙 시스템 위치·높이 파라미터를 LOD 300에서 확정, ESFR 헤드 위치 동시 결정

### 사례 5: 쇼핑몰 수직 동선 BIM 누락으로 피난 지연
- **원인**: 복합쇼핑몰 BIM에서 에스컬레이터·계단·엘리베이터 동선을 단순 물리적 배치만 하고, IfcTransportElement PredefinedType을 구분하지 않음 → Pathfinder 피난 시뮬레이션에서 수직 동선 미인식 → 피난 시간 과대 산출
- **해결**: IfcTransportElement PredefinedType 정확 설정, Pathfinder IFC 임포트 설정에서 에스컬레이터·계단 연결 수동 확인
- **예방**: 수직 동선 요소 BIM 분류 기준표 작성 후 전수 적용

---

## 7. LUA BIM LABS Add-in 적용 방향

### 7.1 방화 셔터 자동 배치 모듈
```csharp
// Revit Add-in — 방화 구획 경계 × 통로 자동 셔터 배치
public class FireShutterAutoplacer : IExternalCommand
{
    private const double MAX_SHUTTER_WIDTH = 6000;  // mm — 단일 셔터 최대 폭

    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        var doc = commandData.Application.ActiveUIDocument.Document;
        
        // 방화 구획 경계 벽 수집
        var fireWalls = new FilteredElementCollector(doc)
            .OfClass(typeof(Wall))
            .Cast<Wall>()
            .Where(w => w.LookupParameter("FireRating")?.AsString()?.Length > 0);
        
        int shutterCount = 0;
        using (var tx = new Transaction(doc, "방화 셔터 자동 배치"))
        {
            tx.Start();
            foreach (var wall in fireWalls)
            {
                // 통로 교차 지점 찾기 (위 Dynamo 로직과 동일)
                var openings = FindOpeningsInWall(wall, doc);
                foreach (var opening in openings)
                {
                    if (opening.Width <= MAX_SHUTTER_WIDTH)
                    {
                        PlaceFireShutter(doc, wall, opening);
                        shutterCount++;
                    }
                    else
                    {
                        // 분할 셔터 필요 경고
                        TaskDialog.Show("경고", 
                            $"개구부 폭 {opening.Width}mm > 최대 {MAX_SHUTTER_WIDTH}mm — 분할 셔터 검토 필요");
                    }
                }
            }
            tx.Commit();
        }
        
        TaskDialog.Show("완료", $"방화 셔터 {shutterCount}개 자동 배치 완료");
        return Result.Succeeded;
    }
}
```

### 7.2 테넌트 면적 자동 집계 및 임대 리포트 출력
```python
# Dynamo — 테넌트별 임대 면적 자동 집계 + Excel 리포트

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

spaces = UnwrapElement(IN[0])

# 테넌트별 집계
tenant_summary = {}
for space in spaces:
    tid = space.LookupParameter("TenantID")
    tname = space.LookupParameter("TenantName")
    tcat = space.LookupParameter("TenantCategory")
    
    if tid and tid.AsString():
        key = tid.AsString()
        if key not in tenant_summary:
            tenant_summary[key] = {
                "name": tname.AsString() if tname else "Unknown",
                "category": tcat.AsString() if tcat else "Unknown",
                "lease_area": 0,
                "common_area": 0
            }
        tenant_summary[key]["lease_area"] += space.Area * 0.0929
        
        # 공용면적 부가
        common = space.LookupParameter("CommonAreaCharge")
        if common:
            tenant_summary[key]["common_area"] += common.AsDouble()

# 층별 집계
floor_summary = {}
for space in spaces:
    level = doc.GetElement(space.LevelId).Name
    if level not in floor_summary:
        floor_summary[level] = {"total_lease": 0, "total_common": 0, "tenant_count": 0}
    
    tid = space.LookupParameter("TenantID")
    if tid and tid.AsString():
        floor_summary[level]["total_lease"] += space.Area * 0.0929
        floor_summary[level]["tenant_count"] += 1

OUT = [tenant_summary, floor_summary]
```

### 7.3 스프링클러 위험 등급 자동 분류 + 검증
| 구역 유형 | NFPA 위험 등급 | 설계 밀도 | LUA 자동 분류 |
|---------|-------------|---------|-------------|
| 일반 판매 (의류·잡화) | OH Group 1 | 0.15 gpm/ft² | ✅ OccupancyType = "Retail" |
| 식품 판매 | OH Group 2 | 0.20 gpm/ft² | ✅ TenantCategory = "F&B" |
| 가구·목재 | EH Group 1 | 0.30 gpm/ft² | ✅ 자동 분류 |
| 창고형 랙 (9m+) | EH Group 2 / ESFR | 별도 계산 | ✅ HeightAboveFloor > 9m |
| 주차 구역 | OH Group 2 | 0.20 gpm/ft² | ✅ OccupancyType = "Parking" |

### 7.4 글로벌 쇼핑몰 BIM 납품 포인트
- **한국**: 방화 구획 자동 검증 + 셔터 배치 리포트 (소방·건축 허가용)
- **일본**: 消防法 스프링클러 기준 자동 체크 + 大規模小売店舗 届出 면적 집계
- **싱가포르**: CORENET X IFC 검증 + BCA Green Mark 에너지 파라미터 체크
- **미국**: NFPA 13 위험 등급 자동 분류 + ESFR 헤드 위치 검증

---

## 관련 파일
- 관련: [[건물유형별_BIM적용기준]] · [[국가별_건설법규_기준비교]] · [[IFC_OpenBIM]] · [[BIM_납품검수]]
- 참고: [[소방기계]] · [[건축]] · [[오피스_업무시설_BIM]] · [[Revit_Addin]] · [[Dynamo]] · [[FM_자산관리]]

## 2026-06-06 쇼핑몰 이커머스 대응·복합용도 전환·ZEB BIM 보강
- Source: 한국 유통업계 이커머스 충격 동향, ZEB 의무화 판매시설, 오프라인 쇼핑몰 리모델링 트렌드
- Tags: retail,shopping-mall,mixed-use,ecommerce,popup,bim,zeb,remodeling,2025,2026

**이커머스 충격 → 오프라인 쇼핑몰 공실 BIM 대응 (2025~2026):**
- 국내 이커머스 비중: 전체 소매 판매의 30%+ 돌파 → 오프라인 판매시설 공실 증가
- 대형 쇼핑몰 공실 대응 전략별 BIM 요구사항:
  | 전환 방향 | BIM 변경 핵심 | 예시 |
  |---------|------------|------|
  | 판매 → 체험형 F&B | 주방 배기·위생 MEP 재설계, 방화구획 변경 | 대형 푸드홀 전환 |
  | 판매 → 오피스 | HVAC 개별 조닝, 화장실 확장, 사무 환경 조도 | 리테일→업무 용도 변경 |
  | 판매 → 주거 | 세대별 수직 MEP 분리, 세대 파라미터 추가 | 상업→주거 복합 전환 |
  | 판매 → 팝업 유연 공간 | 가변형 파티션, 전기 멀티탭 그리드, 임시 배관 | 팝업스토어 존 |

**팝업스토어 확산 → 유연 공간 BIM 설계 (2025~2026 트렌드):**
- 브랜드 팝업스토어: 단기 임대(2주~3개월) → 빠른 설치·철거 반복
- BIM 유연 공간 파라미터:
  ```
  Pset_FlexibleRetailSpace:
    - Partition_Type: Movable / Fixed / None
    - Power_Grid_Spacing_m: 바닥 전원 그리드 간격 (1.2m 추천)
    - Water_Stub_Locations: 임시 급수 접속 포인트 위치
    - Lighting_Circuit_Type: Dimmable / Fixed (팝업별 독립 회로)
    - Max_Floor_Load_kN_m2: 전시 장비·설치물 허용 하중
    - Popup_Lease_Min_Days: 최단 임대 기간
  ```

**판매시설 ZEB 의무화 BIM 설계 임팩트 (2025.12~):**
- 민간 판매시설 1,000m² 이상 → ZEB 5등급 수준 설계 의무화
- 쇼핑몰 에너지 특성: 조명·에스컬레이터·냉방 전력 집중 → ZEB 달성 최고 난이도 시설 중 하나
- BIM 에너지 전략:
  - LED 조명 + DALI 조도 제어: 테넌트별 조명 제어 BIM 그룹 속성화
  - 옥상 태양광: 중정·천창 구조 고려 PV 배치 최적화 BIM
  - 냉방 열회수: 에스컬레이터·조명 발열 → 히트펌프 열원 활용
  - 파라미터: `Tenant_Power_Allowance_kW`, `Common_Area_EUI_kWh_m2`

**온라인-오프라인 통합(O2O) 쇼핑몰 BIM 활용:**
- O2O 전략: 물류 거점 + 체험 매장 통합 → 쇼핑몰 지하/후면 소규모 풀필먼트 센터 도입
- BIM 설계 반영:
  - 풀필먼트 구역 바닥 하중 강화: `Floor_Load_kN_m2 ≥ 7.5` (로봇 물류)
  - 화물 반입 동선: 쇼핑몰 후면 도크 → 지하 물류 동선 BIM 별도 레이어
  - 테넌트 BIM 데이터 연동: 임차인 매장 레이아웃 BIM → 발주처 Mall BIM 통합

**LUA BIM LABS 판매시설 BIM 수주 전략:**
- 공실 쇼핑몰 복합용도 전환 BIM: 현황 BIM + 용도 변경 MEP 재설계 원스톱 패키지
- 팝업 유연 공간 BIM: 가변 파티션·전기 그리드 BIM 템플릿 → 브랜드사 직접 제안
- ZEB 의무화 대응: 쇼핑몰 에너지 시뮬레이션 + 조명·냉방 BIM 최적화 컨설팅

관련: [[물류센터_창고시설_BIM]] · [[오피스_업무시설_BIM]] · [[일반건물_빌딩_BIM]] · [[FM_자산관리]]
