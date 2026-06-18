# Navisworks_Addin 지식 베이스

## 2026-06-05 Navisworks 간섭검토 자동화 및 한국 Add-in 생태계 보강
- Source: info.dec-w.com (Navisworks 강의), KCIM BIMlize, 캐드앤그래픽스, Autodesk Navisworks
- Tags: navisworks,clash-detection,auto-searchset,bim-reporting,korea-addin,2026

**AI 즉시 답변 패턴 — "Navisworks로 간섭검토를 자동화할 수 있나요?"**
```
Navisworks Clash Detective 자동화 방법:
1. Selection Sets 기반 자동 검사: 공종별 Selection Set 미리 구성 →
   Clash Detective에서 Set 간 자동 충돌 검사 (배관 vs 덕트, 구조 vs MEP)
2. 배치 실행(Batch): NWF 파일 기반 자동 간섭 검사 스케줄링 가능
3. 리포트 자동 출력: Excel/HTML 간섭 리포트 자동 생성
4. Add-in 확장: BIMlize for Navisworks — 다량 데이터 통계 그래프 자동 생성
5. API 자동화: Navisworks .NET API로 간섭 항목 분류·필터·보고서 자동 처리
```

**Navisworks 간섭검토 워크플로우 (국내 표준):**
| 단계 | 작업 | 결과물 |
|------|------|--------|
| 1. 모델 통합 | Revit → NWC 내보내기 → NWF 통합 | 통합 Navisworks 모델 |
| 2. Selection Set 구성 | 공종별(구조/MEP/건축) Set 분류 | 간섭 대상 집합 정의 |
| 3. Clash Detective 실행 | 공종 간 자동 충돌 검사 | Hard/Soft Clash 목록 |
| 4. 간섭 분류 | 주요/경미/복제 클래시 분류 | 우선순위 클래시 리스트 |
| 5. BCF 연동 | 클래시 → BCF/RFI 이슈 발행 | 협력사 조율 문서 |
| 6. 리포트 출력 | Excel/PDF 간섭 보고서 | 발주처 납품 문서 |

**한국 Navisworks Add-in 현황 (2025~2026):**
- **BIMlize for Navisworks** (KCIM): 간섭 통계 그래프·데이터 분석·현황 대시보드
- **Auto SearchSet** (LUA BIM LABS 개발 중): Selection Set 자동 생성 도구
- **Data Heatmap** (LUA BIM LABS 후보): 간섭 밀집 구역 열지도 시각화
- 국내 건설사: Revit 내재화와 함께 Navisworks 간섭 워크플로우 자동화 강화

**Navisworks 제품 종류 (선택 기준):**
| 제품 | 용도 | 주요 기능 |
|------|------|---------|
| Navisworks Manage | 설계/시공 팀 | Clash Detective + TimeLiner + Quantification |
| Navisworks Simulate | 시공 시뮬레이션 | TimeLiner + Animator (Clash 편집 불가) |
| Navisworks Freedom | 발주처/열람 | 읽기 전용 뷰어 (무료) |

## Navisworks 제품화 순서 (2026-05-19 09:37:53)
- Source: `docs/autodesk_store/STORE_READINESS_AUDIT.md`, Autodesk Navisworks API overview
- Tags: navisworks,store,searchset

Navisworks 도구는 Revit 통합 제품과 분리해 두 번째 제품군으로 상용화한다. 현재 우선 후보는 `Navisworks Auto SearchSet`이며, `Naviswork Data Heatmap`은 하드코딩 경로와 패키징 준비도가 낮아 후순위다. Navisworks 제품은 지원 Navisworks 버전, 플러그인 매니페스트, 설치 경로, 샘플 NWD/NWC 기준 테스트를 별도 체크리스트로 관리한다.

## 작업 경계 (2026-05-19)
- Source: `commercial_addins/BIM_Command_Center_For_Revit/00_product/WORK_BOUNDARY.md`
- Tags: scope,navisworks-api,validation

Navisworks API 참조가 필요한 빌드, Navisworks 실행 테스트, 최종 호환성 검증은 Autodesk Navisworks가 설치된 소유자 PC에서 수행한다. AI는 상용화 계획, 체크리스트, 문서, 패키징 자동화, 정적 검토까지만 지원한다.


