# 스포츠시설·경기장 BIM 적용 기준 지식 베이스

## 2026-06-05 스포츠시설 BIM AI 즉시 답변 패턴 보강
- Source: 체육시설법, 소방청 대공간 소방 기준, 경기장 MEP 설계 실무
- Tags: sports,stadium,mep,hvac,sprinkler,evacuation,bim,2026

**AI 즉시 답변 패턴 — "경기장 BIM에서 MEP 설계 특이사항이 뭔가요?"**
```
경기장·스포츠시설 BIM MEP 핵심 특이사항:
1. 대공간 HVAC: 일반 건물 기준 아닌 대공간 열부하 계산 적용
   - 관중석 재실 인원 밀도: 0.25~0.4인/㎡
   - 방사패널·복사냉난방으로 에너지 효율 확보
2. 소방: 스프링클러 대신 드렌처·포소화 적용 구간 존재
   - 천장고 10m 초과: NFTC 특수 대공간 기준 적용
3. 급배수: 관중용 화장실 동시 사용률 높음 → 급수 용량 대폭 확대
4. 전기: 방송중계 전원(OB차량), 이벤트 특수조명 임시 전원 고려
5. 피난: 다수 인원 동시 피난 → 계단·출구 수와 MEP 배관 간섭 최소화
```

**스포츠시설 BIM LOD 특수 요건:**
| 항목 | 요건 | BIM 포인트 |
|------|------|-----------|
| 관람석 시야선 | 모든 좌석의 경기장 가시 확보 | Revit 시야선 분석 |
| 피난 경로 | BIM 시뮬레이션으로 피난 시간 검증 | 출구 폭·방향 |
| 잔디 냉난방 | 지열 또는 온돌 배관 | 지하 MEP 복잡도 |
| 대공간 소방 | 드렌처·포소화 구역 별도 표시 | 소방청 특수 기준 |

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #스포츠시설BIM #경기장 #관람석 #피난 #시야각 #방송중계 #잔디 #장스팬 #이벤트운영
- 업데이트: 2026-06-05

---

## 1. 시설 개요 및 BIM 적용 특성

스포츠시설·경기장은 관람객 피난, 시야각, 장스팬 구조, 방송·조명, 선수·관중 동선 분리가 핵심이다. 경기장 BIM은 건축·구조·MEP뿐 아니라 이벤트 운영, 좌석 수익, 방송 카메라 위치까지 포함해야 한다.

| 구분 | 일반 문화시설 | 스포츠시설·경기장 |
|---|---|---|
| 공간 기준 | 객석·무대 | 경기장 규격, 관람석 bowl, 선수 동선 |
| 구조 | 대공간 | 지붕 장스팬, 캔틸레버, 진동 |
| 피난 | 공연 종료 집중 | 경기 종료 동시 퇴장, 군중 흐름 |
| 설비 | 음향·조명 | 스포츠 조명, 방송, 전광판, 잔디 관리 |
| 운영 | 단일 행사 | 경기·콘서트·지역 행사 전환 |

---

## 2. BIM 필수 파라미터 목록

### 2.1 관람석·시야 파라미터

```
Pset_StadiumSeating
  - Seat_Block_ID: 좌석 블록 ID
  - Seat_Row: 열 번호
  - Seat_Number: 좌석 번호
  - Seat_Type: General / Premium / VIP / Accessible / Media
  - C_Value: 시야 C-value (mm)
  - Sightline_Status: Clear / Obstructed / Partial
  - Egress_Aisle_ID: 피난 통로 ID
  - Vomitory_ID: 관람석 출입구 ID
  - Occupant_Load: 구역별 관람 인원
  - Revenue_Category: 일반 / 프리미엄 / 스카이박스
```

### 2.2 경기장·방송·운영 파라미터

| 파라미터명 | 데이터 타입 | 단위 | 설명 |
|---|---|---|---|
| Field_Type | IfcLabel | - | Football / Baseball / Athletics / IndoorCourt |
| Field_Dimension | IfcLabel | - | 경기장 규격 |
| Lux_Level_Field | IfcIlluminanceMeasure | lux | 경기면 조도 |
| Broadcast_Camera_Position | IfcLabel | - | 방송 카메라 포인트 |
| Scoreboard_ID | IfcLabel | - | 전광판 ID |
| Crowd_Flow_Rate | IfcReal | person/min | 피난·입장 흐름 |
| Roof_Span | IfcLengthMeasure | m | 지붕 장스팬 |
| Turf_Irrigation_Zone | IfcLabel | - | 잔디 관수 존 |
| Acoustic_Mode | IfcLabel | - | 경기 / 콘서트 / 행사 |

