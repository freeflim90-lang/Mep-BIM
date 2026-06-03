# Dynamo 지식 베이스

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


## Dynamo 최신 기능 및 BIM 자동화 팁 (2026-05-28)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-28
- Tags: dynamo,automation,revit,update

- Autodesk Dynamo 2025에서는 MEP 배관/덕트 자동 배치 기능을 통해 BIM 실무자가 효율적으로 작업할 수 있습니다.
- 일람표 자동화 기능으로 설계 정보를 빠르게 정리하고 관리할 수 있으며, 이는 시간 절약과 오류 감소에 큰 도움이 됩니다.
- 물량산출 스크립트 예시로는 배관/덕트의 길이와 부재를 자동으로 계산하여 BIM 모델링 과정을 자동화할 수 있습니다.

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


## Dynamo 최신 기능 및 BIM 자동화 팁 (2026-05-29)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-29
- Tags: dynamo,automation,revit,update

- Autodesk Dynamo 2025에서는 MEP 배관/덕트 자동 배치 기능을 통해 BIM 실무자가 효율적인 모델링 작업을 수행할 수 있습니다.
- 일람표 자동화 기능으로, 설계 변경사항에 따른 테이블 업데이트를 자동화하여 시간을 절약할 수 있습니다.
- 물량산출 스크립트 예시로는 배관/덕트 길이 측정 및 자동 산출이 가능합니다. 이를 통해 물량 계산과 관련된 오류를 줄이고 생산성을 높일 수 있습니다.

이러한 기능들은 BIM 프로젝트의 품질 관리와 효율적인 작업을 지원하며, 새로운 버전 업데이트에 따른 적응이 필요할 수 있으므로 주기적으로 스크립트를 확인하고 수정하는 것이 좋습니다.
- 관련: [[Revit_Addin]] · [[CS_기술지원관]] · [[빌드검증]] · [[엑셀자동화]]


## Dynamo 최신 기능 및 BIM 자동화 팁 (2026-05-30)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-30
- Tags: dynamo,automation,revit,update

- Autodesk Dynamo 2025 최신 버전에서는 MEP 배관/덕트 자동 배치 기능을 통해 설계 효율성을 높일 수 있습니다.
- 일람표 자동화 기능으로 데이터 입력 및 수정 작업을 자동화하여 시간과 노력을 절약할 수 있습니다.
- 물량산출 스크립트를 사용하면 자동적으로 필요한 재료와 인건비 등을 계산하고, 이를 바탕으로 정확한 예산을 설정할 수 있습니다.
- 관련: [[Revit_Addin]] · [[CS_기술지원관]] · [[빌드검증]] · [[엑셀자동화]]


## Dynamo 최신 기능 및 BIM 자동화 팁 (2026-05-31)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-31
- Tags: dynamo,automation,revit,update

- Autodesk Dynamo 2025에서는 MEP 배관/덕트 자동 배치 기능을 통해 BIM 실무자가 효율적으로 작업할 수 있습니다.
- 일람표 자동화 스크립트를 활용하여 시간과 노력을 절약할 수 있으며, 물량산출 스크립트도 함께 제공됩니다.
- Dynamo 2025의 새 기능으로는 그리드 배치와 가족 수정 등이 포함되어 있어 BIM 모델링을 더욱 간편하게 만들어줍니다.
- 관련: [[Revit_Addin]] · [[CS_기술지원관]] · [[빌드검증]] · [[엑셀자동화]]


## Dynamo 최신 기능 및 BIM 자동화 팁 (2026-06-01)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-01
- Tags: dynamo,automation,revit,update

- Autodesk Dynamo 2025에서는 MEP 배관/덕트 자동 배치 기능을 통해 BIM 실무자들이 효율적으로 작업할 수 있습니다.
- 일람표 자동화와 물량산출 스크립트를 활용하면 모델링 과정에서의 시간과 노력을 줄일 수 있습니다.
- Dynamo 2025에서는 파일 관리 및 모델 업데이트를 위한 툴들이 강화되어, BIM 프로젝트의 생산성을 높일 수 있습니다.
- 관련: [[Revit_Addin]] · [[CS_기술지원관]] · [[빌드검증]] · [[엑셀자동화]]


## Dynamo 최신 기능 및 BIM 자동화 팁 (2026-06-02)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-02
- Tags: dynamo,automation,revit,update

- Autodesk Dynamo 2025에서는 MEP 배관/덕트 자동 배치 기능을 활용하여 시간과 노력을 줄일 수 있습니다.
- 일람표 자동화를 통해 데이터 입력 및 업데이트 과정을 자동화하여 작업 효율성을 높일 수 있습니다.
- 물량산출 스크립트를 작성하여 BIM 모델에서 필요한 정보를 쉽게 추출하고 분석할 수 있습니다.
- 관련: [[Revit_Addin]] · [[CS_기술지원관]] · [[빌드검증]] · [[엑셀자동화]]


## Dynamo 최신 기능 및 BIM 자동화 팁 (2026-06-03)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-03
- Tags: dynamo,automation,revit,update

- Autodesk Dynamo 2025에서 BIM 실무자들이 활용할 수 있는 자동화 팁과 새 기능 중 하나는 MEP 배관/덕트 자동 배치입니다. 이 기능을 통해 설계자가 배관이나 덕트의 위치와 방향을 빠르고 정확하게 설정할 수 있습니다.
- 일람표 자동화도 중요한 기능으로, Dynamo를 사용하면 Revit 모델에서 자동으로 일람표를 생성하고 업데이트할 수 있습니다. 이는 시간과 노력을 대폭 줄여줍니다.
- 물량산출 스크립트 예시로는 배관 및 덕트의 길이와 부품 수를 자동으로 계산하여 물량을 산출하는 스크립트가 있습니다. 이를 통해 설계 단계에서부터 정확한 공사 계약과 재고 관리를 가능하게 합니다.
- 이러한 새로운 기능들은 BIM 프로세스를 더욱 효율적으로 만들며, 전반적인 작업 속도와 정확성을 향상시킵니다. 하지만 일부 오래된 스크립트는 버전 업데이트로 인해 작동하지 않을 수 있으므로, 새로운 노드와 도구를 배우는 것이 중요합니다.
- 관련: [[Revit_Addin]] · [[CS_기술지원관]] · [[빌드검증]] · [[엑셀자동화]]


## Dynamo 최신 기능 및 BIM 자동화 팁 (2026-06-03)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-03
- Tags: dynamo,automation,revit,update

- Autodesk Dynamo 2025에서는 MEP 배관/덕트 자동 배치 기능을 통해 BIM 실무자가 효율적으로 작업할 수 있습니다.
- 일람표 자동화 기능으로 설계 정보를 쉽게 관리하고 업데이트할 수 있습니다.
- 물량산출 스크립트를 활용하면 시간과 노력을 줄이고 정확도를 높일 수 있습니다. 예시로, 배관/덕트의 길이와 부위를 자동으로 계산하여 물량표를 생성할 수 있습니다.

이러한 새 기능들은 BIM 프로세스에서 자동화를 더욱 강화하며, 설계 및 시공 과정을 효율적으로 지원합니다.
- 관련: [[Revit_Addin]] · [[CS_기술지원관]] · [[빌드검증]] · [[엑셀자동화]]
