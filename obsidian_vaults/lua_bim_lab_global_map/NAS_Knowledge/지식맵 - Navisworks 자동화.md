---
type: knowledge-map
domain: Navisworks
date: 2026-05-22
status: active
tags:
  - Navisworks
  - ClashDetective
  - API
  - BIM실무
  - 상품화
---

# 지식맵 — Navisworks 자동화

LUA BIM LABS의 Navisworks 플러그인 개발 및 간섭 자동화 전체 지식.

---

## 1. 핵심 원칙

- **작업 경계**: Navisworks API 빌드/실행 테스트 → 소유자 PC에서만 수행
- **AI 역할**: 상용화 계획, 체크리스트, 문서, 패키징 자동화, 정적 검토까지만 지원
- **1차 제품**: Navisworks Auto SearchSet
- **2차 후보**: Navisworks Data Heatmap

---

## 2. 플러그인 유형

| 유형 | 특징 | 용도 |
|---|---|---|
| AddInPlugin | 메뉴 명령 등록 | 대부분의 자동화 기능 |
| DockPanePlugin | 패널(사이드바) | 지속 표시 UI |
| ImporterPlugin | 파일 임포터 | 커스텀 포맷 지원 |

```csharp
// AddInPlugin 진입점
[AddInPlugin(DisplayName = "Auto SearchSet", ToolTip = "...")]
public class AutoSearchSetPlugin : AddInPlugin
{
    public override int Execute(params string[] parameters)
    {
        var doc = Autodesk.Navisworks.Api.Application.ActiveDocument;
        // 로직 실행
        return 0;
    }
}
```

---

## 3. Clash Detective API

### 3-1. ClashTest 생성 및 실행

```csharp
var clashState = doc.GetClash();
var tests = clashState.TestsData;

// 새 ClashTest 생성
var test = tests.CreateClash();
test.DisplayName = "MEP vs 구조";
test.Run();
tests.Update(test);
```

### 3-2. 결과 접근

```csharp
foreach (ClashResult result in test.ResultData.ClashResults)
{
    string status = result.Status.ToString();   // Active, Reviewed, Approved
    double distance = result.Distance;          // 미터 단위
    var pt1 = result.Point1;                    // 충돌 좌표 1
    var pt2 = result.Point2;                    // 충돌 좌표 2
    string desc = result.Description;
}
```

### 3-3. Clash 결과 → CSV/Excel 내보내기

Navisworks 내장 보고서보다 커스텀 필드 추가가 용이하다.

```csharp
var sb = new StringBuilder();
sb.AppendLine("ID,상태,거리(mm),공종A,공종B,레벨,구역");

foreach (ClashResult result in test.ResultData.ClashResults)
{
    double distMm = result.Distance * 1000;
    var itemA = result.CompositeItem1;
    var itemB = result.CompositeItem2;

    string discA = ExtractDiscipline(itemA);
    string discB = ExtractDiscipline(itemB);

    sb.AppendLine($"{result.DisplayName},{result.Status},{distMm:F1},{discA},{discB}");
}
File.WriteAllText(outputPath, sb.ToString(), Encoding.UTF8);
```

---

## 4. ModelItem 순회 및 속성 접근

```csharp
// 모든 ModelItem 순회
void WalkItems(ModelItemCollection items)
{
    foreach (ModelItem item in items)
    {
        string name = item.DisplayName;
        string guid = item.InstanceGuid.ToString();

        // 속성 접근
        foreach (PropertyCategory cat in item.PropertyCategories)
        {
            foreach (DataProperty prop in cat.Properties)
            {
                string propName = prop.DisplayName;
                var value = prop.Value;
            }
        }

        if (item.HasChildren)
            WalkItems(item.Children);
    }
}
```

---

## 5. SearchSet (자동 검색세트)

### 5-1. 조건 기반 SearchSet 생성

```csharp
var search = new Search();
search.SearchConditions.Add(
    SearchCondition.HasPropertyByDisplayName(
        "Element", "Category",
        SearchConditionOptions.None,
        VariantData.FromDisplayString("Pipes")
    )
);
var result = search.FindAll(doc, false);

// SearchSet 저장
var savedSet = new SelectionSet(result);
savedSet.DisplayName = "배관 전체";
doc.CurrentSelection.SelectionSets.Add(savedSet);
```

---

## 6. 제품화 기준 (Auto SearchSet)

| 항목 | 기준 |
|---|---|
| 지원 버전 | Navisworks Manage 2024, 2025, 2026 |
| 플러그인 등록 | `%APPDATA%\Autodesk\Navisworks Manage YYYY\Plugins\` |
| 매니페스트 | .NET Assembly + `package.xml` |
| 테스트 파일 | 샘플 NWD/NWC 기준 검증 |
| 가격 | 구독 모델 (Revit 번들 검토) |

---

## 7. Clash XML → Excel 파이프라인 연결

Navisworks Clash Detective XML 내보내기 → Python으로 파싱 → Excel 리포트:
- `엑셀자동화 - BIM 리포트 자동화` 문서 참조
- `parse_clash_xml()` + `build_clash_report()` 함수 완성형 제공

---

## 연결

- [[지식맵 - Revit API 개발]]
- [[지식맵 - BIM 실무 표준]]
- [[엑셀자동화 - BIM 리포트 자동화]]
- [[Global Knowledge Map]]
