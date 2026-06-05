# 사옥_기업본사 BIM 적용 기준 지식 베이스

## 2026-06-05 사옥 BIM AI 즉시 답변 패턴 보강
- Source: 스마트오피스 BIM 설계 기준, LEED v4, BMS/IoT 연동 실무
- Tags: corporate-hq,smart-office,bim,leed,iot,bms,2026

**AI 즉시 답변 패턴 — "기업 사옥 BIM에서 MEP 특이사항이 뭔가요?"**
```
기업 사옥(Corporate HQ) BIM MEP 특이사항:
1. 스마트오피스 연동: IoT 센서·BMS·조명제어 BIM 연동
   - 재실 감지 → 자동 조명·공조 제어
   - BEMS 통합: 에너지 소비 실시간 모니터링
2. VIP 공간 특수 설계:
   - 이사회실·CEO실: 별도 공조 계통 (독립 제어)
   - 보안 구역: 접근제어(통신) + 독립 공조 계통
3. LEED/에너지 인증:
   - 외피 열관류율, 고효율 냉동기·열회수환기
   - 재생에너지 연동 (태양광·지열)
4. 비정형 디자인:
   - 곡선 파사드 → BIM 패럴미트릭 모델링 필요
   - 루버·커튼월 패널 분할 → BIM 공장 제작 연동
```

**사옥 BIM LOD 요건:**
| 공종 | LOD 350 요건 | 특수 항목 |
|------|-------------|---------|
| HVAC | VAV 존별·VIP 독립 | 에너지 분석 연동 |
| 전기 | EMS·태양광 | 스마트미터 위치 |
| 통신/보안 | 접근제어·CCTV | 보안구역 경계 |
| 소방 | 스프링클러·제연 | 아트리움 대공간 |

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #사옥 #기업본사 #LEED #비정형설계 #스마트오피스 #IOT #VIP동선 #보안구역
- 업데이트: 2026-06-05

## 사옥_기업본사 BIM 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28

---

## 1. 시설 개요 및 BIM 적용 특성

### 시설 정의
- 기업 본사 건물: 단순 오피스와 달리 **브랜드 아이덴티티**가 건축 설계에 강하게 반영
- 규모: 대기업 사옥(3만~20만 m²), 중견기업 사옥(5,000~3만 m²)
- 대표 사례: 삼성 서초사옥, 현대차 GBC, LG 사이언스파크, Apple Park, Amazon Spheres

### 사옥 BIM의 특수 과제
| 구분 | 특성 | BIM 대응 전략 |
|------|------|-------------|
| 비정형 설계 | 브랜드 상징성 위한 곡면·비정형 외관 | Revit + Rhino/Grasshopper 연동 |
| VIP 동선 | CEO·VIP 전용 엘리베이터·출입 동선 | Security Zone 파라미터 + BIM 별도 레이어 |
| 보안 구역 | 서버실·임원실·연구소 보안 레벨 분리 | IfcZone + SecurityLevel 파라미터 |
| LEED 인증 | 글로벌 기업 ESG 전략 — LEED Gold 이상 | LEED 파라미터 BIM 전 공정 연동 |
| IoT 통합 | 스마트오피스 센서·디스플레이 위치 | BIM-IoT 좌표 매핑 |
| 홍보 활용 | BIM 모델 → 마케팅·PR 시각화 | Revit → Enscape/3ds Max 렌더링 파이프라인 |

---

## 2. BIM 필수 파라미터 목록 (IFC Property Set 기준)

### Pset_SpaceCommon + 사옥 확장
```
NetFloorArea            : 전용면적 (m²)
OccupancyType           : "Executive" / "Office" / "CommonArea" / "Server" / "Lobby" / "Amenity"
SecurityLevel           : 보안 레벨 (1~5 등급) — 5: 최고보안(서버룸)
VIPRoute                : VIP 동선 포함 여부 (Boolean)
SmartOfficeZoneID       : 스마트오피스 존 ID (IoT 시스템 연동)
LEEDCreditCategory      : LEED 크레딧 카테고리 (예: "IEQ Credit 1")
AccessControlZone       : 출입 통제 구역 ID
```

### Pset_LEED_v4_Building (LEED v4 Gold 기준)
```
LEED_SiteCategory           : SS / WE / EA / MR / IEQ / IN 중 해당
LEED_CreditNumber           : 크레딧 번호 (예: "EA Credit 2")
LEED_PointsAvailable        : 획득 가능 점수
LEED_PointsAchieved         : 실제 획득 점수
LEED_Documentation          : 문서화 상태 ("완료"/"진행중"/"미착수")
LEED_CertificationLevel     : "Certified" / "Silver" / "Gold" / "Platinum"
EnergyUseIntensity          : EUI (kBtu/ft²/yr 또는 kWh/m²/yr)
RenewableEnergyPercent      : 재생에너지 비율 (%)
WaterUseReduction           : 절수율 (%)
RecycledMaterialPercent     : 재활용 재료 비율 (%)
```

