---
type: knowledge-note
domain: 설비기초
sub: MEP전체분류
date: 2026-05-22
tags: [설비, MEP, 공조, 위생, 전기, 소방, 기계, 분류체계]
---

# 설비 기초 — MEP 시스템 전체 분류

> **MEP** = Mechanical + Electrical + Plumbing. 건물의 모든 설비를 포괄하는 용어.
> BIM에서는 건축(Architecture) + 구조(Structure)와 함께 3대 분야로 구분.

---

## 1. MEP 전체 분류 체계

```
MEP 설비
│
├── M — 기계설비 (Mechanical)
│   ├── 공조 (HVAC)
│   │   ├── 냉방 설비 (냉동기, 냉각탑, AHU, FCU)
│   │   ├── 난방 설비 (보일러, 열교환기, 방열기)
│   │   ├── 환기 설비 (급기팬, 배기팬, 전열교환기)
│   │   └── 자동제어 (DDC, BAS/BMS)
│   ├── 위생 (Plumbing)
│   │   ├── 급수/급탕 (수도, 가압펌프, 급탕기)
│   │   ├── 배수/통기 (오배수, 우수, 집수정)
│   │   └── 가스 (도시가스, LPG)
│   └── 소방기계 (Fire Protection - Mechanical)
│       ├── 스프링클러 (습식/건식/준비작동식)
│       ├── 연결송수관 (Standpipe)
│       ├── 옥내소화전
│       └── 가스계 소화 (CO₂, 청정소화약제)
│
├── E — 전기설비 (Electrical)
│   ├── 수변전 (수전, 변압기, 발전기, UPS)
│   ├── 배전 (배선, 트레이, 분전반)
│   ├── 조명
│   ├── 동력 (모터, 엘리베이터, 에스컬레이터)
│   ├── 통신/약전 (LAN, 전화, 방송, CCTV)
│   └── 소방전기 (감지기, 수신기, 방재연동)
│
└── P — 배관 (Plumbing)
    ※ 한국에서는 보통 위생배관을 M에 포함
    ※ 국제 표준에서는 별도 P 분류
```

---

## 2. 공종별 Revit 카테고리 매핑

| 공종 | Revit 분류 | 대표 패밀리 |
|---|---|---|
| 공조 덕트 | Ducts, Duct Fittings, Duct Accessories | 장방형/원형 덕트, 댐퍼, 소음기 |
| 공조 기기 | Mechanical Equipment | AHU, FCU, 냉동기, 냉각탑 |
| 배관 | Pipes, Pipe Fittings, Pipe Accessories | 강관, 동관, PVC, 밸브 |
| 위생기구 | Plumbing Fixtures | 양변기, 세면기, 싱크대 |
| 전기 배관 | Conduits, Conduit Fittings | 금속관, 합성수지관 |
| 전선관 | Cable Trays, Cable Tray Fittings | 사다리형, 바닥형 |
| 전기 기기 | Electrical Equipment | 분전반, 수배전반 |
| 소방 | Sprinklers, Fire Protection Systems | 헤드, 알람밸브 |

---

## 3. 공종별 역할과 담당 시스템

### 3-1. 냉방 계통 흐름

```
외기 → AHU (에어핸들링유닛)
          ↑              ↓
     냉수 환수        냉수 공급 (7℃)
     (CHW-R 13℃)   (CHW-S 7℃)
          ↑              ↓
       냉동기 (Chiller)
          ↑              ↓
     냉각수 공급    냉각수 환수
     (CW-S 32℃)   (CW-R 37℃)
          ↑              ↓
          냉각탑 (Cooling Tower) ← 외기로 열 방출
```

### 3-2. 난방 계통 흐름

```
보일러 / 열교환기
    ↓ 온수 공급 (60℃)
AHU / FCU / 방열기 (팬코일유닛)
    ↓ 온수 환수 (50℃)
보일러 / 열교환기 (재가열)
```

### 3-3. 환기 계통 흐름

```
외부 → OA 덕트 → AHU → SA 덕트 → 실내 취출구 (디퓨저)
                              실내
실내 → RA 덕트 → AHU → 재처리 (일부)
              → EA 덕트 → 외부 배출 (나머지)
```

### 3-4. 급배수 계통 흐름

```
수도 본관 → 저수조 → 가압펌프 → 각 층 급수 (CWS)
                               → 급탕기 → 각 층 급탕 (HWS)
                                              ↕
                                        급탕환수 (HWR)

각 위생기구 → 오배수관 → 집수정/공공하수관
옥상/외부   → 우수관 → 우수집수정/공공우수관
```