## Navisworks API 개발 기준 (2026-05-19 08:53:24)
- Source: LUA BIM LABS curated baseline, Autodesk official docs checked 2026-05-19
- Tags: navisworks-api,plugin,automation

Navisworks .NET API는 Plug-In, Automation, Controls 사용 방식이 있으며, SDK/API 문서와 샘플은 Navisworks Manage/Simulate 설치 폴더의 api 폴더를 기준으로 확인한다. Clash/coordination 제품은 플러그인 실행, 모델/문서 정보 접근, 보고서 추출 및 외부 대시보드 연계를 분리 설계한다. 공식 출처: Autodesk Platform Services Navisworks API overview.


## Navisworks .NET API 기본 구조 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: navisworks-api,plugin,dotnet

Navisworks 플러그인 3가지 방식: AddInPlugin(메뉴 명령), DockPanePlugin(패널), ImporterPlugin(파일 임포터).
진입점: AddInPluginAttribute로 어셈블리 등록, Execute() 메서드에서 로직 실행.
Document 접근: Autodesk.Navisworks.Api.Application.ActiveDocument
모델 항목 순회: ModelItemCollection → ModelItem → PropertyCategoryCollection.


## Clash Detective API 활용 기준 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: navisworks-api,clash,automation

ClashTest 생성/실행: DocumentClash.TestsData.CreateClash() → ClashTest.Run()
결과 접근: ClashTest.ResultData.ClashResults (ClashResult 컬렉션)
ClashResult 주요 속성: Status(Active/Reviewed/Approved), Distance, Point1/Point2(충돌 좌표).
결과 Excel 내보내기: ClashResult를 순회해 OpenXML 또는 CSV로 직접 작성(Navisworks 내장 보고서보다 커스텀 필드 추가 용이).


## Navisworks SearchSet 자동화 기준 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: navisworks-api,searchset,selection

SearchSet은 조건 기반 자동 선택 세트. SelectionSource → ConditionSource → Condition 계층 구조.
저장: document.SelectionSets.InsertCopy(savedItem) 후 NWF 저장으로 유지.
공종별 자동 SearchSet: 카테고리(Category)와 속성(Property) 조합으로 MEP 계통 자동 분류.
Add-in 실행 시 기존 SearchSet 중복 방지를 위해 이름 기준 중복 검사 후 덮어쓰기 옵션 제공.


## Navisworks Addin Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: Navisworks, API, 간섭검토, 자동화보고서, 애드인개발, 2025

Navisworks Manage 2025 API(COM API + .NET Managed API)는 이전 버전 대비 Clash Detective 자동화와 TimeLiner 연동 기능이 강화되었다. LUA BIM LABS의 Navisworks Add-in은 간섭검토 결과를 자동으로 Excel/PDF 보고서로 변환하고, 클라이언트별 커스텀 템플릿을 적용하는 기능을 핵심으로 한다.
- Clash Detective 자동화 API: `ClashDetective.RunTests()` 메서드로 모든 간섭 테스트를 일괄 실행하고, `ClashResult` 객체에서 간섭 유형(Hard/Soft/Clearance/Duplicates), 위치(XYZ 좌표), 관련 요소(Element ID) 정보를 추출한다. 간섭 결과를 공종별(건축/구조/MEP 조합)로 분류하여 보고서를 자동 생성한다.
- 보고서 자동 생성: EPPlus 라이브러리(Apache 2.0 라이선스)를 활용하여 Excel 보고서를 생성하고, 간섭 위치 스냅샷 이미지를 각 시트에 자동 삽입한다. PDF 출력은 iTextSharp 또는 PdfSharp로 구현한다.
- TimeLiner(4D) 연동: `TimeLiner.Tasks` 컬렉션에서 WBS 작업 항목을 읽어 BIM 요소와 매핑하고, 공정률(Progress%)을 외부 MS Project(.mpp) 또는 Primavera P6(XML) 파일에서 자동 동기화한다.
- Autodesk App Store 등록 요건: Revit/Navisworks 버전 호환성 선언(최소 2022~2025), 코드 서명 인증서(Extended Validation 권장), 30일 트라이얼 버전 제공, 유해 코드 정책 준수 확인.
- 관련: [[Revit_Addin]] · [[설비시공조율]] · [[빌드검증]]

