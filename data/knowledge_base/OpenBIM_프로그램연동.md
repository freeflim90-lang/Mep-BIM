# OpenBIM 프로그램 연동 지식 베이스

## OpenBIM 프로그램 간 연동 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: openbim,ifc,interoperability,workflow,revit,archicad,tekla,navisworks,solibri

OpenBIM은 IFC 중립 포맷을 중심으로 여러 BIM 소프트웨어가 데이터를 주고받는 워크플로우.
"어떤 소프트웨어를 쓰든 데이터 손실 없이 협업"이 핵심 목표. buildingSMART International 주도.

**주요 프로그램 역할 분류:**
- **모델 작성(Authoring)**: Revit, ArchiCAD, Vectorworks, Tekla Structures, MagiCAD
- **조율·검토(Coordination)**: Navisworks, Solibri, BIMcollab, Trimble Connect
- **시뮬레이션(Analysis)**: EnergyPlus, IDA ICE, OpenFOAM, ETABS, SAP2000
- **FM/운영(Operation)**: Autodesk Tandem, Archibus, IBM TRIRIGA, Maximo
- **시공관리(Construction)**: ACC Build, Procore, Fieldwire

## OpenBIM 프로그램 연동 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: openbim,ifc,interoperability,revit,archicad,tekla,solibri,energyplus,workflow

---

### 1. 설계 단계 — 건축·구조·MEP 공종 간 IFC 연동

**Revit ↔ ArchiCAD (건축-구조 협업):**
- 방식: Revit .rvt → IFC 4 Export → ArchiCAD `File > Interoperability > Merge IFC`
- 주의사항:
  - Revit Wall Join: IFC에서 벽 조인 표현 손실 → ArchiCAD에서 재수동 조정 필요
  - 공유 파라미터: Revit PSet → ArchiCAD IFC Properties 자동 매핑 (이름 일치 필수)
  - 좌표계: 프로젝트 내부원점(Internal Origin) ≠ Survey Point 혼용 시 좌표 틀어짐 발생
- 효율 팁: `IFC Reference` 방식 — ArchiCAD에서 Revit IFC를 참조 링크로 불러와 편집 없이 조율

**Revit ↔ Tekla Structures (구조-설계 협업):**
- 방식: Tekla → IFC 4 철골/RC 모델 → Revit `Insert > Link IFC`
- Tekla IFC Export 권장 설정: Export Type = `IFC Structural Analysis View` or `Coordination View 2.0`
- 데이터 흐름: Revit 건축 모델 → Tekla 구조 해석 → 보강된 구조 IFC → Revit 재링크
- 핵심 파라미터 유지: IfcStructuralAnalysisDomain (보 단면력, 절점 반력) — Revit에서는 읽기 전용

**MagiCAD ↔ Revit (MEP 전문 설계):**
- MagiCAD: Revit 플러그인 형태, Revit 네이티브 환경에서 MEP 자동 라우팅
- IFC Export: MagiCAD 파라미터 → Revit 공유 파라미터 → IFC PSet 자동 승계
- 장점: 핀란드 CADS/MagiCAD DB 활용 (제조사 카탈로그 통합), 자동 물량 산출

---

### 2. 검토 단계 — 간섭 검토 및 품질 검증

**Navisworks (Clash Detection) 연동:**
```
[Revit .rvt] → .nwc (자동) → Navisworks .nwd (통합)
                                    ↓
                           Clash Detective 실행
                                    ↓
                     BCF 2.1 이슈 → ACC Build / BIMcollab
```
- .nwc 자동 생성: Revit Save → 백그라운드 NWC Export (Revit 2025 설정에서 활성화)
- 클래시 결과 → BCF: Navisworks `BCF Manager` 플러그인 → .bcfzip 내보내기

