# Dynamo 지식 베이스

## 2026-06-05 Dynamo 2026 최신 자동화 도구 비교 및 AI 코딩 트렌드 심화 보강
- Source: piaxis.ai BIM Automation Tools 2026, studiokrew.com Dynamo vs API 비교, BIM Pure Blog
- Tags: dynamo,python,ai-coding,vibe-coding,mcp,revit-automation,2026

**2026년 Revit BIM 자동화 도구 비교 (AEC 전문가 순위):**
| 도구 | 특징 | 적합 용도 |
|------|------|---------|
| Dynamo | 비주얼 프로그래밍, 진입 장벽 낮음 | 반복 모델링, 파라미터 자동화 |
| pyRevit | Python 기반, 커뮤니티 활발 | 커스텀 도구, 스크립트 공유 |
| C# Revit API | 최고 성능, 상용 Add-in | BIM CC 등 상용 제품 |
| APS (Autodesk Platform Services) | 클라우드 기반, RESTful | 웹 연동·대시보드 |
| AI (ChatGPT+MCP) | 대화형 코드 생성 | 빠른 프로토타입, Dynamo 생성 |

**2026 Vibe Coding (AI 기반 BIM 자동화):**
```
Vibe Coding = AI(ChatGPT/Claude)와 대화하며 Dynamo/Python 코드 생성
2026년 주목받는 이유:
- "LED 조명 설치 자동화해줘" → AI가 Dynamo 스크립트 즉시 생성
- Revit MCP(Model Context Protocol) 연동 → AI가 Revit 직접 조작
- 진입 장벽 획기적 감소 → 비개발자도 BIM 자동화 가능
```

**Dynamo vs Python API 선택 기준:**
```
Dynamo 적합:
- 시각적으로 흐름을 보고 싶을 때
- 비개발자가 유지보수해야 할 때
- 간단한 반복 작업 (좌표 배치, 파라미터 입력)

Python/C# API 적합:
- 복잡한 로직·조건 분기
- 상용 제품(App Store) 개발
- 성능이 중요한 대용량 처리
- LUA BIM LABS BIM CC: C# API (상용 제품)
- LUA BIM LABS 업무 자동화: Python + Dynamo
```

## 2026-06-05 Dynamo AI+MCP 자동화 및 MEP 배치 최신 사례 보강
- Source: 비아이엠팩토리(businesskorea), DL이앤씨 능동형 BIM, AIBIM 연구단, 기계설비신문
- Tags: dynamo,ai-bim,mcp,python,mep-automation,pipe-routing,2026

**AI 즉시 답변 패턴 — "Dynamo로 MEP 배관을 자동으로 그릴 수 있나요?"**
```
Dynamo MEP 자동화 가능 사례:
1. 급수배관 자동 모델링: CAD 평면도 → 파이프 경로·위치 자동 분석 → 3D BIM 자동 생성
   (규칙 기반 알고리즘 + Dynamo Python 스크립트)
2. 장비표 → 파라미터 일괄 입력: Excel 기기 목록 → Dynamo로 Revit 파라미터 자동 입력
3. 층별 배관 자동 복사: 표준 배관 패턴을 다른 층에 Dynamo로 자동 복제
4. 공간(Room) 기반 덕트 배치: IfcSpace 위치 기반 취출구 자동 배치

한계: 복잡한 간섭 회피 경로는 아직 수동 조정 필요
```

**2025~2026 한국 Dynamo 최신 동향:**
- **AI+Dynamo**: 2025년 Dynamo User Group에서 "AI 기반 Dynamo Python 활용" 발표
- **Revit MCP 상용화**: AI가 대화형으로 Dynamo 스크립트 생성 → Revit 모델 직접 조작
- **DL이앤씨 능동형 BIM**: 평면도+계산서 → MEP 설계 자동화 (지하주차장 2025년 4월 완성)
- **AIBIM 연구단**: AI 기반 건축설계 자동화 기술 연구 — 급수배관 Dynamo 자동화 사례

