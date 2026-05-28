# Revit_Addin 지식 베이스

## BIM Command Center 우선 개발 방향 (2026-05-19 09:37:53)
- Source: `docs/autodesk_store/STORE_LAUNCH_PLAN.md`, `260519 소스 폴더/01_Revit_Addins/Addin Dashboard`
- Tags: revit-api,commercial-product,addin-dashboard

Revit 애드인 개발 AI는 신규 기능보다 Store 제출 안정화를 우선한다. 첫 제품은 `Addin Dashboard`를 상용 셸로 사용하고, Model Health Dashboard, Workset Dashboard, Auto Save/Sync, MEP Splitter, Clash Point 계열, Unit Conversion을 후보 모듈로 본다. Revit 버전 호환성은 코드의 TargetFramework 선언이 아니라 실제 Revit 실행 테스트로만 확정한다. 공식 Revit add-in 등록 규칙에 맞게 `.addin` 매니페스트와 설치 Assembly 경로를 관리한다.

## 작업 경계 (2026-05-19)
- Source: `commercial_addins/BIM_Command_Center_For_Revit/00_product/WORK_BOUNDARY.md`
- Tags: scope,revit-api,validation

Revit API 참조가 필요한 빌드, Revit 실행 테스트, 최종 호환성 검증은 Autodesk Revit이 설치된 소유자 PC에서 수행한다. AI는 Store 문서, QA 양식, 패키징 자동화, 정적 검토, 비 API 의존 스크립트까지만 지원하며 실제 Revit 버전 지원 여부를 단독으로 확정하지 않는다.

## 경쟁 제품 기능 내재화 기준 (2026-05-19)
- Source: `commercial_addins/BIM_Command_Center_For_Revit/08_feature_backlog/BIMIZE_FEATURE_INTERNALIZATION.md`
- Tags: commercial-feature,benchmark,implementation-policy

시중 판매 중인 BIMIZE 계열 기능은 공개 설명을 시장 벤치마크로만 사용한다. shipped UI, 명칭, 아이콘, 도움말 문구, 코드, UX 흐름을 복제하지 않고 BIM Command Center 고유 기능명과 공정 중심 워크플로우로 재설계한다. 1차 단순 기능은 Line Cleanup Lite, Smart Selector Lite, Workset Inspector Lite이며 Revit API 구현 전에는 JSON 규칙, 미리보기 결과 구조, QA 기준을 먼저 확정한다.

사용자 제공 BIMlize 리본 스크린샷 기준으로는 Settings Profile Manager, View Template Copier, Type Batch Definer, Tag/Text Aligner, Project Cleanup Lite audit mode, Schedule Excel Export를 우선한다. MEP유틸/MEP유틸2 계열은 첫 상용 패키지에서 제외한 `RevitAddin.MepBim` 방향과 충돌할 수 있으므로 별도 제품 또는 후속 릴리스로 분리한다.

1차 구현은 `Addin Dashboard/CommercialFeatures`에 dry-run 명령으로 추가한다. `SettingsProfileCommand`, `ViewTemplateCopierCommand`, `TypeBatchDefinerCommand`, `TagTextAlignerCommand`, `ProjectCleanupLiteCommand`, `ScheduleExcelExportCommand`는 대시보드에서 실행되지만 모델 변경은 하지 않는다. 사용자는 Revit 설치 PC에서 빌드 후 `PHASE1_DRY_RUN_TEST_CHECKLIST.md`에 따라 메뉴 노출, TaskDialog 출력, 무변경 동작을 검증한다. Revit 없는 환경에서는 `scripts/validate_bim_command_center_static.py`로 JSON, csproj, 명령 등록, 설정 파일 존재 여부를 확인한다.


## Revit API 개발 기준 (2026-05-19 08:53:24)
- Source: LUA BIM LABS curated baseline, Autodesk official docs checked 2026-05-19
- Tags: revit-api,addin,manifest

Revit Add-in은 .addin manifest로 등록하고, 명령형 기능은 IExternalCommand, 세션/리본 초기화 기능은 IExternalApplication 중심으로 설계한다. Revit API는 Revit 프로세스 내부 DLL과 단일 스레드 API 접근 제약을 고려해야 하며, 모델 변경은 Transaction 정책을 명확히 둔다. 공식 출처: Autodesk Revit API Add-in Registration, External Commands, Deployment Options.


## Revit API 핵심 패턴 및 Transaction 처리 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: revit-api,transaction,csharp

모든 모델 변경(요소 생성·수정·삭제)은 Transaction 내에서 실행해야 한다.
Transaction 패턴: using(var tx = new Transaction(doc, "작업명")) { tx.Start(); ... tx.Commit(); }
TransactionGroup: 여러 Transaction을 하나의 Undo 단위로 묶을 때 사용.
SubTransaction: Transaction 내부에서 부분 롤백 가능.
UI 업데이트(ExternalEvent)는 별도 IExternalEventHandler에서 처리하고 Idling 이벤트 남용 금지.


