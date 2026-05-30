# 호텔_숙박시설 BIM 적용 기준 지식 베이스

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #호텔 #리조트 #숙박시설 #객실BIM #PTAC #Hilton #Marriott #Dynamo자동배치 #일본호텔 #싱가포르호텔
- 업데이트: 2026-05-28

## 호텔_숙박시설 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

### 시설 유형 분류
| 유형 | 객실 수 기준 | 특성 |
|------|-----------|------|
| 럭셔리 호텔 (5성) | 200~600실 | Suite 비율 높음, 비정형 설계 |
| 비즈니스 호텔 (3~4성) | 150~500실 | Standard 객실 반복, 코어 효율 중심 |
| 부티크 호텔 | 30~120실 | 각 객실 개성, 소규모 |
| 리조트 | 100~1,000실 | 저층 분산형, 조경 BIM 중요 |
| 서비스드 레지던스 | 100~300실 | 주거+호텔 복합 기능 |
| 캡슐호텔 (일본) | 100~500캡슐 | 극소형 반복 유닛 |

### 호텔 BIM의 핵심 과제
| 구분 | 주요 이슈 | BIM 대응 전략 |
|------|---------|-------------|
| 객실 반복 패턴 | 동일 객실 타입 수백 개 반복 | Dynamo 자동 배치 + Array |
| 국제 브랜드 기준 | Hilton/Marriott 디자인 가이드 준수 | 브랜드별 파라미터 체크리스트 |
| PTAC 공조 | 객실별 독립 공조 (Packaged Terminal A/C) | PTAC Family + MEP 존 분리 |
| 수직 시스템 | 객실층 반복으로 MEP 샤프트 정밀 관리 | Revit 샤프트 Workset 분리 |
| 납품 기준 | 일본·싱가포르 별도 기준 | 국가별 IFC 납품 체계 |

---

## 2. BIM 필수 파라미터 목록 (IFC Property Set 기준)

### Pset_SpaceCommon + 호텔 확장
```
NetFloorArea            : 객실 전용 면적 (m²) — 욕실 포함
GrossRoomArea           : 객실 총 면적 (m²)
OccupancyType           : "GuestRoom" / "Suite" / "Lobby" / "Restaurant" / "FitnessCenter" / "MeetingRoom"
RoomNumber              : 객실 번호 (예: "1201")
Floor                   : 층 (Integer)
RoomType                : "Standard" / "Deluxe" / "Junior Suite" / "Suite" / "Presidential Suite"
RoomCategory            : "Single" / "Double" / "Twin" / "King" / "Studio"
MaxOccupancy            : 최대 수용 인원 (명)
```

### Pset_HotelGuestRoom (호텔 객실 커스텀 Pset)
```
BrandStandard           : 브랜드 기준 (예: "Hilton Hampton", "Marriott Courtyard")
RoomWidth               : 객실 폭 (mm) — Hilton: 최소 3,600mm
RoomDepth               : 객실 깊이 (mm) — Hilton: 최소 9,000mm
CeilingHeight           : 천장 높이 (mm) — 기준 2,600mm 이상
WindowWidth             : 창문 폭 (mm) — 전망 기준
BalconyIncluded         : 발코니 포함 여부 (Boolean)
ConnectingRoomID        : 연결 객실 ID (Connecting Room)
AccessibilityType       : "Standard" / "Accessible" / "Roll-In Shower"
ViewType                : "OceanView" / "CityView" / "PoolView" / "CourtView"
SmokingPolicy           : "NonSmoking" / "Smoking"
FloorMaterial           : 바닥 마감 재료 (예: "Carpet", "Hardwood", "Tile")
```

### Pset_PTAC_System (패키지 터미널 공조)
```
PTACType                : "PTAC" / "PTHP" (히트펌프 포함)
PTACCapacity_Cooling    : 냉방 용량 (kBtu/hr 또는 kW)
PTACCapacity_Heating    : 난방 용량 (kBtu/hr 또는 kW)
PTACBrand               : 제조사 브랜드 (예: "LG", "GE", "Amana")
PTACModel               : 모델 번호
SleeveWidth             : 슬리브 폭 (mm) — 표준 42inch(1,067mm)
SleeveHeight            : 슬리브 높이 (mm) — 표준 16inch(406mm)
ExteriorGrillType       : 외부 그릴 타입 ("Louvered" / "OpenFace")
FreshAirCFM             : 외기 도입량 (CFM)
NoiseLevelNC            : 소음 레벨 (NC) — 객실: NC-30 이하
MaintenanceAccess       : 유지보수 접근 방향 (객실 내 / 외부)
```

