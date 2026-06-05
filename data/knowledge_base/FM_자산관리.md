# FM(시설관리) 자산관리 BIM 지식 베이스

## 2026-06-05 기계설비법 2026 성능점검 개정 긴급 업데이트 (심화 보강)
- Source: 기계설비신문, 보고서넷 2026 기계설비법 개정 분석, 국토부 기계설비 성능점검 매뉴얼
- Tags: fm,mechanical-equipment-law,performance-check,revision,2026

**기계설비법 2026 개정 핵심 변경사항 (KST01 공식확인):**
```
2026년 기계설비법 주요 개정:
1. 성능점검 대상 축소:
   - 장기간 미사용 설비 → 점검 대상 제외 가능
   - 실질적으로 가동되는 안전·효율 영향 설비로 집중
2. 자체 성능점검 확대:
   - 인력·장비·체계 갖춘 관리주체 → 자체 점검 가능
   - 외부 성능점검 기관 의존도 감소
3. 유지관리 vs 성능점검 업무 분리 명확화
4. 성능점검보고서 의무 제출 강화:
   - 이전: 지자체 요청 시에만 제출
   - 변경: 의무 제출 (위반 시 개선명령)
5. 점검 기준일 개선: 완공일이 아닌 '준공연월일' 기준

BIM FM 이관 시 적용:
- COBie Component에 성능점검 의무 여부 파라미터 추가
- 자체 점검 가능 여부 → FM 시스템 자동 판별 로직 연동
- 성능점검보고서 링크 → BIM 자산 데이터에 연결
```

**기계설비 성능점검 주기 (개정 후 기준):**
| 설비 유형 | 점검 주기 | 비고 |
|---------|---------|------|
| 완공 후 첫 점검 | 준공연월일로부터 1년 내 | 개정: 준공연월일 기준 |
| 이후 정기 점검 | 1년마다 1회 이상 | 원칙 |
| 냉방설비 | 격년 (홀수년 또는 짝수년) | 냉방·난방 분리 |
| 난방설비 | 격년 (냉방과 교대) | 매년 전체 아님 |

## 2026-06-05 스마트빌딩 BAS/BEMS/디지털트윈 FM BIM 통합 운영 보강
- Source: 공학저널, 한화시스템, 삼성SDS 인사이트, 건물유지관리산업전 2026
- Tags: fm,bas,bems,smart-building,digital-twin,iot,cafm,ai-building,2026

**AI 즉시 활용 — 고객 질문 "BAS, BEMS, FM이 어떻게 연동되나요?"에 대한 답변 패턴:**
```
BAS(건물자동제어)·BEMS(에너지관리)·FM(시설관리)은 2026년 이후 분리 운영이 아닌
하나의 통합 UI에서 관리하는 것이 스마트빌딩 표준입니다.
- BAS: 냉난방·조명·환기·엘리베이터 자동 제어
- BEMS: 에너지 소비 모니터링·절감 목표 관리
- FM: 유지보수·PPM·장애 이력 관리
BIM 모델이 이 세 시스템의 '공간 기준'을 제공합니다.
```

**스마트빌딩 BIM-FM 통합 구조 (2026 기준):**
- **BAS/BMS**: 제어 설비(공조기, 펌프, 조명)의 On/Off·설정값·알람 관리
- **BEMS**: 전기·가스·수도·열량 미터별 에너지 집계 및 탄소 배출 관리
- **CAFM**: 유지보수 워크오더, PPM 일정, 자산 이력
- **BIM 디지털트윈**: BIM 3D 공간에 BAS 실시간 데이터 오버레이 → 문제 위치 즉시 파악

**국내 AI 자율운전 스마트빌딩 기술 (2026 상용화):**
- 나라컨트롤 iBEEMS: AI 기반 자율운전 — 패턴 학습으로 냉난방 예측 제어
- 에너지·탄소 통합 관리: 탄소중립 목표 건물에 CO₂ 배출량 실시간 추적
- 2026 건물유지관리산업전 전시 기술: AI 통합관제, 스마트 공간 예약, 디지털트윈 빌딩 시각화

**FM BIM 디지털트윈 운영 레이어:**
| 레이어 | 데이터 | 갱신 주기 |
|--------|--------|-----------|
| BIM 모델 | 공간·설비 형상 기준 | 모델 변경 시 |
| BAS 실시간 | 온도·압력·상태 포인트 | 1~5분 |
| BEMS 미터 | 에너지 소비량 집계 | 15분~1시간 |
| CAFM 이력 | 유지보수·PPM 기록 | 워크오더 완료 시 |
| 센서/IoT | 공기질·재실·조명 | 1분 미만 |

**BIM-FM 이관 품질 체크리스트 (AI 답변 즉시 사용):**
- [ ] LOD 500 As-Built 모델 완성 여부
- [ ] COBie Component/Type 시트에 SerialNumber·InstallationDate 입력
- [ ] 각 설비의 O&M 문서 링크 연결
- [ ] BAS 포인트 ID와 BIM 설비 GUID 매핑표 작성
- [ ] 기계설비법 성능점검 대상 여부 및 점검 주기 기재
- [ ] 에너지효율등급/ZEB 인증 결과값과 BEMS 목표 EUI 분리 확인
- [ ] 저수조·배수설비 위생점검 기록 연결

