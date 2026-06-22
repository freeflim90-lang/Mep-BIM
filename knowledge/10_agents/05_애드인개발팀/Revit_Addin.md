# Revit_Addin 지식 베이스

## AI 우선 답변 앵커 — Revit API와 2027 AI 기능
Revit API `FilteredElementCollector` 사용법 질문은 요소 수집(Element collection) 흐름으로 답한다. 결론은 Document 기준 Collector를 만들고, Category/Class/WhereElementIsNotElementType 필터를 적용한 뒤 ElementId 또는 Element 리스트로 후속 처리하는 것이다. Revit 2027 새로운 기능 질문은 MCP, AI Assistant, Forma 연계, Design Automation 엔진 버전, .NET 10 마이그레이션 영향까지 함께 확인한다.

## 2026-06-18 Revit 2025/2026 .NET 10 및 Revit 2027 호환성 감시
- Source: Autodesk APS Design Automation release notes, Autodesk APS blog, Autodesk Revit 2026 update notes
- Tags: revit-2026,revit-2027,dotnet10,addin-compatibility,qa,aps

Autodesk는 Revit 2025/2026의 .NET 10 마이그레이션 preview testing을 공지했고, Design Automation Revit Automation Service는 2026년 4월 Revit 2027 지원을 추가했다. BIM Command Center와 Revit Assistant 계열 Add-in은 기능 추가보다 버전별 빌드/런타임 호환성 표를 먼저 관리해야 한다.

운영 기준:
- Revit 2025/2026 고객 환경은 .NET 런타임 변경으로 기존 Add-in이 깨질 수 있으므로 업데이트 전 smoke test를 필수화한다.
- Revit 2027 대응은 UI 명칭 변경보다 API 참조, TargetFramework, PackageContents, 설치 경로, Design Automation 엔진 분기를 먼저 확인한다.
- Store 제출 문서에는 지원 Revit 버전을 “정적 빌드 기준”이 아니라 “실제 Revit 실행 테스트 완료 기준”으로만 적는다.
- 고객지원 FAQ에는 “Revit 업데이트 직후 버튼이 사라짐 / 로드 실패 / DLL 오류” 대응 절차를 준비한다.

QA 체크리스트 후보:
| 항목 | 확인 방법 | 승격 |
|---|---|---|
| Revit 2025/2026 .NET 10 preview | 테스트 PC에서 Add-in 로드, 버튼 실행, TaskDialog 확인 | Store QA |
| Revit 2027 Design Automation | APS 엔진 버전별 샘플 작업 실행 | 자동화 백엔드 |
| Revit 2026 누적 업데이트 | 최신 업데이트 적용 후 smoke test | 고객지원 |
| Multi-version installer | PackageContents.xml, .addin manifest, DLL 경로 확인 | 배포문서 |

## 2026-06-05 Revit 2026 MEP 신기능 및 API 업데이트 (심화 보강)
- Source: Autodesk Revit 2026 공식 릴리즈노트(2025.04.02), BIM Pure Blog, piaxis.ai
- Tags: revit-2026,mep-features,api,hvac-zone,fabrication,gpu,2026

**Revit 2026 MEP 핵심 신기능 (2025년 4월 릴리즈):**
```
1. HVAC Zone 통합 개선:
   - HVAC Zone + System Zone → 통합 Systems Zone
   - 스케치 또는 공간 기반 구역 정의 가능
   - 확장된 속성·스케줄·색채 채우기 지원
   - BIM CC 개발 기회: 공조 구역 자동 생성 Add-in

2. 전기설비 개선:
   - AWG → 케이블 타입·케이블 크기로 변경
   - 도체 상세 정보 추가 (전압강하 제거)
   - BIM CC 전기 모듈에 반영 필요

3. MEP 제작(Fabrication) 성능:
   - 구성 리로드 시간 70% 개선
   - MEP Content Editor에 커넥터 미리보기 추가

4. GPU 가속 (Tech Preview):
   - 대형 3D 모델에서 4~5배 성능 향상
   - 복잡한 MEP 모델 뷰 탐색 속도 대폭 개선

5. API 강화 (자동화 기반):
   - 파트 타입·배전 시스템 파라미터 태깅/스케줄 가능
   - 메타데이터 접근 확장
   - 이벤트 핸들링 안정성 향상 → 더 안정적인 Add-in
```

