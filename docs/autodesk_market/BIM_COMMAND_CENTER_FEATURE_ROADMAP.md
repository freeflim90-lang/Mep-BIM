---
type: feature-roadmap
product: BIM Command Center for Revit
source: Autodesk Marketplace 2,895개 앱 분석 (2026-05-31)
status: draft
---

# BIM Command Center — 기능 통합 로드맵

> Autodesk Marketplace 전수 조사(2,895개) 기반. 중복·차별화·신규 통합 기능을 정리한다.

---

## 1. 현재 보유 기능 vs 시장 경쟁 현황

| 기능 | 경쟁앱 수 | 최다리뷰 경쟁자 | FREE 비율 | BCC 차별화 포인트 | 우선도 |
|---|---|---|---|---|---|
| **Schedule Excel Export/Sync** | 113개 | Export/Import Excel (151리뷰·FREE) | 18% | 한글 파라미터 완벽 지원 + 양방향 동기화 | 🔴 즉시 |
| **Batch Print (시트 일괄출력)** | 14개 | PF Printer PDF (15리뷰) | 0% | 한국 도면 표제란 + 한글 파일명 자동화 | 🔴 즉시 |
| **Project Cleanup / Model Health** | 79+21개 | Drawing Purge (285리뷰·FREE) | 21% | 경고 → 정리 → 리포트 원스톱 (단순 Purge 아님) | 🟡 Phase1 |
| **Line Cleanup** | 261개 | Drawing Purge (285리뷰·FREE) | 34% | CAD Import 잔재 특화 + 규칙 JSON 관리 | 🟡 Phase1 |
| **Smart Selector** | 19개 | RQuick Select (41리뷰·$0) | 21% | 저장 룰셋 + 한국어 카테고리명 지원 | 🟡 Phase1 |
| **Tag/Text Aligner** | 2개 | NonicaTab FREE (25리뷰·FREE) | 50% | 경쟁 희박 → 빠른 가시적 가치 | 🟡 Phase1 |
| **View Template Copier** | 21개 | View Filter Manager (13리뷰·$99) | 23% | 프로젝트 간 전달 + 충돌 정책 명확화 | 🟡 Phase1 |
| **Workset Inspector** | 13개 | Worksets Management (12리뷰·FREE) | 15% | 규칙 기반 이상 워크셋 감지 차별화 | 🟡 Phase1 |
| **Link Health & Reload** | 9개 | LinkReloader (1리뷰·$0) | 0% | 경쟁 희박 → 링크 상태 리포트 차별화 | 🟢 Phase2 |
| **Sheet/View Duplicator** | 4개 | View Duplicator (14리뷰·$0) | 25% | 설정 프리셋 연동 차별화 | 🟢 Phase2 |
| **Type Batch Definer** | 28개 | RQuick Select (41리뷰·$0) | 10% | JSON 타입 정의 + Dry-Run 차별화 | 🟢 Phase2 |
| **MEP Splitter** | 1개 | MEP Splitter ($5.99·1리뷰) | 0% | **사실상 독점** — 한국 배관 분기 기준 특화 | 🟡 즉시강화 |
| **Clash Marker** | 63개 | ElectroBIM (58리뷰·$0) | 27% | 간섭 책임자 배정 + 한글 공문 출력 추가 | 🔴 즉시 |
| **Workset Dashboard** | 0개 | 없음 | — | **시장 유일 기능 → 핵심 USP** | 유지 |

---

## 2. 신규 통합 후보 — 마켓 검증된 미보유 기능

### 2-A. 즉시 통합 권장 (Phase 1 확장)

#### ① 경고 관리 (Warning Manager)
- **시장 근거**: Isolate Warnings 18리뷰, Easy Warnings, NonicaTab 포함 13개 앱, 리뷰합계 60
- **통합 위치**: Model Health Dashboard 탭 → "경고 관리" 패널
- **차별화**: 경고 유형별 분류 + 원클릭 요소 격리 + 경고 감소 추이 리포트
- **난이도**: 하 (Revit `Document.GetWarnings()` API)

#### ② 필터/가시성 관리 (Visibility Filter Manager)
- **시장 근거**: FilterMore 45리뷰·$9.99, DiRootsOne 80리뷰 포함 69개, 리뷰합계 292
- **통합 위치**: BIM Command Center 새 "뷰 설정" 탭
- **차별화**: 필터 프리셋 JSON 저장·공유 (Settings Profile Manager 연동)
- **난이도**: 중

#### ③ 요소 번호 재배정 (Element Renumbering)
- **시장 근거**: ElementRenumbering 56리뷰·FREE — 무료이지만 유료화 수요 검증
- **통합 위치**: BIM Command Center "모델 처리" 탭
- **차별화**: 한국 도면 관행 기반 룸·도어·스페이스 번호 규칙 지원
- **난이도**: 하

#### ④ 클래시 그룹화 (Clash Grouping)
- **시장 근거**: Group Clashes 24리뷰·$10, Define Clash Tests 11리뷰·$10
- **통합 위치**: Clash Marker 확장 — Navisworks 연동 탭
- **차별화**: 공종별 자동 그룹 + 책임자 배정 + 한글 보고서 (개발 큐 1위와 동일)
- **난이도**: 중

---