---

## 4. 건물 용도별 주요 설비 구성

| 건물 유형 | 특이 설비 | 핵심 고려사항 |
|---|---|---|
| 업무(오피스) | VAV 시스템, FCU, 전열교환기 | 개별 제어, 에너지 절감 |
| 병원 | 의료가스(O₂, N₂O), 진공, 증기, 음압격리실 | 무균·감염 제어, 무정전 |
| 데이터센터 | 정밀공조(CRAC), UPS, 발전기, 이중화 | 항온항습, 신뢰성 |
| 주거 | 세대별 보일러, 환기(바닥복사 난방) | 열교 차단, 습기 제어 |
| 산업시설 | 공정 배관, 집진, 압축공기, 특수가스 | 공정 요구사항 우선 |
| 호텔 | 중앙 공조 + 객실 개별 제어, 주방 | 소음, 에너지 |

---

## 5. 설비 간섭 우선순위 (BIM 협의 기준)

간섭 발생 시 일반적 공간 점유 우선순위:

```
우선순위 높음 (이동 어려움)
    1위: 구조체 (빔, 기둥, 슬래브)
    2위: 제연 덕트 / 소방 배관
    3위: 중력식 배관 (배수, 우수) — 구배가 있어 이동 제약
    4위: 대구경 공조 덕트 (SA/RA 메인)
    5위: 냉수·온수 주배관
    6위: 소구경 배관, 배선
    7위: 가지 배관, 플렉시블 덕트
우선순위 낮음 (이동 용이)
```

---

## 6. MEP BIM 모델링 공종별 체크포인트

### 공조 덕트
- [ ] 계통 지정 (SA/RA/EA/OA) 정확히 설정
- [ ] 덕트 단면적 풍속 계산값 기입
- [ ] 댐퍼 위치에 점검구 공간 확보
- [ ] 제연 덕트 별도 레이어 분리

### 배관
- [ ] 계통 지정 (CHW-S/CHW-R/HW-S 등) 정확히 설정
- [ ] 단열 두께 포함 외경으로 간섭 검토
- [ ] 배수관 구배 적용 여부
- [ ] 밸브·플랜지 유지보수 공간 확보

### 전기
- [ ] 강전/약전 트레이 분리 배치
- [ ] 분전반 전면 작업 공간 확보
- [ ] 전선 인입·인출 방향 확인

### 소방
- [ ] 스프링클러 헤드 살수 반경 검토
- [ ] 방화구획 관통 슬리브·채움재 확인
- [ ] 소방 배관이 다른 배관 하부 배치 여부

---

## 7. 공종 약어 모음

| 약어 | 풀이 | 설명 |
|---|---|---|
| HVAC | Heating, Ventilation, Air Conditioning | 공조 전체 |
| AHU | Air Handling Unit | 에어핸들링유닛 (대규모 공기조화기) |
| FCU | Fan Coil Unit | 팬코일유닛 (소규모 실내 공기조화기) |
| VAV | Variable Air Volume | 변풍량 방식 (에너지 효율) |
| CAV | Constant Air Volume | 정풍량 방식 |
| CHW | Chilled Water | 냉수 |
| HW | Hot Water | 온수 (난방) |
| DHW | Domestic Hot Water | 급탕 (위생 온수) |
| CW | Condenser Water | 냉각수 |
| OA | Outside Air | 외기 |
| SA | Supply Air | 급기 |
| RA | Return Air | 환기(환수) |
| EA | Exhaust Air | 배기 |
| PS | Pressurization (Smoke) | 제연 가압 |
| SE | Smoke Exhaust | 배연 |
| CWS | Cold Water Supply | 급수 |
| HWS | Hot Water Supply | 급탕 공급 |
| HWR | Hot Water Return | 급탕 환수 |
| BAS/BMS | Building Automation/Management System | 건물 자동제어 시스템 |
| DDC | Direct Digital Controller | 디지털 자동제어 장치 |
| MDF | Main Distribution Frame | 주배선반 |
| IDF | Intermediate Distribution Frame | 중간배선반 |
| UPS | Uninterruptible Power Supply | 무정전전원장치 |

---

## 연결

- [[설비 기초 - 덕트 계통과 유체 종류]]
- [[설비 기초 - 배관 계통과 유체 종류]]
- [[지식맵 - BIM 실무 표준]]
- [[Global Knowledge Map]]