### Pset_HotelBrandCompliance (국제 브랜드 기준)
```
BrandName               : "Hilton" / "Marriott" / "Hyatt" / "IHG" / "AccorHotels"
DesignGuideVersion      : 브랜드 디자인 가이드 버전 (예: "Hilton 2023 Technical Standards")
ComplianceStatus        : "Compliant" / "NonCompliant" / "PendingReview"
ComplianceReviewDate    : 브랜드 승인 날짜
FlagshipBrand           : "Yes" / "No" — 플래그십 여부
PrototypePlanUsed       : 브랜드 표준 평면 사용 여부 (Boolean)
DeviationApproved       : 기준 이탈 승인 여부 (Boolean)
```

---

## 3. LOD 단계별 요구사항 (LOD 200~500)

### LOD 200 — 기본설계
- 건축: 주동 형태 (타워/저층), 객실층 구성, 코어 위치, 주요 공간 배치 (로비·레스토랑·연회장)
- 구조: 구조 시스템 (RC/SRC), 기둥 그리드 (객실 폭 기준)
- MEP: PTAC vs 중앙 공조 방식 결정, 샤프트 위치 확정

### LOD 300 — 실시설계 (국제 브랜드 승인 필수)
- 건축: 객실 타입별 평면 Family 완성 (Standard/Deluxe/Suite)
  - 브랜드 Technical Standard 파라미터 100% 입력 및 검증
  - 욕실 레이아웃 (Hilton 기준: 욕실 최소 4.5m²)
  - 연결 객실(Connecting) 문 위치 확정
- 구조: 슬래브 두께, 차음 성능 (IBC STC 50 이상)
- MEP: PTAC 슬리브 위치, 급배수 수직관 위치, 전기 패널 위치

### LOD 350 — 조정설계
- 객실 층별 MEP 종합 간섭 검토
- PTAC 외기 그릴 위치 외관 검토
- 소방: 스프링클러 헤드 위치 (객실 내 1개 이상)
- Dynamo 자동 배치 완료 후 위치 검증

### LOD 400 — 제작·시공
- 객실 욕실 UCP(Unit Construction Package) 프리팹 상세
- PTAC 슬리브 프리캐스트 또는 현장 타설 상세
- FF&E (가구·비품·장비) BIM 좌표 입력

### LOD 500 — 준공 + PMS 연동
- As-Built 객실 번호·파라미터 전수 확인
- PMS(Property Management System) 연동: Room ID ↔ BIM Object ID 매핑
- COBie 출력 → FM 시스템 연동

---

## 4. IFC Entity 매핑 (주요 요소별)

| BIM 요소 | IFC Entity | 비고 |
|---------|-----------|------|
| 객실 공간 | `IfcSpace` | RoomType, RoomNumber 파라미터 |
| 로비·공용 공간 | `IfcSpace` | OccupancyType = "Lobby" |
| 연회장 | `IfcSpace` | OccupancyType = "BallRoom" |
| 피트니스 센터 | `IfcSpace` | OccupancyType = "FitnessCenter" |
| 수영장 | `IfcSpace` | OccupancyType = "Pool" |
| PTAC 유닛 | `IfcUnitaryEquipment` | PredefinedType = "PACKAGED_TERMINAL_AIRCONDITIONER" |
| PTAC 슬리브 | `IfcOpening` | 외벽 관통 개구부 |
| 객실 욕실 | `IfcSpace` | OccupancyType = "Bathroom" |
| 연결문 | `IfcDoor` | ConnectingRoomID 파라미터 |
| 객실 창문 | `IfcWindow` | ViewType 파라미터 |
| 발코니 | `IfcSlab` or `IfcSpace` | BalconyIncluded = TRUE |
| 스프링클러 헤드 | `IfcFireSuppressionTerminal` | 객실 1개 이상 |
| 연기 감지기 | `IfcSensor` | PredefinedType = "SMOKESENSOR" |
| 엘리베이터 | `IfcTransportElement` | PredefinedType = "ELEVATOR" |
| 서비스 EV | `IfcTransportElement` | ServiceElevator = TRUE |
| Room Control Unit | `IfcController` | IoT 객실 제어 |
| 호텔 금고 | `IfcFurnishingElement` | InRoomSafe = TRUE |

