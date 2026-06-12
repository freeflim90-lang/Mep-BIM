# AI 지식 고도화 Iteration 21 업데이트 (2026-06-06)

## 보강 배경
- 목표: 각 AI 담당 에이전트가 전문 도메인 지식을 실제로 활용 가능한지 검증하며 갭 보강
- 방법: QA 테스트로 지식 공백 식별 → 웹 검색 기반 전문 지식 작성 → QA 재검증
- QA 결과: 27/27 → 31/31 (100%) — 새 테스트 케이스 4건 추가, 전원 통과

---

## 보강 파일 1: 구조.md

### 추가 섹션: `## 2026-06-06 구조해석-BIM 연동·IFC 구조 엔티티·철근 BIM 실무 전문 지식`

**핵심 지식 내용:**

#### 구조해석 소프트웨어 ↔ BIM 연동 방식
| 소프트웨어 | 연동 방식 | 유지 정보 |
|-----------|---------|---------|
| ETABS 2026 | CSI XRevit 플러그인 (직접 동기화) | 기둥·보 단면, 레벨, 그리드 |
| MIDAS Gen | IFC 2x3 내보내기 → Revit 가져오기 | 단면 형상, 3D 좌표 |
| Tekla Structures | IFC4x3 / Revit Link 직접 교환 | 접합부 상세, 볼트 정보 |

#### CSI XRevit 2026 워크플로우 (5단계)
1. ETABS 해석 완료 → 부재 단면 확정
2. CSI XRevit 플러그인 → Revit 단면 자동 동기화
3. Revit에서 건축·MEP 통합 → 클래시 검토
4. 간섭 발생 → RFI → 구조기술사 재해석
5. 단면 변경 → XRevit 재동기화 → IFC 내보내기 배포

#### IFC 구조 엔티티 전문 가이드 (IFC4.3)
- `IfcBeam`: 수평 구조 부재 (BEAM/JOIST/HOLLOWCORE)
- `IfcColumn`: 수직 구조 부재 (COLUMN/PILASTER)
- `IfcSlab`: 슬래브 (FLOOR/ROOF/BASESLAB)
- `IfcFooting`: 기초 (PAD_FOOTING/STRIP_FOOTING)
- `IfcPile`: 말뚝 (BORED/DRIVEN/JETGROUTING)
- `IfcReinforcingBar`: 개별 철근 (BarRole: MAIN/SHEAR/LIGATURE)
- `IfcReinforcingMesh`: 용접 철망

#### 철근 BIM LOD 기준
| LOD | 철근 표현 | 구현 방법 |
|-----|---------|---------|
| 300 | 파라미터만 (형상 없음) | Pset_ReinforcementBarPitchOfBars |
| 350 | 이음 위치·스터럽 간격 | Revit Area/Path Reinforcement |
| 400 | 개별 철근 3D 형상 | Revit Rebar 또는 Tekla |

#### IfcReinforcingBar 주의사항
- Revit Rebar → IFC 내보낼 때 기본값이 `IfcBuildingElementProxy`로 매핑됨
- 해결: IFC 내보내기 PropertySetMapping 파일에서 `Rebar → IfcReinforcingBar` 명시 추가

---

## 보강 파일 2: 공조덕트.md

### 추가 섹션: `## 2026-06-06 공조덕트 풍량 산출·방화댐퍼 기준·IFC 덕트 엔티티 전문 지식`

**핵심 지식 내용:**

#### 건물 용도별 환기 기준 풍량 (기계설비법 시행규칙)
| 용도 | 환기횟수 | 1인당 외기량 |
|------|---------|-----------|
| 사무실 | 4회/h | 25 m³/인·h |
| 병원 일반 | 6회/h | 30 m³/인·h |
| 수술실 | 15~25회/h | — |
| 지하 주차장 | 10~15회/h | CO 검지 연동 |
| 회의실 | 6회/h | 36 m³/인·h |

#### 덕트 단면 간이 산출
- `Q = 바닥면적 × 층고 × 환기횟수` (체적 기준)
- `A = (Q / 3600) / v_target` (v_target: 주 덕트 10 m/s)
- 장방형: W×H = A, 종횡비 ≤ 4:1

#### 방화댐퍼 기준 (건축법 §49)
- 방화구획 바닥·벽 관통 덕트 의무 설치
- 퓨즈 온도: 일반 72°C / 주방 배기 120°C
- BIM 파라미터: `FuseTemperature`, `DamperOperation`, `FireRatingClass`

#### IFC 덕트 엔티티 매핑
| Revit 요소 | IFC 엔티티 | PredefinedType |
|-----------|-----------|----------------|
| 직관 덕트 | IfcDuctSegment | STRAIGHTSEGMENT |
| 분기·레듀서 | IfcDuctFitting | JUNCTION/TRANSITION |
| 취출구·흡입구 | IfcAirTerminal | REGISTER/GRILLE/DIFFUSER |
| 방화댐퍼 | IfcDamper | FIREDAMPER |
| 방연댐퍼 | IfcDamper | SMOKEDAMPER |
| AHU | IfcUnitaryEquipment | AIRHANDLER |
| FCU | IfcUnitaryEquipment | FANCOILUNIT |

---

## QA 검증 결과

| 항목 | Before | After |
|------|--------|-------|
| 전체 테스트 수 | 27 | 31 |
| 통과 수 | 27 | 31 |
| 통과율 | 100% | 100% |

새 추가 테스트 케이스:
- ✅ 구조: "ETABS Revit 구조 BIM 연동 CSI XRevit 워크플로우"
- ✅ 구조: "IFC IfcReinforcingBar 철근 BIM LOD 300 400"
- ✅ 공조덕트: "공조 덕트 풍량 산출 환기횟수 사무실 병원"
- ✅ 공조덕트: "방화댐퍼 퓨즈온도 설치기준 BIM 파라미터"

---

## 누적 현황 (Iteration 21 기준)
- QA 커버리지: 31개 도메인 질문 100% 통과
- 지식베이스 대상 파일: knowledge/10_agents/ 내 25+ MD 파일
- 전문 지식 보강 누적: 구조·공조덕트·전기·건축·BIM_납품검수·Revit_Addin·BIM 견적·인력파견 등

## 다음 보강 후보
- `통신.md`: Cat6A/광케이블 배선 상세, MDF/IDF 배치 기준 심화
- `토목.md`: Civil 3D BIM 연동, 도로 토공 물량 산출 방법
- `소방전기.md`: 비상발전기 BIM 파라미터, 자동화재탐지 IFC 매핑

---
tags: [지식고도화, BIM, 구조, 공조덕트, IFC, QA검증, Iteration21]
date: 2026-06-06