**Solibri Model Checker (품질 검증):**
- IFC 파일 직접 임포트 (Revit/ArchiCAD/Tekla 모두 지원)
- 검증 규칙 예시:
  - 모든 IfcSpace에 `Name` 파라미터 존재 여부
  - 방화구획 경계 IfcFireSuppression 연속성 체크
  - LOD 기준별 필수 파라미터 입력 완결성
- BCF 이슈 → BIMcollab Cloud → 담당자 알림 자동화

---

### 3. 에너지·구조 해석 — IFC → 시뮬레이션 도구

**Revit → EnergyPlus (에너지 시뮬레이션):**
- 방식: Revit `Energy Analysis` → `gbXML` Export → OpenStudio/EnergyPlus
  또는: IFC 4 → `ifcconvert` (오픈소스) → EnergyPlus .idf
- gbXML vs IFC: gbXML이 에너지 해석에 더 직접적 (공간 경계, 창호 U값 포함)
- 활용: LEED/G-SEED 에너지 성능 계산 근거 자료

**IFC → ETABS/SAP2000 (구조 해석):**
- Tekla/Revit → IFC Structural Analysis View → ETABS 구조 해석 임포트
- 실무: IFC 변환 과정에서 보-기둥 접합 조건(Rigid/Pin) 손실 多 → 수동 보정 필요
- 개선 방향: IFC 5.0 IfcStructuralAnalysisModel 표준화로 해결 예상 (2027~)

---

### 4. 효율적 OpenBIM 프로젝트 운영 전략 (LUA BIM LABS 관점)

**추천 워크플로우 (2026 기준):**
```
Revit (건축·MEP) ──┐
Tekla (구조)       ├──> IFC 4.3 → ACC 폴더 → Navisworks 클래시
MagiCAD (MEP)    ──┘                            ↓
                                        Solibri 품질검증
                                            ↓
                                    BCF → ACC Build 이슈
                                            ↓
                                   LOD 500 → FM/Tandem
```

**핵심 성공 요인:**
1. **좌표 통일**: 프로젝트 시작 전 기준점(Survey Point) GRS80 좌표 합의 → IFC 좌표 일치
2. **파라미터 사전 합의**: EIR 기준 공유 파라미터 목록 → 모든 소프트웨어에서 동일 PSet명 사용
3. **IFC 버전 통일**: IFC 4 Coordination View 2.0 (2026 기준 가장 호환성 높음)
4. **BCF 이슈 중앙화**: BIMcollab 또는 ACC Build → 이슈 이력 관리, 책임자 명확화
5. **자동화 파이프라인**: Revit 저장 → NWC 자동 생성 → Navisworks 클래시 자동 실행 → 이메일 보고

**소프트웨어별 IFC Export 품질 비교 (2026):**
| 소프트웨어 | IFC 품질 | 권장 버전 | 주요 주의사항 |
|---|---|---|---|
| Revit 2025 | ★★★★☆ | IFC 4 | 커튼월 매핑 확인 |
| ArchiCAD 27 | ★★★★★ | IFC 4.3 | 가장 IFC 충실도 높음 |
| Tekla 2024 | ★★★★☆ | IFC 4 | 철골 연결부 상세 우수 |
| MagiCAD 2025 | ★★★★☆ | IFC 4 | MEP PSet 완결성 높음 |
| AutoCAD MEP | ★★★☆☆ | IFC 2×3 | 레거시, IFC 4 미흡 |

- 관련: [[IFC_OpenBIM]] · [[BIM_지침서]] · [[Revit_Addin]] · [[Navisworks_Addin]] · [[ACC_BIM360]] · [[BIM_납품검수]]

## IFC 연동 실패 Top 5 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: IFC연동실패, 커튼월매핑, 좌표틀어짐, PSet대소문자, 링크파일, 단위혼동

IFC 기반 프로그램 연동에서 반복적으로 발생하는 실사례 5가지를 원인과 해결 방법으로 정리한다.