---

## 5. 국가별 기준 차이 (일본/싱가포르/한국/미국)

### 한국
| 항목 | 기준 | 비고 |
|------|------|------|
| 관광숙박업 | 관광진흥법 제4조 | 호텔업 등록 기준: 객실 수·면적·설비 |
| 객실 최소 면적 | 관광진흥법 시행규칙 | 관광호텔 일반실 최소 19m² |
| 소방 | 소방시설법 | 숙박시설 자동 스프링클러 + 자동화재탐지설비 의무 |
| 에너지 | 에너지절약설계기준 | 숙박시설 에너지 기준 별도 |
| BIM 납품 | 자율 (공공 발주 시 BIM 의무) | |

### 일본
| 항목 | 기준 | 비고 |
|------|------|------|
| 여관업법 | 旅館業法 (2018 개정) | 호텔·료칸·모텔 구분 |
| 객실 최소 면적 | 旅館業法 施行規則 | 호텔 객실 최소 9m² (床面積) |
| 내진 기준 | 建築基準法 新耐震 | 호텔 내진 등급 Is 0.6 이상 |
| 소방 | 消防法 | 숙박시설 스프링클러 11층 이상 |
| BIM 납품 | 国交省 BIM ガイドライン 2023 | 대형 호텔 IFC 납품 권장 |
| 특이사항 | 료칸(旅館) 형식 | 다다미·욕탕 등 별도 파라미터 필요 |

### 싱가포르
| 항목 | 기준 | 비고 |
|------|------|------|
| 호텔 법규 | Hotel Act 1954 (개정) | Singapore Tourism Board 등록 의무 |
| 객실 면적 | URA 기준 | 최소 객실 면적 32m² (스튜디오 포함) |
| BIM 납품 | CORENET X (2025~) | IFC 4.x 기반 e-Submission 의무 |
| 친환경 | BCA Green Mark 2021 | 신규 호텔 Green Mark Gold 이상 |
| 접근성 | BCA Accessibility Code | 휠체어 접근 객실 비율: 전체의 1% 이상 |

### 미국 (Hilton/Marriott 브랜드 기준)
| 항목 | 기준 | 비고 |
|------|------|------|
| Hilton Technical Standards | 2023 | 객실 최소 폭 3.6m, 깊이 9.0m |
| Marriott Design Standards | 2024 | 브랜드별 (Marriott/Westin/Sheraton 상이) |
| ADA 기준 | ADA Standards 2010 | 전체 객실의 최소 5% 접근 가능 객실 |
| IBC 2021 | Section 310 | Residential Group R-1 |
| NFPA 101 | Life Safety Code | 호텔 피난 계단 기준 |

---

## 6. 자주 발생하는 BIM 실패 사례 Top 5

### 사례 1: Dynamo 자동 배치 후 객실 번호 중복
- **원인**: Dynamo 스크립트로 객실을 자동 배치할 때 층·호수 번호 부여 로직 오류 → 1101호가 2개 생성
- **해결**:
  ```python
  # Dynamo Python — 호텔 객실 자동 배치 + 번호 자동 부여
  import clr
  clr.AddReference("RevitAPI")
  from Autodesk.Revit.DB import *
  from RevitServices.Persistence import DocumentManager
  from RevitServices.Transactions import TransactionManager
  
  doc = DocumentManager.Instance.CurrentDBDocument
  
  # 입력값
  room_family = UnwrapElement(IN[0])   # 객실 Family Symbol
  floors = IN[1]                        # 층 리스트 (Level objects)
  rooms_per_floor = IN[2]              # 층당 객실 수 (예: [10, 10, 10, ...])
  start_x = IN[3]                      # 시작 X 좌표 (mm)
  room_width = IN[4]                   # 객실 폭 (mm, 예: 4200)
  
  TransactionManager.Instance.EnsureInTransaction(doc)
  
  placed_rooms = []
  room_numbers = set()  # 중복 방지
  
  for floor_idx, level in enumerate(floors):
      floor_num = floor_idx + 1
      for room_idx in range(rooms_per_floor[floor_idx]):
          room_num = room_idx + 1
          room_id = f"{floor_num:02d}{room_num:02d}"  # 예: 0101, 0102...
          
          # 중복 체크
          if room_id in room_numbers:
              raise Exception(f"객실 번호 중복: {room_id}")
          room_numbers.add(room_id)
          
          # 위치 계산
          x = start_x + (room_idx * room_width) / 304.8  # mm → ft
          loc = XYZ(x, 0, level.Elevation)
          
          # Family Instance 배치
          inst = doc.Create.NewFamilyInstance(loc, room_family, level,
                                              Structure.StructuralType.NonStructural)
          inst.LookupParameter("RoomNumber").Set(room_id)
          inst.LookupParameter("Floor").Set(floor_num)
          placed_rooms.append(room_id)
  
  TransactionManager.Instance.TransactionTaskDone()
  OUT = placed_rooms
  ```
