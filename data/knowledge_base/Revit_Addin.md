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

## Revit Addin Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: RevitAPI, 애드인개발, 2025변경사항, AutodeskStore, MEP자동화

Revit API 2025의 주요 변경사항: ① `Application.NewFamilyDocument()` 메서드 deprecation 및 `Document.NewFamilyDocument()` 대체 적용. ② ElementId가 64비트 정수(Int64)로 변경되어 기존 32비트(Int32) 기반 코드는 수정이 필요하다. ③ ForgeTypeId를 사용한 단위 시스템 처리가 표준화되어 UnitUtils 클래스가 업데이트되었다. ④ Revit 2025부터 .NET 8(LTS) 기반 멀티타겟팅 지원이 시작되었다.
- LUA BIM LABS Add-in 핵심 기능: ① MEP 패밀리 일괄 배치 및 공유 파라미터 자동 입력. ② 공간(Space)·룸(Room) 기반 MEP 부하 자동 계산 및 파라미터 기입. ③ BIM 모델 품질검사 자동화(빈 파라미터, 미연결 요소, 좌표계 오류 검출). ④ IFC 내보내기 전 체크리스트 자동 실행.
- 개발 환경 설정: Visual Studio 2022 + Revit API NuGet 패키지(Autodesk.Revit.SDK), 디버깅 시 RevitLookup(오픈소스) 병행 사용, 단위 테스트는 Moq 프레임워크로 API 호출을 모킹하여 Revit 없이 테스트 가능.
- 배포 및 업데이트: Add-in 설치 파일(.addin 매니페스트 + DLL)을 MSIX 패키지로 배포하고, 자동 업데이트는 GitHub Releases API를 활용한 인앱 업데이트 체크로 구현한다.
- Autodesk Store 심사 통과 팁: 보안 정책(외부 서버 통신 시 HTTPS 필수), 데이터 수집 동의 팝업, 크래시 로그 수집 opt-out 옵션 제공.
- 관련: [[Dynamo]] · [[Navisworks_Addin]] · [[프로그램개발]] · [[빌드검증]]

## R&D 개발지원그룹 Revit Add-in 게이트 (2026-05-28)
- Source: LUA BIM LABS group knowledge update 2026-05-28
- Tags: R&D개발지원그룹,RevitAddin,api-gate,dry-run,product-development

Revit_Addin은 [[R&D_개발지원그룹]]의 Autodesk API 실기 검증 지식이다. 성장전략그룹에서 온 제품 후보가 Revit 모델을 읽거나 변경하는 순간, 개발지원그룹은 공식 API 가능성, Transaction 필요 여부, 성능, 고객 모델 안전성을 먼저 판정한다.

Revit API 게이트 질문:
- 읽기 전용인가, 모델 변경인가.
- Transaction, TransactionGroup, FailureHandlingOptions가 필요한가.
- 링크 모델, Workshared 모델, 빈 문서, 선택 없음 상태에서 안전한가.
- 대형 모델에서 `FilteredElementCollector` 범위를 제한할 수 있는가.
- dry-run 결과와 실제 적용 결과를 분리할 수 있는가.
- Store 심사에서 외부 통신·데이터 수집 고지가 필요한가.

게이트 결과는 `PASS`, `PASS_WITH_REAL_REVIT_TEST`, `HOLD_API_RISK`, `REJECT_UNOFFICIAL_API` 중 하나로 남긴다.

- 관련: [[R&D_개발지원그룹]] · [[프로그램개발]] · [[요구사항분석]] · [[QA_테스터]]

## Revit API 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: RevitAPI, ExternalEvent, IUpdater, FailureHandling, 성능최적화, BreakingChange

ExternalEvent + IExternalEventHandler 패턴은 모달리스(Modeless) WPF 다이얼로그에서 Revit API를 호출할 유일한 안전한 방법이다. 다이얼로그가 열린 상태에서 버튼 클릭 시 직접 API를 호출하면 `InvalidOperationException`(Revit API 외부 호출)이 발생한다. 올바른 패턴: `ExternalEvent.Create(handler)` → `externalEvent.Raise()` → Revit이 다음 Idling 시점에 `IExternalEventHandler.Execute(UIApplication app)`를 UI 스레드에서 호출. 멀티스레딩 시도(Task, Thread 내부에서 Revit API 호출)는 절대 금지 — Revit API는 단일 UI 스레드 전용이다.