**Revit 2026 API 개발 주요 변경사항:**
- `MEP Fabrication` API: 단계별 평면 패턴 편차 수정 → 수동 조정 필요 감소
- Systems Zone 객체 모델: 새 Zone 생성 API 업데이트 필요
- GPU 가속 Tech Preview: 대형 모델 뷰 조작 API 성능 개선
- 태깅 API: Part Type·Distribution System 직접 태깅 가능

**LUA BIM LABS BIM CC 개발 시 Revit 2026 고려사항:**
- Systems Zone 통합: MEP 구역 자동 생성 기능에 신규 API 적용
- 지원 버전: Revit 2023~2026 (PackageContents.xml 업데이트)
- GPU 가속 활용: 대형 모델 MEP 분석 속도 향상 가능

## 2026-06-05 Autodesk App Store 수익화 및 한국 Add-in 생태계 최신 업데이트
- Source: Autodesk App Store, 오토데스크 웨비나 자료, 크몽 Revit API 시장 동향
- Tags: revit-api,autodesk-store,monetization,add-in-ecosystem,korea,2026

**AI 즉시 답변 패턴 — "Autodesk App Store에 Add-in을 올리면 수익이 나나요?"**
```
Autodesk App Store Add-in 수익화:
- 플랫폼: apps.autodesk.com (한국어 지원, 1,424개 Revit 앱)
- 수익 모델: 무료(홍보) / 유료 구독 / 일회성 구매
- Autodesk 수수료: 판매액의 약 30% (개발자 70% 수익)
- 한국 시장: Revit 사용 건설사 4,200개↑ 잠재 고객
- 성공 사례: DiRoots (무료 플러그인으로 인지도 → 프리미엄 전환)
- LUA BIM LABS 전략: 무료 베타 → 유료 구독 전환 (Autodesk Store + 직접 라이선스)
```

**Autodesk App Store 등록 요건:**
| 항목 | 요건 |
|------|------|
| 언어 | .addin 매니페스트 + DLL 어셈블리 |
| Revit 버전 | 2023/2024/2025/2026 멀티 버전 지원 권장 |
| 아이콘 | 32×32px (리본 버튼용), 230×140px (스토어 섬네일) |
| 스크린샷 | 최소 3장, 기능 시연 영상 권장 |
| 가격 정책 | 무료·Trial·월/연 구독·영구 라이선스 중 선택 |
| 심사 기간 | 제출 후 2~4주 (기능 테스트·악성코드 검사) |

**한국 Revit Add-in 개발 생태계 현황 (2026):**
- 한국어 Autodesk 웨비나: "설계 실무자를 위한 Revit Add-in 소개 및 활용팁"
- 국내 개발사: 상상진화(X_BOX), REVITBOX, 하나기연 등 활발히 성장
- 크몽 프리랜서 시장: Revit Add-in 맞춤 개발 서비스 활성화
- 성장 기회: 500억↑ BIM 의무화(2026)로 Revit 사용자 급증 예상

**LUA BIM LABS Add-in 로드맵 우선순위 (2026):**
| 제품명 | 상태 | 핵심 기능 | Autodesk Store 전략 |
|--------|------|---------|------------------|
| BIM Command Center | 개발 중 | 모델 품질·작업셋·MEP | 무료 베타 → 유료 전환 |
| Model Health Dashboard | 후보 | 모델 오류 진단 리포트 | 유료 ($9.9/월) |
| MEP Splitter | 후보 | MEP 간섭 자동 분리 | 유료 ($4.9/월) |
| Clash Point Reporter | 후보 | 간섭 리포트 자동 생성 | 유료 ($6.9/월) |

## BIM Command Center 우선 개발 방향 (2026-05-19 09:37:53)
- Source: `docs/autodesk_store/STORE_LAUNCH_PLAN.md`, `260519 소스 폴더/01_Revit_Addins/Addin Dashboard`
- Tags: revit-api,commercial-product,addin-dashboard