**Dynamo 실무 활용 패턴 (즉시 답변용):**
| 목적 | Dynamo 노드/방법 | 결과 |
|------|----------------|------|
| 파라미터 일괄 입력 | Excel → Element.SetParameterByName | 수백 개 설비 데이터 자동 입력 |
| 층별 공정 색상 코딩 | OverrideGraphicSettings | 4D BIM 공종별 색상 자동 적용 |
| ActivityID 일괄 추출 | Element.GetParameterValueByName | 공정표 WBS 연동 CSV 생성 |
| COBie 데이터 추출 | Schedule.Export → Python 변환 | COBie.xlsx 자동 생성 |
| 패밀리 위치 자동 배치 | FamilyInstance.ByPoint | 기기 좌표 Excel → Revit 자동 배치 |

**Dynamo Python 예시 (MEP 기기 파라미터 대량 입력):**
```python
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

# Excel에서 읽은 데이터로 MEP 기기 파라미터 일괄 입력
elements = IN[0]  # Revit 기기 Element 목록
data = IN[1]      # [[SerialNumber, Manufacturer, Model], ...]

for el, row in zip(elements, data):
    el.LookupParameter("SerialNumber").Set(row[0])
    el.LookupParameter("Manufacturer").Set(row[1])
    el.LookupParameter("ModelNumber").Set(row[2])
OUT = "완료"
```

## Dynamo 기본 답변 원칙 (2026-05-22)
- Source: LUA BIM LABS internal Revit/Dynamo automation baseline
- Tags: dynamo,revit,automation,category-selection,bim
- Links: [[Revit_Addin]], [[설비기초]], [[설비도면해석]]

Dynamo 질문은 “어떤 입력을 받아서 어떤 Revit 요소 목록 또는 모델 변경 결과를 만들 것인가”로 답변한다.

답변 순서:
1. 목적: 요소 수집, 선택, 파라미터 조회, 파라미터 수정, 일람표/엑셀 출력 중 무엇인지 구분한다.
2. 입력: 카테고리, 뷰, 레벨, 패밀리명, 타입명, 파라미터명, 조건값을 확인한다.
3. 출력: Dynamo 리스트만 만들 것인지, Revit UI 선택 상태까지 바꿀 것인지 구분한다.
4. 변경 여부: 단순 조회/선택은 Transaction이 필요 없지만, 파라미터 수정·요소 생성·삭제는 Transaction 또는 Dynamo 자동 트랜잭션이 필요하다.
5. 위험: 링크 모델, 타입 요소, 뷰 전용 요소, 대형 모델 성능, 잘못된 카테고리 선택을 주의한다.

## Dynamo 카테고리 객체 일괄 선택 빠른 답변 (2026-05-22)
- Source: LUA BIM LABS internal Dynamo FAQ
- Tags: dynamo,revit,category,selection,python,filtered-element-collector
- Links: [[Revit_Addin]], [[설비도면해석]]

원하는 카테고리 객체를 일괄 선택하려면 두 단계로 생각한다.

노드 방식:
1. `Categories` 노드에서 카테고리를 선택한다.
2. `All Elements of Category` 노드에 연결한다.
3. 결과는 해당 카테고리의 인스턴스 요소 리스트다.
4. 조건이 필요하면 `Element.GetParameterValueByName`과 `List.FilterByBoolMask`로 필터링한다.

Revit 화면 선택까지 바꾸는 Python 노드 예시:

```python
import clr
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ElementId

clr.AddReference("System")
from System.Collections.Generic import List

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

category_map = {
    "Ducts": BuiltInCategory.OST_DuctCurves,
    "Pipes": BuiltInCategory.OST_PipeCurves,
    "Mechanical Equipment": BuiltInCategory.OST_MechanicalEquipment,
    "Cable Trays": BuiltInCategory.OST_CableTray,
}

names = IN[0] if isinstance(IN[0], list) else [IN[0]]
elements = []
seen = set()

for name in names:
    bic = category_map.get(str(name))
    if bic is None:
        continue
    for element in FilteredElementCollector(doc).OfCategory(bic).WhereElementIsNotElementType():
        if element.Id.IntegerValue not in seen:
            seen.add(element.Id.IntegerValue)
            elements.append(element)

uidoc.Selection.SetElementIds(List[ElementId]([e.Id for e in elements]))
OUT = elements
```

