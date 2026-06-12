---
type: knowledge-note
domain: 엑셀자동화
sub: openpyxl
date: 2026-05-22
tags: [엑셀자동화, openpyxl, Python, 심화]
---

# 엑셀 자동화 — openpyxl 심화 패턴

---

## 1. 차트 자동 생성

### 막대 차트 (월별 비용/물량 보고)
```python
from openpyxl.chart import BarChart, Reference

chart = BarChart()
chart.type = "col"
chart.title = "월별 간섭 건수"
chart.y_axis.title = "건수"
chart.x_axis.title = "월"
chart.style = 10

data = Reference(ws, min_col=2, min_row=1, max_col=ws.max_column, max_row=ws.max_row)
cats = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
chart.shape = 4
ws.add_chart(chart, "A20")
```

### 꺾은선 차트 (KPI 추이)
```python
from openpyxl.chart import LineChart, Reference

chart = LineChart()
chart.title = "누적 조치율"
chart.style = 13
chart.y_axis.numFmt = '0%'
chart.y_axis.title = "조치율"

data = Reference(ws, min_col=3, min_row=1, max_row=ws.max_row)
chart.add_data(data, titles_from_data=True)
chart.y_axis.crossAx = 500
chart.x_axis.crossAx = 100
ws.add_chart(chart, "E5")
```

### 원형 차트 (공종별 비율)
```python
from openpyxl.chart import PieChart, Reference

pie = PieChart()
labels = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
data = Reference(ws, min_col=2, min_row=1, max_row=ws.max_row)
pie.add_data(data, titles_from_data=True)
pie.set_categories(labels)
pie.title = "공종별 간섭 비율"
pie.style = 10
ws.add_chart(pie, "C1")
```

---

## 2. 데이터 유효성 검사 (드롭다운)

```python
from openpyxl.worksheet.datavalidation import DataValidation

# 드롭다운 목록
dv = DataValidation(
    type="list",
    formula1='"신규,검토중,조치완료,보류,제외"',
    allow_blank=True,
    showErrorMessage=True,
    errorTitle="입력 오류",
    error="목록에서 선택하세요."
)
ws.add_data_validation(dv)
dv.add("G2:G1000")  # 상태 컬럼 전체

# 숫자 범위 유효성
dv_num = DataValidation(
    type="whole",
    operator="between",
    formula1=0,
    formula2=9999,
    errorTitle="범위 초과",
    error="0~9999 사이 정수를 입력하세요."
)
ws.add_data_validation(dv_num)
dv_num.add("F2:F1000")  # 간섭거리 컬럼
```

---

## 3. 고급 조건부 서식

```python
from openpyxl.styles import PatternFill, Font
from openpyxl.formatting.rule import ColorScaleRule, DataBarRule, CellIsRule, FormulaRule

# 3색 컬러스케일 (열지도)
ws.conditional_formatting.add(
    "F2:F500",
    ColorScaleRule(
        start_type="min", start_color="63BE7B",   # 낮음 → 초록
        mid_type="percentile", mid_value=50, mid_color="FFEB84",  # 중간 → 노랑
        end_type="max", end_color="F8696B",        # 높음 → 빨강
    )
)

# 데이터 막대
ws.conditional_formatting.add(
    "C2:C500",
    DataBarRule(start_type="min", end_type="max", color="638EC6")
)

# 수식 기반 행 강조 (상태가 "긴급"인 경우 행 전체 빨강)
red_fill = PatternFill(fill_type="solid", fgColor="FF9999")
ws.conditional_formatting.add(
    f"A2:J500",
    FormulaRule(formula=["$H2=\"긴급\""], fill=red_fill)
)

# D-30 이내 만료일 강조 (라이선스 관리)
yellow_fill = PatternFill(fill_type="solid", fgColor="FFFF00")
ws.conditional_formatting.add(
    "D2:D200",
    FormulaRule(formula=["AND(D2-TODAY()<=30, D2-TODAY()>=0)"], fill=yellow_fill)
)
```

---

## 4. 셀 서식 고급

```python
from openpyxl.styles import (
    Font, Alignment, Border, Side, PatternFill, numbers
)

# 헤더 스타일 완성형
def apply_header_style(ws, row=1):
    header_fill = PatternFill(fill_type="solid", fgColor="1F4E79")
    header_font = Font(bold=True, color="FFFFFF", size=11, name="맑은 고딕")
    header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin = Side(style="thin", color="FFFFFF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for cell in ws[row]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_align
        cell.border = border
    ws.row_dimensions[row].height = 30

# 열 너비 자동 조정
def auto_fit_columns(ws, min_width=8, max_width=50):
    for col in ws.columns:
        max_len = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = min(max(max_len + 2, min_width), max_width)

# 숫자 서식
ws["C2"].number_format = "#,##0"          # 천 단위 콤마
ws["D2"].number_format = "#,##0.00"       # 소수점 2자리
ws["E2"].number_format = "0.00%"          # 백분율
ws["F2"].number_format = "YYYY-MM-DD"     # 날짜
ws["G2"].number_format = "#,##0\"원\""   # 원화
```

