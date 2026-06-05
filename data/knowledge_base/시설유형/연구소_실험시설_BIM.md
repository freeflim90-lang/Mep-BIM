# 연구소·실험시설 BIM 적용 기준 지식 베이스

## 2026-06-05 반도체 클린룸 BIM AR 자동화 최신 사례 심화 보강
- Source: 기계설비신문 ROUTi-AR, BIM구인동향(반도체·플랜트 수요), 캐드앤그래픽스 MEP AR 전망
- Tags: semiconductor,cleanroom,ar-bim,routing,mep-automation,plant,2026

**반도체 클린룸 BIM 자동화 최신 트렌드 (2025~2026):**
```
ROUTi-AR (SLZ 개발):
- 반도체 플랜트 Hook-up 공정 AR 자동화
- 클린룸 내 설비·MEP 경로 자동 생성
- BIM + AR + AI 통합 → 공기 단축 수개월 가능
- 현재: 15% 수동 작업 잔존 → 2026년 완전 자동화 목표

BIM+MEP 반도체 시장 수요:
- 전문 BIM 인력: 반도체·플랜트·클린룸 특화
- 채용 집중: E3D, SP3D, Revit MEP 3D 모델링
- 배관·덕트 계통 3D 모델링 → 2D 도면 자동 생성
```

**반도체 클린룸 BIM MEP 특화 요건 (추가):**
| 항목 | 기준 | BIM 적용 |
|------|------|---------|
| Hook-up 도면 | 배관 연결도 자동 생성 | ROUTi-AR 등 활용 |
| 공정 배관 | P&ID → 3D BIM 변환 | SP3D/PDMS 연동 |
| 클린룸 경계 | ISO 등급별 압력 차이 | 에어 록·에어 샤워 BIM |
| 특수가스 | H₂·NH₃·SiH₄ 배관 | 위험 구역 별도 표시 |
| UPW (초순수) | 배관 재질·전기저항 | 스테인리스 EP 배관 |

## 2026-06-05 연구소 BIM AI 즉시 답변 패턴 보강
- Source: 연구실 안전법, 클린룸 설계 기준(ISO 14644), 실험실 MEP 실무
- Tags: laboratory,cleanroom,fume-hood,special-gas,bim,mep,2026

**AI 즉시 답변 패턴 — "연구소 BIM에서 MEP 특이사항이 뭔가요?"**
```
연구소·실험시설 BIM 핵심 MEP 특이사항:
1. 흄후드(Fume Hood) 배기: 실내로 재유입 방지 — 옥상 배출 필수
   - 배기 풍속: 0.5 m/s 이상 (면속도)
   - 덕트: 내산성·내화학성 재질 (FRP 또는 스테인리스)
2. 특수가스 배관: 고순도 가스(N₂·Ar·H₂)→ 스테인리스 EP 배관
   - H₂(수소): 폭발 위험 → 전용 환기·누설 감지기 필수
3. 클린룸: ISO 등급별 환기 횟수 차이
   - ISO 5 (반도체): 시간당 600회 이상
   - ISO 7 (일반 실험): 시간당 60~90회
4. 진동 제어: 정밀 기기 주변 배관 고정 — 진동 절연 행거 사용
5. 음압(Negative Pressure): 생물 안전 구역(BSL-2↑) 음압 유지
```

**연구소 BIM LOD 특수 요건:**
| 항목 | 요건 | BIM 포인트 |
|------|------|-----------|
| 흄후드 | 위치·배기 경로 | 배기 덕트 옥상 배출 경로 |
| 클린룸 경계 | 에어 샤워·에어 록 | 청정도 등급별 압력 차이 |
| 특수가스 | 가스 종류·관경·재질 | 위험 구역 표시 |
| 무진동 구역 | 정밀기기 설치 위치 | 바닥 슬라브 두께 강화 |

## 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: #연구소BIM #실험실 #클린룸 #바이오안전 #흄후드 #특수가스 #진동제어 #동물실험실 #BSL
- 업데이트: 2026-06-05

---

## 1. 시설 개요 및 BIM 적용 특성

연구소·실험시설은 일반 업무공간과 고위험 실험공간이 결합된 복합 시설이다. BIM은 실험 등급, 압력 차, 흄후드 배기, 특수가스, 진동·전자파·청정도, 향후 연구 장비 변경성을 함께 관리해야 한다.

| 구분 | 일반 오피스 | 연구소·실험시설 |
|---|---|---|
| 공간 | 업무 존 | 연구실, 장비실, 클린룸, 폐액실 |
| 공조 | 쾌적성 | 음압·양압·환기횟수·배기 안전 |
| 설비 | 표준 MEP | 특수가스, DI Water, Vacuum, CDA, 폐액 |
| 안전 | 일반 피난 | 생물안전, 화학안전, 방폭, 비상샤워 |
| 변경성 | 낮음 | 장비 교체·실험 프로토콜 변화 큼 |

---

## 2. BIM 필수 파라미터 목록

### 2.1 실험실 안전 등급 파라미터