Revit 애드인 개발 AI는 신규 기능보다 Store 제출 안정화를 우선한다. 첫 제품은 `Addin Dashboard`를 상용 셸로 사용하고, Model Health Dashboard, Workset Dashboard, Auto Save/Sync, MEP Splitter, Clash Point 계열, Unit Conversion을 후보 모듈로 본다. Revit 버전 호환성은 코드의 TargetFramework 선언이 아니라 실제 Revit 실행 테스트로만 확정한다. 공식 Revit add-in 등록 규칙에 맞게 `.addin` 매니페스트와 설치 Assembly 경로를 관리한다.

## 작업 경계 (2026-05-19)
- Source: `commercial_addins/BIM_Command_Center_For_Revit/00_product/WORK_BOUNDARY.md`
- Tags: scope,revit-api,validation

Revit API 참조가 필요한 빌드, Revit 실행 테스트, 최종 호환성 검증은 Autodesk Revit이 설치된 소유자 PC에서 수행한다. AI는 Store 문서, QA 양식, 패키징 자동화, 정적 검토, 비 API 의존 스크립트까지만 지원하며 실제 Revit 버전 지원 여부를 단독으로 확정하지 않는다.

## AI 즉시 답변 패턴 — Revit 간섭 확인 실무 (2026-06-13)
- Source: LUA BIM LABS QA simulation reinforcement
- Tags: revit,interference-check,linked-model,beam,pipe,mep,qa

**Q. Revit에서 구조 보 하단에 배관이 겹치는지 어떻게 확인하나요?**
- 같은 모델 안의 구조 보와 배관은 `Collaborate > Interference Check`로 1차 hard clash를 확인한다.
- 링크 구조 모델은 `RevitLinkInstance`와 링크 좌표, 공유 좌표 정합을 먼저 확인한 뒤 간섭 검토를 실행한다.
- 구조 보 하단고, 배관 상단고, 단열 포함 외경, 시공 여유를 같이 비교해야 단순 접촉과 실제 시공 불가를 구분할 수 있다.
- 반복 조율과 보고서는 Revit Interference Check만으로 끝내지 말고 Navisworks Clash Detective, BCF, RFI 흐름으로 넘긴다.
- 답변에는 `link`, `revit`, `interference check` 키워드를 포함하고, 구조 관통은 기둥·전이보 불가, 일반보 조건부 승인으로 분리한다.

## AI 즉시 답변 패턴 — Revit API 링크 모델 요소 가져오기 (2026-06-13)
- Source: LUA BIM LABS Telegram QA review
- Tags: revit-api,linked-model,revitlinkinstance,getlinkdocument,collector,transform

Revit API에서 링크 모델 요소를 가져올 때는 현재 문서의 `RevitLinkInstance`를 먼저 찾고, 그 인스턴스에서 `GetLinkDocument()`로 링크 문서를 얻는다.

빠른 답변:
- `FilteredElementCollector(doc).OfClass(typeof(RevitLinkInstance))`로 링크 인스턴스를 수집한다.
- 각 `RevitLinkInstance`의 `GetLinkDocument()`를 호출한다.
- `GetLinkDocument()`가 null이면 링크가 언로드된 상태이므로 건너뛴다.
- 링크 내부 요소는 `FilteredElementCollector(linkDoc)`로 수집한다.
- 현재 모델 좌표로 위치를 비교하려면 `RevitLinkInstance.GetTransform()`을 적용한다.
- 링크 문서는 읽기 전용 검토 대상으로 보고, 링크 파일 자체를 수정하는 기능은 별도 문서/권한/Transaction 정책을 확인한다.

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

AI 즉시 답변 패턴 — 링크 모델 요소 가져오기:
- 현재 문서에서 `FilteredElementCollector(doc).OfClass(typeof(RevitLinkInstance))`로 링크 인스턴스를 수집한다.
- 각 `RevitLinkInstance`에서 `GetLinkDocument()`를 호출해 링크 문서(Document)를 얻는다.
- 링크 문서가 null이면 언로드된 링크이므로 건너뛴다.
- 링크 내부 요소는 링크 문서에 대해 `FilteredElementCollector(linkDoc)`를 실행해 수집한다.
- 좌표가 필요하면 `RevitLinkInstance.GetTransform()`으로 링크 좌표계를 현재 모델 좌표계로 변환한다.
- 링크 문서는 직접 수정 대상이 아니므로 읽기 전용 검토 흐름으로 다룬다.


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