### 2-B. Phase 2 통합 후보

#### ⑤ 마감재 자동 배정 (Room Finishing Pro)
- **시장 근거**: Room Finishing 53리뷰·FREE (BIM 42), 11개 앱, 리뷰합계 134
- **차별화**: 한국 내장공사 기준 마감 코드 매핑 + 견적 연계
- **난이도**: 중

#### ⑥ MEP 길이 계산 (MEP Length Calculator)
- **시장 근거**: TotalLength 50리뷰·FREE, LengthMEP, 29개 앱, 리뷰합계 130
- **통합 위치**: MEP Splitter 탭 확장
- **차별화**: 공종별(배관/덕트/전선관) 분류 + 자재 산출 연계
- **난이도**: 하

#### ⑦ IFC 납품 검증기 (IFC Delivery Validator)
- **시장 근거**: Codemill IFC 25리뷰·$0, 9개 앱, 리뷰합계 46 — 검증 앱은 0개
- **차별화**: 국토부·LH·도로공사 BIM 납품 기준 룰셋 → **글로벌 경쟁자 진입 불가**
- **난이도**: 상
- **수익 모델**: B2B 연간계약 $500~$2,000

#### ⑧ 프로젝트 간 설정 전달 (Standard Transfer Pro)
- **시장 근거**: TransferSingle 37리뷰·$9.99, 기존 Revit Transfer Project Standards의 Pain Point 해결
- **통합 위치**: View Template Copier 확장
- **차별화**: 선택적 전달 + 충돌 미리보기 + 이력 관리
- **난이도**: 중

---

## 3. 중복 정리 — 통합 우선순위

| 현재 별도 기능 | 통합 대상 | 이유 |
|---|---|---|
| Model Health + Project Cleanup | → **Model Health Pro** (단일 탭) | 기능 목적 동일: 모델 품질 진단 |
| Warning Manager (신규) | → Model Health Pro 패널 | 경고는 모델 상태의 일부 |
| Workset Inspector | → Workset Dashboard 패널 | 이미 Workset Dashboard가 존재 |
| Schedule Excel Export + Schedule Excel Sync | → **Data Sync Hub** (단일 모듈) | Export는 Sync의 부분집합 |
| Clash Marker + Clash Grouping | → **Clash Center** (단일 탭) | Navisworks 연동 워크플로우 통합 |
| MEP Splitter + MEP Length Calculator | → **MEP Tools** 탭 | 같은 MEP 작업 흐름 |

---

## 4. 기능 통합 우선순위 매트릭스

```
              높음 ← 수요(리뷰합계) → 낮음
              ┌─────────────────────────────────┐
높음          │ Clash Center  │ Data Sync Hub   │
↑             │ (그룹화+보고) │ (Excel 양방향)  │
난이도        │───────────────│─────────────────│
대비 가치    │ Warning Mgr   │ MEP Length Calc │
              │ Filter Mgr    │ Element Renum.  │
낮음          │ Tag Aligner   │ Level Creator   │
              └─────────────────────────────────┘
```

### 즉시 착수 (난이도 낮음 + 수요 높음)
1. **Warning Manager** → Model Health 통합 (2주)
2. **Element Renumbering** → 모델 처리 탭 (2주)
3. **Tag/Text Aligner** — 이미 스펙 완성, 구현 시작 (1주)
4. **Schedule Excel Export** — Phase 1 목록 1번, 한글 지원 추가 (2주)

### Phase 1 완성 후 (1~2개월)
5. **Clash Center** (Clash Marker + Grouping + 한글 보고서)
6. **Visibility Filter Manager** (Settings Profile 연동)
7. **MEP Tools 탭** (Splitter + Length 통합)

### Phase 2 (3~6개월)
8. **IFC 납품 검증기** — B2B 고가 상품
9. **Room Finishing Pro** — 한국 마감 특화
10. **Standard Transfer Pro** — View Template Copier 확장

---

## 5. 한국 시장 독점 기능 목록 (글로벌 경쟁자 없음)

| 기능 | 마켓 현황 | 수익 잠재력 |
|---|---|---|
| Workset Dashboard | 경쟁앱 0개 | 현재 보유 USP |
| 클래시 한글 보고서 + 책임자 배정 | 경쟁앱 0개 | $15~30/월 구독 |
| IFC 납품 검증 (국토부/LH 기준) | 경쟁앱 0개 | $500~2,000/프로젝트 |
| 한국 소방·위생 MEP 자동 배치 | 경쟁앱 0개 | $50~100/월 |
| 한글 파라미터 엑셀 동기화 | 한국어 지원 앱 9개 (무관련) | $30~50 일회성 |

---

## 6. 제거/보류 권장 기능

| 기능 | 이유 |
|---|---|
| Line Cleanup (단독) | Drawing Purge(285리뷰·FREE)가 장악. Project Cleanup에 통합 후 CAD 특화만 유지 |
| Sheet/View Duplicator (단독) | 시장 수요 낮음(4개·14리뷰). View Template Copier 확장으로 흡수 |
| Link Health (단독) | 9개 앱 모두 리뷰 1개 이하. Model Health 패널에 "링크 상태" 탭으로 축소 |

---

_생성일: 2026-05-31 | 데이터 기준: market_20260531_1504.json_
