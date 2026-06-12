---
type: knowledge-note
domain: 엑셀자동화
sub: pandas
date: 2026-05-22
tags: [엑셀자동화, pandas, openpyxl, pivot, 집계, Python]
---

# 엑셀 자동화 — pandas 집계 자동화

> **사용 조건**: `pivot_table`, `groupby` 등 집계가 반드시 필요한 경우에만. 그 외에는 `csv + openpyxl` 기본값 사용.
> `pandas`로 xlsx 저장 시 반드시 `engine='openpyxl'` 명시.

---

## 1. pandas + openpyxl 기본 세팅

```python
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter

# xlsx 저장 — engine 명시 필수
df.to_excel("output.xlsx", index=False, engine="openpyxl")

# ExcelWriter로 시트 제어
with pd.ExcelWriter("output.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="데이터", index=False)
    pivot.to_excel(writer, sheet_name="피벗", index=True)
```

---

## 2. 간섭 데이터 pivot_table

### 공종별 × 상태별 교차 집계

```python
import pandas as pd

def clash_pivot_report(df: pd.DataFrame, output_path: str) -> None:
    """
    df 컬럼: 공종A, 공종B, 레벨, 간섭거리(mm), 우선순위, 상태, 담당자, 조치기한
    """
    # 공종 조합 컬럼
    df["공종조합"] = df["공종A"] + " ↔ " + df["공종B"]

    # 상태별 건수 피벗
    pivot_status = df.pivot_table(
        index="공종조합",
        columns="상태",
        values="간섭거리(mm)",
        aggfunc="count",
        fill_value=0,
        margins=True,
        margins_name="합계",
    )

    # 우선순위별 평균 간섭거리
    pivot_dist = df.groupby(["공종조합", "우선순위"])["간섭거리(mm)"].agg(
        건수="count", 평균거리="mean", 최대거리="max"
    ).round(1)

    # 레벨별 집계
    pivot_level = df.pivot_table(
        index="레벨",
        columns="우선순위",
        values="간섭거리(mm)",
        aggfunc="count",
        fill_value=0,
    )

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="원본", index=False)
        pivot_status.to_excel(writer, sheet_name="상태별집계")
        pivot_dist.to_excel(writer, sheet_name="공종별집계")
        pivot_level.to_excel(writer, sheet_name="레벨별집계")

    # 서식 후처리
    _post_format(output_path, sheet_styles={
        "원본": {"header_color": "1F4E79"},
        "상태별집계": {"header_color": "2E4057"},
        "공종별집계": {"header_color": "2E4057"},
        "레벨별집계": {"header_color": "2E4057"},
    })
```

### 월별 추이 집계

```python
def monthly_clash_trend(df: pd.DataFrame) -> pd.DataFrame:
    """조치기한 기준 월별 건수/조치완료 건수 추이"""
    df["조치기한"] = pd.to_datetime(df["조치기한"], errors="coerce")
    df["월"] = df["조치기한"].dt.to_period("M").astype(str)

    trend = df.groupby("월").agg(
        전체=("상태", "count"),
        조치완료=("상태", lambda s: (s == "조치완료").sum()),
    )
    trend["조치율"] = (trend["조치완료"] / trend["전체"]).round(3)
    return trend.reset_index()
```

---

## 3. 비용 정산 groupby 집계

```python
def expense_summary(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    df 컬럼: 날짜, 항목, 금액, 내용, 담당자, 승인여부
    """
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df["월"] = df["날짜"].dt.to_period("M").astype(str)

    # 항목별 합계
    by_category = df.groupby("항목")["금액"].agg(
        건수="count", 합계="sum", 평균="mean"
    ).round(0).reset_index()

    # 월별 항목별 피벗
    monthly_pivot = df.pivot_table(
        index="월", columns="항목", values="금액",
        aggfunc="sum", fill_value=0, margins=True, margins_name="합계"
    )

    # 담당자별 합계
    by_person = df.groupby("담당자")["금액"].sum().sort_values(ascending=False).reset_index()
    by_person.columns = ["담당자", "합계(원)"]

    # 미승인 건 필터
    pending = df[df["승인여부"] == "대기"][["날짜", "항목", "금액", "내용", "담당자"]]

    return {
        "항목별": by_category,
        "월별피벗": monthly_pivot,
        "담당자별": by_person,
        "미승인": pending,
    }


def build_expense_pivot_excel(df: pd.DataFrame, output_path: str, month: str) -> None:
    summaries = expense_summary(df)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="원본", index=False)
        for sheet_name, frame in summaries.items():
            frame.to_excel(writer, sheet_name=sheet_name, index=True)

    _post_format(output_path, sheet_styles={k: {"header_color": "1F4E79"} for k in ["원본"] + list(summaries)})
```