UpdaterRegistry(IUpdater 인터페이스)는 모델 변경을 실시간 감지하는 트리거다. `UpdaterRegistry.RegisterUpdater(updater)` 후 `AddTrigger(updaterId, filter, Element.GetChangeTypeAny())`를 등록하면 해당 카테고리 요소가 수정될 때마다 `Execute(UpdaterData)`가 호출된다. 실무 활용: 덕트 연결 해제 감지 후 자동 알림, 파라미터 변경 즉시 연계 파라미터 동기화. 주의: Updater는 프로젝트 열릴 때마다 재등록이 필요하며 `IExternalApplication.OnStartup`에서 등록한다.

FailureHandlingOptions를 활용하면 Revit 경고 다이얼로그를 코드로 일괄 처리할 수 있다. `Transaction.GetFailureHandlingOptions().SetFailuresPreprocessor(preprocessor)`에서 `IFailuresPreprocessor.PreprocessFailures(FailuresAccessor)`를 구현하여 `failuresAccessor.DeleteWarning(failure)`로 경고를 무시하거나 `ResolveFailures`로 자동 해소한다. 납품 전 일괄 정리 Add-in에서 수백 개 경고를 1초 내 처리한 실적이 있다.

대용량 모델(300MB+) 성능 최적화 핵심 3가지: ① FilteredElementCollector 체인 시 ElementCategoryFilter(빠른 필터)를 먼저 적용하고 ElementParameterFilter(느린 필터)를 뒤에 체이닝한다 — 순서 반대 시 전체 요소 순회 후 필터링으로 3~10배 느려짐. ② `collector.ToElementIds()`가 `collector.ToElements()`보다 메모리 사용량이 훨씬 적다 — ID 목록만 필요할 때는 반드시 ToElementIds 사용. ③ 링크 모델 요소 접근 시 `RevitLinkInstance`마다 `GetLinkDocument()` 후 별도 Collector 실행.

Revit 버전별 Breaking Change 대응: Revit 2025에서 ElementId가 Int32 → Int64로 변경됨(필수 대응). `element.Id.IntegerValue` → `element.Id.Value` 사용. 구버전 코드에 `.IntegerValue`가 남아있으면 2025에서 컴파일 경고 후 향후 버전에서 오류로 전환될 예정. Unit API: `UnitUtils.ConvertToInternalUnits(value, UnitTypeId.Millimeters)` 패턴(2022+)으로 `DisplayUnitType` 기반 구 API를 교체. 멀티버전 대응 시 `#if REVIT2025` 전처리기 지시문으로 분기하고 각 버전별 CI 빌드를 구성한다.

- 관련: [[Dynamo]] · [[Navisworks_Addin]] · [[프로그램개발]] · [[빌드검증]]


## Revit Add-in 최신 동향 및 개발 팁 (2026-05-29)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-29
- Tags: revit,addin,API,update

- Autodesk Revit 2025 API는 .NET 8 기반으로 개발되었으며, Add-in을 새로 만들거나 수정할 때 이에 맞게 다시 빌드해야 합니다.
- 새 API 메서드 중 일부는 C# Enum 지원이 제한되었습니다. 이를 활용하여 더 유연하고 확장 가능한 솔루션을 설계할 수 있습니다.
- Revit 2025의 성능 최적화를 위해, 불필요한 데이터 로딩과 반복적인 계산을 줄이는 것이 중요합니다.
- Autodesk Store에 올리는 Add-in은 신중하게 테스트하고, 사용자 친화성과 안정성을 고려해야 합니다. 특히, 확장성과 보안 검토를 통과하기 위해 API와 UI의 일관성 확인이 필요합니다.
- 관련: [[Dynamo]] · [[Navisworks_Addin]] · [[CS_기술지원관]] · [[빌드검증]]


## Revit Add-in 최신 동향 및 개발 팁 (2026-05-30)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-30
- Tags: revit,addin,API,update

- Autodesk Revit 2025 API는 .NET 8 기반으로 개발되어 있어 Add-in을重建时，请确保按照正确的步骤进行操作。首先，确认您的开发环境已经更新至.NET 8版本。然后，根据官方文档重新构建Add-in项目。