주의:
- `All Elements of Category`는 요소 리스트를 만들지만 Revit UI 선택을 바꾸지는 않는다.
- `uidoc.Selection.SetElementIds()`를 써야 Revit 화면의 선택 상태가 바뀐다.
- 링크 모델 요소는 별도 링크 문서 접근이 필요하다.
- 대형 모델은 현재 뷰, 레벨, 시스템명 등으로 먼저 필터링한다.

## Dynamo 폴더 하위 패밀리 로드 및 배치 빠른 답변 (2026-05-22)
- Source: LUA BIM LABS internal Dynamo FAQ
- Tags: dynamo,revit,family,load-family,place-family,folder,python
- Links: [[Revit_Addin]], [[설비도면해석]]

폴더 하위에 있는 `.rfa` 패밀리를 Dynamo로 배치하려면 “파일 찾기 → 패밀리 로드 → 심볼 활성화 → 좌표 배치” 순서로 구성한다.

노드 방식 개념:
1. `Directory Path`로 패밀리 폴더를 지정한다.
2. `Directory.Contents` 또는 Python으로 하위 폴더까지 `.rfa` 파일을 수집한다.
3. `File Path` 리스트를 만든다.
4. 패밀리 로드는 기본 노드만으로 한계가 있어 Python 노드에서 `doc.LoadFamily()`를 쓰는 편이 안정적이다.
5. 배치 위치는 `Point.ByCoordinates` 또는 Excel 좌표 리스트를 사용한다.
6. Revit 배치는 Python 노드에서 `doc.Create.NewFamilyInstance()`를 사용한다.

Python 노드 입력 예시:
- `IN[0]`: 패밀리 폴더 경로. 예: `C:\BIM\Families`
- `IN[1]`: 배치 좌표 리스트. 예: `[(0,0,0), (3000,0,0)]`
- `IN[2]`: 하위 폴더 포함 여부. `True/False`

Python 노드 핵심 골격:

```python
import clr
import os

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import XYZ, StructuralType

doc = DocumentManager.Instance.CurrentDBDocument

folder = IN[0]
points_raw = IN[1] if isinstance(IN[1], list) else [IN[1]]
points = [XYZ(float(p[0]), float(p[1]), float(p[2])) for p in points_raw]

family_files = [
    os.path.join(root, file)
    for root, dirs, files in os.walk(folder)
    for file in files
    if file.lower().endswith(".rfa")
]

symbols = []
placed = []

TransactionManager.Instance.EnsureInTransaction(doc)

for path in family_files:
    family_ref = clr.Reference[object]()
    if doc.LoadFamily(path, family_ref):
        family = family_ref.Value
        symbol_ids = list(family.GetFamilySymbolIds())
        if symbol_ids:
            symbol = doc.GetElement(symbol_ids[0])
            if not symbol.IsActive:
                symbol.Activate()
                doc.Regenerate()
            symbols.append(symbol)

for index, symbol in enumerate(symbols):
    point = points[index] if index < len(points) else points[-1]
    placed.append(doc.Create.NewFamilyInstance(point, symbol, StructuralType.NonStructural))

TransactionManager.Instance.TransactionTaskDone()

OUT = {"family_files": family_files, "loaded_symbols": symbols, "placed_instances": placed}
```

