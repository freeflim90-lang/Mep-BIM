# 일반건물·빌딩 BIM 적용 기준 지식 베이스

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: general-building,mixed-use,commercial-tower,bim,lod,ifc,neighborhood,small-building
- 업데이트: 2026-05-28

"일반건물"은 단일 용도로 분류하기 어려운 범용 건물을 포괄한다.  
- **근린생활시설 소형 건물**: 5층 이하, 1~2종 근생 혼합, 소규모 건축사무소가 주로 설계
- **도심 상업 빌딩**: 지상 10~40층, 저층부 상업+고층부 오피스 복합, 임대 목적
- **혼합용도(Mixed-Use) 타워**: 오피스+판매+주거+호텔 수직 복합

이 세 유형은 BIM 요구 수준·파라미터·납품 기준이 다르므로 각각 분리해 다룬다.

---

## 일반건물·빌딩 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: general-building-bim,small-building,commercial-tower,mixed-use-bim,neighborhood-facility

---

### 1. 유형별 BIM 적용 수준

| 유형 | 규모 | BIM 의무 여부 | 현실 LOD 수준 | 주요 Pain Point |
|---|---|---|---|---|
| **소형 근린생활시설** | 3~5층, 연면적 500~2,000m² | 미의무 (임의) | LOD 200~250 | BIM 비용 대비 효과 의문, 수작업 도면 병행 |
| **중형 상업 건물** | 6~15층, 2,000~10,000m² | 민간 선택 / 공공 일부 의무 | LOD 300 | 설계사·시공사 BIM 수준 불일치 |
| **도심 상업 빌딩** | 15~40층, 10,000~50,000m² | 대부분 자체 BIM 요구 | LOD 350~400 | 임대 면적 산정, 커튼월 납품, CDE 관리 |
| **혼합용도 타워** | 20층+, 50,000m²+ | 공공 발주 BIM 의무 | LOD 350~500 | 공종 간 데이터 정합성, 용도별 규정 충돌 |

---

### 2. 소형 근린생활시설 BIM

#### 2-1. 특성
소형 건물에 BIM을 적용하는 경우는 대부분 건축주의 자체 요구나 건축사무소의 품질 관리 목적이다. LOD 200~250이 현실적 목표.

**BIM 필수 파라미터:**
```
건물 기본 정보:
- 건축물 용도 (BuildingUse): 1종/2종 근생, 주거, 교육 등
- 연면적 (GrossFloorArea_m2)
- 건폐율 (BuildingCoverageRatio_%): 법정 한도 자동 체크
- 용적률 (FloorAreaRatio_%): 법정 한도 자동 체크
- 높이 제한 준수 여부 (HeightCompliance): 일조권 사선 제한

공간 분류:
- 용도별 면적 (AreaByUse): 주거/근생/주차/기계
- 주차 대수 (ParkingCount): 용도별 설치 기준 자동 산출
- 화장실 수 (ToiletCount): 연면적 기준 법적 최소 수량
```

**소형 건물 BIM 최소 납품 기준 (건축 허가용):**
| 도면 | BIM 요소 | 최소 LOD |
|---|---|---|
| 배치도 | 대지 경계·건물 외곽·주차 | LOD 200 |
| 평면도 | 벽·문·창·공간 면적 | LOD 250 |
| 입면도 | 외벽 마감 재질 파라미터 | LOD 250 |
| 단면도 | 층고·지붕 구조 형태 | LOD 200 |

**소형 건물 BIM 실패 사례:**
- 용적률/건폐율 위반: BIM 공간 면적 합산 오류로 계획 설계 말기에 법적 한도 초과 발견 → 평면 전면 재설계. 해결: 프로젝트 생성 시점에 용적률·건폐율 파라미터 자동 경고 설정.
- 주차장 면적 미확보: 용도별 주차 대수 기준을 BIM에 반영하지 않아 허가 반려. 해결: 용도 입력 시 법정 주차 대수 자동 계산 후 지하 주차장 면적 확보 여부 체크.

---

### 3. 도심 상업 빌딩 (Commercial Tower)

#### 3-1. 특성
임대용 오피스·상업 빌딩은 **임대 면적 극대화**가 핵심 설계 목표. 코어 효율과 임대 면적 비율(Efficiency)이 BIM 설계의 주요 KPI다.

**BIM 필수 파라미터:**
```
면적 체계 (BOMA 2017 기준):
- BOMA 임대 가능 면적 (RentableArea_m2): 전용 + 공용 지분
- 코어 면적 (CoreArea_m2): 엘리베이터·계단·기계실·화장실
- 층 효율 (FloorEfficiency_%): 임대/전체 (목표 75~85%)
- 부하율 (LoadFactor): 공용 면적 분배 비율

커튼월:
- 패널 유형 (CurtainWallPanelType): Unitized/Stick
- 유리 성능 (GlazingUvalue): 열관류율 (한국 지역별 기준)
- SHGC: 태양열 취득률
- 스팬드럴 패널 유무 (SpandrelPanel): 층간 차열

층 구성:
- 저층부 용도 (PodiumUse): 판매/로비/주차
- 표준층 평면 (TypicalFloor): 반복 층 기준 파라미터 세트
- 피난안전구역 층 (RefugeFloor): 30층 초과 시 법적 요구 (한국)
- 기계층 (MechanicalFloor): MEP 수직 조닝 기준점
```