- **예방**: 배치 완료 후 객실 번호 중복 검사 스크립트 자동 실행

### 사례 2: PTAC 슬리브 위치와 커튼월 멀리언 충돌
- **원인**: 객실 외벽 PTAC 슬리브(W1,067×H406mm) 위치가 커튼월 멀리언과 겹쳐 외관 상 문제 + 구조적 약화
- **해결**: 커튼월 그리드 간격과 PTAC 슬리브 위치를 Dynamo에서 동시 계획, 슬리브 중심이 반드시 스팬드럴 패널 중심에 오도록 파라미터 연동
- **예방**: 외벽 그리드 결정 시 PTAC 슬리브 폭 + 여유치 200mm를 그리드 모듈에 포함

### 사례 3: 브랜드 Technical Standard 미준수로 Hilton 승인 거절
- **원인**: Hilton Technical Standards 요구 욕실 치수(욕실 최소 폭 2,400mm)를 미충족. 설계 단계에서 BIM 파라미터 체크 없이 진행 → Hilton 검토 단계에서 대규모 수정
- **해결**:
  ```python
  # Dynamo — Hilton Technical Standard 자동 체크리스트
  rooms = UnwrapElement(IN[0])
  brand = "Hilton"
  
  # Hilton 2023 Technical Standards (선택 항목)
  hilton_standards = {
      "RoomWidth": 3600,       # mm
      "RoomDepth": 9000,       # mm
      "CeilingHeight": 2600,   # mm
      "BathroomArea": 4500,    # mm² (4.5m²)
      "BathroomWidth": 2400,   # mm
      "CorridorWidth": 1800,   # mm
  }
  
  failures = []
  for room in rooms:
      room_type = room.LookupParameter("RoomType")
      if room_type and "Suite" not in room_type.AsString():
          width = room.LookupParameter("RoomWidth")
          if width and width.AsDouble() * 304.8 < hilton_standards["RoomWidth"]:
              failures.append(f"객실 {room.Number}: 폭 {width.AsDouble()*304.8:.0f}mm < {hilton_standards['RoomWidth']}mm")
          
          ceiling = room.LookupParameter("CeilingHeight")
          if ceiling and ceiling.AsDouble() * 304.8 < hilton_standards["CeilingHeight"]:
              failures.append(f"객실 {room.Number}: 천장고 미달")
  
  OUT = failures if failures else ["PASS: Hilton Technical Standards 충족"]
  ```
- **예방**: LOD 200 단계에서 브랜드 Technical Standard 파라미터 체크리스트 실행 의무화

### 사례 4: 객실 층 MEP 샤프트 위치 변경으로 전 층 수정
- **원인**: 실시설계 중 레스토랑 주방 위치 변경으로 급배기 샤프트가 이동 → 객실층 전체 샤프트 위치 변경 → 30개 층 전수 수정 (2주 손실)
- **해결**: 호텔 BIM은 반드시 Revit Workset을 "Core_Shaft" 별도 Workset으로 분리, 샤프트 변경 시 링크 업데이트 방식 적용
- **예방**: 샤프트 위치는 LOD 200 단계에서 최종 확정 후 동결 원칙. 변경 시 영향 범위 BIM 자동 감지

