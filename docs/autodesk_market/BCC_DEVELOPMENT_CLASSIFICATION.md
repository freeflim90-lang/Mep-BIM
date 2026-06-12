---
type: development-classification
product: BIM Command Center
updated: 2026-05-31
---

# BIM Command Center — 개발 분류표

> **범례**
> - 🖥️ Revit Add-in : 별도 Windows 개발 PC 필요 (Revit API)
> - 🔧 Navisworks Add-in : 별도 Windows 개발 PC 필요 (Navisworks API)
> - ✅ Dashboard 독립 : Qwen Coder로 즉시 개발 가능 (Python, 무 Revit)

---

## ✅ Dashboard 독립 개발 항목 (Qwen Coder 즉시 착수)

| 순번 | 기능명 | 모듈 경로 | 우선도 | 비고 |
|---|---|---|---|---|
| 1 | **Settings Profile Manager API** | `backend/bim_command_center/settings_profile_router.py` | P0 | 설정 저장/불러오기 API, 다른 기능의 공통 백본 |
| 2 | **Warning Rule Engine** | `backend/bim_command_center/warning_engine.py` | P1 | 경고 분류 룰셋 + 리포트 생성기 (Revit 데이터는 별도 주입) |
| 3 | **Schedule Excel Export Engine** | `backend/bim_command_center/schedule_export_engine.py` | P1 | 일람표 데이터 → Excel/CSV 포맷터 + 한글 파라미터 매핑 |
| 4 | **Element Renumbering Engine** | `backend/bim_command_center/element_renum_engine.py` | P1 | 번호 룰 엔진 (접두사·순서·충돌 정책) |
| 5 | **Clash Group Engine** | `backend/bim_command_center/clash_group_engine.py` | P1 | 간섭 그룹화 알고리즘 + 한글 리포트 생성기 |
| 6 | **Filter Preset Manager** | `backend/bim_command_center/filter_preset_manager.py` | P2 | 가시성 필터 프리셋 JSON 관리 |
| 7 | **IFC Validator (Korean Standards)** | `backend/bim_command_center/ifc_validator.py` | P2 | 국토부·LH·도로공사 BIM 납품 기준 룰 엔진 |

---

## 🖥️ Revit Add-in 개발 항목 (별도 Windows PC)

| 순번 | 기능명 | Phase | API 수준 | 비고 |
|---|---|---|---|---|
| R-01 | **Tag/Text Aligner** | Phase1 | REVIT_WRITE | 태그·문자 정렬/배분 |
| R-02 | **View Template Copier** | Phase1 | REVIT_WRITE | 뷰 템플릿 복사·충돌 정책 |
| R-03 | **Type Batch Definer** | Phase1 | REVIT_WRITE | JSON 기반 타입 일괄 정의 |
| R-04 | **Schedule Excel Export (Revit 측)** | Phase1 | REVIT_READ | 일람표 데이터 읽기 → Dashboard-3 엔진에 전달 |
| R-05 | **Project Cleanup Lite** | Phase1 | REVIT_READ | 미사용 뷰·CAD Import·경고 감사 |
| R-06 | **Line Cleanup** | Phase1 | REVIT_WRITE | CAD Import 잔재 정리 |
| R-07 | **Smart Selector** | Phase1 | REVIT_READ | 카테고리·파라미터 기반 선택 |
| R-08 | **Workset Inspector** | Phase1 | REVIT_READ | Dashboard의 Workset Dashboard 탭 확장 |
| R-09 | **Batch Print / PDF Export** | Phase2 | REVIT_READ | 시트 일괄 PDF 출력 |
| R-10 | **Sheet / View Duplicator** | Phase2 | REVIT_WRITE | 시트·뷰 복제 |
| R-11 | **Link Health & Reload** | Phase2 | REVIT_WRITE | 링크 상태 리포트 + 일괄 재로드 |
| R-12 | **Standard Transfer Pro** | Phase2 | REVIT_WRITE | 프로젝트 간 설정 전달 |
| R-13 | **Room Finishing Pro** | Phase2 | REVIT_WRITE | 한국 마감 기준 자동 배정 |
| R-14 | **MEP Splitter (강화)** | Phase2 | REVIT_WRITE | 배관·덕트 분기 + 길이 계산 연동 |
| R-15 | **Warning Manager (Revit 측)** | Phase2 | REVIT_READ | 경고 격리·수정 → Dashboard-2 엔진에 전달 |

---

## 🔧 Navisworks Add-in 개발 항목 (별도 Windows PC)

| 순번 | 기능명 | Phase | 비고 |
|---|---|---|---|
| N-01 | **Clash Center — 간섭 책임자 배정** | Phase1 | 개발 큐 1위. 공종별 배정 + 한글 엑셀/PDF 보고서 |
| N-02 | **Clash Grouping** | Phase1 | Dashboard-5 엔진 결과를 Navisworks에서 시각화 |
| N-03 | **Define Clash Tests** | Phase2 | 간섭 테스트 조건 배치 정의 |
| N-04 | **Navisworks → IFC 연동** | Phase2 | Dashboard-7 IFC 검증기와 연동 |
| N-05 | **한글 보고서 출력** | Phase1 | 모든 Navisworks 아이템 공통 출력 레이어 |

---

## 개발 흐름도

```
[Qwen Coder / Dashboard 독립] → backend/bim_command_center/*.py
         ↓
[Revit Add-in / Windows PC]  → Revit API 데이터 수집 → Dashboard API 전송
         ↓
[Navisworks Add-in / Windows PC] → NW API 데이터 수집 → Dashboard API 전송
         ↓
[Dashboard API / server_total.py] → 통합 처리 → 리포트 + 이메일 + Telegram
```

---

_생성일: 2026-05-31 | 시장분석 기반: BIM_COMMAND_CENTER_FEATURE_ROADMAP.md_
