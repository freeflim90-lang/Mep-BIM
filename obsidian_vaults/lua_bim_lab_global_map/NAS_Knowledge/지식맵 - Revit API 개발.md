---
type: knowledge-map
domain: Revit API
date: 2026-05-22
status: active
tags:
  - RevitAPI
  - CSharp
  - AddIn
  - BIM실무
  - 상품화
---

# 지식맵 — Revit API 개발

LUA BIM LABS의 Revit Add-in 개발 전체 지식. BIM Command Center(상용 제품) 기준.

---

## 1. 핵심 원칙

- **1차 구현**: Qwen_Coder_8B가 로컬에서 초안 작성 (순수 C# 도메인 로직 한정)
- **최종 확정**: 소유자 PC(Revit 설치 환경)에서 실기 테스트 후 확정
- **API 의존 판정**: Transaction, Document 변경, ClashResult, ModelItem → 최고지배자 검증 필수
- **제품 목표**: BIM Command Center For Revit (Autodesk Store 상용 출시)

---

## 2. 아키텍처 레이어 구조

```
Presentation  →  WPF ViewModel + View (MVVM)
Application   →  IExternalCommand 구현 클래스
Domain        →  비즈니스 로직 (Revit API 비의존 순수 C#)
Infrastructure → Revit API 호출, 파일 I/O, 외부 서버 통신
```

- 의존성 방향: Presentation → Application → Domain ← Infrastructure
- Domain 레이어: Revit 없이 단위 테스트 가능하도록 설계
- Revit API 참조는 Infrastructure/Application 레이어에만 격리

---

## 3. 핵심 API 패턴

### 3-1. 명령 등록 (.addin 매니페스트)

```xml
<?xml version="1.0" encoding="utf-8"?>
<RevitAddIns>
  <AddIn Type="Command">
    <Assembly>BimCommandCenter.dll</Assembly>
    <ClientId>GUID-HERE</ClientId>
    <FullClassName>BimCommandCenter.Commands.ModelHealthCommand</FullClassName>
    <Text>Model Health Dashboard</Text>
    <VendorId>LUABIMLABS</VendorId>
  </AddIn>
  <AddIn Type="Application">
    <Assembly>BimCommandCenter.dll</Assembly>
    <ClientId>GUID-APP</ClientId>
    <FullClassName>BimCommandCenter.App</FullClassName>
    <Name>BIM Command Center</Name>
    <VendorId>LUABIMLABS</VendorId>
  </AddIn>
</RevitAddIns>
```

### 3-2. Transaction 처리

```csharp
using Autodesk.Revit.DB;

public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
{
    var doc = commandData.Application.ActiveUIDocument.Document;
    using (var tx = new Transaction(doc, "BCC 작업명"))
    {
        tx.Start();
        try
        {
            // 모델 변경 로직
            tx.Commit();
        }
        catch (Exception ex)
        {
            tx.RollbackIfError();
            message = ex.Message;
            return Result.Failed;
        }
    }
    return Result.Succeeded;
}
```

### 3-3. FilteredElementCollector (요소 수집)

```csharp
// 모든 MEP 파이프 수집
var pipes = new FilteredElementCollector(doc)
    .OfClass(typeof(Pipe))
    .WhereElementIsNotElementType()
    .Cast<Pipe>()
    .ToList();

// 레벨로 필터링
var level = new ElementLevelFilter(levelId);
var elemsOnLevel = new FilteredElementCollector(doc)
    .OfCategory(BuiltInCategory.OST_PipeCurves)
    .WherePasses(level)
    .ToElementIds();

// 대형 모델: ElementId만 수집 후 배치 처리 (메모리 최적화)
var ids = new FilteredElementCollector(doc)
    .OfClass(typeof(FamilyInstance))
    .ToElementIds();
```

### 3-4. 파라미터 읽기/쓰기

```csharp
// 내장 파라미터
string mark = elem.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)?.AsString();

// 공유 파라미터
Guid guid = new Guid("파라미터-GUID");
Parameter param = elem.LookupParameter("파라미터명") 
    ?? elem.get_Parameter(guid);

// 파라미터 쓰기 (Transaction 내부)
param?.Set("새 값");
param?.Set(42.0);

// 단위 변환 (Revit 내부 단위: feet)
double mm = UnitUtils.ConvertToInternalUnits(150, UnitTypeId.Millimeters);
double displayMm = UnitUtils.ConvertFromInternalUnits(param.AsDouble(), UnitTypeId.Millimeters);
```

### 3-5. ExternalEvent (비동기 처리)

```csharp
// UI 스레드 블로킹 방지 (대형 모델 처리)
public class BatchProcessEvent : IExternalEventHandler
{
    public void Execute(UIApplication app) { /* Revit API 호출 */ }
    public string GetName() => "BCC Batch Process";
}

var handler = new BatchProcessEvent();
var exEvent = ExternalEvent.Create(handler);

// WPF에서 트리거
exEvent.Raise();
```

---

## 4. BIM Command Center 제품 모듈

| 모듈 | 상태 | 우선순위 |
|---|---|---|
| Model Health Dashboard | 개발 중 | 1 |
| Workset Dashboard | 개발 중 | 2 |
| Auto Save/Sync | 후보 | 3 |
| MEP Splitter | 후보 | 4 |
| Schedule Excel Export | 후보 | 5 |
| Settings Profile Manager | 1차 Dry-Run | 6 |
| View Template Copier | 1차 Dry-Run | 7 |
| Type Batch Definer | 1차 Dry-Run | 8 |

---

## 5. 성능 최적화 기준

- **대형 모델 (10만+ 요소)**: ExternalEvent + IExternalEventHandler로 비동기 처리
- **메모리**: Revit API 객체 사용 후 즉시 참조 해제, IEnumerable 우선
- **시작 시간**: OnStartup에서 무거운 초기화 금지 → Lazy Loading
- **UI**: ProgressBar는 Modeless Dialog로 표시

---

## 6. 작업 경계 (AI 지원 범위)

| 작업 | AI 가능 | 소유자 필수 |
|---|---|---|
| 명령 구조 초안 | O | |
| 순수 C# 도메인 로직 | O | |
| 문서/체크리스트 | O | |
| 정적 검토 (빌드 없이) | O | |
| Transaction/Document 변경 | 초안 | 실기 테스트 |
| ModelItem/ClashResult 접근 | 초안 | 실기 테스트 |
| .addin 매니페스트 | O | 경로 확인 |
| Store 제출 산출물 | 초안 | 최종 확인 |

---

## 7. Autodesk Store 등록 절차

1. Autodesk App Store (apps.autodesk.com) 개발자 계정 등록
2. 제품 패키지: 설치 MSI or APPBUNDLE + 아이콘 + 스크린샷 + 설명문
3. 지원 버전: Revit 2024~2026 (실기 테스트 확인 후 기재)
4. 가격 정책: 구독 모델 권장 (월별/연간)
5. 지역: Korea + Global 동시 출시

---

## 연결

- [[Global Knowledge Map]]
- [[지식맵 - Navisworks 자동화]]
- [[지식맵 - BIM 실무 표준]]