## Navisworks 클래시 검토 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: Navisworks, ClashDetective, 클래시그룹핑, TimeLiner, 성능최적화, COMAPI

Clash Detective 고급 활용에서 가장 중요한 설정은 클래시 그룹핑(Grouping Rules)이다. 같은 MEP 시스템 내부(예: 냉수 공급 배관 vs 냉수 환수 배관) 또는 설계 의도상 겹침이 허용된 요소 간의 클래시는 "Rules" 탭에서 `Same System` 규칙을 추가하여 자동으로 Approved 상태로 분류한다. 허용 공차(Tolerance) 설정 기준: 일반 배관 Hard Clash는 0mm(실물 충돌만), 배관 피팅 주변은 ±25mm Clearance Clash로 설정하여 시공 후 조정 가능 범위를 확보. 덕트 행거와 배관 행거 간 이격은 50mm 이상이면 허용하는 Soft Clash 규칙을 추가한다.

5만 건 이상 클래시 처리 시 성능 최적화: ① 클래시 테스트를 공종 조합별(MEP vs 구조, 기계 vs 전기 등)로 분리하여 개별 실행 — 단일 "All vs All" 테스트는 메모리 부족(OOM) 유발. ② 클래시 결과 저장 시 `NWD` 파일 크기가 폭증하므로 결과 이미지 첨부를 "On Request"로 설정. ③ 결과 Excel 내보내기 시 내장 보고서보다 COM API(`Autodesk.Navisworks.Api.Automation`) 또는 .NET Managed API로 직접 파싱하는 편이 대용량에서 3배 이상 빠름. COM API 사용 예: `Application.OpenFile(path)` → `Document.GetClash().TestsData` 접근.

TimeLiner WBS 자동 매핑 실패 패턴 3가지: ① BIM 요소 속성(Property)과 공정표 Activity Name의 대소문자 불일치 — TimeLiner는 대소문자를 구분하므로 "철골공사"와 "철골 공사"가 다른 항목으로 처리됨. 해결: Dynamo 스크립트로 Revit 파라미터 값과 공정표 명칭을 소문자+공백 제거 기준으로 정규화 후 매핑. ② IFC로 내보낸 모델의 IfcTask GUID가 재익스포트마다 바뀌어 매핑 초기화 — Revit ElementId를 기반으로 한 안정적 ID 체계 필요. ③ Revit 링크 모델(Linked .rvt) 요소는 NWC 변환 시 별도 파일로 분리되어 TimeLiner 매핑 규칙이 적용 안 됨 — 링크 파일도 독립적으로 NWC 변환 후 Append해야 한다.

Navisworks API 선택 가이드 — COM API vs .NET Managed API: COM API(`Autodesk.Navisworks.Automation.dll`)는 외부 프로세스에서 Navisworks를 자동화할 때 사용(배치 처리, CI/CD 파이프라인). .NET Managed API는 플러그인(Add-in) 내부에서 현재 열린 문서에 접근할 때 사용. 클래시 결과 자동화 보고서 생성 권장 방식: COM API로 Navisworks 인스턴스를 띄우고 `.RunAllTests()` 후 결과를 EPPlus Excel 라이브러리로 저장하는 CLI 도구 제작 → Jenkins/GitHub Actions에서 야간 자동 실행.

- 관련: [[Revit_Addin]] · [[설비시공조율]] · [[빌드검증]]


## Navisworks 2027 신기능 및 Clash Detective 재설계 (2026-06-06)
- Source: GRAITEC Navisworks 2027 What's New, datechsolution.com Navisworks 2027 분석, Autodesk Community Navisworks 2026
- Tags: navisworks2027,clash-detective,UI개선,BIM조정,2026-04

**Navisworks 2027 출시 (2026-03-31):**
- "속도를 늦추던 것들을 고쳤다" — 새 기술 도입보다 Clash Detective 전면 재설계·UI 현대화에 집중