주의:
- `doc.LoadFamily()`와 `NewFamilyInstance()`는 모델 변경이므로 Transaction이 필요하다.
- 같은 패밀리가 이미 로드되어 있으면 `LoadFamily()`가 실패처럼 보일 수 있어, 실무용 버전에서는 기존 `FamilySymbol` 재검색 처리를 추가한다.
- 배치할 패밀리가 Face Based, Work Plane Based, Host Based이면 단순 XYZ 배치가 안 될 수 있다. 이 경우 호스트, 면, 레벨 또는 작업평면 입력이 필요하다.
- 좌표 단위는 Revit 내부 단위(feet) 문제를 확인해야 한다. Dynamo Point가 mm 기준이면 단위 변환이 필요할 수 있다.
- 대량 배치 전에는 테스트용 폴더와 1~2개 패밀리로 먼저 검증한다.

## 원하는 카테고리 객체 일괄 선택 Dynamo (2026-05-22)
- Source: LUA BIM LABS internal Dynamo FAQ
- Tags: dynamo,revit,category,selection,python,filtered-element-collector
- Links: [[Revit_Addin]], [[설비도면해석]]

질문: “원하는 카테고리의 객체를 일괄 선택하는 Dynamo를 만들고 싶다.”

핵심 답변:
- 요소 목록만 필요하면 노드 방식으로 `Categories` → `All Elements of Category`를 사용한다.
- Revit 화면에서 실제 선택 상태까지 바꾸고 싶으면 Python 노드에서 `uidoc.Selection.SetElementIds()`를 사용한다.
- 여러 카테고리를 동시에 처리하려면 카테고리 리스트를 입력받고, 각 카테고리의 요소 리스트를 합친 뒤 중복 ElementId를 제거한다.

### 1. 노드만 사용하는 기본 방식

가장 단순한 그래프:
1. `Categories` 노드에서 원하는 카테고리를 선택한다. 예: Ducts, Pipes, Mechanical Equipment, Cable Trays.
2. `All Elements of Category` 노드에 연결한다.
3. 결과 리스트가 해당 카테고리의 인스턴스 요소 목록이다.
4. 필요한 경우 `Element.GetParameterValueByName`으로 레벨, 시스템명, 타입명 등을 읽고 `List.FilterByBoolMask`로 조건 필터링한다.

주의:
- 이 방식은 Dynamo 내부에서 요소 리스트를 얻는 것이다.
- Revit UI의 현재 선택 상태가 자동으로 바뀌는 것은 아니다.
- 대형 모델에서 전체 카테고리를 수집하면 느릴 수 있으므로 뷰, 레벨, 시스템명 같은 조건으로 필터링하는 것이 좋다.

### 2. Revit UI 선택까지 반영하는 Python 노드 방식

Python 노드 입력 예시:
- `IN[0]`: 카테고리 이름 문자열 또는 문자열 리스트. 예: `"Ducts"` 또는 `["Ducts", "Pipes"]`
- 선택 결과를 Revit UI에 반영하려면 Dynamo를 Revit 안에서 실행해야 한다.

Python 노드 예시:

```python
import clr
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI.Selection import ObjectType

clr.AddReference("System")
from System.Collections.Generic import List
from Autodesk.Revit.DB import ElementId

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

category_map = {
    "Ducts": BuiltInCategory.OST_DuctCurves,
    "Pipes": BuiltInCategory.OST_PipeCurves,
    "Mechanical Equipment": BuiltInCategory.OST_MechanicalEquipment,
    "Plumbing Fixtures": BuiltInCategory.OST_PlumbingFixtures,
    "Cable Trays": BuiltInCategory.OST_CableTray,
    "Duct Fittings": BuiltInCategory.OST_DuctFitting,
    "Pipe Fittings": BuiltInCategory.OST_PipeFitting,
}

raw = IN[0]
names = raw if isinstance(raw, list) else [raw]

ids = []
elements = []
for name in names:
    bic = category_map.get(str(name))
    if not bic:
        continue
    collector = (
        FilteredElementCollector(doc)
        .OfCategory(bic)
        .WhereElementIsNotElementType()
    )
    for element in collector:
        if element.Id.IntegerValue not in ids:
            ids.append(element.Id.IntegerValue)
            elements.append(element)

selection_ids = List[ElementId]([element.Id for element in elements])
uidoc.Selection.SetElementIds(selection_ids)

OUT = elements
```