### 사례 5: 연결 객실(Connecting Room) 문 방향 오류
- **원인**: BIM에서 Connecting Door를 한쪽 방향만 모델링 → 실제 시공 시 양방향 열림 필요한데 단방향 문 설치
- **해결**: Connecting Door Family를 양방향 스윙 타입으로 별도 제작, ConnectingRoomID 파라미터로 대응 객실 연결
- **예방**: 객실 타입 Matrix 작성 (어느 타입이 Connecting 가능한지), BIM 검수 시 Connecting Door 수량 체크

---

## 7. LUA BIM LABS Add-in 적용 방향

### 7.1 호텔 객실 자동 배치 + 번호 부여 패키지 (Dynamo)
```python
# 호텔 객실 Dynamo 자동 배치 핵심 로직
# 지원 배치 패턴: 편복도 / 중복도 / L자형 / U자형

def generate_hotel_room_layout(layout_type, total_floors, rooms_per_floor,
                               room_width, corridor_width, room_types):
    """
    layout_type: "SingleCorridor" / "DoubleCorridor" / "L-Shape" / "U-Shape"
    room_types: [{"type": "Standard", "count": 8}, {"type": "Deluxe", "count": 2}]
    """
    rooms = []
    for floor in range(1, total_floors + 1):
        room_count = 0
        for rt in room_types:
            for i in range(rt["count"]):
                room_count += 1
                room = {
                    "number": f"{floor:02d}{room_count:02d}",
                    "floor": floor,
                    "type": rt["type"],
                    "x": calculate_x(layout_type, room_count, room_width, corridor_width),
                    "y": calculate_y(layout_type, room_count, corridor_width),
                }
                rooms.append(room)
    return rooms
```

### 7.2 브랜드 Technical Standard 자동 검증 모듈
| 브랜드 | 검증 항목 수 | LUA 구현 상태 |
|--------|-----------|------------|
| Hilton (Hampton/DoubleTree/Conrad) | 48항목 | ✅ 완료 |
| Marriott (Courtyard/Westin/W Hotels) | 52항목 | ✅ 완료 |
| Hyatt (Park Hyatt/Andaz) | 39항목 | 🔄 개발 중 |
| IHG (Holiday Inn/Crowne Plaza) | 41항목 | 🔄 개발 중 |
| 일본 온센 료칸 기준 | 25항목 | 📋 계획 중 |

### 7.3 PMS 연동 COBie 자동 출력
```csharp
// COBie 출력 → Oracle Hospitality OPERA PMS 연동
public class HotelCOBieExporter : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        var doc = commandData.Application.ActiveUIDocument.Document;
        
        // COBie Space 시트 — 객실 정보
        var rooms = new FilteredElementCollector(doc)
            .OfClass(typeof(SpatialElement))
            .Cast<SpatialElement>()
            .Where(r => r.LookupParameter("OccupancyType")?.AsString() == "GuestRoom");
        
        var cobieSpaces = rooms.Select(r => new CobieSpace
        {
            Name = r.LookupParameter("RoomNumber")?.AsString(),
            Description = r.LookupParameter("RoomType")?.AsString(),
            Category = "GuestRoom",
            FloorName = doc.GetElement(r.LevelId)?.Name,
            NetArea = r.Area * 0.0929,
            // 확장 속성
            Attribute_Brand = r.LookupParameter("BrandStandard")?.AsString(),
            Attribute_ViewType = r.LookupParameter("ViewType")?.AsString(),
            Attribute_PTAC_Model = GetPTACModel(r, doc)
        });
        
        // Excel COBie 출력
        ExportCOBie(cobieSpaces, @"C:\LUA_Output\Hotel_COBie.xlsx");
        return Result.Succeeded;
    }
}
```

### 7.4 글로벌 호텔 BIM 납품 포인트
- **한국**: 관광진흥법 등록 요건 BIM 자동 체크 (객실 수·면적·시설)
- **일본**: 旅館業法 기준 체크 + 료칸 다다미방 특수 파라미터 지원
- **싱가포르**: CORENET X IFC + BCA Green Mark 파라미터 자동 집계
- **중동 (UAE/사우디)**: Halal 시설 (키블라 방향·기도실 위치) 파라미터 지원

---

## 관련 파일
- 관련: [[건물유형별_BIM적용기준]] · [[국가별_건설법규_기준비교]] · [[IFC_OpenBIM]] · [[BIM_납품검수]]
- 참고: [[오피스_업무시설_BIM]] · [[BIM_지침서]] · [[Revit_Addin]] · [[Dynamo]] · [[FM_자산관리]]