---

## 4. 물량 산출 집계

```python
def quantity_rollup(df: pd.DataFrame, group_cols: list[str], value_cols: list[str]) -> pd.DataFrame:
    """
    Revit Schedule 데이터 계층적 집계
    group_cols: ["패밀리", "유형", "레벨"]
    value_cols: ["수량", "길이", "면적"]
    """
    agg_dict = {col: "sum" for col in value_cols if col in df.columns}
    result = df.groupby(group_cols).agg(agg_dict).reset_index()

    # 소계 추가 (상위 그룹)
    if len(group_cols) > 1:
        subtotal = df.groupby(group_cols[:-1]).agg(agg_dict).reset_index()
        subtotal[group_cols[-1]] = "소계"
        result = pd.concat([result, subtotal], ignore_index=True)
        result = result.sort_values(group_cols).reset_index(drop=True)

    return result


def build_quantity_pivot_excel(df: pd.DataFrame, output_path: str) -> None:
    rollup = quantity_rollup(
        df,
        group_cols=["패밀리", "유형", "레벨"],
        value_cols=["수량", "길이", "면적", "체적"],
    )
    pivot = df.pivot_table(
        index=["패밀리", "유형"],
        columns="레벨",
        values="수량",
        aggfunc="sum",
        fill_value=0,
        margins=True,
        margins_name="합계",
    )

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="원본", index=False)
        rollup.to_excel(writer, sheet_name="계층집계", index=False)
        pivot.to_excel(writer, sheet_name="레벨별피벗")

    _post_format(output_path, sheet_styles={
        "원본": {"header_color": "1F4E79"},
        "계층집계": {"header_color": "2E4057"},
        "레벨별피벗": {"header_color": "2E4057"},
    })
```

---

## 5. ExcelWriter 멀티시트 + 서식 후처리

```python
def _post_format(path: str, sheet_styles: dict[str, dict]) -> None:
    """pandas ExcelWriter 저장 후 openpyxl로 서식 적용"""
    wb = load_workbook(path)
    for sheet_name, style in sheet_styles.items():
        if sheet_name not in wb.sheetnames:
            continue
        ws = wb[sheet_name]
        header_color = style.get("header_color", "1F4E79")
        _apply_header_style(ws, row=1, color=header_color)
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        _auto_fit_columns(ws)
    wb.save(path)


def _apply_header_style(ws, row: int = 1, color: str = "1F4E79") -> None:
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
    fill = PatternFill(fill_type="solid", fgColor=color)
    font = Font(bold=True, color="FFFFFF", size=11, name="맑은 고딕")
    align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin = Side(style="thin", color="FFFFFF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for cell in ws[row]:
        cell.fill = fill
        cell.font = font
        cell.alignment = align
        cell.border = border
    ws.row_dimensions[row].height = 30


def _auto_fit_columns(ws, min_w: int = 8, max_w: int = 40) -> None:
    for col in ws.columns:
        letter = col[0].column_letter
        max_len = max((len(str(c.value)) for c in col if c.value), default=0)
        ws.column_dimensions[letter].width = min(max(max_len + 2, min_w), max_w)
```

---

## 6. pandas DataFrame → Excel 변환 완성형

```python
def df_to_excel(
    frames: dict[str, pd.DataFrame],
    output_path: str,
    index: bool = False,
) -> None:
    """
    frames: {"시트명": DataFrame}
    여러 DataFrame을 멀티시트 xlsx로 저장 + 서식
    """
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, df in frames.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=index)

    _post_format(output_path, {name: {"header_color": "1F4E79"} for name in frames})
```

---

## 7. 주의사항

| 항목 | 내용 |
|---|---|
| engine 명시 | `to_excel(..., engine='openpyxl')` 반드시 |
| 날짜 타입 | `pd.to_datetime()` 후 `.dt.strftime()` 또는 그대로 저장 |
| 숫자형 문자 | CSV 읽기 시 `dtype=str` → 후처리로 변환 (자동 변환 실수 방지) |
| 메모리 | 10만 행 이상 → `chunksize` 또는 write_only 모드로 전환 |
| NaN | `df.fillna("")` 후 저장 (엑셀에서 `None` → 빈 셀 자동 처리됨) |

---

## 연결

- [[지식맵 - 엑셀 자동화]]
- [[엑셀자동화 - openpyxl 심화 패턴]]
- [[엑셀자동화 - BIM 리포트 자동화]]
- [[엑셀자동화 - 에러처리와 검증]]
- [[Global Knowledge Map]]