---

## 3. LOD 단계별 요구사항

| LOD | 스포츠시설·경기장 적용 내용 |
|---|---|
| LOD 100 | 수용 인원, 경기장 규격, 지붕 매스 |
| LOD 200 | 관람석 bowl, 주요 동선, 선수·관중·VIP·미디어 구역 |
| LOD 300 | 좌석 블록, 피난 통로, 지붕 구조, 스포츠 조명, 방송실 |
| LOD 350 | 시야각 검토, 군중 피난, 조명·전광판·방송 카메라 간섭 |
| LOD 400 | 좌석·난간·지붕 접합·조명 타워·잔디 설비 상세 |
| LOD 500 | As-Built + 좌석 자산·이벤트 운영·시설관리 연동 |

---

## 4. IFC Entity 매핑

| 요소 | IFC Entity | 비고 |
|---|---|---|
| 경기장 공간 | IfcSpace | 경기 종목 속성 |
| 관람석 블록 | IfcSpace 또는 IfcSlab | Seat_Block_ID |
| 개별 좌석 | IfcFurniture | 좌석 번호 |
| 보미토리 | IfcOpeningElement 또는 IfcSpace | 피난 출입구 |
| 지붕 트러스 | IfcMember / IfcBeam | 장스팬 구조 |
| 조명 타워 | IfcColumn + IfcLightFixture | 조도 속성 |
| 전광판 | IfcBuildingElementProxy | Scoreboard_ID |
| 잔디 관수 | IfcPipeSegment / IfcDistributionSystem | 관수 존 |
| 방송 카메라 위치 | IfcAnnotation 또는 IfcProxy | 시야·전원·신호 |

---

## 5. 국가별 기준 차이

| 국가 | BIM 기준 설계 포인트 |
|---|---|
| 한국 | 건축법 문화·집회시설, 체육시설법, 소방·장애인 편의 기준. 관람석 피난·장애인석·방송 설비 구역 분리 |
| 일본 | 建築基準法, 消防法, 대형 지진 후 피난 거점 활용 고려. 지붕 구조·관람석 내진 검토 중요 |
| 싱가포르 | BCA, SCDF Fire Code, SportsSG 운영 요건. 열대 기후 차양·자연환기·군중 제어 중요 |
| 미국 | IBC Assembly, ADA, NFPA Life Safety Code, NCAA/MLB/FIFA 등 종목별 기준. 접근성 좌석과 피난 수용량 검증 |
| EU | Eurocodes, UEFA/FIFA Guide, EPBD. 군중 안전·구조 신뢰성·에너지 성능의 통합 관리 |

---

## 6. 실패 사례 Top 5

1. 좌석 수만 맞추고 C-value 시야 검토가 누락되어 일부 좌석 판매 불가.
2. 콘서트 모드 전환 시 임시 무대·조명 하중이 구조 BIM에 반영되지 않음.
3. 관중·선수·미디어 동선이 교차해 보안 운영 문제가 발생.
4. 전광판·방송 카메라·조명 위치가 늦게 확정되어 케이블트레이 재설계.
5. 지붕 배수와 관람석 하부 방수 디테일 누락으로 누수 하자 발생.

## 관련 링크
- [[공연장_문화집회시설_BIM]]
- [[건물유형별_BIM적용기준]]
- [[국가별_건설법규_기준비교]]

## 2026-06-06 스마트경기장 디지털트윈·그린경기장 BIM 보강
- Source: FIFA 지속가능성 요건, IOC Agenda 2020, PATHFINDER 피난 시뮬레이션, 국내 체육관 복합시설 BIM 사례
- Tags: smart-stadium,digital-twin,green-stadium,evacuation-simulation,bim,bems,2026