## Revit API 필터링 및 요소 수집 패턴 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: revit-api,filter,collector

FilteredElementCollector로 요소 수집 시 WhereElementIsNotElementType() 필수(타입 제외).
BuiltInCategory 필터: new ElementCategoryFilter(BuiltInCategory.OST_DuctCurves)
빠른 필터(Quick Filter) 먼저 적용 후 느린 필터(Slow Filter) 체이닝해 성능 최적화.
대형 모델(요소 10만↑)에서는 ElementId 배치 처리로 메모리 과부하 방지.
Linked 모델 요소 접근: RevitLinkInstance.GetLinkDocument()로 링크 문서 참조.


## Revit API 예외 처리 및 로깅 기준 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: revit-api,exception,logging

Autodesk.Revit.Exceptions.InvalidOperationException: 잘못된 API 호출 순서(Transaction 외부 변경 시도 등).
Autodesk.Revit.Exceptions.ArgumentNullException: null Document/Element 전달.
try-catch에서 Exception 타입을 구체적으로 잡고 사용자에게 TaskDialog로 안내.
로그 파일은 %AppData%\LUA BIM LABS\logs 에 날짜별 저장, 민감 데이터(모델 경로, 사용자 정보) 제외.


## Revit 리본 UI 구성 기준 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: revit-api,ribbon,ui

RibbonPanel은 IExternalApplication.OnStartup에서 생성, 탭명은 제품명으로 고정.
PushButton: 아이콘 32×32(large), 16×16(small) PNG, 배경 투명.
PulldownButton: 관련 기능 묶음, 최대 8개 이하.
ToolTip에 기능 설명 + 단축키 표기. 비활성 조건(AvailabilityClassName)으로 문서 없을 때 버튼 비활성화.


## LUA BIM LABS Revit Assistant 연동 기준 (2026-05-22)
- Source: LUA BIM LABS internal Revit Add-in architecture decision
- Tags: revit-addin,assistant,knowledge-gateway,obsidian,mep,dynamo
- Links: [[설비기초]], [[설비도면해석]], [[설비시공조율]], [[설비자동제어]]

RevitLOAChat은 외부 AI API를 직접 호출하지 않고 LUA BIM LABS 백엔드 지식 게이트웨이를 호출한다.

권장 흐름:
1. Revit Add-in에서 질문과 선택 요소의 최소 컨텍스트를 수집한다.
2. `/api/revit-assistant/chat`으로 전송한다.
3. 백엔드는 Obsidian/지식 베이스에서 Revit, Dynamo, 설비 BIM 근거를 검색한다.
4. 답변과 근거 문서를 Revit 채팅창에 회신한다.
5. 질문/답변/선택 컨텍스트는 `Revit_Assistant_QA` Obsidian 영역에 저장한다.
6. 사용자가 “아쉬워요” 피드백을 누르면 `knowledge-gap-needs-review`로 전환해 지식 보강 후보로 남긴다.

보안 원칙:
- 모델 전체 데이터는 전송하지 않는다.
- 기본 컨텍스트는 요소명, 카테고리, ID, 계통명, 레벨, 타입명처럼 답변에 필요한 최소 정보로 제한한다.
- 파일 경로, 고객명, 담당자명, 이메일, 전화번호, 계정/토큰은 저장 전 마스킹한다.
- DeepSeek API는 Revit Assistant 일반 질문에 사용하지 않는다. 팀원/실무 답변은 로컬 지식과 Qwen/로컬 흐름을 우선한다.

답변 범위:
- Revit 사용법, Revit API/Add-in 개발, Dynamo 노드/스크립트 방향, MEP 설비 도면/모델링/간섭/점검 기준.
- 법규, 제조사 수치, 과업별 확정 기준은 일반 답변으로 단정하지 않고 기준서 확인 항목으로 분리한다.


## Revit Add-in 최신 동향 및 개발 팁 (2026-05-28)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-28
- Tags: revit,addin,API,update

- Autodesk Revit 2025 API는 .NET 8 기반으로 개발되었으며 C#만 지원합니다.
- Deprecated enum 값이 제거되었습니다.
- 신규 기능으로 확장 가능한 저장 데이터 필터링이 향상되었습니다.
- 성능 최적화를 위해 복잡한 계산 과정을 줄이고 효율적인 메모리 관리를 권장합니다.
- Autodesk Store 심사 통과를 위한 팁으로는 Add-in의 안전성, 사용자 경험, 호환성 등을 철저히 검토하고 테스트하는 것이 중요합니다.