---

## 5. 인쇄 설정

```python
from openpyxl.worksheet.page import PageMargins

# 인쇄 영역
ws.print_area = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"

# 페이지 설정
ws.page_setup.orientation = "landscape"     # 가로
ws.page_setup.paperSize = 9                 # A4
ws.page_setup.fitToPage = True
ws.page_setup.fitToWidth = 1                # 1페이지 너비에 맞춤
ws.page_setup.fitToHeight = 0

# 여백 (인치 단위)
ws.page_margins = PageMargins(
    left=0.5, right=0.5, top=0.75, bottom=0.75,
    header=0.3, footer=0.3
)

# 인쇄 제목 (행 반복)
ws.print_title_rows = "1:1"

# 머리글/바닥글
ws.oddHeader.center.text = "LUA BIM LABS — 내부 보고서"
ws.oddFooter.right.text = "페이지 &P / &N"
ws.oddFooter.left.text = "&D"
```

---

## 6. 하이퍼링크 및 이미지

```python
from openpyxl.drawing.image import Image

# 시트 간 하이퍼링크
ws["A2"].hyperlink = "#요약!A1"
ws["A2"].style = "Hyperlink"

# URL 하이퍼링크
ws["B2"].hyperlink = "https://docs.autodesk.com"
ws["B2"].value = "Autodesk Docs"
ws["B2"].style = "Hyperlink"

# 로고 이미지 삽입
img = Image("logo.png")
img.width = 120
img.height = 40
img.anchor = "A1"
ws.add_image(img)
```

---

## 7. 비밀번호 보호 및 셀 잠금

```python
# 시트 보호 (편집 방지)
ws.protection.sheet = True
ws.protection.password = "lbl2026"
ws.protection.enable()

# 특정 셀만 편집 허용 (보호 해제)
from openpyxl.styles.protection import Protection
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=7, max_col=9):
    for cell in row:
        cell.protection = Protection(locked=False)  # 상태·담당자·비고만 편집 가능
```

---

## 8. 명명된 범위 (Named Range)

```python
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.utils import quote_sheetname, absolute_coordinate

# 합계 공식용 명명된 범위
defn = DefinedName(
    name="간섭합계",
    attr_text=f"{quote_sheetname(ws.title)}!{absolute_coordinate('C2')}:{absolute_coordinate(f'C{ws.max_row}')}"
)
wb.defined_names["간섭합계"] = defn

# 다른 시트에서 참조
ws2["B1"] = "=SUM(간섭합계)"
```

---

## 9. 수식 삽입

```python
# 기본 합계
ws.append(["합계", f"=SUM(B2:B{ws.max_row-1})", f"=SUM(C2:C{ws.max_row-1})"])

# 조건부 합계
last = ws.max_row
ws[f"D{last+1}"] = f'=COUNTIF(G2:G{last},"조치완료")'
ws[f"E{last+1}"] = f'=IFERROR(D{last+1}/COUNTA(G2:G{last}),0)'
ws[f"E{last+1}"].number_format = "0.0%"

# VLOOKUP 수식
ws["H2"] = '=IFERROR(VLOOKUP(A2,담당자목록!A:B,2,FALSE),"미지정")'
```

---

## 10. 멀티 시트 워크북 완성형 예시

```python
def build_workbook(data_by_discipline: dict, output_path: str) -> None:
    wb = Workbook()
    wb.remove(wb.active)  # 기본 시트 제거

    # 요약 시트 먼저
    ws_summary = wb.create_sheet("요약", 0)
    ws_summary.append(["공종", "전체", "신규", "조치완료", "조치율"])
    apply_header_style(ws_summary)

    for disc, rows in sorted(data_by_discipline.items()):
        ws = wb.create_sheet(disc[:31])
        headers = ["번호", "공종A", "공종B", "레벨", "간섭거리", "우선순위", "상태", "담당자", "조치기한"]
        ws.append(headers)
        apply_header_style(ws)
        for i, row in enumerate(rows, 2):
            ws.append(row)
        ws.freeze_panes = "A2"
        auto_fit_columns(ws)

        total = len(rows)
        done = sum(1 for r in rows if r[6] == "조치완료")
        ws_summary.append([disc, total, total - done, done, done / total if total else 0])

    # 요약 서식
    ws_summary.freeze_panes = "A2"
    auto_fit_columns(ws_summary)
    last = ws_summary.max_row
    ws_summary[f"E{last}"].number_format = "0.0%"

    wb.save(output_path)
    print(f"저장 완료: {output_path}")
```

---

## 연결

- [[지식맵 - 엑셀 자동화]]
- [[엑셀자동화 - BIM 리포트 자동화]]
- [[엑셀자동화 - 관리팀 업무 템플릿]]
- [[엑셀자동화 - 에러처리와 검증]]
- [[Global Knowledge Map]]