- 新API方法包括改进的可扩展存储数据过滤功能，利用这些新特性可以更灵活地处理和筛选设计数据。

- 性能优化方面，建议在使用大量数据时采用分页加载策略，以减少内存占用并提高响应速度。同时，合理利用缓存机制来减少重复计算。

- 为了顺利通过Autodesk Store的审核，请确保您的Add-in符合所有提交要求。特别注意文档准备、功能描述以及用户界面设计需满足专业标准。
- 관련: [[Dynamo]] · [[Navisworks_Addin]] · [[CS_기술지원관]] · [[빌드검증]]


## Revit Add-in 최신 동향 및 개발 팁 (2026-05-31)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-31
- Tags: revit,addin,API,update

- Autodesk Revit 2025 API는 .NET 8 기반으로 업그레이드되어 C# 외 다른 언어 지원이 중단되었습니다.
- 새 API 메서드로 성능 최적화가 이루어졌으며, Dynamo의 업데이트와 함께 Revit Home 기능도 추가되었습니다.
- Add-in 개발 시 Autodesk Store 심사 통과를 위한 팁으로는 사용자 경험을 향상시키는 UI/UX 설계와 보안 및 데이터 프라이버시 관련 요구사항 준수를 꼽을 수 있습니다.
- 관련: [[Dynamo]] · [[Navisworks_Addin]] · [[CS_기술지원관]] · [[빌드검증]]


## Revit Add-in 최신 동향 및 개발 팁 (2026-06-01)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-01
- Tags: revit,addin,API,update

- Autodesk Revit 2025 API는 .NET 8 기반으로 업그레이드되어 C# 외의 언어 지원이 제한됨.
- 새롭게 추가된 API 메서드와 성능 최적화를 통해 개발 효율성 향상 가능.
- Add-in 개발 시 Autodesk Store 심사 통과를 위해 사용자 경험을 고려하고, 안전성과 보안성을 철저히 검토해야 함.
- 관련: [[Dynamo]] · [[Navisworks_Addin]] · [[CS_기술지원관]] · [[빌드검증]]


## Revit Add-in 최신 동향 및 개발 팁 (2026-06-02)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-02
- Tags: revit,addin,API,update

- Autodesk Revit 2025 API는 .NET 8 기반으로 업그레이드되어 .NET 4.8 지원이 중단되었습니다.
- Deprecated enum values는 더 이상 지원되지 않으며, Dynamo에서는 성능 모니터링과 새로운 노드가 추가되었습니다.
- 새 API 메서드를 개발할 때는 Autodesk Store 심사 기준을 준수하여 사용자 친화적인 Add-in을 만들어야 합니다. 특히 보안性和性能优化是关键。
- 在开发Add-in时，确保遵循Autodesk Store的审核标准，以通过其审查并获得批准。这包括但不限于提供清晰的功能描述、用户界面友好性以及数据安全措施。
- 开发过程中注意新API方法的应用，并进行充分的测试以确保兼容性和稳定性。
- 관련: [[Dynamo]] · [[Navisworks_Addin]] · [[CS_기술지원관]] · [[빌드검증]]


## Revit Add-in 최신 동향 및 개발 팁 (2026-06-03)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-03
- Tags: revit,addin,API,update

- Autodesk Revit 2025 API는 .NET 8 기반으로 개발되어 Add-in 개발 시 이 프레임워크를 사용해야 한다.
- 새로운 API 메서드 중 일부는 C#에서만 Enum 지원을 제공한다.
- 성능 최적화를 위해 복잡한 계산이나 대량 데이터 처리 작업은 별도 스레드로 분리하여 실행하는 것이 좋다.
- Add-in 개발 시 Autodesk Store 심사 통과를 위한 팁으로는 사용자 경험(UX)을 고려한 인터페이스 설계와 보안 강화, 오류 관리 및 로그 기록이 필수적이다.
- 관련: [[Dynamo]] · [[Navisworks_Addin]] · [[CS_기술지원관]] · [[빌드검증]]


## Revit Add-in 최신 동향 및 개발 팁 (2026-06-03)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-03
- Tags: revit,addin,API,update