### Pset_SmartOffice_IoT (스마트오피스 IoT)
```
IoTDeviceType           : "OccupancySensor" / "AirQuality" / "SmartLighting" / "DigitalSignage" / "AccessReader"
IoTDeviceID             : IoT 기기 고유 ID (BMS 연동)
IoTProtocol             : "BACnet" / "Modbus" / "MQTT" / "KNX"
InstallationHeight      : 설치 높이 (mm) — 천장/벽/바닥
PowerSource             : "PoE" / "Battery" / "Hardwired"
DataEndpoint            : API Endpoint URL (BMS 플랫폼)
MaintenanceCycle        : 유지보수 주기 (월)
```

### Pset_SecurityZone (보안 구역)
```
SecurityZoneID          : 보안 구역 ID
SecurityLevel           : 1 (일반) ~ 5 (최고보안)
AccessCardRequired      : 카드 출입 필요 여부 (Boolean)
BiometricRequired       : 생체 인증 필요 여부 (Boolean)
CCTVCoverage            : CCTV 커버리지 여부 (Boolean)
MotionDetection         : 동체 감지 센서 여부 (Boolean)
VIPExclusiveAccess      : VIP 전용 구역 여부 (Boolean)
```

---

## 3. LOD 단계별 요구사항 (LOD 200~500)

### LOD 200 — 계획설계
- 건축: 브랜드 콘셉트 매스 (비정형 포함), 주요 공간 배치 (임원층·로비·어메니티)
- 구조: 비정형 지지 시스템 개략 (캔틸레버·아트리움 지지)
- LEED: LEED 크레딧 전략 파라미터 초기 설정
- 보안: SecurityLevel 구역 초기 배치

### LOD 300 — 실시설계
- 건축: 비정형 외피 Revit Adaptive Component 완성, 커튼월 패널 패턴 확정
  - 임원층 (Executive Floor) 전용 레이아웃 완성
  - VIP 동선 및 전용 EV Shaft 위치 확정
- LEED 파라미터: 자재별 재활용률·VOC 함량 입력 시작
- IoT: 센서·기기 위치 BIM 초안 (층별 배치 계획)

### LOD 350 — 조정설계
- 비정형 외피: Grasshopper → Revit 형상 정합 완료
- 보안 시스템 BIM: CCTV·출입통제기·금고실 위치 확정
- IoT 배선 루트: MEP 모델에 IoT 배선 트레이 포함
- LEED EA: 에너지 모델링(EnergyPlus/IES-VE) BIM 연동 완료

### LOD 400 — 제작·시공
- 비정형 패널: 패널별 제작 번호, 치수, 앵커 위치, 곡률 데이터
- 서버실: 이중바닥·항온항습·UPS 상세 BIM
- 임원 전용 EV: 전용 피트·기계실 상세

### LOD 500 — 준공 + Smart Building 운영
- IoT 기기 As-Built 위치 + 디바이스 ID BIM 반영
- LEED Certification 취득 후 BIM에 최종 점수 입력
- COBie 출력 → CAFM/IWMS 연동

---

## 4. IFC Entity 매핑 (주요 요소별)

| BIM 요소 | IFC Entity | 비고 |
|---------|-----------|------|
| 임원층 공간 | `IfcSpace` | SecurityLevel = 3, OccupancyType = "Executive" |
| 서버실 | `IfcSpace` | SecurityLevel = 5, OccupancyType = "Server" |
| 비정형 외피 | `IfcCurtainWall` | Adaptive Component 기반 |
| 비정형 패널 | `IfcPlate` | 패널 ID, 곡률 파라미터 |
| VIP 전용 EV | `IfcTransportElement` | VIPExclusiveAccess = TRUE |
| 출입통제기 | `IfcDoor` + `IfcActuator` | AccessControlZone 연결 |
| CCTV | `IfcSensor` | SensorType = "Camera" |
| IoT 센서 | `IfcSensor` | IoTDeviceID 파라미터 |
| 옥상 태양광 | `IfcEnergyConversionDevice` | PredefinedType = "SOLARCOLLECTOR" |
| 녹화 지붕 | `IfcRoof` + `IfcCovering` | LEED SS Credit 연결 |
| 공조 DOAS | `IfcAirHandlingUnit` | LEED IEQ 파라미터 |
| 빗물 재이용 탱크 | `IfcTank` | LEED WE Credit 연결 |
| 디지털 사이니지 | `IfcFurnishingElement` | IoTDeviceType = "DigitalSignage" |