LUAChat 또는 RevitLUAChat은 외부 AI API를 직접 호출하지 않고 LUA BIM LABS 백엔드 지식 게이트웨이를 호출한다.

권장 흐름:
1. Revit Add-in에서 질문과 선택 요소의 최소 컨텍스트를 수집한다.
2. `/api/revit-assistant/chat`으로 전송한다.
3. 백엔드는 Obsidian/지식 베이스에서 Revit, Dynamo, 설비 BIM 근거를 검색한다.
4. 답변과 근거 문서를 Revit 채팅창에 회신한다.
5. 질문/답변/선택 컨텍스트는 `Revit_Assistant_QA` Obsidian 영역에 저장한다.
6. 사용자가 “아쉬워요” 피드백을 누르면 `knowledge-gap-kst02-review`로 전환해 지식 보강 후보로 남긴다.

보안 원칙:
- 모델 전체 데이터는 전송하지 않는다.
- 기본 컨텍스트는 요소명, 카테고리, ID, 계통명, 레벨, 타입명처럼 답변에 필요한 최소 정보로 제한한다.
- 파일 경로, 고객명, 담당자명, 이메일, 전화번호, 계정/토큰은 저장 전 마스킹한다.
- DeepSeek API는 Revit Assistant 일반 질문에 사용하지 않는다. 팀원/실무 답변은 로컬 지식과 Qwen/로컬 흐름을 우선한다.

답변 범위:
- Revit 사용법, Revit API/Add-in 개발, Dynamo 노드/스크립트 방향, MEP 설비 도면/모델링/간섭/점검 기준.
- 법규, 제조사 수치, 과업별 확정 기준은 일반 답변으로 단정하지 않고 기준서 확인 항목으로 분리한다.


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
FilteredElementCollector 사용법은 Revit API 요소 수집의 기본이며, 카테고리/클래스 필터로 범위를 줄인 뒤 ToElementIds 또는 ToElements를 선택한다.

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


## 2026-06-04 Autodesk 공식 신호 기반 Add-in 업데이트 후보
- Source: `knowledge/40_curation/updates/daily/2026-06-04_LUA_BIM_LABS_OFFICIAL_AUTODESK_SIGNAL_UPDATE.md`
- Tags: revit,addin,autodesk,aps,kst02-review

Autodesk 공식 Revit 2026 What's New와 APS 공식 블로그 기준으로 Add-in 운영 지식을 보강한다. 이 섹션은 확정 개발 지시가 아니라 `kst02-review` 후보이며, Store 문구·QA 매트릭스·보안 기준에 반영하기 전 공식 문서와 테스트 증빙을 다시 확인한다.

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


## 2026-06-06 Revit 2027 핵심 신기능 긴급 보강 (2026-04-07 출시)
- Source: Autodesk 공식 Revit 2027 What's New, goto.archi, interscale.com.au, Autodesk Help 2027
- Tags: revit-2027,ai-assistant,mcp,forma-connected,carbon-parameters,accelerated-graphics,add-in,2026

**Revit 2027 출시일: 2026년 4월 7일 (GA 정식 출시)**

**① Autodesk Assistant in Revit (AI 어시스턴트 Tech Preview):**
- 제품 내 명칭은 Autodesk Assistant지만, 고객 질문의 "AI Assistant"는 같은 Revit AI 어시스턴트 맥락으로 해석한다.
- Revit 내 AI 채팅 패널 탑재 → 자연어로 모델 데이터 질의·분석
- 가능 작업: 뷰·스케줄 생성, 파라미터 편집, 공간 관리, 제품 내 가이드
- 기반 기술: **MCP (Model Context Protocol)** 아키텍처 — Revit 모델을 외부 AI(Claude 등)에 컨텍스트로 제공하는 표준 프로토콜
- 사용 예: "3층 공조기(AHU) 목록을 스케줄로 만들어줘" → Revit AI가 즉시 실행
- LUA BIM LABS 시사점: MCP 기반 Revit API 연동 가능성 → LUA BIM LABS 챗봇이 Revit 모델 직접 읽기 중장기 로드맵 검토

