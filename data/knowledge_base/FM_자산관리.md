# FM(시설관리) 자산관리 BIM 지식 베이스

## FM BIM 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: fm,facility-management,cobie,cafm,bim,lod500,asset

FM(Facility Management) BIM은 완공 후 건물 운영·유지보수에 BIM 모델을 활용하는 단계.
LOD 500(As-Built) 모델 + COBie 데이터 → CAFM/CMMS 시스템 연동.

**COBie(Construction Operations Building Information Exchange):**
- NBIMS-US v3 기반, 영국 BS 1192-4:2014 채택, 국토부 BIM 업무지침 COBie 제출 권고
- Excel 형식: Component(기기 ID), Type(유형), Space(공간), Job(유지보수 이력), Resource(자재·부품)

## FM 자산관리 BIM Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: fm,cobie,cafm,cmms,bim,revit,lod500,digital-twin

**COBie 필수 시트 및 파라미터:**
| 시트 | 핵심 컬럼 | 비고 |
|---|---|---|
| Facility | ProjectName, SiteName | 프로젝트 기본 정보 |
| Floor | FloorName, Elevation | 층별 정보 |
| Space | SpaceName, RoomTag, FloorName | 실 정보 (Revit Room) |
| Component | Name, TypeName, SerialNumber, InstallationDate | 기기별 고유 ID |
| Type | Name, Manufacturer, ModelNumber, WarrantyDuration | 기기 유형 스펙 |
| Job | Name, JobType, Frequency, TaskStartUnit | 유지보수 주기 |

**Revit → COBie 자동 추출 설정:**
- Revit 공유 파라미터 → COBie 시트 매핑 (Autodesk COBie Extension 또는 자체 Dynamo 스크립트)
- `COBie.Component.SerialNumber`: 제조 일련번호 (설비팀 현장 입력)
- `COBie.Type.WarrantyDuration`: 냉동기 2년, 펌프 1년, 소화기 1년 (법정 하자보수 기간)
- Python openpyxl: Revit Schedule CSV → COBie.xlsx 자동 변환

**디지털 트윈 연동 (Autodesk Tandem):**
- ACC → Autodesk Tandem: LOD 500 모델 업로드 → BAS BACnet 실시간 데이터 오버레이
- 센서 포인트 매핑: `IfcSensor` → Tandem Parameter (온도·압력·에너지 사용량)
- PM 알림: 냉동기 가동 시간 4,000h 초과 시 → 점검 알림 자동 생성
- 에너지 벤치마킹: ENERGY STAR Portfolio Manager API 연동 (연간 에너지 원단위 비교)

**CAFM 솔루션 연동 옵션 (2026 기준):**
- IBM TRIRIGA: IFC/COBie 임포트, 대형 공공건물 주요 채택
- Archibus: COBie 직접 임포트, 국내 대학·병원 다수 사용
- FM:Systems: ACC/BIM 360 네이티브 연동
- 자체 개발: FastAPI + PostgreSQL + ifcopenshell → LUA BIM LABS Add-in 연동 가능
- 관련: [[BIM_지침서]] · [[IFC_OpenBIM]] · [[설비장비]] · [[ACC_BIM360]]

## FM 자산관리 실전 운영 심화 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: fm,asset-management,ppm,work-order,energy,cobie,cafm

**예방유지보수(PPM) 계획 수립 기준:**
| 설비 유형 | 점검 주기 | 법적 근거 | 주요 항목 |
|---|---|---|---|
| 냉동기 | 연 2회 (6월·12월) | 고압가스 안전관리법 | 냉매 충전량·압력·COP 측정 |
| 공조기(AHU) | 분기 1회 | 건물 위생 관리 규정 | 필터 교체·코일 세척·벨트 점검 |
| 소화펌프 | 월 1회 작동 확인 | 화재예방법 시행규칙 | 압력계·기동·충압 펌프 확인 |
| 수변전 설비 | 연 1회 | 전기안전관리법 | 절연저항·접지저항·보호계전기 |
| 승강기 | 월 1회 자체·연 1회 법정 | 승강기 안전관리법 | 브레이크·안전장치·와이어로프 |

**에너지 소비 벤치마킹 (EUI 기준):**
- EUI(Energy Use Intensity) = 연간 에너지 사용량(kWh) ÷ 건물 연면적(㎡)
- 국내 업무용 건물 평균 EUI: 250~350 kWh/㎡·년
- LEED 에너지 최적화 목표: 평균 대비 30% 절감 (175~245 kWh/㎡·년)
- BAS 에너지 미터 → Python 집계 → ENERGY STAR Portfolio Manager API 업로드

**Revit → FM 시스템 COBie 자동 전환 스크립트:**
```python
import openpyxl
# Revit Schedule CSV → COBie.xlsx Component 시트 생성
wb = openpyxl.Workbook()
ws = wb.create_sheet("Component")
ws.append(["Name","TypeName","SerialNumber","InstallationDate","WarrantyDuration"])
for row in revit_schedule_data:
    ws.append([row["ID"], row["Type"], row["Serial"], row["Install"], row["Warranty"]])
wb.save("COBie_Package.xlsx")
```

**디지털 트윈 운영 KPI:**
- 설비 가동률: 목표 99% 이상 (계획 정지 제외)
- 예방 대 사후 유지보수 비율: PPM 80% : 사후 20% 목표
- 에너지 절감율: 전년 대비 5% 이상
- 입주자 만족도: 연간 설비 서비스 만족도 4.0점/5.0점 이상
- 관련: [[IFC_OpenBIM]] · [[설비장비]] · [[ACC_BIM360]] · [[엔지니어링계산서]]