**실패 1 — 커튼월 IFC 매핑 오류(IfcWall로 잘못 분류)**: Revit에서 커튼월(Curtain Wall)을 IFC로 내보낼 때 기본 설정이 `IfcCurtainWall`이 아닌 `IfcWall`로 내보내지는 경우가 있다. 원인: IFC Export 설정 파일(.ifcxml)의 카테고리 매핑에서 Curtain Wall → IfcWall로 잘못 지정되거나, Revit IFC Export 설정의 "Curtain Wall" 항목을 수동 Override한 경우. 결과: Navisworks에서 커튼월이 일반 벽으로 분류되어 클래시 그룹핑 규칙이 오작동하고, Solibri에서 IfcCurtainWall 관련 규칙 검증이 누락된다. 해결: IFC Export 설정 파일에서 카테고리 매핑 재확인 — `Walls(Curtain Wall)` → `IfcCurtainWall` 명시적 설정. 내보내기 후 ifcopenshell로 `ifc.by_type("IfcCurtainWall")` 건수 확인.

**실패 2 — 좌표 틀어짐(Internal Origin vs Survey Point 혼용)**: Revit에서 IFC Export 시 좌표 기준으로 "Internal Origin"을 선택하면 Survey Point와의 오프셋만큼 좌표가 틀어진 IFC가 생성된다. 다른 공종이 Survey Point 기준으로 내보내면 통합 모델에서 수십~수백 미터 오프셋이 발생. 해결: IFC Export 설정에서 반드시 "Shared Coordinates" 선택. 모든 공종의 내보내기 설정을 동일하게 유지하기 위해 표준 IFC Export 설정 파일(.ifcxml)을 ACC에 잠금 게시하고 공종별로 동일 파일 사용을 BEP에 명시.

**실패 3 — PSet 이름 대소문자 불일치**: Revit 공유 파라미터 그룹명이 `Pset_ManufacturerTypeInformation`인데 일부 소프트웨어에서 `PSET_ManufacturerTypeInformation` 또는 `pset_manufacturertypeinformation`으로 불일치하게 읽히면서 FM 시스템 연동 시 파라미터가 누락된다. 해결: buildingSMART PSet 표준 이름(대소문자 포함 정확한 철자)을 참조하고, ifcopenshell로 검증 시 `psets = ifcopenshell.util.element.get_psets(element)` 후 키 목록 출력으로 실제 PSet 이름 확인.

**실패 4 — 링크 파일 IFC Export 미포함**: Revit에서 IFC를 내보낼 때 링크된 공종 모델(.rvt)은 기본적으로 포함되지 않는다. 단일 IFC 파일로 전체 모델이 포함된 것으로 착각하여 Navisworks나 Solibri에 가져갔을 때 공종이 누락된 상태로 검토하는 실수가 발생. 해결: IFC Export 시 "Export Links" 옵션을 켜거나, 각 공종 담당자가 자기 모델을 별도 IFC로 내보낸 후 통합. 공종별 IFC 파일을 Navisworks에 Append하는 방식을 표준 워크플로우로 설정.

**실패 5 — 레벨 높이 단위 혼동(mm vs m)**: 일부 소프트웨어(특히 구형 IFC 뷰어, ETABS IFC 임포트)는 IFC 파일의 길이 단위를 mm로 읽어야 하는데 m로 해석하거나 그 반대 경우가 발생하여 건물 층고가 1000배 늘어나거나 0.001배로 축소되는 오류가 생긴다. 해결: IFC 파일 내 `IfcSIUnit` 선언을 ifcopenshell로 확인 — `ifc.by_type("IfcSIUnit")`에서 `.Name == "METRE"` 또는 `.Prefix == "MILLI"` 조합을 점검. Revit IFC Export는 기본적으로 mm(MILLI + METRE)를 사용하므로 수신 소프트웨어의 단위 설정과 맞춰야 한다.

- 관련: [[IFC_OpenBIM]] · [[BIM_지침서]] · [[Revit_Addin]] · [[Navisworks_Addin]] · [[ACC_BIM360]] · [[BIM_납품검수]]