**② Revit → Forma 완전 통합 (Forma Connected Client):**
- Revit 2027이 **첫 번째 Forma Connected Client** 로 지정 (Tech Preview)
- Revit 구독에 포함: Forma Data Management Essentials + Forma Site Design + Forma Building Design + Forma Board
- 워크플로우: 초기 부지 검토(Forma) → 상세 설계(Revit) → CDE(Forma Data Management) 끊김 없이 연결
- 기존 ACC Docs/BIM 360과의 차이: 별도 플랫폼 전환 없이 Revit 내에서 Forma 데이터 직접 접근

**③ 가속 그래픽 (Accelerated Graphics) 정식 지원:**
- Revit 2026 Tech Preview → Revit 2027 프로덕션 기능으로 정식 전환
- 성능 예시: 300프레임 Walkthrough(전체 RVT 링크 로드) — 기존 3분 18초 → **38초** (약 5.2배 빠름)
- Add-in 영향: 가속 그래픽 모드에서 커스텀 뷰 렌더링 API 동작 검증 필요

**④ 탄소 파라미터 (Carbon Parameters in Materials) — EC3 연동:**
- 재료(Material) 편집 창에 **Carbon 탭** 신설 → Physical·Thermal 탭과 동급
- EC3(Embodied Carbon in Construction Calculator) 데이터베이스와 연동 → A1~A3 탄소 발자국 비율 직접 입력
- LUA BIM LABS 기회: EC3 탄소 파라미터 자동 입력 Add-in 개발 가능 → G-SEED·LCA 보고 자동화

**⑤ 기타 주요 개선:**
- **Rule-based Numbering**: 규칙 기반 자동 번호 부여 → 수동 번호 변경 사이클 제거
- **Issues for Revit 통합**: Revit 내에서 이슈 생성·확인·해소 가능 → Forma Data Management와 실시간 동기화

**Revit 2027 Add-in 개발 체크리스트:**
- [ ] Revit 2027 API 변경사항 공식 문서 검토 (Autodesk Revit 2027 Developer Guide)
- [ ] Accelerated Graphics 모드에서 커스텀 렌더링 Add-in 동작 테스트 필수
- [ ] MCP 기반 AI 어시스턴트와 충돌 가능성 검토 (동일 명령 채널 사용 여부)
- [ ] Carbon Parameters EC3 연동 API 활용 가능성 검토 → LCA 자동화 Add-in 개발 후보
- [ ] Forma Connected Client 환경에서 기존 Add-in 호환성 스모크 테스트 수행

관련: [[ACC_BIM360]] · [[IFC_OpenBIM]] · [[BIM_납품검수]] · [[패시브하우스_PHIKO]] · [[4D5D_BIM]]

## 2026-06-06 Revit 2027 SDK .NET 10 마이그레이션·배포 변경사항 긴급 보강
- Source: Autodesk Developer Blog "Revit 2027 SDK: .NET 10 Migration and Key API Changes", Autodesk Help Revit 2027 What's New, Microsoft .NET 10 Breaking Changes
- Tags: revit-2027,dotnet10,sdk-migration,add-in-isolation,deployment,breaking-changes,2026

**⚠️ Revit 2027 핵심 변경: .NET 10으로 전환 (LUA BIM LABS Add-in 필수 확인)**

**.NET 10 마이그레이션 개요:**
- Revit 2027(2026-04-07 출시)은 **.NET 10 런타임**으로 전환 (기존 Revit 2025/2026 = .NET 8)
- 모든 신규 Add-in은 .NET 10 SDK로 빌드해야 함
- 장점: 최신 런타임 성능 개선, 툴링 지원 향상, 장기 지원(LTS) 플랫폼 일관성

**호환성 원칙 (가장 중요):**
| 상황 | 동작 | 대응 |
|------|------|------|
| .NET 8 빌드 Add-in → Revit 2027(.NET 10) | **대부분 작동** (하위 호환) | 즉시 테스트, 문제 시 재빌드 |
| .NET 10 빌드 Add-in → Revit 2025/2026(.NET 8) | **로드/실행 불가** | 버전별 별도 빌드 필요 |
| 3rd party 의존 라이브러리 | .NET 10 미지원 라이브러리 존재 시 실패 | NuGet 의존성 전부 .NET 10 호환 확인 필수 |