**Clash Detective 완전 재설계 — 핵심 변경 사항:**
| 항목 | 이전 (Navisworks 2026 이하) | 신규 (Navisworks 2027) |
|------|--------------------------|----------------------|
| 탭 구조 | Rules, Results, Reports 탭 | 전용 창(Dedicated Windows) + 단일 우측 패널 |
| 클래시 테스트 생성 | 1개씩 생성 | **여러 개 동시 생성** 가능 |
| 테스트 구성 | 플랫 목록만 | **폴더 구조** 지원 (복잡한 프로젝트 관리 향상) |
| 정렬·선택 | 드래그 불가 | Drag-and-drop 재정렬, Ctrl/Shift 멀티 선택 |
| 필터링 | 불명확한 동작 | 명확한 필터링 동작 개선 |
| 아이콘·레이아웃 | 구버전 UI | 새 아이콘·클린 레이아웃 |

**Appearance Profiler 업그레이드:**
- 객체 가시성 제어 정밀도 향상
- 규칙 기반 색상을 UI에서 직접 편집 가능 (이전: 별도 다이얼로그 필요)

**Navisworks 2026 추가 기능 (참고):**
- 클래시 속성 데이터 기반 클래시 그룹핑: Clash Detective 폼 내에 그룹핑 기능 직접 내장

**AI 기능 현황 (2026 기준):**
- Navisworks 2027에는 AI 자동 클래시 분류·해결 제안 기능 **미포함**
- Autodesk의 AI BIM 기능은 Revit AI Assistant(MCP)와 Forma에 집중, Navisworks는 UI/UX 개선 우선

**Navisworks API 활용 팁 (2026 실무):**
- Navisworks Manage API (C# .NET): Clash Test 자동 실행, 클래시 보고서 자동 생성
  ```csharp
  // 클래시 보고서 자동 출력 예시 (C# Navisworks API)
  var clashTests = Application.ActiveDocument.GetClash()
                              .TestsData.Tests;
  foreach (var test in clashTests)
  {
      test.TestType = ClashTestType.Hard;
      test.RunTest();
      // 보고서를 HTML로 자동 출력
      ExportClashReport(test, $"{test.DisplayName}_report.html");
  }
  ```
- API 주의사항: Navisworks 2025/2026 버전에서 일부 커스텀 플러그인 성능 이슈 보고됨 → 2027 업그레이드 후 재검증 권장
- AutoCollide: 간섭 검토 자동화 기능 — 반복적인 클래시 배치 검토 자동 실행

**LUA BIM LABS Navisworks 전략 (2027 기준):**
- Navisworks 2027 Clash Detective 폴더 구조 활용 → 공종별(건축/구조/기계/전기/소방) 클래시 체계 정리
- 클래시 보고서 API 자동화 → 발주처 납품용 클래시 리포트 즉시 생성 서비스
- IFC 4.3 읽기 지원 (2026 현황 확인 필요) → MEP IFC 클래시 검토 품질 검증

- 관련: [[Revit_Addin]] · [[BIM_납품검수]] · [[IFC_OpenBIM]] · [[ACC_BIM360]]

## Navisworks Add-in 최신 동향 및 활용 팁 (2026-06-19)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-19
- Tags: navisworks,addin,clash-detection,update

- Autodesk Navisworks 2025에서는 간섭 검토 자동화 기능을 통해 프로젝트에서의 충돌과 간섭을 미리 파악하여 효율적인 작업 환경을 제공한다.
- 보고서 커스터마이징 기능을 활용하면 사용자가 필요한 정보만 선택적으로 포함시켜 보고서를 생성할 수 있어, 프로젝트 관리의 투명성을 높일 수 있다.
- API 활용 방법을 통해 Navisworks와 다른 소프트웨어 시스템을 연동하여 데이터를 자동으로 가져오거나 전송하는 등의 작업을 수행할 수 있다. 이를 통해 생산성 향상과 프로세스 최적화가 가능하다.
- 관련: [[간섭검토]] · [[Revit_Addin]]