**표준층(Typical Floor) BIM 전략:**
```python
# Dynamo Python: 표준층 면적 자동 집계
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Level

doc = IN[0]
typical_levels = [l for l in FilteredElementCollector(doc)
                  .OfCategory(BuiltInCategory.OST_Levels)
                  .ToElements()
                  if "TYPICAL" in l.Name.upper() or "표준" in l.Name]

# 각 표준층의 공간 면적 합산
results = []
for level in typical_levels:
    spaces = [s for s in FilteredElementCollector(doc)
              .OfCategory(BuiltInCategory.OST_Rooms)
              .ToElements()
              if s.Level.Id == level.Id]
    total_area = sum(s.Area * 0.0929 for s in spaces)  # SF → m²
    results.append({"Level": level.Name, "TotalArea_m2": round(total_area, 2)})

OUT = results
```

**IFC 매핑:**
| 요소 | IFC Entity | Property Set |
|---|---|---|
| 임대 공간 | `IfcSpace` | `Qto_SpaceBaseQuantities`, BOMA Pset |
| 커튼월 | `IfcCurtainWall` | `Pset_CurtainWallCommon` |
| 코어 벽 | `IfcWall` | `Pset_WallCommon.IsExternal=false` |
| 기계층 구획 | `IfcSpace` | PredefinedType=TECHNICAL |

---

### 4. 혼합용도 타워 (Mixed-Use Tower)

#### 4-1. 특성
주거+오피스+판매+호텔+문화가 수직으로 적층되는 복합 건물. 각 용도별로 다른 규정·파라미터·BIM 표준이 충돌한다.

**용도별 방화구획 충돌 해결 원칙:**
```
공동주택 용도: 세대 전체 방화구획 (면적 500m² 이하)
오피스 용도: 1,000m² (스프링클러 미설치) / 3,000m² (스프링클러)
판매시설: 1,000m²
호텔: 객실별 방화 차단 + 복도 방화 구획

충돌 지점:
- 저층부 판매 → 중층부 오피스 → 고층부 주거 전환 층:
  방화구획 경계가 용도 전환 층에서 반드시 완전 격리되어야 함
  → BIM에서 용도 전환 층 Slab에 방화 파라미터 명시적 부여
```

**혼합용도 BIM 필수 파라미터:**
```
BuildingMixedUseProfile:
- PodiumUse: "Retail+Parking" (1~5층)
- OfficeFloors: "6~25" (표준 오피스 층 범위)
- HotelFloors: "26~40" (호텔 객실 층)
- ResidentialFloors: "41~60" (주거 층)
- SkyLobby: "26, 41" (수직 동선 분기 로비 층)

법적 요구:
- ParkingRatio_Residential: 세대당 1.0대 이상
- ParkingRatio_Office: 연면적 134m²당 1대
- ParkingRatio_Retail: 연면적 60m²당 1대
→ 용도별 주차 대수 합산 자동 계산
```

**혼합용도 BIM 실패 사례:**

1. **피난 동선 용도별 분리 미흡**: 주거·오피스·호텔 거주자가 동일 비상 계단을 공유하면 화재 시 혼잡 발생. 한국 건축법 시행령 제46조: 용도가 다른 경우 피난 계단 분리 또는 층별 잠금 설비 설치 의무. BIM에서 계단 공유 여부 자동 체크 규칙 필요.

2. **용도별 주차 대수 합산 오류**: 각 용도의 주차 기준을 따로 적용하지 않고 총 연면적에 단일 기준 적용 → 허가 반려. BIM 공간 분류(IfcSpace.OccupancyType)별 주차 기준 계수를 JSON으로 관리하고 자동 산출.

3. **층 구분 경계 MEP 충돌**: 오피스→호텔 전환 층에서 HVAC 조닝이 바뀌는데 덕트 수직 관통이 용도 경계를 무시하고 설계됨 → 방화 댐퍼 누락. 방화구획 경계 관통 자동 감지 규칙 적용.

---

### 5. 국가별 일반 건물·빌딩 기준 차이

| 항목 | 한국 | 일본 | 싱가포르 | 미국 (IBC) |
|---|---|---|---|---|
| 건폐율·용적률 | 용도지역별 (국토계획법) | 用途地域別 (都市計画法) | Plot Ratio (DC 규정) | FAR (Floor Area Ratio) 지자체별 |
| 초고층 기준 | 50층 이상 또는 200m | 60m 이상 (초고층) | 140m 이상 | 75ft (22.9m) 이상 — 고층 기준 |
| 커튼월 에너지 | 열관류율 지역별 고시 | 省エネ法 U값 기준 | BCA Green Mark 기준 | ASHRAE 90.1 SHGC·U값 |
| 혼합용도 용도 정의 | 건축법 용도 분류 | 用途地域 복합 시 특례 | Mixed Development 허가 | IBC Occupancy Separation |

---

### 6. LUA BIM LABS 소형·중형 건물 시장 전략

**소형 건물 시장 — 볼륨 전략:**
- 한국 연간 건축 허가 건수: 약 15만 건/년 → 소형 건물 약 12만 건
- LUA BIM LABS 기회: 저가형 납품 자동화 툴 (월 2~5만원) → 소형 건축사무소 대상 SaaS
- 진입 채널: 건축사협회 제휴, 건축사 시험 기관 협력

**도심 빌딩 시장 — 프리미엄 전략:**
- 대형 디벨로퍼(롯데·현대·SK 등) BIM 표준화 수요
- 임대 면적 최적화 Add-in → 발주처 설계 검토 도구
- 커튼월 BIM 자동화 → 커튼월 전문 시공사(한국커튼월, 삼성엔지니어링) 협력

- 관련: [[건물유형별_BIM적용기준]] · [[국가별_건설법규_기준비교]] · [[아파트_공동주택_BIM]] · [[오피스_업무시설_BIM]] · [[IFC_OpenBIM]] · [[BIM_납품검수]] · [[해외건설기업_동향분석]]