**스마트경기장 디지털트윈 BIM 운영 (2025~2026 글로벌 트렌드):**
- 경기장 BIM → **운영 디지털트윈** 전환: 관중 밀도 실시간 모니터링 + 예측 유지보수
- 핵심 활용 시나리오:
  | 시나리오 | 디지털트윈 역할 | BIM 데이터 원천 |
  |---------|--------------|--------------|
  | 이벤트 당일 군중 제어 | 출입구별 관중 밀도 → 실시간 피난 경로 조정 | IfcSpace + Occupant_Load |
  | 설비 예측 유지보수 | 조명·공조·전광판 상태 → 교체 예측 | FM BIM 자산 ID |
  | 에너지 최적화 | 경기·콘서트·비개최일 별 공조·조명 스케줄 | BEMS 연동 |
  | 구조 모니터링 | 지붕 트러스 진동·변위 센서 → 구조 BIM 연동 | IfcMember 속성 |

**군중 피난 시뮬레이션 BIM 연동 (PATHFINDER/STEPS):**
- 대형 경기장(5만 명+) 피난 시뮬레이션 → 소방청·건축심의 제출 필수
- 워크플로우:
  ```
  Revit BIM (공간·출구 배치) → IFC Export →
  PATHFINDER (피난 시뮬레이션) →
  결과: 경기 종료 후 완전 피난 목표 시간 < 8분 검증
  ```
- BIM 파라미터 강화:
  - `Egress_Flow_Rate_ppm`: 출구 단위 폭당 흐름 (명/분/m)
  - `Max_Travel_Distance_m`: 최대 보행거리
  - `Crowd_Density_Zone`: 고밀도 / 중밀도 / 저밀도 구역 지정

**그린경기장 BIM 설계 기준 (FIFA/IOC 지속가능성 요건):**
- FIFA 2026 이후 경기장: 탄소발자국 보고 의무 → BIM 내재탄소(EC) 파라미터 필요
- IOC Agenda 2020+5: 신규 올림픽 시설 → 탄소 중립 목표 (가능하면 기존 시설 활용)
- **그린경기장 BIM 체크리스트:**
  ```
  [ ] 지붕 태양광: PV_Capacity_kW 파라미터 → 연간 발전량 시뮬레이션
  [ ] 빗물 재이용: Rainwater_Harvest_m3 → 잔디 관수·화장실 flush 절수
  [ ] BEMS 연동: 경기일/비경기일 에너지 스케줄 자동화
  [ ] 잔디 관리: 지열 난방(under-pitch heating) BIM LOD 350 표현
  [ ] LED 스포츠 조명: 경기면 1,500~2,500 lux (방송 기준) + 디밍 제어
  [ ] 지속가능성 리포트: IFC 기반 EC_A1A3 탄소발자국 자동 추출
  ```

**체육관 복합시설 BIM 설계 핵심 (그린스마트학교·학교복합시설 연계):**
- 학교 체육관 + 지역 개방 스포츠센터 복합화 → 구역 분리 MEP 독립 계통 필수
- 공간 전환 모드: 실내 체육관 ↔ 다목적홀 ↔ 공연장 모드 → BIM 공간 파라미터 `Flexible_Mode`
- 비개방 시간대 에너지 절약: BEMS 야간·주말 절전 스케줄 BIM 속성화

**한국 경기장 BIM 발주 증가 배경 (2025~2027):**
- 전국 생활체육시설 노후화 교체: 30년 이상 시설 → 리모델링 BIM 수요
- 국민체육진흥공단 BIM 납품 기준 강화 예정 (공공 체육시설)
- 2036 하계올림픽 유치 검토(서울·부산 공동) → 올림픽 경기장 BIM 수요 예비 시장

**LUA BIM LABS 스포츠시설 수주 전략:**
- 체육관·수영장 복합시설 MEP BIM: 학교복합시설 사업(2025~2027 200개소) 연계
- 기존 경기장 현황 BIM → 리모델링 에너지 분석 → 그린리모델링 패키지
- 특화 기술: PATHFINDER 피난 시뮬레이션 + BIM 결합 심의 납품 → 차별화

관련: [[공연장_문화집회시설_BIM]] · [[학교_교육시설_BIM]] · [[FM_자산관리]] · [[패시브하우스_PHIKO]]