**.NET 10 마이그레이션 시 실패 원인:**
1. **어셈블리 로딩 동작 변경**: .NET 8에서 암묵적으로 동작하던 어셈블리 해결 방식 변경
2. **리플렉션(Reflection) 동작 변경**: 동적 코드 생성 또는 private 멤버 접근 방식 차이
3. **직렬화 동작 변경**: `System.Text.Json` 또는 `Newtonsoft.Json` 버전 불일치
4. **Native Interop 변경**: P/Invoke 호출 또는 COM Interop 처리 방식 차이
5. **의존 NuGet 패키지**: 전이적 의존성 포함 전체 패키지가 .NET 10 지원 여부 확인 필요

**배포(Deployment) 변경사항:**
```
[Revit 2026 이하] 전사용자 Add-in 경로:
%ProgramData%\Autodesk\Revit\Addins\2026\

[Revit 2027] 전사용자 Add-in 경로 변경:
%ProgramFiles%\Autodesk\Revit 2027\AddIns\

이유: ProgramData는 비관리자가 쓰기 가능 → 보안 강화
→ 인스톨러(.msi/.exe) 배포 시 경로 업데이트 필수
→ 사용자별(Current User) Add-in 경로: 변경 없음
```

**강화된 Add-in 격리(Enhanced Add-in Isolation):**
- Revit 2027에서 Add-in 간 **명시적 의존성 정의** 가능
- 어셈블리 해결 방식을 Add-in 단위로 제어 → 플러그인 생태계에서 DLL 충돌 방지
- 대규모 플러그인 환경(여러 Add-in 병존)에서 어셈블리 버전 충돌 문제 해소

**LUA BIM LABS BIM CC 마이그레이션 체크리스트 (Revit 2027 지원 추가 시):**
```
[ ] 1. 프로젝트 파일(.csproj) 타겟 프레임워크 업데이트
    <TargetFramework>net10-windows</TargetFramework>  (기존: net8-windows)

[ ] 2. 전체 NuGet 패키지 .NET 10 호환 여부 확인
    dotnet list package --framework net10-windows

[ ] 3. Revit 2027 Add-in 참조 DLL 교체
    RevitAPI.dll, RevitAPIUI.dll → Revit 2027 설치 경로 버전으로 교체

[ ] 4. 배포 경로 업데이트
    설치 스크립트에서 ProgramData → ProgramFiles 경로 분기 처리

[ ] 5. 멀티 버전 빌드 설정
    Revit 2024~2026: net8-windows 빌드
    Revit 2027: net10-windows 빌드
    → GitHub Actions CI에서 멀티 타깃 빌드 자동화

[ ] 6. App Store 심사 제출 전 Revit 2027 + .NET 10 환경에서 스모크 테스트
```

**Dynamo 4.0.2 (.NET 10) 성능 개선:**
- Dynamo 4.0.2도 .NET 10으로 업데이트 → 기하 연산 속도 대폭 향상
- 복잡한 파라메트릭 워크플로우에서 실행 시간 단축 체감 가능

관련: [[ACC_BIM360]] · [[IFC_OpenBIM]] · [[BIM_납품검수]] · [[빌드검증]] · [[스토어심사]] · [[Dynamo]]

## Revit Add-in 최신 동향 및 개발 팁 (2026-06-22)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-22
- KST04 자동수집: 공식 출처/담당자 검증 전 고객 확정 답변, 납품 기준, 견적 기준으로 사용 금지.
- Tags: revit,addin,API,update

- Autodesk Revit 2025 API에서는 `LoadFamilyInstance` 메서드가 추가되어, 더 효율적인 모델링 작업을 가능하게 하였습니다.
- 성능 최적화를 위해 `Transaction` 사용 시 `IsolateChanges` 옵션을 활용하여 변경사항에 집중할 수 있게 되었습니다.
- Autodesk Store 심사 통과를 위한 팁으로는 Add-in의 호환성 확인, 사용자 프라이버시 보호 및 데이터 보안 강화, 명확한 설명서 제공 등을 꼽을 수 있습니다.
- 관련: [[간섭검토]] · [[Dynamo]] · [[Navisworks_Addin]] · [[CS_기술지원관]]