---

## 5. 국가별 기준 차이

### 한국
- **친환경 인증**: 녹색건축인증(G-SEED) — 최우수(그린4등급) 기업 사옥 목표
- **BIM 납품**: 공공청사는 BIM 설계 의무, 민간 사옥은 자율 (LEED 취득 시 BIM 간접 의무)
- **소방**: 소방시설법 — 업무시설 스프링클러 (11층 이상 전층, 10층 이하 지하층)
- **에너지**: 제로에너지건축물 인증 — 공공 100%, 민간 3,000m² 이상 에너지 절약 의무

### 미국
- **LEED v4.1**: Gold 60~79점, Platinum 80점 이상 — 기업 사옥 ESG 브랜딩 핵심
- **WELL Building Standard**: 직원 웰니스 인증 — 공기질·빛·물·피트니스 파라미터 BIM화
- **Fitwel**: WELL 유사 웰니스 인증

### 일본
- **ZEB(Zero Energy Building)**: 経済産業省 ZEB 로드맵 — 大企業 2030년까지 사옥 ZEB화
- **CASBEE**: 일본 친환경 건축 평가 — S/A/B+/B-/C 등급

### 싱가포르
- **BCA Green Mark 2021**: Platinum/Gold 이상 — 대형 사옥 필수
- **CORENET X**: 2025년부터 5층 이상 모든 신축 IFC 기반 e-Submission 의무

---

## 6. 자주 발생하는 BIM 실패 사례 Top 4

### 사례 1: Rhino 비정형 형상 Revit 변환 시 면적 오류
- **원인**: Grasshopper에서 생성한 비정형 외피가 Revit으로 임포트될 때 면 분할 오류 발생 → 면적 산출 부정확, LOA(Level of Accuracy) 저하
- **해결**:
  ```python
  # Grasshopper → Revit 변환 시 DirectShape 활용 (Revit API)
  # Rhino.Inside.Revit 플러그인 사용 권장
  
  import RhinoInside.Revit
  from Autodesk.Revit.DB import *
  from Autodesk.Revit.DB.DirectShape import *
  
  # Rhino Brep → Revit DirectShape 변환
  def convert_rhino_to_revit_directshape(brep, category_id, doc):
      ds = DirectShape.CreateElement(doc, category_id)
      shape_builder = DirectShapeLibrary.GetDirectShapeLibrary(doc)
      # Brep → TessellatedShapeBuilder 변환
      builder = TessellatedShapeBuilder()
      builder.OpenConnectedFaceSet(False)
      # 면 데이터 변환 (생략)
      builder.CloseConnectedFaceSet()
      builder.Build()
      result = builder.GetBuildResult()
      ds.SetShape(result.GetGeometricalObjects())
      return ds
  ```
- **예방**: 설계 초기에 Revit 처리 가능한 형상 복잡도 한계치 협의 (면 수 제한: 10,000면 이하 권장)

### 사례 2: LEED 파라미터 중간 누락으로 인증 지연
- **원인**: BIM 초기에 LEED 파라미터 체계를 설정하지 않아, 인증 신청 단계에서 자재 데이터·에너지 수치 등을 BIM 외부에서 수작업 취합 → 오류 및 지연
- **해결**: LEED v4 크레딧 카테고리별 BIM 파라미터 매핑 테이블 작성, LOD 200 시점부터 파라미터 입력 시작
  ```
  LEED 파라미터 입력 일정:
  LOD 200: SS·WE 관련 대지/물 파라미터 설정
  LOD 300: EA(에너지) — 자재 열성능 파라미터 전수 입력
  LOD 350: MR(자재) — 재활용·친환경 자재 비율 입력
  LOD 400: IEQ(실내환경) — 공조·조명·VOC 파라미터 확정
  ```
- **예방**: BEP에 LEED 파라미터 입력 책임자·마감일 명시

### 사례 3: IoT 기기 좌표 불일치
- **원인**: BIM 모델의 IoT 센서 위치와 실제 시공 위치가 다름 → 스마트빌딩 플랫폼의 디지털 트윈 맵과 실물 불일치
- **해결**: LOD 400에서 IoT 기기 패밀리 삽입 시 BIM 좌표를 BMS 플랫폼 좌표계로 내보내는 Add-in 개발
  ```csharp
  // IoT 기기 좌표 BMS 형식 내보내기
  public class IoTLocationExporter : IExternalCommand
  {
      public Result Execute(...)
      {
          var sensors = new FilteredElementCollector(doc)
              .OfClass(typeof(FamilyInstance))
              .Cast<FamilyInstance>()
              .Where(fi => fi.LookupParameter("IoTDeviceType") != null);
          
          var iotData = sensors.Select(s => new {
              DeviceID = s.LookupParameter("IoTDeviceID")?.AsString(),
              Type = s.LookupParameter("IoTDeviceType")?.AsString(),
              X = (s.Location as LocationPoint)?.Point.X * 304.8,  // ft → mm
              Y = (s.Location as LocationPoint)?.Point.Y * 304.8,
              Z = (s.Location as LocationPoint)?.Point.Z * 304.8,
              Level = doc.GetElement(s.LevelId)?.Name
          });
          
          // JSON 출력 → BMS 플랫폼 임포트
          ExportToJson(iotData, @"C:\LUA_Output\IoTLocations.json");
          return Result.Succeeded;
      }
  }
  ```