설명:
- `FilteredElementCollector(doc).OfCategory(...).WhereElementIsNotElementType()`는 해당 카테고리의 인스턴스 요소만 수집한다.
- `uidoc.Selection.SetElementIds()`는 Revit UI의 선택 상태를 바꾼다.
- 이 작업은 요소를 수정하지 않으므로 보통 Transaction은 필요 없다.
- `OUT = elements`로 Dynamo에서도 선택된 요소 리스트를 계속 활용할 수 있다.

### 3. 현재 뷰 안의 요소만 선택하고 싶을 때

현재 뷰 기준으로 제한하려면 Collector에 view id를 넣는다.

```python
view = doc.ActiveView
collector = (
    FilteredElementCollector(doc, view.Id)
    .OfCategory(bic)
    .WhereElementIsNotElementType()
)
```

이 방식은 현재 뷰에 보이는 요소 중심으로 수집한다. 3D 뷰, 평면 뷰, 필터, 뷰 범위, 숨김 상태에 따라 결과가 달라질 수 있다.

### 4. BIM 실무 주의사항

- 링크 모델 요소는 현재 문서의 `FilteredElementCollector(doc)`로 바로 수집되지 않는다. 링크 모델은 `RevitLinkInstance.GetLinkDocument()`가 필요하다.
- 타입까지 가져오면 실제 배치 객체가 아닌 타입 정의가 섞일 수 있으므로 `WhereElementIsNotElementType()`를 기본으로 사용한다.
- 카테고리 이름은 Revit 언어/버전에 따라 다르게 보일 수 있으므로 Python에서는 `BuiltInCategory` 기준으로 관리하는 것이 안정적이다.
- 전체 모델 수집은 느릴 수 있으므로 대형 프로젝트에서는 현재 뷰, 레벨, 시스템명, Workset 등으로 필터링한다.
- 선택 이후 파라미터를 수정할 경우에는 백업, 대상 검토, Transaction, 실패 처리 기준이 필요하다.

답변 템플릿:
“카테고리 객체 목록만 필요하면 `Categories`와 `All Elements of Category`로 충분합니다. Revit 화면에서 실제 선택까지 바꾸려면 Python 노드에서 `FilteredElementCollector`로 요소를 수집하고 `uidoc.Selection.SetElementIds()`를 호출하면 됩니다. 여러 카테고리는 리스트로 받아 합친 뒤 중복 ElementId를 제거하세요.”


## Dynamo Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: Dynamo, Revit자동화, MEP배관, 스크립트, 물량산출, 2025

Dynamo for Revit 2025(버전 3.1)에서는 Python 3.x 엔진(CPython)으로 완전 전환되어 Python 2.x 스크립트는 재작성이 필요하다. Dynamo Player를 활용하면 비개발자도 사전 제작된 스크립트를 버튼 클릭으로 실행할 수 있어 현장 적용성이 높다.
- MEP 자동화 핵심 스크립트: ① 덕트·배관 자동 라우팅: MEPover 패키지의 Route MEP 노드를 활용하여 시작점-끝점 좌표 입력 시 최적 경로로 배관을 자동 생성. 장애물 회피 알고리즘 포함. ② 공간(Space) 자동 배치: 건축 룸(Room) 데이터를 읽어 MEP 공간을 일괄 생성, 공간별 냉난방 부하 파라미터를 자동 입력. ③ 물량산출 자동화: Element.GetParameterValueByName으로 배관 직경·길이·재질을 추출, Excel로 내보내어 견적 연동.
- 실무 패키지 추천: MEPover(MEP 특화), Clockwork(Revit API 확장), Rhythm(프로젝트 관리), bimorphNodes(형상 처리). 패키지 설치는 Dynamo Package Manager에서 버전 호환성(Revit 버전과 일치 여부) 확인 후 진행한다.
- 스크립트 버전 관리: .dyn 파일을 Git 저장소에서 관리하며, 파일명에 Revit 버전을 명시한다(예: MEP_AutoRoute_RVT2025.dyn). 공용 스크립트는 사내 Dynamo Player 라이브러리에 등록하여 전사 공유한다.
- 성능 최적화: 대형 모델(5,000개 이상 요소)에서는 List.Chop으로 배치 처리하고, Transaction 단위를 최소화하여 실행 시간을 50% 이상 단축한다.
- 관련: [[Revit_Addin]] · [[설비장비]] · [[설비시공조율]]

