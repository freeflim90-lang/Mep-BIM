# Navisworks_Addin 지식 베이스

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