- **예방**: As-Built 단계에서 현장 측량 데이터(토털스테이션)와 BIM 좌표 비교 검증

### 사례 4: VIP 동선 보안 정보 BIM 데이터 유출
- **원인**: 사옥 BIM 모델에 VIP 동선, 서버실 위치, 보안 카메라 위치 등이 상세히 포함 → BIM 파일 외부 공유 시 보안 취약점 노출
- **해결**: BIM 모델을 보안 레벨별로 레이어/Workset 분리, 납품 시 SecurityLevel 4~5 요소 제거한 '공개용 IFC' 별도 생성
  ```python
  # 보안 요소 제거 IFC 내보내기 스크립트
  def export_public_ifc(doc, output_path):
      # SecurityLevel 4~5 요소 숨김 처리
      elements_to_hide = FilteredElementCollector(doc)\
          .WhereElementIsNotElementType()\
          .ToElements()
      
      elements_to_hide = [e for e in elements_to_hide 
                          if e.LookupParameter("SecurityLevel") is not None
                          and e.LookupParameter("SecurityLevel").AsInteger() >= 4]
      
      # Override Graphics로 숨김 후 IFC 내보내기
      with Transaction(doc, "Hide Security Elements") as t:
          t.Start()
          view = doc.ActiveView
          for elem in elements_to_hide:
              ogs = OverrideGraphicSettings()
              ogs.SetHalftone(True)  # 또는 완전 숨김
              view.SetElementOverrides(elem.Id, ogs)
          t.Commit()
      
      # IFC 내보내기 실행
      ExportIFC(doc, output_path)
  ```
- **예방**: BIM 데이터 보안 분류 정책 수립 (공개/제한/기밀), BEP에 명시

---

## 7. LUA BIM LABS Add-in 적용 방향

### 7.1 사옥 BIM → 홍보 자료 자동 생성 파이프라인
```
Revit BIM 모델
    ↓ [Enscape Real-time Rendering 연동]
고해상도 렌더링 이미지 (2K/4K)
    ↓ [Panorama 360° 내보내기]
VR 투어 파일 (.exe / Web GL)
    ↓ [Navisworks → BIM 360]
인터랙티브 BIM 모델 (클라이언트 공유)
```
- LUA Add-in 기능: Revit → Enscape 카메라 뷰 자동 설정 (로비·임원층·옥상 고정 뷰 10종)
- 클라이언트 PR 패키지: 렌더링 + 면적표 + LEED 인증 예상 점수를 원클릭 출력

### 7.2 LEED/G-SEED 파라미터 자동 집계 대시보드
| 크레딧 | BIM 파라미터 | 자동 계산 여부 |
|--------|------------|-------------|
| EA Prereq 2 최소 에너지 성능 | EUI (kWh/m²/yr) | ✅ EnergyPlus 연동 |
| WE Credit 1 실외 급수 절감 | WaterUseReduction (%) | ✅ 자동 |
| MR Credit 2 환경영향 감소 | RecycledMaterialPercent | ⚠️ 자재 DB 연동 필요 |
| IEQ Credit 1 실내 공기질 | CO2 센서 데이터 | ✅ IoT 연동 |
| SS Credit 5 우선 부지 | 대지 좌표 → GIS 분석 | ✅ API 자동 |

### 7.3 스마트오피스 BIM-IoT 통합 모듈
- IoT 기기 Revit Family 라이브러리 (200종 이상): 센서·디스플레이·스마트 스위치
- BMS/BAS 플랫폼 연동 API (BACnet/MQTT) 내장
- 실시간 재실 현황 BIM 뷰 (색상 오버레이) — 일본·싱가포르 스마트빌딩 납품 레퍼런스

---

## 관련 파일
- 관련: [[건물유형별_BIM적용기준]] · [[국가별_건설법규_기준비교]] · [[IFC_OpenBIM]] · [[BIM_납품검수]]
- 참고: [[오피스_업무시설_BIM]] · [[BIM_지침서]] · [[Revit_Addin]] · [[Dynamo]] · [[FM_자산관리]]