- Autodesk Revit 2025 API는 .NET 8 기반으로 개발되었으며, Add-in은 이 프레임워크에서 다시 빌드해야 합니다.
- 새로운 Enum 지원은 C#에만 제한됩니다.
- 최신 문서와 SDK가 업데이트된 기능을 위한 자료로 제공되고 있습니다.
- 성능 최적화를 위해 코드 리뷰 시 주의해야 할 사항들을 확인하고, 필요한 부분에서 효율적인 알고리즘을 적용하세요.
- Autodesk Store 심사 통과를 위해서는 Add-in이 사용자 프라이버시와 보안에 위배되지 않는지 철저히 검토해야 합니다.
- 관련: [[Dynamo]] · [[Navisworks_Addin]] · [[CS_기술지원관]] · [[빌드검증]]


## Revit Add-in 최신 동향 및 개발 팁 (2026-06-04)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-04
- Tags: revit,addin,API,update

- Autodesk Revit 2025 API는 .NET 8 기반으로 개발되어 성능이 향상되었습니다.
- 새 API 메서드로 프로젝트 관리와 자동화 작업에 도움을 줍니다.
- 새로운 네임스페이스를 통해 기능이 확장되었으며, 이를 통해 더 많은 기능을 활용할 수 있습니다.
- 성능 최적화를 위해 코드 효율성을 높이는 것이 중요합니다. 불필요한 계산이나 반복 작업을 줄여야 합니다.
- Autodesk Store에 Add-in을 등록하려면 철저한 문서 작성과 안전성 검토가 필요합니다. 사용자 가이드와 보안 점검을 포함시켜야 합니다.
- 심사 통과를 위해 API의 기능과 성능, 호환성을 확인하고, 사용자 경험을 최적화하는 것이 중요합니다.
- 관련: [[Dynamo]] · [[Navisworks_Addin]] · [[CS_기술지원관]] · [[빌드검증]]


## 2026-06-04 Autodesk 공식 신호 기반 Add-in 업데이트 후보
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_OFFICIAL_AUTODESK_SIGNAL_UPDATE.md`
- Tags: revit,addin,autodesk,aps,needs-review

Autodesk 공식 Revit 2026 What's New와 APS 공식 블로그 기준으로 Add-in 운영 지식을 보강한다. 이 섹션은 확정 개발 지시가 아니라 `needs-review` 후보이며, Store 문구·QA 매트릭스·보안 기준에 반영하기 전 공식 문서와 테스트 증빙을 다시 확인한다.

운영 판단:
- Revit 2026 Add-in 지원 주장은 Revit 2026.4 계열 스모크 테스트와 릴리스 기준 확인 후에만 사용한다.
- APS AEC Data Model API와 Data Exchanges는 Model Quality Auditor, BIM Command Center, 납품 검수 자동화의 클라우드 데이터 PoC 후보로 둔다.
- APS Secure Service Accounts는 ACC/BIM360 자동화의 3LO 토큰·계정 보안 기준 후보로 검토한다.
- APS 과금·비즈니스 모델 변화는 제품 기능 확정 전 비용·라이선스 영향 검토가 필요하다.

다음 액션:
- `docs/autodesk_store/QA_SMOKE_TEST_PLAN.md`에 Revit 2026 테스트 증빙 연결 여부 확인
- `ACC_BIM360`, `라이선스_보안관`, `제품패키징`과 APS 연동 비용·보안 검토 연결
- 다음 확인일: 2026-06-11

관련: [[ACC BIM360 CDE 지식 베이스]] · [[라이선스_보안관]] · [[지식업데이트]] · [[2026-06-04 LUA BIM LABS Official Autodesk Signal Update]]


## Revit Add-in 최신 동향 및 개발 팁 (2026-06-05)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-05
- Tags: revit,addin,API,update

- Autodesk Revit 2025 API는 .NET 8 기반으로 개발되어 Add-in을 C#으로 재구성해야 합니다.
- 새로운 API 메서드와 성능 최적화 기능이 추가되었습니다, 특히 카본 분석과 MEP/구조 분석에 대한 새 기능들이 포함됩니다.
- Autodesk Store 심사 통과를 위한 팁: Add-in의 호환성을 확인하고, 사용자 경험을 향상시키는 기능들을 강화하세요.
- 관련: [[Dynamo]] · [[Navisworks_Addin]] · [[CS_기술지원관]] · [[빌드검증]]