```
Pset_LaboratorySafety
  - Lab_Type: Chemistry / Biology / Physics / Semiconductor / Animal / Cleanroom
  - Biosafety_Level: BSL-1 / BSL-2 / BSL-3 / BSL-4 / None
  - Cleanroom_Class: ISO 3 / ISO 4 / ISO 5 / ISO 6 / ISO 7 / ISO 8 / None
  - Pressure_Mode: Positive / Negative / Neutral / Cascade
  - Pressure_Differential: 인접 실 대비 압력 차 (Pa)
  - Air_Change_Rate: 환기 횟수 (ACH)
  - FumeHood_Count: 흄후드 수량
  - Emergency_Shower: 비상샤워 설치 여부
  - Eyewash_Station: 세안기 설치 여부
  - Chemical_Storage_Class: 인화성/부식성/독성/산화성
```

### 2.2 특수 유틸리티 파라미터

| 파라미터명 | 데이터 타입 | 단위 | 설명 |
|---|---|---|---|
| Specialty_Gas_Type | IfcLabel | - | N2/O2/H2/Ar/He/Process Gas |
| Gas_Cabinet_ID | IfcLabel | - | 가스 캐비닛 ID |
| CDA_Pressure | IfcPressureMeasure | bar | Clean Dry Air 압력 |
| Vacuum_Level | IfcPressureMeasure | kPa | 진공 수준 |
| DI_Water_Resistivity | IfcReal | MOhm-cm | 초순수 저항률 |
| Exhaust_Type | IfcLabel | - | General / Acid / Solvent / Bio / Heat |
| Vibration_Criteria | IfcLabel | - | VC-A~VC-E |
| EMI_Shielding | IfcBoolean | - | 전자파 차폐 여부 |
| Waste_Liquid_Line_ID | IfcLabel | - | 폐액 배관 ID |

---

## 3. LOD 단계별 요구사항

| LOD | 연구소·실험시설 적용 내용 |
|---|---|
| LOD 100 | 연구 분야, 실험 등급, 클린룸·실험동 매스 |
| LOD 200 | 실험실 모듈, 청정·오염 구역, 주요 샤프트·장비 반입 경로 |
| LOD 300 | 흄후드·특수가스·배기·폐액·비상샤워 위치 확정 |
| LOD 350 | 압력 캐스케이드, 배기 덕트, 가스 배관, 유지보수 clearance 간섭 검토 |
| LOD 400 | 가스 캐비닛, 밸브 박스, 클린룸 패널, 장비기초 상세 |
| LOD 500 | As-Built + 실험실 안전관리·CMMS·장비 이력 연동 |

---

## 4. IFC Entity 매핑

| 요소 | IFC Entity | 비고 |
|---|---|---|
| 실험실 | IfcSpace + Pset_LaboratorySafety | 안전 등급 필수 |
| 클린룸 | IfcSpace | ISO Class, 압력 |
| 흄후드 | IfcFlowTerminal 또는 IfcBuildingElementProxy | 배기량 |
| 생물안전작업대 | IfcFlowTerminal | BSC Class |
| 특수가스 배관 | IfcPipeSegment | Gas_Type |
| 가스 캐비닛 | IfcBuildingElementProxy | Gas_Cabinet_ID |
| 폐액 배관 | IfcPipeSegment | 폐액 종류 |
| 비상샤워·세안기 | IfcSanitaryTerminal | 안전 설비 |
| 진동 제어 기초 | IfcFooting / IfcSlab | VC 기준 |

---

## 5. 국가별 기준 차이

| 국가 | BIM 기준 설계 포인트 |
|---|---|
| 한국 | 산업안전보건법, 화학물질관리법, 연구실 안전법, 고압가스·소방 기준. 실험실 등급·화학물질·배기 계통 분리 중요 |
| 일본 | 建築基準法, 労働安全衛生法, 高圧ガス保安法. 지진 시 가스 차단·장비 전도 방지·배기 안전 검토 강화 |
| 싱가포르 | BCA, SCDF, MOM, NEA 요구. 연구단지 고밀도 입주에서 화학물질 저장·배기 배출·방화 구획 중요 |
| 미국 | OSHA Lab Standard, NFPA 45, CDC/NIH BMBL, IBC. 흄후드 면풍속·생물안전·화학물질 저장 구획 매핑 |
| EU | Eurocodes, ATEX, REACH/CLP, EPBD. 화학물질 분류와 방폭·에너지 성능을 BIM 속성으로 연결 |

---

## 6. 실패 사례 Top 5

1. 연구 장비 반입 크기와 엘리베이터·복도 clearance를 검토하지 않아 반입 실패.
2. 흄후드 증설 후 배기 팬 용량과 샤프트 면적이 부족해 실험실 개소 지연.
3. 압력 캐스케이드가 공간 속성에 없어서 BSL/클린룸 검증을 수작업으로 반복.
4. 특수가스 배관과 일반 배관 색상만 다르고 IFC 속성이 없어 유지관리 위험.
5. 진동 민감 장비를 구조 스팬 중앙에 배치해 장비 성능 불량.

## 관련 링크
- [[오피스_업무시설_BIM]]
- [[공장_제조시설_BIM]]
- [[국가별_건설법규_기준비교]]