관련: [[IFC OpenBIM 지식 베이스]] · [[설비자동제어 지식 베이스]] · [[설비장비 지식 베이스]] · [[위생 지식 베이스]]

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


## 2026-06-04 기계설비법 기반 FM 이관 보강
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_MECHANICAL_EQUIPMENT_MAINTENANCE_LAW_UPDATE.md`
- Tags: fm,mechanical-equipment-law,maintenance,performance-check,cobie,official-source

FM BIM 이관 시 기계설비법과 기계설비 유지관리기준 적용 여부를 확인한다. 장비대장, COBie, O&M 문서, 유지관리지침서, 성능점검 보고서 대응 데이터를 서로 연결해야 한다.

FM 추가 필드:
- 기계설비법 적용 여부
- 점검대상 기계설비 여부
- 성능점검 대상 여부
- 점검 주기
- 점검 항목
- 측정 위치
- 유지관리 책임 주체
- O&M 문서 링크
- 성능점검 보고서 참조 ID

운영 기준:
- COBie Component/Type 데이터는 장비 형상만이 아니라 유지관리·성능점검 책임과 연결한다.
- 성능점검 주기와 점검 항목은 법령·고시·발주처 요구·제조사 O&M 문서 확인 전 확정하지 않는다.

관련: [[설비장비 지식 베이스]] · [[BIM 납품검수 지식 베이스]] · [[ACC BIM360 CDE 지식 베이스]]


## 2026-06-04 에너지/ZEB 기반 FM 이관 보강
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_ENERGY_ZEB_STANDARD_UPDATE.md`
- Tags: fm,energy-saving-design,ZEB,BEMS,COBie,official-source

FM BIM 이관 시 에너지절약계획서, 에너지효율등급, ZEB 인증 결과와 운영 데이터가 끊기지 않아야 한다. 준공 모델은 인증 결과를 설명하는 모델이자, 운영 중 에너지 사용량을 추적하는 기준 모델로 사용될 수 있다.

FM 추가 필드:
- 에너지절약계획서 적용 여부
- 에너지효율등급/ZEB 인증 대상 및 등급
- 단위면적당 1차에너지소요량 참조 ID
- 에너지자립률 참조 ID
- 냉방/난방/급탕/조명/환기 용도별 계량 구분
- 신재생에너지 설비 ID와 대지 내/외 구분
- BEMS/BAS 포인트 및 에너지미터 ID
- 예비인증/본인증 문서 링크

운영 기준:
- 인증 제출 수치와 운영 EUI 수치는 같은 값이 아니다. FM 이관 시 설계 인증값, 준공 본인증값, 운영 실측값을 분리한다.
- 자동 수집된 EUI 평균값과 절감률 문장은 프로젝트 운영 KPI로 확정하기 전에 발주처 목표, 계량 범위, 건물 용도, 인증 기준을 확인한다.

관련: [[설비자동제어 지식 베이스]] · [[BIM 납품검수 지식 베이스]] · [[2026-06-04 LUA BIM LABS Energy ZEB Standard Update]]


## 2026-06-04 위생·저수조·배수설비 FM 이관 보강
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_PLUMBING_WATER_TANK_DRAINAGE_STANDARD_UPDATE.md`
- Tags: fm,plumbing,water-tank,drainage,water-quality,official-source

FM BIM 이관 시 저수조와 배수설비는 수질·위생·신고·유지관리 기록과 연결한다. 준공 모델에는 저수조 위생점검 대상, 청소 접근성, 급수 계통, 공공하수도 접속, 집수정/펌프 점검 정보를 남겨야 한다.

FM 추가 필드:
- 저수조 설치기준 적용 여부
- 저수조 위생점검 대상 여부
- 저수조 청소/위생점검 기록 ID
- 먹는물 수질검사 기록 ID
- 맨홀, 통기관, 월류관, 배수구, 경보장치 ID
- 소화용수 역류방지장치 ID
- 배수설비 설치 신고 참조 ID
- 공공하수도 접속 위치와 복구 기록
- 집수정/오수펌프/배수펌프 점검 기록

운영 기준:
- FM 이관 데이터는 장비명과 위치만으로 충분하지 않다. 수질검사, 위생점검, 청소, 공공하수도 접속 증빙과 연결한다.
- 자동 수집된 점검 주기와 수질 기준 문장은 공식 법령·고시·지자체 요구 확인 전 운영 KPI로 확정하지 않는다.

관련: [[위생 지식 베이스]] · [[설비장비 지식 베이스]] · [[BIM 납품검수 지식 베이스]] · [[2026-06-04 LUA BIM LABS Plumbing Water Tank Drainage Standard Update]]