## Dynamo 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: Dynamo, TransactionGroup, CPython전환, IronPython마이그레이션, 패키지배포, 성능최적화

Element.SetParameterByName을 대량(수천 건)으로 실행할 때 Dynamo의 자동 트랜잭션(Auto-Transaction)에 의존하면 요소 하나마다 별도 트랜잭션이 생성되어 속도가 극도로 저하된다. 해결법: Python 노드에서 `TransactionManager.Instance.EnsureInTransaction(doc)` 하나로 묶어 일괄 처리한 뒤 `TransactionManager.Instance.TransactionTaskDone()` 호출. 5,000개 파라미터 업데이트 기준 자동 트랜잭션 대비 처리 시간이 약 80% 단축된다. 복수 트랜잭션을 하나의 Undo 단위로 묶으려면 Revit API의 `TransactionGroup`을 Python 노드 내부에서 `clr.AddReference("RevitAPI")` 후 직접 인스턴스화한다.

List.Map과 List.ForEach의 성능 차이는 리스트 규모가 커질수록 유의미해진다. List.Map은 결과 리스트를 반환하며 Dynamo 내부 병렬 처리 최적화가 적용된다. List.ForEach는 부작용(Side Effect) 목적(Revit 모델 변경, 파일 저장 등)에 적합하지만 순차 실행이라 느리다. 재귀적 요소 순회가 필요할 때(계층 구조 MEP 시스템 탐색)는 `Element.GetSpatialElementCalculationLocation()`보다 Python 노드에서 `MEPSystem.Elements`로 계통 내 모든 요소를 한 번에 가져오는 방식이 신뢰도가 높다.

사용자 정의 패키지 배포(.dyf → pkg): 커스텀 노드(.dyf)를 Package Manager에 등록하려면 `%AppData%\Dynamo\Dynamo Revit\[버전]\packages\[패키지명]\dyf\` 폴더에 .dyf 파일을 배치하고, `pkg.json`에 `"node_libraries"` 경로를 등록한다. 버전 명시(`"version": "1.0.0"`) 필수. 사내 배포 시 Package Manager 대신 폴더 공유 방식으로 배포하고, 스크립트 파일명에 Revit 버전을 명기(`MEP_AutoTag_RVT2025.dyf`)하여 혼용 방지.

Dynamo 2025(Dynamo 3.x) CPython 3.x 전환 시 기존 IronPython(Python 2.7/3.8) 코드 마이그레이션 핵심: ① `import clr; clr.AddReference("RevitAPI")` 패턴은 CPython에서 `pythonnet` 기반으로 동일하게 작동하지만 일부 .NET 타입 캐스팅 방식이 달라짐. ② `System.Collections.Generic.List[ElementId]` 대신 Python 리스트를 직접 전달 가능한 경우가 늘었지만 RevitAPI 메서드에 따라 명시적 캐스팅이 여전히 필요함. ③ `print()` → Python 3 문법 통일, `unicode` 타입 제거. ④ `xrange` 제거 → `range`로 교체. 마이그레이션 전에 노드별로 Python 버전을 `CPython3`으로 명시적 선택 후 테스트 실행 필수.

- 관련: [[Revit_Addin]] · [[설비장비]] · [[설비시공조율]]


## 2026-06-06 Dynamo 4.0.2 (.NET 10) + AI Assistant Alpha 긴급 보강
- Source: Autodesk AEC Tech Drop (2026.04), architosh.com, archilabs.ai, dynamobim.org 2026
- Tags: dynamo-4,net10,ai-assistant-alpha,mcp,revit2027,performance,2026

**Dynamo 4.0.2 — Revit 2027 탑재 버전 핵심 변경사항:**
- **.NET 10 업그레이드**: Dynamo 런타임이 .NET 10 기반으로 전환 → 복잡한 파라메트릭 워크플로우의 기하학 연산 속도 **대폭 향상**
  - 기존: .NET Framework 4.8 → 신규: .NET 10 (크로스플랫폼 가능)
  - 효과: 대형 MEP 자동화 그래프에서 크래시 감소, 실행 속도 향상
- **Generative Design 템플릿 라이브러리 확장**: 재실자 동선, 구조 트러스 최적화, 공간 레이아웃 등 샘플 연구 템플릿 추가
- 참고: Dynamo 버전은 Revit 릴리즈와 함께 번들, Dynamo 4.x는 Revit 2027 대응

**Autodesk Assistant in Dynamo (Alpha 단계, 2026):**
- Dynamo 내부에 AI 어시스턴트 탑재 (Alpha) → 자연어로 Dynamo 그래프 실행 지시 가능
- 사례: Weir Stone(교량 돌쌓기) 위치 데이터 → AI가 Revit 모델에 자동 배치
- 워크플로우: 자연어 프롬프트 → Dynamo 노드 자동 생성 → Revit 요소 배치·수정
- 현황: Alpha 단계 → 실무 적용 전 안정성 검증 필요
- LUA BIM LABS 기회: MEP 자동 배치 Dynamo 그래프에 AI Assistant 연동 → 자연어 입력으로 덕트·배관 경로 자동 생성 중장기 로드맵

**Revit 2027 MCP 6개 Tool Group (Autodesk Assistant 연동):**
| Tool Group | 기능 | Dynamo 활용 가능성 |
|-----------|------|-----------------|
| Model Queries | 모델 요소 조회·분석 | Dynamo 데이터 추출 대체 |
| Sheet Management | 도면 뷰·시트 생성 | 일람표 자동 생성 보완 |
| Room Management | 공간·실 관리 | 실 번호 자동화 보완 |
| Schedules | 스케줄 생성·편집 | Dynamo 스케줄 노드와 병행 |
| Exports | IFC·DWG 내보내기 | Dynamo IFC Export 보완 |
| Element Operations | 요소 생성·수정·태그 | 핵심 Dynamo 기능과 경쟁 |

**Add-in 개발자 주의사항 (Dynamo 4.x / .NET 10):**
- 기존 .NET Framework 4.8 기반 Dynamo Zero-Touch 노드는 .NET 10 환경에서 재컴파일 필요
- NuGet 패키지 의존성 확인: .NET 10 호환 버전으로 업데이트 필요
- 기존 Dynamo 패키지(MEP Force Layout, MEPover 등) 호환성 검증 필요 (패키지 제작자 업데이트 대기)

관련: [[Revit_Addin]] · [[IFC_OpenBIM]] · [[엑셀자동화]] · [[4D5D_BIM]]

## Dynamo 최신 기능 및 BIM 자동화 팁 (2026-06-26)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-26
- KST04 자동수집: 공식 출처/담당자 검증 전 고객 확정 답변, 납품 기준, 견적 기준으로 사용 금지.
- Tags: dynamo,automation,revit,update

- Autodesk Dynamo 2025에서 BIM 실무자들은 MEP 배관/덕트 자동 배치 기능을 활용하여 설계 과정의 효율성을 높일 수 있습니다.
- 일람표 자동화를 통해 변경사항 반영이 용이해지며, 시간과 노력을 대폭 절약할 수 있습니다. 
- 물량산출 스크립트 예시로는 배관/덕트 길이 측정 및 자동 산출을 포함하여, 설계 변경 시 즉시 재산출이 가능하도록 할 수 있습니다.
- 이러한 기능들은 4차 산업혁명 기술을 활용한 스마트 건설기술의 일환으로, 설계 및 시공 과정의 자동화를 지원합니다.
- 관련: [[간섭검토]] · [[Revit_Addin]] · [[CS_기술지원관]] · [[빌드검증]]

